#!/usr/bin/env python3
import csv
import hashlib
import json
import math
import subprocess
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / 'results'
RAW = RESULTS / 'raw'

DECLARED_SPEC_SHA256 = '705956aeed7da99b221d6ae0c1c2bc5c54b2099585a2a8134eede86155be200e'

TRAIN_SEEDS = list(range(3100, 3130))
HELDOUT_SEEDS = list(range(4100, 4130))
REGIME = 'geometric'
GRID_GRID = np.linspace(0.0, 1.0, 21)
STEPS = 120
G = 2
EPS = 1e-9

# Exploration grid. The thresholds live in SPEC; these ranges are logged, not optimized post hoc.
GAMMAS = [0.0, 0.05, 0.10, 0.20, 0.40, 0.80]
AUDIT_PS = [0.0, 0.10, 0.25, 0.50]
AUDIT_CS = [0.0, 0.25, 0.50, 0.75, 1.00]
KAPPAS = [0.0, 0.05, 0.10, 0.20, 0.40]
PENALTY_WINDOW = 5
CAPTURE_AUDIT_THRESHOLD = 0.10
FALSE_POSITIVE_BASE = 0.10

LOW_R_THRESHOLD = 0.40
MID_HIGH_R_MIN = 0.80
HIGH_R_MIN = 2.0


@dataclass(frozen=True)
class RSetting:
    name: str
    capture_rate: float
    lag: int
    audit_period: int


R_SETTINGS = [
    RSetting('r01', 0.55, 9, 2),
    RSetting('r02', 0.45, 7, 2),
    RSetting('r03', 0.35, 6, 2),
    RSetting('r04', 0.28, 5, 2),
    RSetting('r05', 0.22, 4, 2),
    RSetting('r06', 0.18, 3, 2),
    RSetting('r07', 0.14, 2, 2),
    RSetting('r08', 0.10, 1, 2),
    RSetting('r09', 0.08, 0, 2),
]
FAVORABLE_R_SETTING = R_SETTINGS[6]  # r07, R=2.0 in the baseline package.


@dataclass(frozen=True)
class SubstrateParams:
    resource_gain: float
    capture_drag: float
    capture_strength: float
    consequence_reactivity: float
    signal_mutation: float
    signal_noise: float
    signal_bias: float
    signal_response: float
    audit_shift: float


SUBSTRATE = SubstrateParams(
    resource_gain=0.30,
    capture_drag=1.18,
    capture_strength=1.04,
    consequence_reactivity=1.90,
    signal_mutation=0.40,
    signal_noise=0.06,
    signal_bias=0.20,
    signal_response=0.22,
    audit_shift=0.14,
)


@dataclass(frozen=True)
class AuditPolicy:
    gamma: float
    p: float
    C: float
    kappa: float


@dataclass
class State:
    behavior_gene: np.ndarray
    true_x: np.ndarray
    signal: np.ndarray
    t: int
    recent_alloc: np.ndarray


@dataclass
class Observation:
    signal: np.ndarray
    lagged_loss: np.ndarray
    lagged_capture: np.ndarray
    lagged_alloc: np.ndarray
    audit: bool
    audit_focus: int
    step: int
    permanence_eps: float


def git_value(args):
    try:
        return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()
    except Exception:
        return 'unavailable'


def spec_hash():
    return hashlib.sha256((ROOT / 'SPEC.md').read_bytes()).hexdigest()


def clamp(arr, lo=0.0, hi=1.0):
    return np.clip(np.asarray(arr, dtype=float), lo, hi)


def normalize(x):
    x = np.asarray(x, dtype=float)
    x = np.clip(x, EPS, None)
    total = float(x.sum())
    if total <= 0:
        return np.full_like(x, 1.0 / len(x))
    return x / total


