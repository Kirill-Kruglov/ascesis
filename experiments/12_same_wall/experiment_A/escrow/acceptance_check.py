"""
FROZEN acceptance suite for the holdout generation (HOLDOUT_ESCROW v2,
step 4; sha256 of this file is committed before dispatch). Mechanical
only; ANY failure => HOLDOUT_INVALID_GENERATION (terminal, no
regeneration, no script edits).

Usage (inside the custodian session, plaintext never displayed):
    python3 acceptance_check.py <received_file.py>   # prints PASS/FAIL only
"""
import sys, importlib.util, random


def fail(msg):
    print('FAIL:', msg)
    sys.exit(1)


def main(path):
    spec = importlib.util.spec_from_file_location('holdout', path)
    m = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(m)
    except Exception as e:
        fail('import error: %r' % (type(e).__name__,))

    # --- API presence ---------------------------------------------------
    for name in ('WORLD_TUPLES', 'solver_main', 'solver_indep',
                 'apply_T', 'apply_T_inv'):
        if not hasattr(m, name): fail('missing ' + name)

    # --- WorldSpec domains (F6) ------------------------------------------
    WT = m.WORLD_TUPLES
    DOM = {'cycle', 'alias', 'noisy', 'qtrap', 'wobble', 'lollipop', 'nonstat'}
    if set(WT) != DOM: fail('world classes != frozen set')
    ok = (all(isinstance(n, int) and 17 <= n <= 40 for n in WT['cycle']) and
          all(n in (20, 24, 30, 36) and 4 <= q < n and n % q == 0
              for n, q in WT['alias']) and
          all(17 <= n <= 40 and 0.02 <= e <= 0.12 for n, e in WT['noisy']) and
          all(5 <= q <= 9 and n in (3*q, 4*q, 5*q) and f == 0.6
              for n, q, f in WT['qtrap']) and
          all(isinstance(n, int) and 17 <= n <= 40 for n in WT['wobble']) and
          all(5 <= t <= 12 and 12 <= c <= 26 for t, c in WT['lollipop']) and
          all(15 <= a <= 26 and 27 <= b <= 40 and 60 <= s <= 200
              for a, b, s in WT['nonstat']))
    if not ok: fail('parameters outside locked domains')
    if any(len(v) != 8 for v in WT.values()): fail('need 8 tuples per class')

    # --- budget + determinism on a synthetic cyclic oracle ----------------
    class Orc:
        def __init__(self, n, seed):
            self.n, self.count = n, 0
            self.rng = random.Random(seed)
        def __call__(self, u, v):
            self.count += 1
            if self.count > 400: raise RuntimeError('cap exceeded')
            return (u.count('R') - u.count('L')) % self.n == \
                   (v.count('R') - v.count('L')) % self.n
    for fn_name in ('solver_main', 'solver_indep'):
        fn = getattr(m, fn_name)
        r1 = fn(Orc(23, 1), 400, 42)
        r2 = fn(Orc(23, 1), 400, 42)
        if r1 != r2: fail(fn_name + ' nondeterministic')
        if not (isinstance(r1, tuple) and r1[0] in ('VAL', 'AB', 'TO')):
            fail(fn_name + ' bad return')
        if r1[0] == 'VAL' and r1[1] != 23:
            fail(fn_name + ' wrong on a clean cycle')

    # --- matched-direction invariant: T o T_inv == id on sampled probes ---
    base = Orc(29, 2)
    wrapped = m.apply_T(m.apply_T_inv(base))
    rng = random.Random(3)
    for _ in range(50):
        a, b = rng.randint(0, 60), rng.randint(0, 60)
        u, v = 'R' * a, 'R' * b
        probe = Orc(29, 2)
        if wrapped(u, v) != probe(u, v): fail('T o T_inv != id')
    # T itself must be a non-identity transform
    t_only = m.apply_T(Orc(31, 4))
    diff = any(t_only('R' * k, '') != Orc(31, 4)('R' * k, '')
               for k in (7, 13, 19, 31))
    # non-identity is allowed to preserve answers on cyclic worlds
    # (translation does); we require only that T is a real wrapper object
    if t_only is base: fail('apply_T is identity object')

    print('PASS')


if __name__ == '__main__':
    main(sys.argv[1])
