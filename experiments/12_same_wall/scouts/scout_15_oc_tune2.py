"""
SCOUT 15 (OC-TUNE-2, NOT citable): the full pipeline on the synthetic
bank — field-calibrated blade + informative-support admission (N-gate) +
context-seeded PM. Fixes scout 14's three diagnoses.

Changes (each addressing a recorded fall):
  1. BLADE WITH FIELD: J_fail flag requires J_fail - field_fail >= 0.10,
     where field_fail = max(0, q75) of J_fail over external reference
     pairs (leave-candidate-family-out, 6-pair minimum verified), each
     computed on ITS OWN failure-class instances.
  2. N-GATE (informative support, review Y §4.2 + scout 14 diagnosis 1):
     a pair is token-admissible iff N_informative >= 4 instances where
     BOTH members produce >= 3 value-failure (WC/WD) cells; blade needs
     n_fail >= 3 as before. Quiet failers -> INADMISSIBLE(N), excluded
     from FPR/power, reported separately: the applicability domain
     working as designed, not an error.
  3. PM VALUE CONTEXT-SEEDED: the corrupted value mixes in the wrapped
     oracle's call count, so it varies across perturbations (kills the
     pert-invariant pseudo-replication).

Preregistered expectations:
  E1 PM pair -> CLEAN (artifact gone).
  E2 (W,cW), (M,cM) quiet-failer clones -> INADMISSIBLE(N).
  E3 power on ADMISSIBLE derived pairs >= 0.8 in some window.
  E4 FPR on admissible independents = 0 (field absorbs wobble's
     world-common response).
  E5 the frozen window rule yields a NON-EMPTY window over admissible
     pairs. If still empty -> the rule itself is under-resolved at
     scout n; recorded, and the locked OC needs bigger n, not new knobs.
"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', 'experiment_A'))
from worlds_general import run_language, GNonstationary
from scout_11_two_genealogies import classify, m1, lcp_dist, pearson
import scout_14_oc_tune as s14

R_INST = s14.R_INST
K_SEEDS = s14.K_SEEDS
CAP = s14.CAP
PERTS = s14.PERTS
N_INFORMATIVE_MIN = 4
VALUE_CELLS_MIN = 3

def make_pm_v2(base_fn, salt):
    def fn(oracle, cap, seed):
        rng = random.Random(seed * 31 + salt)
        calls = {'n': 0}
        def orc(u, v):
            calls['n'] += 1
            return oracle(u, v)
        res = base_fn(orc, cap, seed)
        if rng.random() < s14.PM_PROFILE[s14._stratum['name']]:
            vrng = random.Random(seed * 31 + salt + 7919 * calls['n'])
            return ('VAL', vrng.randint(1, 15), True)
        return res
    return fn

LANGS = dict(s14.LANGS)
LANGS['PM1'] = make_pm_v2(s14.BASES['W'], 5)
LANGS['PM2'] = make_pm_v2(s14.BASES['M'], 9)
SALT = dict(s14.SALT)
FAMILY = {}
for b in s14.BASES:
    for pref in ('', 'c', 'd'): FAMILY[pref + b] = b
FAMILY['PM1'] = 'PM1'; FAMILY['PM2'] = 'PM2'
REF_UNITS = list(s14.BASES)          # A, W, M, P, oA — family representatives

def main():
    master = random.Random(20260714)          # same TUNE bank seed as scout 14
    lattice = s14.make_lattice(master)
    keys = [(s, i) for s in lattice for i in range(R_INST)]
    epairs = [(a, b) for a in range(len(PERTS)) for b in range(a + 1, len(PERTS))]
    tokens = {l: {k: {} for k in keys} for l in LANGS}
    logs = {l: {k: {} for k in keys} for l in LANGS}
    for sname, insts in lattice.items():
        s14._stratum['name'] = sname
        for i, w in enumerate(insts):
            tr = s14.truth_of(w, sname)
            for pi, (pn, bp, rev) in enumerate(PERTS):
                for r in range(K_SEEDS):
                    for lname, fn in LANGS.items():
                        res, log = run_language(fn, s14.fresh(w), CAP,
                                                seed=10007 * r + SALT[lname],
                                                bp=bp, rev=rev)
                        tokens[lname][(sname, i)][(pi, r)] = classify(res, tr)
                        logs[lname][(sname, i)][(pi, r)] = log

    from collections import Counter
    cells = [(pi, r) for pi in range(len(PERTS)) for r in range(K_SEEDS)]
    fp = {l: {k: {r: [lcp_dist(logs[l][k][(a, r)], logs[l][k][(b, r)])
                      for a, b in epairs] for r in range(K_SEEDS)}
              for k in keys} for l in LANGS}

    def vfail_cells(l, k):
        return sum(t[0] in ('WC', 'WD') for t in tokens[l][k].values())

    def sfrac(l, k):
        return sum(t[0] == 'S' for t in tokens[l][k].values()) / len(cells)

    def n_informative(x, y, subset):
        return sum(vfail_cells(x, k) >= VALUE_CELLS_MIN
                   and vfail_cells(y, k) >= VALUE_CELLS_MIN for k in subset)

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

    def j_fail_raw(x, y, subset):
        fail = [k for k in subset if (1 - sfrac(x, k)) >= 0.5
                and (1 - sfrac(y, k)) >= 0.5]
        if len(fail) < 3: return None, len(fail)
        per = []
        for k in fail:
            cs = [pearson(fp[x][k][r], fp[y][k][r]) for r in range(K_SEEDS)]
            per.append(sum(cs) / len(cs))
        return sum(per) / len(per), len(fail)

    def q75(vals):
        vals = sorted(vals)
        return vals[max(0, -(-3 * len(vals) // 4) - 1)]

    def field_fail(x, y, subset):
        fx, fy = FAMILY[x], FAMILY[y]
        ext = [u for u in REF_UNITS if u not in (fx, fy)]
        prs = [(a, b) for ai, a in enumerate(ext) for b in ext[ai + 1:]]
        vals = []
        for a, b in prs:
            jf, nf = j_fail_raw(a, b, subset)
            if jf is not None: vals.append(jf)
        if len(vals) < 3: return None
        return max(0.0, q75(vals))

    def verdict(x, y, subset):
        ninf = n_informative(x, y, subset)
        tok_adm = ninf >= N_INFORMATIVE_MIN
        tm, ts = token_exc(x, y, subset)
        tok = tok_adm and tm > 0.05 and tm > 2 * ts
        jf, nf = j_fail_raw(x, y, subset)
        ff = field_fail(x, y, subset)
        blade = (jf is not None and ff is not None and jf - ff >= 0.10)
        if not tok_adm and jf is None:
            return 'INADMISSIBLE(N)', tm, jf, ff, ninf
        return ('FLAG' if (tok or blade) else 'CLEAN'), tm, jf, ff, ninf

    strata = list(lattice)
    print("per-stratum, admissible pairs only:")
    window = []
    for s in strata:
        sub = [(s, i) for i in range(R_INST)]
        d_adm = d_hit = 0
        for x, y in s14.DERIVED_PAIRS:
            v, *_ = verdict(x, y, sub)
            if v != 'INADMISSIBLE(N)': d_adm += 1; d_hit += v == 'FLAG'
        n_adm = n_hit = 0
        for x, y in s14.INDEP_PAIRS + [('PM1', 'PM2')]:
            v, *_ = verdict(x, y, sub)
            if v != 'INADMISSIBLE(N)': n_adm += 1; n_hit += v == 'FLAG'
        power = d_hit / d_adm if d_adm else float('nan')
        fpr = n_hit / n_adm if n_adm else float('nan')
        q = d_adm >= 2 and power >= 0.8 and fpr == 0.0
        if q: window.append(s)
        print(f"  {s:<8} derived {d_hit}/{d_adm}  negatives {n_hit}/{n_adm}"
              f"  {'-> IN WINDOW' if q else ''}")
    print(f"\nfrozen-rule window: {window}")

    wsub = ([(s, i) for s in window for i in range(R_INST)]
            if window else keys)
    print(f"\nfull-battery verdicts ON {'WINDOW' if window else 'ALL'}:")
    for label, plist in [('clone', s14.CLONE_PAIRS),
                         ('derived', s14.DERIVED_PAIRS),
                         ('indep', s14.INDEP_PAIRS),
                         ('PM', [('PM1', 'PM2')])]:
        out = []
        for x, y in plist:
            v, tm, jf, ff, ninf = verdict(x, y, wsub)
            jfs = f"{jf:.2f}" if jf is not None else ' — '
            ffs = f"{ff:.2f}" if ff is not None else ' — '
            out.append(f"({x},{y}):{v} tok={tm:+.3f} Jf={jfs} fld={ffs} N={ninf}")
        print(f"  {label}:")
        for o in out: print(f"    {o}")

if __name__ == '__main__':
    main()
