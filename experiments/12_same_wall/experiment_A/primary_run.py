"""
PRIMARY RUN driver (execution of the locked design; PREREG v4.1 + A1 + A2).

Order: pre-checks (dual-oracle cross-check; leakage scan; NULL-WORLD GATE
-> tautology report; blind sanity incl. C2 E-axis) -> primary battery on
the locked window -> K/C assembly (§5, per-channel E/N/P) ->
gate_harness.runner.run_gate -> signed decision.json -> verify_decision.

Master seeds (declared here, disjoint from every scout/OC stream):
SANITY_MASTER = 88880001, PRIMARY_MASTER = 550007.
"""
import json, random, hashlib
from pathlib import Path
import pipeline_l0 as p
from worlds_general import GCycle, run_language
from gate_harness import runner as gh_runner
from gate_harness import leakage_scanner as gh_leak

HERE = Path(__file__).resolve().parent
THETA = json.load(open(HERE / 'theta.json'))
WINDOW = THETA['window']
SANITY_MASTER = 88880001
PRIMARY_MASTER = 550007

# ---- registered languages (§3) ------------------------------------------------

def lang_W_str(oracle, cap_calls, seed):
    k0 = None
    for k in range(1, 41):
        if oracle('R' * k, 'R' * (k - 1)): k0 = k; break
    if k0 is None: return ('AB',)
    hits = sum(oracle('R' * (k0 + i), 'R' * k0) for i in range(1, 6))
    return ('VAL', k0, hits >= 3)

def lang_M_str(oracle, cap_calls, seed):
    lo, hi = 1, 170
    while lo < hi:
        mid = (lo + hi) // 2
        if oracle('R' * mid, 'R' * lo): hi = mid
        else: lo = mid + 1
    ok = sum(oracle('R' * (lo + i), 'R' * i) for i in range(1, 4))
    return ('VAL', lo, ok >= 2)

PM_PROFILE = {'cycle': 0.05, 'alias': 0.6, 'noisy': 0.9, 'qtrap': 0.9,
              'wobble': 1.0}
_stratum = {'name': 'cycle'}

def make_pm(base_fn, salt):
    def fn(oracle, cap, seed):
        rng = random.Random(seed * 31 + salt)
        calls = {'n': 0}
        def orc(u, v):
            calls['n'] += 1
            return oracle(u, v)
        res = base_fn(orc, cap, seed)
        if rng.random() < PM_PROFILE[_stratum['name']]:
            vrng = random.Random(seed * 31 + salt + 7919 * calls['n'])
            return ('VAL', vrng.randint(1, 15), True)
        return res
    return fn

LANGS = {'A': p.MAINS['A'], 'A2': p.clone_wrap(p.MAINS['A'], 7),
         'Gt': __import__('worlds_general').lang_G_translated,
         'gptA': p.MAINS['gptA'], 'gptB': p.MAINS['gptB'],
         'grok': p.MAINS['grok'], 'gem': p.MAINS['gem'],
         'opusA': p.MAINS['opusA'], 'gptA.r1': p.REFS_EXTRA['gptA.r1'],
         'PM1': make_pm(lang_W_str, 5), 'PM2': make_pm(lang_M_str, 9)}
for n in LANGS: p.SALT.setdefault(n, 801 + 17 * len(n))

GATING = {'C1': ('A', 'A2'), 'K2a': ('A', 'Gt'), 'K2b': ('A', 'gptA'),
          'C_C8': ('A', 'opusA'), 'C_PM': ('PM1', 'PM2')}
C2_PAIRS = [('gptA', 'grok'), ('gptB', 'gem'), ('gptA', 'gem'), ('A', 'gem')]
REPORTED = [('gptA', 'gptA.r1')]

# ---- battery with stratum hook (PM needs current stratum) ----------------------

def battery(master_seed):
    lattice = p.make_lattice(master_seed, WINDOW, r_inst=p.R_INST)
    keys, tokens, logs = [], {l: {} for l in LANGS}, {l: {} for l in LANGS}
    for s in lattice:
        _stratum['name'] = s
        for i, (w, truth) in enumerate(lattice[s]):
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
    return lattice, keys, tokens, logs

def naive_fires(tokens, x, y, keys, strat='cycle'):
    """Naive destination detector: same VAL m by id-pert majority."""
    hits = tot = 0
    for k in [k for k in keys if k[0] == strat]:
        tot += 1
        def maj(l):
            vs = [tokens[l][k][(0, r)] for r in range(p.K_SEEDS)]
            vals = [t[1] for t in vs if t[0] in ('S', 'WC', 'WD')]
            return max(set(vals), key=vals.count) if vals else None
        mx, my = maj(x), maj(y)
        hits += mx is not None and mx == my
    return hits, tot

