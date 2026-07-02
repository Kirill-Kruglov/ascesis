from worldcore.metrics import collision_fraction, novelty_rate, saturation_curve, uniqueness_ratio


def test_novelty_and_collision_rates() -> None:
    hashes = ["a", "b", "a", "c"]
    assert novelty_rate(hashes) == 0.75
    assert uniqueness_ratio(hashes) == 0.75
    assert collision_fraction(hashes) == 0.25


def test_saturation_curve() -> None:
    rows = saturation_curve(["a", "a", "b"], [1, 2, 3])
    assert rows[-1]["unique"] == 2
    assert rows[-1]["samples"] == 3
    assert abs(rows[-1]["collision_fraction"] - (1 / 3)) < 1e-12
