"""
SCOUT 07 (phase 0, NOT citable): field-relative calibration of the journal
channel (M6). Scout 06 left the absolute threshold dead: independent pairs
sit on a world-floor ~ 0.47 because every admitted (world-sensitive)
language's schedule co-adapts with the world to some degree.

The null, without chicken-and-egg (we may not presume to know which pairs
are independent): THE FIELD ITSELF. For a pair (X,Y):

  field(X) = median over other languages Z of coadapt(X,Z)
  excess(X,Y) = coadapt(X,Y) - max(field(X), field(Y))

flag DEPENDENT iff excess > MARGIN and > 2*se (instance-level), on matched
AND crossed seeds (co-adaptation must survive seed decorrelation).

Preregistered limit, stated before running: the field-null PRESUMES POOL
DIVERSITY. A pool of mostly-shared-postulate languages contaminates the
median — "a thousand walkers with one brain is one walker" (Fable review 2)
arriving as a formal precondition of the instrument. Our scout pool is
deliberately cluster-heavy (A~A', S1~S2, N~C, N2~C2); G is added to
thicken the field. If E1 pairs fail to flag, diagnose per-language field
values before declaring the channel dead.

Preregistered expectations:
  E1 (A,A') clone, (N2,C2) postulate, (N,C) coin-masked -> FLAGGED
     (excess above field, matched and crossed).
  E2 (A,P), (N2,P), (G,P) -> NOT flagged (they are the field).
  E3 (S1,S2) cosmetic -> NOT flagged by this channel (corr 0.0; their
     dependence belongs to the v2 token channel: CONTACT_SCHEDULE).
  E4 (A,N2), (A,G) -> borderline EXPECTED and recorded, not presumed:
     scan-family languages share real origin-channel reliance; if flagged,
     that is interface-level dependence — attribution to interface vs
     postulate belongs to the interface arm (varying I), later.
MARGIN = 0.10 (fixed).
"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scout_06_schedule_coadaptation as s6

MARGIN = 0.10
K = s6.K_SEEDS
R_INST = s6.R_INST

def lang_G(orc, cap, rng):
    for k in range(1, cap + 1):
        for j in range(k):
            if orc.same(('R', k), ('R', j)): return ('VAL', k - j, True)
    return ('TO',)

def main():
    LANGS = dict(s6.LANGS); LANGS['G'] = lang_G
    SALT = dict(s6.SALT); SALT['G'] = 211
    master = random.Random(20260710)
    strata = s6.make_strata(master)
    keys = [(s, i) for s in strata for i in range(R_INST)]
    WORLD_PERTS = [i for i, p in enumerate(s6.PERTS) if p[3] == 0]
    epairs = [(a, b) for ai, a in enumerate(WORLD_PERTS)
              for b in WORLD_PERTS[ai + 1:]]

    journals = {l: {k: {} for k in keys} for l in LANGS}
    for sname, insts in strata.items():
        for i, w in enumerate(insts):
            for pi, pert in enumerate(s6.PERTS):
                cap = s6.CAP0 + pert[3]
                for r in range(K):
                    oseed = 7000 + 13 * i + 5 * pi + 1009 * r
                    for lname, fn in LANGS.items():
                        orc = s6.Oracle(w, pert, oseed)
                        fn(orc, cap, random.Random(10007 * r + SALT[lname]))
                        journals[lname][(sname, i)][(pi, r)] = orc.log

    fp = {l: {k: {r: [s6.lcp_dist(journals[l][k][(a, r)],
                                  journals[l][k][(b, r)])
                      for a, b in epairs] for r in range(K)}
              for k in keys} for l in LANGS}

    def coadapt_i(x, y, k, crossed):
        cs = []
        for r in range(K):
            ry = (r + 1) % K if crossed else r
            cs.append(s6.pearson(fp[x][k][r], fp[y][k][ry]))
        return sum(cs) / len(cs)

    def med(v):
        v = sorted(v); n = len(v)
        return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2

    names = list(LANGS)
    # per-instance field for each language: median coadapt with all others
    def excess_stats(x, y, crossed):
        excs = []
        for k in keys:
            cxy = coadapt_i(x, y, k, crossed)
            fx = med([coadapt_i(x, z, k, crossed) for z in names
                      if z not in (x, y)])
            fy = med([coadapt_i(y, z, k, crossed) for z in names
                      if z not in (x, y)])
            excs.append(cxy - max(fx, fy))
        m = sum(excs) / len(excs)
        var = sum((e - m) ** 2 for e in excs) / max(len(excs) - 1, 1)
        return m, (var / len(excs)) ** 0.5

    print("per-language field (matched, mean over instances):")
    for l in names:
        vals = []
        for k in keys:
            vals.append(med([coadapt_i(l, z, k, False) for z in names if z != l]))
        print(f"  {l:<3} field={sum(vals)/len(vals):.3f}")

    pairs = [("A", "A'", 'clone'), ('N2', 'C2', 'postulate'),
             ('N', 'C', 'coin-masked'), ('A', 'P', 'indep'),
             ('N2', 'P', 'indep'), ('G', 'P', 'indep'),
             ('S1', 'S2', 'cosmetic'), ('A', 'N2', 'scan family'),
             ('A', 'G', 'scan family')]
    print(f"\n{'pair':<10} {'type':<12} {'exc_m':>7} {'se':>6} {'exc_c':>7} "
          f"{'se':>6} | verdict (margin {MARGIN})")
    print('-' * 78)
    for x, y, typ in pairs:
        em, sem = excess_stats(x, y, False)
        ec, sec = excess_stats(x, y, True)
        sig = lambda e, s: e > MARGIN and e > 2 * s
        v = 'DEPENDENT (journal)' if sig(em, sem) and sig(ec, sec) else 'not flagged'
        print(f"({x},{y})".ljust(10) + f"{typ:<12} {em:>7.3f} {sem:>6.3f} "
              f"{ec:>7.3f} {sec:>6.3f} | {v}")

if __name__ == '__main__':
    main()
