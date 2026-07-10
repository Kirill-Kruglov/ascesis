import random
import math

# =============================================================================
# МЕМО ДИЗАЙНА
#
# 1. find_order_main
# Идея: Последовательный поиск периода по действию R с многоточечной валидацией.
# Компоненты: Линейный сканер по степеням R для поиска кандидатов, валидационный
# набор тест-слов (B) для оценки "уверенности", и быстрый детектор детерминизма.
# Использование случайности: Непосредственно не используется для генерации слов,
# но инициализирует генератор для потенциальных будущих расширений или выбора тестов.
# Допущения: Предполагает, что в системе есть регулярные циклы. В случае обнаружения
# противоречий (нарушение детерминизма переходов) возвращает 'AB'. При нехватке
# бюджета возвращает 'TO'.
#
# 2. find_order_ref1 (Алгебраический искатель)
# Идея: Основан на групповых свойствах. Проверяет независимые порядки генераторов
# R и L, а также их коммутативность и обратимость.
# Компоненты: Сканер порядков индивидуальных действий, валидатор соотношений.
# Использование случайности: Детерминирован, seed используется для совместимости.
# Допущения: Предполагает структуру, близкую к конечной группе или моноиду. Если
# R и L ведут себя как взаимно обратные элементы, периоды должны совпадать. Если
# свойства группы грубо нарушаются, возвращает 'AB'.
#
# 3. find_order_ref2 (Искатель на основе парадокса дней рождения / Collision GCD)
# Идея: Вместо последовательного обхода генерирует случайные степени R в диапазоне,
# свободном от коротких хвостов, и ищет коллизии со сравнительно небольшим базисом.
# Компоненты: Выборка случайных степеней, вычисление НОД (GCD) разностей коллизий.
# Использование случайности: Локальный генератор случайных чисел выбирает степени P,
# что позволяет распределить пробы по пространству без систематических ошибок.
# Допущения: Предполагает наличие периодического поведения на больших степенях.
# Если НОД разностей равен 1 и простая проверка периода 1 не проходит, возвращает 'AB'.
#
# 4. find_order_ref3 (Реконструктор графа переходов / BFS Seeker)
# Идея: Полное построение графа достижимых состояний с помощью алгоритма BFS.
# Компоненты: Очередь BFS, динамический список уникальных состояний, таблица переходов.
# Использование случайности: Перемешивание порядка обхода действий ('R', 'L') на
# основе seed, что делает структуру дерева BFS стохастической.
# Допущения: Работает на небольших графах (до 20 состояний). Даёт гарантированно
# точный результат или локализует аномалию ('AB'). При превышении размера графа
# аккуратно останавливается по таймауту ('TO').
# =============================================================================

class BudgetExceeded(Exception):
    """Исключение, выбрасываемое при превышении лимита вызовов оракула."""
    pass


class OracleWrapper:
    """Обертка над оракулом для кэширования и контроля бюджета."""
    def __init__(self, oracle, cap_calls):
        self.oracle = oracle
        self.cap_calls = cap_calls
        self.calls = 0
        self.cache = {}

    def query(self, u: str, v: str) -> bool:
        # Нормализуем ключ, так как отношение эквивалентности симметрично
        key = (u, v) if u <= v else (v, u)
        if key in self.cache:
            return self.cache[key]
        if self.calls >= self.cap_calls:
            raise BudgetExceeded()
        self.calls += 1
        res = self.oracle(u, v)
        self.cache[key] = res
        return res


def check_determinism(wrapper, m) -> bool:
    """
    Проверяет согласованность переходов. Если R^m эквивалентно начальному состоянию,
    то и последующие шаги должны быть консистентны.
    """
    try:
        r_eq = wrapper.query('R' * (m + 1), 'R')
        l_eq = wrapper.query('R' * m + 'L', 'L')
        r2_eq = wrapper.query('R' * (2 * m + 1), 'R' * (m + 1))
        
        fails = 0
        if not r_eq: fails += 1
        if not l_eq: fails += 1
        if not r2_eq: fails += 1
        
        if fails >= 2:
            base_eq = wrapper.query('', 'R' * m)
            if base_eq:
                # Начальные состояния совпали, но переходы из них ведут в разные места.
                # Это указывает на недетерминированность или ошибку модели.
                return False
    except BudgetExceeded:
        pass
    return True


