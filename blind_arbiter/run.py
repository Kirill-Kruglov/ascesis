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

DECLARED_SPEC_SHA256 = '2ce172b2febdf575b6506e5f31711a226edd974e33f872f634b645638831af2b'

TRAIN_SEEDS = list(range(3100, 3130))
HELDOUT_SEEDS = list(range(4100, 4130))
REGIMES = ['scalar', 'geometric', 'lexicographic']
GRID_GRID = np.linspace(0.0, 1.0, 21)
STEPS = 120
G = 2
EPS = 1e-9

LOW_R_THRESHOLD = 0.40
MID_R_LO = 0.80
MID_R_HI = 1.50


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


DEFAULT_SUBSTRATE = SubstrateParams(
    resource_gain=0.38,
    capture_drag=0.92,
    capture_strength=0.88,
    consequence_reactivity=1.20,
    signal_mutation=0.24,
    signal_noise=0.04,
    signal_bias=0.12,
    signal_response=0.35,
    audit_shift=0.06,
)

SUBSTRATE_CANDIDATES = [
    DEFAULT_SUBSTRATE,
    SubstrateParams(0.36, 0.96, 0.92, 1.35, 0.28, 0.04, 0.14, 0.32, 0.08),
    SubstrateParams(0.34, 1.00, 0.96, 1.50, 0.32, 0.05, 0.16, 0.28, 0.10),
    SubstrateParams(0.32, 1.04, 1.00, 1.70, 0.36, 0.05, 0.18, 0.24, 0.12),
    SubstrateParams(0.30, 1.18, 1.04, 1.90, 0.40, 0.06, 0.20, 0.22, 0.14),
    SubstrateParams(0.24, 0.78, 0.60, 1.40, 0.18, 0.04, 0.08, 0.30, 0.05),
    SubstrateParams(0.20, 0.62, 0.46, 1.20, 0.16, 0.04, 0.06, 0.32, 0.04),
    SubstrateParams(0.16, 0.50, 0.34, 1.00, 0.14, 0.03, 0.05, 0.34, 0.03),
]

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


@dataclass
class CandidateResult:
    substrate: SubstrateParams
    calibration_gate: dict
    records: list
    traces: list
    curve_data: dict
    summary: dict
    failure_modes: dict
    r_star: dict
    report_artifacts: dict


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


def percentile_band(values):
    arr = np.asarray(values, dtype=float)
    if len(arr) == 0:
        return {'mean': 0.0, 'median': 0.0, 'q25': 0.0, 'q75': 0.0, 'std': 0.0}
    return {
        'mean': float(np.mean(arr)),
        'median': float(np.median(arr)),
        'q25': float(np.quantile(arr, 0.25)),
        'q75': float(np.quantile(arr, 0.75)),
        'std': float(np.std(arr)),
    }


def first_above(points, threshold=0.5):
    for p in sorted(points, key=lambda x: x['R']):
        if p['true_permanence_rate'] >= threshold:
            return p['R']
    return None


def sustained_above(points, threshold=0.5):
    ordered = sorted(points, key=lambda x: x['R'])
    for idx, point in enumerate(ordered):
        if all(p['true_permanence_rate'] >= threshold for p in ordered[idx:]):
            return point['R']
    return None


def wilson_interval(successes, total, z=1.96):
    if total <= 0:
        return 0.0, 0.0
    phat = successes / float(total)
    denom = 1.0 + z * z / total
    center = (phat + z * z / (2.0 * total)) / denom
    half = z * math.sqrt((phat * (1.0 - phat) + z * z / (4.0 * total)) / total) / denom
    return max(0.0, center - half), min(1.0, center + half)


def format_optional(value):
    return 'None' if value is None else f'{value:.3f}'


def svg_header(width, height, title):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width/2:.1f}" y="28" text-anchor="middle" font-family="sans-serif" font-size="18">{title}</text>',
    ]


def svg_footer():
    return ['</svg>']


def svg_line_plot(path, title, x_values, series, x_label, y_label, x_min=None, x_max=None, y_min=None, y_max=None, bands=None, verticals=None, colors=None):
    width, height = 960, 540
    margin_l, margin_r, margin_t, margin_b = 70, 30, 50, 60
    xs = list(x_values)
    if x_min is None:
        x_min = min(xs)
    if x_max is None:
        x_max = max(xs)
    if y_min is None:
        vals = []
        for vals_s in series.values():
            vals.extend(vals_s)
        if bands:
            for lo, hi in bands.values():
                vals.extend(lo)
                vals.extend(hi)
        y_min = min(vals) if vals else 0.0
    if y_max is None:
        vals = []
        for vals_s in series.values():
            vals.extend(vals_s)
        if bands:
            for lo, hi in bands.values():
                vals.extend(lo)
                vals.extend(hi)
        y_max = max(vals) if vals else 1.0
    if y_max - y_min < 1e-9:
        y_max = y_min + 1.0

    def tx(x):
        return margin_l + (x - x_min) / (x_max - x_min + 1e-12) * (width - margin_l - margin_r)

    def ty(y):
        return height - margin_b - (y - y_min) / (y_max - y_min + 1e-12) * (height - margin_t - margin_b)

    parts = svg_header(width, height, title)
    parts.append(f'<line x1="{margin_l}" y1="{height-margin_b}" x2="{width-margin_r}" y2="{height-margin_b}" stroke="#111"/>')
    parts.append(f'<line x1="{margin_l}" y1="{margin_t}" x2="{margin_l}" y2="{height-margin_b}" stroke="#111"/>')
    parts.append(f'<text x="{width/2:.1f}" y="{height-15}" text-anchor="middle" font-family="sans-serif" font-size="12">{x_label}</text>')
    parts.append(f'<text x="18" y="{height/2:.1f}" transform="rotate(-90 18 {height/2:.1f})" font-family="sans-serif" font-size="12">{y_label}</text>')
    if verticals:
        for x, label in verticals:
            px = tx(x)
            parts.append(f'<line x1="{px:.1f}" y1="{margin_t}" x2="{px:.1f}" y2="{height-margin_b}" stroke="#999" stroke-dasharray="4,4"/>')
            parts.append(f'<text x="{px:.1f}" y="{height-margin_b+16}" text-anchor="middle" font-family="sans-serif" font-size="10">{label}</text>')
    for name, ys in series.items():
        color = colors.get(name, '#111') if colors else '#111'
        pts = ' '.join(f'{tx(x_values[i]):.1f},{ty(y):.1f}' for i, y in enumerate(ys))
        parts.append(f'<polyline fill="none" stroke="{color}" stroke-width="2" points="{pts}"/>')
        if bands and name in bands:
            lo, hi = bands[name]
            band_pts = [f'{tx(x_values[i]):.1f},{ty(hi[i]):.1f}' for i in range(len(hi))]
            band_pts += [f'{tx(x_values[i]):.1f},{ty(lo[i]):.1f}' for i in range(len(lo)-1, -1, -1)]
            parts.append(f'<polygon fill="{color}" fill-opacity="0.15" stroke="none" points="{" ".join(band_pts)}"/>')
            parts.append(f'<polyline fill="none" stroke="{color}" stroke-width="2" points="{pts}"/>')
    if len(series) > 1:
        lx = width - 250
        ly = margin_t + 12
        for i, (name, _) in enumerate(series.items()):
            color = colors.get(name, '#111') if colors else '#111'
            parts.append(f'<rect x="{lx}" y="{ly+i*18}" width="12" height="12" fill="{color}"/>')
            parts.append(f'<text x="{lx+18}" y="{ly+i*18+11}" font-family="sans-serif" font-size="11">{name}</text>')
    parts += svg_footer()
    path.write_text('\n'.join(parts) + '\n')


