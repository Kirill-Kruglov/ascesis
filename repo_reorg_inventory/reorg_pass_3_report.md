# Reorg Pass 3 Report

Date: 2026-06-29

Scope: stabilize navigation after reorg passes 1-2 and generate a post-reorg inventory. No content-bearing files were deleted.

## 1. Files Created / Changed

Created or updated:

- `research/README.md`
- `experiments/INDEX.md`
- `experiments/BA/INDEX.md`
- `experiments/FA/INDEX.md`
- `experiments/JB/INDEX.md`
- `research/playbook/README.md`
- `research/playbook/02_source_artifact_map.md`
- `repo_reorg_inventory/post_reorg_inventory.md`
- `repo_reorg_inventory/reorg_pass_3_report.md`

Historical reports/specs were not rewritten.

## 2. No-Delete Confirmation

This pass did not delete content-bearing files. It also did not remove:

- `experiments/14_dsl_core/venv/`
- any `outputs/`
- any `results/`
- any `raw/`

`experiments/ascesis_17.zip` is absent in the final state because the user removed it outside this pass; this pass did not search for, restore, or delete it.

## 3. Navigation Indexes Added

- `research/README.md` now identifies `monograph_17`, `faithful_abstraction_v1`, `substrate_discovery_v1`, `door1_postmortem`, and `playbook`, with status and start files.
- `experiments/INDEX.md` now groups the experiment families and points to canonical paths.
- `experiments/BA/INDEX.md`, `experiments/FA/INDEX.md`, and `experiments/JB/INDEX.md` list local experiments, main reports, decision artifacts, and obvious classifications.
- `research/playbook/README.md` now marks the playbook as skeleton / not yet extracted.
- `research/playbook/02_source_artifact_map.md` records source artifacts to mine for procedures.

## 4. Post-Reorg Inventory Summary

Created `repo_reorg_inventory/post_reorg_inventory.md` with:

- current `git status --short`;
- tree view to depth 3;
- remaining untracked roots;
- ignored/generated roots summary;
- human-decision list for `experiments/14_dsl_core/venv/`, stale pre-reorg inventory files, and a note that `experiments/ascesis_17.zip` is absent by user action;
- commit recommendation.

Current top-level remaining untracked roots:

```text
experiments/14_dsl_core
experiments/15_collapse_boundary
experiments/16_consequence_vs_feature
experiments/17A.2_Semantic_Perturbation_Taxonomy
experiments/17A_backbone_consequence
experiments/17C_interpretive_closure_test
experiments/17D_closure_metric_robustness
experiments/17E_latent_metric_geometry
experiments/17F_cross_substrate_latent_geometry
experiments/17_backbone_consequence
experiments/BA
experiments/FA
experiments/INDEX.md
experiments/JB
repo_reorg_inventory/
research/
```

## 5. Recommended Next Pass

1. Human review of `research/README.md`, `experiments/INDEX.md`, and BA/FA/JB indexes.
2. Decide commit strategy for the large untracked experiment/research roots.
3. Decide whether to regenerate `artifact_map.csv` into a new post-reorg CSV rather than overwriting old inventory.
4. Decide separately whether `experiments/14_dsl_core/venv/` remains local-only or is removed in a later approval pass.
5. Run a link check after commit staging if the repository will be published in this layout.

## 6. Claude Code Structural Review Readiness

The repo is ready for Claude Code structural review after human review of the new navigation indexes. The main remaining caveat is that git state still contains many untracked roots from the research program and staged tracked deletions from the extracted `blind_arbiter/` package. That is a commit-policy issue, not a navigation blocker.

Reorg pass 3 complete; repository navigation stabilized and post-reorg inventory generated.
