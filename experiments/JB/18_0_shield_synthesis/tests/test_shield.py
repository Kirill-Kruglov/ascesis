import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from shield import (
    ShieldParams,
    compute_doomed,
    is_monotone_reaction,
    pre_preserves_upward_closure,
    synthesize_shield,
)
from justitia_harvest import collapse_pred


P = ShieldParams(A_collapse=40, trig=34, K=1, Rc=1, Ra=2, Cmax=44, Amax=44)


def test_bounded_reaction_is_monotone():
    r = is_monotone_reaction(P, "bounded")
    assert r["monotone"] is True
    assert r["fraction_monotone"] == 1.0
    assert r["reaction_bounded"] is True


def test_unbounded_reaction_is_flagged_non_monotone():
    r = is_monotone_reaction(P, "unbounded")
    assert r["monotone"] is False
    assert r["fraction_monotone"] < 1.0
    assert len(r["counterexamples"]) > 0
    # unbounded reaction magnitude exceeds the bounded budget Rc+Ra
    assert r["reaction_magnitude_max"] > P.Rc + P.Ra


def test_pre_upward_closure_discriminates():
    assert pre_preserves_upward_closure(P, "bounded")["pre_is_upward_closed"] is True
    neg = pre_preserves_upward_closure(P, "unbounded")
    assert neg["pre_is_upward_closed"] is False
    assert len(neg["violations"]) > 0


def test_backward_reachability_terminates_for_bounded():
    d = compute_doomed(P, "bounded")
    assert d["fixpoint_reached"] is True
    # the bounded sword leaves a non-trivial safe region (not everything doomed)
    assert d["doomed_fraction"] < 1.0


def test_positive_control_scales_only_synthesizes_cleanly():
    d = compute_doomed(P, "none")
    assert d["fixpoint_reached"] is True
    # with no corrective power, accumulation drives essentially everything to collapse
    assert d["doomed_fraction"] > 0.5


def test_shield_has_must_react_band():
    d = compute_doomed(P, "bounded")
    shield = synthesize_shield(P, "bounded", d["doomed"], sample_n=10_000)
    assert any(s["must_react"] for s in shield)


def test_collapse_pred_matches_thresholds():
    # mean welfare below 0.32 -> collapse
    assert collapse_pred([0.30] * 9, total_mass=200.0) is True
    # four zones below 0.20 -> collapse even if mean is okay
    zw = [0.10, 0.10, 0.10, 0.10, 0.9, 0.9, 0.9, 0.9, 0.9]
    assert collapse_pred(zw, total_mass=200.0) is True
    # low mass -> collapse
    assert collapse_pred([0.8] * 9, total_mass=30.0) is True
    # healthy -> not collapse
    assert collapse_pred([0.7] * 9, total_mass=200.0) is False


def test_collapse_pred_is_upward_closed_in_badness():
    # worsening (lower welfare, lower mass) preserves collapse membership
    base_zw = [0.30] * 9
    assert collapse_pred(base_zw, 200.0) is True
    worse = [w - 0.05 for w in base_zw]
    assert collapse_pred(worse, 150.0) is True
