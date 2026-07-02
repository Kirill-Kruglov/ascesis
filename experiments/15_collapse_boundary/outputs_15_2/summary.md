# Experiment 15.2 — Enumeration to Exhaustion (System C)

Mode: `full`. Semantic caps: [6, 8, 10, 12, 14, 16, 18]. Obs depths: [8, 12, 16]. State-BFS caps: [4, 5, 6] (budget 200000).

**Verdict: `open_candidate`.**

N_semantic(cap) grows exponentially (per-cap multiplier ~constant > 1) and EVERY point is exactly exhausted (no budget). By the scaling-law criterion this is the first semantic-OPEN candidate on the project's path: each depth level adds classes multiplicatively, a property of structure, not of how hard we looked.

## 1. Which caps were genuinely exhausted vs censored?

| instrument | cap | exhausted | censored | N_semantic | nodes/states | layers |
|---|---|---|---|---|---|---|
| state_bfs | 4 | True | False | 4 | 25 | 6 |
| state_bfs | 5 | True | False | 8 | 676 | 12 |
| state_bfs | 6 | False | True | 16 | 200000 | 15 |
| exact_semantic | 6 | True | False | 16 | 46 | 5 |
| exact_semantic | 8 | True | False | 64 | 190 | 7 |
| exact_semantic | 10 | True | False | 256 | 766 | 9 |
| exact_semantic | 12 | True | False | 1024 | 3070 | 11 |
| exact_semantic | 14 | True | False | 4096 | 12286 | 13 |
| exact_semantic | 16 | True | False | 16384 | 49150 | 15 |
| exact_semantic | 18 | True | False | 65536 | 196606 | 17 |

The prescribed full reachable-state BFS **censors at cap≥6**: System C's reachable *state* space is doubly-exponential in the cap (a blow-up of syntactic intermediate F-trees), so it hits the node budget while the semantic space is tiny (16 at cap=6). Under the literal instrument the honest verdict would be `inconclusive_all_censored`. Raising the budget cannot help — the correct fix is exact semantic enumeration, which exhausts the meaning space with no budget at all.

## 2. Per-layer multiplier — does it stay >1 or decay to 1?

Per-cap multiplier (across caps): mean = **2**, trend = -4.398e-17 (≈0 ⇒ constant). A constant multiplier >1 is the fingerprint of multiplicative (exponential) growth; decay toward 1 would indicate bounded/polynomial. Per-layer curves (within each cap) are in `per_level_multiplier_vs_layer.png` and stay ≈2 until the frontier empties (exhaustion).

## 3. Which functional form fits the uncensored N(cap) best?

| form | params | R² (on raw counts) |
|---|---|---|
| exponential a·b^cap | a=0.25, b=2 | 1.000000 |
| polynomial a·cap^k | a=1.179e-05, k=7.545 | 0.727974 |
| bounded a−b·r^cap | a=1.726e+08, r=1 | 0.555609 |

Best by R²: **exponential**. Uncensored points: [(6, 16), (8, 64), (10, 256), (12, 1024), (14, 4096), (16, 16384), (18, 65536)].

## 4. Is N_semantic independent of observation_depth?

Yes — N_semantic_final is identical across obs_depth [8, 12, 16] at every cap (normal-form classes key on full shape, not on the observation window). Confirms 15.1. (independence_holds=True)

## 5. Verdict

`open_candidate` — N_semantic(cap) grows exponentially (per-cap multiplier ~constant > 1) and EVERY point is exactly exhausted (no budget). By the scaling-law criterion this is the first semantic-OPEN candidate on the project's path: each depth level adds classes multiplicatively, a property of structure, not of how hard we looked.

### Structural caveat (read this)

STRUCTURAL CAVEAT: System C's normal forms are exactly the free binary words {a,b}^(cap-2) (sequences of a/b applied to the seed). N_semantic(cap)=2^(cap-2) is therefore the *combinatorially trivial* exponential — maximal diversity with zero structure, the normal-form-level analogue of noisy-TV. 'Open' here means the COUNT is unbounded by structure, NOT that the meanings are non-trivial. The mandated next step (a learnability probe) is exactly what must decide whether these deep classes carry transferable structure or are arbitrary bitstrings. Prior from this structure: expect noise.

## 6. Next action

Run a learnability probe on the deep semantic classes (do they transfer / compress, or are they arbitrary bitstrings?) BEFORE any architectural or substrate claim. Given the free-monoid structure, design it to detect exactly the noisy-TV failure.

## Honesty notes

- Non-saturation under a budget is never a positive signal; we only ever claim openness from points that are *exactly* exhausted (the semantic enumeration has no budget).

- The scaling law is fit ONLY on exhausted points; censored state-BFS caps are excluded.

- 'Open' = unbounded class COUNT by structure. It is NOT a claim that the meanings are non-trivial; the free-monoid caveat says they are likely trivial. That is the next probe's job.
