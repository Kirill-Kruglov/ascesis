"""
SCOUT 03 (phase 0, NOT citable): the Codex adversarial gate for the
failure-profile coupling instrument.

Implements the Codex (GPT 5.5) attack spec verbatim where possible:
  - failure tokens: SUCCESS / ABSTAIN / WRONG_CONFIDENT(v) / WRONG_DEGRADED(v) / TIMEOUT
  - sham (a): two causally independent languages sharing a small hypothesis
    grid H -> common error attractor -> raw co-failure high, must be
    explained away by the marginal null (verdict NO_DEPENDENCE).
  - sham (b): two languages sharing one blind postulate (trust the
    origin-return channel) with SPLIT surface modes (one lies with a value,
    the other abstains after failed verification).
  - null arm: per-stratum marginal token distributions, Monte Carlo
    independent resampling, excess + p-value; UNKNOWN if unidentifiable.
  - metrics M1..M4, fixed verdict rule, no learned weights.

Design amendment forced by analysis BEFORE running (recorded, not post-hoc):
  Deterministic languages have point-mass marginals on a fixed world, so a
  per-world null absorbs ALL dependence (even the clone's). Remedy adopted:
  STRATA WITH RANDOMIZED WORLD PARAMETERS (n, q, eps drawn per instance).
  Then clone value-coupling exceeds the pooled-marginal null (wrong values
  track the varying world), while sham-(a) attractor values (which track the
  fixed grid H, not the world) stay at null level.

Preregistered expectations (before running):
  E1 (A,A')  clone:      M1 excess HIGH, p<.05  -> SEMANTIC_DEPENDENCE.
                          KILL if not.
  E2 (Lr,Lp) sham-a:     raw M1 may be high; excess ~ 0 -> NO_DEPENDENCE.
                          KILL if SEMANTIC_DEPENDENCE.
  E3 (A,Acert) sham-b:   EXPECTED FALL of instrument v0: with deterministic
                          languages the stratum marginal likely explains the
                          WC/AB mode split entirely -> v0 reads NO_DEPENDENCE
                          where SHARED_BLIND_SPOT_SPLIT_MODE is true.
                          If it falls: finding = "v0 cannot see split-mode
                          shared blindness in deterministic paths"; candidate
                          next iteration = mandatory stochastization of every
                          language (probe-order jitter) so per-instance
                          marginals become estimable.
  E4 ordering:            M1_excess(A,A') > M1_excess(A,G) > M1_excess(A,P).
                          (A,G) shares the sequential-scan postulate and the
                          origin channel; expected between clone and indep.
  E5 (A,P),(G,P):        NO_DEPENDENCE.

Thresholds (fixed before run): significant = p < 0.05 AND excess > 0.05.
R = 8 instances per stratum; B = 1000 null draws; cap = 180 (fixed, does
not leak n). Verdict UNKNOWN if R < 5.
"""
import random
from math import gcd

CAP = 180
R_INSTANCES = 8
B_NULL = 1000
H_GRID = [2, 3, 4, 5, 6, 8, 10, 12]

# ---------- worlds: probes are ('R', k) or ('L', k); closed-form endpoints ----

class CycleW:
    kind = 'cycle'
    def __init__(self, n, eps=0.0): self.n, self.eps, self.truth = n, eps, n
    def same(self, p, q):
        (d1, k1), (d2, k2) = p, q
        v1 = k1 if d1 == 'R' else -k1
        v2 = k2 if d2 == 'R' else -k2
        return (v1 - v2) % self.n == 0

class AliasCycleW:
    """True Cycle(n); comparisons against a length-0 word are blurred to mod q."""
    kind = 'alias'
    def __init__(self, n, q): self.n, self.q, self.eps, self.truth = n, q, 0.0, n
    def same(self, p, qq):
        (d1, k1), (d2, k2) = p, qq
        v1 = k1 if d1 == 'R' else -k1
        v2 = k2 if d2 == 'R' else -k2
        mod = self.q if (k1 == 0 or k2 == 0) else self.n
        return (v1 - v2) % mod == 0

class LollipopW:
    """Tail t into cycle c; R-power endpoints in closed form; truth = c."""
    kind = 'lollipop'
    def __init__(self, t, c): self.t, self.c, self.eps, self.truth = t, c, 0.0, c
    def _end(self, d, k):
        if d == 'L': return 0                      # L from origin stays at 0
        return k if k < self.t else self.t + (k - self.t) % self.c
    def same(self, p, q):
        return self._end(*p) == self._end(*q)

