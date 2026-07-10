"""
SCOUT 09 (phase 0, NOT citable): the reference-pair field — the exit from
scout 08's recursion. The null-pool's diversity is not measured; it is
CONSTRUCTED and declared.

Fixed before data:
  REFERENCES = {A, P, W, M} — four constructions declared mechanism-disjoint
  by design (the declaration is an assumption of the design, not a measured
  fact — this goes into the prereg scope verbatim):
    A : linear ascending scan of the ORIGIN channel (algebra family).
    P : random pair sampler, gcd of net differences (probabilistic family).
    W : adjacent-pair walker — probes (R,k) vs (R,k-1); responds to sticky /
        absorbing / blurred structure; never uses the origin channel. NEW.
    M : interval bisection over pair probes (R,mid) vs (R,lo); adaptive
        divide, not linear scan; never uses the origin channel. NEW.
  field(x,y) = max(0, q75 of J_crossed over reference pairs excluding any
  reference in {x,y}); UNKNOWN if fewer than 3 reference pairs remain.
  Flag DEPENDENT(journal) iff excess >= 0.10 AND > 2*se, matched AND crossed.
  The field reads ONLY reference pairs, so pool composition cannot move it:
  both scout-08 attacks are structurally out of reach.

Preregistered expectations:
  E1 (A,A') clone, (N2,C2) postulate, (N,C) coin-masked -> FLAGGED in all
     three pools. KILL if any is not.
  E2 (G,P), (A,Pv) independents -> clean in all pools. KILL if flagged.
     (Pv = P-variant without short-circuit; same family, different instance.)
  E3 (P,Pv) same-construction-family positive control -> expected FLAGGED.
  E4 the field is structurally identical across pools (reference journals
     do not depend on pool composition) — printed to confirm, not tested.
  E5 risk, stated in advance: if J(A,M) or J(A,W) lands high (reference
     disjointness weaker than declared), the field inflates and E1 may
     under-flag — that would falsify the DECLARATION, not the rule; the
     remedy is better references, preregistered again.
"""
import sys, os, random
from math import gcd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scout_06_schedule_coadaptation as s6
import scout_08_component_field as s8

MARGIN = 0.10
K = s6.K_SEEDS
R_INST = s6.R_INST

def lang_W(orc, cap, rng):
    k0 = None
    for k in range(1, 41):
        if orc.same(('R', k), ('R', k - 1)): k0 = k; break
    if k0 is None: return ('AB',)
    hits = sum(orc.same(('R', k0 + i), ('R', k0)) for i in range(1, 6))
    return ('VAL', k0, hits >= 3)

def lang_M(orc, cap, rng):
    lo, hi = 1, cap
    while lo < hi:
        mid = (lo + hi) // 2
        if orc.same(('R', mid), ('R', lo)): hi = mid
        else: lo = mid + 1
    ok = sum(orc.same(('R', lo + i), ('R', i)) for i in range(1, 4))
    return ('VAL', lo, ok >= 2)

def lang_Pv(orc, cap, rng, samples=150):
    g, npos = 0, 0
    for _ in range(samples):
        a, b = rng.randint(0, cap), rng.randint(0, cap)
        if a == b: continue
        r1 = orc.same(('R', a), ('R', b))
        r2 = orc.same(('R', a), ('R', b))          # always emitted (no
        if r1 and r2:                              # short-circuit)
            g = gcd(g, abs(a - b)); npos += 1
    if npos == 0: return ('TO',)
    return ('VAL', g, npos >= 4)

REFS = ['A', 'P', 'W', 'M']
NEW = {'W': lang_W, 'M': lang_M, 'Pv': lang_Pv}
NEW_SALT = {'W': 311, 'M': 331, 'Pv': 347}

def run_pool(pname, LANGS, SALT, targets):
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
                                  journals[l][k][(b, r)]) for a, b in epairs]
                  for r in range(K)} for k in keys} for l in LANGS}

    def J(x, y, crossed):
        per_inst = []
        for k in keys:
            cs = [s6.pearson(fp[x][k][r],
                             fp[y][k][(r + 1) % K if crossed else r])
                  for r in range(K)]
            per_inst.append(sum(cs) / len(cs))
        m = sum(per_inst) / len(per_inst)
        var = sum((c - m) ** 2 for c in per_inst) / max(len(per_inst) - 1, 1)
        return m, (var / len(per_inst)) ** 0.5

    def q75(vals):
        vals = sorted(vals)
        return vals[max(0, -(-3 * len(vals) // 4) - 1)]

    print(f"\n=== pool {pname}")
    ref_pairs = [(a, b) for ai, a in enumerate(REFS) for b in REFS[ai + 1:]]
    print("    reference pairs (J_crossed): " +
          "  ".join(f"({a},{b})={J(a, b, True)[0]:.2f}" for a, b in ref_pairs))

    def field(x, y):
        refs = [r for r in REFS if r not in (x, y)]
        prs = [(a, b) for ai, a in enumerate(refs) for b in refs[ai + 1:]]
        if len(prs) < 3: return None
        return max(0.0, q75([J(a, b, True)[0] for a, b in prs]))

    print(f"    {'pair':<10} {'J_m':>6} {'J_c':>6} {'field':>6} | verdict")
    for x, y, typ in targets:
        jm, sem = J(x, y, False); jc, sec = J(x, y, True)
        f = field(x, y)
        if f is None:
            print(f"    ({x},{y})".ljust(14) +
                  f"{jm:>6.2f} {jc:>6.2f} {'—':>6} | UNKNOWN   [{typ}]")
            continue
        flag = (jm - f >= MARGIN and jm - f > 2 * sem and
                jc - f >= MARGIN and jc - f > 2 * sec)
        v = 'DEPENDENT (journal)' if flag else 'not flagged'
        print(f"    ({x},{y})".ljust(14) + f"{jm:>6.2f} {jc:>6.2f} "
              f"{f:>6.2f} | {v}   [{typ}]")

def main():
    targets = [("A", "A'", 'clone'), ('N2', 'C2', 'postulate'),
               ('N', 'C', 'coin-masked'), ('G', 'P', 'indep'),
               ('A', 'Pv', 'indep'), ('P', 'Pv', 'same family')]
    base = dict(s8.BASE); base.update(NEW)
    bsalt = dict(s8.BASE_SALT); bsalt.update(NEW_SALT)
    run_pool('P0 base+refs', base, bsalt, targets)
    L1 = dict(base); L1.update(s8.EXTRA_P1)
    S1_ = dict(bsalt); S1_.update(s8.SALT_P1)
    run_pool('P1 under-flag (scan-heavy)', L1, S1_, targets)
    L2 = dict(base); L2.update(s8.EXTRA_P2)
    S2_ = dict(bsalt); S2_.update(s8.SALT_P2)
    run_pool('P2 over-flag (decoys)', L2, S2_, targets)

if __name__ == '__main__':
    main()
