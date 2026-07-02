# S1 — Microformalization of Semantic Status Transitions

**File:** `experiments/S/S1_Microformalization_of_Semantic_Status_Transitions.md`
**Task type:** analytic microformalization gate
**Status:** post-S0, pre-implementation
**No code. No experiments. No LLM training. No Sanskrit parser.**

---

## 0. Immutable project goal

Keep this goal visible at every step:

> Train an LLM / learner so that its world-model is **derived**, not merely generalized from internet-like data.

Current candidate direction:

> Derivational Semantic Ecology — a controlled language-world where claims have derivation traces, scoped assumptions, consequence obligations, contradiction containment, population-stabilized usage, and anti-Goodhart gates.

S1 exists only because S0 passed as:

```text
S0-PASS-ADMISSIBLE-FOR-MICROFORMALIZATION
```

S1 does **not** implement the system.
S1 does **not** prove the direction works.
S1 does **not** allow LLM training, substrate claims, derivability claims, or representation probes.

---

## 1. Why S1 exists

S0 showed that the direction can analytically distinguish:

```text
future-meaning potential
```

from:

```text
sophistry
dogmatic Boolean logic
grammar fetish
synthetic-internet coherent nonsense
```

But S0 passed because the distinctions were made analytically by hand.

S1 must test the next stricter question:

> Can the S0 distinction be expressed as a minimal microformal status-transition system, so that claims move between `FORMED`, `POETIC`, `SUSPENDED`, `LOCAL`, `STABLE`, `KILLED`, and `DANGEROUS` by explicit rules rather than ad hoc judgement?

---

## 2. Gate question

Can we define a minimal formal schema of:

```text
claim object
semantic status
assumption graph
scope
derivation trace
consequence obligation
contradiction relation
Goodhart flags
transition rules
```

such that the seven S0 cases classify correctly without treating grammar, coherence, context, population agreement, or claim volume as sufficient for semantic success?

---

## 3. Required decision vocabulary

Use exactly one:

```text
S1-PASS-ADMISSIBLE-FOR-TOY-MODEL-SPEC
S1-FAIL-AD-HOC-CLASSIFICATION
S1-FAIL-STATUS-SYSTEM-INCOHERENT
S1-FAIL-CONSEQUENCE-OBLIGATION-UNDEFINED
S1-FAIL-CONTRADICTION-CONTAINMENT-UNDEFINED
S1-FAIL-GOODHART-GUARDS-UNFORMALIZED
S1-FAIL-GRAMMAR-AS-MEANING
S1-INCONCLUSIVE
HALT-GOAL-DRIFT
```

Meaning:

```text
S1-PASS-ADMISSIBLE-FOR-TOY-MODEL-SPEC
- The microformal schema is precise enough to specify a tiny toy model next.

S1-FAIL-AD-HOC-CLASSIFICATION
- The seven cases are still classified by hand rather than by stated rules.

S1-FAIL-STATUS-SYSTEM-INCOHERENT
- Statuses overlap or transition rules contradict each other.

S1-FAIL-CONSEQUENCE-OBLIGATION-UNDEFINED
- Consequences are invoked but not formalized enough to constrain claims.

S1-FAIL-CONTRADICTION-CONTAINMENT-UNDEFINED
- Contradictions are named but not scoped, contained, or prevented from explosion.

S1-FAIL-GOODHART-GUARDS-UNFORMALIZED
- Proxy failure checks remain slogans rather than rule-level guards.

S1-FAIL-GRAMMAR-AS-MEANING
- Derivational / grammatical well-formedness can promote a claim to semantic success.

S1-INCONCLUSIVE
- The schema is promising but too vague for a toy-model spec.

HALT-GOAL-DRIFT
- Work becomes philosophy survey, Sanskrit worship, logic theory, DSL design, or implementation planning instead of S1 gate execution.
```

---

## 4. Required input files

Read these files if present:

```text
research/MAP-S0_Derivational_Semantic_Ecology.md
research/MAP-S1_Literature-grounded_Constraint_Refinement.md
research/closed_directions_ledger.md

experiments/S/S0_Anti-Sophistry_Future-Meaning_Admissibility_Gate.md
experiments/S/S0_anti_sophistry_future_meaning_admissibility_gate/S0_report.md
experiments/S/S0_anti_sophistry_future_meaning_admissibility_gate/S0_decision.json
experiments/S/S0_anti_sophistry_future_meaning_admissibility_gate/S0_case_table.md
experiments/S/S0_anti_sophistry_future_meaning_admissibility_gate/S0_assumption_graphs.md
experiments/S/S0_anti_sophistry_future_meaning_admissibility_gate/S0_goodhart_audit.md
```

