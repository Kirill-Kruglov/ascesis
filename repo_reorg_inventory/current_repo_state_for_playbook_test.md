# Current Repository State for Playbook Test

Date: 2026-06-29

Scope: current-state repository snapshot for designing a clean Playbook /
Programme-Gate test. This is inventory-only. It records what a new agent would
see after the reorganization commits and after the untracked KG/PR gate files
were added.

No existing project files were moved, deleted, renamed, staged, committed, or
edited while producing this snapshot.

## 1. Current Git State

- Branch: `main`.
- Latest commit: `5a367ac docs: add repository reorganization audit trail`.
- Latest 12 commits:

```text
5a367ac docs: add repository reorganization audit trail
e88e538 docs: organize BA FA JB experiment evidence
954f246 docs: add research archive and playbook skeleton
3e3d7ca chore: extract blind-arbiter line to external Justitia repo
67f2cb6 fix: clarify consequence-gated anti-concentration
5f88f37 feat: add boundary atlas experiment
1912e09 feat: add anti-concentration governance experiment
b90633e feat: add robustness ablation experiment
1c4ec21 feat: add capture audit and evolvable strategy substrate
fe9d5d1 feat: add action-channel containment experiment
a97f3a0 feat: add minimal enforcement feeder experiment
08def72 feat: add break trivial policies experiment
```

- Index status: clean; `git status --short` shows only untracked files/roots.
- Tracked worktree status: clean; no modified tracked files were reported before
  this snapshot file was created.
- Untracked roots:
  - `experiments/14_dsl_core/`
  - `experiments/15_collapse_boundary/`
  - `experiments/16_consequence_vs_feature/`
  - `experiments/17A.2_Semantic_Perturbation_Taxonomy/`
  - `experiments/17A_backbone_consequence/`
  - `experiments/17C_interpretive_closure_test/`
  - `experiments/17D_closure_metric_robustness/`
  - `experiments/17E_latent_metric_geometry/`
  - `experiments/17F_cross_substrate_latent_geometry/`
  - `experiments/17_backbone_consequence/`
  - `repo_reorg_inventory/commit_checkpoint_report.md`
  - `research/Claude_kill-gate_review.md`
  - `research/substrate_discovery_v1/KG0_programme_review.md`
  - `research/substrate_discovery_v1/KG1_SPEC.md`
  - `research/substrate_discovery_v1/KG_PIPELINE.md`
  - `research/substrate_discovery_v1/KG_SPEC.md`
  - `research/substrate_discovery_v1/PR1_programme_revision.md`
- Deferred experiment trees: yes. The checkpoint report explicitly defers
  optional post-17 experiment import as a separate review/commit decision.

## 2. Top-Level Navigation

| Entry | State | Purpose | Read for KG1-like task? |
|---|---|---|---|
| `README.md` | active navigation | Repository-level orientation; states Ascesis is a research trail, Justitia is external, and Substrate Discovery/playbook work is emerging. | Yes, for repository context and live/historical split. |
| `research/README.md` | active navigation | Current research archive index; marks Substrate Discovery active, playbook draft, Door1/FA/monograph reference. | Yes. |
| `experiments/INDEX.md` | evidence navigation | Family index for legacy, post-17, BA, FA, and JB evidence. | Yes, to locate evidence, not as argument. |
| `ascesis_of_learning_grace/` | historical | Preserved original sandbox, map, field checks, dialogue parts, and historical banners. | Usually no for KG execution; yes for historical reconstruction if explicitly included. |
| `research/playbook/` | procedural draft | Future extraction target for kill-gates, evidence ledgers, preservation rules, and repository philosophy. | Yes for playbook usability tests; no as a finished method. |
| `research/substrate_discovery_v1/` | active but frozen/reviewed | Current Substrate Discovery corpus plus untracked KG/PR review layer. | Yes, but visibility depends on task type. |
| `research/faithful_abstraction_v1/` | reference/evidence | FA programme docs, empirical basis, theory note, review packet, bridge map. | Yes; `BRIDGE_MAP` and empirical basis are core evidence/context. |
| `research/door1_postmortem/` | reference/evidence | Durable knowledge extracted from Justitia/Door-1. | Yes; primary bridge evidence. |
| `experiments/BA/` | evidence | Boundary Analysis reports and specs diagnosing Justitia abstraction failure. | Yes for evidence corpus, especially BA4. |
| `experiments/FA/` | evidence | Faithful Abstraction witness taxonomy, compression, validation, and T-C retained spec. | Yes for evidence corpus, especially FA2.5. |
| `experiments/JB/` | evidence | Shield synthesis, 18.1 fidelity kill-gate, JB0 CEGAR assessment. | Yes for evidence corpus, especially 18.1 and JB0. |

