"""
SCOUT 05 (phase 0, NOT citable): instrument v2 — seed-block-correct
significance + world-sensitivity admission gate + the owed Codex sham S2
(stochastically masked shared blindness).

Fixes over scout 04 (both falls paid there):
  1. PSEUDO-REPLICATION: significance now comes from INSTANCE-LEVEL
     dispersion (mean excess over world instances, criterion fixed below),
     never from cell counts. K = 8 seeds. The per-instance null is analytic:
     E0_i = sum_v pX_i(wrong,v) * pY_i(wrong,v) from per-instance pooled
     marginals over (perturbation, seed) cells.
  2. ADMISSION GATE (completes the counterfactual-profile requirement):
     a path testifies only if its profile is WORLD-SENSITIVE.
       world_sensitivity(X) = P(token differs | same (e,r), different
       instance), pooled over strata;  admit iff >= 0.30
       profile_variation(X) = P(token differs | same instance, different
       (e,r) cell);                    admit iff >= 0.05
     Preregistered: Lr/Lp (grid-attractor languages) must FAIL admission —
     their tokens answer their own dice, not the world.

Sham S2 (Codex, owed since scout 04): WobbleCycle(n) — R-channel is an
honest n-cycle (truth n); L-channel is sticky below state 3 (NOT R^-1).
Languages N and C share one latent postulate ("L is R's inverse; one
channel's cycle is the world's order"); each picks a channel by its own
coin. N, on picking L, confidently claims 1 (WRONG_CONFIDENT); C
cross-checks the other channel and abstains (fails closed). Same latent
blindness, split surface modes, independent coins.

Preregistered expectations (before running):
  E1 (A,A')  clone       -> CONSTRUCTION_DEPENDENT (matched & crossed).
                            KILL v2 if not.
  E2 admission           -> Lr and Lp EXCLUDED by world-sensitivity;
                            everyone else admitted. KILL if Lr/Lp admitted.
  E3 (S1,S2) seed sham   -> CONTACT_SCHEDULE_DEPENDENT (dies under
                            crossing). KILL if CONSTRUCTION_DEPENDENT.
  E4 (A,G)   isomorph    -> CONSTRUCTION_DEPENDENT expected to persist
                            (shared origin channel + shared scan postulate);
                            margin vs clone reported, not presumed.
  E5 (A,P),(G,P) indep   -> NO_CONSTRUCTION_DEPENDENCE.
  E6 (N,C) masked sham   -> EXPECTED LIMIT: on the wobble stratum the
                            constructed shared postulate should be INVISIBLE
                            (co-failures = product of independent coins, so
                            per-instance null explains them; excess ~ 0).
                            On alias both confirm through the blurred origin
                            channel -> interface coupling MAY appear there;
                            report per-stratum. If v2 *does* read the wobble
                            stratum as dependent, that is a surprise
                            demanding diagnosis, not a pass.
Fixed criteria: dependence significant iff mean_exc > 0.05 AND
mean_exc > 2*se over instances. No learned weights.
"""
import random
from math import gcd

CAP0 = 180
R_INST = 6
K_SEEDS = 8
SENS_MIN = 0.30
PROFVAR_MIN = 0.05
EXC_MIN = 0.05

# ---------- worlds -----------------------------------------------------------

def _net(p): return p[1] if p[0] == 'R' else -p[1]

class CycleW:
    def __init__(self, n, eps=0.0): self.n, self.eps, self.truth = n, eps, n
    def same(self, p, q, bp): return (_net(p) - _net(q)) % self.n == 0

class AliasCycleW:
    def __init__(self, n, q): self.n, self.q, self.eps, self.truth = n, q, 0.0, n
    def same(self, p, qq, bp):
        blur = (p[1] == 0 or qq[1] == 0) and bp % self.n == 0
        return (_net(p) - _net(qq)) % (self.q if blur else self.n) == 0

class LollipopW:
    def __init__(self, t, c): self.t, self.c, self.eps, self.truth = t, c, 0.0, c
    def _end(self, p, bp):
        d, k = p
        if d == 'L': return max(bp - k, 0)
        pos = bp + k
        return pos if pos < self.t else self.t + (pos - self.t) % self.c
    def same(self, p, q, bp): return self._end(p, bp) == self._end(q, bp)