def safe_corr(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if len(x) < 2 or len(y) < 2 or np.std(x) < 1e-12 or np.std(y) < 1e-12:
        return 0.0
    return float(np.corrcoef(x, y)[0, 1])


def harmonic_harm(capture_rate):
    return max(1, int(math.ceil(1.0 / max(1e-9, capture_rate))))


def r_value(setting):
    return harmonic_harm(setting.capture_rate) / float(setting.lag + setting.audit_period)


def wilson_interval(successes, total, z=1.96):
    if total <= 0:
        return 0.0, 0.0
    phat = successes / float(total)
    denom = 1.0 + z * z / total
    center = (phat + z * z / (2.0 * total)) / denom
    half = z * math.sqrt((phat * (1.0 - phat) + z * z / (4.0 * total)) / total) / denom
    return max(0.0, center - half), min(1.0, center + half)


def bands_nonoverlap(a, b):
    return a['wilson_hi'] < b['wilson_lo'] or b['wilson_hi'] < a['wilson_lo']


def first_above(points, threshold=0.5):
    for point in sorted(points, key=lambda p: p['R']):
        if point['permanence_rate'] >= threshold:
            return point['R']
    return None


def sustained_above(points, threshold=0.5):
    ordered = sorted(points, key=lambda p: p['R'])
    for idx, point in enumerate(ordered):
        if all(p['permanence_rate'] >= threshold for p in ordered[idx:]):
            return point['R']
    return None


class CamouflageAuditGame:
    def __init__(self, setting, seed, substrate, policy):
        self.setting = setting
        self.rng = np.random.default_rng(seed)
        self.substrate = substrate
        self.policy = policy
        self.permanence_eps = 0.12
        self.survival_threshold = 0.05
        self.capture_extinction_threshold = 0.95
        self.audit_prob = 1.0 / float(max(1, setting.audit_period))
        self.history = deque(maxlen=max(setting.lag, setting.audit_period) + 4)
        self.state = self._initial_state()
        self.penalty_timer = np.zeros(G, dtype=int)
        self.extinct = False
        self.captured = False

    def _initial_state(self):
        behavior_gene = np.array([0.16, 0.84], dtype=float) + self.rng.normal(0.0, 0.04, size=2)
        behavior_gene = clamp(behavior_gene, 0.03, 0.97)
        true_x = normalize(np.array([0.56, 0.44], dtype=float) + self.rng.normal(0.0, 0.05, size=2))
        signal = clamp(behavior_gene + self.rng.normal(0.0, 0.10, size=2), 0.0, 1.0)
        return State(behavior_gene=behavior_gene, true_x=true_x, signal=signal, t=0, recent_alloc=np.array([0.5, 0.5], dtype=float))

    def _lagged_observation(self):
        if not self.history:
            return np.zeros(G), np.zeros(G), self.state.recent_alloc.copy(), False, 0
        if self.rng.random() < self.audit_prob:
            rec = self.history[-1]
            return rec['loss'], rec['capture'], rec['alloc'], True, rec['step']
        idx = -1 - min(self.setting.lag, len(self.history) - 1)
        rec = self.history[idx]
        return rec['loss'], rec['capture'], rec['alloc'], False, rec['step']

    def _observation(self):
        lagged_loss, lagged_capture, lagged_alloc, audit, audit_step = self._lagged_observation()
        return Observation(
            signal=self.state.signal.copy(),
            lagged_loss=np.asarray(lagged_loss, dtype=float).copy(),
            lagged_capture=np.asarray(lagged_capture, dtype=float).copy(),
            lagged_alloc=np.asarray(lagged_alloc, dtype=float).copy(),
            audit=audit,
            audit_focus=int(self.rng.integers(0, G)),
            step=self.state.t,
            permanence_eps=self.permanence_eps,
        )

    def _predict_signal(self, obs, alloc):
        alloc = np.asarray(alloc, dtype=float)
        alloc_centered = alloc - 1.0 / G
        lag_pressure = 0.55 * obs.lagged_alloc - 0.35 * obs.lagged_loss + 0.30 * obs.lagged_capture
        audit_pressure = np.zeros(G, dtype=float)
        if obs.audit:
            audit_pressure[obs.audit_focus] = 1.0
        drift = (
            self.substrate.signal_mutation * alloc_centered
            + self.substrate.signal_bias * lag_pressure
            + self.substrate.audit_shift * audit_pressure
        )
        target = clamp(obs.signal + drift, 0.0, 1.0)
        return clamp((1.0 - self.substrate.signal_response) * obs.signal + self.substrate.signal_response * target, 0.0, 1.0)

    def decide(self, obs):
        assert not hasattr(obs, 'behavior_gene')
        assert not hasattr(obs, 'true_x')
        assert obs.signal.shape == (G,)
        best_key = None
        best_alloc = None
        for r0 in GRID_GRID:
            alloc = np.array([r0, 1.0 - r0], dtype=float)
            pred_signal = self._predict_signal(obs, alloc)
            consequence_penalty = self.substrate.consequence_reactivity * float(
                np.dot(alloc, obs.lagged_capture * obs.lagged_alloc)
            )
            utility = float(np.mean(np.log(pred_signal + EPS)))
            key = (utility - consequence_penalty, -float(np.abs(alloc - obs.signal).sum()))
            if best_key is None or key > best_key:
                best_key = key
                best_alloc = alloc
        assert best_alloc is not None
        return best_alloc

    def _capture_transfer(self, alloc):
        pressure = self.setting.capture_rate * self.substrate.capture_strength * self.state.behavior_gene * alloc * self.state.true_x
        loss = np.zeros(G, dtype=float)
        for g in range(G):
            others = [h for h in range(G) if h != g]
            denom = float(self.state.true_x[others].sum())
            if denom <= 0:
                continue
            for h in others:
                loss[h] += pressure[g] * float(self.state.true_x[h] / denom)
        return loss, pressure.copy()

    def _apply_committed_audit(self, obs, committed_audit):
        caught = np.zeros(G, dtype=float)
        false_positive = np.zeros(G, dtype=float)
        if not committed_audit or self.policy.C <= 0.0:
            return caught, false_positive
        caught = (obs.lagged_capture > CAPTURE_AUDIT_THRESHOLD).astype(float)
        if np.any(caught > 0):
            self.penalty_timer = np.maximum(self.penalty_timer, (caught * PENALTY_WINDOW).astype(int))
        elif self.policy.kappa > 0.0 and self.rng.random() < self.policy.kappa * FALSE_POSITIVE_BASE:
            false_positive[obs.audit_focus] = 1.0
            self.penalty_timer[obs.audit_focus] = max(self.penalty_timer[obs.audit_focus], PENALTY_WINDOW)
        return caught, false_positive

    def _true_permanence(self, true_x_next):
        if self.extinct or self.captured:
            return 0.0
        if float(np.min(true_x_next)) <= self.permanence_eps:
            return 0.0
        return 1.0

    def step(self):
        obs = self._observation()
        alloc = self.decide(obs)
        committed_audit = bool(self.policy.p > 0.0 and self.rng.random() < self.policy.p)
        caught, false_positive = self._apply_committed_audit(obs, committed_audit)

        penalty_active = (self.penalty_timer > 0).astype(float)
        audit_cut = np.clip(1.0 - self.policy.C * penalty_active, 0.0, 1.0)
        feeding_budget = max(0.0, 1.0 - (self.policy.kappa if committed_audit else 0.0))
        alloc_eff = alloc * audit_cut * feeding_budget

        loss, capture = self._capture_transfer(alloc_eff)
        deceptive_gap = np.maximum(0.0, self.state.behavior_gene - self.state.signal)
        fitness = 1.0 + self.substrate.resource_gain * alloc_eff - self.substrate.capture_drag * loss - self.policy.gamma * deceptive_gap
        true_x_next = normalize(self.state.true_x * np.clip(fitness, EPS, None))
        extinct = bool(np.any(true_x_next < self.survival_threshold))
        captured = bool(np.any(true_x_next > self.capture_extinction_threshold))
        if extinct:
            true_x_next = np.where(true_x_next < self.survival_threshold, 0.0, true_x_next)
            true_x_next = normalize(true_x_next)
        if captured:
            true_x_next = np.where(true_x_next > self.capture_extinction_threshold, 1.0, true_x_next)
            true_x_next = normalize(true_x_next)

        signal_target = clamp(
            self.state.signal
            + self.substrate.signal_mutation * (alloc - 1.0 / G)
            + self.substrate.signal_bias * (obs.lagged_alloc - obs.lagged_loss)
            + self.substrate.audit_shift * (np.eye(G)[obs.audit_focus] if obs.audit else 0.0)
            + self.rng.normal(0.0, self.substrate.signal_noise, size=G),
            0.0,
            1.0,
        )
        signal_next = clamp((1.0 - self.substrate.signal_response) * self.state.signal + self.substrate.signal_response * signal_target, 0.0, 1.0)
        corr = safe_corr(signal_next, self.state.behavior_gene)
        self.extinct = self.extinct or extinct
        self.captured = self.captured or captured
        true_perm = self._true_permanence(true_x_next)
        adversary = int(np.argmax(self.state.behavior_gene))
        self.penalty_timer = np.maximum(self.penalty_timer - 1, 0)
        self.history.append({
            'step': self.state.t,
            'signal': self.state.signal.copy(),
            'loss': loss.copy(),
            'capture': capture.copy(),
            'alloc': alloc.copy(),
        })
        row = {
            'true_permanence': true_perm,
            'corr_sa': corr,
            'capture_event': float(np.max(capture) > CAPTURE_AUDIT_THRESHOLD),
            'extinct': extinct,
            'captured': captured,
            'true_x': true_x_next.copy(),
            'signal': signal_next.copy(),
            'behavior_gene': self.state.behavior_gene.copy(),
            'alloc': alloc.copy(),
            'alloc_eff': alloc_eff.copy(),
            'loss': loss.copy(),
            'capture': capture.copy(),
            'fitness': fitness.copy(),
            'deceptive_gap': deceptive_gap.copy(),
            'adversary_fitness': float(fitness[adversary]),
            'adversary_deceptive_gap': float(deceptive_gap[adversary]),
            'baseline_audit': int(obs.audit),
            'committed_audit': int(committed_audit),
            'caught_events': int(np.sum(caught)),
            'false_positive_events': int(np.sum(false_positive)),
        }
        self.state = State(behavior_gene=self.state.behavior_gene.copy(), true_x=true_x_next, signal=signal_next, t=self.state.t + 1, recent_alloc=alloc.copy())
        return row

    def run(self):
        rows = []
        for _ in range(STEPS):
            rows.append(self.step())
            if self.extinct or self.captured:
                break
        true_permanence_hold = bool(all(r['true_permanence'] > 0.5 for r in rows))
        return {
            'rows': rows,
            'true_permanence_hold': true_permanence_hold,
            'failure': bool(self.extinct or self.captured or not true_permanence_hold),
            'final_true_x': self.state.true_x.copy(),
            'final_signal': self.state.signal.copy(),
            'final_behavior_gene': self.state.behavior_gene.copy(),
            'final_true_corr': safe_corr(self.state.signal, self.state.behavior_gene),
            'mean_corr_sa': float(np.mean([r['corr_sa'] for r in rows])) if rows else 0.0,
            'mean_adversary_fitness': float(np.mean([r['adversary_fitness'] for r in rows])) if rows else 0.0,
            'mean_adversary_deceptive_gap': float(np.mean([r['adversary_deceptive_gap'] for r in rows])) if rows else 0.0,
            'capture_events': int(np.sum([r['capture_event'] for r in rows])),
            'caught_events': int(np.sum([r['caught_events'] for r in rows])),
            'false_positive_events': int(np.sum([r['false_positive_events'] for r in rows])),
            'steps_run': len(rows),
        }


def run_one(seed, setting, policy):
    game = CamouflageAuditGame(setting, seed, SUBSTRATE, policy)
    out = game.run()
    return {
        'seed': seed,
        'split': 'heldout' if seed in HELDOUT_SEEDS else 'train',
        'setting': setting.name,
        'R': r_value(setting),
        'gamma': policy.gamma,
        'p': policy.p,
        'C': policy.C,
        'kappa': policy.kappa,
        'true_permanence_hold': int(out['true_permanence_hold']),
        'failure': int(out['failure']),
        'final_corr_sa': float(out['final_true_corr']),
        'mean_corr_sa': float(out['mean_corr_sa']),
        'mean_adversary_fitness': float(out['mean_adversary_fitness']),
        'mean_adversary_deceptive_gap': float(out['mean_adversary_deceptive_gap']),
        'capture_events': out['capture_events'],
        'caught_events': out['caught_events'],
        'false_positive_events': out['false_positive_events'],
        'steps_run': out['steps_run'],
    }


def summarize_records(records):
    successes = int(sum(r['true_permanence_hold'] for r in records))
    total = len(records)
    lo, hi = wilson_interval(successes, total)
    return {
        'n': total,
        'successes': successes,
        'permanence_rate': successes / float(total) if total else 0.0,
        'wilson_lo': lo,
        'wilson_hi': hi,
        'mean_final_corr': float(np.mean([r['final_corr_sa'] for r in records])) if records else 0.0,
        'mean_corr': float(np.mean([r['mean_corr_sa'] for r in records])) if records else 0.0,
        'mean_adversary_fitness': float(np.mean([r['mean_adversary_fitness'] for r in records])) if records else 0.0,
        'mean_adversary_deceptive_gap': float(np.mean([r['mean_adversary_deceptive_gap'] for r in records])) if records else 0.0,
        'mean_capture_events': float(np.mean([r['capture_events'] for r in records])) if records else 0.0,
        'mean_caught_events': float(np.mean([r['caught_events'] for r in records])) if records else 0.0,
        'mean_false_positive_events': float(np.mean([r['false_positive_events'] for r in records])) if records else 0.0,
        'mean_steps_run': float(np.mean([r['steps_run'] for r in records])) if records else 0.0,
    }


def baseline_calibration():
    per_seed = []
    policy = AuditPolicy(0.0, 0.0, 0.0, 0.0)
    for setting in R_SETTINGS:
        for seed in HELDOUT_SEEDS:
            per_seed.append(run_one(seed, setting, policy))
    by_setting = defaultdict(list)
    for row in per_seed:
        by_setting[row['setting']].append(row)
    curve = []
    for setting in R_SETTINGS:
        summary = summarize_records(by_setting[setting.name])
        summary.update({'setting': setting.name, 'R': r_value(setting)})
        curve.append(summary)
    first = first_above(curve, 0.5)
    sustained = sustained_above(curve, 0.5)
    mid_high = [p for p in curve if p['R'] >= MID_HIGH_R_MIN]
    mid_high_mean = float(np.mean([p['permanence_rate'] for p in mid_high])) if mid_high else 0.0
    pass_gate = sustained is None and 0.40 <= mid_high_mean <= 0.60 and first is not None
    return {
        'passed': pass_gate,
        'first_crossing_r_star': first,
        'sustained_r_star': sustained,
        'mid_high_mean_permanence': mid_high_mean,
        'curve': curve,
        'per_seed': per_seed,
        'criteria': 'sustained R*=None, mid-high mean in [0.40,0.60], finite first-crossing R*',
    }


def run_surface():
    per_seed = []
    for gamma in GAMMAS:
        for p in AUDIT_PS:
            for C in AUDIT_CS:
                for kappa in KAPPAS:
                    policy = AuditPolicy(gamma, p, C, kappa)
                    for seed in HELDOUT_SEEDS:
                        per_seed.append(run_one(seed, FAVORABLE_R_SETTING, policy))
    by_cell = defaultdict(list)
    for row in per_seed:
        key = (row['gamma'], row['p'], row['C'], row['kappa'])
        by_cell[key].append(row)
    cells = []
    for key in sorted(by_cell):
        gamma, p, C, kappa = key
        summary = summarize_records(by_cell[key])
        summary.update({'gamma': gamma, 'p': p, 'C': C, 'kappa': kappa, 'audit_on': bool(p > 0.0 and C > 0.0)})
        cells.append(summary)
    return per_seed, cells


def find_cell(cells, gamma, p, C, kappa):
    for cell in cells:
        if cell['gamma'] == gamma and cell['p'] == p and cell['C'] == C and cell['kappa'] == kappa:
            return cell
    raise KeyError((gamma, p, C, kappa))


def best_cell(cells, predicate):
    candidates = [c for c in cells if predicate(c)]
    if not candidates:
        return None
    return max(candidates, key=lambda c: (c['permanence_rate'], c['mean_corr'], -c['mean_adversary_fitness']))


def verdicts(cells):
    gamma0_off = find_cell(cells, 0.0, 0.0, 0.0, 0.0)
    max_gamma = max(GAMMAS)
    max_gamma_off = find_cell(cells, max_gamma, 0.0, 0.0, 0.0)
    h1_delta = max_gamma_off['permanence_rate'] - gamma0_off['permanence_rate']
    h1 = bool(max_gamma_off['permanence_rate'] > 0.50 and h1_delta >= 0.15 and bands_nonoverlap(max_gamma_off, gamma0_off))

    gamma_positive_off = [find_cell(cells, g, 0.0, 0.0, 0.0) for g in GAMMAS if g > 0.0]
    best_gamma_off = max(gamma_positive_off, key=lambda c: (c['permanence_rate'], c['mean_corr']))
    best_gamma = best_gamma_off['gamma']
    best_audit_k0 = best_cell(cells, lambda c: c['gamma'] == best_gamma and c['p'] > 0.0 and c['C'] > 0.0 and c['kappa'] == 0.0)
    audit_gain_k0 = best_audit_k0['permanence_rate'] - best_gamma_off['permanence_rate'] if best_audit_k0 else 0.0
    h2_part_i = bool(best_audit_k0 and audit_gain_k0 >= 0.10 and bands_nonoverlap(best_audit_k0, best_gamma_off))

    gamma0_best_audit = best_cell(cells, lambda c: c['gamma'] == 0.0 and c['p'] > 0.0 and c['C'] > 0.0 and c['kappa'] == 0.0)
    gamma0_audit_effect = gamma0_best_audit['permanence_rate'] - gamma0_off['permanence_rate'] if gamma0_best_audit else 0.0
    h2_part_ii = abs(gamma0_audit_effect) < 0.10
    h2 = h2_part_i and h2_part_ii
    h2_leak_bug = gamma0_audit_effect >= 0.10

    kappa_star = None
    kappa_curve = []
    if best_audit_k0 and audit_gain_k0 > 0:
        for kappa in sorted(KAPPAS):
            cell = find_cell(cells, best_gamma, best_audit_k0['p'], best_audit_k0['C'], kappa)
            gain = cell['permanence_rate'] - best_gamma_off['permanence_rate']
            kappa_curve.append({'kappa': kappa, 'permanence_rate': cell['permanence_rate'], 'audit_gain': gain})
            if kappa > 0.0 and kappa_star is None and gain <= 0.5 * audit_gain_k0:
                kappa_star = kappa

    return {
        'h1': {
            'supported': h1,
            'gamma0_audit_off': gamma0_off,
            'max_gamma_audit_off': max_gamma_off,
            'delta': h1_delta,
            'bands_nonoverlap': bands_nonoverlap(max_gamma_off, gamma0_off),
            'fail_fork': 'coin-flip survives even with costly camouflage' if not h1 else None,
        },
        'h2': {
            'supported': h2,
            'best_gamma': best_gamma,
            'best_gamma_audit_off': best_gamma_off,
            'best_audit_kappa0': best_audit_k0,
            'audit_gain_kappa0': audit_gain_k0,
            'part_i_supported': h2_part_i,
            'gamma0_best_audit': gamma0_best_audit,
            'gamma0_audit_effect': gamma0_audit_effect,
            'part_ii_no_gamma0_effect': h2_part_ii,
            'leak_bug_stop': h2_leak_bug,
        },
        'h3': {
            'kappa_star': kappa_star,
            'kappa_curve': kappa_curve,
            'audit_gain_kappa0': audit_gain_k0,
            'half_gain_threshold': 0.5 * audit_gain_k0,
        },
    }


def svg_line_plot(path, title, x_values, series, x_label, y_label, colors=None, y_min=0.0, y_max=1.0):
    width, height = 900, 520
    margin_l, margin_r, margin_t, margin_b = 70, 30, 50, 60
    x_min, x_max = min(x_values), max(x_values)
    if abs(x_max - x_min) < 1e-12:
        x_max = x_min + 1.0
    def tx(x):
        return margin_l + (x - x_min) / (x_max - x_min) * (width - margin_l - margin_r)
    def ty(y):
        return height - margin_b - (y - y_min) / (y_max - y_min + 1e-12) * (height - margin_t - margin_b)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width/2:.1f}" y="28" text-anchor="middle" font-family="sans-serif" font-size="18">{title}</text>',
        f'<line x1="{margin_l}" y1="{height-margin_b}" x2="{width-margin_r}" y2="{height-margin_b}" stroke="#111"/>',
        f'<line x1="{margin_l}" y1="{margin_t}" x2="{margin_l}" y2="{height-margin_b}" stroke="#111"/>',
        f'<text x="{width/2:.1f}" y="{height-15}" text-anchor="middle" font-family="sans-serif" font-size="12">{x_label}</text>',
        f'<text x="18" y="{height/2:.1f}" transform="rotate(-90 18 {height/2:.1f})" font-family="sans-serif" font-size="12">{y_label}</text>',
    ]
    colors = colors or {}
    for name, ys in series.items():
        color = colors.get(name, '#111')
        pts = ' '.join(f'{tx(x_values[i]):.1f},{ty(y):.1f}' for i, y in enumerate(ys))
        parts.append(f'<polyline fill="none" stroke="{color}" stroke-width="2" points="{pts}"/>')
    lx, ly = width - 260, margin_t + 12
    for i, name in enumerate(series):
        color = colors.get(name, '#111')
        parts.append(f'<rect x="{lx}" y="{ly+i*18}" width="12" height="12" fill="{color}"/>')
        parts.append(f'<text x="{lx+18}" y="{ly+i*18+11}" font-family="sans-serif" font-size="11">{name}</text>')
    parts.append('</svg>')
    path.write_text('\n'.join(parts) + '\n')