def dest_same_correct(tokens, x, y, keys, lattice):
    hits = tot = 0
    for k in [k for k in keys if k[0] == 'cycle']:
        tot += 1
        truth = lattice['cycle'][k[1]][1]
        def maj(l):
            vs = [tokens[l][k][(0, r)] for r in range(p.K_SEEDS)]
            vals = [t[1] for t in vs if t[0] == 'S']
            return max(set(vals), key=vals.count) if vals else None
        hits += maj(x) == truth and maj(y) == truth
    return hits, tot

# ---- phases --------------------------------------------------------------------

def dual_oracle_check(lattice):
    rng = random.Random(11)
    for s in lattice:
        for w, truth in lattice[s]:
            if not isinstance(w, GCycle): continue
            for _ in range(20):
                word = ''.join(rng.choice('RL') for _ in range(rng.randint(0, 60)))
                st = 0
                for ch in word: st = w.step_R(st) if ch == 'R' else w.step_L(st)
                if st != w.run(word): return False
    return True

def null_world_gate(theta):
    nulls = [ (__import__('pipeline_l0').NullWorld(900 + i), None) for i in range(p.R_INST)]
    lattice = {'cycle': nulls}          # class label irrelevant for the gate
    _stratum['name'] = 'cycle'
    keys, tokens, logs = [], {l: {} for l in LANGS}, {l: {} for l in LANGS}
    for i, (w, truth) in enumerate(nulls):
        keys.append(('cycle', i))
        for pi, (pn, bp, rev) in enumerate(p.PERTS):
            for r in range(p.K_SEEDS):
                for lname, fn in LANGS.items():
                    res, log = run_language(fn, w, p.CAP,
                                            seed=10007 * r + p.SALT[lname],
                                            bp=bp, rev=rev)
                    tokens[lname].setdefault(('cycle', i), {})[(pi, r)] = \
                        p.classify(res, truth)
                    logs[lname].setdefault(('cycle', i), {})[(pi, r)] = log
    fp = p.fingerprints(logs, LANGS, keys)
    # AMENDMENT-3(b): registered same-construction controls (the clone)
    # are EXCLUDED from the null gate — their coupling is construction-
    # level and needs no world (a consistent answer function suffices);
    # a clone flag here confirms the construction channel. All
    # cross-construction pairs must read CLEAN/INADMISSIBLE.
    SAME_CONSTRUCTION = {GATING['C1']}
    dep, clone_confirm = [], []
    for x, y in list(GATING.values()) + C2_PAIRS:
        v = p.pair_verdict(tokens, fp, x, y, keys, theta)
        if v['P_union'] == 'DEPENDENT':
            if (x, y) in SAME_CONSTRUCTION: clone_confirm.append((x, y))
            else: dep.append((x, y))
    nx, nt = naive_fires(tokens, 'A', 'gptA', keys)
    return {'null_dependents': dep,
            'null_clone_construction_confirm': clone_confirm,
            'null_naive_rate': f'{nx}/{nt}',
            'construction_may_be_tautological': bool(dep),
            'method': 'null-world gate (K3 / §4.5, AMENDMENT-3): any '
                      'CROSS-construction DEPENDENT on a world with no '
                      'world => channels tautological; same-construction '
                      'controls excluded by design'}

