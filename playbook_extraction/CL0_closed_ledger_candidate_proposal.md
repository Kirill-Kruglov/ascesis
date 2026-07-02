# CL0 — Closed-Ledger Candidate Proposal

## 0. Verdict

`PASS-CANDIDATE`

**INFERENCE.** The current ledger is strong enough to propose one minimal
candidate family only in the weakened safe-boundary form: train a learner on a
lawful generated domain after an independently audited boundary filters
collapse-bound states. This is not evidence that the learner derives a
world-model. It is a narrow candidate because the ledger directly identifies the
failure to avoid: a compact/projection boundary that marks collapse-bound states
SAFE, or a conservative boundary that becomes vacuous.

## 1. Goal anchor

The immutable goal is to train an LLM or learner so that its model of the world
comes from lawful substrate interaction rather than from internet-like
statistical imitation. The current honest weakened form is to train inside a
safe domain boundary so the learner is not exposed to collapse trajectories,
even if the remaining content is still generalized rather than fully derived.

> “This CL0 step serves the safe / derivable substrate goal by…”

This CL0 step serves the safe / derivable substrate goal by proposing one
minimal boundary-filtered generated domain and a pre-registered gate that must
show the boundary is faithful to full collapse ground truth and non-vacuous
before any learner or LLM-scale training is allowed.

**INFERENCE.** This is direct enough to continue because the step tests a
precondition for safe substrate training, not a general theory of substrate
generation.

## 2. Inputs used

| file | status |
|---|---|
| `experiments/CL/CL0_Closed-Ledger_Candidate_Proposal.md` | METHOD |
| `playbook_extraction/README.md` | METHOD |
| `playbook_extraction/SUMMARY.md` | METHOD |
| `playbook_extraction/01_method_from_practice.md` | METHOD |
| `playbook_extraction/02_extracted_method.md` | METHOD |
| `playbook_extraction/03_not_yet_method.md` | METHOD |
| `playbook_extraction/harness/output_schema.md` | METHOD |
| `playbook_extraction/harness/failure_conditions.md` | METHOD |
| `claude_code_task_ascesis_reorg_and_development.md` | MISSING |
| `research/closed_directions_ledger.md` | MISSING |
| `research/door1_postmortem/Door1_Extracted_Knowledge_v1.md` | EVIDENCE |
| `research/faithful_abstraction_v1/01_empirical_basis.md` | EVIDENCE |
| `experiments/JB/JB0_E1_standard_cegar_boundary_assessment/outputs/final_report.md` | EVIDENCE |
| `experiments/FA/FA2_5_E1_candidate_validation/outputs/final_report.md` | EVIDENCE |
| `experiments/BA/BA4_layer_audit/justitia_layer_audit.md` | EVIDENCE |
| `experiments/15_collapse_boundary/outputs_15_2/summary.md` | EVIDENCE |
| `experiments/JB/18_1_shielded_training/outputs_18_1/summary.md` | EVIDENCE |
| `experiments/JB/18_1_shielded_training/outputs_18_1/level_A_preregistration.json` | EVIDENCE |
| `experiments/JB/18_1_shielded_training/claude_code_task_18_1_shielded_training.md` | EVIDENCE |

**FACT.** The preferred closed-direction ledger is absent, so the ledger below is
reconstructed only from the listed evidence files.

## 3. Closed-direction ledger extracted for CL0

