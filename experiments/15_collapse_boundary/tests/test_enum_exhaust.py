from collapse_boundary.enum_exhaust import (
    exact_normal_forms,
    prefix_layers,
    state_bfs,
)
from collapse_boundary.scaling import fit_scaling


def test_exact_normal_forms_equals_two_pow_cap_minus_2() -> None:
    for cap in [4, 6, 8, 10]:
        res = exact_normal_forms(cap)
        assert res["n_semantic_final"] == 2 ** (cap - 2)
        assert res["exhausted"] is True
        assert res["censored"] is False


def test_prefix_layers_exhausts_and_matches_exact() -> None:
    res = prefix_layers(8, obs_depth=12)
    assert res["exhausted"] is True
    assert res["n_semantic_final"] == 64
    # frontier doubles per layer until terminal: layer counts are powers of two
    sizes = [row["frontier_size"] for row in res["by_layer"]]
    assert sizes[0] == 1
    assert sizes[-1] == 2 ** (8 - 2)  # 64 terminal normal-form prefixes


def test_state_bfs_exhausts_small_cap_but_censors_cap6() -> None:
    small = state_bfs(4, node_budget=100_000)
    assert small["exhausted"] is True
    assert small["censored"] is False
    assert small["n_semantic_final"] == 4

    big = state_bfs(6, node_budget=3_000)
    assert big["censored"] is True
    assert big["exhausted"] is False
    # The semantic space is tiny (16) even though states explode past budget.
    assert big["nodes_expanded"] >= 3_000
    assert big["n_semantic_final"] <= 16


def test_fit_scaling_picks_exponential_for_doubling_data() -> None:
    caps = [6, 8, 10, 12, 14, 16]
    counts = [2 ** (c - 2) for c in caps]
    fit = fit_scaling(caps, counts)
    assert fit["best_form_by_r2"] == "exponential"
    assert fit["forms"]["exponential"]["r2"] > 0.999
    # per-cap multiplier ~2, roughly constant (trend ~0)
    assert abs(fit["per_cap_multiplier_mean"] - 2.0) < 0.05
    assert abs(fit["per_cap_multiplier_trend"]) < 0.05


def test_fit_scaling_picks_polynomial_for_power_data() -> None:
    caps = [6, 8, 10, 12, 14, 16]
    counts = [c ** 3 for c in caps]
    fit = fit_scaling(caps, counts)
    assert fit["best_form_by_r2"] == "polynomial"
    assert fit["forms"]["polynomial"]["r2"] > 0.999
    assert abs(fit["forms"]["polynomial"]["k"] - 3.0) < 0.1
