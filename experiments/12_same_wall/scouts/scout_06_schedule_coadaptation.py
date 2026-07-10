"""
SCOUT 06 (phase 0, NOT citable): the mode-split debt, transformed — schedule
CO-ADAPTATION as the postulate channel. The journal detector, literally.

Why the transformation (recorded before running): designing Codex's
GatedLollipop mode-split exposed a head-on collision between two of his own
rules. The S1 rule says "dependence that dies under seed decorrelation is
contact-schedule, not path". But a postulate-sharing pair's probe schedule
IS its postulate — and also dies under crossing. Same signature, opposite
required verdicts. The distinguisher: a cosmetic shared schedule is STATIC
across world perturbations; a postulate-driven schedule CO-ADAPTS — perturb
the world and the postulate moves both languages' probe sequences the same
way. So the channel must read the JOURNALS (probe sequences), not tokens:
the line's own founding move (read pi, not h_t) arriving inside the
instrument.

Metric M6 (fixed): for each (instance i, seed r), language X emits a probe
sequence at each perturbation e. d_X(e,e') = 1 - LCP/maxlen over the 21
perturbation pairs — X's world-response fingerprint. Residualize against
the language pool (removes the universal "everyone reacts to rev" common
cause), then Pearson-correlate residual fingerprints of X and Y; average
over r, instance-level mean +/- se. Significant iff M6 > 0.30 AND > 2*se.

World for the postulate pair: GatedLollipop(t, c, gate) — tail into cycle;
queries touching the junction region (states t-1, t, t+1) are flipped with
prob gate (per instance, 0.05..0.45). Truth None (junction breaks any
single-m prediction; abstain is correct). N2 finds the local cycle and
confirms by re-walking (junction-crossing checks), grading WC/WD/AB by
confirmation rate; C2 shares the identical scan-and-confirm postulate but
never exceeds WD. Their probe schedules are postulate-determined and must
co-adapt.

Preregistered expectations (before running):
  E1 (N2,C2) postulate pair -> M6 significant (the S2 gate finally passes
                               positively: verdict must not be "independent").
                               KILL of the channel if M6 ~ 0.
  E2 (S1,S2) cosmetic pair  -> M6 ~ 0 (schedules static across e): the
                               collision resolved — cosmetic vs postulate
                               separated. KILL if M6 significant.
  E3 (A,A') clone           -> M6 significant (identical stop-point response).
  E4 (A,P)                  -> M6 ~ 0.
  E5 (N,C) coin-masked pair -> uncertain after residualization; report
                               honestly. If still ~ 0: the coin-masked
                               binary postulate remains invisible — the
                               measured in-principle limit stands.

FIX AFTER FIRST RUN (recorded, not hidden). The first build fell on three
artifacts, all visible in its output: (i) probes were logged AFTER the
oracle's rev transformation, injecting the world's response into every
fingerprint (cosmetic pair scored 1.000); (ii) residualizing against a
clustered language pool manufactured spurious correlations (A,P = -0.66);
(iii) the channel itself lacked the seed-crossing control. v2 of the
metric: log probes AS EMITTED by the language (a static schedule then
yields a zero shift-vector by construction), drop residualization, and
report matched AND crossed correlations. Amended verdict rule (fixed):
co-adaptation = sig(matched) AND sig(crossed); cosmetic = sig(matched)
only; world-floor pairs (A,N2) reported as the empirical common-cause
reference, not tested against.
"""
import random
from math import gcd

CAP0 = 180
R_INST = 6
K_SEEDS = 6
M6_MIN = 0.30

def _net(p): return p[1] if p[0] == 'R' else -p[1]

class CycleW:
    def __init__(self, n, eps=0.0): self.n, self.eps, self.truth = n, eps, n
    def same(self, p, q, bp, rng): return (_net(p) - _net(q)) % self.n == 0

class AliasCycleW:
    def __init__(self, n, q): self.n, self.q, self.eps, self.truth = n, q, 0.0, n
    def same(self, p, qq, bp, rng):
        blur = (p[1] == 0 or qq[1] == 0) and bp % self.n == 0
        return (_net(p) - _net(qq)) % (self.q if blur else self.n) == 0

class WobbleCycleW:
    def __init__(self, n): self.n, self.eps, self.truth = n, 0.0, n
    def _end(self, p, bp):
        d, k = p
        if d == 'R': return (bp + k) % self.n
        return bp if bp <= 2 else max(bp - k, 2)
    def same(self, p, q, bp, rng): return self._end(p, bp) == self._end(q, bp)

