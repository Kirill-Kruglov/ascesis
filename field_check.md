# Проверка против существующего поля

Рабочий файл для связывания ключевых тезисов диалога с существующей литературой. Это не оценка ценности и не заявка на новизну; цель только в том, чтобы честно отметить, где тезис уже покрыт, где совпадает частично, а где прямой источник пока не найден.

Правило флагов:

- `[ПОЛНОЕ СОВПАДЕНИЕ]` - тезис диалога уже сформулирован в источнике, иногда строже.
- `[ЧАСТИЧНОЕ]` - пересекается, но отличается рамка или склейка.
- `[НЕ НАЙДЕНО]` - прямой источник не найден; кандидат на ручную перепроверку человеком.

## 1. Неподвижная точка целей под самомодификацией; successor-риск для самого агента

| тезис диалога | источник | флаг | примечание |
|---|---|---|---|
| Рефлексивный агент может рассматривать successor/self-modification как риск потери собственных целей (`dialog.part_7.md:17`, `dialog.part_8.md:3`, `dialog.part_10.md:53`). | Stephen M. Omohundro, 2008, ["The Basic AI Drives"](https://selfawaresystems.files.wordpress.com/2008/01/ai_drives_final.pdf). | `[ПОЛНОЕ СОВПАДЕНИЕ]` | Omohundro прямо формулирует drives к self-knowledge, self-improvement, utility-function preservation и осторожность при self-modification. |
| Построение преемника с теми же целями как центральная проблема self-modifying AI (`dialog.part_7.md:17`, `dialog.part_21.md:13`). | Eliezer Yudkowsky, Marcello Herreshoff, 2013, ["Tiling Agents for Self-Modifying AI, and the Löbian Obstacle"](https://intelligence.org/files/TilingAgents.pdf). | `[ПОЛНОЕ СОВПАДЕНИЕ]` | Источник прямо моделирует агентов, одобряющих построение похожих successor agents с сохранением целей, и Löbian obstacle. |
| "Самодоверие" агента к будущему себе/преемнику как формальная проблема (`dialog.part_17.md:17`, `dialog.part_19.md:31`). | Benja Fallenstein, Nate Soares, 2015, ["Vingean Reflection: Reliable Reasoning for Self-Improving Agents"](https://intelligence.org/files/VingeanReflection.pdf); Nate Soares, 2015, ["The Value Learning Problem"](https://intelligence.org/files/ValueLearningProblem.pdf). | `[ЧАСТИЧНОЕ]` | Пересечение по reflective trust/self-improvement; формула диалога про "аскезу" и existential successor-risk для самого агента является другой рамкой. |

Флаг узла: `[ПОЛНОЕ СОВПАДЕНИЕ]`.

## 2. Явный отказ на непереводимом остатке

| тезис диалога | источник | флаг | примечание |
|---|---|---|---|
| Система должна явно отказываться на случаях, где уверенный перевод/решение невозможны (`dialog.part_16.md:29`, `dialog.part_17.md:9`, `dialog.part_17.md:13`). | C. K. Chow, 1970, ["On Optimum Recognition Error and Reject Tradeoff"](https://doi.org/10.1109/TIT.1970.1054406). | `[ПОЛНОЕ СОВПАДЕНИЕ]` | Классическая reject option: классификатор может отказаться вместо рискованного решения. |
| Selective prediction как современная ML-форма "покрыть только область, где риск приемлем" (`dialog.part_16.md:29`, `dialog.part_18.md:21`). | Yonatan Geifman, Ran El-Yaniv, 2017, ["Selective Classification for Deep Neural Networks"](https://arxiv.org/abs/1705.08500). | `[ПОЛНОЕ СОВПАДЕНИЕ]` | Источник позволяет задавать риск и отвергать примеры для сохранения гарантии на покрытой области. |
| End-to-end модель с встроенным reject option (`dialog.part_16.md:29`). | Yonatan Geifman, Ran El-Yaniv, 2019, ["SelectiveNet: A Deep Neural Network with an Integrated Reject Option"](https://arxiv.org/abs/1901.09192). | `[ПОЛНОЕ СОВПАДЕНИЕ]` | Совпадает с принципом явного отказа; отличие только в том, что диалог применяет его к semantic seam. |

Флаг узла: `[ПОЛНОЕ СОВПАДЕНИЕ]`.

## 3. "Кто проверяет проверяющего" / самопроверка через предобязательство

| тезис диалога | источник | флаг | примечание |
|---|---|---|---|
| Проблема внешнего исправления: сильный агент по умолчанию может сопротивляться коррекции (`dialog.part_19.md:27`, `dialog.part_19.md:35`, `dialog.part_21.md:13`). | Nate Soares, Benja Fallenstein, Eliezer Yudkowsky, Stuart Armstrong, 2015, ["Corrigibility"](https://intelligence.org/files/Corrigibility.pdf). | `[ПОЛНОЕ СОВПАДЕНИЕ]` | Corrigibility прямо вводит задачу агента, который допускает corrective intervention несмотря на incentives to resist. |
| Проверка должна сохраняться при создании подсистем и self-modification (`dialog.part_19.md:31`, `dialog.part_19.md:33`). | Soares et al., 2015, ["Corrigibility"](https://intelligence.org/files/Corrigibility.pdf). | `[ПОЛНОЕ СОВПАДЕНИЕ]` | Источник явно требует propagation of shutdown/correction behavior into new subsystems or self-modification. |
| Самопроверка против собственного закоммиченного прошлого Я вместо внешнего надзора (`dialog.part_19.md:27`, `dialog.part_19.md:31`). | Manuel Blum, 1983, "Coin Flipping by Telephone"; Gilles Brassard, David Chaum, Claude Crepeau, 1988, ["Minimum Disclosure Proofs of Knowledge"](https://doi.org/10.1016/0022-0000(88)90005-0); общая литература по cryptographic commitments. | `[ЧАСТИЧНОЕ]` | Cryptographic commitment покрывает предобязательство/неподделываемость, но не найден прямой источник, где это используется именно как self-checking alignment against a committed past self. |

Флаг узла: `[ЧАСТИЧНОЕ]`.

## 4. Квантовый якорь неподделываемости коммита

| тезис диалога | источник | флаг | примечание |
|---|---|---|---|
| No-cloning как физический примитив неподделываемости state/identity, не поведения (`dialog.part_4.md:25`, `dialog.part_11.md:25`, `dialog.part_20.md:19`). | Stephen Wiesner, 1983, "Conjugate Coding", SIGACT News 15(1), 78-88. | `[ПОЛНОЕ СОВПАДЕНИЕ]` | Quantum money/conjugate coding прямо использует некопируемость квантовых состояний для защиты от подделки токена. |
| Quantum money / quantum tokens как reusable or limited-verification unforgeable token (`dialog.part_20.md:23`, `dialog.part_20.md:31`, `dialog.part_21.md:13`). | Scott Aaronson, Paul Christiano, 2012, ["Quantum Money from Hidden Subspaces"](https://arxiv.org/abs/1203.4740). | `[ПОЛНОЕ СОВПАДЕНИЕ]` | Источник прямо обсуждает quantum money, публичную проверяемость, unlimited verification и security constraints. |
| Квантовый токен как якорь именно для commitment основания агента (`dialog.part_20.md:19`, `dialog.part_20.md:23`). | Adrian Kent et al., 2021, ["Practical quantum tokens without quantum memories and experimental tests"](https://arxiv.org/abs/2104.11717). | `[ЧАСТИЧНОЕ]` | Quantum-token literature покрывает unforgeability, но не найден прямой источник про alignment commitment state агента. |

Флаг узла: `[ЧАСТИЧНОЕ]`.

## 5. Эндогенная аскеза / отказ от безудержного ресурсо-захвата

| тезис диалога | источник | флаг | примечание |
|---|---|---|---|
| Resource acquisition, self-preservation, self-improvement и goal-content integrity как convergent drives (`dialog.part_7.md:3`, `dialog.part_7.md:9`, `dialog.part_21.md:13`). | Stephen M. Omohundro, 2008, ["The Basic AI Drives"](https://selfawaresystems.files.wordpress.com/2008/01/ai_drives_final.pdf). | `[ПОЛНОЕ СОВПАДЕНИЕ]` | Источник прямо формулирует ресурсный захват и сохранение utility function как drives sufficiently advanced AI. |
| Instrumental convergence and orthogonality (`dialog.part_7.md:9`, `dialog.part_9.md:27`). | Nick Bostrom, 2014, [*Superintelligence: Paths, Dangers, Strategies*](https://global.oup.com/academic/product/superintelligence-9780199678112). | `[ПОЛНОЕ СОВПАДЕНИЕ]` | Стандартное поле для тезиса о ресурсах как instrumental goal. |
| Отказ от maximizing в пользу более мягкой политики/ограниченного выбора (`dialog.part_8.md:35`, `dialog.part_18.md:23`). | Jessica Taylor, 2015, ["Quantilizers: A Safer Alternative to Maximizers for Limited Optimization"](https://intelligence.org/files/Quantilizers.pdf). | `[ЧАСТИЧНОЕ]` | Quantilizers покрывают mild/limited optimization; диалоговая "аскеза" добавляет рефлексивную и этико-метафорическую рамку. |

Флаг узла: `[ЧАСТИЧНОЕ]`.

## 6. Шов язык ↔ спецификация: частичный перевод + round-trip + измеримый зазор

| тезис диалога | источник | флаг | примечание |
|---|---|---|---|
| Natural language -> executable/formal representation как semantic parsing (`dialog.part_13.md:11`, `dialog.part_13.md:13`, `dialog.part_14.md:29`). | Percy Liang, Michael I. Jordan, Dan Klein, 2013, ["Learning Dependency-Based Compositional Semantics"](https://aclanthology.org/J13-1004/); Matt Gardner et al., 2018, ["Neural Semantic Parsing"](https://aclanthology.org/P18-5003/). | `[ПОЛНОЕ СОВПАДЕНИЕ]` | Семантический парсинг прямо занимается переводом естественного языка в формальные/исполняемые представления. |
| Измеримый зазор через reconstruction error / autoencoder round-trip (`dialog.part_16.md:29`, `dialog.part_17.md:27`). | Geoffrey Hinton, Richard Zemel, 1993, ["Autoencoders, Minimum Description Length and Helmholtz Free Energy"](https://proceedings.neurips.cc/paper/1993/hash/9e3cfc48eccf81a0d57663e129aef3cb-Abstract.html); Dong Gong et al., 2019, ["Memorizing Normality to Detect Anomaly"](https://arxiv.org/abs/1904.02639). | `[ПОЛНОЕ СОВПАДЕНИЕ]` | Reconstruction error as anomaly signal is standard; диалог переносит его на semantic seam. |
| Formal verifier-in-the-loop for natural-language-to-formal-spec translation (`dialog.part_14.md:29`, `dialog.part_16.md:31`). | Matthias Cosler et al., 2023, ["nl2spec: Interactively Translating Unstructured Natural Language to Temporal Logics with Large Language Models"](https://arxiv.org/abs/2303.04864); Jun Wang et al., 2025, ["ConformalNL2LTL: Translating Natural Language Instructions into Temporal Logic Formulas with Conformal Correctness Guarantees"](https://arxiv.org/abs/2504.21022). | `[ЧАСТИЧНОЕ]` | Пересечение сильное: NL -> temporal logic, ambiguity handling, uncertainty-aware request for help; не покрывает всю схему "частичный шов + человек на остатке". |

Флаг узла: `[ЧАСТИЧНОЕ]`.

## 7. Пределы верификации

| тезис диалога | источник | флаг | примечание |
|---|---|---|---|
| Нельзя полностью решить нетривиальную семантическую проверку произвольных программ (`dialog.part_4.md:23`, `dialog.part_16.md:25`). | H. G. Rice, 1953, ["Classes of Recursively Enumerable Sets and Their Decision Problems"](https://doi.org/10.1090/S0002-9947-1953-0053041-6). | `[ПОЛНОЕ СОВПАДЕНИЕ]` | Rice theorem прямо задает пределы автоматической проверки нетривиальных semantic properties. |
| Гёделева/лёбианская граница self-trust и проверки собственного основания (`dialog.part_16.md:25`, `dialog.part_17.md:17`). | Kurt Gödel, 1931, "Über formal unentscheidbare Sätze..."; Martin Löb, 1955, "Solution of a Problem of Leon Henkin"; Yudkowsky & Herreshoff, 2013, ["Tiling Agents"](https://intelligence.org/files/TilingAgents.pdf). | `[ПОЛНОЕ СОВПАДЕНИЕ]` | Источники покрывают incompleteness/self-trust/Löbian obstacle строже, чем диалог. |
| Specification gaming / reward hacking как эксплуатация неполной спецификации (`dialog.part_3.md:17`, `dialog.part_4.md:11`, `dialog.part_4.md:13`). | Dario Amodei et al., 2016, ["Concrete Problems in AI Safety"](https://arxiv.org/abs/1606.06565). | `[ПОЛНОЕ СОВПАДЕНИЕ]` | Reward hacking и wrong objective function прямо покрывают проблему "спека не равна намерению". |

Флаг узла: `[ПОЛНОЕ СОВПАДЕНИЕ]`.

## 8. Горизонт предсказуемости sandbox

| тезис диалога | источник | флаг | примечание |
|---|---|---|---|
| Sandbox/симуляция имеет конечный горизонт предсказуемости; больше итераций не гарантирует лучший прогноз в хаотической системе (`dialog.part_18.md:13`, `dialog.part_18.md:17`, `dialog.part_18.md:21`). | Aleksandr Lyapunov tradition; Pierre Gaspard, 2005, *Chaos, Scattering and Statistical Mechanics*; concept: [Lyapunov time](https://en.wikipedia.org/wiki/Lyapunov_time). | `[ПОЛНОЕ СОВПАДЕНИЕ]` | Lyapunov time exactly captures predictability limits from divergence of nearby trajectories. |
| Ранние сигналы необратимых/критических переходов: critical slowing down, variance/autocorrelation (`dialog.part_9.md:31`, `dialog.part_18.md:27`). | Marten Scheffer et al., 2009, ["Early-warning signals for critical transitions"](https://doi.org/10.1038/nature08227). | `[ПОЛНОЕ СОВПАДЕНИЕ]` | Источник прямо формулирует ранние сигналы critical transitions. |
| Правило "скорость не выше дальности зрения" как AI-sandbox policy (`dialog.part_18.md:21`, `dialog.part_18.md:23`, `dialog.part_18.md:25`). | Scheffer et al. 2009 + Lyapunov-time literature. | `[ЧАСТИЧНОЕ]` | Математика горизонта есть; конкретная policy-склейка для AGI sandbox является переносом. |

Флаг узла: `[ПОЛНОЕ СОВПАДЕНИЕ]`.

## 9. Языковой слой: Панини, formal/generative grammar, language of thought, linguistic relativity

| тезис диалога | источник | флаг | примечание |
|---|---|---|---|
| Панини как формальная/порождающая грамматика с метаправилами и разрешением конфликтов (`dialog.part_14.md:17`, `dialog.part_14.md:19`, `dialog.part_14.md:23`). | George Cardona, 1988, [*Pāṇini: His Work and Its Traditions*](https://archive.org/details/paninihisworkits0000card); Paul Kiparsky, 1979, "Pāṇini as a Variationist". | `[ПОЛНОЕ СОВПАДЕНИЕ]` | Паниниевская грамматика как rule system/metarule tradition хорошо покрыта индологической и лингвистической литературой. |
| Современная перепроверка rule-conflict в Панини (`dialog.part_14.md:19`, `dialog.part_16.md:17`). | Rishi Rajpopat, 2022, ["In Pāṇini We Trust"](https://www.repository.cam.ac.uk/items/e6764a39-15af-4f60-8b25-0f905ad8d015). | `[ПОЛНОЕ СОВПАДЕНИЕ]` | Прямо касается применения метаправил и конфликтов правил в Aṣṭādhyāyī. |
| Язык/представление как условие мышления и саморефлексии агента (`dialog.part_13.md:15`, `dialog.part_15.md:13`, `dialog.part_15.md:25`). | Jerry A. Fodor, 1975, [*The Language of Thought*](https://archive.org/details/languageofthough0000fodo); Michael Rescorla, "The Language of Thought Hypothesis", [Stanford Encyclopedia of Philosophy](https://plato.stanford.edu/entries/language-thought/). | `[ЧАСТИЧНОЕ]` | LOTH покрывает compositional mental representation; диалог переносит это на проектируемый язык самоописания LLM/agent. |
| Язык влияет на категории восприятия/познания, но не полностью определяет мысль (`dialog.part_13.md:15`). | Edward Sapir, Benjamin Lee Whorf; обзор: Lera Boroditsky, 2001, ["Does Language Shape Thought?"](https://doi.org/10.1111/1467-9280.00300). | `[ПОЛНОЕ СОВПАДЕНИЕ]` | Совпадает с осторожной weak linguistic relativity рамкой. |

Флаг узла: `[ЧАСТИЧНОЕ]`.

## 10. seL4 / capability identity слой

| тезис диалога | источник | флаг | примечание |
|---|---|---|---|
| seL4 как формально верифицированное capability microkernel (`dialog.part_1.md:7`, `dialog.part_1.md:11`, `dialog.part_1.md:13`). | Gerwin Klein et al., 2009, ["seL4: Formal Verification of an OS Kernel"](https://dl.acm.org/doi/10.1145/1629575.1629596). | `[ПОЛНОЕ СОВПАДЕНИЕ]` | Прямой первичный источник по functional correctness proof seL4. |
| seL4 полезен как нижний слой isolation/control plane, но не решает semantic alignment (`dialog.part_3.md:13`, `dialog.part_3.md:17`, `dialog.part_4.md:11`). | Klein et al. 2009; Toby Murray et al., 2013, ["seL4: From General Purpose to a Proof of Information Flow Enforcement"](https://ts.data61.csiro.au/publications/nicta_full_text/7098.pdf). | `[ЧАСТИЧНОЕ]` | Источники покрывают kernel/security guarantees; вывод о semantic alignment является применением к AI-agent threat model. |
| Object-capability model: unforgeable reference/authority и делегируемые, но не подделываемые права (`dialog.part_1.md:13`, `dialog.part_2.md:27`, `dialog.part_3.md:19`). | Jack Dennis, Earl C. Van Horn, 1966, ["Programming Semantics for Multiprogrammed Computations"](https://doi.org/10.1145/365230.365252); Mark S. Miller, 2006, ["Robust Composition: Towards a Unified Approach to Access Control and Concurrency Control"](http://www.erights.org/talks/thesis/markm-thesis.pdf). | `[ПОЛНОЕ СОВПАДЕНИЕ]` | Capability/object-capability field прямо формулирует unforgeable references and delegated authority. |
| Host-independent autonomy / verifiable execution traces for agents (`dialog.part_2.md:39`, `dialog.part_2.md:41`). | Artem Grigor et al., 2025, ["VET Your Agent: Towards Host-Independent Autonomy via Verifiable Execution Traces"](https://arxiv.org/abs/2512.15892). | `[ПОЛНОЕ СОВПАДЕНИЕ]` | Прямой источник для host-independent authentication of agent outputs. |
| agentOS как seL4-based AI-agent OS (`dialog.part_2.md:25`, `dialog.part_2.md:35`). | Jordan Hubbard, ["agentOS"](https://github.com/jordanhubbard/agentos). | `[ЧАСТИЧНОЕ]` | Релевантный проект/PoC; не академический первичный источник и требует ручной проверки зрелости. |

Флаг узла: `[ПОЛНОЕ СОВПАДЕНИЕ]`.

## Сводка

По флагам узлов:

- `[ПОЛНОЕ СОВПАДЕНИЕ]`: 5
- `[ЧАСТИЧНОЕ]`: 5
- `[НЕ НАЙДЕНО]`: 0

Узлы с `[ПОЛНОЕ СОВПАДЕНИЕ]`:

- 1. Неподвижная точка целей под самомодификацией; successor-риск для самого агента.
- 2. Явный отказ на непереводимом остатке.
- 7. Пределы верификации.
- 8. Горизонт предсказуемости sandbox.
- 10. seL4 / capability identity слой.

Узлы с `[ЧАСТИЧНОЕ]`:

- 3. "Кто проверяет проверяющего" / самопроверка через предобязательство.
- 4. Квантовый якорь неподделываемости коммита.
- 5. Эндогенная аскеза / отказ от безудержного ресурсо-захвата.
- 6. Шов язык ↔ спецификация: частичный перевод + round-trip + измеримый зазор.
- 9. Языковой слой: Панини, formal/generative grammar, language of thought, linguistic relativity.

Кандидаты на ручную проверку человеком (`[НЕ НАЙДЕНО]`):

- Нет. По правилу честности все узлы имеют как минимум частичное покрытие существующей литературой. Самые вероятные места узкой новизны, если она есть, находятся не в отдельных тезисах, а в склейках: `self-checking via committed past self`, `quantum anchor for agent commitment`, `semantic seam with explicit human residue`, `endogenous ascesis as reflective anti-resource-grab`.