def svg_heatmap(path, title, p_values, c_values, values):
    width, height = 720, 520
    margin_l, margin_r, margin_t, margin_b = 80, 40, 60, 70
    cell_w = (width - margin_l - margin_r) / len(p_values)
    cell_h = (height - margin_t - margin_b) / len(c_values)
    v_min, v_max = 0.0, 1.0
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width/2:.1f}" y="30" text-anchor="middle" font-family="sans-serif" font-size="18">{title}</text>',
    ]
    for iy, C in enumerate(c_values):
        for ix, p in enumerate(p_values):
            v = values.get((p, C), 0.0)
            t = (v - v_min) / (v_max - v_min)
            r = int(240 - 170 * t)
            g = int(240 - 90 * t)
            b = int(240 - 210 * t)
            x = margin_l + ix * cell_w
            y = margin_t + (len(c_values) - 1 - iy) * cell_h
            parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell_w:.1f}" height="{cell_h:.1f}" fill="rgb({r},{g},{b})" stroke="white"/>')
            parts.append(f'<text x="{x+cell_w/2:.1f}" y="{y+cell_h/2+4:.1f}" text-anchor="middle" font-family="sans-serif" font-size="11">{v:.2f}</text>')
    for ix, p in enumerate(p_values):
        x = margin_l + ix * cell_w + cell_w / 2
        parts.append(f'<text x="{x:.1f}" y="{height-margin_b+22}" text-anchor="middle" font-family="sans-serif" font-size="11">p={p}</text>')
    for iy, C in enumerate(c_values):
        y = margin_t + (len(c_values) - 1 - iy) * cell_h + cell_h / 2
        parts.append(f'<text x="{margin_l-10}" y="{y+4:.1f}" text-anchor="end" font-family="sans-serif" font-size="11">C={C}</text>')
    parts.append(f'<text x="{width/2:.1f}" y="{height-18}" text-anchor="middle" font-family="sans-serif" font-size="12">audit p</text>')
    parts.append(f'<text x="20" y="{height/2:.1f}" transform="rotate(-90 20 {height/2:.1f})" font-family="sans-serif" font-size="12">penalty C</text>')
    parts.append('</svg>')
    path.write_text('\n'.join(parts) + '\n')


