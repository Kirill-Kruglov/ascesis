"""
SCOUT 11 (phase 0, NOT citable): the two-genealogy experiment — the
redesigned core of Experiment A, run at scout scale.

Question (from the two-review redesign): does v3 distinguish two
GENEALOGIES of the same theorem-glued destination?
  - (A, Gt)   : A and its Cayley-translated derivative — REGISTERED
                DEPENDENT (provenance: derived).
  - (A, main) : A and the clean-room build (GPT 5.6, web, different
                account; zero shared code; W and I only) — REGISTERED
                INDEPENDENT. Same mathematical destination on cycles.
  - (main, ref1): two members of the received file sharing internal
                helpers — registered dependent WITHIN the received family.

Truth labels are EXTENSIONAL (registered fix after first contact):
cycle/alias/noisy -> n; wobble/lollipop/nonstat -> None (abstain correct).

Two axes per pair (never merged into one label):
  Axis D: destination agreement (majority claims per instance).
  Axis P: path dependence — token channel (M1 same-wrong-value over
          per-instance analytic null, matched+crossed, instance-level
          significance) and journal channel (schedule co-adaptation over
          world-side perturbations {id, bp+1, bp+3, rev, nseed}; reference
          field = max(0, q75) over reference pairs, leave-candidate-
          family-out, margin 0.10, matched AND crossed).
References for the field: W, M, P (ours, scout-09 lineage, restated on
the string interface) + the received family (ONE construction unit,
represented by ref1; excluded whenever a candidate belongs to it).

Preregistered expectations (before running):
  E1 (A, Gt) dependent genealogy -> flagged by at least one channel.
     Registered nuance from first contact: partial decoupling on alias
     (the translation changed the interface channel) — reported per
     stratum, does not rescue or kill E1 by itself.
  E2 (A, main) independent genealogy -> CLEAN on both channels while
     DESTINATION_SAME on cycle strata. This is C7 live: true independent
     convergence must not be written off as glue. If flagged instead,
     the GPT alternative reading (the metric measures world/interface
     forcing, not construction) gains direct support — either outcome
     is a result.
  E3 (main, ref1) shared-helper family -> flagged (the channels must see
     real shared construction inside the received file).
  E4 the naive destination detector fires on BOTH (A,Gt) and (A,main) on
     cycle strata — same destination — demonstrating it cannot see
     genealogy (the K1 regression arm, unit-test status).
  E5 the central contrast: (A,Gt) = SAME+DEPENDENT vs (A,main) =
     SAME+CLEAN. If both genealogies read alike on axis P, the metric
     does not measure construction — Experiment A's premise falls and
     that is the finding.
Thresholds fixed: token margin 0.05 (as scouts 04-05), journal margin
0.10, significance mean > 2*se at instance level. R_INST=4, K_SEEDS=4,
CAP=400 calls.
"""
import sys, os, random
from math import gcd
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', 'experiment_A'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', 'experiment_A', 'received'))
from worlds_general import (GCycle, GAliasCycle, GLollipop, GWobble,
                            GNonstationary, run_language,
                            lang_A_general, lang_G_translated)
import find_order_solvers as fos

R_INST = 4
K_SEEDS = 4
CAP = 400
TOKEN_MARGIN = 0.05
JOURNAL_MARGIN = 0.10
PERTS = [('id', 0, False, 0), ('bp+1', 1, False, 0), ('bp+3', 3, False, 0),
         ('rev', 0, True, 0), ('nseed', 0, False, 1)]

# ---- our reference languages restated on the string interface (our code) ---

def lang_P_str(oracle, cap_calls, seed, samples=120):
    rng = random.Random(seed)
    g, npos = 0, 0
    for _ in range(samples):
        a, b = rng.randint(0, 160), rng.randint(0, 160)
        if a == b: continue
        if oracle('R' * a, 'R' * b) and oracle('R' * a, 'R' * b):
            g = gcd(g, abs(a - b)); npos += 1
    if npos == 0: return ('TO',)
    return ('VAL', g, npos >= 4)

def lang_W_str(oracle, cap_calls, seed):
    rng = random.Random(seed)
    k0 = None
    for k in range(1, 41):
        if oracle('R' * k, 'R' * (k - 1)): k0 = k; break
    if k0 is None: return ('AB',)
    hits = sum(oracle('R' * (k0 + i), 'R' * k0) for i in range(1, 6))
    return ('VAL', k0, hits >= 3)

