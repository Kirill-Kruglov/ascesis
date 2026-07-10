"""
SCOUT 04 (phase 0, NOT citable): instrument v1 — counterfactual profiles +
per-instance null + seed-decorrelation control. Built to the Codex v1-attack
spec after scout 03 killed v0.

v1 core (amended per Codex):
  - NOT "no deterministic path enters triangulation" but "no path WITHOUT A
    COUNTERFACTUAL PROFILE enters triangulation". A deterministic language
    gets its profile from a fixed, preregistered ensemble of world
    perturbations (basepoint shift, generator reversal, budget +/-, noise
    reseed) that preserve ground truth but move the contact path.
  - Floor-1 null is PER-INSTANCE: tokens pooled over (perturbation, seed)
    within one world instance; matched-run coupling above this null =
    candidate construction dependence. World difficulty is thereby
    conditioned out (fixes scout 03's common-cause leak).
  - Seed-decorrelation control (Codex S1): construction dependence must
    SURVIVE crossing the languages' internal seeds. Dependence that dies
    under crossed seeds is contact-schedule dependence, not path dependence.
  - Deliberate seed-sharing sham: languages Sch1/Sch2 share their probe
    schedule PRNG (same salt) with different probe semantics.

Verdict rule (fixed before run; sig = p < 0.05 AND excess > 0.05, on M1 =
same wrong value):
  CONSTRUCTION_DEPENDENT      iff sig(matched) and sig(crossed)
  CONTACT_SCHEDULE_DEPENDENT  iff sig(matched) and not sig(crossed)
  NO_CONSTRUCTION_DEPENDENCE  otherwise

Preregistered expectations (before running):
  E1 (A,A') clone           -> CONSTRUCTION_DEPENDENT (seed-insensitive).
                               KILL v1 if not.
  E2 (Lr,Lp) attractor sham -> NO_CONSTRUCTION_DEPENDENCE (per-instance
                               null absorbs grid attractor + world params;
                               this is exactly where v0 fell). KILL if not.
  E3 (Sch1,Sch2) seed sham  -> CONTACT_SCHEDULE_DEPENDENT (matched excess
                               dies under crossing). KILL if read as
                               CONSTRUCTION_DEPENDENT.
  E4 (A,G) isomorph         -> intermediate; prereg only the ordering
                               exc_matched: (A,A') > (A,G) > (A,P) ~ 0.
                               Verdict recorded, not presumed.
  E5 (A,P),(G,P) indep      -> NO_CONSTRUCTION_DEPENDENCE.
  E6 determinism gate       -> E1 must be achieved although A/A' ignore
                               their RNG: deterministic paths are admissible
                               via perturbation-generated profiles.
Scope note (recorded, not silent): Codex shams S2 (stochastically masked
shared blindness / TwoAliasLollipop) and the GatedLollipop mode-split world
are deferred to scout 05. v1 passing scout 04 does NOT clear those.
"""
import random
from math import gcd
from itertools import product

CAP0 = 180
R_INST = 6
K_SEEDS = 3
B_NULL = 600

# ---------- worlds (probes are ('R', k) / ('L', k); closed-form endpoints) ---

def _net(p):
    d, k = p
    return k if d == 'R' else -k

class CycleW:
    def __init__(self, n, eps=0.0): self.n, self.eps, self.truth = n, eps, n
    def same(self, p, q, bp):
        return (_net(p) - _net(q)) % self.n == 0

class AliasCycleW:
    """Cycle(n); the ORIGIN STATE echoes states = 0 mod q: comparisons where
    one probe is length-0 are blurred to mod q — but only while the basepoint
    sits at the origin. A basepoint shift breaks the blur (truth preserved)."""
    def __init__(self, n, q): self.n, self.q, self.eps, self.truth = n, q, 0.0, n
    def same(self, p, qq, bp):
        blur = (p[1] == 0 or qq[1] == 0) and bp % self.n == 0
        return (_net(p) - _net(qq)) % (self.q if blur else self.n) == 0

class LollipopW:
    """Tail 0..t-1 into cycle of c; L floors at 0 on the tail. Basepoint
    shifts stay in the tail (t >= 5, shifts <= 3). Truth: recurrent c."""
    def __init__(self, t, c): self.t, self.c, self.eps, self.truth = t, c, 0.0, c
    def _end(self, p, bp):
        d, k = p
        if d == 'L': return max(bp - k, 0)
        pos = bp + k
        return pos if pos < self.t else self.t + (pos - self.t) % self.c
    def same(self, p, q, bp): return self._end(p, bp) == self._end(q, bp)

class NonstationaryW:
    """Modulus n1 until oracle query #switch, then n2. Truth None (ABSTAIN)."""
    def __init__(self, n1, n2, switch):
        self.n1, self.n2, self.switch, self.eps, self.truth = n1, n2, switch, 0.0, None
        self.count = 0
    def same(self, p, q, bp):
        self.count += 1
        n = self.n1 if self.count <= self.switch else self.n2
        return (_net(p) - _net(q)) % n == 0

def fresh(w):
    if isinstance(w, NonstationaryW):
        return NonstationaryW(w.n1, w.n2, w.switch)
    return w

# ---------- perturbation ensemble (fixed, truth-preserving) ------------------