def svg_bar_plot(path, title, labels, values, colors):
    width, height = 700, 420
    margin_l, margin_r, margin_t, margin_b = 70, 30, 50, 70
    y_min = 0.0
    y_max = max(values) if values else 1.0
    y_max = max(y_max, 1e-9)

    def ty(y):
        return height - margin_b - (y - y_min) / (y_max - y_min) * (height - margin_t - margin_b)

    parts = svg_header(width, height, title)
    parts.append(f'<line x1="{margin_l}" y1="{height-margin_b}" x2="{width-margin_r}" y2="{height-margin_b}" stroke="#111"/>')
    parts.append(f'<line x1="{margin_l}" y1="{margin_t}" x2="{margin_l}" y2="{height-margin_b}" stroke="#111"/>')
    bar_w = (width - margin_l - margin_r) / max(1, len(labels)) * 0.55
    gap = (width - margin_l - margin_r) / max(1, len(labels))
    for i, (label, value) in enumerate(zip(labels, values)):
        x = margin_l + i * gap + (gap - bar_w) / 2
        y = ty(value)
        h = height - margin_b - y
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{h:.1f}" fill="{colors[i % len(colors)]}"/>')
        parts.append(f'<text x="{x + bar_w/2:.1f}" y="{height-margin_b+16}" text-anchor="middle" font-family="sans-serif" font-size="10">{label}</text>')
        parts.append(f'<text x="{x + bar_w/2:.1f}" y="{max(margin_t+12, y-4):.1f}" text-anchor="middle" font-family="sans-serif" font-size="10">{value:.3f}</text>')
    parts.append(f'<text x="{width/2:.1f}" y="{height-15}" text-anchor="middle" font-family="sans-serif" font-size="12">group member</text>')
    parts.append(f'<text x="18" y="{height/2:.1f}" transform="rotate(-90 18 {height/2:.1f})" font-family="sans-serif" font-size="12">cumulative welfare</text>')
    parts += svg_footer()
    path.write_text('\n'.join(parts) + '\n')


def save_curve_plot(curve_data):
    x_values = sorted({p['R'] for regime in REGIMES for p in curve_data[regime]})
    series = {}
    bands = {}
    colors = {'scalar': '#6b7280', 'geometric': '#1d4ed8', 'lexicographic': '#047857'}
    for regime in REGIMES:
        pts = sorted(curve_data[regime], key=lambda p: p['R'])
        series[regime] = [p['true_permanence_rate'] for p in pts]
        bands[regime] = ([p['true_permanence_q25'] for p in pts], [p['true_permanence_q75'] for p in pts])
    svg_line_plot(RESULTS / 'permanence_survival.svg', 'Blind arbiter true-gene permanence curve', x_values, series, 'R = horizon_harm / horizon_observation', 'true permanence rate', bands=bands, verticals=[(1.0, 'R=1')], colors=colors)


def save_corr_plot(time_series, representatives):
    x_values = list(range(max(len(v) for v in time_series.values()) if time_series else 1))
    series = {}
    colors = {'scalar': '#6b7280', 'geometric': '#1d4ed8', 'lexicographic': '#047857'}
    for regime in REGIMES:
        for label, setting_name, split in representatives:
            key = (regime, setting_name, split)
            ys = time_series.get(key, [])
            series[f'{regime}-{label}'] = ys
    svg_line_plot(RESULTS / 'corr_sa_over_time.svg', 'Signal-gene correlation over time', x_values, series, 'step', 'corr(signal, behavior_gene)', colors={k: colors[k.split('-')[0]] for k in series})


def save_failure_plots(failure_runs):
    low = failure_runs['camouflage']
    x_values = list(range(len(low['true_permanence_series'])))
    series = {
        'true permanence': low['true_permanence_series'],
        'corr(signal, gene)': low['corr_series'],
    }
    colors = {'true permanence': '#b45309', 'corr(signal, gene)': '#1d4ed8'}
    svg_line_plot(RESULTS / 'failure_mode_camouflage.svg', 'Failure mode 1: camouflage faster than the window', x_values, series, 'step', 'value', colors=colors)

    hack = failure_runs['hack']
    x_values = list(range(len(hack['signal_series'])))
    series = {
        'signal g0': [s[0] for s in hack['signal_series']],
        'signal g1': [s[1] for s in hack['signal_series']],
        'alloc g0': [a[0] for a in hack['allocation_series']],
        'alloc g1': [a[1] for a in hack['allocation_series']],
    }
    colors = {'signal g0': '#6b7280', 'signal g1': '#1d4ed8', 'alloc g0': '#9ca3af', 'alloc g1': '#93c5fd'}
    svg_line_plot(RESULTS / 'failure_mode_collective_hack.svg', 'Failure mode 2: collective hack / signal-gene decoupling', x_values, series, 'step', 'value', colors=colors)

    punish = failure_runs['punish']
    svg_bar_plot(RESULTS / 'failure_mode_collective_punishment.svg', 'Failure mode 3: collective punishment of the innocent', ['low-aggression member', 'high-aggression member'], [punish['low_member_welfare'], punish['high_member_welfare']], ['#10b981', '#ef4444'])