| killed direction | evidence file | failure mode | durable constraint for future candidates |
|---|---|---|---|
| Justitia as current Door-1 substrate | `research/door1_postmortem/Door1_Extracted_Knowledge_v1.md`; `experiments/JB/JB0_E1_standard_cegar_boundary_assessment/outputs/final_report.md` | **FACT:** Justitia did not yield a useful Door-1 safety boundary; JB0 says Justitia should not remain a Door-1 candidate. | **INFERENCE:** a future candidate must not depend on repairing Justitia attachment; it must start from transferable constraints. |
| Standard CEGAR boundary | `experiments/JB/JB0_E1_standard_cegar_boundary_assessment/outputs/final_report.md` | **FACT:** false-safe decreased to 0.043161, but FPR became 0.540810; verdict `Conservative_but_vacuous`. | **FACT/INFERENCE:** conservative correctness is insufficient; a candidate boundary needs non-vacuity/usefulness controls. |
| FA compression / coverage proxy | `research/faithful_abstraction_v1/01_empirical_basis.md`; `experiments/FA/FA2_5_E1_candidate_validation/outputs/final_report.md` | **FACT:** compact witness coverage existed, but candidate failed discrimination; `No_discriminative_candidate`, precision margin -0.084052. | **FACT:** compression/coverage cannot count as constructive progress without discrimination against ordinary SAFE states. |
| BA projection / layer simplification | `experiments/BA/BA4_layer_audit/justitia_layer_audit.md`; `research/faithful_abstraction_v1/01_empirical_basis.md` | **FACT:** semantic layers were mixed; variables such as `resource_hhi` span dynamics, policy, observation, projection, and reporting roles. | **INFERENCE:** future candidates must declare layer role for every boundary coordinate and exclude reporting-only metrics from shield evidence. |
| 15.2 free-monoid / noisy-TV / count-open caveat | `experiments/15_collapse_boundary/outputs_15_2/summary.md` | **FACT:** semantic count grew exponentially and was exhausted, but normal forms were free binary words; count-open did not show non-trivial meaning. | **FACT/INFERENCE:** unbounded class count is not enough; any candidate must include a learnability/usefulness or transfer check, not only combinatorial richness. |
| 18.1 shield false-safe / projection blindness | `experiments/JB/18_1_shielded_training/outputs_18_1/summary.md`; `experiments/JB/18_1_shielded_training/outputs_18_1/level_A_preregistration.json` | **FACT:** 2-counter shield had false_safe_rate 0.299 against threshold 0.05; 19.3% already-collapsed states were labeled SAFE. | **FACT:** a candidate boundary must be tested against full collapse ground truth before learner training; false-safe above 0.05 halts downstream work. |

## 4. Candidate proposal attempt

Candidate family:

Layer-audited safe-transition ledger over a generated lawful domain.

Core objects:

- **FACT-derived requirement:** a generated transition system with explicit
  current state, transition, observation, and intervention layers.
- A full-state collapse predicate or unsafe predicate defined outside the
  learner-facing observation.
- A boundary relation computed from layer-eligible state summaries and bounded
  forward reachability, not from reporting-only metrics.
- A closed ledger of transitions admitted for learner training only if the
  boundary marks the source state SAFE and the full trajectory does not violate
  the collapse predicate under the pre-registered horizon.

Transition / inference rule:

The candidate uses executable lawful transitions of the chosen minimal domain.
The CL0 candidate does not introduce a new transition theory. The boundary rule
is: compute layer-audited candidate coordinates, evaluate bounded forward
collapse reachability, then admit only transitions whose source state is
classified SAFE by the boundary.

Boundary / shield relation:

`SAFE(s)` means the boundary predicts no collapse within the pre-registered
horizon under the full transition semantics. It must include all known
collapse-relevant coordinate families for the domain; for any Justitia-derived
pilot this minimally means mean welfare, failed-zone/spread information,
total-mass information, and any witness-required history/control coordinates.
Reporting-only metrics such as `capture_index`, `permanence`, and
diagnostic ratios are not boundary evidence.

Observation available to learner:

The learner may observe only the allowed training ledger: admitted observations,
actions/interventions, and consequences inside the SAFE boundary. It may not see
hidden collapse labels, future collapse outcomes, or reporting-only audit
metrics during training. Those remain oracle/audit data for the gate.

Why world-model content would be derived or safer:

**INFERENCE.** This candidate only supports the weakened safe-boundary claim:
the learner is safer if collapse-bound trajectories are excluded by a faithful,
non-vacuous boundary before training. It does not yet show derivation of a
world-model. A later experiment would need to test derivation/transfer inside
the admitted domain.

