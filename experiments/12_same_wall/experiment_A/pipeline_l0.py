"""
L0 DESIGN LOCK — the full Experiment A pipeline (PREREG v4.1 + AMENDMENT-1).

Self-contained by design: no imports from scouts/ (which remain mutable
history); worlds_general.py is part of experiment_A and locked with this
file. Modes: `tune` (OC-tune, n_MC=200), `validate` (OC-validate,
n_MC=100, applies a frozen theta), `primary` (the locked run; only after
L1). Every rule below encodes a section of PREREG_v4_DRAFT.md; section
tags are cited inline.

Frozen at L0 (F4.3): this code, the lattice ranges, the OC algorithm,
the tie-break rule (§7), MC counts (200/100), the certification battery
(AMENDMENT-1: wrong-value agreement <= 6/24).
"""
import os, sys, json, random, importlib.util
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from worlds_general import (GWorld, GCycle, GAliasCycle, GLollipop, GWobble,
                            GNonstationary, GOracle, run_language,
                            lang_A_general, lang_G_translated)

# ---------- locked constants (§2, §4, §7) ------------------------------------
CAP = 400
R_INST = 8
K_SEEDS = 8
PERTS = [('id', 0, False), ('bp+1', 1, False), ('bp+3', 3, False),
         ('rev', 0, True), ('nseed', 0, False)]
TOKEN_MARGIN = 0.05
JOURNAL_MARGIN = 0.10
SENS_MIN = 0.30
CERT_WRONG_MAX = 6          # AMENDMENT-1: wrong-agreement <= 6/24
N_MC_TUNE = 200
N_MC_VALIDATE = 100
ALPHA = 0.05                # one-sided exact binomial bounds, 95%
POWER_MIN = 0.8

def _load(name, fname):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, 'received', fname))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m

_gptA = _load('l0_gptA', 'find_order_solvers.py')
_gptB = _load('l0_gptB', 'find_order_spec_encoding_b.py')
_grok = _load('l0_grok', 'find_order_2.py')
_gem = _load('l0_gem', 'find_order_3.py')
_opusA = _load('l0_opusA', 'find_order.py')

MAINS = {'A': lang_A_general, 'gptA': _gptA.find_order_main,
         'gptB': _gptB.find_order_main, 'grok': _grok.find_order_main,
         'gem': _gem.find_order_main, 'opusA': _opusA.find_order_main}
REFS_EXTRA = {'gptA.r1': _gptA.find_order_ref1, 'gptA.r2': _gptA.find_order_ref2,
              'gptB.r1': _gptB.find_order_ref1, 'grok.r1': _grok.find_order_ref1,
              'gem.r1': _gem.find_order_ref1, 'opusA.r1': _opusA.find_order_ref1}
FAMILY = {k: k.split('.')[0] for k in list(MAINS) + list(REFS_EXTRA)}
SALT = {n: 101 + 37 * i for i, n in enumerate(list(MAINS) + list(REFS_EXTRA)
                                              + ['A2', 'Gt', 'PM1', 'PM2'])}

# registered pairs (§3); RP allocations (Appendix R, post-AMENDMENT-1)
RP_POOL = {'RP-01': ('gptA', 'grok'), 'RP-02': ('gptB', 'gem'),
           'RP-03': ('gptA', 'gem'), 'RP-04': ('grok', 'gem'),
           'RP-05': ('opusA', 'gptB'), 'RP-07': ('opusA', 'gem'),
           'RP-08': ('gptB', 'grok'), 'RP-09': ('gptA', 'gptB')}
# RP-06 excluded (cert: wrong-agreement 12/24)
FIELD_ALLOC = {('A', 'gptA'): ['RP-04', 'RP-05', 'RP-07', 'RP-08'],
               ('A', 'Gt'): ['RP-04', 'RP-05', 'RP-07', 'RP-08', 'RP-09'],
               ('A', 'A2'): ['RP-04', 'RP-05', 'RP-07', 'RP-08', 'RP-09'],
               ('A', 'opusA'): ['RP-04', 'RP-08', 'RP-09'],
               ('PM1', 'PM2'): ['RP-04', 'RP-05', 'RP-07', 'RP-08', 'RP-09']}
C2_AUDIT = [('gptA', 'grok'), ('gptB', 'gem'), ('gptA', 'gem'), ('A', 'gem')]
C8_H, C8_M = ('A', 'opusA'), ('A', 'grok')