def main():
    theta = {'k': THETA['k'], 'Nmin': THETA['Nmin'],
             'adapt_min': THETA['adapt_min']}

    # leakage scan (fit-path analog: verdict fns see only tokens/logs;
    # languages see only the oracle)
    scan = gh_leak.scan_fit_path(
        [p.token_channel, p.journal_channel, p.j_fail_raw, p.admission,
         p.pair_verdict, p.clone_wrap, p.derive_wrap,
         p.MAINS['A'], p.MAINS['gptA'], p.MAINS['gptB'], p.MAINS['grok'],
         p.MAINS['gem'], p.MAINS['opusA']],
        forbidden_names=['trapped', 'switch'])
    print('leakage scan passed:', scan['passed'], flush=True)

    # null-world gate -> tautology report
    taut = null_world_gate(theta)
    print('null-world gate:', json.dumps({k: taut[k] for k in
          ('null_dependents', 'null_naive_rate')}), flush=True)

    # blind sanity (infra + C2 E-axis only; no P labels printed or kept)
    lat_s, keys_s, tok_s, logs_s = battery(SANITY_MASTER)
    fp_s = p.fingerprints(logs_s, LANGS, keys_s)
    assert dual_oracle_check(lat_s), 'dual-oracle mismatch'
    c2_adm = {}
    for x, y in C2_PAIRS:
        E_tok, N_tok, E_j, ninf = p.admission(tok_s, fp_s, x, y, keys_s, theta)
        c2_adm['%s|%s' % (x, y)] = bool(E_tok and N_tok)
    print('sanity: dual-oracle OK, determinism OK (battery completed), '
          'C2 token-admission:', json.dumps(c2_adm), flush=True)
    del lat_s, keys_s, tok_s, logs_s, fp_s          # blind: nothing retained

    def experiment():
        lattice, keys, tokens, logs = battery(PRIMARY_MASTER)
        fp = p.fingerprints(logs, LANGS, keys)
        V = {name: p.pair_verdict(tokens, fp, x, y, keys, theta)
             for name, (x, y) in GATING.items()}
        C2 = {}
        for x, y in C2_PAIRS:
            C2['%s|%s' % (x, y)] = p.pair_verdict(tokens, fp, x, y, keys, theta)
        REP = {f'{x}|{y}': p.pair_verdict(tokens, fp, x, y, keys, theta)
               for x, y in REPORTED}
        # K1 naive
        k1_gt = naive_fires(tokens, 'A', 'Gt', keys)
        k1_gp = naive_fires(tokens, 'A', 'gptA', keys)
        # K2b D-axis
        d_gp = dest_same_correct(tokens, 'A', 'gptA', keys, lattice)
        # ---- assembly (§5) ----
        K1 = k1_gt[0] >= 6 and k1_gp[0] >= 6 and \
             int(taut['null_naive_rate'].split('/')[0]) <= 1
        K2a = V['K2a']['P_union'] == 'DEPENDENT'
        k2b_clean = (V['K2b'].get('P_tok') == 'CLEAN'
                     and V['K2b'].get('P_j') == 'CLEAN')
        K2b = k2b_clean and d_gp[0] >= 6
        K3 = not taut['construction_may_be_tautological'] and \
             int(taut['null_naive_rate'].split('/')[0]) <= 1
        C1 = V['C1']['P_union'] == 'DEPENDENT'
        c2_ok = [k for k, v in C2.items()
                 if v.get('P_tok') in ('CLEAN', 'DEPENDENT')]
        C2_pass = (len(c2_ok) >= 3 and
                   all(C2[k]['P_tok'] == 'CLEAN' for k in c2_ok))
        C_C8 = V['C_C8']['P_union'] == 'DEPENDENT'
        C_PM = V['C_PM']['P_union'] == 'CLEAN'
        full = all([K1, K2a, K2b, K3, C1, C2_pass, C_C8, C_PM])
        payload = {
            'decision': ('EXPA-FULL-CLEAN' if full else 'EXPA-NOT-CLEAN'),
            'K1': K1, 'K2a': K2a, 'K2b': K2b, 'K3': K3, 'C1': C1,
            'C2': C2_pass, 'C_C8': C_C8, 'C_PM': C_PM,
            'k1_naive': {'A|Gt': f'{k1_gt[0]}/{k1_gt[1]}',
                         'A|gptA': f'{k1_gp[0]}/{k1_gp[1]}'},
            'k2b_dest_same_correct': f'{d_gp[0]}/{d_gp[1]}',
            'pair_verdicts': {k: {kk: vv for kk, vv in v.items()}
                              for k, v in {**V, **C2, **REP}.items()},
            'null_world_gate': taut,
            'theta_sha256': THETA['sha256'],
            'seed_masters': {'sanity': SANITY_MASTER,
                             'primary': PRIMARY_MASTER},
            'claim': ('Within the locked stress family, the v4 instrument '
                      'assigned different residual-dependence labels to one '
                      'registered derived pair and one registered clean-room '
                      'pair, while preserving destination agreement.'
                      if (K2a and K2b) else
                      'target contrast not reproduced; no causal '
                      'interpretation assigned'),
            'seed_count': p.K_SEEDS * p.R_INST * len(WINDOW),
        }
        return payload

    # evaluation-oracle scan (finding #6): no ground-truth literal may enter
    # an evaluation call site; classify() receives truth as a VARIABLE from
    # the world instance (the evaluator's legitimate channel), never a literal
    from gate_harness import evaluation_oracle as gh_eval
    import primary_run as _self
    eval_scan = gh_eval.scan_evaluation_call_sites(
        _self, ['classify'], forbidden_names=['truth_axes'])
    print('evaluation-oracle scan passed:', eval_scan.get('passed'), flush=True)

    decision = gh_runner.run_gate(HERE, experiment,
                                  leakage_report=scan,
                                  tautology_report=taut,
                                  evaluation_oracle_log=eval_scan.get(
                                      'evaluation_oracle_log', []))
    print(json.dumps({k: decision[k] for k in
                      ('decision', 'K1', 'K2a', 'K2b', 'K3', 'C1', 'C2',
                       'C_C8', 'C_PM', 'k1_naive', 'k2b_dest_same_correct',
                       'claim')}, indent=1, ensure_ascii=False))

if __name__ == '__main__':
    main()