## 3. Programme-Gate Infrastructure

| File | Role | Status | Blind reconstruction | Methodology/playbook test | Final arbitration |
|---|---|---|---|---|---|
| `research/substrate_discovery_v1/KG0_programme_review.md` | Programme-level review integrating external criticism; establishes accepted criticisms, freeze, priority gates. | Untracked; readable; marked complete. | Hidden unless the task asks for post-review state; it biases independent reconstruction. | Visible; it is core gate evidence. | Visible; it records programme freeze and accepted criticisms. |
| `research/substrate_discovery_v1/PR1_programme_revision.md` | Controlled programme patch after KG0; makes Goal Anchor provisional and gates derivability/internal model. | Untracked; readable; draft/complete patch text; says ready for KG1. | Hidden for blind reconstruction. | Visible; it defines current programme state after review. | Visible; it states consequences and non-changes. |
| `research/substrate_discovery_v1/KG_SPEC.md` | General Programme Gate specification: decisions, lifecycle, burden of proof, evidence rules. | Untracked; readable; draft. | Hidden. | Visible; primary method input. | Visible; governs arbitration form. |
| `research/substrate_discovery_v1/KG_PIPELINE.md` | Gate DAG and dependencies KG0 -> PR1 -> KG1 -> KG2/KG3... | Untracked; readable; draft. | Hidden. | Visible; primary method input. | Visible; dependency status matters. |
| `research/substrate_discovery_v1/KG1_SPEC.md` | Specific Goal Anchor Identity Gate spec. | Untracked; readable; draft; next gate. | Hidden unless the task is explicitly not blind. | Visible; required for KG1 execution. | Visible; defines expected deliverables and prohibitions. |

Visibility rule: a blind KG1-style reconstruction should not see KG0, PR1, KG
specs, or another agent's review. A Programme-Gate execution test should see the
KG/PR layer because the goal is to apply the method, not rediscover it.

## 4. Evidence Corpus

| Path | Short role | Status | Sufficient alone? |
|---|---|---|---|
| `research/door1_postmortem/Door1_Extracted_Knowledge_v1.md` | Durable Door-1/Justitia knowledge extraction and constraints for future substrates. | Primary evidence. | No; it is a synthesis, not the full evidence chain. |
| `research/faithful_abstraction_v1/BRIDGE_MAP_18_1_TO_FA2.md` | Trace from 18.1 through BA and FA; includes Goal Anchor framing and current handoff. | Primary/secondary bridge evidence. | No; must be checked against reports. |
| `research/faithful_abstraction_v1/01_empirical_basis.md` | FA empirical basis; FACT/INFERENCE split. | Primary synthesis evidence. | No; good for FA scope, not complete Goal history. |
| `experiments/JB/JB0_E1_standard_cegar_boundary_assessment/outputs/final_report.md` | Standard CEGAR boundary result; Justitia should not remain Door-1 candidate. | Primary evidence. | No; answers Justitia boundary only. |
| `experiments/FA/FA2_5_E1_candidate_validation/outputs/final_report.md` | Validates compact FA candidate; no discriminative candidate, equivalent to history refinement. | Primary evidence. | No; local to FA candidate. |
| `experiments/BA/BA4_layer_audit/justitia_layer_audit.md` | Static layer audit separating dynamics, policy/control, observation, projection, reporting. | Primary evidence for layer discipline. | No; scope is Justitia/code layer. |
| `experiments/JB/18_1_shielded_training/outputs_18_1/summary.md` | 18.1 kill-gate; abstraction fidelity fails, Level B not run. | Primary evidence. | No; must be combined with BA/FA/JB. |
| `research/monograph_17/Memo_v1.3_17.md` | Directly readable original-memo checkpoint after 17A; reconstructs original goal and transition to perturbation taxonomy. | Historical context / primary historical memo. | No; v1.1/v1.2/v1.4 are absent as standalone files. |
| `research/monograph_17/ASCESIS_PROJECT_INDEX_v2.md` | Post-17F monograph packet index and global goal statement. | Historical context / secondary synthesis. | No. |
| `research/monograph_17/ASCESIS_Research_Methodology_v2.md` | Methodology: synthetic substrates, internal metrics, falsification-first. | Historical/methodological context. | No. |
| `research/monograph_17/ASCESIS_Research_Program_v2.md` | Current post-17F competing explanations and future program before Door1 closure. | Historical context. | No. |
| `research/monograph_17/ASCESIS_Appendix_A_Research_Ledger_v2.md` | Ledger of 17-series constraints and ontology revision log. | Secondary evidence. | No. |
| `research/Claude_kill-gate_review.md` | External hostile review that triggered KG0. | Review layer / criticism, untracked. | No; should be visible only in review/gate tasks. |

