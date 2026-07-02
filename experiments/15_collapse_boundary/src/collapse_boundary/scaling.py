"""Scaling-law fitting for Experiment 15.2.

Fits N_semantic(cap) against three candidate functional forms and reports R²
(computed on the raw counts, so the three are directly comparable) plus the
per-cap multiplier. No form is chosen by eye; the caller reads the numbers.
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import curve_fit


def _r2(y: np.ndarray, y_hat: np.ndarray) -> float:
    ss_res = float(np.sum((y - y_hat) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    if ss_tot == 0:
        return 1.0 if ss_res == 0 else 0.0
    return 1.0 - ss_res / ss_tot


def fit_scaling(caps: list[int], counts: list[int]) -> dict[str, object]:
    """Fit bounded/asymptotic, polynomial, and exponential forms to N(cap).

    Returns per-form params + R² (on raw N), the per-cap multiplier series (and
    its mean / trend), and a `best_form` purely by highest R² — interpretation is
    left to the decision logic, which also requires exhaustion before any
    openness claim.
    """
    x = np.asarray(caps, dtype=float)
    y = np.asarray(counts, dtype=float)
    n = len(x)
    forms: dict[str, object] = {}

    # Exponential  N = a * b^cap   (fit log-linear, exact for 2^(cap-2))
    try:
        slope, intercept = np.polyfit(x, np.log(y), 1)
        a_exp, b_exp = float(np.exp(intercept)), float(np.exp(slope))
        y_hat = a_exp * b_exp ** x
        forms["exponential"] = {"a": a_exp, "b": b_exp, "r2": _r2(y, y_hat),
                                "form": "a*b^cap", "per_cap_multiplier": b_exp}
    except Exception as exc:  # pragma: no cover
        forms["exponential"] = {"error": str(exc)}

    # Polynomial  N = a * cap^k   (fit log-log)
    try:
        k, log_a = np.polyfit(np.log(x), np.log(y), 1)
        a_poly = float(np.exp(log_a))
        y_hat = a_poly * x ** k
        forms["polynomial"] = {"a": a_poly, "k": float(k), "r2": _r2(y, y_hat), "form": "a*cap^k"}
    except Exception as exc:  # pragma: no cover
        forms["polynomial"] = {"error": str(exc)}

    # Bounded / asymptotic  N = a - b*r^cap,  0<r<1  (saturates to a)
    try:
        def bounded(cap, a, b, r):
            return a - b * np.power(r, cap)
        p0 = [float(max(y)) * 1.5, float(max(y)), 0.5]
        popt, _ = curve_fit(bounded, x, y, p0=p0,
                            bounds=([0, 0, 1e-6], [np.inf, np.inf, 1 - 1e-6]),
                            maxfev=20000)
        y_hat = bounded(x, *popt)
        forms["bounded"] = {"a": float(popt[0]), "b": float(popt[1]), "r": float(popt[2]),
                            "r2": _r2(y, y_hat), "form": "a-b*r^cap", "asymptote": float(popt[0])}
    except Exception as exc:
        forms["bounded"] = {"error": str(exc), "form": "a-b*r^cap"}

    # Per-cap multiplier (normalized to a +1-cap step, since the grid steps by 2).
    multipliers = []
    for i in range(1, n):
        step = x[i] - x[i - 1]
        ratio = y[i] / y[i - 1] if y[i - 1] else float("nan")
        per_cap = ratio ** (1.0 / step) if (ratio == ratio and step) else float("nan")
        multipliers.append({"from_cap": int(x[i - 1]), "to_cap": int(x[i]),
                            "ratio": float(ratio), "per_cap_multiplier": float(per_cap)})
    per_cap_vals = [m["per_cap_multiplier"] for m in multipliers if m["per_cap_multiplier"] == m["per_cap_multiplier"]]
    mult_mean = float(np.mean(per_cap_vals)) if per_cap_vals else float("nan")
    # Trend: does the per-cap multiplier decay toward 1 (bounded/poly) or stay >1 (exp)?
    mult_trend = float(np.polyfit(range(len(per_cap_vals)), per_cap_vals, 1)[0]) if len(per_cap_vals) >= 2 else 0.0

    r2s = {f: v.get("r2") for f, v in forms.items() if isinstance(v, dict) and v.get("r2") is not None}
    best_form = max(r2s, key=r2s.get) if r2s else None

    return {
        "n_points": n,
        "caps": [int(c) for c in caps],
        "counts": [int(c) for c in counts],
        "forms": forms,
        "best_form_by_r2": best_form,
        "per_cap_multiplier_series": multipliers,
        "per_cap_multiplier_mean": mult_mean,
        "per_cap_multiplier_trend": mult_trend,
    }
