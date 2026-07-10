"""
Four independent order finders for an unknown two-action world.

Public API:
    find_order_main(oracle, cap_calls, seed)
    find_order_ref1(oracle, cap_calls, seed)
    find_order_ref2(oracle, cap_calls, seed)
    find_order_ref3(oracle, cap_calls, seed)

Return values:
    ('VAL', m, confident)
    ('AB',)
    ('TO',)

DESIGN MEMO
===========

Shared conservative model
-------------------------
All four solvers treat the intended periodic world as a cyclic action:
for every word w, its state depends only on

    displacement(w) = count('R') - count('L')  (mod m),

and m is the least positive period.  Thus L is the inverse shift of R.
This is stronger than merely saying that the R-orbit eventually cycles;
it is deliberate.  The public contract allows abstention on tails, sticky
states and inconsistent actions, so the solvers prefer AB/TO over silently
changing the meaning of "period".

The oracle may occasionally lie.  Search calls are mostly single-shot to
preserve range, but every accepted relation is checked with several
*different word pairs* representing the same displacement relation.  This
helps both with transient noise and with pair-specific bad answers.  A
confident result additionally requires positive period witnesses, proper-
divisor rejections, inverse/same-displacement checks, and non-congruence
checks.  One isolated contradiction never causes AB.

All randomness comes from random.Random(seed).  No helper uses module-level
randomness.  Every oracle call passes through _Budget, which enforces the
cap exactly.  Words are capped at _MAX_WORD characters as a practical
resource guard; inability to represent a needed probe leads to TO, never a
fabricated value.

find_order_main -- randomized contextual first-relation scan
------------------------------------------------------------
Scans positive offsets k = 1, 2, ... .  Instead of always asking whether
R**k equals the empty word, it asks randomized equivalent questions whose
net displacements differ by k, sometimes using mixed R/L words.  The first
well-confirmed hit is a multiple of m.  Prime-factor stripping then reduces
that multiple to the least supported period.  This mechanism is ordered,
local and deliberately sensitive to the first return.

Randomness: choice of base displacement, orientation and neutral R/L pairs.
Assumptions: the full cyclic-action model above.
Abstention: AB after repeated structural contradictions; TO if no relation
is found or evidence is too weak.

find_order_ref1 -- Brent-style cycle detection
----------------------------------------------
Runs Brent's power-of-two landmark algorithm on the canonical R-walk.  It
compares a moving hare with a landmark and obtains a candidate cycle length
from the block-local counter.  Unlike the main solver, it does not enumerate
candidate offsets in order and does not use random search probes.  Mixed-word
checks are reserved for validation.

Randomness: only validation witness construction.
Assumptions: R is periodic from the start; validation additionally requires
L to act as the inverse shift.
Abstention: a tail can produce a Brent cycle length, but start-based period
checks then force AB/TO rather than a confident answer.

find_order_ref2 -- birthday collisions and gcd reconstruction
--------------------------------------------------------------
Samples many distinct random integer displacements, compares shuffled pairs,
and collects genuine state collisions.  In a cycle, every collision
difference is a multiple of m; their gcd is therefore a multiple of m and is
usually m once several collisions are present.  Factor stripping and the
shared validator finish the reconstruction.  This can discover periods
larger than the number of oracle calls, unlike the ordered scans.

Randomness: sampled exponents and pair order, plus validation witnesses.
Assumptions: signed canonical exponents use L as R^{-1}.
Abstention: TO when no confirmed birthday collision occurs; AB only on
repeated model contradictions.

find_order_ref3 -- random/smooth multiple hunting
-------------------------------------------------
Queries whether selected positive integers q are periods directly.  The
probe stream mixes smooth numbers (good coverage for orders with small prime
factors), lcm-ladder values, powers, and uniform random integers.  A hit says
m divides q; prime-factor stripping reconstructs the least period.  This is
not a walk or a collision table: it searches the divisibility lattice of
possible relation lengths.

Randomness: uniform and smooth probe construction, probe order, and
validation witnesses.
Assumptions: canonical R powers form a pure cycle and L is inverse in the
validation model.
Abstention: TO if no multiple is hit; AB only after strong structural
incompatibility.
"""

import random
import math


_MAX_WORD = 50000


class _Exhausted(Exception):
    pass


class _WordTooLong(Exception):
    pass


