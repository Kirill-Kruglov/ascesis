import random

from collapse_boundary.explore import canonical_trajectory, compression_stats, limited_reachable, random_trajectory
from collapse_boundary.systems import build_systems


def test_random_trajectory_has_canonical_shape() -> None:
    rng = random.Random(3)
    system = build_systems()[2]
    traj = random_trajectory(system, system.sampler(rng, 3), 4, rng)
    assert canonical_trajectory(traj)
    assert traj.terms


def test_limited_reachable_collects_edges() -> None:
    rng = random.Random(4)
    system = build_systems()[3]
    seen, edges = limited_reachable(system, system.sampler(rng, 3), 3)
    assert seen
    assert edges


def test_compression_stats_are_bounded() -> None:
    stats = compression_stats(["a", "a", "a"])
    assert stats["raw_size"] > 0
    assert stats["compressed_size"] > 0
    assert stats["compression_ratio"] > 0
