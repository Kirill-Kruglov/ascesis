#!/usr/bin/env python3
"""dialog2md — convert a saved Claude / ChatGPT conversation page to Markdown.

The forge's raw material was dialogue; this is the harvester for its primary
sources. Feed it an HTML file saved from the browser (full page or the
conversation container) and it emits clean Markdown, preserving code fences,
lists, and quotes — or splits the dialog into one file per exchange.

    python3 dialog2md.py saved_page.html out.md
    python3 dialog2md.py saved_page.html out --split-dir parts/

Design choices:
  - DOM-based, not text-based: messages are located by stable-ish data
    attributes (Claude: data-testid="user-message" inside per-message render
    containers; ChatGPT: data-message-author-role), so accessibility strings
    like "You said:" are stripped rather than relied upon.
  - File input only. Share-page URLs render client-side and fetching them adds
    fragility and a temptation to over-share; save the page, then convert.
    (Creating a share link publishes the conversation to anyone with the URL —
    do that only for dialogs you have reviewed.)
  - Raw converted dialogs are working material; review before committing any
    of them to a public repository.

Requires: beautifulsoup4.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

# --------------------------------------------------------------------------- #
# HTML -> Markdown (small, dependency-free, code-fence-preserving)
# --------------------------------------------------------------------------- #
BLOCK = {"p", "div", "section", "article", "ul", "ol", "li", "pre", "blockquote",
         "h1", "h2", "h3", "h4", "h5", "h6", "table", "tr", "br", "hr"}


def _code_lang(pre: Tag) -> str:
    for el in [pre] + pre.find_all("code"):
        for cls in (el.get("class") or []):
            m = re.match(r"language-([\w+-]+)", cls)
            if m:
                return m.group(1)
    return ""


def _render(node, indent: str = "") -> str:
    if isinstance(node, NavigableString):
        return re.sub(r"\s+", " ", str(node))
    if not isinstance(node, Tag):
        return ""
    name = node.name
    if name in ("script", "style", "svg", "button"):
        return ""
    if name == "br":
        return "\n"
    if name == "hr":
        return "\n\n---\n\n"
    if name == "pre":
        code = node.get_text()
        fence = "````" if "```" in code else "```"
        return f"\n\n{fence}{_code_lang(node)}\n{code.rstrip()}\n{fence}\n\n"
    if name == "code":  # inline
        text = node.get_text()
        return f"`{text}`" if "\n" not in text else _render_children(node, indent)
    if name in ("strong", "b"):
        return f"**{_render_children(node, indent).strip()}**"
    if name in ("em", "i"):
        inner = _render_children(node, indent).strip()
        return f"*{inner}*" if inner else ""
    if name == "a":
        text = _render_children(node, indent).strip()
        href = node.get("href", "")
        return f"[{text}]({href})" if href and text and href != text else text or href
    if re.fullmatch(r"h[1-6]", name):
        level = int(name[1])
        return f"\n\n{'#' * (level + 1)} {_render_children(node, indent).strip()}\n\n"
    if name == "blockquote":
        inner = _render_children(node, indent).strip()
        quoted = "\n".join("> " + line for line in inner.splitlines())
        return f"\n\n{quoted}\n\n"
    if name in ("ul", "ol"):
        out = ["\n"]
        idx = 1
        for li in node.find_all("li", recursive=False):
            marker = f"{idx}." if name == "ol" else "-"
            body = _render_children(li, indent + "  ").strip()
            body = body.replace("\n", "\n" + indent + "  ")
            out.append(f"{indent}{marker} {body}\n")
            idx += 1
        return "".join(out) + "\n"
    if name == "table":
        rows = []
        for tr in node.find_all("tr"):
            cells = [re.sub(r"\s+", " ", td.get_text()).strip()
                     for td in tr.find_all(["td", "th"])]
            rows.append("| " + " | ".join(cells) + " |")
        if len(rows) > 1:
            rows.insert(1, "|" + "---|" * rows[0].count("|", 1))
        return "\n\n" + "\n".join(rows) + "\n\n"
    inner = _render_children(node, indent)
    if name in BLOCK:
        return f"\n\n{inner.strip()}\n\n" if inner.strip() else ""
    return inner


def _render_children(node: Tag, indent: str = "") -> str:
    return "".join(_render(child, indent) for child in node.children)


def to_markdown(container: Tag) -> str:
    md = _render_children(container)
    md = re.sub(r"[ \t]+\n", "\n", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip()


# --------------------------------------------------------------------------- #
# Adapters: locate (role, message-container) pairs
# --------------------------------------------------------------------------- #
def _messages_claude(soup: BeautifulSoup):
    containers = soup.select("div[data-test-render-count]")
    for c in containers:
        role = "user" if c.find(attrs={"data-testid": "user-message"}) else "assistant"
        yield role, c


def _messages_chatgpt(soup: BeautifulSoup):
    for c in soup.select("[data-message-author-role]"):
        yield c["data-message-author-role"], c


def detect_messages(soup: BeautifulSoup):
    if soup.find(attrs={"data-message-author-role": True}):
        return "chatgpt", list(_messages_chatgpt(soup))
    if soup.find(attrs={"data-test-render-count": True}):
        return "claude", list(_messages_claude(soup))
    raise SystemExit(
        "error: no recognizable message containers "
        "(expected Claude data-test-render-count or ChatGPT data-message-author-role); "
        "the page layout may have changed — save the full conversation DOM and retry"
    )


SR_NOISE = re.compile(r"^\s*(You said:|ChatGPT said:|Claude said:)\s*", re.IGNORECASE)


def convert(html: str, user_label: str, assistant_label: str):
    soup = BeautifulSoup(html, "html.parser")
    flavor, messages = detect_messages(soup)
    if not messages:
        raise SystemExit("error: message containers matched but none found")
    turns = []
    for role, container in messages:
        md = to_markdown(container)
        md = SR_NOISE.sub("", md)
        if md:
            label = user_label if role == "user" else assistant_label
            turns.append((role, f"# {label}\n\n{md}\n"))
    return flavor, turns


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("html", help="saved conversation page (.html)")
    ap.add_argument("out", help="output .md file, or basename when using --split-dir")
    ap.add_argument("--split-dir", help="write one .md per exchange into this directory")
    ap.add_argument("--user-label", default="Kirill")
    ap.add_argument("--assistant-label", default=None,
                    help="default: Claude or GPT, by detected flavor")
    args = ap.parse_args()

    html = Path(args.html).read_text(encoding="utf-8", errors="replace")
    flavor, turns = convert(html, args.user_label, args.assistant_label or "?")
    assistant = args.assistant_label or ("Claude" if flavor == "claude" else "GPT")
    turns = [(r, t.replace("# ?\n", f"# {assistant}\n", 1) if r != "user" else t)
             for r, t in turns]

    if args.split_dir:
        outdir = Path(args.split_dir)
        outdir.mkdir(parents=True, exist_ok=True)
        part, n = [], 0
        for role, text in turns:
            if role == "user" and part:
                (outdir / f"{args.out}.part_{n:03d}.md").write_text(
                    "\n".join(part), encoding="utf-8")
                part, n = [], n + 1
            part.append(text)
        if part:
            (outdir / f"{args.out}.part_{n:03d}.md").write_text(
                "\n".join(part), encoding="utf-8")
        print(f"{flavor}: {len(turns)} messages -> {n + 1} parts in {outdir}/")
    else:
        Path(args.out).write_text("\n".join(t for _, t in turns), encoding="utf-8")
        print(f"{flavor}: {len(turns)} messages -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