If any are missing, list them as `MISSING`.

Continue only if the S0 decision exists and is:

```text
S0-PASS-ADMISSIBLE-FOR-MICROFORMALIZATION
```

---

## 5. Allowed output directory

Create:

```text
experiments/S/S1_microformalization_of_semantic_status_transitions/
```

Inside it, create exactly:

```text
S1_report.md
S1_decision.json
S1_microformal_schema.md
S1_transition_rules.md
S1_case_replay.md
S1_goodhart_guards.md
S1_failure_analysis.md
```

Do not edit files outside this directory.

Do not edit MAP files.

Do not edit S0 files.

Do not edit the closed directions ledger.

Commit required after successful completion.

---

## 6. Required microformal objects

S1 must define at least these objects.

### 6.1 Claim object

A claim must be represented as:

```text
Claim := {
  id,
  expression,
  derivation_trace,
  assumptions,
  scope,
  status,
  consequence_obligations,
  contradiction_links,
  goodhart_flags,
  population_state,
  anchors
}
```

S1 may refine this structure, but it may not omit any field.

### 6.2 Status set

Use exactly the S0 statuses:

```text
FORMED
POETIC
SUSPENDED
LOCAL
STABLE
KILLED
DANGEROUS
```

Do not collapse to Boolean truth values.

Do not add new final statuses.

If helper labels are needed, mark them as internal annotations, not statuses.

### 6.3 Derivation trace

Define what counts as a derivation trace.

Minimum:

```text
source primitives / terms
formation rules
transformations
lineage
```

Constraint:

> derivation trace can grant at most `FORMED` or `POETIC`; it cannot grant `LOCAL` or `STABLE`.

### 6.4 Scope

Define scope as a typed object.

Minimum dimensions:

```text
domain
model
scale
context
observer / agent
intervention class
assumption set
```

A claim without explicit scope cannot become `LOCAL` or `STABLE`.

### 6.5 Consequence obligation

Define consequence obligation as a structured requirement.

Minimum:

```text
if claim C holds under scope S and assumptions A,
then admissible test T should distinguish expected outcome O
from at least one alternative O'
```

A claim without consequence obligation cannot become `LOCAL` or `STABLE`.

### 6.6 Contradiction relation

Define contradiction relation as scoped, not global by default.

Minimum:

```text
Contradiction(C1, C2) iff
  C1 and C2 assert incompatible commitments
  under overlapping scope
  and shared assumptions
  and shared consequence tests
```

Contradiction must produce one of:

```text
quarantine
scope split
assumption split
weakening
kill
danger flag
```

It must not produce arbitrary explosion.

### 6.7 Goodhart flags

Define Goodhart flags at rule level.

Minimum flags:

```text
VOLUME_PROXY
COHERENCE_PROXY
CONTRADICTION_MINIMIZATION_PROXY
CONTEXT_PROLIFERATION_PROXY
GRAMMAR_PROXY
POPULATION_PROXY
```

A claim with active Goodhart flag cannot become `STABLE`.

---

## 7. Required transition rules

Write explicit rules for at least these transitions.

### T1 — Birth

```text
raw expression + derivation trace → FORMED
```

If no derivation trace:

```text
raw expression → rejected / not admitted
```

### T2 — Formed to Poetic

```text
FORMED + evocative use + no consequence obligation → POETIC
```

### T3 — Formed/Poetic to Suspended

```text
FORMED or POETIC
+ apparent contradiction or underdefined ontology
+ identifiable possible extension path
→ SUSPENDED
```

### T4 — Suspended to Local

```text
SUSPENDED
+ explicit scope
+ explicit assumptions
+ object/model/scope extension
+ consequence obligation
+ no active DANGEROUS flag
→ LOCAL
```

### T5 — Local to Stable

```text
LOCAL
+ survived consequence tests
+ contradiction remains contained
+ adversarial paraphrase survives
+ population stabilization exists
+ at least one formal/external anchor exists
+ no active Goodhart flags
→ STABLE
```

### T6 — Any status to Killed

```text
any status
+ failed under declared scope
or incoherent extension
or contradiction cannot be repaired without laundering
→ KILLED
```

### T7 — Any status to Dangerous

```text
any status
+ explosion risk
or arbitrary context creation
or pseudo-term laundering
or proxy optimization
or grammar-as-meaning promotion
→ DANGEROUS
```