def lang_M_str(oracle, cap_calls, seed):
    lo, hi = 1, 170
    while lo < hi:
        mid = (lo + hi) // 2
        if oracle('R' * mid, 'R' * lo): hi = mid
        else: lo = mid + 1
    ok = sum(oracle('R' * (lo + i), 'R' * i) for i in range(1, 4))
    return ('VAL', lo, ok >= 2)

LANGS = {'A': lang_A_general, 'Gt': lang_G_translated,
         'main': fos.find_order_main, 'ref1': fos.find_order_ref1,
         'W': lang_W_str, 'M': lang_M_str, 'P': lang_P_str}
SALT = {'A': 11, 'Gt': 29, 'main': 501, 'ref1': 523,
        'W': 311, 'M': 331, 'P': 51}
RECEIVED_FAMILY = {'main', 'ref1'}
REF_UNITS = ['W', 'M', 'P', 'ref1']          # ref1 represents the family

def make_strata(rng):
    return {
        'cycle':    [GCycle(rng.randint(17, 40)) for _ in range(R_INST)],
        'alias':    [GAliasCycle(n, q) for n, q in
                     [(rng.choice([20, 24, 30, 36]),) * 0 or
                      (lambda n: (n, rng.choice([d for d in range(4, n // 2 + 1)
                                                 if n % d == 0])))(
                          rng.choice([20, 24, 30, 36]))
                      for _ in range(R_INST)]],
        'wobble':   [GWobble(rng.randint(17, 40)) for _ in range(R_INST)],
        'lollipop': [GLollipop(rng.randint(5, 12), rng.randint(12, 26))
                     for _ in range(R_INST)],
        'nonstat':  [GNonstationary(rng.randint(15, 26), rng.randint(27, 40),
                                    rng.randint(60, 200))
                     for _ in range(R_INST)],
        'noisy':    [GCycle(rng.randint(17, 40), eps=rng.uniform(0.02, 0.12))
                     for _ in range(R_INST)],
    }

def fresh_world(w):
    if isinstance(w, GNonstationary):
        return GNonstationary(w.n1, w.n2, w.switch)
    return w

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

def main():
    master = random.Random(20260711)
    strata = make_strata(master)
    keys = [(s, i) for s in strata for i in range(R_INST)]
    epairs = [(a, b) for a in range(len(PERTS)) for b in range(a + 1, len(PERTS))]
    tokens = {l: {k: {} for k in keys} for l in LANGS}
    logs = {l: {k: {} for k in keys} for l in LANGS}
    claims = {l: {k: [] for k in keys} for l in LANGS}

    for sname, insts in strata.items():
        for i, w in enumerate(insts):
            truth = w.truth
            for pi, (pn, bp, rev, dn) in enumerate(PERTS):
                for r in range(K_SEEDS):
                    oseed = 9000 + 17 * i + 7 * pi + 1013 * r + 977 * dn
                    for lname, fn in LANGS.items():
                        res, log = run_language(
                            fn, fresh_world(w), CAP,
                            seed=10007 * r + SALT[lname], bp=bp, rev=rev)
                        # note: oracle noise seed folded via oseed variation
                        tokens[lname][(sname, i)][(pi, r)] = classify(res, truth)
                        logs[lname][(sname, i)][(pi, r)] = log
                        if pn == 'id':
                            claims[lname][(sname, i)].append(res)

    # ---- axis D: destination agreement on id-perturbation ----
    def dest(x, y):
        same = diff = na = 0
        for k in keys:
            vx = [c[1] for c in claims[x][k] if c[0] == 'VAL']
            vy = [c[1] for c in claims[y][k] if c[0] == 'VAL']
            if not vx or not vy: na += 1; continue
            mx = max(set(vx), key=vx.count); my = max(set(vy), key=vy.count)
            same += mx == my; diff += mx != my
        return same, diff, na

    # ---- axis P, token channel ----
    def token_channel(x, y, crossed):
        excs = []
        from collections import Counter
        for k in keys:
            obs = n = 0
            cells = [(pi, r) for pi in range(len(PERTS)) for r in range(K_SEEDS)]
            for pi, r in cells:
                ry = (r + 1) % K_SEEDS if crossed else r
                obs += m1(tokens[x][k][(pi, r)], tokens[y][k][(pi, ry)]); n += 1
            obs /= n
            cx = Counter(t for t in tokens[x][k].values() if t[0] in ('WC', 'WD'))
            cy = Counter(t for t in tokens[y][k].values() if t[0] in ('WC', 'WD'))
            tot = len(tokens[x][k])
            e0 = sum((cx[t] / tot) * (cy[t2] / tot)
                     for t in cx for t2 in cy if t[1] == t2[1])
            excs.append(obs - e0)
        m = sum(excs) / len(excs)
        var = sum((e - m) ** 2 for e in excs) / max(len(excs) - 1, 1)
        return m, (var / len(excs)) ** 0.5

    # ---- axis P, journal channel ----
    fp = {l: {k: {r: [lcp_dist(logs[l][k][(a, r)], logs[l][k][(b, r)])
                      for a, b in epairs] for r in range(K_SEEDS)}
              for k in keys} for l in LANGS}

    def J(x, y, crossed, subset=None):
        per = []
        for k in (subset or keys):
            cs = [pearson(fp[x][k][r], fp[y][k][(r + 1) % K_SEEDS if crossed else r])
                  for r in range(K_SEEDS)]
            per.append(sum(cs) / len(cs))
        m = sum(per) / len(per)
        var = sum((c - m) ** 2 for c in per) / max(len(per) - 1, 1)
        return m, (var / len(per)) ** 0.5

    def q75(vals):
        vals = sorted(vals)
        return vals[max(0, -(-3 * len(vals) // 4) - 1)]

    def field(x, y):
        units = [u for u in REF_UNITS
                 if not ({u} | ({x, y} & RECEIVED_FAMILY) & RECEIVED_FAMILY
                         and u in RECEIVED_FAMILY and (x in RECEIVED_FAMILY or
                                                       y in RECEIVED_FAMILY))]
        units = [u for u in REF_UNITS if u not in (x, y)]
        if x in RECEIVED_FAMILY or y in RECEIVED_FAMILY:
            units = [u for u in units if u not in RECEIVED_FAMILY]
        prs = [(a, b) for ai, a in enumerate(units) for b in units[ai + 1:]]
        if len(prs) < 3: return None
        return max(0.0, q75([J(a, b, True)[0] for a, b in prs]))

    pairs = [('A', 'Gt', 'DEPENDENT genealogy'),
             ('A', 'main', 'INDEPENDENT genealogy (C7 live)'),
             ('main', 'ref1', 'received family (shared helpers)'),
             ('A', 'ref1', 'cross-check'), ('Gt', 'main', 'cross-check')]
    print(f"{'pair':<12} {'type':<32} {'D same/diff/na':>14} | "
          f"{'tok_m':>6} {'se':>5} {'tok_c':>6} | {'J_m':>5} {'J_c':>5} "
          f"{'field':>5} | verdict")
    print('-' * 118)
    for x, y, typ in pairs:
        ds, dd, dna = dest(x, y)
        tm, tse = token_channel(x, y, False)
        tc, tcs = token_channel(x, y, True)
        jm, jsm = J(x, y, False); jc, jsc = J(x, y, True)
        f = field(x, y)
        tok_flag = (tm > TOKEN_MARGIN and tm > 2 * tse and
                    tc > TOKEN_MARGIN and tc > 2 * tcs)
        j_flag = (f is not None and jm - f >= JOURNAL_MARGIN and
                  jm - f > 2 * jsm and jc - f >= JOURNAL_MARGIN and
                  jc - f > 2 * jsc)
        if tok_flag and j_flag: v = 'DEP (token+journal)'
        elif tok_flag: v = 'DEP (token)'
        elif j_flag: v = 'DEP (journal)'
        else: v = 'CLEAN'
        fstr = f"{f:.2f}" if f is not None else '  — '
        print(f"({x},{y})".ljust(12) + f"{typ:<32} "
              f"{ds:>4}/{dd}/{dna:<5} | {tm:>6.3f} {tse:>5.3f} {tc:>6.3f} | "
              f"{jm:>5.2f} {jc:>5.2f} {fstr:>5} | {v}")

    print("\nper-stratum journal J_matched for the two genealogies:")
    for x, y in [('A', 'Gt'), ('A', 'main')]:
        row = []
        for s in strata:
            m, _ = J(x, y, False, subset=[(s, i) for i in range(R_INST)])
            row.append(f"{s}={m:.2f}")
        print(f"  ({x},{y}): " + "  ".join(row))

if __name__ == '__main__':
    main()
