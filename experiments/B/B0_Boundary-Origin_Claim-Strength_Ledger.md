# B0 — Boundary-Origin / Claim-Strength Ledger

## 0. Зачем это нужно

Проект сейчас содержит несколько разных мечт и несколько разных границ:

1. граница формы;
2. граница смысла;
3. граница внешней реальности;
4. граница безопасности / выживания;
5. граница, заданная человеком в toy-world;
6. граница, порождённая правилом;
7. граница, подтверждённая consequence-tests.

Главная опасность:

> назвать одну границу другой.

Если protective boundary назвать truth boundary — получим оправданный bias, замаскированный под истину.
Если grammar boundary назвать semantic boundary — получим санскритскую / деривационную софистику.
Если human-authored boundary назвать derived boundary — получим красивую ручную разметку.
Если toy boundary назвать world boundary — повторим ошибку CL-ветки.

---

## 1. Центральная трилемма

Текущая трилемма проекта:

```text
A. Truth boundary
граница задаётся внешней реальностью / последствиями мира.

B. Viability boundary
граница задаётся защитой популяции от коллапса.

C. Rule-generated boundary
граница вынуждена конечным правилом, как у фрактала.
```

Нельзя безнаказанно слить эти три границы.

### Truth boundary

Сильная сторона:

> даёт контакт с объективной реальностью.

Слабость:

> может быть опасной, неантропоцентричной, разрушительной; также почти всегда дана через инструменты, практики, историю и интерпретацию.

### Viability boundary

Сильная сторона:

> защищает популяцию / learner от collapse-trajectories.

Слабость:

> это bias, shield, ограничение доступа; не истина сама по себе.

### Rule-generated boundary

Сильная сторона:

> вычислима и вынуждена правилом; ближе к “выводится, не обобщается”.

Слабость:

> может быть пустой или нерелевантной миру, как красивый фрактал без содержания.

---

## 2. Закон, который надо зафиксировать

```text
Never call a protective boundary a truth boundary.
Never call a truth boundary safe.
Never call a grammar boundary semantic.
Never call a human-authored boundary derived.
Never call a toy boundary world-like without a transfer gate.
Never call a rule-generated boundary meaningful without consequence pressure.
```

Это главный дисциплинарный закон следующего этапа.

---

## 3. Что сейчас доказуемо вычислительно

### 3.1 В конечном toy-world вычислимо

Если домены конечны, как в S2, то вычислимо:

```text
- достижимый статус claim через T1–T9;
- какие Goodhart flags активны;
- какие transition rules заблокированы;
- есть ли replay-time human oracle;
- зависит ли итоговый статус от human-authored fields;
- есть ли прямой lookup expression_id → final_status;
- есть ли скрытый shortcut grammar → meaning;
- может ли population_state продвинуть claim без consequence-tests;
- может ли context creation спасти contradiction без cost/lineage/consequence_delta.
```

Это сильная зона. Здесь можно писать проверяемые протоколы.

### 3.2 В общем выразительном мире невычислимо / неразрешимо

Для достаточно богатого языка / логики / теории, в общем случае нельзя ожидать разрешимости:

```text
- глобальной непротиворечивости;
- максимального непротиворечивого подмножества;
- различения локального и фундаментального противоречия для всех claims;
- истинности произвольного утверждения;
- будущей meaningfulness произвольного выражения;
- полного отсутствия скрытого semantic oracle в открытой системе.
```

Это не поражение. Это граница.

Следовательно, общий проект не должен обещать “движок, который всегда решит смысл”. Он может строить **локальные, конечные, аудируемые boundary protocols**.

### 3.3 В реальном мире можно только опосредованно

Внешняя граница приходит через:

```text
- тесты;
- инструменты;
- практики;
- научно-технический уровень;
- историческое развитие;
- вмешательства;
- ошибки;
- репликации;
- социальную стабилизацию.
```

Поэтому “жидкий порошок” не выводится из грамматики. Он удерживается как `SUSPENDED` до появления object-class и consequence-tests.

---

## 4. Что сейчас демонстрируемо людям

Можно показать людям не AGI и не substrate, а серию маленьких демонстраций.

### Demo 1 — Boundary accounting

Один и тот же claim проходит через разные источники границы:

```text
grammar boundary → FORMED
semantic consequence boundary → LOCAL/STABLE
viability boundary → allowed/blocked for learner
human-authored boundary → audit only
```

Цель: показать, что границы нельзя смешивать.

### Demo 2 — Future-meaning vs sophistry

Сравнить:

```text
жидкий порошок
квадратный круг
всё истинно в каком-то контексте
X связан с Y как-то
```

Цель: показать, почему `SUSPENDED` не равно “пустить всё”.

### Demo 3 — Protective bias vs truth

Один claim может быть truth-relevant, но недопустим для learner в текущей viability boundary.

Цель: показать, что safety bias честно отделён от truth.

### Demo 4 — Goodhart failure