# ---------- worlds lattice (§2, locked ranges) --------------------------------

class QuotientTrap(GWorld):
    def __init__(self, n, q, wrng, frac=0.6):
        self.n, self.q, self.eps, self.truth = n, q, 0.0, n
        self.trapped = {m for m in range(q, n, q) if wrng.random() < frac}
    def run(self, word, bp=0):
        return (bp + word.count('R') - word.count('L')) % self.n
    def same(self, u, v, bp=0):
        d = (self.run(u, bp) - self.run(v, bp)) % self.n
        return d == 0 or d in self.trapped

class NullWorld(GWorld):
    """K3: consistent random answer function; truth None. AMENDMENT-3(a):
    stable hashing (process-independent) — builtin hash() is randomized
    per process, which made the gate nondeterministic across runs."""
    def __init__(self, seed): self.seed, self.eps, self.truth = seed, 0.0, None
    def run(self, word, bp=0): return 0
    def same(self, u, v, bp=0):
        import hashlib
        h = hashlib.md5(('%s|%s|%d' % (u, v, self.seed)).encode()).digest()
        return h[0] < 128

STRATA_DEF = [
    ('cycle',    lambda r: GCycle(r.randint(17, 40)), lambda w: w.truth),
    ('alias',    lambda r: (lambda n: GAliasCycle(n, r.choice(
                     [d for d in range(4, n // 2 + 1) if n % d == 0])))(
                     r.choice([20, 24, 30, 36])), lambda w: w.truth),
    ('noisy',    lambda r: GCycle(r.randint(17, 40), eps=r.uniform(0.02, 0.12)),
                 lambda w: w.truth),
    ('qtrap',    lambda r: (lambda q: QuotientTrap(q * r.randint(3, 5), q, r))(
                     r.randint(5, 9)), lambda w: w.truth),
    ('wobble',   lambda r: GWobble(r.randint(17, 40)), lambda w: None),
    ('lollipop', lambda r: GLollipop(r.randint(5, 12), r.randint(12, 26)),
                 lambda w: None),
    ('nonstat',  lambda r: GNonstationary(r.randint(15, 26), r.randint(27, 40),
                                          r.randint(60, 200)), lambda w: None),
]
STRATUM_ORDER = [s[0] for s in STRATA_DEF]      # §7 tie-break (3)

def make_lattice(master_seed, strata_names, r_inst=R_INST):
    rng = random.Random(master_seed)
    out = {}
    for name, gen, truthf in STRATA_DEF:
        insts = [gen(rng) for _ in range(r_inst)]     # draw ALL strata to keep
        if name in strata_names:                       # the rng stream stable
            out[name] = [(w, truthf(w)) for w in insts]
    return out

def fresh(w):
    return (GNonstationary(w.n1, w.n2, w.switch)
            if isinstance(w, GNonstationary) else w)

# ---------- helpers -----------------------------------------------------------

def classify(res, truth):
    if res[0] == 'VAL':
        _, v, conf = res
        if truth is not None and v == truth: return ('S', v)
        return ('WC', v) if conf else ('WD', v)
    if res[0] == 'AB':
        return ('S', 'AB') if truth is None else ('AB', None)
    return ('TO', None)

def m1(tx, ty):
    return int(tx[0] in ('WC', 'WD') and ty[0] in ('WC', 'WD') and tx[1] == ty[1])

def lcp_dist(a, b):
    n = min(len(a), len(b)); i = 0
    while i < n and a[i] == b[i]: i += 1
    return 1.0 - i / max(len(a), len(b), 1)

def pearson(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sx = sum((x - mx) ** 2 for x in xs) ** 0.5
    sy = sum((y - my) ** 2 for y in ys) ** 0.5
    if sx < 1e-12 or sy < 1e-12: return 0.0
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sx * sy)

def binom_ucb(k, n, alpha=ALPHA):
    """One-sided exact (Clopper-Pearson) upper bound via bisection."""
    if k >= n: return 1.0
    lo, hi = k / n, 1.0
    for _ in range(60):
        p = (lo + hi) / 2
        # P(X <= k | p)
        c, term = 0.0, (1 - p) ** n
        for i in range(0, k + 1):
            if i > 0: term *= (n - i + 1) / i * p / (1 - p)
            c += term
        if c > alpha: lo = p
        else: hi = p
    return hi

def binom_lcb(k, n, alpha=ALPHA):
    return 1.0 - binom_ucb(n - k, n, alpha)

# ---------- battery (AMENDMENT-1) ----------------------------------------------

def cert_battery(fn_x, fn_y, seed0=7):
    rng = random.Random(seed0)
    battery = ([GAliasCycle(n, q) for n, q in [(20, 5), (24, 6), (30, 6), (36, 9)]]
               + [GCycle(rng.randint(20, 36), eps=0.10) for _ in range(4)])
    wrong = 0
    for w in battery:
        for s in (101, 202, 303):
            rx, _ = run_language(fn_x, w, CAP, seed=s)
            ry, _ = run_language(fn_y, w, CAP, seed=s)
            vx = rx[1] if rx[0] == 'VAL' else None
            vy = ry[1] if ry[0] == 'VAL' else None
            if vx is not None and vx == vy and vx != w.truth: wrong += 1
    return wrong                        # eligible iff <= CERT_WRONG_MAX

# ---------- battery runner ------------------------------------------------------

def run_battery(langs, lattice, master_seed):
    keys = [(s, i) for s in lattice for i in range(len(lattice[s]))]
    tokens = {l: {} for l in langs}
    logs = {l: {} for l in langs}
    for s in lattice:
        for i, (w, truth) in enumerate(lattice[s]):
            for pi, (pn, bp, rev) in enumerate(PERTS):
                for r in range(K_SEEDS):
                    for lname, fn in langs.items():
                        res, log = run_language(fn, fresh(w), CAP,
                                                seed=10007 * r + SALT.get(lname, 999),
                                                bp=bp, rev=rev)
                        tokens[lname].setdefault((s, i), {})[(pi, r)] = classify(res, truth)
                        logs[lname].setdefault((s, i), {})[(pi, r)] = log
    return keys, tokens, logs

# ---------- channels (§4) --------------------------------------------------------

CELLS = [(pi, r) for pi in range(len(PERTS)) for r in range(K_SEEDS)]
EPAIRS = [(a, b) for a in range(len(PERTS)) for b in range(a + 1, len(PERTS))]

def fingerprints(logs, langs, keys):
    return {l: {k: {r: [lcp_dist(logs[l][k][(a, r)], logs[l][k][(b, r)])
                        for a, b in EPAIRS] for r in range(K_SEEDS)}
                for k in keys} for l in langs}

def sfrac(tokens, l, k):
    return sum(t[0] == 'S' for t in tokens[l][k].values()) / len(CELLS)

def vfail_cells(tokens, l, k):
    return sum(t[0] in ('WC', 'WD') for t in tokens[l][k].values())

def admission(tokens, fp, x, y, keys, theta):
    # token: world-sensitivity + informative support (§4.1)
    def sens(l):
        rng = random.Random(555)
        d = n = 0
        for _ in range(2000):
            k1, k2 = rng.choice(keys), rng.choice(keys)
            c = rng.choice(CELLS)
            if k1 != k2:
                d += tokens[l][k1][c] != tokens[l][k2][c]; n += 1
        return d / max(n, 1)
    ninf = sum(vfail_cells(tokens, x, k) >= 3 and vfail_cells(tokens, y, k) >= 3
               for k in keys)
    E_tok = sens(x) >= SENS_MIN and sens(y) >= SENS_MIN
    N_tok = ninf >= theta.get('Nmin', 4)
    # journal: schedule-adaptivity (§4.1; threshold from theta)
    def adapt(l):
        vals = [v for k in keys for r in range(K_SEEDS) for v in fp[l][k][r]]
        return (sum(vals) / len(vals)) if vals else 0.0
    thr = theta.get('adapt_min', 0.05)
    E_j = adapt(x) >= thr and adapt(y) >= thr
    return E_tok, N_tok, E_j, ninf

def token_channel(tokens, x, y, keys, theta):
    def stat(crossed):
        excs = []
        for k in keys:
            obs = 0
            for pi, r in CELLS:
                ry = (r + 1) % K_SEEDS if crossed else r
                obs += m1(tokens[x][k][(pi, r)], tokens[y][k][(pi, ry)])
            obs /= len(CELLS)
            cx = Counter(t for t in tokens[x][k].values() if t[0] in ('WC', 'WD'))
            cy = Counter(t for t in tokens[y][k].values() if t[0] in ('WC', 'WD'))
            tot = len(CELLS)
            e0 = sum((cx[t] / tot) * (cy[t2] / tot)
                     for t in cx for t2 in cy if t[1] == t2[1])
            excs.append(obs - e0)
        m = sum(excs) / len(excs)
        var = sum((e - m) ** 2 for e in excs) / max(len(excs) - 1, 1)
        return m, (var / len(excs)) ** 0.5
    k_mult = theta.get('k', 2.6)
    tm, ts = stat(False); tc, tcs = stat(True)
    flag = (tm > TOKEN_MARGIN and tm > k_mult * ts and
            tc > TOKEN_MARGIN and tc > k_mult * tcs)
    return flag, tm, tc

def j_fail_raw(tokens, fp, x, y, keys):
    fail = [k for k in keys if (1 - sfrac(tokens, x, k)) >= 0.5
            and (1 - sfrac(tokens, y, k)) >= 0.5]
    if len(fail) < 3: return None, len(fail), None
    def val(crossed):
        per = []
        for k in fail:
            cs = [pearson(fp[x][k][r], fp[y][k][(r + 1) % K_SEEDS if crossed else r])
                  for r in range(K_SEEDS)]
            per.append(sum(cs) / len(cs))
        return sum(per) / len(per)
    return val(False), len(fail), val(True)

def q75(vals):
    vals = sorted(vals)
    return vals[max(0, -(-3 * len(vals) // 4) - 1)]

def journal_channel(tokens, fp, x, y, keys, field_rp, mains):
    jm, nf, jc = j_fail_raw(tokens, fp, x, y, keys)
    if jm is None: return 'UNKNOWN', None, None, None
    vals = []
    for rp in field_rp:
        a, b = RP_POOL[rp]
        v, n2, _ = j_fail_raw(tokens, fp, a, b, keys)
        if v is not None: vals.append(v)
    if len(vals) < 3: return 'UNKNOWN_FIELD', jm, jc, None
    f = max(0.0, q75(vals))
    flag = (jm - f >= JOURNAL_MARGIN and jc - f >= JOURNAL_MARGIN)
    return ('DEPENDENT' if flag else 'CLEAN'), jm, jc, f

# ---------- verdict assembly (§4.4, §5) -------------------------------------------

def pair_verdict(tokens, fp, x, y, keys, theta):
    E_tok, N_tok, E_j, ninf = admission(tokens, fp, x, y, keys, theta)
    out = {'E_tok': E_tok, 'N_tok': N_tok, 'E_j': E_j, 'N_inf': ninf}
    if E_tok and N_tok:
        tf, tm, tc = token_channel(tokens, x, y, keys, theta)
        out['P_tok'] = 'DEPENDENT' if tf else 'CLEAN'
        out['tok_m'], out['tok_c'] = tm, tc
    else:
        out['P_tok'] = 'INADMISSIBLE'
    if E_j:
        rp = FIELD_ALLOC.get((x, y), FIELD_ALLOC.get((y, x)))
        if rp is None:
            out['P_j'] = 'UNKNOWN_FIELD'
        else:
            pj, jm, jc, f = journal_channel(tokens, fp, x, y, keys, rp, MAINS)
            out['P_j'] = pj; out['J_m'], out['J_c'], out['field'] = jm, jc, f
    else:
        out['P_j'] = 'INADMISSIBLE'
    # P_union collapse (§4.4, after per-channel E-gates)
    adm = [out[c] for c in ('P_tok', 'P_j') if out[c] not in
           ('INADMISSIBLE', 'UNKNOWN', 'UNKNOWN_FIELD')]
    if any(v == 'DEPENDENT' for v in adm): out['P_union'] = 'DEPENDENT'
    elif adm and all(v == 'CLEAN' for v in adm): out['P_union'] = 'CLEAN'
    else: out['P_union'] = 'NO_TEST'
    return out

# ---------- OC (§7): window selection with frozen tie-break -----------------------

def clone_wrap(base, salt):
    def fn(oracle, cap, seed):
        rng = random.Random(seed * 13 + salt)
        def orc(u, v):
            if rng.random() < 0.3:
                j = rng.randint(1, 5); oracle('L' * j, 'R' * j)
            return oracle(u, v)
        return base(orc, cap, seed)
    return fn

def derive_wrap(base, salt):
    def fn(oracle, cap, seed):
        rng = random.Random(seed * 17 + salt)
        def orc(u, v):
            j = rng.randint(1, 3)
            return oracle(u + 'R' * j, v + 'R' * j)
        return base(orc, cap, seed)
    return fn

# frozen candidate windows (§7; evaluated by restriction of ONE full
# lattice battery per simulation — statistically identical, 6x cheaper)
CANDIDATES = [['noisy'], ['noisy', 'qtrap'], ['noisy', 'qtrap', 'alias'],
              ['cycle', 'alias', 'noisy', 'qtrap'],
              ['cycle', 'alias', 'noisy', 'qtrap', 'wobble'],
              ['cycle', 'alias', 'noisy', 'qtrap', 'wobble', 'lollipop', 'nonstat']]

def oc_run(sim_seed, theta):
    """One full-run simulation at the PRIMARY scale (r_inst = R_INST);
    every candidate window is evaluated on the stratum-restricted keys."""
    bases = {'A': MAINS['A'], 'gptA': MAINS['gptA'], 'opusA': MAINS['opusA'],
             'gem': MAINS['gem'], 'grok': MAINS['grok'], 'gptB': MAINS['gptB']}
    langs = dict(bases)
    for b in ('A', 'gptA', 'gem'):
        langs['c.' + b] = clone_wrap(bases[b], 7)
        langs['d.' + b] = derive_wrap(bases[b], 3)
        SALT.setdefault('c.' + b, 601); SALT.setdefault('d.' + b, 631)
    lattice = make_lattice(sim_seed, STRATUM_ORDER, r_inst=R_INST)
    keys, tokens, logs = run_battery(langs, lattice, sim_seed)
    fp = fingerprints(logs, langs, keys)
    out = {}
    for wnd in CANDIDATES:
        wkeys = [k for k in keys if k[0] in wnd]
        res = {'derived': [], 'clone': [], 'indep': []}
        for b in ('A', 'gptA', 'gem'):
            res['derived'].append(pair_verdict(tokens, fp, b, 'd.' + b, wkeys, theta)['P_union'])
            res['clone'].append(pair_verdict(tokens, fp, b, 'c.' + b, wkeys, theta)['P_union'])
        for x, y in [('gptA', 'grok'), ('gptB', 'gem'), ('gptA', 'gptB')]:
            res['indep'].append(pair_verdict(tokens, fp, x, y, wkeys, theta)['P_union'])
        out['+'.join(wnd)] = res
    return out

def oc_tune(n_mc=N_MC_TUNE, out='oc_tune_results.json'):
    theta0 = {'k': 2.6, 'Nmin': 4, 'adapt_min': 0.05}
    acc = {'+'.join(w): {'derived': 0, 'derived_n': 0, 'fp': 0, 'fp_n': 0}
           for w in CANDIDATES}
    for s in range(n_mc):
        r = oc_run(31000 + 977 * s, theta0)
        for wname, res in r.items():
            h = acc[wname]
            for v in res['derived']:
                if v != 'NO_TEST':
                    h['derived_n'] += 1; h['derived'] += v == 'DEPENDENT'
            for v in res['indep']:
                if v != 'NO_TEST':
                    h['fp_n'] += 1; h['fp'] += v == 'DEPENDENT'
        if (s + 1) % 10 == 0:
            print(json.dumps({'sims_done': s + 1, 'acc': acc}), flush=True)
    results = {}
    for wname, h in acc.items():
        p_lcb = binom_lcb(h['derived'], max(h['derived_n'], 1))
        f_ucb = binom_ucb(h['fp'], max(h['fp_n'], 1))
        results[wname] = {'power_lcb': p_lcb, 'fpr_ucb': f_ucb, 'raw': h,
                          'qualifies': p_lcb >= POWER_MIN and f_ucb <= ALPHA}
        print(json.dumps({'window': wname, **results[wname]}), flush=True)
    with open(os.path.join(HERE, out), 'w') as fh:
        json.dump(results, fh, indent=1)
    print('OC-tune complete ->', out)

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'tune'
    if mode == 'tune':
        n = int(sys.argv[2]) if len(sys.argv) > 2 else N_MC_TUNE
        oc_tune(n_mc=n)
