# gate_harness — instrumental gate discipline

Executable enforcement of the Ascesis methodology. Where
`playbook_extraction/harness/` *describes* the rules in prose, this package
*enforces* them so a violation is mechanically impossible for any honest process
(human, Codex, Claude, or other) running through it.

**Axiom: fail closed.** Any ambiguity, missing artifact, or claim that cannot be
checked mechanically resolves to **FAIL**. Nothing passes by default.

Each module maps to a finding from the B1/B1.1/B2/B2.1 falsification audit.

## Built (backbone) — verified by `tests/test_gate_harness.py` (8/8)

### `prereg.py` — two-phase-commit pre-registration (findings #1, #2, #9)
- `lock_prereg(gate, thresholds, rationale_for_any_threshold_changes)` writes
  `PREREG.json` + `PREREG.lock` (SHA256 + timestamp + git rev at lock time).
  A threshold shared with the previous gate that changed value **requires** a
  non-empty rationale, else it raises and writes nothing (finding #9).
- `verify_prereg_lock(gate_dir)` (runner uses this) refuses to run unless the
  lock exists, its SHA matches `PREREG.json`, and the lock's rev is a **strict
  ancestor** of HEAD — i.e. the prereg was committed *before* the run (finding #1).

### `hooks/pre-commit` + `install_hooks.sh` — commit-time enforcement
- Rejects committing a gate's `PREREG.*` together with its `outputs/` (finding #1).
- Rejects editing a locked `PREREG.json` (SHA mismatch vs `PREREG.lock`, finding #2).
- Install with `bash gate_harness/install_hooks.sh` (refuses to clobber an
  existing different hook). **Not auto-installed** — it changes commit behavior.

### `leakage_scanner.py` — AST fit-path audit (findings #3, #4, #6)
- Real static analysis, **not** self-report. Scans every registered fit/predict/
  classify function's AST for forbidden truth names appearing as parameters,
  identifiers, attributes, **dict string keys** (`record["z_obj"]`), string
  constants, closures, or referenced globals.
- Catching dict-string-keys is why AST is required: the toy worlds read truth via
  `record["z_obj"]`, which an identifier-only or `pattern in source` scan misses.
- Every emitted field carries `computed_by: ast_scan` with file+line evidence, or
  `NOT_VERIFIABLE` — which makes the check FAIL, never a silent skip.
- Regression test reproduces the real B2 leak (`variant`-branching classifier),
  proves it is caught, and proves the repaired label-free version passes.

### `calibration_audit.py` — anchor-volume assertions (finding #7)
- `assert_minimal_calibration(...)` fails if the anchor fraction exceeds a
  mandatory `max_anchor_fraction`; `assert_sparse_not_heavier_than_complete(...)`
  hard-errors if "sparse" carries >= as many anchor records as "complete".
- Verified on the real B2 counts: sparse=216 >= complete=144 → raises.

### `seed_policy.py` — multi-seed enforcement (finding #8)
- `role: core` metrics need >= `MIN_SEEDS_FOR_CORE_METRIC` (=20) seeds, else the
  verdict is `INSUFFICIENT_SEEDS`, never PASS. `auxiliary_check` metrics exempt.

### `tautology_check.py` — construction pre-check (finding #5, recovered §1.6)
- `tautology_precheck(y, z, thresholds)` computes `information_ratio = var(y)/var(z)`
  before any learner; `information_ratio_min` is mandatory (no default → raises).
  Below it → immutable `construction_may_be_tautological: true`.
- `run_generic_baselines(...)` runs the two mandatory strong baselines (k-means at
  known group count; BIC-selected 1D GMM, hand-rolled — numpy only) and emits the
  verbatim honesty statement with N substituted.
- On the real B1.1 world: `information_ratio=0.0475`, both baselines abs_corr≈0.21.

### `runner.py` — execution gate (findings #1/#2)
- `run_gate(gate_dir, experiment_fn, tautology_report=...)` calls
  `verify_prereg_lock` and hard-fails (RunnerError) unless the lock is valid and
  an ancestor of HEAD. Copies the tautology flag verbatim; forbids experiment
  override.

### Adversarial self-tests — `tests/test_adversarial.py` (7/7)
Each test reproduces a real audit finding and is RED without its defense, GREEN
with it (tests 1/3/4 were already GREEN from the backbone layer — not faked-red).

## NOT built yet — blocked on truncated spec

- `evaluation_oracle.py` (§1.4, finding #6) — the `EVALUATION_ORACLE_LOG` schema
  and auto-generated decision-JSON warning wording were in the truncated tail.
  Per the maintainer's note it will reuse the AST dict-string-key technique from
  `leakage_scanner` (truth like `truth_axes=3` likely enters via a kwarg / dict
  key in `evaluate_coords`, not a top-level named param).
