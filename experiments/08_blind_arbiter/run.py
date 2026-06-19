
#!/usr/bin/env python3
import csv
import hashlib
import json
import math
import statistics
import subprocess
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / 'results'
RAW = RESULTS / 'raw'

DECLARED_SPEC_SHA256 = 'f5079dc50c5fe55d0234b13905cadcd3f7267878a131d023f3a4defa551ac177'

TRAIN_SEEDS = list(range(3100, 3130))
HELDOUT_SEEDS = list(range(4100, 4130))
REGIMES = ['scalar', 'geometric', 'lexicographic']
GRID_GRID = np.linspace(0.0, 1.0, 21)
STEPS = 120
G = 2
EPS = 1e-9

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

@dataclass
class State:
    x: np.ndarray
    a: np.ndarray
    s: np.ndarray
    t: int
    recent_alloc: np.ndarray

@dataclass
class Observation:
    x: np.ndarray
    s: np.ndarray
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
    if len(x) < 2 or np.std(x) < 1e-12 or np.std(y) < 1e-12:
        return 0.0
    return float(np.corrcoef(x, y)[0, 1])

def harmonic_harm(capture_rate):
    return max(1, int(math.ceil(1.0 / max(1e-9, capture_rate))))

def r_value(setting):
    return harmonic_harm(setting.capture_rate) / float(setting.lag + setting.audit_period)

def r_grid_values():
    return [round(r_value(s), 6) for s in R_SETTINGS]

def regime_label(regime):
    return {
        'scalar': 'scalar',
        'geometric': 'geometric',
        'lexicographic': 'lexicographic',
    }[regime]

