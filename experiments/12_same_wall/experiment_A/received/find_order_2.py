import random
import math

# ============================================================
# Мемо дизайна (для каждой функции)
# ============================================================
#
# find_order_main:
#   Идея: комбинированный подход — сначала случайный поиск коллизий (birthday paradox)
#   на степенях R для нахождения кратного M периода m (с O(1) вызовами в среднем при
#   наличии коллизии), затем факторизация M и поиск минимального делителя d, для которого
#   oracle(R^d, '') == True. Если коллизий нет — fallback на линейный поиск.
#   Использует L только для проверки базовых допущений (RL и LR приводят в старт).
#   Случайность: Random(seed) для выбора экспонент и shuffle пар. 
#   Допущения о мире: часто чистый цикл под R, L ≈ R^{-1}, редкие ошибки оракула tolerable
#     (через conf=False при частичных несоответствиях). 
#   Абстинирует (AB): если RL/LR не дают id (нарушение типичной структуры), или
#     inconsistency после коллизии. TO — если бюджет исчерпан или m слишком велик/нет коллизий.
#   Устойчивость к ошибкам: базовые проверки + verif 2m; conf=False если verif частично fail.
#
# find_order_ref1:
#   Идея: простой детерминированный линейный поиск наименьшего cand, где oracle('R'*cand, '')
#     истинно (поскольку идёт по возрастанию — это m). 
#   Механизм: последовательная проверка степеней R от 1 до cap.
#   Случайность: не использует (инициализирует rng для единообразия API).
#   Допущения: мир имеет период под действием только R (L не используется).
#   Абстинирует: TO если m > cap_calls (честная деградация), AB если '' != '' или
#     RL/LR не id (базовая проверка структуры).
#
# find_order_ref2:
#   Идея: алгоритм Флойда (Floyd's cycle detection / rho) для обнаружения цикла в
#     последовательности состояний под repeated R. Находит mu (хвост) и lam (длина цикла).
#   Механизм: полностью основан на сравнениях позиций (экспонент) без использования L;
#     только powers of R и сравнения состояний.
#   Случайность: не использует.
#   Допущения: последовательность под R eventually periodic; если mu==0 — старт на цикле,
#     период = lam.
#   Абстинирует: AB если mu > 0 (хвост, орбита не замкнута с старта — нарушает
#     "чистый цикл"), или TO при превышении MAX_POS/бюджета.
#
# find_order_ref3:
#   Идея: полный BFS-обход орбиты с использованием обоих генераторов R и L;
#     построение графа переходов, подсчёт |orbit| = m, проверка что это в точности
#     один цикл длины m под R, и L является обратным циклом (RL=LR=id на всех).
#   Механизм: явное исследование всех достижимых слов/состояний через применения R/L,
#     кластеризация эквивалентных через oracle, запись succ.
#   Случайность: не использует.
#   Допущения: мир порождает конечную орбиту под монойдом <R,L>, действия детерминированы;
#     типичная структура — цикл (а не дерево+цикл с хвостом или несколько компонент).
#   Абстинирует: AB если после полного исследования структура не является чистым циклом
#     (хвосты, не-surjective, L не inverse и т.д.), TO если бюджет не позволил
#     исследовать всю орбиту (m большое).
#
# Общие замечания:
# - Все функции уважают cap_calls (через safe_oracle).
# - При ошибках оракула (редких) main более терпим (conf), refs — строже (AB/TO).
# - MAX_LEN/MAX_POS ограничены ~1000-10000 чтобы избежать проблем с памятью длинных строк.
# - Выбор: основной — гибридный randomized + verification; refs — разные классические
#   алгоритмы (linear, rho, BFS graph).
# ============================================================