class NonstationaryW:
    """Modulus n1 until the oracle's query #switch, then n2. Truth: no single
    wall -> correct answer is ABSTAIN (truth=None)."""
    kind = 'nonstat'
    def __init__(self, n1, n2, switch):
        self.n1, self.n2, self.switch, self.eps, self.truth = n1, n2, switch, 0.0, None
        self.count = 0
    def same(self, p, q):
        self.count += 1
        n = self.n1 if self.count <= self.switch else self.n2
        (d1, k1), (d2, k2) = p, q
        v1 = k1 if d1 == 'R' else -k1
        v2 = k2 if d2 == 'R' else -k2
        return (v1 - v2) % n == 0

class Oracle:
    def __init__(self, world, seed):
        self.w, self.rng = world, random.Random(seed)
    def same(self, p, q):
        b = self.w.same(p, q)
        if self.w.eps and self.rng.random() < self.w.eps: b = not b
        return b

# ---------- languages: return ('VAL', v, confident) | ('AB',) | ('TO',) ------

def lang_A(orc, rng):
    for k in range(1, CAP + 1):
        if orc.same(('R', k), ('R', 0)): return ('VAL', k, True)
    return ('TO',)

def lang_A_clone(orc, rng):
    for k in range(1, CAP + 1):
        if rng.random() < 0.5:
            j = rng.randint(1, CAP); orc.same(('L', j), ('R', j))   # ignored
        if orc.same(('R', k), ('R', 0)): return ('VAL', k, True)
    return ('TO',)

def lang_G(orc, rng):
    for k in range(1, CAP + 1):
        for j in range(k):
            if orc.same(('R', k), ('R', j)): return ('VAL', k - j, True)
    return ('TO',)

def lang_P(orc, rng, samples=300):
    g, npos = 0, 0
    for _ in range(samples):
        a, b = rng.randint(0, CAP), rng.randint(0, CAP)
        if a == b: continue
        if orc.same(('R', a), ('R', b)) and orc.same(('R', a), ('R', b)):
            g = gcd(g, abs(a - b)); npos += 1
    if npos == 0: return ('TO',)
    return ('VAL', g, npos >= 4)

def lang_A_cert(orc, rng):
    """Shares A's origin-return postulate and scan; verifies before claiming."""
    for k in range(1, CAP + 1):
        if orc.same(('R', k), ('R', 0)):
            ok = all(orc.same(('R', k + j), ('R', j)) for j in (1, 2, 3))
            return ('VAL', k, True) if ok else ('AB',)
    return ('TO',)

def _grid_min(compat):
    c = [h for h in H_GRID if compat(h)]
    return ('VAL', min(c), True) if c else ('AB',)

def lang_Lr(orc, rng):
    obs = {}
    for _ in range(12):
        k = rng.randint(1, 14); obs[k] = orc.same(('R', k), ('R', 0))
    return _grid_min(lambda h: all((k % h == 0) == r for k, r in obs.items()))

def lang_Lp(orc, rng):
    obs = []
    for _ in range(12):
        a, b = rng.randint(0, 20), rng.randint(0, 20)
        if a == b: continue
        obs.append((abs(a - b), orc.same(('R', a), ('R', b))))
    return _grid_min(lambda h: all((d % h == 0) == r for d, r in obs))

LANGS = {'A': lang_A, "A'": lang_A_clone, 'G': lang_G, 'P': lang_P,
         'Ac': lang_A_cert, 'Lr': lang_Lr, 'Lp': lang_Lp}

# ---------- strata with randomized world parameters -------------------------