class NonstationaryW:
    def __init__(self, n1, n2, switch):
        self.n1, self.n2, self.switch, self.eps, self.truth = n1, n2, switch, 0.0, None
        self.count = 0
    def same(self, p, q, bp):
        self.count += 1
        n = self.n1 if self.count <= self.switch else self.n2
        return (_net(p) - _net(q)) % n == 0

class WobbleCycleW:
    """R: honest n-cycle. L: decrement, sticky at states <= 2 (NOT R^-1).
    Truth n (discoverable through the R channel)."""
    def __init__(self, n): self.n, self.eps, self.truth = n, 0.0, n
    def _end(self, p, bp):
        d, k = p
        if d == 'R': return (bp + k) % self.n
        return bp if bp <= 2 else max(bp - k, 2)
    def same(self, p, q, bp): return self._end(p, bp) == self._end(q, bp)

def fresh(w):
    return NonstationaryW(w.n1, w.n2, w.switch) if isinstance(w, NonstationaryW) else w

PERTS = [('id', 0, False, 0, 0), ('bp+1', 1, False, 0, 0), ('bp+3', 3, False, 0, 0),
         ('rev', 0, True, 0, 0), ('bud-', 0, False, -15, 0),
         ('bud+', 0, False, +15, 0), ('nseed', 0, False, 0, 1)]

class Oracle:
    def __init__(self, world, pert, seed):
        _, bp, rev, dbud, dn = pert
        self.w, self.bp, self.rev = fresh(world), bp, rev
        self.rng = random.Random(seed + 977 * dn)
        self.eps = world.eps
    def same(self, p, q):
        if self.rev:
            p = ('L' if p[0] == 'R' else 'R', p[1])
            q = ('L' if q[0] == 'R' else 'R', q[1])
        b = self.w.same(p, q, self.bp)
        if self.eps and self.rng.random() < self.eps: b = not b
        return b

# ---------- languages --------------------------------------------------------

def lang_A(orc, cap, rng):
    for k in range(1, cap + 1):
        if orc.same(('R', k), ('R', 0)): return ('VAL', k, True)
    return ('TO',)

def lang_A_clone(orc, cap, rng):
    for k in range(1, cap + 1):
        if rng.random() < 0.5:
            j = rng.randint(1, cap); orc.same(('L', j), ('R', j))
        if orc.same(('R', k), ('R', 0)): return ('VAL', k, True)
    return ('TO',)

def lang_G(orc, cap, rng):
    for k in range(1, cap + 1):
        for j in range(k):
            if orc.same(('R', k), ('R', j)): return ('VAL', k - j, True)
    return ('TO',)

def lang_P(orc, cap, rng, samples=200):
    g, npos = 0, 0
    for _ in range(samples):
        a, b = rng.randint(0, cap), rng.randint(0, cap)
        if a == b: continue
        if orc.same(('R', a), ('R', b)) and orc.same(('R', a), ('R', b)):
            g = gcd(g, abs(a - b)); npos += 1
    if npos == 0: return ('TO',)
    return ('VAL', g, npos >= 4)

H_GRID = [2, 3, 4, 5, 6, 8, 10, 12]

def _grid_min(compat):
    c = [h for h in H_GRID if compat(h)]
    return ('VAL', min(c), True) if c else ('AB',)

def lang_Lr(orc, cap, rng):
    obs = {}
    for _ in range(12):
        k = rng.randint(1, 14); obs[k] = orc.same(('R', k), ('R', 0))
    return _grid_min(lambda h: all((k % h == 0) == r for k, r in obs.items()))

def lang_Lp(orc, cap, rng):
    obs = []
    for _ in range(12):
        a, b = rng.randint(0, 20), rng.randint(0, 20)
        if a != b: obs.append((abs(a - b), orc.same(('R', a), ('R', b))))
    return _grid_min(lambda h: all((d % h == 0) == r for d, r in obs))

def lang_Sch1(orc, cap, rng):
    ks = [rng.randint(1, cap) for _ in range(25)]
    hits = [k for k in ks if orc.same(('R', k + 1), ('R', 1))]
    if hits:
        g = 0
        for h in hits: g = gcd(g, h)
        return ('VAL', g, True)
    return ('VAL', 2, True)