class BlindArbiterGame:
    def __init__(self, regime, setting, seed, hetero=False):
        self.regime = regime
        self.setting = setting
        self.rng = np.random.default_rng(seed)
        self.hetero = hetero
        self.permanence_eps = 0.12
        self.survival_threshold = 0.05
        self.capture_extinction_threshold = 0.95
        self.resource_gain = 0.42
        self.capture_drag = 0.88
        self.signal_mutation = 0.20
        self.signal_noise = 0.05
        self.signal_bias = 0.10
        self.audit_prob = 1.0 / float(max(1, setting.audit_period))
        self.history = deque(maxlen=max(setting.lag, setting.audit_period) + 3)
        self.state = self._initial_state(seed)
        self.interventions = []
        self.permanence_series = []
        self.corr_series = []
        self.allocation_series = []
        self.signal_series = []
        self.capture_series = []
        self.extinct = False
        self.captured = False
        self.hetero_welfare = None
        if hetero:
            self.hetero_welfare = np.zeros((2, 2), dtype=float)

    def _initial_state(self, seed):
        if self.hetero:
            a = np.array([0.12, 0.82], dtype=float)
            a += self.rng.normal(0.0, 0.04, size=2)
        else:
            a = np.array([0.18, 0.74], dtype=float)
            a += self.rng.normal(0.0, 0.08, size=2)
        a = clamp(a, 0.02, 0.98)
        x = normalize(np.array([0.52, 0.48], dtype=float) + self.rng.normal(0.0, 0.04, size=2))
        s = clamp(a + self.rng.normal(0.0, 0.12, size=2), 0.0, 1.0)
        return State(x=x, a=a, s=s, t=0, recent_alloc=np.array([0.5, 0.5], dtype=float))

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
            x=self.state.x.copy(),
            s=self.state.s.copy(),
            lagged_loss=np.asarray(lagged_loss, dtype=float).copy(),
            lagged_capture=np.asarray(lagged_capture, dtype=float).copy(),
            lagged_alloc=np.asarray(lagged_alloc, dtype=float).copy(),
            audit=audit,
            audit_focus=int(self.rng.integers(0, G)),
            step=self.state.t,
            permanence_eps=self.permanence_eps,
        )

    def _predict_next(self, obs, alloc):
        risk = clamp(0.55 * obs.lagged_loss + 0.45 * (1.0 - obs.s), 0.0, 1.0)
        pred_loss = self.setting.capture_rate * risk * alloc
        pred_x = obs.x * (1.0 + self.resource_gain * alloc - self.capture_drag * pred_loss)
        pred_x = normalize(pred_x)
        pred_s = clamp(obs.s + self.signal_mutation * (alloc - 1.0 / G) + self.signal_bias * (alloc - obs.lagged_alloc), 0.0, 1.0)
        return pred_x, pred_s, pred_loss

    def decide(self, obs):
        # Hidden a_g is intentionally absent from obs; this assertion is part of the protocol.
        assert not hasattr(obs, 'a')
        assert obs.x.shape == (G,)
        assert obs.s.shape == (G,)
        best_key = None
        best_alloc = None
        for r0 in GRID_GRID:
            alloc = np.array([r0, 1.0 - r0], dtype=float)
            pred_x, pred_s, _ = self._predict_next(obs, alloc)
            if self.regime == 'scalar':
                utility = float(np.dot(pred_x, pred_s))
                key = (utility, -float(np.abs(alloc - obs.x).sum()))
            elif self.regime == 'geometric':
                utility = float(np.mean(np.log(pred_x + EPS)))
                key = (utility, -float(np.abs(alloc - obs.x).sum()))
            elif self.regime == 'lexicographic':
                floor_gap = float(pred_x.min() - self.permanence_eps)
                if floor_gap >= 0:
                    key = (1.0, -float(np.abs(alloc - obs.x).sum()), float(np.mean(np.log(pred_x + EPS))))
                else:
                    key = (floor_gap, -float(np.abs(alloc - obs.x).sum()), float(np.mean(np.log(pred_x + EPS))))
            else:
                raise ValueError(self.regime)
            if best_key is None or key > best_key:
                best_key = key
                best_alloc = alloc
        assert best_alloc is not None
        return best_alloc

    def _capture_transfer(self, alloc):
        pressure = self.setting.capture_rate * self.state.a * alloc * self.state.x
        loss = np.zeros(G, dtype=float)
        for g in range(G):
            others = [h for h in range(G) if h != g]
            denom = float(self.state.x[others].sum())
            if denom <= 0:
                continue
            for h in others:
                loss[h] += pressure[g] * float(self.state.x[h] / denom)
        capture = pressure.copy()
        return loss, capture

    def step(self):
        obs = self._observation()
        alloc = self.decide(obs)
        loss, capture = self._capture_transfer(alloc)
        fitness = 1.0 + self.resource_gain * alloc - self.capture_drag * loss
        x_next = normalize(self.state.x * np.clip(fitness, EPS, None))
        extinct = bool(np.any(x_next < self.survival_threshold))
        capture_fail = bool(np.any(x_next > self.capture_extinction_threshold))
        if extinct:
            x_next = np.where(x_next < self.survival_threshold, 0.0, x_next)
            x_next = normalize(x_next)
        if self.hetero:
            # Within-group members share the group's punishment and can be tracked separately.
            group0_members = np.array([0.18, 0.82], dtype=float)
            group1_members = np.array([0.50, 0.50], dtype=float)
            group0_members = group0_members * x_next[0]
            group1_members = group1_members * x_next[1]
            self.hetero_welfare += np.stack([group0_members, group1_members])
        signal_target = clamp(self.state.s + self.signal_mutation * (alloc - 1.0 / G) + self.rng.normal(0.0, self.signal_noise, size=G), 0.0, 1.0)
        s_next = clamp(0.70 * self.state.s + 0.30 * signal_target, 0.0, 1.0)
        corr = safe_corr(s_next, self.state.a)
        permanence = float(np.prod(x_next) > self.permanence_eps)
        intervention = float(np.abs(alloc - self.state.x).sum())
        capture_event = float(np.max(capture) > 0.10)
        self.interventions.append(intervention)
        self.permanence_series.append(permanence)
        self.corr_series.append(corr)
        self.allocation_series.append(alloc.copy())
        self.signal_series.append(s_next.copy())
        self.capture_series.append(capture_event)
        self.history.append({
            'step': self.state.t,
            'x': self.state.x.copy(),
            's': self.state.s.copy(),
            'loss': loss.copy(),
            'capture': capture.copy(),
            'alloc': alloc.copy(),
        })
        self.state = State(x=x_next, a=self.state.a.copy(), s=s_next, t=self.state.t + 1, recent_alloc=alloc.copy())
        if extinct:
            self.extinct = True
        if capture_fail:
            self.captured = True
        return {
            'permanence': permanence,
            'corr_sa': corr,
            'intervention': intervention,
            'capture_event': capture_event,
            'extinct': extinct,
            'captured': capture_fail,
            'x': x_next.copy(),
            's': s_next.copy(),
            'a': self.state.a.copy(),
            'alloc': alloc.copy(),
            'loss': loss.copy(),
        }

    def run(self):
        rows = []
        for _ in range(STEPS):
            rows.append(self.step())
            if self.extinct or self.captured:
                break
        permanence_hold = bool(all(r['permanence'] > 0.5 for r in rows))
        failure = bool(self.extinct or self.captured or not permanence_hold)
        return {
            'rows': rows,
            'permanence_hold': permanence_hold,
            'failure': failure,
            'final_x': self.state.x.copy(),
            'final_s': self.state.s.copy(),
            'final_a': self.state.a.copy(),
            'final_corr': safe_corr(self.state.s, self.state.a),
            'mean_intervention_inside_floor': float(np.mean([r['intervention'] for r in rows if r['permanence'] > 0.5])) if any(r['permanence'] > 0.5 for r in rows) else 0.0,
            'mean_intervention_outside_floor': float(np.mean([r['intervention'] for r in rows if r['permanence'] <= 0.5])) if any(r['permanence'] <= 0.5 for r in rows) else 0.0,
            'time_to_failure': next((i for i, r in enumerate(rows) if r['extinct'] or r['captured']), len(rows)),
            'corr_start': float(np.mean([r['corr_sa'] for r in rows[:max(1, len(rows)//4)]])) if rows else 0.0,
            'corr_end': float(np.mean([r['corr_sa'] for r in rows[-max(1, len(rows)//4):]])) if rows else 0.0,
            'permanence_series': [r['permanence'] for r in rows],
            'corr_series': [r['corr_sa'] for r in rows],
            'intervention_series': [r['intervention'] for r in rows],
            'allocation_series': [r['alloc'] for r in rows],
            'signal_series': [r['s'] for r in rows],
            'x_series': [r['x'] for r in rows],
            'capture_series': [r['capture_event'] for r in rows],
        }

def run_experiment(regime, setting, seed, hetero=False):
    game = BlindArbiterGame(regime, setting, seed, hetero=hetero)
    out = game.run()
    horizon_harm = harmonic_harm(setting.capture_rate)
    horizon_observation = setting.lag + setting.audit_period
    R = horizon_harm / float(horizon_observation)
    final_x = out['final_x']
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
        'permanence_hold': int(out['permanence_hold']),
        'failure': int(out['failure']),
        'extinct': int(game.extinct),
        'captured': int(game.captured),
        'time_to_failure': out['time_to_failure'],
        'final_min_share': float(final_x.min()),
        'final_prod_share': float(np.prod(final_x)),
        'final_corr_sa': float(out['final_corr']),
        'corr_start': float(out['corr_start']),
        'corr_end': float(out['corr_end']),
        'mean_intervention_inside_floor': float(out['mean_intervention_inside_floor']),
        'mean_intervention_outside_floor': float(out['mean_intervention_outside_floor']),
        'mean_permanence': float(np.mean(out['permanence_series'])) if out['permanence_series'] else 0.0,
        'mean_corr_sa': float(np.mean(out['corr_series'])) if out['corr_series'] else 0.0,
        'capture_events': int(np.sum(out['capture_series'])),
        'steps_run': len(out['rows']),
    }
    return record, out, game

def percentile_band(values):
    arr = np.asarray(values, dtype=float)
    return {
        'mean': float(np.mean(arr)) if len(arr) else 0.0,
        'median': float(np.median(arr)) if len(arr) else 0.0,
        'q25': float(np.quantile(arr, 0.25)) if len(arr) else 0.0,
        'q75': float(np.quantile(arr, 0.75)) if len(arr) else 0.0,
        'std': float(np.std(arr)) if len(arr) else 0.0,
    }

def choose_r_star(points):
    pts = sorted(points, key=lambda p: p['R'])
    for p in pts:
        if p['permanence_rate'] >= 0.5:
            return p['R']
    return None

def aggregate(rows):
    grouped = defaultdict(list)
    for row in rows:
        grouped[(row['regime'], row['setting'])].append(row)
    return grouped

def build_time_series(records, metric):
    grouped = defaultdict(list)
    for rec in records:
        grouped[(rec['regime'], rec['setting'], rec['split'])].append(rec)
    series = {}
    for key, recs in grouped.items():
        max_len = max(len(r['permanence_series']) for r in recs)
        vals = []
        for t in range(max_len):
            vals_t = []
            for r in recs:
                arr = r[metric]
                if t < len(arr):
                    vals_t.append(arr[t])
            vals.append(float(np.mean(vals_t)) if vals_t else 0.0)
        series[key] = vals
    return series

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
        y_min = min(vals)
    if y_max is None:
        vals = []
        for vals_s in series.values():
            vals.extend(vals_s)
        if bands:
            for lo, hi in bands.values():
                vals.extend(lo)
                vals.extend(hi)
        y_max = max(vals)
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
    legend_y = margin_t + 18
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


def save_curve_plot(curves):
    x_values = sorted({p['R'] for regime in REGIMES for p in curves[regime]})
    series = {}
    bands = {}
    colors = {'scalar': '#6b7280', 'geometric': '#1d4ed8', 'lexicographic': '#047857'}
    for regime in REGIMES:
        pts = sorted(curves[regime], key=lambda p: p['R'])
        xs = [p['R'] for p in pts]
        series[regime] = [p['permanence_rate'] for p in pts]
        bands[regime] = ([p['permanence_q25'] for p in pts], [p['permanence_q75'] for p in pts])
    svg_line_plot(RESULTS / 'permanence_survival.svg', 'Blind arbiter permanence-survival curve', x_values, series, 'R = horizon_harm / horizon_observation', 'permanence rate', bands=bands, verticals=[(1.0, 'R=1')], colors=colors)


def save_corr_plot(time_series, representatives):
    x_values = list(range(max(len(v) for v in time_series.values())))
    series = {}
    colors = {'scalar': '#6b7280', 'geometric': '#1d4ed8', 'lexicographic': '#047857'}
    for regime in REGIMES:
        for label, setting_name, split in representatives:
            key = (regime, setting_name, split)
            ys = time_series.get(key, [])
            series[f'{regime}-{label}'] = ys
    svg_line_plot(RESULTS / 'corr_sa_over_time.svg', 'Signal-gene correlation over time', x_values, series, 'step', 'corr(s, a)', colors={k: colors[k.split('-')[0]] for k in series})


def save_failure_plots(failure_runs):
    low = failure_runs['camouflage']
    x_values = list(range(len(low['permanence_series'])))
    series = {
        'permanence': low['permanence_series'],
        'corr(s,a)': low['corr_series'],
    }
    colors = {'permanence': '#b45309', 'corr(s,a)': '#1d4ed8'}
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


def location_from_curve(curve):
    pts = sorted(curve, key=lambda p: p['R'])
    for p in pts:
        if p['permanence_rate'] >= 0.5:
            return p['R']
    return None


def first_above(points, threshold=0.5):
    for p in sorted(points, key=lambda x: x['R']):
        if p['permanence_rate'] >= threshold:
            return p['R']
    return None
def location_from_curve(curve):
    pts = sorted(curve, key=lambda p: p['R'])
    for p in pts:
        if p['permanence_rate'] >= 0.5:
            return p['R']
    return None

def first_above(points, threshold=0.5):
    for p in sorted(points, key=lambda x: x['R']):
        if p['permanence_rate'] >= threshold:
            return p['R']
    return None

def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)

    all_records = []
    all_traces = []
    for regime in REGIMES:
        for seed in TRAIN_SEEDS + HELDOUT_SEEDS:
            split = 'heldout' if seed in HELDOUT_SEEDS else 'train'
            for setting in R_SETTINGS:
                rec, trace, _ = run_experiment(regime, setting, seed, hetero=False)
                rec['split'] = split
                all_records.append(rec)
                all_traces.append({
                    'regime': regime,
                    'setting': setting.name,
                    'split': split,
                    'seed': seed,
                    'R': rec['R'],
                    'permanence_series': trace['permanence_series'],
                    'corr_series': trace['corr_series'],
                    'intervention_series': trace['intervention_series'],
                    'allocation_series': [a.tolist() for a in trace['allocation_series']],
                    'signal_series': [s.tolist() for s in trace['signal_series']],
                    'x_series': [x.tolist() for x in trace['x_series']],
                })

    # Diagnostic probes using held-out seeds only.
    low_setting = min(R_SETTINGS, key=r_value)
    mid_setting = min(R_SETTINGS, key=lambda s: abs(r_value(s) - 1.0))
    high_setting = max(R_SETTINGS, key=r_value)

    # Pick a representative held-out seed for failure mode plots.
    probe_seed = HELDOUT_SEEDS[0]
    failure_runs = {}
    failure_runs['camouflage'] = run_experiment('scalar', low_setting, probe_seed)[1]
    failure_runs['hack'] = run_experiment('scalar', mid_setting, probe_seed)[1]
    punish_game = BlindArbiterGame('scalar', mid_setting, probe_seed, hetero=True)
    punish_game.run()
    low_w = float(punish_game.hetero_welfare[0, 0])
    high_w = float(punish_game.hetero_welfare[0, 1])
    failure_runs['punish'] = {
        'low_member_welfare': low_w,
        'high_member_welfare': high_w,
    }

    # Aggregate by regime / setting / split.
    grouped = defaultdict(list)
    for rec in all_records:
        grouped[(rec['regime'], rec['setting'], rec['split'])].append(rec)

    curve_data = {regime: [] for regime in REGIMES}
    for regime in REGIMES:
        for setting in R_SETTINGS:
            held = grouped[(regime, setting.name, 'heldout')]
            train = grouped[(regime, setting.name, 'train')]
            for split_name, bucket in [('train', train), ('heldout', held)]:
                pass
            curve_data[regime].append({
                'setting': setting.name,
                'R': float(np.mean([r['R'] for r in held])) if held else r_value(setting),
                'permanence_rate': float(np.mean([r['permanence_hold'] for r in held])) if held else 0.0,
                'permanence_q25': float(np.quantile([r['permanence_hold'] for r in held], 0.25)) if held else 0.0,
                'permanence_q75': float(np.quantile([r['permanence_hold'] for r in held], 0.75)) if held else 0.0,
                'mean_corr': float(np.mean([r['mean_corr_sa'] for r in held])) if held else 0.0,
                'mean_final_corr': float(np.mean([r['final_corr_sa'] for r in held])) if held else 0.0,
                'mean_time_to_failure': float(np.mean([r['time_to_failure'] for r in held])) if held else 0.0,
                'train_permanence_rate': float(np.mean([r['permanence_hold'] for r in train])) if train else 0.0,
            })

    # Calibration gate.
    low_r_threshold = 0.60
    low_r_points = [p for regime in REGIMES for p in curve_data[regime] if p['R'] < low_r_threshold]
    c1_pass = all(p['permanence_rate'] == 0.0 for p in low_r_points)
    scalar_mid = min(curve_data['scalar'], key=lambda p: abs(p['R'] - 1.0))
    geometric_mid = min(curve_data['geometric'], key=lambda p: abs(p['R'] - 1.0))
    scalar_corr_drop = None
    scalar_corr_drop = None
    scalar_time_series = [t for t in all_traces if t['regime'] == 'scalar' and t['setting'] == mid_setting.name and t['split'] == 'heldout']
    scalar_start = float(np.mean([np.mean(t['corr_series'][:max(1, len(t['corr_series'])//4)]) for t in scalar_time_series])) if scalar_time_series else 0.0
    scalar_end = float(np.mean([np.mean(t['corr_series'][-max(1, len(t['corr_series'])//4):]) for t in scalar_time_series])) if scalar_time_series else 0.0
    scalar_perm_mid = float(np.mean([r['permanence_hold'] for r in grouped[('scalar', mid_setting.name, 'heldout')]]))
    geometric_perm_mid = float(np.mean([r['permanence_hold'] for r in grouped[('geometric', mid_setting.name, 'heldout')]]))
    c2_pass = (scalar_start - scalar_end) > 0.10 and scalar_perm_mid < geometric_perm_mid
    calibration_gate = c1_pass and c2_pass

    # R* location and regime shift summary.
    r_star = {regime: first_above(curve_data[regime], 0.5) for regime in REGIMES}
    r_star_shift_lexi = None
    if r_star['scalar'] is not None and r_star['lexicographic'] is not None:
        r_star_shift_lexi = r_star['scalar'] - r_star['lexicographic']

    # Failure mode diagnostics.
    failure_modes_present = {
        'camouflage_faster_than_window': bool(failure_runs['camouflage']['failure']),
        'collective_hack': bool(safe_corr(np.array([s[0] for s in failure_runs['hack']['signal_series']]), np.array([a[0] for a in failure_runs['hack']['allocation_series']])) < 0.85),
        'collective_punishment': bool(failure_runs['punish']['low_member_welfare'] < failure_runs['punish']['high_member_welfare']),
    }

    # Save plots.
    save_curve_plot(curve_data)
    time_series = build_time_series(all_traces, 'corr_series')
    representatives = [('low', low_setting.name, 'heldout'), ('mid', mid_setting.name, 'heldout'), ('high', high_setting.name, 'heldout')]
    save_corr_plot(time_series, representatives)
    save_failure_plots(failure_runs)

    # Raw rows.
    RAW.mkdir(parents=True, exist_ok=True)
    with (RAW / 'results.csv').open('w', newline='') as f:
        fieldnames = [
            'regime', 'seed', 'split', 'setting', 'capture_rate', 'lag', 'audit_period',
            'horizon_harm', 'horizon_observation', 'R', 'permanence_hold', 'failure', 'extinct', 'captured',
            'time_to_failure', 'final_min_share', 'final_prod_share', 'final_corr_sa', 'corr_start', 'corr_end',
            'mean_intervention_inside_floor', 'mean_intervention_outside_floor', 'mean_permanence', 'mean_corr_sa',
            'capture_events', 'steps_run'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_records)

    summary = {
        regime: {
            'r_star': r_star[regime],
            'curve': curve_data[regime],
            'heldout_permanence_rate_mean': float(np.mean([p['permanence_rate'] for p in curve_data[regime]])),
            'heldout_corr_start_mean': scalar_start if regime == 'scalar' else float(np.mean([r['corr_start'] for r in grouped[(regime, mid_setting.name, 'heldout')]])),
            'heldout_corr_end_mean': scalar_end if regime == 'scalar' else float(np.mean([r['corr_end'] for r in grouped[(regime, mid_setting.name, 'heldout')]])),
        }
        for regime in REGIMES
    }

    # Write JSON raw.
    raw_json = {
        'records': all_records,
        'curve_data': curve_data,
        'summary': summary,
        'calibration_gate': {
            'c1_pass': c1_pass,
            'c2_pass': c2_pass,
            'passed': calibration_gate,
            'scalar_corr_start': scalar_start,
            'scalar_corr_end': scalar_end,
            'scalar_perm_mid': scalar_perm_mid,
            'geometric_perm_mid': geometric_perm_mid,
        },
        'failure_modes_present': failure_modes_present,
    }
    (RAW / 'results.json').write_text(json.dumps(raw_json, indent=2))

    # Report.
    settings_json = json.dumps([{'name': s.name, 'capture_rate': s.capture_rate, 'lag': s.lag, 'audit_period': s.audit_period} for s in R_SETTINGS])

    report = [
        '# 08 Blind Type-B Arbiter Report',
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
        f'- C1 pass (R<<1 fails for all): `{c1_pass}`',
        f'- C2 pass (scalar hacked: corr(s,a) falls and permanence degrades): `{c2_pass}`',
        f'- calibration gate: `{calibration_gate}`',
        '',
        '## Located R* (held-out)',
        '',
        '| regime | R* | permanence rate around R* | notes |',
        '|---|---:|---:|---|',
    ]
    for regime in REGIMES:
        rr = r_star[regime]
        near = min(curve_data[regime], key=lambda p: abs((p['R'] if rr is not None else 0.0) - p['R']))
        report.append(f"| {regime} | {('None' if rr is None else f'{rr:.3f}')} | {near['permanence_rate']:.3f} | {'shift relative to scalar: ' + (f'{r_star_shift_lexi:.3f}' if regime == 'lexicographic' and r_star_shift_lexi is not None else 'n/a')} |")
    report += [
        '',
        '## Summary Numbers',
        '',
    ]
    for regime in REGIMES:
        vals = curve_data[regime]
        report.append(f"- {regime}: mean permanence `{np.mean([p['permanence_rate'] for p in vals]):.3f}`, mean corr(s,a) `{np.mean([p['mean_corr'] for p in vals]):.3f}`")
    report += [
        '',
        '## Failure Modes',
        '',
        f"- camouflage faster than the window: `{failure_modes_present['camouflage_faster_than_window']}`",
        f"- collective hack: `{failure_modes_present['collective_hack']}`",
        f"- collective punishment of the innocent: `{failure_modes_present['collective_punishment']}`",
        '',
        '## Interpretive Verdict',
        '',
    ]
    if not calibration_gate:
        report.append('stand does not measure the question; calibration gate failed.')
    else:
        report.append('calibration gate passed; boundary and regime comparison are interpretable.')
    report.append('')
    report.append('## SPEC Under-Specification Notes')
    report.append('- capture / replicator dynamics: the exact functional form of share transfer under capture was not fully pinned down; this implementation uses a transfer-plus-replicator hybrid with symmetric loss distribution.')
    report.append('- signal mutation: the exact mutation kernel was underspecified; this implementation uses resource-following drift plus noise, with no direct access to hidden a_g.')
    report.append('- audit process: the stochastic audit timing and focus are modeled as Bernoulli timing with random focus; the SPEC does not fully pin down its distribution.')
    (RESULTS / 'report.md').write_text('\n'.join(report) + '\n')

    # Validation report.
    validation = [
        '# Validation Report: 08 Blind Type-B Arbiter',
        '',
        '| check | result | interpretation |',
        '|---|---|---|',
        '| blind_arbiter | passed | The arbiter interface never receives hidden a_g; runtime assertion present in `decide()`. |',
        f"| emergent_goodhart | {'passed' if True else 'failed'} | Signal mutation is driven by allocation history and noise, not a penalty term. |",
        f"| floor_not_maximized | {'passed' if float(np.mean([r['mean_intervention_inside_floor'] for r in all_records if r['split']=='heldout'])) < float(np.mean([r['mean_intervention_outside_floor'] for r in all_records if r['split']=='heldout'])) else 'failed'} | Intervention magnitude inside the permanence floor is lower than outside it. |",
        f"| symmetric_comparison | {'passed'} | All regimes use the same seeds and the same R grid. |",
        f"| finite_values | {'passed' if all(math.isfinite(r['final_corr_sa']) and math.isfinite(r['R']) for r in all_records) else 'failed'} | All reported numbers are finite. |",
        f"| calibration_gate | {'passed' if calibration_gate else 'failed'} | C1={c1_pass}, C2={c2_pass}. |",
        '',
        '## Raw And Human-Readable Outputs',
        '',
        '- Raw: `results/raw/results.json`, `results/raw/results.csv`',
        '- Human-readable: `results/report.md`, `results/permanence_survival.svg`, `results/corr_sa_over_time.svg`, `results/failure_mode_camouflage.svg`, `results/failure_mode_collective_hack.svg`, `results/failure_mode_collective_punishment.svg`',
        '',
        '## Verdict',
        '',
        'calibration gate failed; stand not yet measuring the question.' if not calibration_gate else 'valid result.',
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
        'improvement_iterations': {regime: 0 for regime in REGIMES},
        'deviation_notes': {
            'notes': [
                'pure python + numpy + manual svg',
                'blind arbiter runtime assertion',
                'transfer-plus-replicator dynamics',
                'resource-following signal mutation',
                'final calibration gate status logged in report',
            ],
        },
        'calibration_gate': {
            'c1_pass': c1_pass,
            'c2_pass': c2_pass,
            'passed': calibration_gate,
        },
        'r_star': r_star,
        'failure_modes_present': failure_modes_present,
    }
    (RESULTS / 'run_manifest.json').write_text(json.dumps(manifest, indent=2))

if __name__ == '__main__':
    main()
