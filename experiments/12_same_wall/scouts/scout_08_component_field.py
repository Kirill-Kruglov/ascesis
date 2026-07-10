"""
SCOUT 08 (phase 0, NOT citable): the Codex field repair under both of his
contamination attacks. Journal channel only.

Fixed rules (locked in this docstring before running):
  - Cluster the pool: edge(i,j) iff crossed co-adaptation mean >= 0.30 AND
    mean > 2*se (instance-level) — scout stand-in for his p_perm <= .01.
    Components by union-find.
  - field_for_pair(i,j): EXTERNAL component pairs only (candidates' own
    components never calibrate their null); value per component pair =
    median of cross-language J; field = max(0, q75 nearest-rank);
    UNKNOWN if fewer than 3 external component pairs.
  - Flag DEPENDENT(journal) iff (J_matched - field >= 0.10) AND
    (J_crossed - field >= 0.10), each also > 2*se.

Pools:
  P0 base       — the 10 languages of scouts 06-07 (already cluster-heavy).
  P1 under-flag — 69% scan family (adds A'', A2, G2, N3): Codex sham (a).
  P2 over-flag  — base + 3 decoy languages with orthogonal-subset world
                  response (approximation of his anti-correlated decoys;
                  they emit constant ABSTAIN tokens — journal-admitted,
                  token-inadmissible — and enter the journal field pool).

Preregistered expectations:
  E1 P0/P1: clone (A,A') and postulate (N2,C2) FLAGGED with the external
     field (the scan component no longer calibrates its own members);
     coin-masked (N,C) reported (may join the scan component — recorded).
  E2 P0: independents (A,P),(G,P) — likely UNKNOWN, not clean: with so few
     components the <3-external-pairs rule fires. That is itself the
     measurement: the field-null demands >= 3 external components — the
     pool-diversity precondition, quantified.
  E3 P2: honest independents must NOT flag (q75 + max(0,.) must hold the
     floor against decoys); clone must still flag.
  Kills (Codex's, verbatim): under-flag pool still changes candidate
  verdicts after component collapse; decoys make independent pairs flag;
  <3 external pairs silently treated as low field instead of UNKNOWN;
  candidate's own component contributes to its field.
"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scout_06_schedule_coadaptation as s6

MARGIN = 0.10
EDGE_MIN = 0.30
K = s6.K_SEEDS
R_INST = s6.R_INST

def lang_G(orc, cap, rng):
    for k in range(1, cap + 1):
        for j in range(k):
            if orc.same(('R', k), ('R', j)): return ('VAL', k - j, True)
    return ('TO',)

def lang_A2(orc, cap, rng):                     # scan evens first, then odds
    for k in list(range(2, cap + 1, 2)) + list(range(1, cap + 1, 2)):
        if orc.same(('R', k), ('R', 0)): return ('VAL', k, True)
    return ('TO',)

def lang_G2(orc, cap, rng):                     # pairwise, j descending
    for k in range(1, cap + 1):
        for j in range(k - 1, -1, -1):
            if orc.same(('R', k), ('R', j)): return ('VAL', k - j, True)
    return ('TO',)

def lang_N3(orc, cap, rng):                     # scan+confirm, 4 checks
    m = k0 = None
    for k in range(1, 60):
        for j in range(k):
            if orc.same(('R', k), ('R', j)): m, k0 = k - j, j; break
        if m: break
    if not m: return ('TO',)
    conf = sum(orc.same(('R', k0 + i * m), ('R', k0)) for i in range(1, 5)) / 4
    return ('VAL', m, True) if conf > 0.5 else ('AB',)

def lang_A3(orc, cap, rng):                     # second clone, lighter padding
    for k in range(1, cap + 1):
        if rng.random() < 0.25:
            j = rng.randint(1, cap); orc.same(('L', j), ('R', j))
        if orc.same(('R', k), ('R', 0)): return ('VAL', k, True)
    return ('TO',)

def lang_D1(orc, cap, rng):                     # decoy: L-channel responder
    nb = sum(orc.same(('L', j), ('L', 0)) for j in range(1, 5))
    for _ in range(5 + 8 * nb): orc.same(('R', 1), ('R', 1))
    return ('AB',)

def lang_D2(orc, cap, rng):                     # decoy: basepoint responder
    nb = sum(orc.same(('L', j), ('R', j)) for j in range(1, 4))
    for _ in range(4 + 10 * nb): orc.same(('R', 2), ('R', 2))
    return ('AB',)

def lang_D3(orc, cap, rng):                     # decoy: noise responder
    nb = sum(orc.same(('R', 1), ('R', 0)) for _ in range(6))
    for _ in range(3 + 6 * nb): orc.same(('R', 3), ('R', 3))
    return ('AB',)

BASE = dict(s6.LANGS); BASE['G'] = lang_G
BASE_SALT = dict(s6.SALT); BASE_SALT['G'] = 211
EXTRA_P1 = {'A2': lang_A2, 'G2': lang_G2, 'N3': lang_N3, "A''": lang_A3}
SALT_P1 = {'A2': 227, 'G2': 241, 'N3': 257, "A''": 271}
EXTRA_P2 = {'D1': lang_D1, 'D2': lang_D2, 'D3': lang_D3}
SALT_P2 = {'D1': 281, 'D2': 293, 'D3': 307}

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

    names = list(LANGS)
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

    Jm = {}; Jc = {}
    for a in range(len(names)):
        for b in range(a + 1, len(names)):
            x, y = names[a], names[b]
            Jm[(x, y)] = Jm[(y, x)] = J(x, y, False)
            Jc[(x, y)] = Jc[(y, x)] = J(x, y, True)

    # components on crossed co-adaptation
    parent = {l: l for l in names}
    def find(a):
        while parent[a] != a: parent[a] = parent[parent[a]]; a = parent[a]
        return a
    for x in names:
        for y in names:
            if x < y:
                m, se = Jc[(x, y)]
                if m >= EDGE_MIN and m > 2 * se:
                    parent[find(x)] = find(y)
    comps = {}
    for l in names: comps.setdefault(find(l), []).append(l)
    comp_of = {l: find(l) for l in names}
    print(f"\n=== pool {pname} — components:")
    for c, ms in comps.items(): print(f"    {sorted(ms)}")

    def q75(vals):
        vals = sorted(vals)
        idx = max(0, -(-3 * len(vals) // 4) - 1)      # nearest-rank 75%
        return vals[idx]

    def field(x, y):
        cx, cy = comp_of[x], comp_of[y]
        ext = [c for c in comps if c not in (cx, cy)]
        pairs = [(a, b) for ai, a in enumerate(ext) for b in ext[ai + 1:]]
        if len(pairs) < 3: return None
        vals = [sorted(Jc[(i, j)][0] for i in comps[a] for j in comps[b])
                [len(comps[a]) * len(comps[b]) // 2]
                for a, b in pairs]
        return max(0.0, q75(vals))

    print(f"    {'pair':<10} {'J_m':>6} {'J_c':>6} {'field':>6} | verdict")
    for x, y, typ in targets:
        jm, sem = Jm[(x, y)]; jc, sec = Jc[(x, y)]
        f = field(x, y)
        if f is None:
            v = 'UNKNOWN (<3 external component pairs)'
            print(f"    ({x},{y})".ljust(14) + f"{jm:>6.2f} {jc:>6.2f} "
                  f"{'—':>6} | {v}   [{typ}]")
            continue
        flag = (jm - f >= MARGIN and jm - f > 2 * sem and
                jc - f >= MARGIN and jc - f > 2 * sec)
        v = 'DEPENDENT (journal)' if flag else 'not flagged'
        print(f"    ({x},{y})".ljust(14) + f"{jm:>6.2f} {jc:>6.2f} "
              f"{f:>6.2f} | {v}   [{typ}]")

def main():
    t0 = [("A", "A'", 'clone'), ('N2', 'C2', 'postulate'),
          ('N', 'C', 'coin-masked'), ('A', 'P', 'indep'), ('G', 'P', 'indep')]
    run_pool('P0 base', BASE, BASE_SALT, t0)
    L1 = dict(BASE); L1.update(EXTRA_P1)
    S1_ = dict(BASE_SALT); S1_.update(SALT_P1)
    run_pool('P1 under-flag (69% scan family)', L1, S1_, t0)
    L2 = dict(BASE); L2.update(EXTRA_P2)
    S2_ = dict(BASE_SALT); S2_.update(SALT_P2)
    run_pool('P2 over-flag (3 decoys)', L2, S2_, t0)

if __name__ == '__main__':
    main()