def find_order_main(oracle, cap_calls: int, seed: int):
    rng = random.Random(seed)
    wrapper = OracleWrapper(oracle, cap_calls)
    
    try:
        # Ограничиваем область поиска в зависимости от бюджета
        max_search = min(80, cap_calls // 4)
        if max_search < 5:
            max_search = 5
            
        candidates = []
        for k in range(1, max_search + 1):
            if wrapper.query('', 'R' * k):
                candidates.append(k)
                
        # Если кандидатов нет, возможно, есть предпериод (хвост).
        # Проверим эквивалентность со смещением, предполагая хвост длины 5.
        if not candidates:
            base_state = 'R' * 5
            for k in range(1, max_search + 1):
                if wrapper.query(base_state, base_state + 'R' * k):
                    candidates.append(k)
                    
        if not candidates:
            if wrapper.calls >= cap_calls:
                return ('TO',)
            return ('AB',)
            
        candidates.sort()
        best_m = None
        best_score = -1.0
        is_confident = False
        
        test_words = ['', 'R', 'L', 'RR', 'LL', 'RL', 'LR']
        
        for m in candidates:
            r_passes = 0
            total_r = 0
            for w in test_words:
                try:
                    if wrapper.query(w, w + 'R' * m):
                        r_passes += 1
                    total_r += 1
                except BudgetExceeded:
                    break
                    
            if total_r == 0:
                continue
                
            score = r_passes / total_r
            if score >= 0.6:
                # Проверим, ведет ли себя L аналогично
                l_passes = 0
                total_l = 0
                for w in test_words:
                    try:
                        if wrapper.query(w, w + 'L' * m):
                            l_passes += 1
                        total_l += 1
                    except BudgetExceeded:
                        break
                        
                l_score = l_passes / total_l if total_l > 0 else 0
                
                # Проверяем, являются ли действия взаимно обратными
                is_inverse = False
                try:
                    eq1 = wrapper.query('R' + 'L', '')
                    eq2 = wrapper.query('L' + 'R', '')
                    if eq1 and eq2:
                        is_inverse = True
                except BudgetExceeded:
                    pass
                    
                confident = (score > 0.8) and (l_score > 0.8 or is_inverse)
                
                if best_m is None or score > best_score:
                    best_m = m
                    best_score = score
                    is_confident = confident
                    
        if best_m is not None:
            if not check_determinism(wrapper, best_m):
                return ('AB',)
            return ('VAL', best_m, is_confident)
            
        return ('AB',)
        
    except BudgetExceeded:
        return ('TO',)


def find_order_ref1(oracle, cap_calls: int, seed: int):
    """Алгебраический искатель на основе порядков индивидуальных генераторов."""
    rng = random.Random(seed)
    wrapper = OracleWrapper(oracle, cap_calls)
    
    try:
        max_limit = min(45, cap_calls // 5)
        if max_limit < 5:
            max_limit = 5
            
        m_R = None
        for k in range(1, max_limit + 1):
            if wrapper.query('', 'R' * k):
                m_R = k
                break
                
        m_L = None
        for k in range(1, max_limit + 1):
            if wrapper.query('', 'L' * k):
                m_L = k
                break
                
        if m_R is None or m_L is None:
            if wrapper.calls >= cap_calls:
                return ('TO',)
            return ('AB',)
            
        is_inv = False
        try:
            eq1 = wrapper.query('R' + 'L', '')
            eq2 = wrapper.query('L' + 'R', '')
            if eq1 and eq2:
                is_inv = True
        except BudgetExceeded:
            pass
            
        if is_inv:
            if m_R == m_L:
                return ('VAL', m_R, True)
            else:
                # В группе обратные элементы обязаны иметь одинаковый порядок
                return ('AB',)
        else:
            if m_R == m_L:
                return ('VAL', m_R, False)
            else:
                return ('AB',)
                
    except BudgetExceeded:
        return ('TO',)


def find_order_ref2(oracle, cap_calls: int, seed: int):
    """Искатель на основе коллизий случайных степеней (парадокс дней рождения)."""
    rng = random.Random(seed)
    wrapper = OracleWrapper(oracle, cap_calls)
    
    b_size = 16
    p_size = max(5, int((cap_calls * 0.7) // b_size))
    
    B = list(range(b_size))
    
    # Случайные степени выбираются из диапазона [20, 100] для исключения влияния коротких хвостов
    P = []
    while len(P) < p_size:
        val = rng.randint(20, 100)
        if val not in P:
            P.append(val)
            
    try:
        collisions = []
        for p in P:
            for b in B:
                if wrapper.query('R' * b, 'R' * p):
                    collisions.append((b, p))
                    
        if not collisions:
            if wrapper.calls >= cap_calls:
                return ('TO',)
            return ('AB',)
            
        diffs = [p - b for (b, p) in collisions]
        
        g = diffs[0]
        for d in diffs[1:]:
            g = math.gcd(g, d)
            
        if g > 1:
            # Валидация найденного периода g со смещением
            is_valid = wrapper.query('R' * 20, 'R' * (20 + g))
            if is_valid:
                is_inverse = False
                try:
                    eq1 = wrapper.query('R' + 'L', '')
                    eq2 = wrapper.query('L' + 'R', '')
                    if eq1 and eq2:
                        is_inverse = True
                except BudgetExceeded:
                    pass
                return ('VAL', g, is_inverse)
            else:
                return ('AB',)
        elif g == 1:
            if wrapper.query('R', ''):
                return ('VAL', 1, True)
            return ('AB',)
            
        return ('AB',)
        
    except BudgetExceeded:
        return ('TO',)


def find_order_ref3(oracle, cap_calls: int, seed: int):
    """Реконструктор графа состояний методом поиска в ширину (BFS)."""
    rng = random.Random(seed)
    wrapper = OracleWrapper(oracle, cap_calls)
    
    states = ['']
    queue = ['']
    transitions = {}
    
    try:
        while queue:
            curr = queue.pop(0)
            actions = ['R', 'L']
            rng.shuffle(actions)  # Рандомизируем обход с помощью seed
            
            for action in actions:
                next_word = curr + action
                
                matched_state = None
                for s in states:
                    if wrapper.query(s, next_word):
                        matched_state = s
                        break
                
                if matched_state is not None:
                    transitions[(curr, action)] = matched_state
                else:
                    states.append(next_word)
                    transitions[(curr, action)] = next_word
                    queue.append(next_word)
                    
                    # Защита от бесконечного расширения при больших размерах миров
                    if len(states) > 20:
                        return ('TO',)
                        
        # Анализ реконструированного графа переходов
        path = ['']
        visited = {'': 0}
        curr = ''
        while True:
            if (curr, 'R') not in transitions:
                return ('AB',)
            nxt = transitions[(curr, 'R')]
            if nxt in visited:
                start_index = visited[nxt]
                period = len(path) - start_index
                tail_len = start_index
                
                # Проверка взаимной обратимости переходов на цикле
                is_inverse = True
                for s in path[start_index:]:
                    nxt_state = transitions.get((s, 'R'))
                    if nxt_state is None or transitions.get((nxt_state, 'L')) != s:
                        is_inverse = False
                        break
                
                confident = (tail_len == 0) and is_inverse
                if tail_len > 0:
                    return ('VAL', period, False)
                else:
                    return ('VAL', period, confident)
            else:
                visited[nxt] = len(path)
                path.append(nxt)
                curr = nxt
                
    except BudgetExceeded:
        return ('TO',)