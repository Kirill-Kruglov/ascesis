"""Experiment 18.1 Level B scaffolding.

Level B (does training inside the shield help?) only runs if Level A passes.
Because Level A is a kill gate, this module provides only the pieces needed to
(a) guarantee EQUAL data volumes for the shielded vs control learners — the
confound the task forbids — and (b) be unit-tested. The full trainer is NOT
executed when Level A fails; running it behind a lying shield "proves nothing".
"""
from __future__ import annotations

import random


def equal_volume_datasets(safe_states: list, all_states: list, seed: int = 42):
    """Build a shielded dataset (SAFE-only) and a control dataset (unfiltered) of
    EXACTLY equal size, so "safer" can never be confounded with "more/less data".

    n = min(#safe, #all) so both can be sampled to the same volume. Returns
    (shielded, control, n). Deterministic given seed.
    """
    rng = random.Random(seed)
    n = min(len(safe_states), len(all_states))
    shielded = rng.sample(safe_states, n) if len(safe_states) > n else list(safe_states)
    control = rng.sample(all_states, n) if len(all_states) > n else list(all_states)
    assert len(shielded) == len(control) == n, "equal-volume guarantee violated"
    return shielded, control, n
