from __future__ import annotations

import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def ensure_output_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    pd.DataFrame(rows).to_csv(path, index=False)


def save_line_plot(path: Path, rows: list[dict[str, object]], x: str, ys: list[str], title: str) -> None:
    frame = pd.DataFrame(rows)
    plt.figure(figsize=(7, 4))
    for y in ys:
        if y in frame:
            plt.plot(frame[x], frame[y], marker="o", label=y)
    plt.title(title)
    plt.xlabel(x)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def possible_world_upper_bound(num_valid_facts: int, max_facts: int) -> int:
    total = 0
    for k in range(max_facts + 1):
        total += math.comb(num_valid_facts, min(k, num_valid_facts))
    return total