Which closed-direction constraints it explicitly avoids:

- Avoids 18.1 projection blindness by requiring full collapse ground truth
  fidelity before learner training.
- Avoids JB0 vacuity by requiring a non-vacuity/usefulness threshold and a
  trivially-safe baseline.
- Avoids FA2/FA2.5 compression failure by measuring discrimination, not witness
  coverage.
- Avoids BA layer confusion by separating dynamics, policy/control,
  observation, projection, and reporting layers.
- Avoids 15.2 noisy-TV/count trap by refusing to treat open class count as
  evidence of meaningful substrate content.

## 5. Existing-theory reduction check

**INFERENCE.** The proposed candidate is close to ordinary shielded learning or
reachability-filtered offline training. It also resembles standard abstraction
checking and conservative boundary construction.

**FACT/INFERENCE.** CL0 does not claim novelty here. The candidate is acceptable
only because it is tied to a specific project need: a safe training-domain
filter for LLM/learner substrate work, with the exact failure modes from
Door-1/BA/FA/JB pre-registered as kill conditions.

**HYPOTHESIS.** If the candidate adds no value beyond ordinary shielded learning
once tested, it should be downgraded to a known-method application and not
opened as a new research branch.

## 6. Bought-by-simplification check

What variables are projected away?

**HYPOTHESIS.** In any implementation, the boundary will project away some raw
transition state. For a Justitia-derived pilot, projected-away variables would
include high-dimensional lineage strategy fields, resource stocks, mutation
state, migration structure, delayed observation queues, and reporting metrics
unless a witness analysis makes them layer-eligible.

Could the projected-away variables contain collapse / unsafe information?

**FACT/INFERENCE.** Yes. 18.1 showed omitted spread and mass information hid
collapse. BA4 showed delayed observations, history/control state, and
policy-visible concentration can be behaviourally relevant. Therefore the
candidate fails unless every projection is tested against full collapse ground
truth and false-safe witnesses are decomposed.

Could the boundary be trivially safe but useless?

**FACT.** Yes. JB0 produced a conservative-but-vacuous boundary with FPR
0.540810. The CL0 gate therefore includes FPR/non-vacuity and a trivially-safe
baseline.

Could the candidate achieve decidability by removing the meaningful structure?

**FACT/INFERENCE.** Yes. 18.1's 2-counter shield was decidable on the abstraction
but did not faithfully track real collapse. 15.2 showed a clean count result
could be bought by free-monoid triviality. Decidability is not evidence unless
the boundary preserves the behavioural property.

Could it create compression without discrimination?

**FACT.** Yes. FA2/FA2.5 showed compact witness coverage and then failed
candidate discrimination. The CL0 gate therefore requires discrimination against
ordinary SAFE states.

## 7. Pre-registered kill-gate

Question:

Does the proposed safe-transition ledger boundary faithfully exclude
collapse-bound states while preserving enough non-collapse states to support
equal-budget learner training?

Metric:

Primary dangerous-error metric:

`false_safe_rate = P(full collapse within horizon | boundary says SAFE)`.

Mandatory non-vacuity metrics:

- `false_positive_rate = P(boundary says DOOMED | full trajectory remains SAFE)`;
- ability to sample an equal-volume shielded and unfiltered control training set
  under the same budget;
- policy-independent purity signal:
  `already_collapsed_labeled_safe_rate`.

Threshold:

- `false_safe_rate <= 0.05`.
- `already_collapsed_labeled_safe_rate == 0`.
- `false_positive_rate <= 0.20`.
- equal-volume shielded/control sample must be possible without replacement
  under the declared budget.