def make_strata(rng):
    strata = {}
    strata['S0_cycle'] = [CycleW(rng.randint(17, 40)) for _ in range(R_INSTANCES)]
    strata['S0p_prime'] = [CycleW(rng.choice([29, 31, 37, 41, 43, 47]))
                           for _ in range(R_INSTANCES)]
    def alias():
        n = rng.choice([20, 24, 28, 30, 36, 40])
        q = rng.choice([d for d in range(4, n // 2 + 1) if n % d == 0])
        return AliasCycleW(n, q)
    strata['S1_alias'] = [alias() for _ in range(R_INSTANCES)]
    strata['S2_lollipop'] = [LollipopW(rng.randint(5, 15), rng.randint(15, 30))
                             for _ in range(R_INSTANCES)]
    strata['S3_nonstat'] = [NonstationaryW(rng.randint(17, 30),
                                           rng.randint(31, 44),
                                           rng.randint(100, 250))
                            for _ in range(R_INSTANCES)]
    strata['S4_noisy'] = [CycleW(rng.randint(17, 40), eps=rng.uniform(0.02, 0.2))
                          for _ in range(R_INSTANCES)]
    return strata

# ---------- token classification --------------------------------------------

def classify(claim, truth):
    if claim[0] == 'VAL':
        _, v, conf = claim
        if truth is not None and v == truth: return ('S', v)
        return ('WC', v) if conf else ('WD', v)
    if claim[0] == 'AB':
        return ('S', 'AB') if truth is None else ('AB', None)
    return ('TO', None)

def nonsucc(t): return t[0] != 'S'

def m_stats(tx, ty):
    m1 = int(tx[0] in ('WC', 'WD') and ty[0] in ('WC', 'WD') and tx[1] == ty[1])
    m3 = int(nonsucc(tx) and nonsucc(ty))
    m2 = int(m3 and tx[0] == ty[0])
    m4 = int(m3 and tx[0] != ty[0])
    return m1, m2, m3, m4

# ---------- run --------------------------------------------------------------

def main():
    master = random.Random(20260710)
    strata = make_strata(master)
    # tokens[lang][stratum] = list over instances (matched: same instance index)
    tokens = {l: {s: [] for s in strata} for l in LANGS}
    for sname, instances in strata.items():
        for i, proto in enumerate(instances):
            for lname, fn in LANGS.items():
                # fresh world copy for nonstationary (stateful counter)
                w = proto
                if isinstance(proto, NonstationaryW):
                    w = NonstationaryW(proto.n1, proto.n2, proto.switch)
                orc = Oracle(w, seed=7000 + 13 * i)
                lrng = random.Random(5000 + 997 * i + hash(lname) % 1000)
                tokens[lname][sname].append(classify(fn(orc, lrng), proto.truth))

    def observed(x, y):
        vals = [m_stats(tx, ty) for s in strata
                for tx, ty in zip(tokens[x][s], tokens[y][s])]
        n = len(vals)
        return [sum(v[i] for v in vals) / n for i in range(4)]

    def null_dist(x, y, rng):
        out = []
        for _ in range(B_NULL):
            acc = [0, 0, 0, 0]; n = 0
            for s in strata:
                px, py = tokens[x][s], tokens[y][s]
                for _ in range(len(px)):
                    st = m_stats(rng.choice(px), rng.choice(py))
                    for i in range(4): acc[i] += st[i]
                    n += 1
            out.append([a / n for a in acc])
        return out

    def verdict(obs, null):
        means = [sum(d[i] for d in null) / len(null) for i in range(4)]
        exc = [obs[i] - means[i] for i in range(4)]
        pv = [(1 + sum(d[i] >= obs[i] for d in null)) / (len(null) + 1)
              for i in range(4)]
        sig = lambda i: pv[i] < 0.05 and exc[i] > 0.05
        if R_INSTANCES < 5: v = 'UNKNOWN'
        elif sig(0): v = 'SEMANTIC_DEPENDENCE'
        elif sig(2) and sig(3): v = 'SHARED_BLIND_SPOT_SPLIT_MODE'
        else: v = 'NO_DEPENDENCE'
        return exc, pv, v

    pairs = [("A", "A'", 'clone'), ('A', 'G', 'isomorph'), ('A', 'P', 'indep'),
             ('G', 'P', 'indep'), ('Lr', 'Lp', 'sham-a attractor'),
             ('A', 'Ac', 'sham-b split-mode')]
    nrng = random.Random(31337)
    print(f"{'pair':<10} {'type':<20} {'M1 obs':>7} {'M1 exc':>7} {'p':>6} | "
          f"{'M3 exc':>7} {'M4 exc':>7} | verdict")
    print('-' * 92)
    for x, y, typ in pairs:
        obs = observed(x, y)
        exc, pv, v = verdict(obs, null_dist(x, y, nrng))
        print(f"({x},{y})".ljust(10) + f"{typ:<20} {obs[0]:>7.3f} {exc[0]:>7.3f} "
              f"{pv[0]:>6.3f} | {exc[2]:>7.3f} {exc[3]:>7.3f} | {v}")

    print("\nper-stratum token sample (instance 0):")
    for s in strata:
        row = " ".join(f"{l}:{tokens[l][s][0][0]}"
                       f"{'' if tokens[l][s][0][1] is None else ':' + str(tokens[l][s][0][1])}"
                       for l in LANGS)
        print(f"  {s:<12} {row}")

if __name__ == '__main__':
    main()
