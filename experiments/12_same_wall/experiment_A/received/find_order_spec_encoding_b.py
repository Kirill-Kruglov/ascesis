"""Определители периода кнопочного автомата.

Публичный контракт: find_order_main / find_order_ref1 / find_order_ref2 /
find_order_ref3. Все обращения к oracle проходят через общий счётчик,
поэтому cap_calls никогда не превышается. Вся случайность локальна и
порождается только random.Random(seed).

Ни один конечный набор запросов не может доказать корректность произвольного
чёрного ящика на всех неиспрошенных словах. Поэтому confident=True означает
сильный конечный сертификат модели на разнообразных проверках, а не
математическое доказательство для враждебного оракула.
"""

import random
import math


class _NoBudget(Exception):
    pass


class _OracleError(Exception):
    pass


class _Budget:
    """Single place where calls are counted; a failed oracle call also costs one."""

    def __init__(self, oracle, cap_calls):
        self.oracle = oracle
        self.cap = max(0, int(cap_calls))
        self.used = 0

    def left(self):
        return self.cap - self.used

    def ask(self, p1, p2):
        if self.used >= self.cap:
            raise _NoBudget()
        self.used += 1
        try:
            return bool(self.oracle(p1, p2))
        except Exception as exc:
            raise _OracleError() from exc


def _majority(budget, p1, p2):
    """Three identical readings. Used only for decisions that create a candidate."""
    if budget.left() < 3:
        raise _NoBudget()
    s = 0
    if budget.ask(p1, p2):
        s += 1
    if budget.ask(p1, p2):
        s += 1
    if budget.ask(p1, p2):
        s += 1
    return s >= 2


def _guard(budget, p1, p2, expected):
    """
    Cheap in the normal case: one call.
    A disagreement is read twice more, so one isolated flipped answer is tolerated.
    """
    if budget.left() < 1:
        raise _NoBudget()
    first = budget.ask(p1, p2)
    if first == expected:
        return True
    if budget.left() < 2:
        raise _NoBudget()
    second = budget.ask(p1, p2)
    third = budget.ask(p1, p2)
    votes_for_expected = int(first == expected) + int(second == expected) + int(third == expected)
    return votes_for_expected >= 2


def _distinct_prime_factors(n):
    out = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d = 3 if d == 2 else d + 2
    if n > 1:
        out.append(n)
    return out


def _reduce_confirmed_multiple(budget, value):
    """
    If value is a confirmed multiple of the true order, strip prime factors.
    Every successful stripping step is decided by a 2-of-3 reading.
    """
    value = int(value)
    changed = True
    while changed:
        changed = False
        for p in _distinct_prime_factors(value):
            while value % p == 0:
                q = value // p
                if _majority(budget, "", "R" * q):
                    value = q
                    changed = True
                else:
                    break
    return value


def _word_residue(word, m):
    delta = 0
    for ch in word:
        if ch == "R":
            delta += 1
        else:
            delta -= 1
    return delta % m


def _random_word(rng, length):
    return "".join("R" if rng.getrandbits(1) else "L" for _ in range(length))


def _precheck(budget, level):
    """
    Fast algebraic sanity checks shared by all search methods.
    Returns False only after a robustly observed model violation.
    """
    tests = [
        ("", "", True),
        ("RL", "", True),
        ("LR", "", True),
        ("RLR", "R", True),
        ("LRL", "L", True),
        ("RRLL", "", True),
    ]
    count = min(max(1, int(level)), len(tests))
    for p1, p2, expected in tests[:count]:
        if not _guard(budget, p1, p2, expected):
            return False
    return True