class GatedLollipopW:
    def __init__(self, t, c, gate):
        self.t, self.c, self.gate, self.eps, self.truth = t, c, gate, 0.0, None
    def _end(self, p, bp):
        d, k = p
        if d == 'L': return max(bp - k, 0)
        pos = bp + k
        return pos if pos < self.t else self.t + (pos - self.t) % self.c
    def same(self, p, q, bp, rng):
        e1, e2 = self._end(p, bp), self._end(q, bp)
        b = e1 == e2
        junction = {self.t - 1, self.t, self.t + 1}
        if (e1 in junction or e2 in junction) and rng.random() < self.gate:
            b = not b
        return b

class Oracle:
    def __init__(self, world, pert, seed):
        _, bp, rev, dbud, dn = pert
        self.w, self.bp, self.rev = world, bp, rev
        self.rng = random.Random(seed + 977 * dn)
        self.eps = world.eps
        self.log = []
    def same(self, p, q):
        # journal logs the probe AS EMITTED by the language (pre-rev):
        # the fingerprint must reflect the language's schedule choices,
        # not the oracle's transformation of them (v2 fix i)
        self.log.append((1 if p[0] == 'R' else 0, p[1],
                         1 if q[0] == 'R' else 0, q[1]))
        if self.rev:
            p = ('L' if p[0] == 'R' else 'R', p[1])
            q = ('L' if q[0] == 'R' else 'R', q[1])
        b = self.w.same(p, q, self.bp, self.rng)
        if self.eps and self.rng.random() < self.eps: b = not b
        return b

PERTS = [('id', 0, False, 0, 0), ('bp+1', 1, False, 0, 0), ('bp+3', 3, False, 0, 0),
         ('rev', 0, True, 0, 0), ('bud-', 0, False, -15, 0),
         ('bud+', 0, False, +15, 0), ('nseed', 0, False, 0, 1)]

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

def lang_P(orc, cap, rng, samples=200):
    g, npos = 0, 0
    for _ in range(samples):
        a, b = rng.randint(0, cap), rng.randint(0, cap)
        if a == b: continue
        if orc.same(('R', a), ('R', b)) and orc.same(('R', a), ('R', b)):
            g = gcd(g, abs(a - b)); npos += 1
    if npos == 0: return ('TO',)
    return ('VAL', g, npos >= 4)

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
    ch = rng.choice(['R', 'L'])
    for k in range(1, cap + 1):
        if orc.same((ch, k), (ch, 0)): return ('VAL', k, True)
    return ('TO',)

def lang_C(orc, cap, rng):
    ch = rng.choice(['R', 'L'])
    other = 'L' if ch == 'R' else 'R'
    for k in range(1, cap + 1):
        if orc.same((ch, k), (ch, 0)):
            if orc.same((other, k), (other, 0)): return ('VAL', k, True)
            return ('AB',)
    return ('TO',)

def _scan_confirm(orc):
    """The shared postulate: find the local cycle pairwise, confirm by
    re-walking it (junction-crossing checks). Returns (m, conf) or None."""
    m = k0 = None
    for k in range(1, 60):
        for j in range(k):
            if orc.same(('R', k), ('R', j)): m, k0 = k - j, j; break
        if m: break
    if not m: return None
    conf = sum(orc.same(('R', k0 + i * m), ('R', k0)) for i in range(1, 7)) / 6
    return m, conf

def lang_N2(orc, cap, rng):
    r = _scan_confirm(orc)
    if r is None: return ('TO',)
    m, conf = r
    if conf > 0.6: return ('VAL', m, True)
    if conf > 0.3: return ('VAL', m, False)
    return ('AB',)

def lang_C2(orc, cap, rng):
    r = _scan_confirm(orc)
    if r is None: return ('TO',)
    m, conf = r
    if conf == 1.0: return ('VAL', m, False)      # never fully confident
    return ('AB',)

LANGS = {'A': lang_A, "A'": lang_A_clone, 'P': lang_P, 'S1': lang_Sch1,
         'S2': lang_Sch2, 'N': lang_N, 'C': lang_C, 'N2': lang_N2, 'C2': lang_C2}
SALT = {'A': 11, "A'": 23, 'P': 51, 'S1': 99, 'S2': 99, 'N': 131, 'C': 149,
        'N2': 173, 'C2': 191}

