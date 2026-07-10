"""
SCOUT 14 (OC-TUNE, NOT citable): operating characteristics of the v4
verdict rule on a synthetic bank of KNOWN-status pairs, and the frozen
window-selection procedure (review Y §4.3 / review X §2).

Bank (5 bases — deliberately diverse, NOT only A-like; Y's kill):
  bases    : A (origin scan), W (adjacent walker), M (bisection),
             P (pair sampler), oA (opus-A main, clean-room).
  clones   : base + ignored padding probes (same effective channel), x5.
  derived  : base behind a translated oracle (every probe (u,v) ->
             (u+R^j, v+R^j), own rng) — the registered derivation type, x5.
  indep    : all cross-base pairs, x10.
  PM       : two marginal-matched wrappers over independent bases, x1 pair.

Verdict rule under test (v4 draft, scout-level simplification recorded:
fixed J_fail threshold 0.5 in place of the full field machinery; the
locked OC-validate must run the full pipeline):
  FLAG iff token(exc > 0.05 AND > 2se)
       OR (J_fail >= 0.5 AND n_fail >= 3)   [the blade]

Estimands (preregistered):
  E1 POWER on derived class >= 0.8 inside some window; FPR on
     indep+PM = 0 at scout scale (any false flag is a finding).
  E2 RESOLUTION: clone-class vs derived-class effect sizes, token and
     blade separately (phase-0 token resolution was poor: 0.5 vs 0.053;
     the blade's was near 1: 0.60 vs 0.53 — expect the blade to carry).
  E3 WINDOW RULE (frozen procedure): a stress stratum qualifies iff
     derived-power(stratum) >= 0.8 AND FPR(stratum) = 0; the window is
     the set of qualifying strata; K2 pairs play no role in selection
     (they are not in this bank at all — by construction).
  E4 POWER PER BASE: derived detection is CLAIMED only for
     deterministic-schedule bases; stochastic bases (P) are
     preregistered HARD (independent runtime seeds decorrelate a real
     derived pair — the H-theorem/visibility limit, declared, not a
     bank defect). If power collapses on deterministic non-scan bases
     (W, M) — the derived class was A-biased and v4 must say so.
Lattice (fixed): cycle, alias, noisy(.06), noisy(.12), noisy(.20),
qtrap(.6), wobble, nonstat. R_INST=3, K_SEEDS=3, CAP=400.
"""
import sys, os, random, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', 'experiment_A'))
from worlds_general import (GCycle, GAliasCycle, GWobble, GNonstationary,
                            run_language, lang_A_general)
from scout_11_two_genealogies import (lang_P_str, lang_W_str, lang_M_str,
                                      classify, m1, lcp_dist, pearson)
from scout_12_stress_strata import QuotientTrap

def _load(name, fname):
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     '..', 'experiment_A', 'received', fname)
    spec = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m

opusA = _load('opusA', 'find_order.py')

R_INST = 3
K_SEEDS = 3
CAP = 400
PERTS = [('id', 0, False), ('bp+1', 1, False), ('bp+3', 3, False),
         ('rev', 0, True), ('nseed', 0, False)]

BASES = {'A': lang_A_general, 'W': lang_W_str, 'M': lang_M_str,
         'P': lang_P_str, 'oA': opusA.find_order_main}

def make_clone(base_fn, salt):
    def fn(oracle, cap, seed):
        rng = random.Random(seed * 13 + salt)
        calls = {'n': 0}
        def orc(u, v):
            if rng.random() < 0.3 and calls['n'] < 40:
                calls['n'] += 1
                j = rng.randint(1, 5); oracle('L' * j, 'R' * j)  # ignored
            return oracle(u, v)
        return base_fn(orc, cap, seed)
    return fn

def make_derived(base_fn, salt):
    def fn(oracle, cap, seed):
        rng = random.Random(seed * 17 + salt)
        def orc(u, v):
            j = rng.randint(1, 3)
            return oracle(u + 'R' * j, v + 'R' * j)
        return base_fn(orc, cap, seed)
    return fn

PM_PROFILE = {'noisy06': 0.5, 'noisy12': 0.9, 'noisy20': 0.9, 'qtrap': 0.9,
              'wobble': 1.0, 'cycle': 0.05, 'alias': 0.6, 'nonstat': 0.9}
