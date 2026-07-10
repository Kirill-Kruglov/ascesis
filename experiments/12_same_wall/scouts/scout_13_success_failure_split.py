"""
SCOUT 13 (phase 0 extension, NOT citable): the success/failure split
(review X's blade) against THREE genealogies + the split's own validity
gate + the performance-matched control (review Y) + the 6-unit reference
bank (formal-bug fix verified by construction).

The blade: co-adaptation that survives into CORRELATED FAILURE is
ancestry; co-adaptation living only in success is the world's one door.
Operational form (fixed): per pair, classify world instances into
SUCC-class (both members' S-token fraction >= 0.5) and FAIL-class (both
non-S fraction >= 0.5; mixed excluded); compute journal co-adaptation J
separately on each class; the token channel (M1) is inherently
failure-borne and is computed as before.

Split verdict (scout thresholds, OC will calibrate):
  ANCESTRY    iff J_fail >= 0.5 with n_fail >= 3 instances
  WORLD_DOOR  iff J_succ >= 0.5 and (J_fail < 0.25 or n_fail < 3)
  NO_SIGNAL   otherwise

Preregistered expectations (before running):
  E1 VALIDITY GATE: clone (A,A') retains co-adaptation through the
     transition (J_fail comparable to J_succ, ANCESTRY). If the clone
     loses it, the split is NOT a discriminator and falls with a record
     (review X's own kill condition).
  E2 (A, Gt) derived: token flags; ANCESTRY.
  E3 (A, opus-A) common-prior: EXPECTED to read like ancestry too
     (24/24 co-wrong at first contact) — the blade cuts
     construction-vs-world, NOT provenance-within-construction; derived
     vs common-prior separation belongs to the C8 factorial. Registered
     limitation, not a failure.
  E4 (A, gpt-A) independent (cross-prior): token clean; J_fail ~ 0; any
     J signal confined to success classes (deterministic-strata
     competence convergence) -> WORLD_DOOR or NO_SIGNAL. This is X's
     original worry made into a measurement.
  E5 (gptA-main, gptA-ref1) shared helpers: expected still invisible
     (H-theorem: decorrelated falls) — the declared blind spot persists.
  E6 performance-matched pair (PM1, PM2): wrappers over two INDEPENDENT
     bases (gptB-main, gptA-ref2), each corrupting its output to the
     registered marginal error profile of the (A,Gt) class with its OWN
     rng. Must be CLEAN / NO_SIGNAL on all channels. KILL if it flags:
     the channels would be reading marginals, not coupling.
  E7 reference bank: 6 provenance units {W, M, P, gptA-fam, gptB-fam,
     opusA-fam}; for every gating pair (incl. C2 pairs (W,P), (M,P))
     leave-family-out must leave >= 3 external pairs — the v3 formal bug
     fixed by construction; the scout PRINTS the check.
"""
import sys, os, random, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', 'experiment_A'))
from worlds_general import (GCycle, GAliasCycle, GWobble, GNonstationary,
                            run_language, lang_A_general, lang_G_translated)
from scout_11_two_genealogies import (lang_P_str, lang_W_str, lang_M_str,
                                      classify, m1, lcp_dist, pearson)
from scout_12_stress_strata import QuotientTrap

def _load(name, fname):
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     '..', 'experiment_A', 'received', fname)
    spec = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m

gptA = _load('gptA', 'find_order_solvers.py')
gptB = _load('gptB', 'find_order_spec_encoding_b.py')
opusA = _load('opusA', 'find_order.py')

R_INST = 4
K_SEEDS = 4
CAP = 400
PERTS = [('id', 0, False), ('bp+1', 1, False), ('bp+3', 3, False),
         ('rev', 0, True), ('nseed', 0, False)]

# performance-matched wrappers: registered marginal error profile of the
# (A,Gt) class; each wrapper has its OWN rng and an INDEPENDENT base
PM_PROFILE = {'noisy': 0.9, 'qtrap': 0.9, 'wobble': 1.0,
              'cycle': 0.05, 'alias': 0.6, 'nonstat': 0.9}
_current_stratum = {'name': 'cycle'}          # set by the runner loop

def _pm_wrap(base_fn, salt):
    def fn(oracle, cap_calls, seed):
        rng = random.Random(seed * 31 + salt)
        res = base_fn(oracle, cap_calls, seed)
        if rng.random() < PM_PROFILE[_current_stratum['name']]:
            return ('VAL', rng.randint(1, 15), True)
        return res
    return fn

LANGS = {'A': lang_A_general,
         "A'": lambda o, c, s: lang_A_general(o, c, s),   # clone (identical)
         'Gt': lang_G_translated,
         'gA': gptA.find_order_main, 'gA1': gptA.find_order_ref1,
         'gB': gptB.find_order_main, 'oA': opusA.find_order_main,
         'W': lang_W_str, 'M': lang_M_str, 'P': lang_P_str,
         'PM1': _pm_wrap(gptB.find_order_main, 7),
         'PM2': _pm_wrap(gptA.find_order_ref2, 13)}
SALT = {'A': 11, "A'": 23, 'Gt': 29, 'gA': 501, 'gA1': 523, 'gB': 601,
        'oA': 701, 'W': 311, 'M': 331, 'P': 51, 'PM1': 801, 'PM2': 823}
FAMILY = {'gA': 'gptA', 'gA1': 'gptA', 'gB': 'gptB', 'oA': 'opusA',
          'W': 'W', 'M': 'M', 'P': 'P'}
REF_UNITS = ['W', 'M', 'P', 'gptA', 'gptB', 'opusA']

