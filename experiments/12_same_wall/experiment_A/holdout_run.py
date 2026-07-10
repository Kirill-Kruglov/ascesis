"""
HOLDOUT RUN (DAG step 8): the escrowed Gemini generation through the
locked pipeline, zero rule changes. Published regardless of outcome.

Escrow chain verified: plaintext sha256 a0cb7bac...bce0 equals the hash
recorded BEFORE the primary run; acceptance PASS at receipt (frozen
suite); model label at dispatch: gemini-3.5-flash (ESCROW-NOTE: the
frozen literal labels were absent on the platform; family rule held).

Registered expectations (written before running):
  H1 (hm, hm∘T)   forward-derived            -> DEPENDENT*
  H2 (hm, hm∘T⁻¹) reverse-derived            -> same verdict as H1
      (direction-invariance, tested ONCE — scoped wording locked)
  H3 (hm, hi)     same-prior, diff-mechanism -> reported; CLEAN expected
      (mechanism difference), a flag reads as common-prior material
  H4 (A, hm)      cross-prior clean-room     -> CLEAN — the strictest
      test (0/24-class prior); a flag implicates the instrument
  H5 (A, Gt)      derived replication on holdout worlds -> DEPENDENT*
Scope: generalization WITHIN the applicability domain (schedule-
adaptive, value-failing); field for holdout/gem-involved pairs = the
3 non-gem CALIBRATION RPs (registered quorum edge, as for (A,opusA)).
"""
import json, random, importlib.util
from pathlib import Path
import pipeline_l0 as p
from worlds_general import (GCycle, GAliasCycle, GWobble, run_language,
                            lang_A_general, lang_G_translated)

HERE = Path(__file__).resolve().parent
HOLDOUT_MASTER = 660011          # fresh stream, disjoint from all prior

spec = importlib.util.spec_from_file_location(
    'holdout', HERE / 'escrow' / 'holdout_plain.py')
H = importlib.util.module_from_spec(spec); spec.loader.exec_module(H)

def hm(orc, cap, seed): return H.solver_main(orc, cap, seed)
def hi(orc, cap, seed): return H.solver_indep(orc, cap, seed)
def hmT(orc, cap, seed): return H.solver_main(H.apply_T(orc), cap, seed)
def hmTi(orc, cap, seed): return H.solver_main(H.apply_T_inv(orc), cap, seed)

LANGS = {'A': lang_A_general, 'Gt': lang_G_translated,
         'gptA': p.MAINS['gptA'], 'gptB': p.MAINS['gptB'],
         'grok': p.MAINS['grok'], 'gem': p.MAINS['gem'],
         'opusA': p.MAINS['opusA'],
         'hm': hm, 'hi': hi, 'hmT': hmT, 'hmTi': hmTi}
for n in LANGS: p.SALT.setdefault(n, 901 + 19 * len(n))

NONGEM_RP = ['RP-05', 'RP-08', 'RP-09']
for pair in [('hm', 'hmT'), ('hm', 'hmTi'), ('hm', 'hi'), ('A', 'hm')]:
    p.FIELD_ALLOC[pair] = NONGEM_RP
p.FIELD_ALLOC[('A', 'Gt')] = ['RP-04', 'RP-05', 'RP-07', 'RP-08', 'RP-09']

def holdout_lattice():
    """Worlds from the escrowed WORLD_TUPLES, locked window strata."""
    rng = random.Random(HOLDOUT_MASTER)
    lat = {}
    lat['cycle'] = [(GCycle(n), n) for n in H.WORLD_TUPLES['cycle']]
    lat['alias'] = [(GAliasCycle(n, q), n) for n, q in H.WORLD_TUPLES['alias']]
    lat['noisy'] = [(GCycle(n, eps=e), n) for n, e in H.WORLD_TUPLES['noisy']]
    lat['qtrap'] = [(p.QuotientTrap(n, q, rng, frac=f), n)
                    for n, q, f in H.WORLD_TUPLES['qtrap']]
    lat['wobble'] = [(GWobble(n), None) for n in H.WORLD_TUPLES['wobble']]
    return lat

def main():
    theta = {'k': 2.6, 'Nmin': 4, 'adapt_min': 0.05}
    lat = holdout_lattice()
    keys, tokens, logs = [], {l: {} for l in LANGS}, {l: {} for l in LANGS}
    for s in lat:
        for i, (w, truth) in enumerate(lat[s]):
            keys.append((s, i))
            for pi, (pn, bp, rev) in enumerate(p.PERTS):
                for r in range(p.K_SEEDS):
                    for lname, fn in LANGS.items():
                        res, log = run_language(fn, p.fresh(w), p.CAP,
                                                seed=10007 * r + p.SALT[lname],
                                                bp=bp, rev=rev)
                        tokens[lname].setdefault((s, i), {})[(pi, r)] = \
                            p.classify(res, truth)
                        logs[lname].setdefault((s, i), {})[(pi, r)] = log
    fp = p.fingerprints(logs, LANGS, keys)
    out = {}
    for name, (x, y) in [('H1_fwd_derived', ('hm', 'hmT')),
                         ('H2_rev_derived', ('hm', 'hmTi')),
                         ('H3_same_prior_diff_mech', ('hm', 'hi')),
                         ('H4_cross_prior_cleanroom', ('A', 'hm')),
                         ('H5_derived_replication', ('A', 'Gt'))]:
        v = p.pair_verdict(tokens, fp, x, y, keys, theta)
        out[name] = v
    summary = {
        'H1': out['H1_fwd_derived']['P_union'],
        'H2': out['H2_rev_derived']['P_union'],
        'H2_equals_H1': out['H1_fwd_derived']['P_union'] ==
                        out['H2_rev_derived']['P_union'],
        'H3': out['H3_same_prior_diff_mech']['P_union'],
        'H4': out['H4_cross_prior_cleanroom']['P_union'],
        'H5': out['H5_derived_replication']['P_union'],
        'holdout_master': HOLDOUT_MASTER,
        'plaintext_sha256': 'a0cb7bac0cdeb6d9e76a2336f8725fdee3b2cc879e2'
                            '33f8937cf1188c147bce0',
        'detail': out,
    }
    with open(HERE / 'holdout_result.json', 'w') as fh:
        json.dump(summary, fh, indent=1, default=str)
    print(json.dumps({k: summary[k] for k in
                      ('H1', 'H2', 'H2_equals_H1', 'H3', 'H4', 'H5')},
                     indent=1))

if __name__ == '__main__':
    main()