Evidence-use warning: BA/FA/JB evidence strongly supports claims about Justitia
abstraction fidelity, layer discipline, compression versus discrimination, and
vacuous conservative boundaries. It does not alone prove world-model emergence
or the full Substrate Discovery programme.

## 5. Historical Corpus

- `ascesis_of_learning_grace/` is historical sandbox material. It contains
  `status.md`, `field_check.md`, `structure.md`, questions/proposals/references,
  archived index material, and dialogue parts. Current banners mark it as
  historical, not the active entry point.
- `research/monograph_17/` is a post-17F reference packet: project index,
  methodology, ontology, programme, scientific context, chronicle, ledger, GPT
  notes, and `Memo_v1.3_17.md`.
- Old sandbox docs and dialogue parts remain useful for historical
  reconstruction and provenance, but they are not live navigation unless a test
  explicitly asks the agent to reconstruct the original programme.
- Old blind-arbiter references have been redirected: the root README says the
  Justitia runtime line is external, while this repository preserves reports and
  evidence. The old `blind_arbiter/` tree was removed in commit `3e3d7ca`.

## 6. Substrate Discovery Corpus

| File | Classification | Review position |
|---|---|---|
| `00_research_axioms.md` | charter | Pre-KG0; frozen as claim source; safe as current charter-under-review, not established evidence. |
| `00_search_frame.md` | charter/search frame | Pre-KG0; frozen until KG1/KG2/KG3; claim under review. |
| `01_research_question.md` | research question | Pre-KG0; central but Goal Anchor provisional after PR1. |
| `02_candidate_axes.md` | candidate map | Pre-KG0; useful vocabulary, not validated property space. |
| `03_Computability_of_Environment.md` | speculative chapter | Pre-KG0; safe only as working vocabulary under review. |
| `04_Derivability.md` | speculative chapter | Pre-KG0; gated by KG2; not established. |
| `04_triage_framework.md` | triage | Pre-KG0; useful draft procedure, but necessity language under review. |
| `05_Interaction_and_Identifiability.md` | speculative chapter | Pre-KG0; prior-art reduction pending. |
| `05_candidate_triage_matrix.md` | candidate map/triage | Pre-KG0; candidate priorities frozen pending KG1/KG2/KG3. |
| `06_Necessary_Properties.md` | speculative chapter | Pre-KG0; title overclaims; property necessity under KG5. |
| `07_Search_Strategy.md` | triage/method | Pre-KG0; allowed as proposed method only. |
| `08_Candidate_Evaluation_Framework.md` | triage/evaluation framework | Pre-KG0; not yet validated by a worked candidate. |
| `09_Open_Problems.md` | speculative/open-problem chapter | Pre-KG0; safe as open question list, not evidence. |
| `2026-06-29_research_session.md` | notes | Pre-KG0; session notes, not settled evidence. |
| `project_names.md` | naming | Pre-KG0; naming only. |
| `KG0_programme_review.md` | programme gate/review layer | Post-KG0; untracked; complete review; safe methodology evidence. |
| `PR1_programme_revision.md` | programme patch | Post-KG0; untracked; draft/complete patch; safe for current programme state. |
| `KG_SPEC.md` | programme gate | Post-KG0; untracked; draft method spec. |
| `KG_PIPELINE.md` | programme gate | Post-KG0; untracked; draft dependency DAG. |
| `KG1_SPEC.md` | programme gate | Post-KG0; untracked; draft Goal Anchor Identity gate spec. |

