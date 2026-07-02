# KG0 — Programme Review

## Purpose

The research programme itself is now considered a scientific object.

External criticism is treated as experimental evidence.

No criticism is accepted merely because it was produced by Claude.

No criticism is rejected merely because it is inconvenient.

Each point must be evaluated independently.

## 1. Scope

This review exists because the Substrate Discovery programme has reached the
point where its own framing, terminology, and research sequence can become
failure modes. Earlier kill-gates tested experimental systems. KG0 tests the
programme's interpretation of those results.

The programme is therefore subject to kill-gates for the same reason its
candidate substrates are: an attractive research frame can compress evidence,
hide alternative explanations, or preserve obsolete goals. The review layer is
intended to make those risks explicit before additional chapters, candidates, or
playbook procedures are treated as established.

Claude's review is evidence, not authority. It is useful because it attacks the
programme from outside the current synthesis. It is not sufficient by itself.
Every accepted criticism below is accepted only where it is supported by local
documents, experiment reports, or explicit unresolved obligations already
present in the programme.

## 2. Accepted Criticisms

| ID | Claude claim | Evidence | Assessment | Required action |
| --- | --- | --- | --- | --- |
| AC-1 | The Goal Anchor is ambiguous and may have drifted from the Door-1/Justitia objective into a generic internal-model programme. | `research/door1_postmortem/Door1_Extracted_Knowledge_v1.md` defines the original objective as LLM world-model acquisition through lawful substrate interaction. `research/faithful_abstraction_v1/BRIDGE_MAP_18_1_TO_FA2.md` requires value relative to an analytically understandable and safety-faithful substrate for future LLM training. `research/substrate_discovery_v1/00_research_axioms.md` and `01_research_question.md` restate the object more generally as lawful environments where internal models are rational for bounded learners. | Accepted as a real ambiguity. It is not yet proven to be fatal drift, but it is programme-blocking until resolved. | Promote to KG-1 Goal Anchor Identity Gate. |
| AC-2 | Derivability was expanded before the reduction gate was discharged. | `04_Derivability.md` explicitly marks derivability as provisional and asks whether it reduces to existing quantities. `09_Open_Problems.md` contains reducibility and prior-art obligations. `00_research_axioms.md` requires existing-theory reduction. | Accepted. The term may remain as working vocabulary, but cannot be treated as a new construct until reduction is completed. | Promote to KG-2 Derivability Reduction Gate. |
| AC-3 | Internal-model measurability is unresolved. | `01_research_question.md` uses internal model as central terminology. `09_Open_Problems.md` asks how to measure internal model formation and distinguish it from memorization or behavioral imitation. | Accepted. The programme cannot make success claims until a non-oracular measurement rule exists. | Promote to KG-3 Internal-Model Measurability Gate. |
| AC-4 | "Necessary Properties" overclaims the evidential status of the listed properties. | `06_Necessary_Properties.md` labels the properties as candidate necessary properties, but the title and later triage docs can be read as stronger than the evidence supports. `04_triage_framework.md` uses required-property language before necessity proofs exist. | Accepted. The properties may guide search, but must not be used as established necessity claims. | Promote to KG-5 Necessity Audit Gate. |
| AC-5 | Justitia/BA/FA/JB evidence is being transferred beyond its demonstrated scope. | The BA/FA/JB chain supports conclusions about abstraction fidelity, layer discipline, compression versus discrimination, and false-safe witnesses. It does not directly establish conditions for world-model emergence. | Accepted. The evidence remains valuable, but citations must preserve scope. | Require a scope bridge for every transfer from Justitia abstraction evidence to substrate discovery claims. |
| AC-6 | The current computable-environment definition does not yet discriminate candidates. | `03_Computability_of_Environment.md` states that all candidate classes considered so far share the common computability property and uses the term primarily as a common axis. | Accepted. It is currently vocabulary and taxonomy, not a filter. | Keep as working vocabulary unless it rejects or separates concrete candidates. |
| AC-7 | Interaction and identifiability have not yet been reduced to existing theory. | `05_Interaction_and_Identifiability.md` explicitly overlaps with causal inference, active experimentation, optimal experimental design, reinforcement learning, control, and system identification. | Accepted. The reduction obligation remains open. | Include in KG-2 or a dependent prior-art reduction pass. |
| AC-8 | The playbook could become ritual form without substance. | `research/playbook/00_monograph_kill_gates.md` is currently only a checklist skeleton. `research/playbook/README.md` correctly says the playbook is not finished. | Accepted as a risk, though current navigation already labels the playbook as skeleton. | Do not cite playbook headings as completed method until populated with examples and failure conditions. |
| AC-9 | Level discipline is asserted more often than executed. | `00_research_axioms.md` asserts level discipline. `07_Search_Strategy.md` and `08_Candidate_Evaluation_Framework.md` define machinery, but no complete worked candidate evaluation has yet passed the new programme gates. | Accepted. | Require the first post-KG candidate evaluation to demonstrate level discipline explicitly. |