Если оптимизировать claim volume, coherence или low contradiction, система начинает производить пустые claims, псевдо-термины или dogmatic kills.

Цель: показать, почему нужен вектор guard’ов, а не одна метрика.

### Demo 5 — Boundary drift over time

Claim сначала `SUSPENDED`, потом при появлении нового test/outcome становится `LOCAL`.

Цель: показать, как “будущий смысл” может быть сохранён без софистики.

---

## 5. Что должно быть первой целью

Первая цель:

```text
B0: построить ledger происхождения границ для S0–S2 и текущей философской развилки.
```

B0 должен классифицировать каждый boundary decision по источнику:

```text
FORM_BOUNDARY
- grammar / derivation / syntax

CONSEQUENCE_BOUNDARY
- tests / outcomes / anchors

VIABILITY_BOUNDARY
- safety / collapse protection / justitia-like shield

RULE_GENERATED_BOUNDARY
- follows from finite rule without human field annotation

HUMAN_AUTHORED_BOUNDARY
- manually supplied fields, assumptions, outcomes, scopes

POPULATION_BOUNDARY
- stabilized usage, but not truth by itself

UNKNOWN_OR_MIXED_BOUNDARY
- source unclear
```

Для каждого claim / rule / status transition B0 должен спросить:

```text
1. Какая граница сработала?
2. Кто или что её породило?
3. Вычислима ли она в toy-world?
4. Требует ли она внешнего мира?
5. Требует ли она human-authored field?
6. Является ли она truth-boundary или viability-boundary?
7. Можно ли её честно использовать как evidence?
8. Если нет — как понизить claim?
```

---

## 6. Почему именно B0 первый

B0 выбран потому что он фальсифицирует почти все остальные будущие пути.

Если B0 покажет:

```text
semantic statuses mostly come from human-authored fields
```

то S3 implementation нельзя продавать как boundary generator. Это будет только boundary-accounting protocol.

Если B0 покажет:

```text
protective boundary is being called truth boundary
```

то проект уходит в опасный bias-as-truth drift.

Если B0 покажет:

```text
grammar boundary is treated as semantic boundary
```

то direction закрывается как grammar fetish.

Если B0 покажет:

```text
rule-generated boundary is empty or not consequence-bearing
```

то фрактальная интуиция не даёт content.

Если B0 покажет:

```text
external boundary is required for meaning
```

то надо честно признать: язык не выводит смысл сам; он удерживает candidates до контакта с реальностью.

---

## 7. Первый допустимый результат B0

B0 может завершиться одним из статусов:

```text
B0-PASS-BOUNDARY-SOURCES-SEPARATED
B0-FAIL-HUMAN-AUTHORED-BOUNDARY-AS-DERIVED
B0-FAIL-PROTECTIVE-BOUNDARY-AS-TRUTH
B0-FAIL-GRAMMAR-BOUNDARY-AS-SEMANTIC
B0-FAIL-RULE-BOUNDARY-NONCONTENTFUL
B0-FAIL-EXTERNAL-BOUNDARY-UNAVAILABLE
B0-INCONCLUSIVE
HALT-GOAL-DRIFT
```

Лучший честный pass не будет означать “мы нашли путь”.

Он будет означать:

> теперь мы знаем, какая граница откуда берётся, и не имеем права смешивать claims.

---

## 8. Что B0 должен зафиксировать для эссе

Главный центр будущего эссе:

```text
Мы ищем не данные, а границу.
Но существует не одна граница.
Граница истины, граница выживания, граница формы и граница вычислимого правила расходятся.
Проект становится честным только тогда, когда перестаёт называть одну границу другой.
```

Трилемма эссе:

```text
1. Чистая truth boundary может быть нечеловеческой и опасной.
2. Viability boundary защищает жизнь, но является bias.
3. Rule-generated boundary вычислима, но может быть бессодержательной.
```

Рабочая гипотеза после B0:

```text
AGI/ASI не должна обучаться на интернете как на proxy-world.
Но и не должна получать “чистую истину” без viability boundary.
Нужен процесс согласования:
- что выразимо;
- что имеет последствия;
- что безопасно допускать;
- что вычислимо из правила;
- что пока только удерживается на границе как SUSPENDED.
```

---

## 9. Что B0 не должен делать

B0 не должен:

```text
- писать код;
- строить S3;
- запускать toy model;
- делать Sanskrit experiment;
- утверждать substrate;
- утверждать derivability;
- выбирать окончательную философию истины;
- обещать полную разрешимость;
- называть protective bias объективной истиной.
```

---

## 10. Итог

Первая цель:

```text
B0 — Boundary-Origin / Claim-Strength Ledger
```

Почему она первая:

> потому что она проверяет источник границы. Если источник границы нечестен, все дальнейшие toy-world demos будут красивой ручной разметкой.

Самый важный вопрос B0:

```text
Граница порождена правилом, внешним consequence-test, protective bias или человеком?
```

Пока мы не ответили на это для каждого claim, переход к S3 опасен.