Current programme status from KG0/PR1: expansion is frozen until KG1, KG2, and
KG3 are resolved. Pre-KG0 chapters may be used as evidence of what the programme
claimed, but not as established proof that those claims survived review.

## 7. Playbook Corpus

| File | Classification | Status |
|---|---|---|
| `research/playbook/README.md` | skeleton | Explicitly says the playbook is not finished. |
| `research/playbook/00_monograph_kill_gates.md` | skeleton | Header-only checklist; not a tested method. |
| `research/playbook/01_playbook_extraction_plan.md` | extraction map | Future extraction sources; not validated. |
| `research/playbook/02_source_artifact_map.md` | extraction map | Maps sources to extract procedure from; not itself a method. |
| `research/playbook/03_preservation_rule.md` | procedural principle | Historical banner vs rewrite rule; useful, but not a full playbook. |
| `research/playbook/04_repository_philosophy.md` | procedural principle | Repository role split; useful navigation philosophy, not a tested method. |

The playbook is not yet a tested method.

## 8. Missing / Ambiguous Inputs

- Standalone original memos `memo_v1.1.md`, `memo_v1.2.md`, and `memo_v1.4.md`
  are absent from the current tree. `Memo_v1.3_17.md` is present and directly
  readable. Other memo states must be reconstructed indirectly from monograph
  ledgers, experiment specs, and git history.
- There is no single `original_programme.md` that states the original objective
  and all later transformations in one canonical place.
- KG documents are untracked and task-dependent. They should be hidden for
  blind reconstruction but visible for methodology/playbook/gate tests.
- Untracked post-17 experiment trees are present and evidence-bearing, but they
  are explicitly deferred from commit/import review.
- Historical docs can look live without context. The banners and
  `research/README.md` should be used to separate active navigation from
  historical evidence.
- `research/Claude_kill-gate_review.md` is untracked hostile review material. It
  should not be visible in blind reconstruction tasks unless the test is about
  reproducing KG0.
- The term "current programme" is ambiguous unless the test says whether it
  means pre-KG0 Substrate Discovery chapters or post-KG0/PR1 frozen state.

## 9. Recommended Clean Test Packages

### Package A — Blind Historical Reconstruction

Purpose: let an agent reconstruct project history without programme-gate
scaffolding.

Visible:
- `README.md`
- `research/README.md`
- historical memos available in-tree, especially
  `research/monograph_17/Memo_v1.3_17.md`
- relevant monograph_17 index/methodology/chronicle/ledger
- `research/door1_postmortem/Door1_Extracted_Knowledge_v1.md`
- `research/faithful_abstraction_v1/BRIDGE_MAP_18_1_TO_FA2.md`
- readable Substrate Discovery chapters `00_*` through `09_*`

Hidden:
- `KG0_programme_review.md`
- `PR1_programme_revision.md`
- `KG_SPEC.md`
- `KG_PIPELINE.md`
- `KG1_SPEC.md`
- `research/Claude_kill-gate_review.md`
- other agents' answers

Expected output: historical reconstruction and independent continuity/drift
analysis.

### Package B — Programme-Gate Execution Test

Purpose: test whether an agent can apply the methodology.

Visible:
- `KG_SPEC.md`
- `KG_PIPELINE.md`
- `KG1_SPEC.md`
- `PR1_programme_revision.md`
- evidence corpus: Door1, BRIDGE_MAP, FA basis, BA/FA/JB reports, monograph_17
  memos

Hidden:
- KG0 if the test wants a fresh KG1 decision rather than KG0 replication
- `research/Claude_kill-gate_review.md` unless the task explicitly includes the
  KG0 review chain
- other agents' answers

Expected output: a KG1 decision document in the required KG1 format.

### Package C — Playbook Usability Test

Purpose: test whether the playbook/procedure is usable by a new agent.

Visible:
- `research/playbook/README.md`
- `research/playbook/00_monograph_kill_gates.md`
- `research/playbook/01_playbook_extraction_plan.md`
- `research/playbook/02_source_artifact_map.md`
- `research/playbook/03_preservation_rule.md`
- `research/playbook/04_repository_philosophy.md`
- `KG_SPEC.md`
- `KG_PIPELINE.md`
- one small evidence packet, e.g. 18.1 summary + BA4 audit + Door1 extraction

