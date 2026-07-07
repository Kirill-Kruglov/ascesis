# dialog2md

Convert a saved Claude / ChatGPT conversation page into clean Markdown. The
forge's raw material was dialogue; this is the harvester for its primary
sources.

```sh
python3 dialog2md.py saved_page.html out.md --user-label Kirill                 # single file
python3 dialog2md.py saved_page.html base --user-label Kirill --split-dir parts # one file per exchange
```

Requires `beautifulsoup4`. `--user-label` (required) names your turns;
`--assistant-label` defaults to `Claude`/`GPT` by detected flavor.

## How it works

DOM-based, not text-based: messages are located by data attributes
(Claude: per-message render containers + `data-testid="user-message"`;
ChatGPT: `data-message-author-role`), then each message's HTML is converted to
Markdown with code fences, lists, quotes, tables, and links preserved.
Accessibility strings like "You said:" are stripped, never relied upon.

## Deliberate limits

- **File input only.** Share pages render client-side; fetching URLs adds
  fragility and a temptation to over-share. Save the page from the browser,
  then convert. Remember: *creating* a share link publishes the conversation to
  anyone holding the URL — do that only for dialogs you have reviewed.
- **Raw dialogs are working material.** Review before committing any converted
  dialog to a public repository; they contain unedited thinking.
- Layout drift will break the selectors eventually; when it does, the fix is
  the adapter functions at the bottom of the script, nothing else.

## Known rough edges

- UI chrome that sits inside a message container (timestamps, retry buttons)
  can occasionally leak into output — grep for stray short lines after
  conversion.
- Nested code fences inside list items may lose a newline; verified counts on a
  1.4 MB real dialog: 132/132 messages, 41/41 fences emitted.
