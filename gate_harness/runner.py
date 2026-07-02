"""Gate runner — refuses to run an experiment unless its prereg lock is valid.

Fixes findings #1/#2 at execution time: before any experiment code runs,
``run_gate`` calls ``verify_prereg_lock`` and hard-fails (RunnerError, not a
warning) unless the prereg was locked, is unedited, and was committed in a
strict-ancestor commit of the current HEAD.

This module is intentionally thin: it is the enforcement gate in front of the
experiment callable. The domain-specific checks (leakage_scanner, seed_policy,
calibration_audit, tautology_check) are composed here by the caller and their
results attached to the decision payload. The tautology flag, once set by
``tautology_check``, is copied verbatim and cannot be overridden by the
experiment's own output.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from . import prereg as _prereg


class RunnerError(RuntimeError):
    pass


def run_gate(
    gate_dir: Path,
    experiment_fn: Callable[[], dict[str, Any]],
    *,
    tautology_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Verify the prereg lock, then run the experiment. Fail closed.

    Raises RunnerError if the lock is missing/edited/not an ancestor of HEAD.
    """
    gate_dir = Path(gate_dir)
    ok, reason = _prereg.verify_prereg_lock(gate_dir)
    if not ok:
        raise RunnerError(f"refusing to run {gate_dir.name}: {reason}")

    result = experiment_fn()
    if not isinstance(result, dict):
        raise RunnerError("experiment_fn must return a dict decision payload (fail closed)")

    # tautology flag is authoritative: copy verbatim, forbid experiment override
    if tautology_report is not None:
        flag = bool(tautology_report.get("construction_may_be_tautological"))
        if result.get("construction_may_be_tautological") not in (None, flag):
            raise RunnerError(
                "experiment attempted to override construction_may_be_tautological; "
                "only tautology_check may set it (finding #5)"
            )
        result["construction_may_be_tautological"] = flag
        result["information_ratio"] = tautology_report.get("information_ratio")

    result["prereg_lock_verified"] = True
    return result