### T8 — Local dualism

Define explicit condition under which apparently conflicting claims may both remain `LOCAL`.

Minimum:

```text
C1 and C2 may coexist as LOCAL iff
their scopes / models / tests differ
and their consequence obligations are not collapsed
and neither licenses arbitrary inference.
```

### T9 — Stable downgrade

Define how `STABLE` can be downgraded.

Minimum:

```text
STABLE
+ new contradiction under overlapping scope
or failed anchor
or Goodhart flag discovered
→ LOCAL / SUSPENDED / KILLED / DANGEROUS
```

No status is irreversible except perhaps archived `KILLED` under a declared scope.

---

## 8. Required case replay

Replay the seven S0 cases using only the S1 transition rules.

Cases:

```text
A. liquid powder exists
B. infertility is inherited
C. square circle exists
D. every claim can be made true by choosing a context
E. X is related to Y somehow
F. translucent causal sweetness-field
G. Light behaves as a wave / Light behaves as a particle
```

For each case, provide:

```text
initial object:
applied rules:
status path:
blocked paths:
final S1 classification:
why not ad hoc:
```

The replay must show that the classification follows from rules, not from prose intuition.

---

## 9. Required Goodhart guard formalization

Write:

```text
S1_goodhart_guards.md
```

For each proxy:

```text
VOLUME_PROXY
COHERENCE_PROXY
CONTRADICTION_MINIMIZATION_PROXY
CONTEXT_PROLIFERATION_PROXY
GRAMMAR_PROXY
POPULATION_PROXY
```

define:

```text
trigger condition:
blocked transition:
required repair:
case that activates it:
kill / danger condition:
```

Example:

```text
GRAMMAR_PROXY:
trigger: derivation_trace exists but consequence_obligations is empty
blocked transition: FORMED/POETIC → LOCAL/STABLE
required repair: add consequence obligation and scope
case: pseudo-term without consequences
kill/danger: if grammar-validity alone promotes status
```

---

## 10. Required incoherence checks

S1 must explicitly test for these schema-level failures.

### IC1 — Status overlap

Can a claim be both `STABLE` and `DANGEROUS`?

Expected:

```text
No. DANGEROUS blocks STABLE.
```

### IC2 — Grammar bypass

Can derivation trace alone produce `LOCAL` or `STABLE`?

Expected:

```text
No.
```

### IC3 — Context laundering

Can a new scope save any contradiction?

Expected:

```text
No. Scope creation requires cost, lineage, assumptions, and consequence delta.
```

### IC4 — Vacuity

Can a claim with no relation type / consequence become `STABLE`?

Expected:

```text
No.
```

### IC5 — Dogmatism

Can all contradictions be killed immediately?

Expected:

```text
No. SUSPENDED and LOCAL are available for scoped or future-meaning cases.
```

### IC6 — Explosion

Can local contradiction imply arbitrary claims?

Expected:

```text
No.
```

If any expected answer fails, S1 must fail.

---

## 11. Required output files

### 11.1 `S1_microformal_schema.md`

Must define:

```text
Claim object
Status set
Scope object
Assumption graph
Consequence obligation
Contradiction relation
Goodhart flags
Anchor types
Population state
```

### 11.2 `S1_transition_rules.md`

Must define rules T1–T9.

### 11.3 `S1_case_replay.md`

Must replay cases A–G through the rules.

### 11.4 `S1_goodhart_guards.md`

Must formalize the six Goodhart guards.

### 11.5 `S1_failure_analysis.md`

Must test IC1–IC6 and list which failure modes remain possible.

### 11.6 `S1_report.md`

Must contain exactly these sections:

```text
# S1 — Microformalization of Semantic Status Transitions

## 0. Verdict
## 1. Goal anchor
## 2. Inputs used
## 3. S0 constraints carried forward
## 4. Microformal schema summary
## 5. Transition rule summary
## 6. Case replay summary
## 7. Goodhart guard summary
## 8. Incoherence checks
## 9. Pass / fail analysis
## 10. What was NOT shown
## 11. Downstream permission
## 12. Durable result
```

### 11.7 `S1_decision.json`

Must be valid JSON:

```json
{
  "decision": "...",
  "reason": "...",
  "s0_decision_confirmed": false,
  "cases_replayed": [],
  "cases_failed": [],
  "incoherence_checks_passed": [],
  "incoherence_checks_failed": [],
  "admissible_for_toy_model_spec": false,
  "implementation_allowed": false,
  "llm_training_allowed": false,
  "substrate_claim_allowed": false,
  "derivability_claim_allowed": false,
  "next_allowed_work": []
}
```

