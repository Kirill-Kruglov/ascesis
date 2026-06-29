# Experiment 18.1 — Does Training Inside the Shield Help?

Two levels; **Level A is a kill gate**. No Sanskrit, no language, no LLM — the "model" is a
lightweight learner (LLM scale is 18.3, only if this survives).

## How this connects to the goal

The special theory says: train inside a safe boundary so the model never learns
collapse-trajectories — safer than internet-trained, even though content inside is
generalized not derived. 18.0 showed the boundary is a decidable shield *on an abstraction*.
**18.1 Level A tests whether that abstraction is faithful to real justitia** (or the shield
filters a phantom); Level B (gated) would test whether training inside it actually buys
safety without buying uselessness, on unseen environments. If Level A fails we need a richer
abstraction before anything else.

## Result — Level A FAILED (`fidelity_fails_false_safe`)

Pre-registered bar: false_safe_rate ≤ 0.05 (fixed in `level_A_preregistration.json` before
the confusion matrix). Measured on 16,000 real states:

- **false_safe_rate = 0.299** — 30% of states the shield calls SAFE actually reach real collapse.
- **pure abstraction-blindness = 0.193** — of states that are *already* collapsed, 19% are
  labeled SAFE (no lookahead, no policy: a direct projection failure).
- Even under the strongest containment policies, forward false-safe stays ~0.08–0.09 > 0.05.

**Blind coordinates** (the reformulation hint): the 2-counter abstraction (concentration,
mean-welfare-deficit) is blind to (1) **zone-welfare spread** — the `≥4 zones<0.20` collapse
clause; (2) **total mass** — the `mass<35` clause; (3) **forward dynamics** — 18.0's doomed
set converged in 1 iteration to U itself, so the shield is a current-mean-welfare-collapse
*detector*, not a forward predictor.

**Level B was NOT run** (kill gate). Training behind a lying shield manufactures false
confidence. This also retroactively exposes that 18.0's `shield_synthesizable` holds only for
the abstraction — which 18.1 shows does not track real collapse.

**Next step:** reformulate the abstraction with min-zone-welfare / failed-zone-count and
total-mass coordinates plus a genuine forward reachability, then re-run 18.0 fidelity BEFORE
any training. Do NOT proceed to 18.2/18.3.

## Run

```bash
python scripts/run_18_1.py --mode full     # Level A; Level B gated behind a pass
pytest tests/                               # fidelity confusion-matrix + equal-volume guarantee
```

Requires 18.0 at `../18_0_shield_synthesis` (shield + harvester reused) and the justitia repo
at `/home/master/llm_projects/justitia` (imported read-only).