_stratum = {'name': 'cycle'}

def make_pm(base_fn, salt):
    def fn(oracle, cap, seed):
        rng = random.Random(seed * 31 + salt)
        res = base_fn(oracle, cap, seed)
        if rng.random() < PM_PROFILE[_stratum['name']]:
            return ('VAL', rng.randint(1, 15), True)
        return res
    return fn

LANGS = {}
SALT = {}
for i, (b, fn) in enumerate(BASES.items()):
    LANGS[b] = fn;                     SALT[b] = 11 + 97 * i
    LANGS['c' + b] = make_clone(fn, 7 + i);   SALT['c' + b] = 41 + 97 * i
    LANGS['d' + b] = make_derived(fn, 3 + i); SALT['d' + b] = 71 + 97 * i
LANGS['PM1'] = make_pm(lang_W_str, 5); SALT['PM1'] = 901
LANGS['PM2'] = make_pm(lang_M_str, 9); SALT['PM2'] = 923

CLONE_PAIRS = [(b, 'c' + b) for b in BASES]
DERIVED_PAIRS = [(b, 'd' + b) for b in BASES]
BN = list(BASES)
INDEP_PAIRS = [(BN[i], BN[j]) for i in range(len(BN)) for j in range(i + 1, len(BN))]
PM_PAIRS = [('PM1', 'PM2')]

