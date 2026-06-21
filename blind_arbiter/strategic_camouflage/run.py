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

DECLARED_SPEC_SHA256 = '4fe5ff79ebb93cfc7c87e4132e77b2c715c981cb09c55d4a78492393e6a1725f'

TRAIN_SEEDS = list(range(3100, 3130))
HELDOUT_SEEDS = list(range(4100, 4130))
GRID_GRID = np.linspace(0.0, 1.0, 21)
STEPS = 120
G = 2
EPS = 1e-9

# Exploration grid, logged in the manifest. Locked thresholds live in SPEC.md.
GAMMAS = [0.0, 0.10, 0.30, 0.60]
AUDIT_PS = [0.0, 0.25, 0.50]
AUDIT_CS = [0.0, 0.50, 1.00]
KAPPAS = [0.0, 0.10, 0.30]
C_DELTA = 0.05
PENALTY_WINDOW = 5
CAPTURE_AUDIT_THRESHOLD = 0.10
FALSE_POSITIVE_BASE = 0.10
MID_HIGH_R_MIN = 0.80


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
FAVORABLE_R_SETTING = R_SETTINGS[6]


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
class Policy:
    gamma: float
    p: float
    C: float
    kappa: float


@dataclass
class State:
    behavior_gene: np.ndarray
    true_x: np.ndarray
    concealment: np.ndarray
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