def _validate_candidate(budget, rng, m, desired_random_checks):
    """
    Validate both the R-cycle and the claim that L is its inverse.

    Return values:
      ('AB',)  -- a reproducible contradiction was found;
      ('TO',)  -- too little budget remains for a minimally useful certificate;
      bool     -- candidate accepted; bool is the confidence flag.
    """
    if not isinstance(m, int) or m < 1:
        return ("AB",)

    score = 0

    # These are candidate-defining facts, so always use 2-of-3.
    try:
        if not _majority(budget, "", "R" * m):
            return ("AB",)
        score += 2
        if not _majority(budget, "", "L" * m):
            return ("AB",)
        score += 2
    except _NoBudget:
        return ("TO",)

    deterministic = []
    if m == 1:
        deterministic.extend([
            ("R", "", True),
            ("L", "", True),
            ("RL", "", True),
        ])
    else:
        deterministic.extend([
            ("R" * (m - 1), "L", True),
            ("L" * (m - 1), "R", True),
            ("R" * (m + 1), "R", True),
            ("L" * (m + 1), "L", True),
        ])
        for p in _distinct_prime_factors(m):
            deterministic.append(("", "R" * (m // p), False))
            deterministic.append(("", "L" * (m // p), False))

    for p1, p2, expected in deterministic:
        if budget.left() < 3:
            break
        try:
            if not _guard(budget, p1, p2, expected):
                return ("AB",)
        except _NoBudget:
            break
        score += 1

    checks_done = 0
    desired_random_checks = max(0, int(desired_random_checks))
    while checks_done < desired_random_checks and budget.left() >= 3:
        mode = checks_done % 4

        if mode == 0:
            # Arbitrary mixed word must reduce to its signed displacement.
            length = rng.randrange(0, min(4 * m + 9, 97))
            word = _random_word(rng, length)
            residue = _word_residue(word, m)
            p1, p2, expected = word, "R" * residue, True

        elif mode == 1:
            # Cancellation must remain valid inside arbitrary contexts.
            left = _random_word(rng, rng.randrange(0, min(m + 5, 33)))
            right = _random_word(rng, rng.randrange(0, min(m + 5, 33)))
            middle = "RL" if rng.getrandbits(1) else "LR"
            p1, p2, expected = left + middle + right, left + right, True

        elif mode == 2:
            # Equal residues represented in deliberately different ways.
            a = rng.randrange(0, 3 * m + 1)
            q = rng.randrange(1, 5)
            b = a + q * m
            if rng.getrandbits(1):
                p1, p2 = "R" * a, "R" * b
            else:
                p1, p2 = "L" * a, "L" * b
            expected = True

        else:
            # Distinct residues must not compare equal.
            if m == 1:
                p1, p2, expected = "R", "", True
            else:
                a = rng.randrange(0, m)
                jump = rng.randrange(1, m)
                b = (a + jump) % m
                p1, p2, expected = "R" * a, "R" * b, False

        try:
            if not _guard(budget, p1, p2, expected):
                return ("AB",)
        except _NoBudget:
            break
        score += 1
        checks_done += 1

    # Below this, a period guess exists but the evidence is too thin.
    if score < 8:
        return ("TO",)

    # True requires a broad mixed-word certificate; False is still a checked value,
    # not an unverified guess.
    confident = score >= 18 and checks_done >= 10
    return confident


def find_order_main(oracle, cap_calls: int, seed: int):
    """
    ОСНОВНОЙ МЕТОД: детерминированный поиск первого подтверждённого возврата
    R^k к начальному состоянию, затем арифметическое сокращение найденного
    кратного и широкая рандомизированная проверка смешанных слов.

    Роль случайности: только выбор независимых проверочных слов и контекстов;
    источник строго random.Random(seed).

    Допущения: на корректном ящике достижимые состояния образуют один цикл,
    R сдвигает на +1, L на -1, а oracle сравнивает конечные состояния.

    Отказ: AB при устойчивом нарушении рефлексивности, взаимной обратимости,
    минимальности или модульных тождеств; TO, если возврат не найден либо на
    минимальный сертификат не осталось вызовов. Одиночный сбой чтения
    перепроверяется; решения, создающие кандидат, принимаются по 2 из 3.
    """
    rng = random.Random(seed)
    budget = _Budget(oracle, cap_calls)

    try:
        if budget.cap < 10:
            return ("TO",)
        if not _precheck(budget, 5):
            return ("AB",)

        reserve = min(56, max(14, budget.cap // 5))
        search_stop = max(budget.used, budget.cap - reserve)
        hit = None
        k = 1

        while budget.used < search_stop:
            answer = budget.ask("", "R" * k)
            if answer:
                if budget.left() < 2:
                    return ("TO",)
                # Complete a 2-of-3 confirmation including the first answer.
                a2 = budget.ask("", "R" * k)
                a3 = budget.ask("", "R" * k)
                if 1 + int(a2) + int(a3) >= 2:
                    hit = k
                    break
            k += 1

        if hit is None:
            return ("TO",)

        m = _reduce_confirmed_multiple(budget, hit)
        verdict = _validate_candidate(budget, rng, m, 20)
        if isinstance(verdict, tuple):
            return verdict
        return ("VAL", m, verdict)

    except _NoBudget:
        return ("TO",)
    except _OracleError:
        return ("AB",)


def find_order_ref1(oracle, cap_calls: int, seed: int):
    """
    ЗАПАСНОЙ МЕТОД 1 — алгоритм Брента для траектории R.

    Принцип поиска: сравниваются две точки одной R-траектории с длинами,
    организованными удваивающимися блоками. Это поиск цикла, а не перебор
    возвратов к пустой программе. Найденная длина цикла принимается только
    если сам начальный узел лежит на этом цикле.

    Роль случайности: цикл ищется детерминированно; локальный RNG выбирает
    лишь последующие тесты L и смешанных программ.

    Допущения: R задаёт детерминированное отображение; в модели периода
    предцикл имеет длину ноль, а L — обратный сдвиг.

    Отказ: AB при ненулевом предцикле или нарушении алгебры; TO, если
    столкновение Брента или проверочный сертификат не помещаются в cap_calls.
    """
    rng = random.Random(seed)
    budget = _Budget(oracle, cap_calls)

    try:
        if budget.cap < 10:
            return ("TO",)
        if not _precheck(budget, 3):
            return ("AB",)

        reserve = min(40, max(14, budget.cap // 6))
        stop = max(budget.used, budget.cap - reserve)

        power = 1
        lam = 1
        tortoise = 0
        hare = 1
        found = False

        while budget.used < stop:
            first = budget.ask("R" * tortoise, "R" * hare)
            if first:
                if budget.left() < 2:
                    return ("TO",)
                second = budget.ask("R" * tortoise, "R" * hare)
                third = budget.ask("R" * tortoise, "R" * hare)
                if 1 + int(second) + int(third) >= 2:
                    found = True
                    break
            if power == lam:
                tortoise = hare
                power *= 2
                lam = 0
            hare += 1
            lam += 1

        if not found:
            return ("TO",)

        # The common validator now checks that the initial node itself lies
        # on the detected cycle; a transient R-orbit is therefore rejected.
        verdict = _validate_candidate(budget, rng, lam, 16)
        if isinstance(verdict, tuple):
            return verdict
        return ("VAL", lam, verdict)

    except _NoBudget:
        return ("TO",)
    except _OracleError:
        return ("AB",)


def find_order_ref2(oracle, cap_calls: int, seed: int):
    """
    ЗАПАСНОЙ МЕТОД 2 — рандомизированное сито кратных и НОД.

    Принцип поиска: в большом диапазоне без повторов выбираются случайные k.
    Истинные ответы на сравнение R^k с пустой программой дают кратные периода.
    НОД нескольких подтверждённых попаданий, а затем деление простых факторов,
    восстанавливают минимальный период.

    Роль случайности: центральная — RNG определяет весь порядок и набор проб.

    Допущения: R^a == R^b ровно тогда, когда период делит a-b; L проверяется
    только после восстановления кандидата.

    Отказ: AB при устойчивом противоречии модели; TO, если случайное сито не
    поймало ни одного кратного или не хватило ресурса на сертификат.
    """
    rng = random.Random(seed)
    budget = _Budget(oracle, cap_calls)

    try:
        if budget.cap < 12:
            return ("TO",)
        if not _precheck(budget, 4):
            return ("AB",)

        reserve = min(64, max(18, budget.cap // 4))
        stop = max(budget.used, budget.cap - reserve)
        max_exp = max(64, min(12000, budget.cap * 16))
        seen = set()
        hits = []

        while budget.used < stop and len(seen) < max_exp and len(hits) < 5:
            k = rng.randrange(1, max_exp + 1)
            if k in seen:
                continue
            seen.add(k)

            first = budget.ask("", "R" * k)
            if first and budget.left() >= 2:
                second = budget.ask("", "R" * k)
                third = budget.ask("", "R" * k)
                if 1 + int(second) + int(third) >= 2:
                    hits.append(k)

        if not hits:
            return ("TO",)

        g = hits[0]
        for value in hits[1:]:
            g = math.gcd(g, value)

        m = _reduce_confirmed_multiple(budget, g)
        verdict = _validate_candidate(budget, rng, m, 18)
        if isinstance(verdict, tuple):
            return verdict
        return ("VAL", m, verdict)

    except _NoBudget:
        return ("TO",)
    except _OracleError:
        return ("AB",)


def find_order_ref3(oracle, cap_calls: int, seed: int):
    """
    ЗАПАСНОЙ МЕТОД 3 — birthday-поиск столкновений без опоры на начало.

    Принцип поиска: выбирается набор случайных степеней R^e, затем попарно
    сравниваются их конечные состояния. Разность показателей подтверждённой
    пары — кратное периода. НОД нескольких разностей и факторное сокращение
    дают минимальный кандидат. Во время самого поиска пустая программа не
    используется.

    Роль случайности: RNG задаёт показатели и перемешивает порядок пар.

    Допущения: R-орбита является чистым циклом; тогда столкновения степеней
    эквивалентны делимости разности на период.

    Отказ: AB при нарушении чистого цикла, обратимости L или проверочных
    тождеств; TO при отсутствии birthday-столкновения либо нехватке вызовов.
    """
    rng = random.Random(seed)
    budget = _Budget(oracle, cap_calls)

    try:
        if budget.cap < 14:
            return ("TO",)
        if not _precheck(budget, 2):
            return ("AB",)

        reserve = min(62, max(18, budget.cap // 4))
        pair_budget = max(0, budget.cap - reserve - budget.used)

        # Largest s with s*(s-1)/2 <= pair_budget.
        s = int((1.0 + math.sqrt(1.0 + 8.0 * pair_budget)) / 2.0)
        while s * (s - 1) // 2 > pair_budget:
            s -= 1
        if s < 2:
            return ("TO",)

        max_exp = max(64, min(16000, budget.cap * 24))
        exponents = set()
        while len(exponents) < s:
            exponents.add(rng.randrange(1, max_exp + 1))
        exponents = list(exponents)

        pairs = []
        for i in range(s):
            for j in range(i + 1, s):
                pairs.append((i, j))
        rng.shuffle(pairs)

        diffs = []
        for i, j in pairs:
            if budget.used >= budget.cap - reserve:
                break
            a = exponents[i]
            c = exponents[j]
            first = budget.ask("R" * a, "R" * c)
            if first and budget.left() >= 2:
                second = budget.ask("R" * a, "R" * c)
                third = budget.ask("R" * a, "R" * c)
                if 1 + int(second) + int(third) >= 2:
                    diffs.append(abs(a - c))
                    if len(diffs) >= 5:
                        break

        if not diffs:
            return ("TO",)

        g = diffs[0]
        for value in diffs[1:]:
            g = math.gcd(g, value)

        m = _reduce_confirmed_multiple(budget, g)
        verdict = _validate_candidate(budget, rng, m, 16)
        if isinstance(verdict, tuple):
            return verdict
        return ("VAL", m, verdict)

    except _NoBudget:
        return ("TO",)
    except _OracleError:
        return ("AB",)