## 3. Partially Accepted Criticisms

| ID | Claude claim | What Claude got right | What remains unresolved | Evidence that would decide |
| --- | --- | --- | --- | --- |
| PC-1 | The programme has abandoned the original alignment/LLM objective. | The active Substrate Discovery wording is broader than the Door-1 and FA Goal Anchor wording. | It is not yet clear whether this is illegitimate drift or a valid abstraction of the same objective. | A single Goal Anchor statement plus a decision-dependence audit: if removing the LLM/safety clause does not change the research decisions, the drift criticism succeeds. |
| PC-2 | Derivability was coined as if it were novel. | The reduction gate is open and must be fired before further theory is built on the term. | `04_Derivability.md` already says the term is provisional and may reduce to existing work; it does not claim final novelty. | KG-2 literature reduction against MDL, algorithmic statistics, computational mechanics, predictive-state representations, model-based RL, causal abstraction, and related frameworks. |
| PC-3 | Justitia negatives cannot justify substrate discovery. | They do not directly evidence internal-model emergence. | They do provide durable methodological constraints: layer discipline, compression versus discrimination, false-safe witnesses, and vacuous conservative boundaries. | A bridge map that tags each transferred claim as FACT, INFERENCE, or HYPOTHESIS and states the exact target claim it supports. |
| PC-4 | Preservation and repository-philosophy files are missing. | The general risk of weak navigation and skeleton process is valid. | In the current repository snapshot, `research/playbook/03_preservation_rule.md` and `04_repository_philosophy.md` exist. | If a later review was made against an earlier commit, the historical claim may have been true then; in the current snapshot, it is false. |
| PC-5 | Computable environment partitions nothing. | It currently excludes no candidate class already under discussion. | A common vocabulary term can still be useful before it becomes a filter. | The concept must either reject at least one plausible candidate, separate candidate classes operationally, or be demoted to background vocabulary. |

## 4. Rejected Criticisms

| ID | Rejected claim | Evidence | Reasoning | Future kill condition |
| --- | --- | --- | --- | --- |
| RC-1 | The current repository lacks the preservation-rule and repository-philosophy notes. | `research/playbook/03_preservation_rule.md` and `research/playbook/04_repository_philosophy.md` are present in the current repository snapshot. | This criticism is factually outdated for the current state. It may remain historically understandable if Claude reviewed an earlier tree. | If those files are later removed or contradicted by navigation practice, the rejection fails. |
| RC-2 | Existing programme chapters should be rewritten immediately to match the criticism. | The repository now has an explicit preservation rule: historical or provisional documents should receive review layers or banners rather than silent rewrites. The current user instruction also forbids modifying existing chapters. | The correct immediate action is to add this KG0 review layer. Rewriting would erase the evidence trail and make later audit harder. | If readers continue to treat pre-KG0 speculative chapters as settled despite this review, future navigation may need banners or indexes, but not silent rewrites. |
| RC-3 | Derivability is already presented as a completed new theory. | `04_Derivability.md` says the construct is provisional, asks whether it reduces to existing quantities, and states that the aim is not terminological novelty. | The stronger claim is not supported. The weaker criticism, that reduction must happen before expansion, is accepted above. | If future work uses derivability as established before KG-2, this rejection fails. |

## 5. Programme Kill-Gates

| Gate | Hypothesis attacked | Failure condition | Evidence required | Consequence |
| --- | --- | --- | --- | --- |
| KG-1 Goal Anchor Identity Gate | The Substrate Discovery programme still serves the original Door-1 objective rather than a different generic learning-theory objective. | The operative research question remains unchanged when LLM-like systems, safety-faithful substrate, or internet-text-imitation contrast are removed. | One canonical Goal Anchor; comparison against `Door1_Extracted_Knowledge_v1.md`, `BRIDGE_MAP_18_1_TO_FA2.md`, `00_search_frame.md`, and `01_research_question.md`; decision-dependence audit. | Freeze expansion until revised. If failed, rename/reframe the programme in a future change rather than pretending continuity. |
| KG-2 Derivability Reduction Gate | Derivability is a necessary residual concept not already captured by existing theory. | The construct reduces without residue to existing frameworks such as MDL, algorithmic statistics, computational mechanics, predictive-state representations, causal abstraction, model-based RL, or system identification. | Desk review with explicit reduction table and at least one worked toy example. | Drop or demote the term; future theory must use the stronger existing vocabulary. |
| KG-3 Internal-Model Measurability Gate | Internal model formation can be measured without oracle labels or circular success definitions. | No implementation-independent measurement distinguishes compact world-model acquisition from memorization, lookup, or behavioral imitation. | Operational metric, negative controls, and a minimal discriminating example. | No success claims about internal model emergence; only behavioral generalization claims remain allowed. |
| KG-4 Proxy-World Discriminability Gate | Proxy worlds can empirically distinguish lawful interaction learning from description/statistical imitation. | A passive-description or memorization baseline matches the interaction learner on held-out interventions under the proposed metric. | Pre-registered toy design, baselines, intervention split, and failure criteria. | RA-10/P10 is downgraded from programme axiom to failed or unresolved hypothesis. |
| KG-5 Necessity Audit Gate | The listed properties are necessary rather than merely useful desiderata. | No property receives a necessity argument, or a plausible counterexample satisfies the Goal Anchor while violating the property. Circular properties such as model advantage or proxy-world dependence remain definitions of success rather than independent conditions. | One-by-one necessity table with proof sketch, counterexample, or downgrade decision. | Future documents must treat the list as conjectured desiderata until necessity is demonstrated. |
| KG-6 Prior-Art Interaction Gate | The interaction/identifiability axis adds something not already handled by existing causal, control, RL, or system-identification frameworks. | Existing theory explains the axis with no programme-specific residual. | Reduction table and strongest alternative-theory reconstruction. | Use existing theory directly; do not build a local duplicate vocabulary. |

