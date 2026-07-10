import math
import random

# =====================================================================
# Наборы параметров для различных типов миров.
# Каждому типу соответствует ровно 8 кортежей с параметрами в заданных диапазонах.
# =====================================================================
WORLD_TUPLES = {
    'cycle': [17, 21, 25, 29, 31, 35, 37, 40],
    'alias': [
        (20, 4), (20, 5), (24, 4), (24, 6), 
        (30, 5), (30, 6), (36, 6), (36, 9)
    ],
    'noisy': [
        (19, 0.02), (23, 0.04), (27, 0.05), (31, 0.07), 
        (33, 0.08), (35, 0.10), (38, 0.11), (40, 0.12)
    ],
    'qtrap': [
        (15, 5, 0.6), (18, 6, 0.6), (21, 7, 0.6), (24, 8, 0.6), 
        (27, 9, 0.6), (20, 5, 0.6), (24, 6, 0.6), (28, 7, 0.6)
    ],
    'wobble': [18, 22, 26, 28, 30, 32, 36, 39],
    'lollipop': [
        (5, 12), (7, 15), (9, 18), (10, 20), 
        (11, 22), (12, 24), (8, 25), (12, 26)
    ],
    'nonstat': [
        (15, 27, 60), (18, 30, 80), (20, 32, 100), (22, 35, 120), 
        (24, 38, 140), (25, 40, 160), (26, 39, 180), (24, 36, 200)
    ]
}


# =====================================================================
# Вспомогательный класс для надежного опроса оракула с контролем лимита вызовов.
# Поддерживает мажоритарное голосование для борьбы с шумом.
# =====================================================================
class RobustOracle:
    def __init__(self, oracle, cap_calls):
        self.oracle = oracle
        self.cap_calls = cap_calls
        self.calls = 0
        self.raw_cache = {}

    def query_raw(self, u, v):
        """Выполняет один прямой запрос к оракулу с проверкой лимита."""
        if u > v:
            u, v = v, u
        if self.calls >= self.cap_calls:
            raise TimeoutError()
        self.calls += 1
        val = self.oracle(u, v)
        if (u, v) not in self.raw_cache:
            self.raw_cache[(u, v)] = []
        self.raw_cache[(u, v)].append(val)
        return val

    def query(self, u, v, repeats=1):
        """Возвращает мажоритарное значение по результатам нескольких попыток."""
        if u > v:
            u, v = v, u
        
        existing = self.raw_cache.get((u, v), [])
        needed = repeats - len(existing)
        for _ in range(needed):
            self.query_raw(u, v)
            
        trues = sum(self.raw_cache[(u, v)][:repeats])
        return trues > repeats / 2


def detect_noise(robust_oracle):
    """
    Оценивает наличие шума в оракуле с помощью небольшого числа тестовых запросов.
    """
    test_pairs = [("", ""), ("R", "R"), ("R", "L")]
    for u, v in test_pairs:
        results = []
        for _ in range(5):
            try:
                results.append(robust_oracle.query_raw(u, v))
            except TimeoutError:
                break
        if len(set(results)) > 1:
            return True
    return False


# =====================================================================
# ПРИНЦИПЫ И МЕХАНИЗМЫ РАБОТЫ СОЛВЕРОВ (Описание)
#
# 1. solver_main:
#    - Метод: Прямое сканирование кандидатов периода по орбите R^i.
#    - Логика: Находит потенциальные совпадения R^start_i и R^(start_i + k) для k в рабочем диапазоне.
#      Затем верифицирует отобранных кандидатов на дополнительных точках и суффиксах (например, с 'L').
#    - Допущение: Последовательность состояний, порождаемая R^i, выходит на стационарный цикл в пределах
#      используемых глубин.
#    - Условие AB: Если ни один кандидат периода не прошел базовые тесты или не обнаружено периодичности.
#    - Условие TO: Превышен лимит вызовов оракула (обрабатывается перехватом TimeoutError).
#
# 2. solver_indep:
#    - Метод: Анализ многомерных сигнатур (fingerprinting) и расчет автокорреляционного профиля расстояний.
#    - Логика: Для каждого шага i на орбите R^i строится вектор ответов (профиль эквивалентности) по отношению
#      к фиксированному набору тестовых слов-зондов. Период ищется как сдвиг p, минимизирующий среднее
#      расстояние Хэмминга между профилями F(i) и F(i+p).
#    - Различие механизмов: solver_main осуществляет точечные парные сравнения на фиксированном расстоянии,
#      тогда как solver_indep строит инвариантное векторное описание каждого состояния и ищет глобальную
#      периодичность в последовательности этих векторов (что значительно устойчивее к локальным аномалиям).
# =====================================================================

