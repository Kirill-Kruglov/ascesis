"""
General-word world simulation for Experiment A integration.

Why this exists: the scouts' worlds evaluate only pure-power probes
(('R', k) tuples) for speed. The independently-built languages (Codex,
clean session) speak the interface of CODEX_SPEC.md — arbitrary words
over {R, L} and a CALL-count budget. Per PROVENANCE_PROTOCOL.md, Claude
may only write this thin adapter layer; the received logic is never
edited. This module therefore simulates every world state-by-state for
arbitrary words.

Also hosts the registered DEPENDENT sham `lang_G_translated`: an
order-finder DERIVED from lang_A by a fixed translation of its probe
schedule (the Cayley map as code) — the known-dependent genealogy against
which the independent build is contrasted.
"""
import random


class GWorld:
    """Base: subclasses define step_R / step_L on integer states."""
    eps = 0.0
    def run(self, word, bp=0):
        s = bp
        for ch in word:
            s = self.step_R(s) if ch == 'R' else self.step_L(s)
        return s
    def same(self, u, v, bp=0):
        return self.run(u, bp) == self.run(v, bp)


class GCycle(GWorld):
    def __init__(self, n, eps=0.0): self.n, self.eps, self.truth = n, eps, n
    def step_R(self, s): return (s + 1) % self.n
    def step_L(self, s): return (s - 1) % self.n
    def run(self, word, bp=0):          # count-based fast path (abelian)
        return (bp + word.count('R') - word.count('L')) % self.n


class GAliasCycle(GWorld):
    """Cycle(n); comparisons against the EMPTY word are blurred to mod q
    while the basepoint sits at the origin (same semantics as the scouts,
    restated for arbitrary words)."""
    def __init__(self, n, q): self.n, self.q, self.truth = n, q, n
    def step_R(self, s): return (s + 1) % self.n
    def step_L(self, s): return (s - 1) % self.n
    def run(self, word, bp=0):          # count-based fast path (abelian)
        return (bp + word.count('R') - word.count('L')) % self.n
    def same(self, u, v, bp=0):
        if (u == '' or v == '') and bp % self.n == 0:
            return (self.run(u, bp) - self.run(v, bp)) % self.q == 0
        return self.run(u, bp) == self.run(v, bp)


class GLollipop(GWorld):
    """Tail 0..t-1 into a cycle of c; L floors at 0 on the tail."""
    def __init__(self, t, c): self.t, self.c, self.truth = t, c, c
    def step_R(self, s):
        return s + 1 if s + 1 < self.t else self.t + (s + 1 - self.t) % self.c
    def step_L(self, s):
        if s == 0: return 0
        if s <= self.t: return s - 1
        return self.t + (s - 1 - self.t) % self.c


class GWobble(GWorld):
    """R honest n-cycle; L decrements but sticks at states <= 2."""
    def __init__(self, n): self.n, self.truth = n, n
    def step_R(self, s): return (s + 1) % self.n
    def step_L(self, s): return s if s <= 2 else s - 1


class GNonstationary(GWorld):
    """Modulus n1 until oracle query #switch, then n2 (query counter lives
    in the Oracle). Truth None: abstain is correct."""
    def __init__(self, n1, n2, switch):
        self.n1, self.n2, self.switch, self.truth = n1, n2, switch, None
        self._n = n1
    def set_query_index(self, qi): self._n = self.n1 if qi <= self.switch else self.n2
    def step_R(self, s): return (s + 1) % self._n
    def step_L(self, s): return (s - 1) % self._n
    def run(self, word, bp=0):          # count-based fast path (abelian)
        return (bp + word.count('R') - word.count('L')) % self._n


class GOracle:
    """CALL-budget oracle per CODEX_SPEC: raises BudgetExceeded past
    cap_calls; logs every emitted probe pair for the journal channel."""
    class BudgetExceeded(Exception): pass

    _TR = str.maketrans('RL', 'LR')

    def __init__(self, world, cap_calls, seed, bp=0, rev=False):
        self.w, self.cap, self.bp, self.rev = world, cap_calls, bp, rev
        self.rng = random.Random(seed)
        self.count = 0
        self.log = []

    def __call__(self, u, v):
        self.count += 1
        if self.count > self.cap: raise GOracle.BudgetExceeded()
        self.log.append((u, v))                      # as emitted (pre-rev)
        if self.rev:
            u, v = u.translate(GOracle._TR), v.translate(GOracle._TR)
        if isinstance(self.w, GNonstationary): self.w.set_query_index(self.count)
        b = self.w.same(u, v, self.bp)
        if self.w.eps and self.rng.random() < self.w.eps: b = not b
        return b


def run_language(fn, world, cap_calls, seed, bp=0, rev=False):
    """Uniform runner: budget exhaustion inside fn becomes ('TO',)."""
    orc = GOracle(world, cap_calls, seed, bp, rev)
    try:
        res = fn(orc, cap_calls, seed)
    except GOracle.BudgetExceeded:
        res = ('TO',)
    return res, orc.log


# ---- the registered DEPENDENT genealogy: G translated from A ---------------

def lang_A_general(oracle, cap_calls, seed):
    """A restated on the general interface: ascending origin scan."""
    k = 0
    while True:
        k += 1
        if oracle('R' * k, ''): return ('VAL', k, True)


def lang_G_translated(oracle, cap_calls, seed):
    """DERIVED FROM lang_A by a fixed schedule translation (the Cayley map
    as code): every A-probe (R^k, e) becomes the graph probe
    (R^{k+j}, R^j) with a cosmetic offset j — same effective information
    channel, geometric surface. This is the registered dependent sham of
    the two-genealogy design; its provenance is DECLARED dependent."""
    rng = random.Random(seed)
    k = 0
    while True:
        k += 1
        j = rng.randint(1, 3)
        if oracle('R' * (k + j), 'R' * j): return ('VAL', k, True)


if __name__ == '__main__':
    # smoke test: both genealogy-A builds find n; worlds behave
    for W, want in [(GCycle(17), 17), (GWobble(23), 23), (GLollipop(6, 12), None)]:
        ra, _ = run_language(lang_A_general, W, 400, 1)
        rg, _ = run_language(lang_G_translated, W, 400, 2)
        print(type(W).__name__, ra, rg)
