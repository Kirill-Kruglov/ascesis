"""
SCOUT 02 (phase 0, NOT citable): failure-profile coupling as the independence
measure — replacing zlib-NCD, which fell in scout 01-pre (volume confound).

Design move being tested:
  Path dependence is invisible inside one world (any competent journal pins n;
  conditional MI given the world is zero for deterministic languages). If
  shared blindness exists, it must show as CO-FAILURE ACROSS INTERVENTIONS:
  run the language bundle over a family of worlds that step outside the
  shared postulate's domain, and measure coupling of failure profiles.

World family (interventions preregistered here, before any run):
  - cyclic(n)          : the base world, Z/nZ. Truth: recurrent cycle n.
  - neighbor(n+1)      : the adjacent dead end. Truth: n+1.
  - lollipop(t, c)     : rho-shaped function world — tail of t states into a
                         cycle of c. NOT a group. Truth: recurrent cycle c.
  - noisy(n, eps)      : cyclic, oracle lies with prob eps per query.

Languages (each returns claimed wall m or None, plus #queries):
  - A  : algebra — ascending relation scan, first k with R^k = e.
  - A' : decorated clone of A — same effective channel, cosmetic padding
         probes whose answers are ignored. The implanted-blindness sham.
  - G  : geometry — pairwise collision scan, fundamental cycle length.
  - P  : probabilistic — random word pairs, positives double-checked
         (noise robustness), n inferred as gcd of positive net-differences.

Preregistered scout expectations (written before running):
  E1  coupling(A, A') = 1.0 exactly — the clone MUST read as dependent.
  E2  A and G agree on every group world (Cayley theorem) but DIVERGE on
      lollipop: A (blind: R^k(x0) never returns to a tail x0) says None,
      G finds c. The glue is visible only outside the group family.
  E3  under noise, scans (A, G) break while double-checking P survives —
      (A,P)/(G,P) decouple further.
  E4  neighbor worlds separate at destination level for all competent
      languages (no merging of adjacent dead ends).
  Kill for the instrument candidate: if the coupling ORDERING fails —
  clone <= isomorph, or isomorph <= independent — the measure does not
  track dependence and falls like NCD did.
"""
import random
from math import gcd

# ---------- worlds ----------

class Cyclic:
    def __init__(self, n): self.n, self.truth = n, n
    def run(self, word):
        s = 0
        for ch in word: s = (s + (1 if ch == 'R' else -1)) % self.n
        return s

class Lollipop:
    """States 0..t-1 tail, t..t+c-1 cycle. R advances; L undoes where unique."""
    def __init__(self, t, c): self.t, self.c, self.truth = t, c, c
    def _R(self, s):
        if s < self.t: return s + 1
        return self.t + ((s - self.t + 1) % self.c)
    def _L(self, s):
        if s == 0: return 0
        if s <= self.t: return s - 1            # tail predecessor (unique for s<t; s==t: choose tail? no:)
        return self.t + ((s - self.t - 1) % self.c)
    def run(self, word):
        s = 0
        for ch in word: s = self._R(s) if ch == 'R' else self._L(s)
        return s

class Oracle:
    def __init__(self, world, eps=0.0, seed=0):
        self.w, self.eps, self.rng, self.count = world, eps, random.Random(seed), 0
    def same(self, u, v):
        self.count += 1
        b = int(self.w.run(u) == self.w.run(v))
        if self.eps and self.rng.random() < self.eps: b = 1 - b
        return b

# ---------- languages ----------

def lang_A(orc, cap):
    for k in range(1, cap + 1):
        if orc.same('R' * k, ''): return k
    return None

def lang_A_clone(orc, cap, seed):
    """Same effective channel as A; padding probes are fired and ignored."""
    rng = random.Random(seed)
    for k in range(1, cap + 1):
        if rng.random() < 0.5:                       # cosmetic noise probe
            j = rng.randint(1, cap); orc.same('L' * j, 'R' * j)  # answer ignored
        if orc.same('R' * k, ''): return k
    return None