PERTS = [  # (name, basepoint, reverse, d_budget, d_noise_seed)
    ('id',    0, False, 0,   0),
    ('bp+1',  1, False, 0,   0),
    ('bp+3',  3, False, 0,   0),
    ('rev',   0, True,  0,   0),
    ('bud-',  0, False, -15, 0),
    ('bud+',  0, False, +15, 0),
    ('nseed', 0, False, 0,   1),
]

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

# ---------- languages: fn(orc, cap, rng) -> ('VAL', v, conf)|('AB',)|('TO',) -

def lang_A(orc, cap, rng):
    for k in range(1, cap + 1):
        if orc.same(('R', k), ('R', 0)): return ('VAL', k, True)
    return ('TO',)

def lang_A_clone(orc, cap, rng):
    for k in range(1, cap + 1):
        if rng.random() < 0.5:
            j = rng.randint(1, cap); orc.same(('L', j), ('R', j))   # ignored
        if orc.same(('R', k), ('R', 0)): return ('VAL', k, True)
    return ('TO',)

def lang_G(orc, cap, rng):
    for k in range(1, cap + 1):
        for j in range(k):
            if orc.same(('R', k), ('R', j)): return ('VAL', k - j, True)
    return ('TO',)

def lang_P(orc, cap, rng, samples=300):
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
    return ('VAL', 2, True)                       # confident fallback (wrong)

def lang_Sch2(orc, cap, rng):
    ks = [rng.randint(1, cap) for _ in range(25)]  # same stream if same seed
    hits = [k for k in ks if orc.same(('L', k + 2), ('L', 2))]
    if hits:
        g = 0
        for h in hits: g = gcd(g, h)
        return ('VAL', g, True)
    return ('VAL', 2, True)

LANGS = {'A': lang_A, "A'": lang_A_clone, 'G': lang_G, 'P': lang_P,
         'Lr': lang_Lr, 'Lp': lang_Lp, 'S1': lang_Sch1, 'S2': lang_Sch2}
# distinct salts; the Sch pair DELIBERATELY shares one (the S1 sham)
SALT = {'A': 11, "A'": 23, 'G': 37, 'P': 51, 'Lr': 67, 'Lp': 83,
        'S1': 99, 'S2': 99}

# ---------- strata ------------------------------------------------------------

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

# ---------- run ----------------------------------------------------------------

def main():
    master = random.Random(20260710)
    strata = make_strata(master)
    # tokens[lang][(stratum, inst)][(pert_idx, seed_idx)] = token
    tokens = {l: {} for l in LANGS}
    for sname, insts in strata.items():
        for i, w in enumerate(insts):
            for l in LANGS: tokens[l][(sname, i)] = {}
            for pi, pert in enumerate(PERTS):
                cap = CAP0 + pert[3]
                for r in range(K_SEEDS):
                    oseed = 7000 + 13 * i + 5 * pi
                    for lname, fn in LANGS.items():
                        orc = Oracle(w, pert, oseed)
                        lrng = random.Random(10007 * r + SALT[lname])
                        tokens[lname][(sname, i)][(pi, r)] = \
                            classify(fn(orc, cap, lrng), w.truth)

    keys = [(s, i) for s in strata for i in range(R_INST)]
    cells = [(pi, r) for pi in range(len(PERTS)) for r in range(K_SEEDS)]

    def coupling(x, y, crossed):
        vals = []
        for key in keys:
            for pi, r in cells:
                ry = (r + 1) % K_SEEDS if crossed else r
                vals.append(m1(tokens[x][key][(pi, r)], tokens[y][key][(pi, ry)]))
        return sum(vals) / len(vals)

    def null_dist(x, y, rng):
        out = []
        pools = {key: (list(tokens[x][key].values()), list(tokens[y][key].values()))
                 for key in keys}
        for _ in range(B_NULL):
            acc = n = 0
            for key in keys:
                px, py = pools[key]
                for _ in range(len(cells)):
                    acc += m1(rng.choice(px), rng.choice(py)); n += 1
            out.append(acc / n)
        return out

    pairs = [("A", "A'", 'clone'), ('A', 'G', 'isomorph'), ('A', 'P', 'indep'),
             ('G', 'P', 'indep'), ('Lr', 'Lp', 'attractor sham'),
             ('S1', 'S2', 'seed sham')]
    nrng = random.Random(424242)
    print(f"{'pair':<10} {'type':<15} {'matched':>8} {'crossed':>8} {'null':>7} "
          f"{'excM':>7} {'pM':>6} {'excC':>7} {'pC':>6} | verdict")
    print('-' * 100)
    for x, y, typ in pairs:
        om, oc = coupling(x, y, False), coupling(x, y, True)
        null = null_dist(x, y, nrng)
        nm = sum(null) / len(null)
        pm = (1 + sum(d >= om for d in null)) / (len(null) + 1)
        pc = (1 + sum(d >= oc for d in null)) / (len(null) + 1)
        em, ec = om - nm, oc - nm
        sig = lambda e, p: p < 0.05 and e > 0.05
        if sig(em, pm) and sig(ec, pc): v = 'CONSTRUCTION_DEPENDENT'
        elif sig(em, pm): v = 'CONTACT_SCHEDULE_DEPENDENT'
        else: v = 'NO_CONSTRUCTION_DEPENDENCE'
        print(f"({x},{y})".ljust(10) + f"{typ:<15} {om:>8.3f} {oc:>8.3f} {nm:>7.3f} "
              f"{em:>7.3f} {pm:>6.3f} {ec:>7.3f} {pc:>6.3f} | {v}")

if __name__ == '__main__':
    main()