def solver_main(oracle, cap_calls, seed):
    robust = RobustOracle(oracle, cap_calls)
    try:
        is_noisy = detect_noise(robust)
        repeats_scan = 5 if is_noisy else 1
        repeats_verify = 7 if is_noisy else 1
        
        # Адаптация параметров под оставшийся бюджет
        max_k = 50
        start_i = 16
        if cap_calls < 120:
            max_k = 25
            repeats_scan = 1
            repeats_verify = 1
        elif cap_calls < 300:
            max_k = 40
            repeats_scan = 3 if is_noisy else 1
            repeats_verify = 3 if is_noisy else 1

        candidates = []
        for k in range(1, max_k + 1):
            if robust.query("R" * start_i, "R" * (start_i + k), repeats=repeats_scan):
                candidates.append(k)
                
        if not candidates and start_i > 10:
            # Попытка поиска с измененной стартовой позиции
            start_i = 25
            for k in range(1, max_k + 1):
                if robust.query("R" * start_i, "R" * (start_i + k), repeats=repeats_scan):
                    candidates.append(k)
                    
        if not candidates:
            return ('AB',)
            
        valid_candidates = []
        for k in candidates:
            # Верификация кандидата на других точках
            points = [start_i + 1, start_i + 3, start_i + 5]
            passed = True
            for pt in points:
                if not robust.query("R" * pt, "R" * (pt + k), repeats=repeats_verify):
                    passed = False
                    break
            if not passed:
                continue
                
            # Проверка устойчивости перехода при добавлении суффиксов
            suffix_passed = True
            for pt in [start_i, start_i + 3]:
                for suf in ['L', 'RL']:
                    u = "R" * pt + suf
                    v = "R" * (pt + k) + suf
                    if not robust.query(u, v, repeats=repeats_verify):
                        suffix_passed = False
                        break
                if not suffix_passed:
                    break
            
            valid_candidates.append((k, suffix_passed))
            
        if not valid_candidates:
            return ('AB',)
            
        with_suffix = [k for k, suf in valid_candidates if suf]
        if with_suffix:
            best_k = min(with_suffix)
            confident = True
        else:
            best_k = min(k for k, _ in valid_candidates)
            confident = False
            
        return ('VAL', best_k, confident)
        
    except TimeoutError:
        return ('TO',)


def solver_indep(oracle, cap_calls, seed):
    robust = RobustOracle(oracle, cap_calls)
    try:
        is_noisy = detect_noise(robust)
        repeats = 5 if is_noisy else 1
        
        probes = ["", "R", "L", "RR", "RL", "LR"]
        start_i, end_i = 12, 52
        
        # Адаптация параметров под бюджет
        if cap_calls < 150:
            start_i, end_i = 15, 35
            repeats = 1
            probes = ["", "R", "L"]
        elif cap_calls < 300:
            start_i, end_i = 12, 42
            repeats = 3 if is_noisy else 1
            probes = ["", "R", "L", "RR"]
            
        fingerprints = {}
        for i in range(start_i, end_i + 1):
            fp = []
            u = "R" * i
            for probe in probes:
                val = robust.query(u, probe, repeats=repeats)
                fp.append(val)
            fingerprints[i] = tuple(fp)
            
        best_p = None
        min_dist = 999.0
        dist_profile = {}
        max_p_search = min(35, (end_i - start_i) // 2)
        
        for p in range(1, max_p_search + 1):
            total_diff = 0
            count = 0
            for i in range(start_i, end_i + 1 - p):
                fp1 = fingerprints[i]
                fp2 = fingerprints[i+p]
                diff = sum(1 for a, b in zip(fp1, fp2) if a != b)
                total_diff += diff
                count += 1
            if count > 0:
                avg_diff = total_diff / (count * len(probes))
                dist_profile[p] = avg_diff
                if avg_diff < min_dist:
                    min_dist = avg_diff
                    best_p = p
                    
        threshold = 0.20 if is_noisy else 0.01
        if best_p is not None and min_dist <= threshold:
            # Проверяем, не является ли найденный период кратным меньшему истинному периоду
            for small_p in range(1, best_p):
                if small_p in dist_profile and dist_profile[small_p] <= min_dist + 0.05:
                    if best_p % small_p == 0:
                        best_p = small_p
                        break
            confident = min_dist < (0.10 if is_noisy else 0.001)
            return ('VAL', best_p, confident)
        else:
            return ('AB',)
            
    except TimeoutError:
        return ('TO',)


# =====================================================================
# СЕМЕЙСТВО ПРЕОБРАЗОВАНИЙ ОРАКУЛА (Описание T)
#
# Трансформация T строится на основе обратимого посимвольного кодирования,
# зависящего от локального контекста (префикса). 
# Encoder последовательно сканирует строку и инвертирует символ ('R' <-> 'L'),
# если триггерный бит состояния установлен в False. Бит состояния инвертируется
# при встрече символа 'R'.
# Decoder восстанавливает исходную последовательность благодаря тому, что
# решение об инверсии на текущем шаге опирается на уже декодированный префикс.
# =====================================================================

def _encode_word(w: str) -> str:
    res = []
    state = True
    for c in w:
        if state:
            res.append(c)
        else:
            res.append('L' if c == 'R' else 'R')
        state = (c == 'R')
    return "".join(res)


def _decode_word(w: str) -> str:
    res = []
    state = True
    for c in w:
        orig = c if state else ('L' if c == 'R' else 'R')
        res.append(orig)
        state = (orig == 'R')
    return "".join(res)


def apply_T(oracle_fn):
    """Возвращает обертку оракула с предварительным кодированием входных слов."""
    return lambda u, v: oracle_fn(_encode_word(u), _encode_word(v))


def apply_T_inv(oracle_fn):
    """Возвращает обертку оракула с предварительным декодированием входных слов."""
    return lambda u, v: oracle_fn(_decode_word(u), _decode_word(v))