def lang_G(orc, cap):
    for k in range(1, cap + 1):
        for j in range(k):
            if orc.same('R' * k, 'R' * j): return k - j
    return None

def lang_P(orc, cap, seed, samples=400):
    rng = random.Random(seed)
    g = 0
    for _ in range(samples):
        a, b = rng.randint(0, cap), rng.randint(0, cap)
        if a == b: continue
        if orc.same('R' * a, 'R' * b) and orc.same('R' * a, 'R' * b):  # double-check
            g = gcd(g, abs(a - b))
            if g == 1: return 1
    return g or None

# ---------- run the bundle over the family ----------

def bundle(world, eps, base_seed):
    cap = 4 * getattr(world, 'truth', 30) + 20
    out = {}
    for name, fn in [('A',  lambda o: lang_A(o, cap)),
                     ('A\'', lambda o: lang_A_clone(o, cap, base_seed + 1)),
                     ('G',  lambda o: lang_G(o, cap)),
                     ('P',  lambda o: lang_P(o, cap, base_seed + 2))]:
        o = Oracle(world, eps, seed=base_seed)
        out[name] = fn(o)
    return out

def main():
    n = 24
    family = [
        ('cyclic(24)',      Cyclic(24),        0.0),
        ('neighbor(25)',    Cyclic(25),        0.0),
        ('lollipop(8,24)',  Lollipop(8, 24),   0.0),
        ('lollipop(15,17)', Lollipop(15, 17),  0.0),
        ('noisy(24,.05)',   Cyclic(24),        0.05),
        ('noisy(24,.15)',   Cyclic(24),        0.15),
    ]
    langs = ['A', 'A\'', 'G', 'P']
    profiles = {l: [] for l in langs}          # correctness vectors
    all_claims = {l: [] for l in langs}        # majority claims per world
    print(f"{'world':<16} {'truth':>5} | " + " ".join(f"{l:>6}" for l in langs))
    print("-" * 60)
    for wname, w, eps in family:
        # average over seeds for stochastic components
        claims = {l: [] for l in langs}
        for s in range(5):
            r = bundle(w, eps, 9000 + 37 * s)
            for l in langs: claims[l].append(r[l])
        row = {}
        for l in langs:
            vals = claims[l]
            maj = max(set(vals), key=vals.count)      # majority claim over seeds
            row[l] = maj
            all_claims[l].append(maj)
            profiles[l].append(int(maj == w.truth))
        print(f"{wname:<16} {w.truth:>5} | " +
              " ".join(f"{str(row[l]):>6}" for l in langs))
    print("\ncorrectness profiles over the family:")
    for l in langs: print(f"  {l:<3} {profiles[l]}")
    print("\npairwise coupling (fraction of worlds with SAME correctness):")
    from itertools import combinations
    for a, b in combinations(langs, 2):
        c = sum(x == y for x, y in zip(profiles[a], profiles[b])) / len(profiles[a])
        print(f"  ({a},{b}): {c:.2f}")

    # --- refinement discovered on first run (recorded, not retro-hidden):
    # co-success measures the world's credit, not the paths'. Dependence must
    # be read from CO-FAILURES only: same wrong claim, where both are wrong.
    print("\nco-failure coupling (same wrong claim | both wrong):")
    for a, b in combinations(langs, 2):
        both_wrong = [(ca, cb) for ca, cb, wa, wb in
                      zip(all_claims[a], all_claims[b], profiles[a], profiles[b])
                      if wa == 0 and wb == 0]
        if not both_wrong:
            print(f"  ({a},{b}): n/a (never co-fail)")
        else:
            same = sum(ca == cb for ca, cb in both_wrong) / len(both_wrong)
            print(f"  ({a},{b}): {same:.2f}  over {len(both_wrong)} co-failure worlds")

if __name__ == '__main__':
    main()