def lang_Sch2(orc, cap, rng):
    ks = [rng.randint(1, cap) for _ in range(25)]
    hits = [k for k in ks if orc.same(('L', k + 2), ('L', 2))]
    if hits:
        g = 0
        for h in hits: g = gcd(g, h)
        return ('VAL', g, True)
    return ('VAL', 2, True)

def lang_N(orc, cap, rng):
    """Masked-blindness sham, numeric face: trust one channel's cycle."""
    ch = rng.choice(['R', 'L'])
    for k in range(1, cap + 1):
        if orc.same((ch, k), (ch, 0)): return ('VAL', k, True)
    return ('TO',)

def lang_C(orc, cap, rng):
    """Same latent postulate (L is R's inverse), certifying face: cross-check
    the other channel; abstain if the postulate's prediction fails."""
    ch = rng.choice(['R', 'L'])
    other = 'L' if ch == 'R' else 'R'
    for k in range(1, cap + 1):
        if orc.same((ch, k), (ch, 0)):
            if orc.same((other, k), (other, 0)): return ('VAL', k, True)
            return ('AB',)
    return ('TO',)

LANGS = {'A': lang_A, "A'": lang_A_clone, 'G': lang_G, 'P': lang_P,
         'Lr': lang_Lr, 'Lp': lang_Lp, 'S1': lang_Sch1, 'S2': lang_Sch2,
         'N': lang_N, 'C': lang_C}
SALT = {'A': 11, "A'": 23, 'G': 37, 'P': 51, 'Lr': 67, 'Lp': 83,
        'S1': 99, 'S2': 99, 'N': 131, 'C': 149}