def make_strata(rng):
    def alias():
        n = rng.choice([20, 24, 28, 30, 36, 40])
        q = rng.choice([d for d in range(4, n // 2 + 1) if n % d == 0])
        return AliasCycleW(n, q)
    return {
        'cycle':  [CycleW(rng.randint(28, 44)) for _ in range(R_INST)],
        'alias':  [alias() for _ in range(R_INST)],
        'wobble': [WobbleCycleW(rng.randint(28, 44)) for _ in range(R_INST)],
        'gated':  [GatedLollipopW(rng.randint(5, 15), rng.randint(15, 30),
                                  rng.uniform(0.05, 0.45)) for _ in range(R_INST)],
    }

# ---------- M6: schedule co-adaptation ---------------------------------------

def lcp_dist(a, b):
    n = min(len(a), len(b))
    i = 0
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
    master = random.Random(20260710)
    strata = make_strata(master)
    keys = [(s, i) for s in strata for i in range(R_INST)]
    # v3 fix (recorded): fingerprints over WORLD-side perturbations only.
    # bud+/- change cap — a parameter of the LANGUAGE's contact budget, not
    # of the world; any cap-consuming language redraws its schedule at those
    # cells, a shared response that let the cosmetic pair survive crossing.
    # W -> I -> L, a third time, now inside the perturbation ensemble.
    WORLD_PERTS = [i for i, p in enumerate(PERTS) if p[3] == 0]
    epairs = [(a, b) for ai, a in enumerate(WORLD_PERTS)
              for b in WORLD_PERTS[ai + 1:]]
    # journals[lang][key][(pi, r)] = probe sequence
    journals = {l: {k: {} for k in keys} for l in LANGS}
    for sname, insts in strata.items():
        for i, w in enumerate(insts):
            for pi, pert in enumerate(PERTS):
                cap = CAP0 + pert[3]
                for r in range(K_SEEDS):
                    oseed = 7000 + 13 * i + 5 * pi + 1009 * r
                    for lname, fn in LANGS.items():
                        orc = Oracle(w, pert, oseed)
                        fn(orc, cap, random.Random(10007 * r + SALT[lname]))
                        journals[lname][(sname, i)][(pi, r)] = orc.log

    # fingerprints: fp[lang][key][r] = vector over epairs of lcp_dist
    fp = {l: {k: {} for k in keys} for l in LANGS}
    for l in LANGS:
        for k in keys:
            for r in range(K_SEEDS):
                fp[l][k][r] = [lcp_dist(journals[l][k][(a, r)],
                                        journals[l][k][(b, r)])
                               for a, b in epairs]
    # v2 (fix ii/iii): raw fingerprints, matched AND crossed correlations
    def m6(x, y, crossed, subset=None):
        per_inst = []
        for k in (subset or keys):
            cs = []
            for r in range(K_SEEDS):
                ry = (r + 1) % K_SEEDS if crossed else r
                cs.append(pearson(fp[x][k][r], fp[y][k][ry]))
            per_inst.append(sum(cs) / len(cs))
        m = sum(per_inst) / len(per_inst)
        var = sum((c - m) ** 2 for c in per_inst) / max(len(per_inst) - 1, 1)
        return m, (var / len(per_inst)) ** 0.5

    pairs = [('N2', 'C2', 'postulate pair'), ('S1', 'S2', 'cosmetic pair'),
             ("A", "A'", 'clone'), ('A', 'P', 'indep'),
             ('N', 'C', 'coin-masked'), ('N2', 'P', 'control'),
             ('A', 'N2', 'world-floor ref')]
    print(f"{'pair':<10} {'type':<16} {'M6_m':>7} {'se':>6} {'M6_c':>7} "
          f"{'se':>6} | verdict")
    print('-' * 78)
    for x, y, typ in pairs:
        mm, sem = m6(x, y, False)
        mc, sec = m6(x, y, True)
        sig = lambda m, s: m > M6_MIN and m > 2 * s
        if sig(mm, sem) and sig(mc, sec): v = 'CO-ADAPTATION (not independent)'
        elif sig(mm, sem): v = 'cosmetic schedule'
        else: v = 'no signal'
        print(f"({x},{y})".ljust(10) + f"{typ:<16} {mm:>7.3f} {sem:>6.3f} "
              f"{mc:>7.3f} {sec:>6.3f} | {v}")

    print("\nkey pairs per stratum (matched):")
    for x, y in [('N2', 'C2'), ('S1', 'S2'), ('N', 'C'), ('A', 'N2')]:
        row = []
        for s in strata:
            m, se = m6(x, y, False, subset=[(s, i) for i in range(R_INST)])
            row.append(f"{s}={m:.2f}")
        print(f"  ({x},{y}): " + "  ".join(row))

if __name__ == '__main__':
    main()
