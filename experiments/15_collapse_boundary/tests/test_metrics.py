from collapse_boundary.explore import observation_prefix, semantic_class
from collapse_boundary.metrics import (
    DEGENERATE,
    OPEN,
    SATURATING,
    TRIVIAL,
    axis_classify,
    channel_closure,
)
from collapse_boundary.explore import Trajectory
from collapse_boundary.types import Term


HORIZONS = [1, 2, 4, 8, 16, 32]
HORIZONS8 = [1, 2, 4, 8, 16, 32, 64, 128]


def test_dip_then_reexpand_is_non_monotonic_not_early_freeze() -> None:
    # Marginal novelty dips below epsilon (two small deltas) then re-expands.
    # deltas:        [0.20, 0.005, 0.004, 0.40, 0.30]
    values = [0.0, 0.20, 0.205, 0.209, 0.609, 0.909]
    res = channel_closure(HORIZONS, values, epsilon=0.01, k=3)
    assert res["non_monotonic_plateau"] is True
    # Must NOT freeze on the first dip: no sustained plateau (only 2 consecutive sub-eps deltas).
    assert res["sustained_plateau_horizon"] is None
    assert res["dips"] == [4]
    assert res["re_expansions"] == [16]


def test_clean_sustained_plateau() -> None:
    # deltas: [0.50, 0.05, 0.005, 0.004, 0.003] -> first run of 3 sub-eps deltas starts at h=8
    values = [0.0, 0.50, 0.55, 0.555, 0.559, 0.562]
    res = channel_closure(HORIZONS, values, epsilon=0.01, k=3)
    assert res["non_monotonic_plateau"] is False
    assert res["sustained_plateau_horizon"] == 8


def test_short_plateau_below_k_not_declared() -> None:
    # Only two sub-eps deltas at the tail; with k=3 no sustained plateau.
    values = [0.0, 0.3, 0.6, 0.9, 0.905, 0.909]
    res = channel_closure(HORIZONS, values, epsilon=0.01, k=3)
    assert res["sustained_plateau_horizon"] is None
    assert res["non_monotonic_plateau"] is False


def test_none_values_do_not_count_as_plateau() -> None:
    # Normal-form channel undefined early, then a real plateau later.
    values = [None, None, 0.5, 0.505, 0.508, 0.509]
    res = channel_closure(HORIZONS, values, epsilon=0.01, k=3)
    assert res["sustained_plateau_horizon"] == 8


def test_axis_classify_bounded_semantic_set_is_saturating_not_open() -> None:
    # The C-semantic case: count grows then saturates at a finite 1024, far below the
    # 20000 sample budget. Rate (1024/20000 ~ 0.05) must NOT be read as "open".
    counts = [5, 15, 99, 393, 428, 1252, 1024, 1024]
    budget = [20000] * 8
    res = axis_classify(HORIZONS8, counts, budget)
    assert res["verdict"] == SATURATING
    assert res["saturation_count"] == 1024
    assert res["sample_limited"] is False


def test_axis_classify_frozen_tiny_count_is_trivial() -> None:
    # B-semantic noisy-TV: a handful of classes, frozen -> trivial.
    counts = [3, 5, 9, 9, 9, 9, 9, 9]
    res = axis_classify(HORIZONS8, counts, [20000] * 8)
    assert res["verdict"] == TRIVIAL
    assert res["saturation_count"] == 9


def test_axis_classify_exploding_count_is_open() -> None:
    # B-state: term shapes keep exploding, budget is huge -> open.
    counts = [5, 36, 520, 48049, 270614, 718312, 1609343]
    budget = [40000, 100000, 180000, 340000, 660000, 1300000, 2580000]
    res = axis_classify([1, 2, 4, 8, 16, 32, 64], counts, budget)
    assert res["verdict"] == OPEN
    assert res["still_growing"] is True


def test_axis_classify_sample_limited_is_open_but_flagged() -> None:
    # C-trajectory: distinct count rises to the sample cap -> open(sample-limited).
    counts = [5, 20, 724, 12256, 19975, 19999, 20000, 19999]
    res = axis_classify(HORIZONS8, counts, [20000] * 8)
    assert res["verdict"] == OPEN
    assert res["sample_limited"] is True


def test_axis_classify_degenerate_single_class() -> None:
    res = axis_classify(HORIZONS8, [1, 1, 1, 1, 1, 1, 1, 1], [20000] * 8)
    assert res["verdict"] == DEGENERATE


def test_observation_prefix_truncates_at_depth() -> None:
    deep = Term("f", (Term("g", (Term("h", (Term("x"),)),)),))
    assert observation_prefix(deep, 0) == "*"
    assert observation_prefix(deep, 1) == "f(*)"
    assert observation_prefix(deep, 2) == "f(g(*))"
    # Beyond actual depth, leaves render as "_" (identity erased).
    assert observation_prefix(deep, 9) == "f(g(h(_)))"


def test_semantic_class_uses_normal_form_or_observation() -> None:
    nf_term = Term("a", (Term("x"),))
    terminated = Trajectory(initial=nf_term, terms=[nf_term], rules=[], collapsing_steps=0, terminated=True)
    assert semantic_class(terminated, obs_depth=4).startswith("NF:")

    deep = Term("F", (Term("G", (Term("a", (Term("x"),)),)),))
    running = Trajectory(initial=deep, terms=[deep], rules=["G_expand"], collapsing_steps=0, terminated=False)
    assert semantic_class(running, obs_depth=2).startswith("OBS:")