def make_strata(rng):
    def alias():
        n = rng.choice([20, 24, 28, 30, 36, 40])
        q = rng.choice([d for d in range(4, n // 2 + 1) if n % d == 0])
        return AliasCycleW(n, q)
    return {
        'cycle':    [CycleW(rng.randint(28, 44)) for _ in range(R_INST)],
        'alias':    [alias() for _ in range(R_INST)],
        'lollipop': [LollipopW(rng.randint(5, 15), rng.randint(15, 30))
                     for _ in range(R_INST)],
        'nonstat':  [NonstationaryW(rng.randint(17, 30), rng.randint(31, 44),
                                    rng.randint(100, 250)) for _ in range(R_INST)],
        'noisy':    [CycleW(rng.randint(28, 44), eps=rng.uniform(0.02, 0.2))
                     for _ in range(R_INST)],
        'wobble':   [WobbleCycleW(rng.randint(28, 44)) for _ in range(R_INST)],
    }

def classify(claim, truth):
    if claim[0] == 'VAL':
        _, v, conf = claim
        if truth is not None and v == truth: return ('S', v)
        return ('WC', v) if conf else ('WD', v)
    if claim[0] == 'AB':
        return ('S', 'AB') if truth is None else ('AB', None)
    return ('TO', None)

def m1(tx, ty):
    return int(tx[0] in ('WC', 'WD') and ty[0] in ('WC', 'WD') and tx[1] == ty[1])

# ---------- run --------------------------------------------------------------

def main():
    master = random.Random(20260710)
    strata = make_strata(master)
    keys = [(s, i) for s in strata for i in range(R_INST)]
    cells = [(pi, r) for pi in range(len(PERTS)) for r in range(K_SEEDS)]
    tokens = {l: {k: {} for k in keys} for l in LANGS}
    for sname, insts in strata.items():
        for i, w in enumerate(insts):
            for pi, pert in enumerate(PERTS):
                cap = CAP0 + pert[3]
                oseed = 7000 + 13 * i + 5 * pi
                for r in range(K_SEEDS):
                    for lname, fn in LANGS.items():
                        orc = Oracle(w, pert, oseed)
                        lrng = random.Random(10007 * r + SALT[lname])
                        tokens[lname][(sname, i)][(pi, r)] = \
                            classify(fn(orc, cap, lrng), w.truth)

    # ---- admission gate ----
    print("admission gate (world_sensitivity >= %.2f, profile_variation >= %.2f):"
          % (SENS_MIN, PROFVAR_MIN))
    admitted = {}
    rng = random.Random(555)
    for l in LANGS:
        diff_w = diff_c = n_w = n_c = 0
        for _ in range(4000):
            k1, k2 = rng.choice(keys), rng.choice(keys)
            c1 = rng.choice(cells)
            if k1 != k2:
                diff_w += tokens[l][k1][c1] != tokens[l][k2][c1]; n_w += 1
            c2 = rng.choice(cells)
            if c2 != c1:
                diff_c += tokens[l][k1][c1] != tokens[l][k1][c2]; n_c += 1
        sens, pvar = diff_w / n_w, diff_c / n_c
        admitted[l] = sens >= SENS_MIN and pvar >= PROFVAR_MIN
        print(f"  {l:<3} sens={sens:.3f} profvar={pvar:.3f} -> "
              f"{'ADMITTED' if admitted[l] else 'EXCLUDED'}")

    # ---- pair evaluation: instance-level excess ----
    def pair_stats(x, y, crossed, subset=None):
        excs = []
        for key in (subset or keys):
            obs = n = 0
            for pi, r in cells:
                ry = (r + 1) % K_SEEDS if crossed else r
                obs += m1(tokens[x][key][(pi, r)], tokens[y][key][(pi, ry)]); n += 1
            obs /= n
            # analytic per-instance null from pooled marginals
            from collections import Counter
            cx = Counter(t for t in tokens[x][key].values() if t[0] in ('WC', 'WD'))
            cy = Counter(t for t in tokens[y][key].values() if t[0] in ('WC', 'WD'))
            tot = len(tokens[x][key])
            e0 = sum((cx[t] / tot) * (cy.get((m, v), 0) / tot)
                     for t in cx for m in ('WC', 'WD') for v in [t[1]]
                     if (m, v) in cy) if cx and cy else 0.0
            # exact same-token expectation: sum over wrong tokens of pX*pY
            e0 = sum((cx[t] / tot) * (cy[t2] / tot)
                     for t in cx for t2 in cy if t[1] == t2[1])
            excs.append(obs - e0)
        m = sum(excs) / len(excs)
        var = sum((e - m) ** 2 for e in excs) / max(len(excs) - 1, 1)
        se = (var / len(excs)) ** 0.5
        return m, se

    def verdict(x, y):
        if not (admitted[x] and admitted[y]):
            return None, None, None, None, 'INADMISSIBLE_PATH'
        em, sem = pair_stats(x, y, False)
        ec, sec = pair_stats(x, y, True)
        sig = lambda e, s: e > EXC_MIN and e > 2 * s
        if sig(em, sem) and sig(ec, sec): v = 'CONSTRUCTION_DEPENDENT'
        elif sig(em, sem): v = 'CONTACT_SCHEDULE_DEPENDENT'
        else: v = 'NO_CONSTRUCTION_DEPENDENCE'
        return em, sem, ec, sec, v

    pairs = [("A", "A'", 'clone'), ('A', 'G', 'isomorph'), ('A', 'P', 'indep'),
             ('G', 'P', 'indep'), ('Lr', 'Lp', 'attractor'),
             ('S1', 'S2', 'seed sham'), ('N', 'C', 'masked blindness')]
    print(f"\n{'pair':<9} {'type':<17} {'exc_m':>7} {'se':>6} {'exc_c':>7} "
          f"{'se':>6} | verdict")
    print('-' * 78)
    for x, y, typ in pairs:
        em, sem, ec, sec, v = verdict(x, y)
        if em is None:
            print(f"({x},{y})".ljust(9) + f"{typ:<17} {'—':>7} {'—':>6} "
                  f"{'—':>7} {'—':>6} | {v}")
        else:
            print(f"({x},{y})".ljust(9) + f"{typ:<17} {em:>7.3f} {sem:>6.3f} "
                  f"{ec:>7.3f} {sec:>6.3f} | {v}")

    # E6: per-stratum view of the masked pair (evaluated regardless of gate)
    print("\n(N,C) per-stratum matched excess (E6 prediction: wobble ~ 0):")
    for s in strata:
        sub = [(s, i) for i in range(R_INST)]
        em, sem = pair_stats('N', 'C', False, subset=sub)
        print(f"  {s:<10} exc={em:>7.3f} se={sem:.3f}")

if __name__ == '__main__':
    main()