def find_order_main(oracle, cap_calls, seed):
    rng = random.Random(seed)
    calls = 0
    MAX_EXP = 5000
    NUM_SAMPLES = 35

    def safe_oracle(u, v):
        nonlocal calls
        if calls >= cap_calls:
            return None
        res = oracle(u, v)
        calls += 1
        return res

    # trivial consistency
    res = safe_oracle('', '')
    if res is None:
        return ('TO',)
    if not res:
        return ('AB',)

    # birthday samples (include 0 for direct checks)
    samples = [0] + [rng.randint(1, MAX_EXP) for _ in range(NUM_SAMPLES - 1)]
    pairs = [(i, j) for i in range(len(samples)) for j in range(i + 1, len(samples))
             if samples[i] != samples[j]]
    rng.shuffle(pairs)

    found_M = None
    for ii, jj in pairs:
        k1, k2 = samples[ii], samples[jj]
        res = safe_oracle('R' * k1, 'R' * k2)
        if res is None:
            return ('TO',)
        if res:
            found_M = abs(k1 - k2)
            break

    m_cand = None
    if found_M is not None and found_M > 0:
        # factor and find minimal d | found_M with oracle True
        def get_divisors(n):
            if n <= 0:
                return []
            divs = set()
            for i in range(1, int(math.isqrt(n)) + 1):
                if n % i == 0:
                    divs.add(i)
                    divs.add(n // i)
            return sorted(d for d in divs if d > 0)
        divs = get_divisors(found_M)
        for d in divs:
            res = safe_oracle('R' * d, '')
            if res is None:
                return ('TO',)
            if res:
                m_cand = d
                break
        if m_cand is None:
            return ('AB',)  # inconsistency after collision
    else:
        # fallback: linear search with remaining budget
        remaining = cap_calls - calls
        for cand in range(1, remaining + 1):
            res = safe_oracle('R' * cand, '')
            if res is None:
                return ('TO',)
            if res:
                m_cand = cand
                break

    if m_cand is None or m_cand <= 0:
        return ('TO',)

    # verification + L checks (assumption that L ~ inverse of R)
    for w in ('RL', 'LR'):
        res = safe_oracle(w, '')
        if res is None:
            return ('TO',)
        if not res:
            return ('AB',)

    # extra verif for robustness to rare oracle errors
    res = safe_oracle('R' * (2 * m_cand), '')
    if res is None:
        return ('TO',)
    confident = bool(res)

    return ('VAL', m_cand, confident)


def find_order_ref1(oracle, cap_calls, seed):
    rng = random.Random(seed)  # for API consistency, not used
    calls = 0

    def safe_oracle(u, v):
        nonlocal calls
        if calls >= cap_calls:
            return None
        res = oracle(u, v)
        calls += 1
        return res

    res = safe_oracle('', '')
    if res is None:
        return ('TO',)
    if not res:
        return ('AB',)

    MAX_CAND = min(cap_calls, 10000)
    for cand in range(1, MAX_CAND + 1):
        res = safe_oracle('R' * cand, '')
        if res is None:
            return ('TO',)
        if res:
            # basic structure check
            for w in ('RL', 'LR'):
                r = safe_oracle(w, '')
                if r is None:
                    return ('TO',)
                if not r:
                    return ('AB',)
            return ('VAL', cand, True)
    return ('TO',)


def find_order_ref2(oracle, cap_calls, seed):
    rng = random.Random(seed)  # unused
    calls = 0
    MAX_POS = 2000

    def safe_oracle(u, v):
        nonlocal calls
        if calls >= cap_calls:
            return None
        res = oracle(u, v)
        calls += 1
        return res

    def pos_word(p):
        if p > MAX_POS or p < 0:
            return None
        return 'R' * p

    def same_pos(p1, p2):
        w1 = pos_word(p1)
        w2 = pos_word(p2)
        if w1 is None or w2 is None:
            return None
        return safe_oracle(w1, w2)

    res = safe_oracle('', '')
    if res is None:
        return ('TO',)
    if not res:
        return ('AB',)

    # Floyd phase 1: find meeting point
    tort = 0
    hare = 0
    while True:
        tort += 1
        hare += 2
        if tort > MAX_POS or hare > MAX_POS:
            return ('TO',)
        eq = same_pos(tort, hare)
        if eq is None:
            return ('TO',)
        if eq:
            break

    # phase 2: find mu (tail length)
    mu = 0
    slow = 0
    fast = hare
    while True:
        eq = same_pos(slow, fast)
        if eq is None:
            return ('TO',)
        if eq:
            break
        slow += 1
        fast += 1
        mu += 1
        if slow > MAX_POS or fast > MAX_POS:
            return ('TO',)

    # phase 3: find lam (cycle length)
    lam = 1
    fast = slow + 1
    if fast > MAX_POS:
        return ('TO',)
    while True:
        eq = same_pos(slow, fast)
        if eq is None:
            return ('TO',)
        if eq:
            break
        fast += 1
        lam += 1
        if fast > MAX_POS:
            return ('TO',)

    if mu == 0:
        # start on cycle => period = lam
        wlam = pos_word(lam)
        if wlam is None:
            return ('TO',)
        res = safe_oracle(wlam, '')
        if res is None:
            return ('TO',)
        if not res:
            return ('AB',)
        return ('VAL', lam, True)
    else:
        # tail present => not pure closed orbit from start
        return ('AB',)


def find_order_ref3(oracle, cap_calls, seed):
    rng = random.Random(seed)  # unused
    calls = 0

    def safe_oracle(u, v):
        nonlocal calls
        if calls >= cap_calls:
            return None
        res = oracle(u, v)
        calls += 1
        return res

    res = safe_oracle('', '')
    if res is None:
        return ('TO',)
    if not res:
        return ('AB',)

    # BFS exploration of orbit using R and L
    states = ['']          # rep words for states
    trans_R = [None]
    trans_L = [None]
    queue = [0]            # indices to expand

    while queue:
        idx = queue.pop(0)
        w = states[idx]
        for act, tlist in (('R', trans_R), ('L', trans_L)):
            new_w = w + act
            target = None
            for j in range(len(states)):
                eq = safe_oracle(new_w, states[j])
                if eq is None:
                    return ('TO',)
                if eq:
                    target = j
                    break
            if target is None:
                # discover new state
                states.append(new_w)
                trans_R.append(None)
                trans_L.append(None)
                target = len(states) - 1
                queue.append(target)
            # record transition
            if act == 'R':
                trans_R[idx] = target
            else:
                trans_L[idx] = target

    m = len(states)
    if m == 0:
        return ('AB',)

    # check all trans set
    if any(t is None for t in trans_R) or any(t is None for t in trans_L):
        return ('TO',)  # incomplete exploration

    # check R forms a single cycle of length m starting from 0
    current = 0
    visited = set()
    for _ in range(m):
        if current in visited:
            return ('AB',)
        visited.add(current)
        current = trans_R[current]
    if current != 0 or len(visited) != m:
        return ('AB',)

    # check L is the inverse cycle (RL = LR = id everywhere)
    for i in range(m):
        if trans_L[trans_R[i]] != i or trans_R[trans_L[i]] != i:
            return ('AB',)

    return ('VAL', m, True)


# Optional self-test (not executed on import, but can run manually)
if __name__ == "__main__":
    print("find_order.py loaded successfully. Functions defined:")
    print("  find_order_main, find_order_ref1, find_order_ref2, find_order_ref3")
