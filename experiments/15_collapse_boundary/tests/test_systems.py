import random

from collapse_boundary.explore import random_trajectory
from collapse_boundary.systems import build_collapsing_system, build_systems, sample_dead


def test_all_required_systems_exist() -> None:
    systems = build_systems()
    assert [system.name for system in systems] == [
        "A_dead_control",
        "B_fake_live_control",
        "C_collapsing_live_candidate",
        "D_structured_live_candidate",
    ]


def test_dead_control_reaches_normal_form() -> None:
    rng = random.Random(1)
    system = build_systems()[0]
    traj = random_trajectory(system, sample_dead(rng, 10), 64, rng)
    assert traj.terminated
    assert not system.rewrites(traj.final)


def test_fake_live_expands_without_terminating_early() -> None:
    rng = random.Random(2)
    system = build_systems()[1]
    traj = random_trajectory(system, system.sampler(rng, 2), 8, rng)
    assert len(traj.rules) == 8
    assert not traj.terminated


def test_collapsing_system_depth_cap_controls_g_expand() -> None:
    rng = random.Random(3)
    shallow = build_collapsing_system(depth_cap=2)
    permissive = build_collapsing_system(depth_cap=3)
    initial = permissive.sampler(rng, 2)
    # Force the canonical G(x) case: sample_collapse may also emit F(G(a(x)), G(b(x))).
    while initial.symbol != "G":
        initial = permissive.sampler(rng, 2)
    shallow_rules = {step.rule_name for step in shallow.rewrites(initial)}
    permissive_rules = {step.rule_name for step in permissive.rewrites(initial)}
    assert "G_expand" not in shallow_rules
    assert "G_expand" in permissive_rules


def test_default_collapsing_system_keeps_original_depth_cap() -> None:
    default_c = build_systems()[2]
    explicit_c = build_collapsing_system(depth_cap=12)
    rng1 = random.Random(4)
    rng2 = random.Random(4)
    default_traj = random_trajectory(default_c, default_c.sampler(rng1, 10), 16, rng1)
    explicit_traj = random_trajectory(explicit_c, explicit_c.sampler(rng2, 10), 16, rng2)
    assert default_traj.canonical_shape() == explicit_traj.canonical_shape()
    assert default_traj.rule_shape() == explicit_traj.rule_shape()