class _Budget:
    def __init__(self, oracle, cap_calls):
        self.oracle = oracle
        self.cap = max(0, int(cap_calls))
        self.calls = 0
        self.faults = 0

    @property
    def remaining(self):
        return self.cap - self.calls

    def ask(self, u, v):
        if self.calls >= self.cap:
            raise _Exhausted
        self.calls += 1
        try:
            ans = self.oracle(u, v)
        except Exception:
            self.faults += 1
            return None
        if ans is True:
            return True
        if ans is False:
            return False
        # The specified interface returns bool.  A non-bool is treated as a
        # faulty answer, not silently coerced into evidence.
        self.faults += 1
        return None


def _canon(n):
    n = int(n)
    if abs(n) > _MAX_WORD:
        raise _WordTooLong
    if n >= 0:
        return "R" * n
    return "L" * (-n)


def _mixed_word(net, rng, max_extra=7):
    net = int(net)
    extra = rng.randrange(max_extra + 1) if max_extra > 0 else 0
    r_count = max(net, 0) + extra
    l_count = max(-net, 0) + extra
    if r_count + l_count > _MAX_WORD:
        raise _WordTooLong
    chars = ["R"] * r_count + ["L"] * l_count
    rng.shuffle(chars)
    return "".join(chars)


def _difference_pair(diff, rng, style=None):
    """Return words whose integer displacements differ by abs(diff)."""
    diff = abs(int(diff))
    if diff <= 0:
        raise ValueError("positive difference required")
    if diff > _MAX_WORD:
        raise _WordTooLong

    if style is None:
        style = rng.randrange(6)

    room = _MAX_WORD - diff
    base_bound = min(23, max(0, room // 2))
    base = rng.randint(-base_bound, base_bound) if base_bound else 0

    if style == 0:
        u, v = _canon(base), _canon(base + diff)
    elif style == 1:
        u, v = _canon(base), _canon(base - diff)
    elif style == 2:
        u, v = _mixed_word(base, rng, 4), _mixed_word(base + diff, rng, 4)
    elif style == 3:
        u, v = _mixed_word(base, rng, 4), _mixed_word(base - diff, rng, 4)
    elif style == 4:
        # Canonical opposite-side representatives exercise both actions.
        left = min(diff, 1 + rng.randrange(min(diff, 17)))
        u, v = _canon(-left), _canon(diff - left)
    else:
        u, v = _mixed_word(base, rng, 2), _canon(base + diff)

    if rng.randrange(2):
        u, v = v, u
    return u, v


def _same_displacement_pair(net, rng):
    net = int(net)
    u = _mixed_word(net, rng, 7)
    v = _mixed_word(net, rng, 7)
    if u == v:
        # Force a syntactically different equivalent representative when
        # possible; RL has zero displacement in the intended model.
        if len(v) + 2 <= _MAX_WORD:
            v = v + ("RL" if rng.randrange(2) else "LR")
    if rng.randrange(2):
        u, v = v, u
    return u, v


def _evidence_for_difference(budget, rng, diff, trials):
    yes = 0
    no = 0
    seen = 0
    for t in range(max(0, int(trials))):
        if budget.remaining <= 0:
            break
        try:
            u, v = _difference_pair(diff, rng, t % 6)
        except _WordTooLong:
            break
        ans = budget.ask(u, v)
        if ans is None:
            continue
        seen += 1
        if ans:
            yes += 1
        else:
            no += 1
    return yes, no, seen


def _model_screen(budget, rng, target=8):
    """Cheap structural screen.  Returns (passes, failures, observed)."""
    tests = [
        ("", ""),
        ("R", "R"),
        ("L", "L"),
        ("", "RL"),
        ("", "LR"),
        ("R", "LRR"),       # both have displacement +1
        ("L", "RLL"),       # both have displacement -1
    ]
    # Add several pair-diverse same-displacement checks.
    while len(tests) < max(7, target):
        net = rng.randint(-7, 7)
        try:
            tests.append(_same_displacement_pair(net, rng))
        except _WordTooLong:
            break

    passes = 0
    failures = 0
    observed = 0
    for u, v in tests[:target]:
        if budget.remaining <= 0:
            break
        ans = budget.ask(u, v)
        if ans is None:
            continue
        observed += 1
        if ans:
            passes += 1
        else:
            failures += 1
    return passes, failures, observed


def _screen_says_ab(screen):
    passes, failures, observed = screen
    return observed >= 5 and failures >= 3 and failures > passes


def _distinct_prime_factors(n):
    n = abs(int(n))
    out = []
    p = 2
    while p * p <= n:
        if n % p == 0:
            out.append(p)
            while n % p == 0:
                n //= p
        p = 3 if p == 2 else p + 2
    if n > 1:
        out.append(n)
    return out


def _minimize_multiple(budget, rng, candidate, trials=3):
    """Strip prime factors whose quotient is itself well-supported.

    Returns (reduced_candidate, strong_reduction_evidence).
    """
    n = abs(int(candidate))
    if n <= 0:
        return n, False
    strong = True
    # Recompute factors after every successful division.  This handles prime
    # powers without assuming the original exponent.
    changed = True
    while changed and n > 1:
        changed = False
        for p in _distinct_prime_factors(n):
            d = n // p
            if d <= 0:
                continue
            yes, no, seen = _evidence_for_difference(budget, rng, d, trials)
            if seen < trials:
                strong = False
            if seen >= 2 and yes > no:
                n = d
                changed = True
                break
    return n, strong


def _choose_nonmultiple(m, rng):
    if m <= 1:
        return None
    # Small differences make words cheap and are especially useful against
    # tail/sticky worlds.  Avoid 0 mod m by construction.
    bound = min(_MAX_WORD, max(9, 3 * m + 7))
    for _ in range(20):
        d = rng.randint(1, bound)
        if d % m:
            return d
    return 1 if m != 1 else None


def _validate_candidate(budget, rng, m, initial_screen=None):
    """Return ('ok', confident), ('ab', False), or ('to', False)."""
    m = int(m)
    if m <= 0 or m > _MAX_WORD:
        return "to", False

    # 1) Candidate-period witnesses.  Include the start state explicitly,
    # because that is what rejects an eventual cycle with a nonempty tail.
    pos_pass = 0
    pos_fail = 0
    pos_seen = 0

    # The start relation is semantically indispensable: an eventual cycle
    # after a tail is not a period of the orbit from its start.  Vote on this
    # exact fact in both orientations before considering contextual returns.
    start_pass = 0
    start_fail = 0
    start_seen = 0
    start_word = _canon(m)
    for u, v in (("", start_word), (start_word, ""), ("", start_word)):
        if budget.remaining <= 0:
            break
        ans = budget.ask(u, v)
        if ans is None:
            continue
        start_seen += 1
        if ans:
            start_pass += 1
        else:
            start_fail += 1

    positive_pairs = []
    if 2 * m <= _MAX_WORD:
        positive_pairs.append((_canon(m), _canon(2 * m)))
    for style in range(5):
        try:
            positive_pairs.append(_difference_pair(m, rng, style))
        except _WordTooLong:
            pass

    for u, v in positive_pairs[:6]:
        if budget.remaining <= 0:
            break
        ans = budget.ask(u, v)
        if ans is None:
            continue
        pos_seen += 1
        if ans:
            pos_pass += 1
        else:
            pos_fail += 1

    # 2) Proper-divisor rejection.  Testing m/p for every distinct prime p
    # is enough to exclude every smaller divisor of m in the cyclic model.
    divisor_records = []
    for p in _distinct_prime_factors(m):
        d = m // p
        yes, no, seen = _evidence_for_difference(budget, rng, d, 3)
        divisor_records.append((d, yes, no, seen))

    # 3) Structural same-displacement / inverse checks.
    model_pass = 0
    model_fail = 0
    model_seen = 0
    model_pairs = [
        ("", ""),
        ("", "RL"),
        ("", "LR"),
        ("R", "LRR"),
        ("L", "RLL"),
    ]
    for _ in range(3):
        try:
            model_pairs.append(_same_displacement_pair(rng.randint(-9, 9), rng))
        except _WordTooLong:
            break
    for u, v in model_pairs[:7]:
        if budget.remaining <= 0:
            break
        ans = budget.ask(u, v)
        if ans is None:
            continue
        model_seen += 1
        if ans:
            model_pass += 1
        else:
            model_fail += 1

    # 4) Differences that must not be periods.  For m == 1 every difference
    # is a multiple, so use extra arbitrary-pair equality checks instead.
    neg_pass = 0   # oracle correctly said False
    neg_fail = 0   # oracle unexpectedly said True
    neg_seen = 0
    if m > 1:
        for _ in range(4):
            d = _choose_nonmultiple(m, rng)
            if d is None or budget.remaining <= 0:
                break
            try:
                u, v = _difference_pair(d, rng)
            except _WordTooLong:
                break
            ans = budget.ask(u, v)
            if ans is None:
                continue
            neg_seen += 1
            if ans:
                neg_fail += 1
            else:
                neg_pass += 1
    else:
        for _ in range(4):
            if budget.remaining <= 0:
                break
            a = rng.randint(-12, 12)
            c = rng.randint(-12, 12)
            try:
                u = _mixed_word(a, rng, 3)
                v = _mixed_word(c, rng, 3)
            except _WordTooLong:
                break
            ans = budget.ask(u, v)
            if ans is None:
                continue
            neg_seen += 1
            if ans:
                neg_pass += 1
            else:
                neg_fail += 1

    # Combine the initial screen with validation diagnostics only for deciding
    # whether the model itself is contradicted.  Candidate-specific failures
    # alone normally mean TO, because the candidate may simply be wrong.
    screen_pass = screen_fail = screen_seen = 0
    if initial_screen is not None:
        screen_pass, screen_fail, screen_seen = initial_screen
    all_model_pass = model_pass + screen_pass
    all_model_fail = model_fail + screen_fail
    all_model_seen = model_seen + screen_seen

    if (all_model_seen >= 9 and all_model_fail >= 4 and
            all_model_fail > all_model_pass):
        return "ab", False

    # Strong evidence of an eventual-but-not-start-periodic R walk: several
    # contextual m-relations succeeded, but the explicit start relation did
    # not.  This is a model contradiction, not merely an unknown period.
    if (start_seen >= 2 and start_fail > start_pass and
            pos_seen >= 2 and pos_pass > pos_fail):
        return "ab", False
    if start_seen >= 2 and start_fail > start_pass:
        return "to", False

    if pos_seen >= 4 and pos_fail >= 3 and pos_fail > pos_pass:
        return "ab", False

    if start_seen < 2 or start_pass <= start_fail:
        return "to", False
    if pos_seen < 2 or pos_pass <= pos_fail:
        return "to", False

    # A proper divisor looking like a period means minimization is unresolved.
    for _d, yes, no, seen in divisor_records:
        if seen >= 2 and yes > no:
            return "to", False

    if m > 1 and neg_seen >= 2 and neg_fail > neg_pass:
        return "to", False
    if m == 1 and neg_seen >= 2 and neg_fail > neg_pass:
        return "to", False

    divisor_strong = all(seen >= 3 and no >= 2 and yes <= 1
                         for _d, yes, no, seen in divisor_records)
    if not divisor_records:
        divisor_strong = True

    confident = (
        start_seen >= 3 and start_pass >= 2 and start_fail <= 1 and
        pos_seen >= 4 and pos_pass >= 3 and pos_fail <= 1 and
        all_model_seen >= 9 and all_model_pass >= all_model_fail + 5 and
        model_seen >= 5 and model_fail <= 1 and
        neg_seen >= 3 and neg_pass >= 3 and neg_fail <= 1 and
        divisor_strong and budget.faults == 0
    )

    # A low-confidence value still needs a positive majority, no strong model
    # contradiction, and at least one successful structural witness.
    plausible = (
        start_pass > start_fail and
        pos_pass >= 2 and pos_pass > pos_fail and
        all_model_pass >= all_model_fail and
        (neg_seen == 0 or neg_pass >= neg_fail)
    )
    if plausible:
        return "ok", bool(confident)
    return "to", False


def _finalize(budget, rng, candidate, screen, minimize=True):
    if candidate is None or candidate <= 0:
        return ("AB",) if _screen_says_ab(screen) else ("TO",)
    try:
        reduced = int(candidate)
        reduction_strong = True
        if minimize:
            reduced, reduction_strong = _minimize_multiple(
                budget, rng, reduced, trials=3
            )
        status, confident = _validate_candidate(
            budget, rng, reduced, initial_screen=screen
        )
        if status == "ab":
            return ("AB",)
        if status == "ok":
            # Weak factor-stripping evidence cannot support a confident exact
            # minimum even if the other checks happened to pass.
            return ("VAL", reduced, bool(confident and reduction_strong))
        return ("TO",)
    except (_Exhausted, _WordTooLong):
        return ("TO",)


def find_order_main(oracle, cap_calls: int, seed: int):
    """Primary solver: randomized contextual scan of offsets 1, 2, ... ."""
    rng = random.Random(seed)
    budget = _Budget(oracle, cap_calls)
    if budget.cap < 4:
        return ("TO",)

    try:
        screen_target = min(9, max(5, budget.cap // 20 + 4))
        screen = _model_screen(budget, rng, screen_target)
        if _screen_says_ab(screen):
            return ("AB",)

        reserve = min(72, max(24, budget.cap // 3))
        candidate = None
        k = 1
        while budget.remaining > reserve and k <= _MAX_WORD:
            u, v = _difference_pair(k, rng)
            ans = budget.ask(u, v)
            if ans is True:
                # Two independent formulations suppress isolated false hits.
                yes = 1
                no = 0
                for style in ((k + 1) % 6, (k + 4) % 6):
                    if budget.remaining <= reserve:
                        break
                    cu, cv = _difference_pair(k, rng, style)
                    check = budget.ask(cu, cv)
                    if check is True:
                        yes += 1
                    elif check is False:
                        no += 1
                if yes >= 2 and yes > no:
                    candidate = k
                    break
            k += 1

        return _finalize(budget, rng, candidate, screen, minimize=True)
    except (_Exhausted, _WordTooLong):
        return ("TO",)


def find_order_ref1(oracle, cap_calls: int, seed: int):
    """Reference 1: Brent power-of-two landmark cycle detector."""
    rng = random.Random(seed)
    budget = _Budget(oracle, cap_calls)
    if budget.cap < 4:
        return ("TO",)

    try:
        screen = _model_screen(budget, rng, min(7, max(5, budget.cap // 30 + 4)))
        if _screen_says_ab(screen):
            return ("AB",)

        # Brent has a larger search overhead than a linear scan (up to the
        # preceding power-of-two block), so reserve a fixed validation tail
        # instead of one third of the whole budget.
        reserve = min(58, max(32, budget.cap // 5))
        power = 1
        lam = 1
        tortoise_index = 0
        hare_index = 1
        candidate = None

        while budget.remaining > reserve and hare_index <= _MAX_WORD:
            ans = budget.ask(_canon(tortoise_index), _canon(hare_index))
            if ans is True:
                # Confirm the landmark collision in reverse orientation.  A
                # second hit is cheap and blocks a single false positive.
                if budget.remaining > reserve:
                    confirm = budget.ask(
                        _canon(hare_index), _canon(tortoise_index)
                    )
                else:
                    confirm = None
                if confirm is True or confirm is None:
                    candidate = lam
                    break

            if power == lam:
                tortoise_index = hare_index
                power *= 2
                lam = 0
            hare_index += 1
            lam += 1

        # Brent should already return the least cycle length in a noiseless
        # pure cycle, but factor stripping repairs occasional missed equality.
        return _finalize(budget, rng, candidate, screen, minimize=True)
    except (_Exhausted, _WordTooLong):
        return ("TO",)


def find_order_ref2(oracle, cap_calls: int, seed: int):
    """Reference 2: birthday collisions plus gcd of exponent differences."""
    rng = random.Random(seed)
    budget = _Budget(oracle, cap_calls)
    if budget.cap < 6:
        return ("TO",)

    try:
        screen = _model_screen(budget, rng, min(7, max(5, budget.cap // 30 + 4)))
        if _screen_says_ab(screen):
            return ("AB",)

        reserve = min(78, max(26, budget.cap // 3))
        pair_budget = max(0, budget.remaining - reserve)
        # n(n-1)/2 approximately equals pair_budget.  Cap n so sampled words
        # stay modest even when cap_calls is unexpectedly large.
        n = int((1.0 + math.sqrt(1.0 + 8.0 * pair_budget)) / 2.0)
        n = max(3, min(n, 180))
        span = min(_MAX_WORD, max(64, 16 * n * n))

        if 2 * span + 1 < n:
            return ("TO",)
        exponents = rng.sample(range(-span, span + 1), n)
        pairs = [(i, j) for i in range(n) for j in range(i)]
        rng.shuffle(pairs)

        g = 0
        confirmed_hits = 0
        for i, j in pairs:
            if budget.remaining <= reserve:
                break
            a = exponents[i]
            c = exponents[j]
            ans = budget.ask(_canon(a), _canon(c))
            if ans is not True:
                continue

            d = abs(a - c)
            # Confirm with a fresh pair having the same difference, rather
            # than merely repeating the exact oracle query.
            if budget.remaining <= reserve:
                break
            u, v = _difference_pair(d, rng)
            confirm = budget.ask(u, v)
            if confirm is True:
                g = d if g == 0 else math.gcd(g, d)
                confirmed_hits += 1
                if g == 1 or confirmed_hits >= 4:
                    break

        candidate = g if g > 0 else None
        return _finalize(budget, rng, candidate, screen, minimize=True)
    except (_Exhausted, _WordTooLong, ValueError):
        return ("TO",)


def _lcm(a, b):
    return abs(a // math.gcd(a, b) * b) if a and b else 0


def _smooth_random(rng, limit):
    primes = (2, 3, 5, 7, 11, 13)
    q = 1
    # Random multiplicative walk; stopping before overflow keeps words cheap.
    for _ in range(18):
        p = primes[rng.randrange(len(primes))]
        if q > limit // p:
            break
        if rng.randrange(100) < 68:
            q *= p
    return max(1, q)


def _multiple_probe_stream(rng, count, limit):
    values = set()
    front = []

    # Exhaustively cover a small prefix.  These are still direct divisibility
    # probes (not state-walk cycle detection), and they prevent needless
    # variance on small prime orders.
    for q0 in range(1, min(64, limit) + 1):
        front.append(q0)
        values.add(q0)

    # LCM ladder: each term covers every order dividing it.
    q = 1
    for k in range(2, 14):
        q = _lcm(q, k)
        if q <= limit:
            values.add(q)

    # Prime powers and a few structured smooth products.
    for p in (2, 3, 5, 7, 11, 13):
        q = p
        while q <= limit:
            values.add(q)
            if q > limit // p:
                break
            q *= p
    for q in (6, 12, 24, 30, 60, 120, 210, 420, 840, 1260,
              1680, 2520, 5040, 7560, 10080, 15120, 20160, 27720):
        if q <= limit:
            values.add(q)

    # Random probes provide coverage for orders with a large prime factor;
    # smooth probes heavily favor the complementary regime.
    while len(values) < max(count * 2, 24):
        if rng.randrange(2):
            values.add(rng.randint(1, limit))
        else:
            values.add(_smooth_random(rng, limit))
        if len(values) >= limit:
            break

    # Keep the guaranteed small cover first; randomize the remaining lattice
    # probes so fixed seeds still produce deterministic but diverse searches.
    rest = [q for q in values if q not in set(front)]
    rng.shuffle(rest)
    return (front + rest)[:count]


def find_order_ref3(oracle, cap_calls: int, seed: int):
    """Reference 3: hunt relation multiples in a divisibility lattice."""
    rng = random.Random(seed)
    budget = _Budget(oracle, cap_calls)
    if budget.cap < 6:
        return ("TO",)

    try:
        screen = _model_screen(budget, rng, min(7, max(5, budget.cap // 30 + 4)))
        if _screen_says_ab(screen):
            return ("AB",)

        reserve = min(78, max(26, budget.cap // 3))
        search_calls = max(0, budget.remaining - reserve)
        limit = min(_MAX_WORD, max(256, 160 * max(1, search_calls)))
        probes = _multiple_probe_stream(rng, search_calls, limit)

        candidate = None
        for q in probes:
            if budget.remaining <= reserve:
                break
            # Alternate orientation to expose gross oracle asymmetry while
            # retaining the same mathematical relation.
            if rng.randrange(2):
                u, v = "", _canon(q)
            else:
                u, v = _canon(q), ""
            ans = budget.ask(u, v)
            if ans is not True:
                continue

            # Confirm q through two contextual formulations.  Two positives
            # out of three are enough to send q to the expensive validator.
            yes = 1
            no = 0
            for _ in range(2):
                if budget.remaining <= reserve:
                    break
                cu, cv = _difference_pair(q, rng)
                check = budget.ask(cu, cv)
                if check is True:
                    yes += 1
                elif check is False:
                    no += 1
            if yes >= 2 and yes > no:
                candidate = q
                break

        return _finalize(budget, rng, candidate, screen, minimize=True)
    except (_Exhausted, _WordTooLong):
        return ("TO",)