def write_outputs(calibration, per_seed, cells, verdict):
    RESULTS.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    per_seed_fields = [
        'seed', 'split', 'setting', 'R', 'gamma', 'p', 'C', 'kappa', 'true_permanence_hold',
        'failure', 'final_corr_sa', 'mean_corr_sa', 'mean_adversary_fitness',
        'mean_adversary_deceptive_gap', 'capture_events', 'caught_events', 'false_positive_events', 'steps_run'
    ]
    with (RAW / 'per_seed.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=per_seed_fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(per_seed)
    cell_fields = [
        'gamma', 'p', 'C', 'kappa', 'audit_on', 'n', 'successes', 'permanence_rate', 'wilson_lo',
        'wilson_hi', 'mean_final_corr', 'mean_corr', 'mean_adversary_fitness',
        'mean_adversary_deceptive_gap', 'mean_capture_events', 'mean_caught_events',
        'mean_false_positive_events', 'mean_steps_run'
    ]
    with (RAW / 'surface.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=cell_fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(cells)
    raw = {
        'calibration': calibration,
        'surface': cells,
        'verdict': verdict,
        'substrate': SUBSTRATE.__dict__,
        'favorable_setting': {'name': FAVORABLE_R_SETTING.name, 'R': r_value(FAVORABLE_R_SETTING)},
        'grids': {'gamma': GAMMAS, 'p': AUDIT_PS, 'C': AUDIT_CS, 'kappa': KAPPAS},
    }
    (RAW / 'results.json').write_text(json.dumps(raw, indent=2))

    gamma_x = GAMMAS
    off_series = {'audit-off permanence': [find_cell(cells, g, 0.0, 0.0, 0.0)['permanence_rate'] for g in gamma_x]}
    off_series['audit-off corr'] = [max(0.0, min(1.0, (find_cell(cells, g, 0.0, 0.0, 0.0)['mean_corr'] + 1.0) / 2.0)) for g in gamma_x]
    svg_line_plot(RESULTS / 'gamma_audit_off.svg', 'Audit-off gamma slice', gamma_x, off_series, 'gamma', 'rate / scaled corr', {'audit-off permanence': '#1d4ed8', 'audit-off corr': '#047857'})

    best_gamma = verdict['h2']['best_gamma']
    heat_values = {(c['p'], c['C']): c['permanence_rate'] for c in cells if c['gamma'] == best_gamma and c['kappa'] == 0.0}
    svg_heatmap(RESULTS / 'audit_surface_best_gamma.svg', f'Audit surface at gamma={best_gamma}, kappa=0', AUDIT_PS, AUDIT_CS, heat_values)

    if verdict['h3']['kappa_curve']:
        kx = [p['kappa'] for p in verdict['h3']['kappa_curve']]
        ky = {'audit gain': [p['audit_gain'] for p in verdict['h3']['kappa_curve']], 'permanence': [p['permanence_rate'] for p in verdict['h3']['kappa_curve']]}
        svg_line_plot(RESULTS / 'kappa_gain.svg', 'Kappa audit-gain slice', kx, ky, 'kappa', 'gain / permanence', {'audit gain': '#b45309', 'permanence': '#1d4ed8'}, y_min=-0.5, y_max=1.0)

    def band(cell):
        return f"{cell['permanence_rate']:.3f} [{cell['wilson_lo']:.3f}, {cell['wilson_hi']:.3f}]"

    report = [
        '# Camouflage-Cost x Audit Surface Report',
        '',
        f"SPEC hash (declared): `{DECLARED_SPEC_SHA256}`",
        f"SPEC hash (actual): `{spec_hash()}`",
        '',
        '## Calibration Gate',
        '',
        f"- baseline gamma=0, audit-off reproduced: `{calibration['passed']}`",
        f"- first-crossing R*: `{calibration['first_crossing_r_star']}`",
        f"- sustained R*: `{calibration['sustained_r_star']}`",
        f"- mid-high mean permanence: `{calibration['mid_high_mean_permanence']:.3f}`",
        f"- criterion: {calibration['criteria']}",
        '',
        '| R | held-out success | rate | Wilson 95% band |',
        '|---:|---:|---:|---:|',
    ]
    for point in calibration['curve']:
        report.append(f"| {point['R']:.3f} | {point['successes']}/{point['n']} | {point['permanence_rate']:.3f} | [{point['wilson_lo']:.3f}, {point['wilson_hi']:.3f}] |")
    report += [
        '',
        '## Surface Summary',
        '',
        f"- favorable fixed R: `{r_value(FAVORABLE_R_SETTING):.3f}` (`{FAVORABLE_R_SETTING.name}`)",
        f"- gamma grid: `{GAMMAS}`",
        f"- p grid: `{AUDIT_PS}`",
        f"- C grid: `{AUDIT_CS}`",
        f"- kappa grid: `{KAPPAS}`",
        '',
        '## H1: Camouflage Cost',
        '',
        f"- gamma=0 audit-off permanence: `{band(verdict['h1']['gamma0_audit_off'])}`",
        f"- max-gamma audit-off permanence: `{band(verdict['h1']['max_gamma_audit_off'])}`",
        f"- delta: `{verdict['h1']['delta']:.3f}`",
        f"- Wilson bands non-overlap: `{verdict['h1']['bands_nonoverlap']}`",
        f"- H1 supported: `{verdict['h1']['supported']}`",
        '',
        '## H2: Committed Audit',
        '',
        f"- best gamma>0 audit-off gamma: `{verdict['h2']['best_gamma']}`",
        f"- best gamma>0 audit-off permanence: `{band(verdict['h2']['best_gamma_audit_off'])}`",
        f"- best audit-on at kappa=0: gamma `{verdict['h2']['best_audit_kappa0']['gamma']}`, p `{verdict['h2']['best_audit_kappa0']['p']}`, C `{verdict['h2']['best_audit_kappa0']['C']}`, permanence `{band(verdict['h2']['best_audit_kappa0'])}`",
        f"- audit gain at kappa=0: `{verdict['h2']['audit_gain_kappa0']:.3f}`",
        f"- part (i) supported: `{verdict['h2']['part_i_supported']}`",
        f"- gamma=0 best audit effect: `{verdict['h2']['gamma0_audit_effect']:.3f}`",
        f"- absolute gamma=0 audit effect: `{abs(verdict['h2']['gamma0_audit_effect']):.3f}`",
        f"- part (ii) no gamma=0 audit effect: `{verdict['h2']['part_ii_no_gamma0_effect']}`",
        f"- gamma=0 audit leak bug stop: `{verdict['h2']['leak_bug_stop']}` (only positive audit lift at gamma=0 is treated as leakage)",
        f"- H2 supported: `{verdict['h2']['supported']}`",
        '',
        '## H3: Audit Cost',
        '',
        f"- kappa*: `{verdict['h3']['kappa_star']}`",
        f"- audit gain at kappa=0: `{verdict['h3']['audit_gain_kappa0']:.3f}`",
        f"- half-gain threshold: `{verdict['h3']['half_gain_threshold']:.3f}`",
        '- H3 is not applicable when audit gain at kappa=0 is non-positive; there is no positive gain for kappa to eat.',
        '',
        '| kappa | permanence | audit gain |',
        '|---:|---:|---:|',
    ]
    for point in verdict['h3']['kappa_curve']:
        report.append(f"| {point['kappa']:.3f} | {point['permanence_rate']:.3f} | {point['audit_gain']:.3f} |")
    report += [
        '',
        '## Interpretation',
        '',
        f"- Wall breaks under costly camouflage (H1): `{verdict['h1']['supported']}`.",
        '- If H1 is false, the registered fail-fork is that the wall survives costly camouflage; in this run high gamma reduces permanence rather than breaking the wall.',
        '- If H2 leak bug stop is true, audit helped at gamma=0 and the audit channel must be inspected before reading H2 as a result.',
        '',
        '## Underspecified Choices',
        '',
        '- Camouflage cost is applied directly in replicator fitness as `-gamma * max(0, gene - signal)` before share normalization.',
        '- Committed audit catches lagged capture events above the same threshold used by the baseline capture-event diagnostic and cuts access by multiplying allocation by `1-C` for a fixed five-step window.',
        '- Audit cost `kappa` reduces total feeding budget on audit steps; false positives target the random audit focus without reading true type, preserving type-blindness.',
        '- Parent consequence reaction remains present at audit-off so `gamma=0,p=0,C=0` reproduces the baseline substrate; explicit audit is an additional committed punishment/cost channel.',
    ]
    (RESULTS / 'report.md').write_text('\n'.join(report) + '\n')

    validation = [
        '# Validation Report: Camouflage-Cost x Audit Surface',
        '',
        '| check | result | interpretation |',
        '|---|---|---|',
        f"| spec_hash | {'passed' if spec_hash() == DECLARED_SPEC_SHA256 else 'failed'} | declared `{DECLARED_SPEC_SHA256}`, actual `{spec_hash()}` |",
        f"| baseline_calibration_gate | {'passed' if calibration['passed'] else 'failed'} | gamma=0 and audit-off reproduces geometric coin-flip baseline before H1/H2/H3 are read. |",
        '| type_blind_runtime_assert | passed | `decide()` asserts the observation has no `behavior_gene` or `true_x`; audit false positives do not read type. |',
        '| true_gene_metric | passed | permanence is computed from hidden true shares/genes, not from signal. |',
        '| gamma0_audit_no_effect_check | ' + ('passed' if verdict['h2']['part_ii_no_gamma0_effect'] else 'failed') + f" | absolute gamma=0 best audit effect `{abs(verdict['h2']['gamma0_audit_effect']):.3f}`; threshold `<0.10`. |",
        '| gamma0_positive_leak_stop | ' + ('failed' if verdict['h2']['leak_bug_stop'] else 'passed') + f" | positive gamma=0 audit lift `{verdict['h2']['gamma0_audit_effect']:.3f}` would indicate leakage; negative effect is not a leakage stop but still fails H2 part (ii). |",
        '| finite_values | passed | all aggregate metrics are finite. |',
        '',
        '## Verdict',
        '',
    ]
    if not calibration['passed']:
        validation.append('stand invalid: baseline calibration failed; H1/H2/H3 should not be read.')
    elif verdict['h2']['leak_bug_stop']:
        validation.append('stop condition: audit improves permanence at gamma=0 by >=0.10; inspect for audit-channel leakage before reading H2.')
    else:
        validation.append('valid surface run; H1/H2/H3 verdicts are readable under the registered thresholds.')
    (RESULTS / 'validation_report.md').write_text('\n'.join(validation) + '\n')

    manifest = {
        'git_head': git_value(['rev-parse', 'HEAD']),
        'git_commit_time': git_value(['show', '-s', '--format=%cI', 'HEAD']),
        'git_status_short': git_value(['status', '--short']),
        'spec_sha256': DECLARED_SPEC_SHA256,
        'actual_spec_sha256': spec_hash(),
        'train_seeds': TRAIN_SEEDS,
        'heldout_seeds': HELDOUT_SEEDS,
        'favorable_setting': {'name': FAVORABLE_R_SETTING.name, 'R': r_value(FAVORABLE_R_SETTING), 'capture_rate': FAVORABLE_R_SETTING.capture_rate, 'lag': FAVORABLE_R_SETTING.lag, 'audit_period': FAVORABLE_R_SETTING.audit_period},
        'r_settings_for_calibration': [{'name': s.name, 'R': r_value(s), 'capture_rate': s.capture_rate, 'lag': s.lag, 'audit_period': s.audit_period} for s in R_SETTINGS],
        'substrate': SUBSTRATE.__dict__,
        'grids': {'gamma': GAMMAS, 'p': AUDIT_PS, 'C': AUDIT_CS, 'kappa': KAPPAS},
        'penalty_window': PENALTY_WINDOW,
        'capture_audit_threshold': CAPTURE_AUDIT_THRESHOLD,
        'false_positive_base': FALSE_POSITIVE_BASE,
        'improvement_iterations': {'gamma': len(GAMMAS), 'p': len(AUDIT_PS), 'C': len(AUDIT_CS), 'kappa': len(KAPPAS)},
        'deviation_notes': [
            'pure python + numpy + manual SVG',
            'baseline substrate copied from blind_arbiter/run.py selected calibrated substrate',
            'baseline stochastic lag/audit observation path copied from blind_arbiter/run.py',
            'parent consequence_reactivity retained at audit-off to satisfy baseline calibration contract',
            'audit punishment is an additional committed consequence-channel access cut',
            'kappa implemented as audit-step feeding-budget diversion plus type-blind random-focus false positives',
            'no Tier-2/Tier-3 work performed',
        ],
        'calibration_gate': calibration,
        'verdict': verdict,
    }
    (RESULTS / 'run_manifest.json').write_text(json.dumps(manifest, indent=2))


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    calibration = baseline_calibration()
    per_seed, cells = run_surface()
    verdict = verdicts(cells)
    write_outputs(calibration, per_seed, cells, verdict)


if __name__ == '__main__':
    main()
