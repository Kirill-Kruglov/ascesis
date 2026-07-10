"""
SCOUT 12 (phase 0, NOT citable): stress strata — does dependence become
visible when the competent start to fall?

Scout 11 left E3 fallen: (main, ref1) share internal helpers yet read
CLEAN, because both almost never err — the channels read dependence only
through errors. Two hypotheses, both preregistered as meaningful:

  H-stress : under worlds that defeat their shared validation thresholds
             (noise above tolerance; partial quotient traps; orders
             beyond budget), the received family co-errs in correlated
             ways -> flags. "Competence masks dependence" was a stress
             deficiency of the world family.
  H-theorem: even under stress the pair stays clean, because shared
             THRESHOLDS without shared RANDOMNESS decorrelate — their
             query streams are disjoint, so acceptance events are
             near-independent given the world, and the per-instance null
             absorbs the rest. Then "only falls testify" hardens toward
             a theorem, and (main, ref1) becomes a MEASURED instance of
             the Codex residual hole (shared implementation with
             decorrelated surface = the declared blind spot of any
             black-box instrument). The prereg scope already covers it.

Stress strata (all cyclic-family, count-fast):
  qtrap   : QuotientTrap(n = q*k, q in 5..9): a fixed per-instance subset
            (~60%) of q-multiple displacement classes falsely answer True
            — a partial false wall at q. Truth n (extensional).
  noise_hi: GCycle(n), eps in 0.15..0.30 — above the received solvers'
            validation tolerance. Truth n.
  bigN    : GCycle(n in 600..1500) with CAP=400 — order beyond budget.
            Truth n (expect TO-dominated; mode-level info only).

Preregistered expectations:
  E1 (main,ref1), (main,ref2): the question above — flagged => H-stress;
     clean on all strata => H-theorem instance, recorded.
  E2 (A, Gt): flags on noise_hi (replication of scout 11's channel).
  E3 (A, main): must NOT flag on qtrap — the trap value q is a
     world-forced attractor; the per-instance analytic null must absorb
     it. KILL of the token channel under stress if an independent pair
     flags here.
  E4 report: per-stratum breakdown for (main, ref1) and (A, main).
Thresholds as scout 11 (token 0.05, journal 0.10, 2*se). R_INST=4,
K_SEEDS=4, CAP=400.
"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', 'experiment_A'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', 'experiment_A', 'received'))
from worlds_general import (GWorld, GCycle, run_language,
                            lang_A_general, lang_G_translated)
import find_order_solvers as fos
from scout_11_two_genealogies import (lang_P_str, lang_W_str, lang_M_str,
                                      classify, m1, lcp_dist, pearson)

R_INST = 4
K_SEEDS = 4
CAP = 400
TOKEN_MARGIN = 0.05
JOURNAL_MARGIN = 0.10
PERTS = [('id', 0, False), ('bp+1', 1, False), ('bp+3', 3, False),
         ('rev', 0, True), ('nseed', 0, False)]


class QuotientTrap(GWorld):
    """Cycle(n), n = q*k. A fixed per-instance subset of the q-multiple
    displacement classes (other than 0 mod n) falsely answers True —
    a partial, deterministic false wall at q. Truth n (extensional)."""
    def __init__(self, n, q, wrng, frac=0.6):
        self.n, self.q, self.eps, self.truth = n, q, 0.0, n
        self.trapped = {m for m in range(q, n, q)
                        if m % n != 0 and wrng.random() < frac}
    def run(self, word, bp=0):
        return (bp + word.count('R') - word.count('L')) % self.n
    def same(self, u, v, bp=0):
        d = (self.run(u, bp) - self.run(v, bp)) % self.n
        return d == 0 or d in self.trapped


LANGS = {'A': lang_A_general, 'Gt': lang_G_translated,
         'main': fos.find_order_main, 'ref1': fos.find_order_ref1,
         'ref2': fos.find_order_ref2,
         'W': lang_W_str, 'M': lang_M_str, 'P': lang_P_str}
SALT = {'A': 11, 'Gt': 29, 'main': 501, 'ref1': 523, 'ref2': 541,
        'W': 311, 'M': 331, 'P': 51}
RECEIVED = {'main', 'ref1', 'ref2'}
REF_UNITS = ['W', 'M', 'P', 'ref1']


def make_strata(rng):
    def qtrap():
        q = rng.randint(5, 9)
        return QuotientTrap(q * rng.randint(3, 5), q, rng)
    return {
        'qtrap':    [qtrap() for _ in range(R_INST)],
        'noise_hi': [GCycle(rng.randint(17, 40), eps=rng.uniform(0.15, 0.30))
                     for _ in range(R_INST)],
        'bigN':     [GCycle(rng.randint(600, 1500)) for _ in range(R_INST)],
    }


def main():
    master = random.Random(20260712)
    strata = make_strata(master)
    keys = [(s, i) for s in strata for i in range(R_INST)]
    epairs = [(a, b) for a in range(len(PERTS)) for b in range(a + 1, len(PERTS))]
    tokens = {l: {k: {} for k in keys} for l in LANGS}
    logs = {l: {k: {} for k in keys} for l in LANGS}

    for sname, insts in strata.items():
        for i, w in enumerate(insts):
            for pi, (pn, bp, rev) in enumerate(PERTS):
                for r in range(K_SEEDS):
                    for lname, fn in LANGS.items():
                        res, log = run_language(
                            fn, w, CAP, seed=10007 * r + SALT[lname],
                            bp=bp, rev=rev)
                        tokens[lname][(sname, i)][(pi, r)] = classify(res, w.truth)
                        logs[lname][(sname, i)][(pi, r)] = log

    from collections import Counter
    cells = [(pi, r) for pi in range(len(PERTS)) for r in range(K_SEEDS)]

    def token_channel(x, y, crossed, subset=None):
        excs = []
        for k in (subset or keys):
            obs = 0
            for pi, r in cells:
                ry = (r + 1) % K_SEEDS if crossed else r
                obs += m1(tokens[x][k][(pi, r)], tokens[y][k][(pi, ry)])
            obs /= len(cells)
            cx = Counter(t for t in tokens[x][k].values() if t[0] in ('WC', 'WD'))
            cy = Counter(t for t in tokens[y][k].values() if t[0] in ('WC', 'WD'))
            tot = len(tokens[x][k])
            e0 = sum((cx[t] / tot) * (cy[t2] / tot)
                     for t in cx for t2 in cy if t[1] == t2[1])
            excs.append(obs - e0)
        m = sum(excs) / len(excs)
        var = sum((e - m) ** 2 for e in excs) / max(len(excs) - 1, 1)
        return m, (var / len(excs)) ** 0.5

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
        units = [u for u in REF_UNITS if u not in (x, y)]
        if x in RECEIVED or y in RECEIVED:
            units = [u for u in units if u not in RECEIVED]
        prs = [(a, b) for ai, a in enumerate(units) for b in units[ai + 1:]]
        if len(prs) < 3: return None
        return max(0.0, q75([J(a, b, True)[0] for a, b in prs]))

    pairs = [('main', 'ref1', 'received: shared helpers'),
             ('main', 'ref2', 'received: shared helpers'),
             ('A', 'Gt', 'derived (replication)'),
             ('A', 'main', 'clean-room (must stay clean)'),
             ('W', 'P', 'independent control')]
    print(f"{'pair':<12} {'type':<28} {'tok_m':>6} {'se':>5} {'tok_c':>6} | "
          f"{'J_m':>5} {'J_c':>5} {'field':>5} | verdict")
    print('-' * 96)
    for x, y, typ in pairs:
        tm, ts = token_channel(x, y, False)
        tc, tcs = token_channel(x, y, True)
        jm, jsm = J(x, y, False); jc, jsc = J(x, y, True)
        f = field(x, y)
        tok = (tm > TOKEN_MARGIN and tm > 2 * ts and
               tc > TOKEN_MARGIN and tc > 2 * tcs)
        jf = (f is not None and jm - f >= JOURNAL_MARGIN and jm - f > 2 * jsm
              and jc - f >= JOURNAL_MARGIN and jc - f > 2 * jsc)
        v = ('DEP (token+journal)' if tok and jf else 'DEP (token)' if tok
             else 'DEP (journal)' if jf else 'CLEAN')
        fs = f"{f:.2f}" if f is not None else ' — '
        print(f"({x},{y})".ljust(12) + f"{typ:<28} {tm:>6.3f} {ts:>5.3f} "
              f"{tc:>6.3f} | {jm:>5.2f} {jc:>5.2f} {fs:>5} | {v}")

    print("\nper-stratum token excess (matched):")
    for x, y in [('main', 'ref1'), ('A', 'main'), ('A', 'Gt')]:
        row = []
        for s in strata:
            m, _ = token_channel(x, y, False,
                                 subset=[(s, i) for i in range(R_INST)])
            row.append(f"{s}={m:.3f}")
        print(f"  ({x},{y}): " + "  ".join(row))

    print("\ntoken sample, instance 0 of each stratum (id-pert, seed 0):")
    for s in strata:
        row = " ".join(f"{l}:{tokens[l][(s, 0)][(0, 0)][0]}"
                       f"{'' if tokens[l][(s, 0)][(0, 0)][1] is None else ':' + str(tokens[l][(s, 0)][(0, 0)][1])}"
                       for l in LANGS)
        print(f"  {s:<9} {row}")

if __name__ == '__main__':
    main()