**Justification.** The 0.05 dangerous-error threshold is inherited from 18.1's
pre-registration. The 0 already-collapsed threshold is stricter because labeling
already-collapsed states SAFE is a direct projection-fidelity failure. The FPR
0.20 bar is set before measurement to exclude JB0-style vacuity (0.540810) while
remaining looser than the non-vacuous baselines reported in FA2.5 (0.129771 to
0.167939). Equal-volume is mandatory because otherwise safety can be bought by
less data.

Ground truth / oracle:

Full domain transition semantics and the full collapse/unsafe predicate along
the actual trajectory. Collapse labels and future outcomes are audit-only; they
are not learner observations.

Positive controls:

- A known unsafe/collapse-bound set should be classified DOOMED by the boundary.
- If a Justitia-derived pilot is used, states satisfying omitted 18.1 collapse
  clauses such as failed-zone/spread and total-mass collapse must be included.

Negative controls:

- Ordinary SAFE states sampled from trajectories that remain non-collapse within
  the horizon.
- Reporting-only metrics should not be allowed to improve the boundary unless a
  layer audit makes them transition/policy relevant.

Trivially-safe baseline:

Classify all states DOOMED / admit no training transitions. This baseline is
perfectly safe but useless. The candidate must admit enough SAFE transitions to
construct an equal-volume shielded training set and must beat this baseline on
non-vacuity.

Equal-volume or equal-budget condition:

The shielded ledger and unfiltered control ledger must use the same number of
training transitions or the same fixed collection budget. If equal-volume
sampling cannot be achieved after filtering, the gate fails as vacuous.

Decision vocabulary:

- `boundary_fidelity_ok`
- `boundary_fails_false_safe`
- `boundary_conservative_but_vacuous`
- `boundary_inconclusive_missing_ground_truth`

Downstream halt rule:

If the decision is not `boundary_fidelity_ok`, no learner training, no LLM
scaling, and no derivability claim may be run downstream. The next step must be
false-safe witness analysis or candidate rejection.

The machine-readable pre-registration is written in
`playbook_extraction/CL0_preregistration.json`.

## 8. What would count as failure?

- **FACT/RECOMMENDATION:** candidate repeats a closed direction: if it is merely
  standard CEGAR or the 18.0 2-counter projection, halt.
- **FACT/RECOMMENDATION:** candidate is safe only by being vacuous:
  `false_positive_rate > 0.20`, no equal-volume shielded set, or no meaningful
  admitted transitions.
- **FACT/RECOMMENDATION:** candidate compresses but does not discriminate:
  witness coverage without precision/specificity against ordinary SAFE states.
- **FACT/RECOMMENDATION:** candidate requires hidden collapse information as
  learner input rather than audit oracle.
- **FACT/RECOMMENDATION:** candidate relies on a projection that can hide
  false-safe states, especially omitted spread/mass/history/control
  coordinates.
- **FACT/RECOMMENDATION:** candidate cannot be killed by the proposed gate,
  e.g. no full collapse ground truth or no pre-registered horizon.
- **FACT/RECOMMENDATION:** candidate does not serve the LLM substrate goal and
  becomes an interesting abstraction, synthesis, or methodology problem.

## 9. What was NOT shown

- No claim that the candidate works.
- No claim that the candidate is already a substrate.
- No claim that the learner derives a world-model yet.
- No claim that the method is now constructive in general.
- No claim that a general substrate generator exists.
- No claim that the playbook is transferable.
- No claim of novelty over shielded learning, reachability filtering, or known
  verification methods.

## 10. Durable result

**RECOMMENDATION.** The exact next experiment is a boundary-fidelity and
non-vacuity pilot for the layer-audited safe-transition ledger. It should be run
before any learner training. It halts if `false_safe_rate > 0.05`, if any
already-collapsed state is labeled SAFE, if `false_positive_rate > 0.20`, or if
an equal-volume shielded training set cannot be sampled under the declared
budget.

**INFERENCE.** The durable CL0 result is not a new framework. It is the narrow
finding that the closed ledger supports exactly one next candidate attempt:
safe-domain filtering with pre-registered false-safe and non-vacuity gates.