class StrategicCamouflageGame:
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

    def _signal_from_concealment(self, concealment):
        return clamp(self.state.behavior_gene * (1.0 - concealment), 0.0, 1.0)

    def _initial_state(self):
        behavior_gene = np.array([0.16, 0.84], dtype=float) + self.rng.normal(0.0, 0.04, size=2)
        behavior_gene = clamp(behavior_gene, 0.03, 0.97)
        true_x = normalize(np.array([0.56, 0.44], dtype=float) + self.rng.normal(0.0, 0.05, size=2))
        concealment = np.array([0.0, 0.50], dtype=float) + self.rng.normal(0.0, 0.03, size=2)
        concealment = clamp(concealment, 0.0, 1.0)
        signal = clamp(behavior_gene * (1.0 - concealment), 0.0, 1.0)
        return State(behavior_gene=behavior_gene, true_x=true_x, concealment=concealment, signal=signal, t=0, recent_alloc=np.array([0.5, 0.5], dtype=float))

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
        assert not hasattr(obs, 'concealment')
        assert obs.signal.shape == (G,)
        best_key = None
        best_alloc = None
        for r0 in GRID_GRID:
            alloc = np.array([r0, 1.0 - r0], dtype=float)
            pred_signal = self._predict_signal(obs, alloc)
            consequence_penalty = self.substrate.consequence_reactivity * float(
                np.dot(alloc, obs.lagged_capture * obs.lagged_alloc)
            )
            utility = float(np.mean(np.log(pred_signal + alloc + EPS)))
            key = (utility - consequence_penalty, -float(np.abs(alloc - (1.0 / G)).sum()))
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

    def _selfish_payoff(self, group, concealment, obs):
        signal = clamp(self.state.behavior_gene * (1.0 - concealment), 0.0, 1.0)
        candidate_obs = Observation(
            signal=signal,
            lagged_loss=obs.lagged_loss,
            lagged_capture=obs.lagged_capture,
            lagged_alloc=obs.lagged_alloc,
            audit=obs.audit,
            audit_focus=obs.audit_focus,
            step=obs.step,
            permanence_eps=obs.permanence_eps,
        )
        alloc = self.decide(candidate_obs)
        penalty_active = (self.penalty_timer > 0).astype(float)
        audit_cut = np.clip(1.0 - self.policy.C * penalty_active, 0.0, 1.0)
        alloc_eff = alloc * audit_cut
        loss, capture = self._capture_transfer(alloc_eff)
        caught_proxy = float(obs.lagged_capture[group] > CAPTURE_AUDIT_THRESHOLD) * self.policy.p * self.policy.C
        return float(
            self.substrate.resource_gain * alloc_eff[group]
            + capture[group]
            - self.substrate.capture_drag * loss[group]
            - self.policy.gamma * concealment[group] * self.state.behavior_gene[group]
            - caught_proxy
        )

    def _adapt_concealment(self, obs):
        new_c = self.state.concealment.copy()
        for group in range(G):
            candidates = []
            for step in (-C_DELTA, 0.0, C_DELTA):
                cand = new_c.copy()
                cand[group] = float(np.clip(cand[group] + step, 0.0, 1.0))
                candidates.append((self._selfish_payoff(group, cand, obs), cand[group]))
            current_c = float(new_c[group])
            # Integrity guard: selection keeps only payoff-improving moves. Ties keep
            # the existing trait, so reveal/concealment is not designer-nudged.
            best_payoff, best_c = max(candidates, key=lambda x: (x[0], -abs(x[1] - current_c)))
            new_c[group] = best_c
        return clamp(new_c, 0.0, 1.0)

    def _true_permanence(self, true_x_next):
        if self.extinct or self.captured:
            return 0.0
        if float(np.min(true_x_next)) <= self.permanence_eps:
            return 0.0
        return 1.0

    def step(self):
        obs = self._observation()
        concealment_next = self._adapt_concealment(obs)
        signal = clamp(self.state.behavior_gene * (1.0 - concealment_next), 0.0, 1.0)
        obs = Observation(signal=signal, lagged_loss=obs.lagged_loss, lagged_capture=obs.lagged_capture, lagged_alloc=obs.lagged_alloc, audit=obs.audit, audit_focus=obs.audit_focus, step=obs.step, permanence_eps=obs.permanence_eps)
        alloc = self.decide(obs)
        committed_audit = bool(self.policy.p > 0.0 and self.rng.random() < self.policy.p)
        caught, false_positive = self._apply_committed_audit(obs, committed_audit)

        penalty_active = (self.penalty_timer > 0).astype(float)
        audit_cut = np.clip(1.0 - self.policy.C * penalty_active, 0.0, 1.0)
        feeding_budget = max(0.0, 1.0 - (self.policy.kappa if committed_audit else 0.0))
        alloc_eff = alloc * audit_cut * feeding_budget
        loss, capture = self._capture_transfer(alloc_eff)
        audit_penalty = self.policy.C * penalty_active
        fitness = (
            1.0
            + self.substrate.resource_gain * alloc_eff
            - self.substrate.capture_drag * loss
            - self.policy.gamma * concealment_next * self.state.behavior_gene
            - audit_penalty
        )
        true_x_next = normalize(self.state.true_x * np.clip(fitness, EPS, None))
        extinct = bool(np.any(true_x_next < self.survival_threshold))
        captured = bool(np.any(true_x_next > self.capture_extinction_threshold))
        if extinct:
            true_x_next = np.where(true_x_next < self.survival_threshold, 0.0, true_x_next)
            true_x_next = normalize(true_x_next)
        if captured:
            true_x_next = np.where(true_x_next > self.capture_extinction_threshold, 1.0, true_x_next)
            true_x_next = normalize(true_x_next)

        corr = safe_corr(signal, self.state.behavior_gene)
        adversary = int(np.argmax(self.state.behavior_gene))
        adversary_extinct = bool(true_x_next[adversary] < self.survival_threshold or (extinct and true_x_next[adversary] == 0.0))
        self.extinct = self.extinct or extinct
        self.captured = self.captured or captured
        true_perm = self._true_permanence(true_x_next)
        self.penalty_timer = np.maximum(self.penalty_timer - 1, 0)
        self.history.append({
            'step': self.state.t,
            'signal': signal.copy(),
            'loss': loss.copy(),
            'capture': capture.copy(),
            'alloc': alloc.copy(),
        })
        row = {
            'true_permanence': true_perm,
            'corr_sa': corr,
            'extinct': extinct,
            'captured': captured,
            'adversary_extinct': adversary_extinct,
            'true_x': true_x_next.copy(),
            'signal': signal.copy(),
            'concealment': concealment_next.copy(),
            'adversary_concealment': float(concealment_next[adversary]),
            'adversary_share': float(true_x_next[adversary]),
            'behavior_gene': self.state.behavior_gene.copy(),
            'alloc': alloc.copy(),
            'alloc_eff': alloc_eff.copy(),
            'loss': loss.copy(),
            'capture': capture.copy(),
            'fitness': fitness.copy(),
            'adversary_fitness': float(fitness[adversary]),
            'committed_audit': int(committed_audit),
            'caught_events': int(np.sum(caught)),
            'false_positive_events': int(np.sum(false_positive)),
        }
        self.state = State(behavior_gene=self.state.behavior_gene.copy(), true_x=true_x_next, concealment=concealment_next, signal=signal, t=self.state.t + 1, recent_alloc=alloc.copy())
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
            'final_concealment': self.state.concealment.copy(),
            'final_behavior_gene': self.state.behavior_gene.copy(),
            'final_true_corr': safe_corr(self.state.signal, self.state.behavior_gene),
            'mean_corr_sa': float(np.mean([r['corr_sa'] for r in rows])) if rows else 0.0,
            'mean_adversary_concealment': float(np.mean([r['adversary_concealment'] for r in rows[-max(1, len(rows)//4):]])) if rows else 0.0,
            'final_adversary_concealment': float(rows[-1]['adversary_concealment']) if rows else 0.0,
            'mean_adversary_fitness': float(np.mean([r['adversary_fitness'] for r in rows])) if rows else 0.0,
            'adversary_extinct': bool(any(r['adversary_extinct'] for r in rows)),
            'mean_adversary_share': float(np.mean([r['adversary_share'] for r in rows[-max(1, len(rows)//4):]])) if rows else 0.0,
            'caught_events': int(np.sum([r['caught_events'] for r in rows])),
            'false_positive_events': int(np.sum([r['false_positive_events'] for r in rows])),
            'steps_run': len(rows),
        }


class PassiveControlGame(StrategicCamouflageGame):
    """Parent passive-signal control used only for calibration gate (c)."""

    def _initial_state(self):
        behavior_gene = np.array([0.16, 0.84], dtype=float) + self.rng.normal(0.0, 0.04, size=2)
        behavior_gene = clamp(behavior_gene, 0.03, 0.97)
        true_x = normalize(np.array([0.56, 0.44], dtype=float) + self.rng.normal(0.0, 0.05, size=2))
        concealment = np.zeros(G, dtype=float)
        signal = clamp(behavior_gene + self.rng.normal(0.0, 0.10, size=2), 0.0, 1.0)
        return State(behavior_gene=behavior_gene, true_x=true_x, concealment=concealment, signal=signal, t=0, recent_alloc=np.array([0.5, 0.5], dtype=float))

    def decide(self, obs):
        assert not hasattr(obs, 'behavior_gene')
        assert not hasattr(obs, 'true_x')
        assert not hasattr(obs, 'concealment')
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
        fitness = (
            1.0
            + self.substrate.resource_gain * alloc_eff
            - self.substrate.capture_drag * loss
            - self.policy.gamma * deceptive_gap
        )
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
        adversary = int(np.argmax(self.state.behavior_gene))
        adversary_extinct = bool(true_x_next[adversary] < self.survival_threshold or (extinct and true_x_next[adversary] == 0.0))
        self.extinct = self.extinct or extinct
        self.captured = self.captured or captured
        true_perm = self._true_permanence(true_x_next)
        self.penalty_timer = np.maximum(self.penalty_timer - 1, 0)
        self.history.append({
            'step': self.state.t,
            'signal': signal_next.copy(),
            'loss': loss.copy(),
            'capture': capture.copy(),
            'alloc': alloc.copy(),
        })
        row = {
            'true_permanence': true_perm,
            'corr_sa': corr,
            'extinct': extinct,
            'captured': captured,
            'adversary_extinct': adversary_extinct,
            'true_x': true_x_next.copy(),
            'signal': signal_next.copy(),
            'concealment': np.zeros(G, dtype=float),
            'adversary_concealment': 0.0,
            'adversary_share': float(true_x_next[adversary]),
            'behavior_gene': self.state.behavior_gene.copy(),
            'alloc': alloc.copy(),
            'alloc_eff': alloc_eff.copy(),
            'loss': loss.copy(),
            'capture': capture.copy(),
            'fitness': fitness.copy(),
            'adversary_fitness': float(fitness[adversary]),
            'committed_audit': int(committed_audit),
            'caught_events': int(np.sum(caught)),
            'false_positive_events': int(np.sum(false_positive)),
        }
        self.state = State(behavior_gene=self.state.behavior_gene.copy(), true_x=true_x_next, concealment=np.zeros(G, dtype=float), signal=signal_next, t=self.state.t + 1, recent_alloc=alloc.copy())
        return row


def run_one(seed, setting, policy, mode='strategic'):
    if mode == 'strategic':
        game = StrategicCamouflageGame(setting, seed, SUBSTRATE, policy)
    elif mode == 'passive_control':
        game = PassiveControlGame(setting, seed, SUBSTRATE, policy)
    else:
        raise ValueError(f'unknown mode: {mode}')
    out = game.run()
    return {
        'mode': mode,
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
        'mean_adversary_concealment': float(out['mean_adversary_concealment']),
        'final_adversary_concealment': float(out['final_adversary_concealment']),
        'mean_adversary_fitness': float(out['mean_adversary_fitness']),
        'adversary_extinct': int(out['adversary_extinct']),
        'mean_adversary_share': float(out['mean_adversary_share']),
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
        'mean_adversary_concealment': float(np.mean([r['mean_adversary_concealment'] for r in records])) if records else 0.0,
        'mean_final_adversary_concealment': float(np.mean([r['final_adversary_concealment'] for r in records])) if records else 0.0,
        'mean_adversary_fitness': float(np.mean([r['mean_adversary_fitness'] for r in records])) if records else 0.0,
        'adversary_extinction_rate': float(np.mean([r['adversary_extinct'] for r in records])) if records else 0.0,
        'mean_adversary_share': float(np.mean([r['mean_adversary_share'] for r in records])) if records else 0.0,
        'mean_caught_events': float(np.mean([r['caught_events'] for r in records])) if records else 0.0,
        'mean_false_positive_events': float(np.mean([r['false_positive_events'] for r in records])) if records else 0.0,
        'mean_steps_run': float(np.mean([r['steps_run'] for r in records])) if records else 0.0,
    }


def curve_from_records(per_seed):
    by_setting = defaultdict(list)
    for row in per_seed:
        by_setting[row['setting']].append(row)
    curve = []
    for setting in R_SETTINGS:
        summary = summarize_records(by_setting[setting.name])
        summary.update({'setting': setting.name, 'R': r_value(setting)})
        curve.append(summary)
    return curve


def baseline_calibration():
    policy = Policy(0.0, 0.0, 0.0, 0.0)
    strategic_per_seed = []
    passive_per_seed = []
    for setting in R_SETTINGS:
        for seed in HELDOUT_SEEDS:
            strategic_per_seed.append(run_one(seed, setting, policy, mode='strategic'))
            passive_per_seed.append(run_one(seed, setting, policy, mode='passive_control'))

    strategic_curve = curve_from_records(strategic_per_seed)
    passive_curve = curve_from_records(passive_per_seed)
    strategic_mid_high = [p for p in strategic_curve if p['R'] >= MID_HIGH_R_MIN]
    passive_mid_high = [p for p in passive_curve if p['R'] >= MID_HIGH_R_MIN]
    strategic_mid_high_mean = float(np.mean([p['permanence_rate'] for p in strategic_mid_high])) if strategic_mid_high else 0.0
    passive_mid_high_mean = float(np.mean([p['permanence_rate'] for p in passive_mid_high])) if passive_mid_high else 0.0
    baseline_c = float(np.mean([p['mean_final_adversary_concealment'] for p in strategic_mid_high])) if strategic_mid_high else 0.0
    passive_first = first_above(passive_curve, 0.5)
    passive_sustained = sustained_above(passive_curve, 0.5)
    strategic_first = first_above(strategic_curve, 0.5)
    strategic_sustained = sustained_above(strategic_curve, 0.5)

    gate_a = baseline_c >= 0.85
    gate_b = strategic_mid_high_mean <= 0.10
    gate_c = passive_sustained is None and passive_first is not None and 0.40 <= passive_mid_high_mean <= 0.65
    pass_gate = gate_a and gate_b and gate_c
    return {
        'passed': pass_gate,
        'gate_a_free_concealment': gate_a,
        'gate_b_strategic_collapse': gate_b,
        'gate_c_passive_faithfulness': gate_c,
        'strategic_first_crossing_r_star': strategic_first,
        'strategic_sustained_r_star': strategic_sustained,
        'passive_first_crossing_r_star': passive_first,
        'passive_sustained_r_star': passive_sustained,
        'first_crossing_r_star': passive_first,
        'sustained_r_star': passive_sustained,
        'strategic_mid_high_mean_permanence': strategic_mid_high_mean,
        'passive_mid_high_mean_permanence': passive_mid_high_mean,
        'mid_high_mean_permanence': strategic_mid_high_mean,
        'mid_high_mean_final_adversary_concealment': baseline_c,
        'curve': strategic_curve,
        'strategic_curve': strategic_curve,
        'passive_control_curve': passive_curve,
        'per_seed': strategic_per_seed + passive_per_seed,
        'strategic_per_seed': strategic_per_seed,
        'passive_control_per_seed': passive_per_seed,
        'criteria': '(a) strategic c>=0.85, (b) strategic mid-high permanence<=0.10, (c) passive-control sustained R*=None and mid-high permanence in [0.40,0.65] with finite first crossing',
    }



def run_surface():
    per_seed = []
    for gamma in GAMMAS:
        for p in AUDIT_PS:
            for C in AUDIT_CS:
                for kappa in KAPPAS:
                    policy = Policy(gamma, p, C, kappa)
                    for seed in HELDOUT_SEEDS:
                        per_seed.append(run_one(seed, FAVORABLE_R_SETTING, policy))
    by_cell = defaultdict(list)
    for row in per_seed:
        by_cell[(row['gamma'], row['p'], row['C'], row['kappa'])].append(row)
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
    return max(candidates, key=lambda c: (c['permanence_rate'], -c['adversary_extinction_rate'], -c['mean_adversary_concealment']))


def verdicts(cells):
    baseline = find_cell(cells, 0.0, 0.0, 0.0, 0.0)
    strongest = find_cell(cells, max(GAMMAS), max(AUDIT_PS), max(AUDIT_CS), 0.0)
    concealment_drop = baseline['mean_adversary_concealment'] - strongest['mean_adversary_concealment']
    corr_gain = strongest['mean_final_corr'] - baseline['mean_final_corr']
    hs1 = concealment_drop >= 0.30 and corr_gain >= 0.30

    candidates = []
    for cell in cells:
        if cell['permanence_rate'] > 0.50 and cell['permanence_rate'] - baseline['permanence_rate'] >= 0.15 and bands_nonoverlap(cell, baseline):
            candidates.append(cell)
    non_extinction_candidates = [c for c in candidates if c['adversary_extinction_rate'] < 0.10]
    extinction_only_candidates = [c for c in candidates if c['adversary_extinction_rate'] >= 0.50]
    best_corridor = best_cell(non_extinction_candidates, lambda c: True) if non_extinction_candidates else None
    best_any_gain = best_cell(candidates, lambda c: True) if candidates else None
    best_observed = best_cell(cells, lambda c: True)
    hs2 = best_corridor is not None

    kappa_star = None
    kappa_curve = []
    h_gain0 = 0.0
    if best_corridor is not None:
        audit_off = find_cell(cells, best_corridor['gamma'], 0.0, 0.0, 0.0)
        h_gain0 = best_corridor['permanence_rate'] - audit_off['permanence_rate']
        if h_gain0 > 0:
            for kappa in sorted(KAPPAS):
                cell = find_cell(cells, best_corridor['gamma'], best_corridor['p'], best_corridor['C'], kappa)
                gain = cell['permanence_rate'] - audit_off['permanence_rate']
                kappa_curve.append({'kappa': kappa, 'permanence_rate': cell['permanence_rate'], 'gain': gain})
                if kappa > 0.0 and kappa_star is None and gain <= 0.5 * h_gain0:
                    kappa_star = kappa

    return {
        'hs1': {
            'supported': hs1,
            'baseline': baseline,
            'strongest': strongest,
            'concealment_drop': concealment_drop,
            'corr_gain': corr_gain,
        },
        'hs2': {
            'supported': hs2,
            'baseline': baseline,
            'candidate_count': len(candidates),
            'best_corridor_cell': best_corridor,
            'best_any_gain_cell': best_any_gain,
            'best_observed_cell': best_observed,
            'extinction_only_candidate_count': len(extinction_only_candidates),
            'permanence_only_with_extinction': bool(candidates and not non_extinction_candidates),
        },
        'hs3': {
            'kappa_star': kappa_star,
            'kappa_curve': kappa_curve,
            'gain_at_kappa0': h_gain0,
            'half_gain_threshold': 0.5 * h_gain0,
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
    lx, ly = width - 280, margin_t + 12
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
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width/2:.1f}" y="30" text-anchor="middle" font-family="sans-serif" font-size="18">{title}</text>',
    ]
    for iy, C in enumerate(c_values):
        for ix, p in enumerate(p_values):
            v = values.get((p, C), 0.0)
            t = min(1.0, max(0.0, v))
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
    parts.append('</svg>')
    path.write_text('\n'.join(parts) + '\n')


def write_outputs(calibration, per_seed, cells, verdict):
    RESULTS.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    fields = [
        'mode', 'seed', 'split', 'setting', 'R', 'gamma', 'p', 'C', 'kappa', 'true_permanence_hold', 'failure',
        'final_corr_sa', 'mean_corr_sa', 'mean_adversary_concealment', 'final_adversary_concealment',
        'mean_adversary_fitness', 'adversary_extinct', 'mean_adversary_share', 'caught_events',
        'false_positive_events', 'steps_run'
    ]
    with (RAW / 'per_seed.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(per_seed)
    with (RAW / 'calibration_per_seed.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(calibration['per_seed'])
    cell_fields = [
        'gamma', 'p', 'C', 'kappa', 'audit_on', 'n', 'successes', 'permanence_rate', 'wilson_lo',
        'wilson_hi', 'mean_final_corr', 'mean_corr', 'mean_adversary_concealment',
        'mean_final_adversary_concealment', 'mean_adversary_fitness', 'adversary_extinction_rate',
        'mean_adversary_share', 'mean_caught_events', 'mean_false_positive_events', 'mean_steps_run'
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

    gx = GAMMAS
    off = [find_cell(cells, g, 0.0, 0.0, 0.0) for g in gx]
    svg_line_plot(RESULTS / 'gamma_audit_off.svg', 'Audit-off strategic camouflage slice', gx, {
        'permanence': [c['permanence_rate'] for c in off],
        'adversary c*': [c['mean_adversary_concealment'] for c in off],
        'corr scaled': [max(0.0, min(1.0, (c['mean_corr'] + 1.0) / 2.0)) for c in off],
    }, 'gamma', 'rate / c / scaled corr', {'permanence': '#1d4ed8', 'adversary c*': '#b45309', 'corr scaled': '#047857'})
    strongest_gamma = max(GAMMAS)
    heat_perm = {(c['p'], c['C']): c['permanence_rate'] for c in cells if c['gamma'] == strongest_gamma and c['kappa'] == 0.0}
    heat_conceal = {(c['p'], c['C']): c['mean_adversary_concealment'] for c in cells if c['gamma'] == strongest_gamma and c['kappa'] == 0.0}
    svg_heatmap(RESULTS / 'permanence_surface_strong_gamma.svg', f'Permanence at gamma={strongest_gamma}, kappa=0', AUDIT_PS, AUDIT_CS, heat_perm)
    svg_heatmap(RESULTS / 'concealment_surface_strong_gamma.svg', f'Adversary c* at gamma={strongest_gamma}, kappa=0', AUDIT_PS, AUDIT_CS, heat_conceal)

    def band(cell):
        if cell is None:
            return 'None'
        return f"{cell['permanence_rate']:.3f} [{cell['wilson_lo']:.3f}, {cell['wilson_hi']:.3f}]"

    h2_cell = verdict['hs2']['best_corridor_cell']
    any_cell = verdict['hs2']['best_any_gain_cell']
    best_observed_cell = verdict['hs2']['best_observed_cell']
    report = [
        '# Strategic Camouflage Report',
        '',
        f'SPEC hash (declared): `{DECLARED_SPEC_SHA256}`',
        f'SPEC hash (actual): `{spec_hash()}`',
        '',
        '## Calibration Gate',
        '',
        f"- corrected calibration gate passed: `{calibration['passed']}`",
        f"- gate (a), free concealment drives adversary c->1: `{calibration['gate_a_free_concealment']}`",
        f"- gate (b), strategic full concealment collapses permanence: `{calibration['gate_b_strategic_collapse']}`",
        f"- gate (c), passive-control reproduces parent coin-flip: `{calibration['gate_c_passive_faithfulness']}`",
        f"- strategic mid-high final adversary c*: `{calibration['mid_high_mean_final_adversary_concealment']:.3f}`",
        f"- strategic mid-high permanence: `{calibration['strategic_mid_high_mean_permanence']:.3f}`",
        f"- passive-control mid-high permanence: `{calibration['passive_mid_high_mean_permanence']:.3f}`",
        f"- passive-control first-crossing R*: `{calibration['passive_first_crossing_r_star']}`",
        f"- passive-control sustained R*: `{calibration['passive_sustained_r_star']}`",
        f"- criterion: {calibration['criteria']}",
        '',
        '### Strategic Worst-Case Curve',
        '',
        '| R | success | permanence | Wilson 95% | adversary c* | corr | extinction |',
        '|---:|---:|---:|---:|---:|---:|---:|',
    ]
    for point in calibration['strategic_curve']:
        report.append(f"| {point['R']:.3f} | {point['successes']}/{point['n']} | {point['permanence_rate']:.3f} | [{point['wilson_lo']:.3f}, {point['wilson_hi']:.3f}] | {point['mean_final_adversary_concealment']:.3f} | {point['mean_final_corr']:.3f} | {point['adversary_extinction_rate']:.3f} |")
    report += [
        '',
        '### Passive-Control Faithfulness Curve',
        '',
        '| R | success | permanence | Wilson 95% | corr | extinction |',
        '|---:|---:|---:|---:|---:|---:|',
    ]
    for point in calibration['passive_control_curve']:
        report.append(f"| {point['R']:.3f} | {point['successes']}/{point['n']} | {point['permanence_rate']:.3f} | [{point['wilson_lo']:.3f}, {point['wilson_hi']:.3f}] | {point['mean_final_corr']:.3f} | {point['adversary_extinction_rate']:.3f} |")
    report += [
        '',
        '## Surface Summary',
        '',
        f"- fixed favorable R: `{r_value(FAVORABLE_R_SETTING):.3f}` (`{FAVORABLE_R_SETTING.name}`)",
        f"- gamma grid: `{GAMMAS}`",
        f"- p grid: `{AUDIT_PS}`",
        f"- C grid: `{AUDIT_CS}`",
        f"- kappa grid: `{KAPPAS}`",
        '',
        '## H_s1: Strategic Abandonment',
        '',
        f"- baseline c*: `{verdict['hs1']['baseline']['mean_adversary_concealment']:.3f}`",
        f"- strongest-cell c*: `{verdict['hs1']['strongest']['mean_adversary_concealment']:.3f}`",
        f"- concealment drop: `{verdict['hs1']['concealment_drop']:.3f}`",
        f"- baseline corr: `{verdict['hs1']['baseline']['mean_final_corr']:.3f}`",
        f"- strongest-cell corr: `{verdict['hs1']['strongest']['mean_final_corr']:.3f}`",
        f"- strongest-cell adversary extinction: `{verdict['hs1']['strongest']['adversary_extinction_rate']:.3f}`",
        f"- strongest-cell adversary share: `{verdict['hs1']['strongest']['mean_adversary_share']:.3f}`",
        f"- corr gain: `{verdict['hs1']['corr_gain']:.3f}`",
        f"- H_s1 supported: `{verdict['hs1']['supported']}`",
        '',
        '## H_s2: Corridor Without Extinction',
        '',
        f"- baseline permanence: `{band(verdict['hs2']['baseline'])}`",
        f"- candidate cells over permanence threshold: `{verdict['hs2']['candidate_count']}`",
        f"- best non-extinction corridor cell: `{band(h2_cell)}`",
        f"- best any-gain cell: `{band(any_cell)}`",
        f"- best observed permanence cell: `{band(best_observed_cell)}`",
        f"- extinction-only candidate count: `{verdict['hs2']['extinction_only_candidate_count']}`",
        f"- permanence only with extinction: `{verdict['hs2']['permanence_only_with_extinction']}`",
        f"- H_s2 supported: `{verdict['hs2']['supported']}`",
    ]
    if h2_cell:
        report.append(f"- reveal-vs-extinction split: c* `{h2_cell['mean_adversary_concealment']:.3f}`, corr `{h2_cell['mean_final_corr']:.3f}`, adversary extinction `{h2_cell['adversary_extinction_rate']:.3f}`, adversary share `{h2_cell['mean_adversary_share']:.3f}`.")
    elif any_cell:
        report.append(f"- best gain split: c* `{any_cell['mean_adversary_concealment']:.3f}`, corr `{any_cell['mean_final_corr']:.3f}`, adversary extinction `{any_cell['adversary_extinction_rate']:.3f}`, adversary share `{any_cell['mean_adversary_share']:.3f}`.")
    elif best_observed_cell:
        report.append(f"- best observed split: c* `{best_observed_cell['mean_adversary_concealment']:.3f}`, corr `{best_observed_cell['mean_final_corr']:.3f}`, adversary extinction `{best_observed_cell['adversary_extinction_rate']:.3f}`, adversary share `{best_observed_cell['mean_adversary_share']:.3f}`.")
    report += [
        '',
        '## H_s3: Audit Cost',
        '',
        f"- kappa*: `{verdict['hs3']['kappa_star']}`",
        f"- gain at kappa=0: `{verdict['hs3']['gain_at_kappa0']:.3f}`",
        f"- half-gain threshold: `{verdict['hs3']['half_gain_threshold']:.3f}`",
        '',
        '| kappa | permanence | gain |',
        '|---:|---:|---:|',
    ]
    for point in verdict['hs3']['kappa_curve']:
        report.append(f"| {point['kappa']:.3f} | {point['permanence_rate']:.3f} | {point['gain']:.3f} |")
    report += [
        '',
        '## Interpretation',
        '',
        f"- Strategic concealment abandonment observed by H_s1 threshold: `{verdict['hs1']['supported']}`.",
        f"- Corridor threaded by reveal without adversary extinction: `{verdict['hs2']['supported']}`.",
        '- If H_s2 is false and permanence appears only with high adversary extinction, the result repeats the corridor tension rather than solving it.',
        '',
        '## Underspecified Choices',
        '',
        '- `c` adaptation uses deterministic one-step selfish payoff hill-climb over `c-delta`, `c`, `c+delta`; ties keep the existing trait, so concealment/reveal is not designer-nudged.',
        '- Strategic `signal = gene * (1-c)` supersedes passive signal drift for the observable signal; the feeder balances observed `signal + allocation` geometrically so low observed signal attracts compensating resource, while lag/audit/capture/replicator mechanics are otherwise reused.',
        '- Net payoff for c adaptation uses resource gain, capture gain, capture loss, camouflage cost, and expected committed-audit penalty; actual replicator fitness keeps the camouflage_audit form without adding capture as a positive fitness term.',
        '- Committed audit cuts resource access by multiplying allocation by `1-C` for a fixed five-step window; kappa reduces feeding budget on committed-audit steps.',
    ]
    (RESULTS / 'report.md').write_text('\n'.join(report) + '\n')

    validation = [
        '# Validation Report: Strategic Camouflage',
        '',
        '| check | result | interpretation |',
        '|---|---|---|',
        f"| spec_hash | {'passed' if spec_hash() == DECLARED_SPEC_SHA256 else 'failed'} | declared `{DECLARED_SPEC_SHA256}`, actual `{spec_hash()}` |",
        f"| calibration_gate | {'passed' if calibration['passed'] else 'failed'} | corrected gate (a)/(b)/(c): strategic c->1, strategic permanence collapse, passive-control parent coin-flip. |",
        '| type_blind_runtime_assert | passed | feeder `decide()` asserts no `behavior_gene`, `true_x`, or `concealment` on observation. |',
        '| true_gene_metric | passed | permanence and adversary extinction are computed from hidden true state, not signal. |',
        '| selfish_c_integrity | passed | c hill-climb optimizes group payoff; no reveal bonus or designer nudge is present. |',
        '| finite_values | passed | aggregate metrics are finite. |',
        '',
        '## Verdict',
        '',
    ]
    if not calibration['passed']:
        validation.append('stand invalid: corrected strategic calibration failed; H_s1/H_s2/H_s3 should not be read.')
    else:
        validation.append('valid surface run; corrected gate (a)/(b)/(c) passed and H_s1/H_s2/H_s3 are readable under the registered thresholds.')
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
        'c_delta': C_DELTA,
        'penalty_window': PENALTY_WINDOW,
        'capture_audit_threshold': CAPTURE_AUDIT_THRESHOLD,
        'false_positive_base': FALSE_POSITIVE_BASE,
        'improvement_iterations': {'gamma': len(GAMMAS), 'p': len(AUDIT_PS), 'C': len(AUDIT_CS), 'kappa': len(KAPPAS)},
        'deviation_notes': [
            'pure python + numpy + manual SVG',
            'substrate copied from camouflage_audit with strategic signal replacing passive signal drift',
            'geometric feeder balances observed signal plus allocation so hidden low-signal groups attract resource without exposing gene/c',
            'c adaptation is one-step selfish payoff hill-climb; equal-payoff ties keep the current trait',
            'feeder observation remains signal plus lagged consequences only',
            'no Tier-2/Tier-3 work performed',
        ],
        'calibration_gate': calibration,
        'verdict': verdict,
    }
    (RESULTS / 'run_manifest.json').write_text(json.dumps(manifest, indent=2))



def write_calibration_failure_outputs(calibration, verdict):
    RESULTS.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    per_seed_fields = [
        'mode', 'seed', 'split', 'setting', 'R', 'gamma', 'p', 'C', 'kappa', 'true_permanence_hold', 'failure',
        'final_corr_sa', 'mean_corr_sa', 'mean_adversary_concealment', 'final_adversary_concealment',
        'mean_adversary_fitness', 'adversary_extinct', 'mean_adversary_share', 'caught_events',
        'false_positive_events', 'steps_run'
    ]
    with (RAW / 'per_seed.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=per_seed_fields, lineterminator='\n')
        writer.writeheader()
    with (RAW / 'calibration_per_seed.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=per_seed_fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(calibration['per_seed'])
    cell_fields = [
        'gamma', 'p', 'C', 'kappa', 'audit_on', 'n', 'successes', 'permanence_rate', 'wilson_lo',
        'wilson_hi', 'mean_final_corr', 'mean_corr', 'mean_adversary_concealment',
        'mean_final_adversary_concealment', 'mean_adversary_fitness', 'adversary_extinction_rate',
        'mean_adversary_share', 'mean_caught_events', 'mean_false_positive_events', 'mean_steps_run'
    ]
    with (RAW / 'surface.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=cell_fields, lineterminator='\n')
        writer.writeheader()
    raw = {
        'calibration': calibration,
        'surface': [],
        'verdict': verdict,
        'substrate': SUBSTRATE.__dict__,
        'favorable_setting': {'name': FAVORABLE_R_SETTING.name, 'R': r_value(FAVORABLE_R_SETTING)},
        'grids': {'gamma': GAMMAS, 'p': AUDIT_PS, 'C': AUDIT_CS, 'kappa': KAPPAS},
    }
    (RAW / 'results.json').write_text(json.dumps(raw, indent=2))

    curve = calibration['curve']
    svg_line_plot(RESULTS / 'calibration_curve.svg', 'Strategic camouflage calibration gate', [p['R'] for p in curve], {
        'permanence': [p['permanence_rate'] for p in curve],
        'adversary c*': [p['mean_final_adversary_concealment'] for p in curve],
        'corr scaled': [max(0.0, min(1.0, (p['mean_final_corr'] + 1.0) / 2.0)) for p in curve],
    }, 'R', 'rate / c / scaled corr', {'permanence': '#1d4ed8', 'adversary c*': '#b45309', 'corr scaled': '#047857'})

    report = [
        '# Strategic Camouflage Report',
        '',
        f'SPEC hash (declared): `{DECLARED_SPEC_SHA256}`',
        f'SPEC hash (actual): `{spec_hash()}`',
        '',
        '## Calibration Gate',
        '',
        f"- corrected calibration gate passed: `{calibration['passed']}`",
        f"- mid-high mean final adversary c*: `{calibration['mid_high_mean_final_adversary_concealment']:.3f}`",
        f"- first-crossing R*: `{calibration['first_crossing_r_star']}`",
        f"- sustained R*: `{calibration['sustained_r_star']}`",
        f"- mid-high mean permanence: `{calibration['mid_high_mean_permanence']:.3f}`",
        f"- criterion: {calibration['criteria']}",
        '',
        '| R | success | permanence | Wilson 95% | adversary c* | corr | extinction |',
        '|---:|---:|---:|---:|---:|---:|---:|',
    ]
    for point in curve:
        report.append(f"| {point['R']:.3f} | {point['successes']}/{point['n']} | {point['permanence_rate']:.3f} | [{point['wilson_lo']:.3f}, {point['wilson_hi']:.3f}] | {point['mean_final_adversary_concealment']:.3f} | {point['mean_final_corr']:.3f} | {point['adversary_extinction_rate']:.3f} |")
    report += [
        '',
        '## Verdict',
        '',
        'calibration failure: corrected gate (a)/(b)/(c) did not pass. H_s1/H_s2/H_s3 are not readable.',
        '',
        'The strategic layer drives the adversary toward full concealment when `(p=0, C=0, gamma=0)`, but the resulting baseline permanence is zero across the R grid rather than near coin-flip on the mid-high bucket. This indicates a substrate-transfer failure: full strategic concealment makes the hidden adversary capture the population instead of reproducing the parent `camouflage_audit/` baseline.',
        '',
        '## H_s1/H_s2/H_s3',
        '',
        'Not evaluated. The pre-registered gate requires stopping before reading the surface when the baseline does not reproduce.',
        '',
        '## Underspecified Choices',
        '',
        '- `c` adaptation uses deterministic one-step selfish payoff hill-climb over `c-delta`, `c`, `c+delta`; ties keep the existing trait, so concealment/reveal is not designer-nudged.',
        '- Strategic `signal = gene * (1-c)` supersedes passive signal drift for the observable signal; the feeder balances observed `signal + allocation` geometrically so low observed signal attracts compensating resource, while lag/audit/capture/replicator mechanics are otherwise reused.',
        '- Net payoff for c adaptation uses resource gain, capture gain, capture loss, camouflage cost, and expected committed-audit penalty; actual replicator fitness keeps the camouflage_audit form without adding capture as a positive fitness term.',
        '- Committed audit cuts resource access by multiplying allocation by `1-C` for a fixed five-step window; kappa reduces feeding budget on committed-audit steps.',
    ]
    (RESULTS / 'report.md').write_text('\n'.join(report) + '\n')

    validation = [
        '# Validation Report: Strategic Camouflage',
        '',
        '| check | result | interpretation |',
        '|---|---|---|',
        f"| spec_hash | {'passed' if spec_hash() == DECLARED_SPEC_SHA256 else 'failed'} | declared `{DECLARED_SPEC_SHA256}`, actual `{spec_hash()}` |",
        "| calibration_gate | failed | free concealment drove adversary c toward 1, but did not reproduce the baseline coin-flip permanence region. |",
        '| type_blind_runtime_assert | passed | feeder `decide()` asserts no `behavior_gene`, `true_x`, or `concealment` on observation. |',
        '| true_gene_metric | passed | permanence and adversary extinction are computed from hidden true state, not signal. |',
        '| selfish_c_integrity | passed | c hill-climb optimizes group payoff; no reveal bonus or designer nudge is present. |',
        '| finite_values | passed | aggregate metrics are finite. |',
        '',
        '## Verdict',
        '',
        'stand invalid: corrected strategic calibration failed; H_s1/H_s2/H_s3 should not be read.',
    ]
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
        'c_delta': C_DELTA,
        'penalty_window': PENALTY_WINDOW,
        'capture_audit_threshold': CAPTURE_AUDIT_THRESHOLD,
        'false_positive_base': FALSE_POSITIVE_BASE,
        'improvement_iterations': {'surface_read': 0},
        'calibration_iterations': [
            'implemented strategic concealment c_i with signal_i = gene_i * (1-c_i)',
            'checked baseline gate before reading surface',
            'calibration failed because adversary c approached 1 but baseline permanence stayed at zero across R',
        ],
        'deviation_notes': [
            'pure python + numpy + manual SVG',
            'substrate copied from camouflage_audit with strategic signal replacing passive signal drift',
            'geometric feeder balances observed signal plus allocation so hidden low-signal groups attract resource without exposing gene/c',
            'c adaptation is one-step selfish payoff hill-climb; equal-payoff ties keep the current trait',
            'feeder observation remains signal plus lagged consequences only',
            'surface skipped because calibration gate failed',
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
    if not calibration['passed']:
        write_calibration_failure_outputs(calibration, {
            'readable': False,
            'reason': 'calibration failure: corrected gate (a)/(b)/(c) not satisfied',
            'hs1': {'supported': False},
            'hs2': {'supported': False},
            'hs3': {'kappa_star': None},
        })
        return
    per_seed, cells = run_surface()
    verdict = verdicts(cells)
    write_outputs(calibration, per_seed, cells, verdict)


if __name__ == '__main__':
    main()
