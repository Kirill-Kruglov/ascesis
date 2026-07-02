#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

try:
    from tqdm import tqdm
except Exception:  # pragma: no cover
    def tqdm(iterable, **_: object):
        return iterable

from worldcore.canonical import canonical_world_hash
from worldcore.experiments import ensure_output_dir, possible_world_upper_bound, save_line_plot, write_csv, write_json
from worldcore.generator import generate_entities, generate_random_world, make_rng, valid_assignments
from worldcore.metrics import collision_fraction, saturation_curve, uniqueness_ratio
from worldcore.types import PREDICATES, TYPES


CONFIGS = {
    "small": {"num_entities": 8, "max_facts": 12, "samples": 2_000},
    "medium": {"num_entities": 12, "max_facts": 18, "samples": 5_000},
}


def _expected_unique(samples: int, state_bound: int) -> float:
    if state_bound <= 0:
        return 0.0
    if state_bound > 10**12:
        return float(samples)
    return state_bound * (1.0 - ((state_bound - 1) / state_bound) ** samples)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="small", choices=CONFIGS)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--outputs", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    cfg = CONFIGS[args.config]
    rng = make_rng(args.seed)
    out = ensure_output_dir(args.outputs)

    template_entities = generate_entities(make_rng(args.seed), cfg["num_entities"])
    valid_fact_count = sum(len(valid_assignments(template_entities, spec)) for spec in PREDICATES)
    typed_entity_assignments = len(TYPES) ** cfg["num_entities"]
    upper_bound = possible_world_upper_bound(valid_fact_count, cfg["max_facts"])

    hashes = []
    for idx in tqdm(range(cfg["samples"]), desc="sampling worlds"):
        world = generate_random_world(rng, f"capacity_{idx}", cfg["num_entities"], cfg["max_facts"], entity_prefix=f"cap{idx}_")
        hashes.append(canonical_world_hash(world))

    checkpoints = sorted(set([10, 25, 50, 100, 250, 500, 1_000, cfg["samples"]]))
    checkpoints = [point for point in checkpoints if point <= cfg["samples"]]
    curve = saturation_curve(hashes, checkpoints)
    for row in curve:
        row["expected_unique_uniform_bound"] = _expected_unique(int(row["samples"]), upper_bound)
        row["canonical_collisions"] = int(row["samples"] - row["unique"])
    summary = {
        "config": args.config,
        "seed": args.seed,
        "num_entities": cfg["num_entities"],
        "max_facts": cfg["max_facts"],
        "typed_entity_assignments": typed_entity_assignments,
        "possible_valid_facts": valid_fact_count,
        "world_state_upper_bound": str(upper_bound),
        "sampled_worlds": len(hashes),
        "unique_canonical_worlds": len(set(hashes)),
        "uniqueness_ratio": uniqueness_ratio(hashes),
        "collision_fraction": collision_fraction(hashes),
        "canonical_collisions": len(hashes) - len(set(hashes)),
        "expected_unique_at_sample_count": _expected_unique(len(hashes), upper_bound),
        "saturates_early": len(set(hashes[: min(250, len(hashes))])) < min(125, len(hashes)),
    }

    write_json(out / "capacity_summary.json", summary)
    write_csv(out / "capacity_curve.csv", curve)
    save_line_plot(out / "capacity_curve.png", curve, "samples", ["unique", "expected_unique_uniform_bound"], "Capacity saturation curve")
    save_line_plot(out / "capacity_diagnostics.png", curve, "samples", ["uniqueness_ratio", "collision_fraction"], "Capacity diagnostics")


if __name__ == "__main__":
    main()