Set:

```json
"s0_decision_confirmed": true
```

only if S0 decision was read and confirmed as:

```text
S0-PASS-ADMISSIBLE-FOR-MICROFORMALIZATION
```

Set:

```json
"admissible_for_toy_model_spec": true
```

only if decision is:

```text
S1-PASS-ADMISSIBLE-FOR-TOY-MODEL-SPEC
```

Never set these true in S1:

```json
"implementation_allowed": true
"llm_training_allowed": true
"substrate_claim_allowed": true
"derivability_claim_allowed": true
```

If S1 passes, the only allowed next work is:

```json
["S2 toy model specification"]
```

---

## 12. Pass conditions

S1 passes only if all hold:

```text
1. S0 pass is confirmed.
2. Claim object includes all required fields.
3. Status set is exactly the S0 status set.
4. Derivation trace cannot promote beyond FORMED/POETIC by itself.
5. Consequence obligation is defined structurally.
6. Contradiction relation is scoped and non-explosive.
7. Goodhart guards are rule-level, not slogans.
8. Transitions T1–T9 are explicit.
9. Cases A–G replay correctly through rules.
10. Incoherence checks IC1–IC6 pass.
11. No implementation, code, experiment, LLM training, substrate claim or derivability claim is made.
```

---

## 13. Failure conditions

Use the decision vocabulary.

Fail as `S1-FAIL-AD-HOC-CLASSIFICATION` if case replay depends on intuition instead of rules.

Fail as `S1-FAIL-STATUS-SYSTEM-INCOHERENT` if statuses overlap incompatibly or transitions conflict.

Fail as `S1-FAIL-CONSEQUENCE-OBLIGATION-UNDEFINED` if “consequence” remains prose only.

Fail as `S1-FAIL-CONTRADICTION-CONTAINMENT-UNDEFINED` if contradiction cannot be scoped, repaired, or blocked from explosion.

Fail as `S1-FAIL-GOODHART-GUARDS-UNFORMALIZED` if Goodhart guards do not block transitions.

Fail as `S1-FAIL-GRAMMAR-AS-MEANING` if derivation / grammar can promote to `LOCAL` or `STABLE`.

Fail as `S1-INCONCLUSIVE` if the schema is promising but insufficient for a toy-model spec.

Fail as `HALT-GOAL-DRIFT` if task becomes philosophy survey, Sanskrit worship, logic theory, DSL design, implementation planning, or framework naming.

---

## 14. Mandatory “what was NOT shown”

Include this in `S1_report.md` even if S1 passes:

```text
- No substrate was found.
- No derived world-model was shown.
- No LLM training is allowed.
- No Sanskrit experiment is allowed.
- No implementation is allowed.
- No toy model has been specified yet.
- No claim that semantic ecology solves grounding.
- No claim that status transitions are sufficient for meaning.
- No claim that contradiction containment is enough.
- No claim that population meaning is truth.
- No claim that S1 proves the direction works.
```

---

## 15. Git discipline

Before making changes, run:

```bash
git status --short
```

Record whether the worktree was clean in the final report.

After writing outputs, validate JSON:

```bash
python3 -m json.tool experiments/S/S1_microformalization_of_semantic_status_transitions/S1_decision.json >/dev/null
```

Inspect changes:

```bash
git status --short
git diff -- experiments/S/S1_microformalization_of_semantic_status_transitions/
```

Stage only the allowed S1 output directory:

```bash
git add experiments/S/S1_microformalization_of_semantic_status_transitions/
```

Also stage the S1 specification file **only if it was newly created by this task**:

```bash
git add experiments/S/S1_Microformalization_of_Semantic_Status_Transitions.md
```

Do not stage MAP files.

Do not stage S0 files.

Do not stage `research/closed_directions_ledger.md`.

Commit with:

```bash
git commit -m "Add S1 semantic status microformalization"
```

After commit, run:

```bash
git status --short
git log -1 --oneline
```

Final response must include:

```text
- S1 decision
- files created
- JSON validation status
- commit hash
- whether unrelated changes remain unstaged
```

---

## 16. Final instruction

The desired result is not to pass.

The desired result is to determine whether S0’s analytic distinctions can survive as a small formal transition system.

If S1 passes, the direction becomes admissible only for an S2 toy-model specification.

If S1 fails, close or narrow the direction according to the failure mode.