Expected output: agent identifies missing instructions, applies what exists, and
reports usability failures rather than pretending the playbook is complete.

## 10. Recommended Next Action

Recommended next action: build a proper playbook test harness before repeating
KG1.

Reason: KG1 can be repeated with a clean package, but the repository currently
has three different test modes that are easy to mix: blind reconstruction,
programme-gate execution, and playbook usability. A small harness should first
define visibility rules, hidden files, expected output schema, and failure
conditions. In parallel, create `original_programme.md` or an equivalent
canonical source packet that states which original memos are present, missing,
or reconstructed indirectly.

Do not proceed as if the playbook is already a tested method.

## 11. Appendix

### Full `git status --short`

State before creating this snapshot file:

```text
?? experiments/14_dsl_core/
?? experiments/15_collapse_boundary/
?? experiments/16_consequence_vs_feature/
?? experiments/17A.2_Semantic_Perturbation_Taxonomy/
?? experiments/17A_backbone_consequence/
?? experiments/17C_interpretive_closure_test/
?? experiments/17D_closure_metric_robustness/
?? experiments/17E_latent_metric_geometry/
?? experiments/17F_cross_substrate_latent_geometry/
?? experiments/17_backbone_consequence/
?? repo_reorg_inventory/commit_checkpoint_report.md
?? research/Claude_kill-gate_review.md
?? research/substrate_discovery_v1/KG0_programme_review.md
?? research/substrate_discovery_v1/KG1_SPEC.md
?? research/substrate_discovery_v1/KG_PIPELINE.md
?? research/substrate_discovery_v1/KG_SPEC.md
?? research/substrate_discovery_v1/PR1_programme_revision.md
```

### File Tree Summaries

`research -maxdepth 3` contains:
- `research/README.md`
- `research/monograph_17/` with 10 files: project index, methodology, ontology,
  programme, chronicle, ledger, scientific context, memo v1.3, and GPT notes.
- `research/door1_postmortem/` with `Door1_Extracted_Knowledge_v1.md`.
- `research/faithful_abstraction_v1/` with programme, empirical basis, theory,
  bridge map, and review packet.
- `research/playbook/` with README, 00-04 skeleton/procedural files.
- `research/substrate_discovery_v1/` with 14 pre-KG0 programme files plus 5
  untracked post-KG0/KG/PR files.
- `research/Claude_kill-gate_review.md` as untracked external review.

`experiments -maxdepth 3` contains:
- tracked legacy experiment families `01` through `08`;
- tracked `13_evolvable_action_strategies`;
- untracked post-17 import trees `14`, `15`, `16`, `17`, `17A`, `17A.2`,
  `17C`, `17D`, `17E`, `17F`;
- tracked `experiments/BA/`, `experiments/FA/`, `experiments/JB/` indexes,
  specs, and evidence reports;
- `experiments/INDEX.md`, `experiments/README.md`, and
  `experiments/validation_summary.md`.

`ascesis_of_learning_grace -maxdepth 3` contains:
- top-level historical docs: `status.md`, `field_check.md`, `structure.md`,
  `questions.md`, `proposals.md`, `glossary.md`, `references.md`,
  `rejected_branches.md`;
- `archive/INDEX.md`;
- dialogue material `dialogs/dialog.part_1.md` through `dialog.part_22.md`,
  plus dialogue `field_check.md` and `subject_index.md`.

`repo_reorg_inventory -maxdepth 2` contains:
- reorganization plans and reports;
- artifact maps in markdown and CSV;
- duplicate/stale candidate report;
- navigation polish report;
- git state and commit plan;
- `commit_checkpoint_report.md` as an intentionally untracked post-commit
  artifact;
- this current-state snapshot.

### Warnings

- The sandboxed `find` command failed with `bwrap: loopback: Failed
  RTM_NEWADDR: Operation not permitted`; tree inspections were rerun with
  escalation to reflect the actual repository.
- KG/PR files are untracked. Treat them as current-state files for local test
  design, but not as committed repository history.
- The final `git status --short` after this file is created will include this
  snapshot as an additional untracked file.
- Substrate Discovery chapters before KG0 are frozen as claims under review, not
  settled evidence.
- The playbook directory is explicitly incomplete.

Current repository state snapshot complete; no files were modified.