def make_strata(rng):
    def qt():
        q = rng.randint(5, 9)
        return QuotientTrap(q * rng.randint(3, 5), q, rng)
    return {'cycle':   [GCycle(rng.randint(17, 40)) for _ in range(R_INST)],
            'alias':   [GAliasCycle(n, q) for n, q in
                        [(lambda n: (n, rng.choice([d for d in range(4, n // 2 + 1)
                                                    if n % d == 0])))(
                             rng.choice([20, 24, 30, 36]))
                         for _ in range(R_INST)]],
            'noisy':   [GCycle(rng.randint(17, 40), eps=rng.uniform(0.05, 0.12))
                        for _ in range(R_INST)],
            'qtrap':   [qt() for _ in range(R_INST)],
            'wobble':  [GWobble(rng.randint(17, 40)) for _ in range(R_INST)],
            'nonstat': [GNonstationary(rng.randint(15, 26), rng.randint(27, 40),
                                       rng.randint(60, 200))
                        for _ in range(R_INST)]}

def truth_of(w, sname):
    return None if sname in ('wobble', 'nonstat') else w.truth

def fresh(w):
    if isinstance(w, GNonstationary):
        return GNonstationary(w.n1, w.n2, w.switch)
    return w

def main():
    master = random.Random(20260713)
    strata = make_strata(master)
    keys = [(s, i) for s in strata for i in range(R_INST)]
    epairs = [(a, b) for a in range(len(PERTS)) for b in range(a + 1, len(PERTS))]
    tokens = {l: {k: {} for k in keys} for l in LANGS}
    logs = {l: {k: {} for k in keys} for l in LANGS}

    for sname, insts in strata.items():
        _current_stratum['name'] = sname
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

    def token_exc(x, y):
        excs = []
        for k in keys:
            obs = sum(m1(tokens[x][k][c], tokens[y][k][c]) for c in cells) / len(cells)
            cx = Counter(t for t in tokens[x][k].values() if t[0] in ('WC', 'WD'))
            cy = Counter(t for t in tokens[y][k].values() if t[0] in ('WC', 'WD'))
            tot = len(cells)
            e0 = sum((cx[t] / tot) * (cy[t2] / tot)
                     for t in cx for t2 in cy if t[1] == t2[1])
            excs.append(obs - e0)
        m = sum(excs) / len(excs)
        var = sum((e - m) ** 2 for e in excs) / max(len(excs) - 1, 1)
        return m, (var / len(excs)) ** 0.5

    fp = {l: {k: {r: [lcp_dist(logs[l][k][(a, r)], logs[l][k][(b, r)])
                      for a, b in epairs] for r in range(K_SEEDS)}
              for k in keys} for l in LANGS}

    def sfrac(l, k):
        return sum(t[0] == 'S' for t in tokens[l][k].values()) / len(cells)

    def J_on(x, y, subset):
        if not subset: return None
        per = []
        for k in subset:
            cs = [pearson(fp[x][k][r], fp[y][k][r]) for r in range(K_SEEDS)]
            per.append(sum(cs) / len(cs))
        return sum(per) / len(per)

    def split(x, y):
        succ = [k for k in keys if sfrac(x, k) >= 0.5 and sfrac(y, k) >= 0.5]
        fail = [k for k in keys if (1 - sfrac(x, k)) >= 0.5
                and (1 - sfrac(y, k)) >= 0.5]
        js, jf = J_on(x, y, succ), J_on(x, y, fail)
        if jf is not None and jf >= 0.5 and len(fail) >= 3: v = 'ANCESTRY'
        elif js is not None and js >= 0.5 and (jf is None or jf < 0.25
                                               or len(fail) < 3):
            v = 'WORLD_DOOR'
        else: v = 'NO_SIGNAL'
        return js, jf, len(succ), len(fail), v

    pairs = [("A", "A'", 'clone (validity gate)'),
             ('A', 'Gt', 'derived'),
             ('A', 'oA', 'common-prior'),
             ('A', 'gA', 'independent x-prior'),
             ('gA', 'gA1', 'shared helpers'),
             ('PM1', 'PM2', 'performance-matched'),
             ('gA', 'gB', 'same prior, diff encoding'),
             ('oA', 'gA', 'x-prior, same encoding')]
    print(f"{'pair':<10} {'type':<26} {'tok_exc':>8} {'se':>6} | "
          f"{'J_succ':>6} {'J_fail':>6} {'nS':>3} {'nF':>3} | split")
    print('-' * 92)
    for x, y, typ in pairs:
        tm, ts = token_exc(x, y)
        js, jf, ns, nf, v = split(x, y)
        jss = f"{js:.2f}" if js is not None else '  — '
        jfs = f"{jf:.2f}" if jf is not None else '  — '
        print(f"({x},{y})".ljust(10) + f"{typ:<26} {tm:>8.3f} {ts:>6.3f} | "
              f"{jss:>6} {jfs:>6} {ns:>3} {nf:>3} | {v}")

    # E7: mechanical reference-bank check (the v3 formal-bug fix)
    print("\nE7 reference-bank check (external pairs after leave-family-out):")
    for x, y in [('W', 'P'), ('M', 'P'), ('A', 'gA'), ('A', 'oA'), ('gA', 'gA1')]:
        fx, fy = FAMILY.get(x, x), FAMILY.get(y, y)
        ext = [u for u in REF_UNITS if u not in (fx, fy)]
        npairs = len(ext) * (len(ext) - 1) // 2
        print(f"  ({x},{y}): external units={len(ext)} pairs={npairs} "
              f"{'OK' if npairs >= 3 else 'FAIL'}")

if __name__ == '__main__':
    main()