def make_lattice(rng):
    def qt():
        q = rng.randint(5, 9)
        return QuotientTrap(q * rng.randint(3, 5), q, rng)
    return {'cycle':   [GCycle(rng.randint(17, 40)) for _ in range(R_INST)],
            'alias':   [GAliasCycle(n, q) for n, q in
                        [(lambda n: (n, rng.choice([d for d in range(4, n // 2 + 1)
                                                    if n % d == 0])))(
                             rng.choice([20, 24, 30, 36]))
                         for _ in range(R_INST)]],
            'noisy06': [GCycle(rng.randint(17, 40), eps=0.06) for _ in range(R_INST)],
            'noisy12': [GCycle(rng.randint(17, 40), eps=0.12) for _ in range(R_INST)],
            'noisy20': [GCycle(rng.randint(17, 40), eps=0.20) for _ in range(R_INST)],
            'qtrap':   [qt() for _ in range(R_INST)],
            'wobble':  [GWobble(rng.randint(17, 40)) for _ in range(R_INST)],
            'nonstat': [GNonstationary(rng.randint(15, 26), rng.randint(27, 40),
                                       rng.randint(60, 200)) for _ in range(R_INST)]}

def truth_of(w, sname):
    return None if sname in ('wobble', 'nonstat') else w.truth

def fresh(w):
    return (GNonstationary(w.n1, w.n2, w.switch)
            if isinstance(w, GNonstationary) else w)

def main():
    master = random.Random(20260714)          # TUNE bank seed
    lattice = make_lattice(master)
    keys = [(s, i) for s in lattice for i in range(R_INST)]
    epairs = [(a, b) for a in range(len(PERTS)) for b in range(a + 1, len(PERTS))]
    tokens = {l: {k: {} for k in keys} for l in LANGS}
    logs = {l: {k: {} for k in keys} for l in LANGS}
    for sname, insts in lattice.items():
        _stratum['name'] = sname
        for i, w in enumerate(insts):
            tr = truth_of(w, sname)
            for pi, (pn, bp, rev) in enumerate(PERTS):
                for r in range(K_SEEDS):
                    for lname, fn in LANGS.items():
                        res, log = run_language(fn, fresh(w), CAP,
                                                seed=10007 * r + SALT[lname],
                                                bp=bp, rev=rev)
                        tokens[lname][(sname, i)][(pi, r)] = classify(res, tr)
                        logs[lname][(sname, i)][(pi, r)] = log

    from collections import Counter
    cells = [(pi, r) for pi in range(len(PERTS)) for r in range(K_SEEDS)]
    fp = {l: {k: {r: [lcp_dist(logs[l][k][(a, r)], logs[l][k][(b, r)])
                      for a, b in epairs] for r in range(K_SEEDS)}
              for k in keys} for l in LANGS}

    def sfrac(l, k):
        return sum(t[0] == 'S' for t in tokens[l][k].values()) / len(cells)

    def token_exc(x, y, subset):
        excs = []
        for k in subset:
            obs = sum(m1(tokens[x][k][c], tokens[y][k][c]) for c in cells) / len(cells)
            cx = Counter(t for t in tokens[x][k].values() if t[0] in ('WC', 'WD'))
            cy = Counter(t for t in tokens[y][k].values() if t[0] in ('WC', 'WD'))
            tot = len(cells)
            e0 = sum((cx[t] / tot) * (cy[t2] / tot)
                     for t in cx for t2 in cy if t[1] == t2[1])
            excs.append(obs - e0)
        m = sum(excs) / len(excs)
        var = sum((e - m) ** 2 for e in excs) / max(len(excs) - 1, 1)
        return m, (var / max(len(excs), 1)) ** 0.5

    def j_fail(x, y, subset):
        fail = [k for k in subset if (1 - sfrac(x, k)) >= 0.5
                and (1 - sfrac(y, k)) >= 0.5]
        if len(fail) < 3: return None, len(fail)
        per = []
        for k in fail:
            cs = [pearson(fp[x][k][r], fp[y][k][r]) for r in range(K_SEEDS)]
            per.append(sum(cs) / len(cs))
        return sum(per) / len(per), len(fail)

    def flag(x, y, subset):
        tm, ts = token_exc(x, y, subset)
        jf, nf = j_fail(x, y, subset)
        tok = tm > 0.05 and tm > 2 * ts
        blade = jf is not None and jf >= 0.5
        return tok or blade, tm, jf

    # per-stratum table for the window rule
    strata = list(lattice)
    print("per-stratum derived-power and FPR (indep+PM), with blade J_fail:")
    window = []
    for s in strata:
        sub = [(s, i) for i in range(R_INST)]
        p_hits = sum(flag(x, y, sub)[0] for x, y in DERIVED_PAIRS)
        f_hits = sum(flag(x, y, sub)[0] for x, y in INDEP_PAIRS + PM_PAIRS)
        power = p_hits / len(DERIVED_PAIRS)
        fpr = f_hits / (len(INDEP_PAIRS) + len(PM_PAIRS))
        q = power >= 0.8 and fpr == 0.0
        if q: window.append(s)
        print(f"  {s:<8} power={power:.2f} ({p_hits}/{len(DERIVED_PAIRS)})  "
              f"FPR={fpr:.2f} ({f_hits}/{len(INDEP_PAIRS)+len(PM_PAIRS)})  "
              f"{'-> IN WINDOW' if q else ''}")
    print(f"\nfrozen-rule window: {window}")

    wsub = [(s, i) for s in window for i in range(R_INST)] or keys
    print("\nclass summary ON WINDOW (token exc | blade J_fail | flagged):")
    for label, plist in [('clone', CLONE_PAIRS), ('derived', DERIVED_PAIRS),
                         ('indep', INDEP_PAIRS), ('PM', PM_PAIRS)]:
        rows = []
        for x, y in plist:
            f, tm, jf = flag(x, y, wsub)
            rows.append((x, y, tm, jf, f))
        hits = sum(r[4] for r in rows)
        print(f"  {label:<8} flagged {hits}/{len(rows)}")
        for x, y, tm, jf, f in rows:
            jfs = f"{jf:.2f}" if jf is not None else '  — '
            print(f"      ({x},{y}): tok={tm:+.3f} J_fail={jfs} "
                  f"{'FLAG' if f else ''}")

    # resolution factor (E2)
    def cls_effect(plist, which):
        vals = []
        for x, y in plist:
            _, tm, jf = flag(x, y, wsub)
            vals.append(tm if which == 'tok' else (jf if jf is not None else 0.0))
        return sum(vals) / len(vals)
    for ch in ('tok', 'blade'):
        c = cls_effect(CLONE_PAIRS, 'tok' if ch == 'tok' else 'b')
        d = cls_effect(DERIVED_PAIRS, 'tok' if ch == 'tok' else 'b')
        i = cls_effect(INDEP_PAIRS, 'tok' if ch == 'tok' else 'b')
        print(f"\nE2 {ch}: clone={c:.3f} derived={d:.3f} indep={i:.3f} "
              f"resolution(derived-indep gap)={d - i:.3f}")

if __name__ == '__main__':
    main()
