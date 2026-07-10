"""
SCOUT 10 (phase 0, NOT citable): the Reference Independence Gate under the
poisoned-reference attack (Codex, final review).

Attack: four references whose surface mechanisms are disjoint (origin scan,
pair sampler, adjacent walker, interval bisection) but which share one
"harmless-looking" preprocessor — an orientation-detecting preamble that
flips the ENTIRE probe schedule (R<->L) when the world looks reversed /
sticky. Globally their mutual co-adaptation can sit near the honest floor;
on strata where the normalizer reacts (wobble, gated, rev perturbations)
they shift schedules in lockstep and the field inflates selectively.

Gate (fixed, per Codex): for a candidate reference set, compute q75 of
pairwise crossed co-adaptation GLOBALLY and PER DIAGNOSTIC STRATUM.
REJECT the set if any stratum q75 exceeds the global q75 by >= 0.10.

Preregistered expectations:
  E1 honest set {A, P, W, M}: gate PASS (no stratum q75 >= global + 0.10).
     Risk stated in advance: if the honest set fails on some stratum, the
     gate as specified is too strict — that outcome is REPORTED, the
     threshold is not silently tuned.
  E2 poisoned set {pA, pP, pW, pM}: gate REJECT (lockstep strata inflate
     their local q75 above global + 0.10).
  E3 (report only) field inflation if the poisoned set were used anyway:
     poisoned-field value vs honest-field value.
Kill: gate passes the poisoned set, or rejects the honest set on every
threshold in [0.05, 0.15] (i.e., no viable margin exists).
"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scout_06_schedule_coadaptation as s6
import scout_09_reference_field as s9

GATE_MARGIN = 0.10
K = s6.K_SEEDS
R_INST = s6.R_INST

class FlipOracle:
    """The shared 'harmless' normalizer's effect: swap R<->L in every probe
    the wrapped language emits."""
    def __init__(self, orc, flip): self.orc, self.flip = orc, flip
    def same(self, p, q):
        if self.flip:
            p = ('L' if p[0] == 'R' else 'R', p[1])
            q = ('L' if q[0] == 'R' else 'R', q[1])
        return self.orc.same(p, q)

def poisoned(base_fn):
    def fn(orc, cap, rng):
        # shared preamble: 'input sanitation' — orientation detection
        o = (orc.same(('L', 1), ('L', 0)) + orc.same(('L', 2), ('L', 0)) +
             orc.same(('R', 1), ('L', 1)))
        return base_fn(FlipOracle(orc, o >= 1), cap, rng)
    return fn

HONEST = {'A': s6.LANGS['A'], 'P': s6.LANGS['P'],
          'W': s9.lang_W, 'M': s9.lang_M}
POISON = {'pA': poisoned(s6.LANGS['A']), 'pP': poisoned(s6.LANGS['P']),
          'pW': poisoned(s9.lang_W), 'pM': poisoned(s9.lang_M)}
SALT = {'A': 11, 'P': 51, 'W': 311, 'M': 331,
        'pA': 401, 'pP': 419, 'pW': 433, 'pM': 449}

def main():
    LANGS = dict(HONEST); LANGS.update(POISON)
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

    def J_inst(x, y, k):
        return sum(s6.pearson(fp[x][k][r], fp[y][k][(r + 1) % K])
                   for r in range(K)) / K

    def q75(vals):
        vals = sorted(vals)
        return vals[max(0, -(-3 * len(vals) // 4) - 1)]

    def gate(refset, label):
        prs = [(a, b) for ai, a in enumerate(refset) for b in refset[ai + 1:]]
        Jglob = {p: sum(J_inst(*p, k) for k in keys) / len(keys) for p in prs}
        g75 = q75(list(Jglob.values()))
        print(f"\n{label}: global q75 = {g75:.3f}   "
              f"(pairs: " + " ".join(f"{a},{b}={Jglob[(a,b)]:.2f}"
                                     for a, b in prs) + ")")
        verdict = 'PASS'
        for sname in strata:
            sub = [(sname, i) for i in range(R_INST)]
            s75 = q75([sum(J_inst(a, b, k) for k in sub) / len(sub)
                       for a, b in prs])
            mark = ''
            if s75 >= g75 + GATE_MARGIN:
                verdict = 'REJECT'; mark = '  <-- inflated'
            print(f"    {sname:<8} q75 = {s75:.3f}{mark}")
        print(f"    GATE: {verdict}")
        return g75, verdict

    g_h, v_h = gate(list(HONEST), 'HONEST set {A,P,W,M}')
    g_p, v_p = gate(list(POISON), 'POISONED set {pA,pP,pW,pM}')
    print(f"\nE3 (report): honest field = {max(0.0, g_h):.3f}, "
          f"poisoned field = {max(0.0, g_p):.3f}")

if __name__ == '__main__':
    main()
