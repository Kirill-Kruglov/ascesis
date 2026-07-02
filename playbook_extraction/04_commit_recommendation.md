# 04 — Commit recommendation (untracked-tree triage)

Recommend only. Kirill decides all commits and all destructive operations. No
files were moved, deleted, or staged to produce this.

Tags: **FACT**, **INFERENCE**, **RECOMMENDATION**.

---

## Context

**FACT.** The snapshot (§1) and `commit_checkpoint_report.md` show four reorg
commits done, with "Optional Commit 5" (post-17 experiment import) explicitly
deferred for human review. Current untracked roots: ten post-17 experiment trees,
the KG/PR programme-gate layer, the Claude review, and two reorg reports.

**INFERENCE.** This extraction depends on a specific subset of the untracked
material. That subset should be committed so the method extraction is reproducible;
the rest follows the checkpoint report's existing deferral.

---

## Tier 1 — Evidence the method extraction depends on (RECOMMEND COMMIT)

**RECOMMENDATION.** These are cited as load-bearing evidence in this pass and
should be committed so `playbook_extraction/` does not reference untracked files:

| path | why it must be committed | size |
|---|---|---|
| `research/substrate_discovery_v1/KG_SPEC.md` | the programme-gate method spec; cited throughout | small |
| `research/substrate_discovery_v1/KG_PIPELINE.md` | gate DAG; defines KG0→KG6 state | small |
| `research/substrate_discovery_v1/KG0_programme_review.md` | the one worked programme-gate example | small |
| `research/substrate_discovery_v1/PR1_programme_revision.md` | the programme patch KG0 produced | small |
| `research/substrate_discovery_v1/KG1_SPEC.md` | next-gate spec (note: currently unrunnable, §D of 03) | small |
| `research/Claude_kill-gate_review.md` | the external review that triggered KG0; cited as method-evidence | small |
| `experiments/15_collapse_boundary/` | worked example for steps 5/6/9 (non-saturation, free-monoid, parallel-reality) | 9.4M |

**INFERENCE.** The KG/PR layer is text-only and small; committing it has no
downside and removes the "untracked, task-dependent" ambiguity the snapshot flags.
`15_collapse_boundary` is the only post-17 tree this extraction cites directly (the
15.2 lessons); committing it makes step 5/6/9 evidence durable. **RECOMMENDATION:**
commit `15_collapse_boundary` minus its generated artifacts (see Tier 4).

## Tier 2 — Evidence-bearing but not cited here (DEFER per existing plan)

**RECOMMENDATION.** Leave as the checkpoint report already decided — import in a
separate, explicit, human-reviewed commit, optionally split by family:

| path | note | size |
|---|---|---|
| `experiments/16_consequence_vs_feature/` | post-17 evidence, not cited in this pass | 328K |
| `experiments/17_backbone_consequence/` + `17A`, `17A.2`, `17C`, `17D`, `17E`, `17F` | the post-17 monograph evidence chain; evidence-bearing but outside this extraction's scope | ~67M total |
| `experiments/14_dsl_core/` (its source/specs) | DSL core; large mostly because of generated content (Tier 4) | 114M incl. venv |

**INFERENCE.** Committing ~180M of post-17 trees blindly is exactly what the task
and the checkpoint report warn against. These are not duplicates or stale — they
are real evidence — but they are not needed for the playbook extraction and deserve
their own review.

## Tier 3 — This extraction's own output (RECOMMEND COMMIT separately)

**RECOMMENDATION.** `playbook_extraction/` (this directory) should be committed as
its own docs commit, after Kirill reviews it, with a message like
`docs: add falsification-playbook extract-and-test pass (working label)`. It must
not be merged into an evidence-import commit.

## Tier 4 — Generated / stale (RECOMMEND EXCLUDE, do not delete without approval)

**FACT.** `duplicate_and_stale_candidates.md` already lists these. Before any
commit of Tier 1/Tier 2 trees:

| pattern | action | reason (from the stale report) |
|---|---|---|
| `experiments/14_dsl_core/venv` | exclude / gitignore | local virtualenv, ~100M, reproducible |
| `**/__pycache__`, `**/.pytest_cache` | exclude | bytecode/test cache; already gitignored |
| `experiments/14_dsl_core/worldcore/outputs/proofs` | archive bulk, keep sampled/final | large generated proof dump |
| `experiments/ascesis_17.zip` (if present) | confirm before deletion | likely duplicates monograph/experiment files |
| `experiments/*/outputs*` raw bulk | keep `final_report.md`/`summary.md`/decision JSONs; archive raw if reproducible | preserve evidence, not build products |

**RECOMMENDATION.** Do not delete anything in Tier 4 in this pass. Recommend a
later, explicit "archive generated artifacts" pass. Deletion is Kirill's call.

## Tier 5 — Duplicate dotted vs underscore experiment dirs (RECOMMEND a compare-then-merge pass, not now)

**FACT.** `duplicate_and_stale_candidates.md` lists spec-only dotted dirs
(`BA1.E1_…`, `FA2.5.E1_…`, `JB0.E1_…`, etc.) paralleling the underscore
implementation dirs that hold the outputs this pass cites. **RECOMMENDATION:**
before merging, hash/diff contents (the report says the BA2 pair both contain
outputs); do not assume the dotted dir is redundant. Out of scope for this pass.

---

## Summary recommendation

1. **Commit now (small, text-only):** the KG/PR layer + Claude review (Tier 1).
2. **Commit now (after excluding Tier 4 artifacts):** `15_collapse_boundary`.
3. **Commit separately after review:** `playbook_extraction/` (Tier 3).
4. **Defer with explicit review:** the rest of the post-17 trees (Tier 2).
5. **Do not delete anything;** schedule a later archive/merge pass for Tier 4/5.