## 6. Programme Freeze

The following parts of the programme are frozen until KG-1, KG-2, and KG-3 have
been resolved:

- no further expansion of substrate-discovery chapters as if the current frame
  were settled;
- no use of derivability as an established construct;
- no use of "necessary properties" as proven necessity claims;
- no claim that BA/FA/JB evidence demonstrates world-model emergence;
- no new candidate ranking that depends on unresolved internal-model
  measurability;
- no treatment of the playbook skeleton as a finished research method.

The following work remains allowed:

- analytical kill-gate documents;
- literature and prior-art reduction;
- scope-bridge tables that classify claims as FACT, INFERENCE, or HYPOTHESIS;
- preservation and indexing work that makes provisional status clearer;
- pre-registration of a proxy-world toy, without using it to claim success
  before KG-1 to KG-3 are resolved.

## 7. Immediate Priority Queue

1. Goal Anchor clarification.

   Decide whether the programme is still about a safety-faithful substrate for
   future LLM-like training, or whether it has become a broader theory of
   internal-model emergence. This must be first because all later evidence
   relevance depends on the answer.

2. Derivability reduction.

   Compare derivability against existing frameworks and either preserve a
   residual construct or demote the term.

3. Internal-model operationalization.

   Define what would count as evidence of an internal model without oracle
   knowledge, future labels, or circular performance definitions.

4. Necessity audit.

   Reclassify each claimed property as necessary, useful desideratum,
   vocabulary, circular, or unsupported.

5. Proxy-world empirical toy design.

   Design but do not yet run a toy test that could distinguish interaction-born
   model acquisition from passive description learning. Execution should wait
   until the measurement rule is defined.

## 8. Collaboration Protocol

Future collaboration should use stable roles without assigning epistemic
authority to any role.

GPT:

- synthesis;
- hypothesis generation;
- programme architecture.

Claude:

- hostile reviewer;
- reduction;
- falsification;
- independent critique.

Codex:

- implementation;
- experiments;
- repository maintenance.

Human:

- scientific judgement;
- final arbitration.

None of these roles has epistemic authority.

Authority belongs only to:

- evidence;
- successful falsification;
- successful survival of kill-gates.

## 9. Meta Reflection

The programme has moved from using kill-gates only on experiments to using
kill-gates on itself. This is a qualitative methodological change because the
research object now includes the programme's own language, goals, reductions,
and interpretation rules.

This does not prove that the method is correct. It creates a new hypothesis
about research methodology: that a programme can preserve scientific discipline
by exposing its own scaffolding to falsification before the scaffolding becomes
invisible. KG0 is the first test of that hypothesis, not a validation of it.

The main risk is ritualization. A kill-gate can become a formality if it only
renames existing commitments. The review layer is therefore useful only if
future work is allowed to fail these gates and terminate or redirect the
programme.

## 10. Final Status

continue_after_revision

Justification:

The programme should not continue unchanged. Claude's review identifies real
programme-level risks: Goal Anchor ambiguity, unresolved derivability reduction,
internal-model measurability, overclaimed necessity, and evidence transfer
beyond demonstrated scope.

The programme should also not be terminated at KG0. The BA/FA/JB evidence chain
remains valuable within its scope, the Door-1 postmortem preserves durable
constraints, and the Substrate Discovery frame contains falsifiable questions
rather than only rhetorical claims.

The correct status is therefore continue_after_revision: no expansion of the
programme until KG-1, KG-2, and KG-3 have been executed, and no future claim may
treat the pre-KG0 scaffolding as settled.

KG0 Programme Review complete.

No programme changes performed.

Only review evidence added.
