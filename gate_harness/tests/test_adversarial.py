"""Adversarial self-tests: prove the harness catches the EXACT bugs the audit found.

Every test reproduces a real finding. Each test is written so it would be RED
without the corresponding defense and GREEN with it. Imports are lazy inside each
test so a missing module reports as that test failing (RED) rather than crashing
the whole file — this lets us show the red->green transition per finding.

Run: python3 -m gate_harness.tests.test_adversarial
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


def _run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


# 1 — finding #3/leakage: classifier branches on ground-truth generator label
def test_catches_variant_branching_classifier():
    from gate_harness import leakage_scanner as LS

    def classify(relation_metric, coords, variant):
        if variant == "chain":
            return "ORDER_1D"
        if variant == "product2d":
            return "PRODUCT_2D"
        return "INCONCLUSIVE"

    report = LS.scan_fit_path([classify])
    assert report["passed"] is False, "must flag variant-branching classifier"
    assert any(h["forbidden_name"] == "variant" for h in report["leak_hits"])


# 2 — finding #3: audit fields that are hardcoded constants, not computed
def test_rejects_hardcoded_audit_fields():
    from gate_harness import leakage_scanner as LS

    def leakage_audit(records):
        item_ids_by_u = {}  # pretend real work
        return {
            "u_uniquely_identifies_item_id": any(len(v) <= 1 for v in item_ids_by_u.values()),
            "learner_fit_reads_true_z_obj": False,   # hardcoded self-report
            "aux_leakage_detected": False,           # hardcoded self-report
            "human_authored_outcomes_detected": False,  # hardcoded self-report
        }

    report = LS.scan_audit_report_integrity(leakage_audit)
    assert report["passed"] is False, "hardcoded audit fields must fail the verdict"
    nv = {k for k, v in report["fields"].items() if v["computed_by"] == "NOT_VERIFIABLE"}
    assert {"learner_fit_reads_true_z_obj", "aux_leakage_detected", "human_authored_outcomes_detected"} <= nv
    assert report["fields"]["u_uniquely_identifies_item_id"]["computed_by"] == "ast_scan"


# 3 — finding #1: prereg + outputs committed together
def test_precommit_blocks_prereg_and_outputs_together():
    hook = Path(__file__).resolve().parents[1] / "hooks" / "pre-commit"
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        _run(["git", "init", "-q"], repo)
        _run(["git", "config", "user.email", "t@t"], repo)
        _run(["git", "config", "user.name", "t"], repo)
        (repo / ".git" / "hooks").mkdir(parents=True, exist_ok=True)
        (repo / ".git" / "hooks" / "pre-commit").write_text(hook.read_text())
        (repo / ".git" / "hooks" / "pre-commit").chmod(0o755)
        gate = repo / "experiments" / "G1"
        (gate / "outputs").mkdir(parents=True)
        (repo / "s").write_text("x"); _run(["git", "add", "s"], repo); _run(["git", "commit", "-qm", "i"], repo)
        (gate / "PREREG.json").write_text('{"gate":"G1","thresholds":{}}\n')
        (gate / "PREREG.lock").write_text('{"prereg_sha256":"deadbeef"}\n')
        (gate / "outputs" / "metrics.json").write_text('{"corr":0.99}\n')
        _run(["git", "add", "-A"], repo)
        res = _run(["git", "commit", "-m", "both"], repo)
        assert res.returncode != 0, "commit with prereg+outputs must be blocked"
        assert "finding #1" in (res.stdout + res.stderr)


# 4 — finding #2: editing a locked prereg
def test_precommit_blocks_locked_prereg_edit():
    from gate_harness import prereg as PR
    import os

    hook = Path(__file__).resolve().parents[1] / "hooks" / "pre-commit"
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        _run(["git", "init", "-q"], repo)
        _run(["git", "config", "user.email", "t@t"], repo)
        _run(["git", "config", "user.name", "t"], repo)
        (repo / ".git" / "hooks").mkdir(parents=True, exist_ok=True)
        (repo / ".git" / "hooks" / "pre-commit").write_text(hook.read_text())
        (repo / ".git" / "hooks" / "pre-commit").chmod(0o755)
        (repo / "experiments" / "G1").mkdir(parents=True)
        (repo / "s").write_text("x"); _run(["git", "add", "s"], repo); _run(["git", "commit", "-qm", "i"], repo)
        cwd0 = os.getcwd(); os.chdir(repo)
        try:
            PR.lock_prereg("G1", {"corr_min": 0.9}, experiments_root=repo / "experiments")
        finally:
            os.chdir(cwd0)
        _run(["git", "add", "experiments/G1/PREREG.json", "experiments/G1/PREREG.lock"], repo)
        _run(["git", "commit", "-qm", "lock"], repo)
        (repo / "experiments" / "G1" / "PREREG.json").write_text('{"gate":"G1","thresholds":{"corr_min":0.5}}\n')
        _run(["git", "add", "experiments/G1/PREREG.json"], repo)
        res = _run(["git", "commit", "-m", "loosen"], repo)
        assert res.returncode != 0, "editing locked prereg must be blocked"
        assert "finding #2" in (res.stdout + res.stderr)


# 5 — finding #5: bias = -center construction makes y information-empty
def test_tautology_check_flags_negated_bias_construction():
    from gate_harness import tautology_check as TC

    centers = {"U0": -2.4, "U1": -0.8, "U2": 0.8, "U3": 2.4}
    biases = {u: -c for u, c in centers.items()}  # exact negation, as in B1.1
    import random
    rng = random.Random(0)
    y, z = [], []
    for u in centers:
        for _ in range(80):
            zi = centers[u] + rng.uniform(-0.7, 0.7)
            yi = zi + biases[u] + rng.uniform(-0.025, 0.025)
            z.append(zi); y.append(yi)
    report = TC.tautology_precheck(y, z, thresholds={"information_ratio_min": 0.5})
    assert report["construction_may_be_tautological"] is True


# 6 — finding #7: "sparse" anchor set larger than "complete"
def test_calibration_audit_rejects_oversized_sparse_anchor_set():
    from gate_harness import calibration_audit as CA

    sparse = list(range(216))    # real B2 numbers
    complete = list(range(144))
    try:
        CA.assert_sparse_not_heavier_than_complete(sparse, complete)
    except CA.CalibrationError:
        return
    raise AssertionError("oversized sparse anchor set must raise before any learner runs")


# 7 — finding #1: runner refuses to run without a valid, ancestor-committed lock
def test_runner_refuses_without_valid_lock():
    from gate_harness import runner as R
    from gate_harness import prereg as PR
    import os

    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        _run(["git", "init", "-q"], repo)
        _run(["git", "config", "user.email", "t@t"], repo)
        _run(["git", "config", "user.name", "t"], repo)
        gate = repo / "experiments" / "G1"
        gate.mkdir(parents=True)
        (repo / "s").write_text("x"); _run(["git", "add", "s"], repo); _run(["git", "commit", "-qm", "i"], repo)

        # (a) no lock at all
        (gate / "PREREG.json").write_text('{"gate":"G1","thresholds":{}}\n')
        try:
            R.run_gate(gate, experiment_fn=lambda: {"ran": True})
        except R.RunnerError:
            pass
        else:
            raise AssertionError("runner must refuse without PREREG.lock")

        # (b) lock exists but rev == HEAD (prereg not committed before run)
        cwd0 = os.getcwd(); os.chdir(repo)
        try:
            PR.lock_prereg("G1", {}, experiments_root=repo / "experiments")
        finally:
            os.chdir(cwd0)
        try:
            R.run_gate(gate, experiment_fn=lambda: {"ran": True})
        except R.RunnerError:
            return
        raise AssertionError("runner must refuse when lock rev is not a strict ancestor of HEAD")


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    results = []
    for t in tests:
        try:
            t()
            results.append((t.__name__, "GREEN"))
        except Exception as exc:  # noqa: BLE001 - report every failure kind as RED
            results.append((t.__name__, f"RED  ({type(exc).__name__}: {str(exc)[:60]})"))
    width = max(len(n) for n, _ in results)
    for name, status in results:
        print(f"  {name.ljust(width)}  {status}")
    reds = sum(1 for _, s in results if s.startswith("RED"))
    print(f"\n{len(results) - reds}/{len(results)} GREEN")
    return 1 if reds else 0


if __name__ == "__main__":
    sys.exit(main())
