"""Repaired measurement instruments for Experiment 15.0.1.

These functions are deliberately pure (no I/O, no system simulation) so the
sustained-plateau logic can be unit-tested against hand-built novelty curves.

Nothing here changes the four rewrite systems under study; this is instrument
repair only (closure-horizon estimator + per-axis classification).
"""
from __future__ import annotations

from typing import Optional

# Verdicts emitted per channel/axis.
TRIVIAL = "trivial"        # novelty rate ~0: channel collapses to (near) one object
SATURATING = "saturating"  # novelty rate settles (sustained plateau) at a moderate, non-growing level
OPEN = "open"              # novelty rate stays high / never reaches a sustained plateau
DEGENERATE = "degenerate"  # the proxy itself collapses everything to one class (uninformative)


def channel_closure(
    horizons: list[int],
    values: list[Optional[float]],
    epsilon: float = 0.01,
    k: int = 3,
) -> dict[str, object]:
    """Sustained-plateau closure horizon for a SINGLE novelty channel.

    A plateau is declared only when the marginal novelty delta stays below
    ``epsilon`` for ``k`` consecutive horizon steps (the first sustained plateau,
    not the first dip). If novelty dips below ``epsilon`` and later re-expands
    above it, ``non_monotonic_plateau`` is flagged and the dip / re-expansion
    horizons are reported instead of freezing on the first dip.

    ``values`` is aligned with ``horizons`` and may contain ``None`` for
    undefined points (e.g. a normal-form channel before any normal form exists);
    deltas spanning a ``None`` are treated as undefined (not below epsilon).
    """
    if len(horizons) != len(values):
        raise ValueError("horizons and values must be the same length")
    n = len(values)

    # deltas[i] is the marginal change over the transition horizons[i] -> horizons[i+1]
    deltas: list[Optional[float]] = []
    for i in range(1, n):
        prev_v, cur_v = values[i - 1], values[i]
        if prev_v is None or cur_v is None:
            deltas.append(None)
        else:
            deltas.append(abs(cur_v - prev_v))

    below = [(d is not None and d < epsilon) for d in deltas]

    dips: list[int] = []
    re_expansions: list[int] = []
    for i, is_below in enumerate(below):
        h = horizons[i + 1]
        if is_below and (i == 0 or not below[i - 1]):
            dips.append(h)
        if (not is_below) and deltas[i] is not None and i > 0 and below[i - 1]:
            re_expansions.append(h)
    non_monotonic = len(re_expansions) > 0

    # First sustained plateau: earliest run of k consecutive below-epsilon deltas.
    sustained: Optional[int] = None
    if len(below) >= k:
        for i in range(len(below) - k + 1):
            if all(below[i : i + k]):
                sustained = horizons[i + 1]
                break

    return {
        "epsilon": epsilon,
        "k": k,
        "sustained_plateau_horizon": sustained,
        "non_monotonic_plateau": non_monotonic,
        "dips": dips,
        "re_expansions": re_expansions,
        "marginal_deltas": {
            str(horizons[i + 1]): (None if deltas[i] is None else round(deltas[i], 6))
            for i in range(len(deltas))
        },
        "values": {
            str(horizons[i]): (None if values[i] is None else round(values[i], 6))
            for i in range(n)
        },
    }


def final_value(values: list[Optional[float]]) -> Optional[float]:
    """Last defined (non-None) value in a channel series."""
    for v in reversed(values):
        if v is not None:
            return v
    return None


def axis_classify(
    horizons: list[int],
    unique_counts: list[int],
    generated: list[int],
    growth_eps: float = 0.05,
    tau_low_rate: float = 0.05,
    sample_limit_frac: float = 0.9,
    window: int = 2,
) -> dict[str, object]:
    """Classify one axis as open / saturating / trivial / degenerate.

    Openness is judged on the UNIQUE-OBJECT COUNT as a function of HORIZON
    (depth), NOT on the novelty *rate* at a fixed sample budget. A rate can sit at
    a "moderate" value purely because a finite set of classes is divided by a large
    sample count; only the count-vs-horizon trend reveals whether the object space
    is genuinely unbounded.

      - ``degenerate``: <=1 distinct object ever (proxy collapses everything).
      - ``open``: count still growing at the largest horizon (or saturated only
        because it filled the sample budget -> ``sample_limited``, openness then
        indeterminate but not closed).
      - ``trivial``: count plateaued AND final novelty rate < ``tau_low_rate``
        (the channel settles to ~no per-object diversity).
      - ``saturating``: count plateaued at a finite set well below the sample
        budget, with non-trivial rate.

    ``generated`` is the per-horizon object budget for this channel (terms for the
    state channel; trajectories for trajectory/semantic; terminating trajectories
    for normal_form). Returns a verdict plus the evidence behind it.
    """
    U = list(unique_counts)
    B = list(generated)
    n = len(U)
    if n == 0 or max(U) <= 1:
        return {"verdict": DEGENERATE, "saturation_count": (U[-1] if U else 0),
                "saturation_horizon": None, "final_rate": None,
                "sample_limited": False, "still_growing": False}

    final_rate = (U[-1] / B[-1]) if (B and B[-1]) else None
    sample_limited = bool(B and B[-1] and U[-1] >= sample_limit_frac * B[-1])

    # "Still growing" uses CUMULATIVE growth over the last `window` horizons, so a
    # single noisy step between otherwise-flat counts does not read as openness.
    base_idx = max(0, n - 1 - window)
    base = U[base_idx]
    still_growing = (U[-1] - base) / max(1, base) > growth_eps

    # Earliest horizon from which the count stays within growth_eps of its final value.
    saturation_horizon = None
    for i in range(n):
        if all(abs(U[j] - U[-1]) / max(1, U[-1]) <= growth_eps for j in range(i, n)):
            saturation_horizon = horizons[i]
            break

    if still_growing and not sample_limited:
        verdict = OPEN
    elif sample_limited:
        verdict = OPEN  # syntactic space >= sample budget; openness indeterminate, but not closed
    elif final_rate is not None and final_rate < tau_low_rate:
        verdict = TRIVIAL
    else:
        verdict = SATURATING

    return {
        "verdict": verdict,
        "saturation_count": U[-1],
        "saturation_horizon": saturation_horizon,
        "final_rate": final_rate,
        "sample_limited": sample_limited,
        "still_growing": still_growing,
    }
