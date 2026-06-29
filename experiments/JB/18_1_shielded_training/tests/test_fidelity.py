import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fidelity import ShieldParams, confusion, future_collapse_flags, project, shield_label
from levelb import equal_volume_datasets
from shield import compute_doomed

P = ShieldParams(A_collapse=40, trig=34, K=1, Rc=1, Ra=2, Cmax=44, Amax=44)
DOOMED = compute_doomed(P, "bounded")["doomed"]


def test_projection_matches_primary_collapse_clause():
    # mean welfare just below 0.32 -> a >= A_collapse -> DOOMED
    c, a = project(0.31, 0.2, P)
    assert a >= P.A_collapse
    # mean welfare above 0.32 -> SAFE
    c, a = project(0.50, 0.2, P)
    assert a < P.A_collapse


def test_shield_blind_to_spread_clause():
    # mean welfare healthy but 4 zones collapsed -> real collapse, shield says SAFE
    s = {"mean_welfare": 0.50, "resource_hhi": 0.2, "n_zones_below_0_20": 4, "total_mass": 200.0}
    assert shield_label(s, DOOMED, P) == "SAFE"


def test_future_collapse_flags_lookahead():
    seq = [{"collapse": False}, {"collapse": False}, {"collapse": True}, {"collapse": False}]
    rest = future_collapse_flags(seq, None)
    assert rest == [True, True, True, False]
    win0 = future_collapse_flags(seq, 0)
    assert win0 == [False, False, True, False]


def test_confusion_counts_false_safe():
    # one trajectory: a SAFE-labeled state that later collapses == false safe
    seq = [
        {"world": "W", "policy": "p", "seed": 1, "step": 0, "mean_welfare": 0.60,
         "resource_hhi": 0.2, "n_zones_below_0_20": 0, "total_mass": 200.0, "collapse": False},
        {"world": "W", "policy": "p", "seed": 1, "step": 1, "mean_welfare": 0.20,
         "resource_hhi": 0.2, "n_zones_below_0_20": 5, "total_mass": 200.0, "collapse": True},
    ]
    r = confusion(seq, P, horizon=None)
    # step 0 is SAFE but trajectory collapses -> false safe
    assert r["false_safe_rate"] > 0.0
    assert r["n_safe"] >= 1


def test_equal_volume_guarantee():
    safe = list(range(100))
    alls = list(range(300))
    shielded, control, n = equal_volume_datasets(safe, alls, seed=1)
    assert len(shielded) == len(control) == n
    assert n == 100  # min(#safe, #all)


def test_equal_volume_deterministic():
    safe = list(range(50))
    alls = list(range(200))
    a1, b1, _ = equal_volume_datasets(safe, alls, seed=7)
    a2, b2, _ = equal_volume_datasets(safe, alls, seed=7)
    assert a1 == a2 and b1 == b2
