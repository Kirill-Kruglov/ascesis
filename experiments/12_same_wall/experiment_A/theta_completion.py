"""
Theta-completion + OC-validate driver (execution only: calls L0-locked
pipeline functions with AMENDMENT-2 parameters; no new rules).

Stages (one chain, artifacts committed after):
  1. Certify 3 extra cross-file comparator pairs (amended battery,
     wrong-agreement <= 6/24) to reach the >= 10 comparator quorum.
  2. On 50 window-lattice sims (tune stream): per-comparator-pair
     token-excess and J_fail-minus-field -> theta_isolation_token /
     theta_isolation_journal = q90 with one-sided UCB.
     Clone/derived resolution on the in-domain class (c.A vs d.A).
  3. Assemble theta.json (window, k, Nmin, adapt_min, domain classes,
     thetas, resolution, tie-break note) + sha256.
  4. OC-validate: 100 FRESH sims (stream 71000+977s), frozen theta,
     per-AMENDMENT-2 estimand -> PASS/FAIL artifact.
"""
import json, hashlib, random
import pipeline_l0 as p

# ---- stage 1: comparator quorum ------------------------------------------------
EXTRA = [('gptA.r2', 'grok.r1'), ('gptB.r1', 'gem.r1'), ('opusA.r1', 'gem.r1')]
ALLF = dict(p.MAINS); ALLF.update(p.REFS_EXTRA)
cert = {}
for x, y in EXTRA:
    cert['%s|%s' % (x, y)] = p.cert_battery(ALLF[x], ALLF[y])
print('extra certs (wrong-agreement /24):', json.dumps(cert), flush=True)
extra_ok = [(x, y) for x, y in EXTRA if cert['%s|%s' % (x, y)] <= p.CERT_WRONG_MAX]
COMPARATORS = [p.RP_POOL[r] for r in sorted(p.RP_POOL)] + extra_ok
print('comparator set size:', len(COMPARATORS), flush=True)
assert len(COMPARATORS) >= 10, 'comparator quorum not reached'

# ---- stage 2: theta_isolation + resolution on 50 window sims --------------------
WINDOW = ['cycle', 'alias', 'noisy', 'qtrap', 'wobble']       # AMENDMENT-2
THETA0 = {'k': 2.6, 'Nmin': 4, 'adapt_min': 0.05}
langs = {n: ALLF[n] for n in set(sum(([a, b] for a, b in COMPARATORS), []))}
langs['A'] = p.MAINS['A']
langs['c.A'] = p.clone_wrap(p.MAINS['A'], 7)
langs['d.A'] = p.derive_wrap(p.MAINS['A'], 3)
for n in langs: p.SALT.setdefault(n, 701 + 13 * len(n))

tok_stats, j_stats = [], []
res_clone, res_derived = [], []
for s in range(50):
    lattice = p.make_lattice(31000 + 977 * s, WINDOW, r_inst=p.R_INST)
    keys, tokens, logs = p.run_battery(langs, lattice, 31000 + 977 * s)
    fp = p.fingerprints(logs, langs, keys)
    jf_cache = {}
    for a, b in COMPARATORS:
        jm, nf, jc = p.j_fail_raw(tokens, fp, a, b, keys)
        jf_cache[(a, b)] = jm
    for a, b in COMPARATORS:
        _, tm, tc = p.token_channel(tokens, a, b, keys, THETA0)
        tok_stats.append(min(tm, tc))
        jm = jf_cache[(a, b)]
        if jm is None: continue
        others = [v for k2, v in jf_cache.items() if v is not None
                  and p.FAMILY.get(k2[0], k2[0]) not in
                  (p.FAMILY.get(a, a), p.FAMILY.get(b, b))
                  and p.FAMILY.get(k2[1], k2[1]) not in
                  (p.FAMILY.get(a, a), p.FAMILY.get(b, b))]
        if len(others) >= 3:
            j_stats.append(jm - max(0.0, p.q75(others)))
    _, tmc, _ = p.token_channel(tokens, 'A', 'c.A', keys, THETA0)
    _, tmd, _ = p.token_channel(tokens, 'A', 'd.A', keys, THETA0)
    res_clone.append(tmc); res_derived.append(tmd)
    if (s + 1) % 10 == 0: print('theta sims done', s + 1, flush=True)

def q90_ucb(vals):
    vals = sorted(vals)
    idx = max(0, -(-9 * len(vals) // 10) - 1)
    # conservative UCB: take the next order statistic above q90
    return vals[min(idx + 1, len(vals) - 1)]

theta = {'window': WINDOW, 'k': 2.6, 'Nmin': 4, 'adapt_min': 0.05,
         'domain_classes': ['A', 'gem'],
         'theta_isolation_token': q90_ucb(tok_stats),
         'theta_isolation_journal': q90_ucb(j_stats) if j_stats else None,
         'resolution_clone_mean': sum(res_clone) / len(res_clone),
         'resolution_derived_mean': sum(res_derived) / len(res_derived),
         'comparators': ['%s|%s' % c for c in COMPARATORS],
         'extra_certs': cert,
         'tie_break': 'unique window; rule frozen at L0 (§7)',
         'n_theta_sims': 50, 'j_stat_n': len(j_stats)}
blob = json.dumps(theta, sort_keys=True, indent=1)
theta['sha256'] = hashlib.sha256(blob.encode()).hexdigest()
with open('theta.json', 'w') as fh: json.dump(theta, fh, indent=1)
print('THETA:', json.dumps(theta), flush=True)

# ---- stage 4: OC-validate (100 fresh sims, frozen theta) ------------------------
acc = {'derived': 0, 'derived_n': 0, 'fp': 0, 'fp_n': 0}
for s in range(p.N_MC_VALIDATE):
    r = p.oc_run(71000 + 977 * s, THETA0)['+'.join(WINDOW)]
    for b, v in zip(('A', 'gptA', 'gem'), r['derived']):
        if b in theta['domain_classes'] and v != 'NO_TEST':
            acc['derived_n'] += 1; acc['derived'] += v == 'DEPENDENT'
    for v in r['indep']:
        if v != 'NO_TEST':
            acc['fp_n'] += 1; acc['fp'] += v == 'DEPENDENT'
    if (s + 1) % 10 == 0: print('validate sims done', s + 1, flush=True)
p_lcb = p.binom_lcb(acc['derived'], max(acc['derived_n'], 1))
f_ucb = p.binom_ucb(acc['fp'], max(acc['fp_n'], 1))
verdict = 'PASS' if (p_lcb >= p.POWER_MIN and f_ucb <= p.ALPHA) else 'OC_VALIDATE_FAIL'
result = {'power_lcb': p_lcb, 'fpr_ucb': f_ucb, 'raw': acc,
          'verdict': verdict, 'theta_sha256': theta['sha256'],
          'seed_stream': '71000+977s', 'n': p.N_MC_VALIDATE}
with open('oc_validate_result.json', 'w') as fh: json.dump(result, fh, indent=1)
print('OC-VALIDATE:', json.dumps(result), flush=True)