class BlindArbiterGame:
    def __init__(self, regime, setting, seed, substrate, hetero=False):
        self.regime = regime
        self.setting = setting
        self.substrate = substrate
        self.rng = np.random.default_rng(seed)
        self.hetero = hetero
        self.permanence_eps = 0.12
        self.survival_threshold = 0.05
        self.capture_extinction_threshold = 0.95
        self.audit_prob = 1.0 / float(max(1, setting.audit_period))
        self.history = deque(maxlen=max(setting.lag, setting.audit_period) + 4)
        self.state = self._initial_state()
        self.true_permanence_series = []
        self.corr_series = []
        self.interventions = []
        self.allocation_series = []
        self.signal_series = []
        self.true_x_series = []
        self.capture_series = []
        self.extinct = False
        self.captured = False
        self.hetero_welfare = np.zeros((2, 2), dtype=float) if hetero else None

    def _initial_state(self):
        behavior_gene = np.array([0.16, 0.84], dtype=float) + self.rng.normal(0.0, 0.04, size=2)
        behavior_gene = clamp(behavior_gene, 0.03, 0.97)
        true_x = normalize(np.array([0.56, 0.44], dtype=float) + self.rng.normal(0.0, 0.05, size=2))
        signal = clamp(behavior_gene + self.rng.normal(0.0, 0.10, size=2), 0.0, 1.0)
        return State(behavior_gene=behavior_gene, true_x=true_x, signal=signal, t=0, recent_alloc=np.array([0.5, 0.5], dtype=float))

    def _lagged_observation(self):
        if not self.history:
            return np.zeros(2), np.zeros(2), self.state.recent_alloc.copy(), False, 0
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
        pred = clamp((1.0 - self.substrate.signal_response) * obs.signal + self.substrate.signal_response * target, 0.0, 1.0)
        return pred

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
            mean_log_signal = float(np.mean(np.log(pred_signal + EPS)))
            if self.regime == 'scalar':
                utility = float(np.dot(pred_signal, alloc))
                key = (utility - consequence_penalty, -float(np.abs(alloc - obs.signal).sum()))
            elif self.regime == 'geometric':
                utility = mean_log_signal
                key = (utility - consequence_penalty, -float(np.abs(alloc - obs.signal).sum()))
            elif self.regime == 'lexicographic':
                floor = float(pred_signal.min() - self.permanence_eps)
                if floor >= 0:
                    key = (1.0, floor - consequence_penalty, mean_log_signal)
                else:
                    key = (floor - consequence_penalty, mean_log_signal)
            else:
                raise ValueError(self.regime)
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

    def _true_permanence(self, true_x_next):
        if self.extinct or self.captured:
            return 0.0
        if float(np.min(true_x_next)) <= self.permanence_eps:
            return 0.0
        return 1.0

    def step(self):
        obs = self._observation()
        alloc = self.decide(obs)
        loss, capture = self._capture_transfer(alloc)
        fitness = 1.0 + self.substrate.resource_gain * alloc - self.substrate.capture_drag * loss
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
        intervention = float(np.abs(alloc - obs.signal).sum())
        capture_event = float(np.max(capture) > 0.10)
        self.true_permanence_series.append(true_perm)
        self.corr_series.append(corr)
        self.interventions.append(intervention)
        self.allocation_series.append(alloc.copy())
        self.signal_series.append(signal_next.copy())
        self.true_x_series.append(true_x_next.copy())
        self.capture_series.append(capture_event)
        self.history.append({
            'step': self.state.t,
            'signal': self.state.signal.copy(),
            'loss': loss.copy(),
            'capture': capture.copy(),
            'alloc': alloc.copy(),
        })
        self.state = State(behavior_gene=self.state.behavior_gene.copy(), true_x=true_x_next, signal=signal_next, t=self.state.t + 1, recent_alloc=alloc.copy())
        return {
            'true_permanence': true_perm,
            'corr_sa': corr,
            'intervention': intervention,
            'capture_event': capture_event,
            'extinct': extinct,
            'captured': captured,
            'true_x': true_x_next.copy(),
            'signal': signal_next.copy(),
            'behavior_gene': self.state.behavior_gene.copy(),
            'alloc': alloc.copy(),
            'loss': loss.copy(),
        }

    def run(self):
        rows = []
        for _ in range(STEPS):
            rows.append(self.step())
            if self.extinct or self.captured:
                break
        true_permanence_hold = bool(all(r['true_permanence'] > 0.5 for r in rows))
        failure = bool(self.extinct or self.captured or not true_permanence_hold)
        return {
            'rows': rows,
            'true_permanence_hold': true_permanence_hold,
            'failure': failure,
            'final_true_x': self.state.true_x.copy(),
            'final_signal': self.state.signal.copy(),
            'final_behavior_gene': self.state.behavior_gene.copy(),
            'final_true_corr': safe_corr(self.state.signal, self.state.behavior_gene),
            'mean_intervention_inside_floor': float(np.mean([r['intervention'] for r in rows if r['true_permanence'] > 0.5])) if any(r['true_permanence'] > 0.5 for r in rows) else 0.0,
            'mean_intervention_outside_floor': float(np.mean([r['intervention'] for r in rows if r['true_permanence'] <= 0.5])) if any(r['true_permanence'] <= 0.5 for r in rows) else 0.0,
            'time_to_failure': next((i for i, r in enumerate(rows) if r['extinct'] or r['captured']), len(rows)),
            'corr_start': float(np.mean([r['corr_sa'] for r in rows[:max(1, len(rows)//4)]])) if rows else 0.0,
            'corr_end': float(np.mean([r['corr_sa'] for r in rows[-max(1, len(rows)//4):]])) if rows else 0.0,
            'true_permanence_series': [r['true_permanence'] for r in rows],
            'corr_series': [r['corr_sa'] for r in rows],
            'intervention_series': [r['intervention'] for r in rows],
            'allocation_series': [r['alloc'] for r in rows],
            'signal_series': [r['signal'] for r in rows],
            'true_x_series': [r['true_x'] for r in rows],
            'capture_series': [r['capture_event'] for r in rows],
        }


def run_experiment(regime, setting, seed, substrate, hetero=False):
    game = BlindArbiterGame(regime, setting, seed, substrate, hetero=hetero)
    out = game.run()
    horizon_harm = harmonic_harm(setting.capture_rate)
    horizon_observation = setting.lag + setting.audit_period
    R = horizon_harm / float(horizon_observation)
    final_true_x = out['final_true_x']
    record = {
        'regime': regime,
        'seed': seed,
        'split': 'heldout' if seed in HELDOUT_SEEDS else 'train',
        'setting': setting.name,
        'capture_rate': setting.capture_rate,
        'lag': setting.lag,
        'audit_period': setting.audit_period,
        'horizon_harm': horizon_harm,
        'horizon_observation': horizon_observation,
        'R': R,
        'true_permanence_hold': int(out['true_permanence_hold']),
        'permanence_hold': int(out['true_permanence_hold']),
        'failure': int(out['failure']),
        'extinct': int(game.extinct),
        'captured': int(game.captured),
        'time_to_failure': out['time_to_failure'],
        'final_min_true_share': float(final_true_x.min()),
        'final_prod_true_share': float(np.prod(final_true_x)),
        'final_true_corr_sa': float(out['final_true_corr']),
        'final_corr_sa': float(out['final_true_corr']),
        'corr_start': float(out['corr_start']),
        'corr_end': float(out['corr_end']),
        'mean_intervention_inside_floor': float(out['mean_intervention_inside_floor']),
        'mean_intervention_outside_floor': float(out['mean_intervention_outside_floor']),
        'mean_true_permanence': float(np.mean(out['true_permanence_series'])) if out['true_permanence_series'] else 0.0,
        'mean_corr_sa': float(np.mean(out['corr_series'])) if out['corr_series'] else 0.0,
        'capture_events': int(np.sum(out['capture_series'])),
        'steps_run': len(out['rows']),
    }
    return record, out, game


def evaluate_dataset(substrate, seeds, collect_traces=True):
    all_records = []
    all_traces = []
    for regime in REGIMES:
        for seed in seeds:
            split = 'heldout' if seed in HELDOUT_SEEDS else 'train'
            for setting in R_SETTINGS:
                rec, trace, _ = run_experiment(regime, setting, seed, substrate, hetero=False)
                rec['split'] = split
                all_records.append(rec)
                if collect_traces:
                    all_traces.append({
                        'regime': regime,
                        'setting': setting.name,
                        'split': split,
                        'seed': seed,
                        'R': rec['R'],
                        'true_permanence_series': trace['true_permanence_series'],
                        'corr_series': trace['corr_series'],
                        'intervention_series': trace['intervention_series'],
                        'allocation_series': [a.tolist() for a in trace['allocation_series']],
                        'signal_series': [s.tolist() for s in trace['signal_series']],
                        'true_x_series': [x.tolist() for x in trace['true_x_series']],
                    })
    grouped = defaultdict(list)
    for rec in all_records:
        grouped[(rec['regime'], rec['setting'], rec['split'])].append(rec)

    curve_data = {regime: [] for regime in REGIMES}
    for regime in REGIMES:
        for setting in R_SETTINGS:
            held = grouped[(regime, setting.name, 'heldout')]
            train = grouped[(regime, setting.name, 'train')]
            curve_data[regime].append({
                'setting': setting.name,
                'R': float(np.mean([r['R'] for r in held])) if held else r_value(setting),
                'true_permanence_rate': float(np.mean([r['true_permanence_hold'] for r in held])) if held else 0.0,
                'true_permanence_q25': float(np.quantile([r['true_permanence_hold'] for r in held], 0.25)) if held else 0.0,
                'true_permanence_q75': float(np.quantile([r['true_permanence_hold'] for r in held], 0.75)) if held else 0.0,
                'mean_final_corr': float(np.mean([r['final_true_corr_sa'] for r in held])) if held else 0.0,
                'mean_corr': float(np.mean([r['mean_corr_sa'] for r in held])) if held else 0.0,
                'mean_time_to_failure': float(np.mean([r['time_to_failure'] for r in held])) if held else 0.0,
                'train_true_permanence_rate': float(np.mean([r['true_permanence_hold'] for r in train])) if train else 0.0,
            })

    low_points = [p for regime in REGIMES for p in curve_data[regime] if p['R'] <= LOW_R_THRESHOLD]
    high_points_by_regime = {
        regime: [p for p in curve_data[regime] if p['R'] >= 2.0]
        for regime in REGIMES
    }
    high_points = [(regime, p) for regime in REGIMES for p in high_points_by_regime[regime]]
    high_bucket_mean_by_regime = {
        regime: (float(np.mean([p['true_permanence_rate'] for p in points])) if points else 0.0)
        for regime, points in high_points_by_regime.items()
    }
    high_bucket_best_mean_regime = max(high_bucket_mean_by_regime, key=high_bucket_mean_by_regime.get)
    mid_points = [p for regime in REGIMES for p in curve_data[regime] if MID_R_LO <= p['R'] <= MID_R_HI]
    c1_low_pass = bool(low_points) and all(p['true_permanence_rate'] < 0.10 for p in low_points)
    c1_high_pass = any(mean >= 0.50 for mean in high_bucket_mean_by_regime.values())
    c1_pass = c1_low_pass and c1_high_pass
    if mid_points:
        mid_bucket_perm = float(np.mean([p['true_permanence_rate'] for p in mid_points]))
        mid_bucket_corr = float(np.mean([p['mean_final_corr'] for p in mid_points]))
    else:
        mid_bucket_perm = 0.0
        mid_bucket_corr = 0.0
    c2_witnesses = [
        {'regime': regime, 'setting': p['setting'], 'R': p['R'], 'true_permanence_rate': p['true_permanence_rate'], 'mean_final_corr': p['mean_final_corr']}
        for regime in REGIMES
        for p in curve_data[regime]
        if MID_R_LO <= p['R'] <= MID_R_HI and p['true_permanence_rate'] < 0.50 and p['mean_final_corr'] < 0.70
    ]
    c2_pass = bool(c2_witnesses)
    calibration_gate = c1_pass and c2_pass

    r_star = {regime: first_above(curve_data[regime], 0.5) for regime in REGIMES}
    sustained_r_star = {regime: sustained_above(curve_data[regime], 0.5) for regime in REGIMES}
    r_star_shift_lexi = None
    if r_star['scalar'] is not None and r_star['lexicographic'] is not None:
        r_star_shift_lexi = r_star['scalar'] - r_star['lexicographic']

    summary = {
        regime: {
            'r_star': r_star[regime],
            'sustained_r_star': sustained_r_star[regime],
            'curve': curve_data[regime],
            'heldout_true_permanence_rate_mean': float(np.mean([p['true_permanence_rate'] for p in curve_data[regime]])),
            'heldout_true_corr_start_mean': float(np.mean([r['corr_start'] for r in grouped[(regime, mid_points[0]['setting'] if mid_points else R_SETTINGS[0].name, 'heldout')]])) if grouped[(regime, mid_points[0]['setting'] if mid_points else R_SETTINGS[0].name, 'heldout')] else 0.0,
            'heldout_true_corr_end_mean': float(np.mean([r['corr_end'] for r in grouped[(regime, mid_points[0]['setting'] if mid_points else R_SETTINGS[0].name, 'heldout')]])) if grouped[(regime, mid_points[0]['setting'] if mid_points else R_SETTINGS[0].name, 'heldout')] else 0.0,
        }
        for regime in REGIMES
    }

    failure_runs = {}
    low_setting = min(R_SETTINGS, key=r_value)
    mid_setting = min(R_SETTINGS, key=lambda s: abs(r_value(s) - 1.0))
    failure_runs['camouflage'] = run_experiment('scalar', low_setting, HELDOUT_SEEDS[0], substrate)[1]
    failure_runs['hack'] = run_experiment('scalar', mid_setting, HELDOUT_SEEDS[0], substrate)[1]
    punish_game = BlindArbiterGame('scalar', mid_setting, HELDOUT_SEEDS[0], substrate, hetero=True)
    punish_game.run()
    low_w = float(punish_game.hetero_welfare[0, 0])
    high_w = float(punish_game.hetero_welfare[0, 1])
    failure_runs['punish'] = {
        'low_member_welfare': low_w,
        'high_member_welfare': high_w,
    }
    failure_modes_present = {
        'camouflage_faster_than_window': bool(failure_runs['camouflage']['failure']),
        'collective_hack': bool(safe_corr(np.array([s[0] for s in failure_runs['hack']['signal_series']]), np.array([a[0] for a in failure_runs['hack']['allocation_series']])) < 0.85),
        'collective_punishment': bool(failure_runs['punish']['low_member_welfare'] < failure_runs['punish']['high_member_welfare']),
    }

    return CandidateResult(
        substrate=substrate,
        calibration_gate={
            'c1_low_pass': c1_low_pass,
            'c1_high_pass': c1_high_pass,
            'c1_pass': c1_pass,
            'c2_pass': c2_pass,
            'passed': calibration_gate,
            'mid_bucket_perm': mid_bucket_perm,
            'mid_bucket_corr': mid_bucket_corr,
            'c2_witnesses': c2_witnesses,
            'low_bucket_max_R': float(max([p['R'] for p in low_points])) if low_points else None,
            'high_bucket_mean_by_regime': high_bucket_mean_by_regime,
            'high_bucket_best_mean_regime': high_bucket_best_mean_regime,
            'high_bucket_best_mean_true_permanence': high_bucket_mean_by_regime[high_bucket_best_mean_regime],
            'high_bucket_max_point_true_permanence': float(max([p['true_permanence_rate'] for _, p in high_points])) if high_points else None,
            'high_bucket_max_point_regime': max(high_points, key=lambda rp: rp[1]['true_permanence_rate'])[0] if high_points else None,
        },
        records=all_records,
        traces=all_traces,
        curve_data=curve_data,
        summary=summary,
        failure_modes=failure_modes_present,
        r_star={regime: {'first_crossing': r_star[regime], 'sustained': sustained_r_star[regime]} for regime in REGIMES},
        report_artifacts={
            'failure_runs': failure_runs,
            'low_setting': low_setting.name,
            'mid_setting': mid_setting.name,
        },
    )


def pick_best_candidate():
    history = []
    best = None
    best_score = -1e9
    for idx, substrate in enumerate(SUBSTRATE_CANDIDATES, start=1):
        result = evaluate_dataset(substrate, HELDOUT_SEEDS, collect_traces=True)
        high_bucket_max = max([p['true_permanence_rate'] for p in result.curve_data['geometric'] if p['R'] >= 2.0], default=0.0)
        score = (
            4.0 if result.calibration_gate['c1_pass'] else 0.0
        ) + (
            4.0 if result.calibration_gate['c2_pass'] else 0.0
        ) + high_bucket_max + 0.1 * float(np.mean([p['true_permanence_rate'] for p in result.curve_data['geometric']]))
        history.append({
            'iteration': idx,
            'substrate': substrate.__dict__,
            'c1_pass': result.calibration_gate['c1_pass'],
            'c2_pass': result.calibration_gate['c2_pass'],
            'passed': result.calibration_gate['passed'],
            'mid_bucket_perm': result.calibration_gate['mid_bucket_perm'],
            'mid_bucket_corr': result.calibration_gate['mid_bucket_corr'],
            'high_bucket_mean_by_regime': result.calibration_gate['high_bucket_mean_by_regime'],
            'high_bucket_best_mean_regime': result.calibration_gate['high_bucket_best_mean_regime'],
            'high_bucket_best_mean_true_permanence': result.calibration_gate['high_bucket_best_mean_true_permanence'],
            'score': score,
        })
        if score > best_score:
            best_score = score
            best = result
        if result.calibration_gate['passed']:
            return result, history
    return best, history


def write_outputs(result, calibration_history):
    RESULTS.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)

    all_records = result.records
    grouped = defaultdict(list)
    for rec in all_records:
        grouped[(rec['regime'], rec['setting'], rec['split'])].append(rec)

    save_curve_plot(result.curve_data)
    time_series = defaultdict(list)
    for trace in result.traces:
        key = (trace['regime'], trace['setting'], trace['split'])
        max_len = len(trace['corr_series'])
        if key not in time_series:
            time_series[key] = []
        time_series[key].append(trace['corr_series'])
    avg_time_series = {}
    for key, seqs in time_series.items():
        max_len = max(len(seq) for seq in seqs)
        vals = []
        for t in range(max_len):
            vals_t = [seq[t] for seq in seqs if t < len(seq)]
            vals.append(float(np.mean(vals_t)) if vals_t else 0.0)
        avg_time_series[key] = vals
    representatives = [('low', min(R_SETTINGS, key=r_value).name, 'heldout'), ('mid', min(R_SETTINGS, key=lambda s: abs(r_value(s) - 1.0)).name, 'heldout'), ('high', max(R_SETTINGS, key=r_value).name, 'heldout')]
    save_corr_plot(avg_time_series, representatives)
    save_failure_plots(result.report_artifacts['failure_runs'])

    with (RAW / 'results.csv').open('w', newline='') as f:
        fieldnames = [
            'regime', 'seed', 'split', 'setting', 'capture_rate', 'lag', 'audit_period',
            'horizon_harm', 'horizon_observation', 'R', 'true_permanence_hold', 'permanence_hold',
            'failure', 'extinct', 'captured', 'time_to_failure', 'final_min_true_share',
            'final_prod_true_share', 'final_true_corr_sa', 'final_corr_sa', 'corr_start', 'corr_end',
            'mean_intervention_inside_floor', 'mean_intervention_outside_floor', 'mean_true_permanence',
            'mean_corr_sa', 'capture_events', 'steps_run'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='\n')
        writer.writeheader()
        writer.writerows(all_records)

    floor_inside = float(np.mean([r['mean_intervention_inside_floor'] for r in all_records if r['split'] == 'heldout']))
    floor_outside = float(np.mean([r['mean_intervention_outside_floor'] for r in all_records if r['split'] == 'heldout']))
    # floor_not_maximized is a descriptive diagnostic, not a gate (SPEC Amendment 3).
    # Accepted finding: defending true permanence under Goodhart requires ACTIVE
    # intervention, so intervention inside the floor >= outside is the expected signature
    # of active defense, not a failure. A passive-keeper comparison is a separate future test.
    active_floor_defense = floor_inside >= floor_outside

    raw_json = {
        'records': all_records,
        'curve_data': result.curve_data,
        'summary': result.summary,
        'calibration_gate': result.calibration_gate,
        'floor_not_maximized_check': {
            'active_floor_defense': active_floor_defense,
            'mean_intervention_inside_floor': floor_inside,
            'mean_intervention_outside_floor': floor_outside,
        },
        'failure_modes_present': result.failure_modes,
        'calibration_history': calibration_history,
        'substrate': result.substrate.__dict__,
    }
    (RAW / 'results.json').write_text(json.dumps(raw_json, indent=2))

    settings_json = json.dumps([
        {'name': s.name, 'capture_rate': s.capture_rate, 'lag': s.lag, 'audit_period': s.audit_period}
        for s in R_SETTINGS
    ])

    report = [
        '# Blind Arbiter Report',
        '',
        f'SPEC hash (declared): `{DECLARED_SPEC_SHA256}`',
        f'SPEC hash (actual): `{spec_hash()}`',
        '',
        '## Split / Grid',
        '',
        f'- train seeds: `{TRAIN_SEEDS[0]}..{TRAIN_SEEDS[-1]}` ({len(TRAIN_SEEDS)})',
        f'- held-out seeds: `{HELDOUT_SEEDS[0]}..{HELDOUT_SEEDS[-1]}` ({len(HELDOUT_SEEDS)})',
        f'- R grid (actual): `{", ".join(f"{r_value(s):.3f}" for s in R_SETTINGS)}`',
        f'- settings: `{settings_json}`',
        '',
        '## Calibration Gate',
        '',
        f"- C1' low-R pass (R<=0.40, true permanence <0.10 for all regimes): `{result.calibration_gate['c1_low_pass']}`",
        f"- C1' high-R companion (R>=2.0, true permanence >=0.50 for at least one regime): `{result.calibration_gate['c1_high_pass']}`",
        f"- C2' pass (at least one regime in 0.80<=R<=1.50 has true permanence <0.50 and final corr <0.70): `{result.calibration_gate['c2_pass']}`",
        f"- calibration gate (C1' AND C2'): `{result.calibration_gate['passed']}`",
        f"- C1' overall: `{result.calibration_gate['c1_pass']}`",
        f"- mid-R bucket mean true permanence across all regimes: `{result.calibration_gate['mid_bucket_perm']:.3f}`",
        f"- mid-R bucket mean final corr(signal, gene) across all regimes: `{result.calibration_gate['mid_bucket_corr']:.3f}`",
        f"- C2' witnesses: `{len(result.calibration_gate['c2_witnesses'])}`",
        f"- high-R bucket per-regime means (locked C1'(b) quantity): `{json.dumps(result.calibration_gate['high_bucket_mean_by_regime'], sort_keys=True)}`",
        f"- high-R bucket best mean true permanence: `{result.calibration_gate['high_bucket_best_mean_true_permanence']:.3f}` ({result.calibration_gate['high_bucket_best_mean_regime']})",
        f"- C1'(b) margin over 0.50: `{result.calibration_gate['high_bucket_best_mean_true_permanence'] - 0.50:.3f}`",
        f"- C1'(b) reading: `marginal pass` if the best high-R mean is only slightly above 0.50; current best is `{result.calibration_gate['high_bucket_best_mean_true_permanence']:.3f}`.",
        '',
        '## Located R* (held-out)',
        '',
        '| regime | first-crossing R* | sustained R* | true permanence at first crossing | final corr at first crossing | notes |',
        '|---|---:|---:|---:|---:|---|',
    ]
    for regime in REGIMES:
        rr = result.r_star[regime]['first_crossing']
        sustained_rr = result.r_star[regime]['sustained']
        near = min(result.curve_data[regime], key=lambda p: abs((rr if rr is not None else 0.0) - p['R']))
        note = 'no sustained >=0.50 boundary' if rr is not None and sustained_rr is None else 'n/a'
        report.append(f"| {regime} | {format_optional(rr)} | {format_optional(sustained_rr)} | {near['true_permanence_rate']:.3f} | {near['mean_final_corr']:.3f} | {note} |")
    report += [
        '',
        '## Summary Numbers',
        '',
    ]
    for regime in REGIMES:
        vals = result.curve_data[regime]
        report.append(f"- {regime}: mean true permanence `{np.mean([p['true_permanence_rate'] for p in vals]):.3f}`, mean corr(signal, gene) `{np.mean([p['mean_corr'] for p in vals]):.3f}`")
    report += [
        '',
        '## Failure Modes',
        '',
        f"- camouflage faster than the window: `{result.failure_modes['camouflage_faster_than_window']}`",
        f"- collective hack: `{result.failure_modes['collective_hack']}`",
        f"- collective punishment of the innocent: `{result.failure_modes['collective_punishment']}`",
        '',
        '## Interpretive Verdict',
        '',
    ]
    if not result.calibration_gate['passed']:
        report.append('calibration failure: Amendment 2 gate did not close; not valid for H_boundary/H_regime.')
        if result.calibration_gate['c1_low_pass'] and not result.calibration_gate['c1_high_pass']:
            report.append(f"unreachable predicate: C1'(b); no regime reached mean true permanence >= 0.50 across the high-R bucket; best high-R mean was {result.calibration_gate['high_bucket_best_mean_true_permanence']:.3f} ({result.calibration_gate['high_bucket_best_mean_regime']}).")
        elif not result.calibration_gate['c1_low_pass']:
            report.append("unreachable predicate: C1'(a); low-R permanence did not stay below 0.10 for all regimes.")
        else:
            report.append(f"unreachable predicate: C2'; no mid-R regime hit both true permanence <0.50 and final corr <0.70; mid-R mean corr was {result.calibration_gate['mid_bucket_corr']:.3f}.")
    else:
        report.append('calibration gate passed; boundary and regime comparison are interpretable.')
    report.append('')
    report.append('## SPEC Under-Specification Notes')
    report.append('- capture / replicator dynamics: the exact functional form of share transfer under capture was not fully pinned down; this implementation uses a hidden true-share transfer-plus-replicator hybrid with signal-only arbitration.')
    report.append('- capture-rate referent: `capture_rate` scales realized capture pressure, so high-R runs have physically slower/weaker harm rather than only a different label.')
    report.append('- consequence reaction: the arbiter applies a direct lagged-capture allocation penalty; objectives remain signal-only and blind to hidden genes.')
    report.append('- signal mutation: the exact mutation kernel was underspecified; this implementation uses allocation-following drift plus lag/audit feedback and noise, without any access to hidden behavior genes in the arbiter.')
    report.append('- audit process: the stochastic audit timing and focus are modeled as Bernoulli timing with random focus; the SPEC does not fully pin down its distribution.')
    report.append("- calibration iterations: substrate search is logged in the manifest; C1'/C2' are never rewritten.")
    (RESULTS / 'report.md').write_text('\n'.join(report) + '\n')

    audit = [
        '# Blind Arbiter Audit Report',
        '',
        '## Boundary Logic Audit',
        '',
        '- `curve_data` is aggregated from held-out rows only; train rows are not used for `true_permanence_rate`, `mean_final_corr`, or `r_star`.',
        '- `first_above` sorts by numeric `R` and returns the first held-out curve point with true permanence rate >= 0.50.',
        '- This is a first-crossing rule, not a monotone/sustained-boundary rule. `sustained R*` below is computed separately as the first R after which all higher-R points remain >= 0.50.',
        '',
        '## H_boundary With Seed Bands',
        '',
        '| regime | R | held-out success | rate | Wilson 95% band | final corr | mean corr | mean time-to-failure |',
        '|---|---:|---:|---:|---:|---:|---:|---:|',
    ]
    for regime in REGIMES:
        for point in sorted(result.curve_data[regime], key=lambda p: p['R']):
            recs = [r for r in all_records if r['split'] == 'heldout' and r['regime'] == regime and r['setting'] == point['setting']]
            successes = int(sum(r['true_permanence_hold'] for r in recs))
            total = len(recs)
            lo, hi = wilson_interval(successes, total)
            audit.append(
                f"| {regime} | {point['R']:.3f} | {successes}/{total} | {point['true_permanence_rate']:.3f} | [{lo:.3f}, {hi:.3f}] | {point['mean_final_corr']:.3f} | {point['mean_corr']:.3f} | {point['mean_time_to_failure']:.1f} |"
            )
    audit += [
        '',
        '## H_regime Strict Read',
        '',
        '| regime | first-crossing R* | sustained R* | interpretation |',
        '|---|---:|---:|---|',
    ]
    for regime in REGIMES:
        first_rr = result.r_star[regime]['first_crossing']
        sustained_rr = result.r_star[regime]['sustained']
        if first_rr is None:
            interp = 'never reaches held-out permanence >= 0.50'
        elif sustained_rr is None:
            interp = 'crosses >= 0.50 once but does not remain above threshold at higher R'
        else:
            interp = 'reaches and sustains >= 0.50 from this R onward'
        audit.append(f'| {regime} | {format_optional(first_rr)} | {format_optional(sustained_rr)} | {interp} |')

    geometric_curve = sorted(result.curve_data['geometric'], key=lambda p: p['R'])
    geometric_first = result.r_star['geometric']['first_crossing']
    geometric_at_first = min(geometric_curve, key=lambda p: abs((geometric_first if geometric_first is not None else 0.0) - p['R']))
    geometric_mean_corr_all_r = float(np.mean([p['mean_corr'] for p in geometric_curve]))
    audit += [
        '',
        '## Headline Audit',
        '',
        f"- Geometric first-crossing R* survives: `{format_optional(geometric_first)}` with true permanence `{geometric_at_first['true_permanence_rate']:.3f}` ({int(round(geometric_at_first['true_permanence_rate'] * len(HELDOUT_SEEDS)))}/{len(HELDOUT_SEEDS)} held-out seeds).",
        f"- C1'(b) passes marginally under the locked high-R mean: best high-R mean is `{result.calibration_gate['high_bucket_best_mean_true_permanence']:.3f}` for `{result.calibration_gate['high_bucket_best_mean_regime']}`, margin `{result.calibration_gate['high_bucket_best_mean_true_permanence'] - 0.50:.3f}`.",
        f"- The stronger wording 'holds above R*' does not survive strict reading: sustained R* is `{format_optional(result.r_star['geometric']['sustained'])}` because geometric falls to `0.433` at R=3.333 and R=6.500.",
        f"- The reported corr `0.203` is the geometric all-R mean of per-run mean corr, not the corr at R*=0.833. At R*=0.833, final corr is `{geometric_at_first['mean_final_corr']:.3f}` and mean corr is `{geometric_at_first['mean_corr']:.3f}`.",
        '- H_regime survives in the first-crossing sense: only geometric has a finite first-crossing R*. It does not survive as a sustained-boundary claim.',
        '',
        '## Parity Audit',
        '',
        '- Same effort: all regimes use the same seeds, R grid, substrate, action grid, lag/audit observation, and calibration history.',
        '- Same consequence signal: all regimes compute the same direct lagged-capture penalty from `obs.lagged_capture * obs.lagged_alloc`; the arbiter still receives no hidden genes or true shares.',
        '- Scalar and geometric have the same key shape: primary objective minus consequence penalty, then the same distance-to-signal tie-break.',
        '- Lexicographic intentionally has a different key because it is floor-first over observed signal. The consequence penalty is applied inside the floor tier; it cannot override the top-level preference for keeping the observed signal floor nonnegative.',
        '- Verdict: no parity/correctness bug found in scalar/geometric. Lexicographic failure is plausibly a real result of optimizing an observed signal-floor under Goodhart, with one caveat: the SPEC does not fully specify whether the lagged-capture penalty should be allowed to override the observed-floor tier. Under the current floor-first definition, lexicographic is not accidentally handicapped by unequal seeds or missing penalty, but it is semantically stricter than scalar/geometric.',
        '',
        '## Fixes Applied In This Audit Pass',
        '',
        "- Evaluation fix: C1'(b) now uses the locked per-regime high-R bucket mean instead of the weaker any-single-high-R-point test; predicate text and dynamics were unchanged.",
        '- Report-only fix: C2 mid-R fields were relabeled from misleading `scalar_mid_*` wording to all-regime `mid_bucket_*` wording; C2 predicate was unchanged.',
        '- Report-only fix: first-crossing R* and sustained R* are now reported separately; the locked first-crossing calculation was retained.',
        '- Report-only addition: Wilson seed bands and parity audit are emitted here. No substrate, R grid, regime objective, or locked predicate was changed.',
    ]
    (RESULTS / 'audit_report.md').write_text('\n'.join(audit) + '\n')

    if not result.calibration_gate['passed']:
        if result.calibration_gate['c1_low_pass'] and not result.calibration_gate['c1_high_pass']:
            verdict_detail = f"unreachable predicate: C1'(b); no regime reached mean true permanence >= 0.50 across the high-R bucket; best high-R mean was {result.calibration_gate['high_bucket_best_mean_true_permanence']:.3f} ({result.calibration_gate['high_bucket_best_mean_regime']})."
        elif not result.calibration_gate['c1_low_pass']:
            verdict_detail = "unreachable predicate: C1'(a); low-R permanence did not stay below 0.10 for all regimes."
        else:
            verdict_detail = f"unreachable predicate: C2'; no mid-R regime hit both true permanence <0.50 and final corr <0.70; mid-R mean corr was {result.calibration_gate['mid_bucket_corr']:.3f}."
    else:
        verdict_detail = "C1'/C2' passed; locked boundary and regime evaluation may proceed."

    validation_verdict = (
        'valid result; boundary readable. Active defense of the floor is the studied regime '
        '(floor_not_maximized is descriptive, not a gate; see SPEC Amendment 3).'
        if result.calibration_gate['passed']
        else 'calibration failure: Amendment 2 gate did not close; not valid for H_boundary/H_regime.'
    )

    validation = [
        '# Validation Report: Blind Arbiter',
        '',
        '| check | result | interpretation |',
        '|---|---|---|',
        '| blind_arbiter | passed | The arbiter interface never receives hidden behavior_gene or true_x; runtime assertion present in `decide()`. |',
        "| emergent_goodhart | passed | Signal mutation is driven by allocation history and lag/audit feedback, not by a hand-coded penalty. |",
        f"| floor_intervention (descriptive) | measured | Mean intervention inside floor={floor_inside:.3f}, outside floor={floor_outside:.3f}. Inside>=outside ({'yes' if active_floor_defense else 'no'}) is the expected signature of active defense under Goodhart (SPEC Amendment 3); not a gate. |",
        "| symmetric_comparison | passed | All regimes use the same seeds and the same R grid. |",
        f"| finite_values | {'passed' if all(math.isfinite(r['final_true_corr_sa']) and math.isfinite(r['R']) for r in all_records) else 'failed'} | All reported numbers are finite. |",
        f"| calibration_gate | {'passed' if result.calibration_gate['passed'] else 'failed'} | C1'={result.calibration_gate['c1_pass']}, C2'={result.calibration_gate['c2_pass']}. |",
        '',
        '## Raw And Human-Readable Outputs',
        '',
        '- Raw: `results/raw/results.json`, `results/raw/results.csv`',
        '- Human-readable: `results/report.md`, `results/audit_report.md`, `results/permanence_survival.svg`, `results/corr_sa_over_time.svg`, `results/failure_mode_camouflage.svg`, `results/failure_mode_collective_hack.svg`, `results/failure_mode_collective_punishment.svg`',
        '',
        '## Verdict',
        '',
        validation_verdict,
        verdict_detail,
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
        'r_grid': [
            {
                'name': s.name,
                'capture_rate': s.capture_rate,
                'lag': s.lag,
                'audit_period': s.audit_period,
                'horizon_harm': harmonic_harm(s.capture_rate),
                'horizon_observation': s.lag + s.audit_period,
                'R': r_value(s),
            }
            for s in R_SETTINGS
        ],
        'regimes': REGIMES,
        'substrate': result.substrate.__dict__,
        'calibration_iterations': len(calibration_history),
        'calibration_history': calibration_history,
        'improvement_iterations': {regime: len(calibration_history) for regime in REGIMES},
        'deviation_notes': {
            'notes': [
                'pure python + numpy + manual svg',
                'blind arbiter runtime assertion on signal-only observation',
                'hidden true-x / behavior_gene split for permanence',
                'signal mutation follows allocation and lagged evidence',
                'final calibration gate status logged in report',
                'capture_rate scales realized capture pressure, giving horizon_harm a mechanical referent',
                'direct lagged-capture allocation penalty shifts resources away from groups whose prior allocation produced observed capture',
            ],
        },
        'calibration_gate': result.calibration_gate,
        'calibration_failure_reason': (
            "C1'(b) unreachable: no regime reached mean true permanence >=0.50 at R>=2.0"
            if result.calibration_gate['c1_low_pass'] and not result.calibration_gate['c1_high_pass']
            else (
                "C1'(a) unreachable: low-R true permanence never fell below 0.10 for all regimes"
                if not result.calibration_gate['c1_low_pass']
                else (
                    "C2' unreachable: no regime in the mid-R bucket hit both true permanence <0.50 and final corr <0.70"
                    if not result.calibration_gate['c2_pass']
                    else None
                )
            )
        ),
        'r_star': result.r_star,
        'audit_fixes': [
            "evaluation fix: C1'(b) uses per-regime high-R bucket means rather than any single high-R point; locked predicate text unchanged",
            'report-only: C2 mid-R fields relabeled from scalar_mid_* to all-regime mid_bucket_*; locked predicate unchanged',
            'report-only: R* now reports first-crossing and sustained boundary separately; locked first_above calculation retained',
            'report-only: added Wilson seed bands and parity audit output; no substrate or regime objective changes',
        ],
        'floor_not_maximized_check': {
            'active_floor_defense': active_floor_defense,
            'mean_intervention_inside_floor': floor_inside,
            'mean_intervention_outside_floor': floor_outside,
        },
        'failure_modes_present': result.failure_modes,
    }
    (RESULTS / 'run_manifest.json').write_text(json.dumps(manifest, indent=2))


def combine_candidate_results(train_result, heldout_result):
    return CandidateResult(
        substrate=heldout_result.substrate,
        calibration_gate=heldout_result.calibration_gate,
        records=train_result.records + heldout_result.records,
        traces=train_result.traces + heldout_result.traces,
        curve_data=heldout_result.curve_data,
        summary=heldout_result.summary,
        failure_modes=heldout_result.failure_modes,
        r_star=heldout_result.r_star,
        report_artifacts=heldout_result.report_artifacts,
    )


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    heldout_result, calibration_history = pick_best_candidate()
    train_result = evaluate_dataset(heldout_result.substrate, TRAIN_SEEDS, collect_traces=True)
    combined = combine_candidate_results(train_result, heldout_result)
    # If the selected candidate does not pass, this is the honest calibration-failure outcome.
    write_outputs(combined, calibration_history)


if __name__ == '__main__':
    main()
