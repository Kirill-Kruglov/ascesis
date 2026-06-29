# Commit Plan

This plan prepares human review and commit staging after reorg passes 1-4. It does not assume that commands have been run. Review paths before staging because the current worktree contains large untracked evidence trees and already-staged tracked deletions from `blind_arbiter/`.

## Commit 1 - Remove extracted blind_arbiter package and point to external Justitia repo

Purpose: remove the stale local blind-arbiter implementation after extraction to <https://github.com/Kirill-Kruglov/justitia>, while keeping live README navigation accurate.

Paths to stage:

- `blind_arbiter/` tracked deletions
- `README.md`
- `experiments/README.md`

Commands:

```sh
git rm -r blind_arbiter/
git add README.md experiments/README.md
```

Current-state note: `blind_arbiter/` deletions already appear staged from pass 2 (`D  ...`). If committing from the current worktree, verify with `git status --short`; if already staged, do not rerun `git rm -r blind_arbiter/`.

Risk level: medium.

Review notes: confirm that the external Justitia URL is correct and that no live navigation still points to local `../blind_arbiter/`.

## Commit 2 - Add research tree and active writing skeletons

Purpose: move research docs out of `experiments/`, preserve monograph/FA/Substrate Discovery/Door-1 postmortem material, and add the playbook skeleton.

Paths to stage:

- `research/`

Commands:

```sh
git add research/
```

Risk level: medium.

Review notes: check that `research/README.md` clearly marks Substrate Discovery and playbook as active/draft work, and that historical monograph/FA docs are reference material rather than rewritten theory.

## Commit 3 - Add BA/FA/JB evidence trees and experiment navigation indexes

Purpose: preserve reorganized Boundary Analysis, Faithful Abstraction, and Justitia Boundary evidence chains under canonical family directories.

Paths to stage:

- `experiments/BA/`
- `experiments/FA/`
- `experiments/JB/`
- `experiments/INDEX.md`

Commands:

```sh
git add experiments/BA/ experiments/FA/ experiments/JB/ experiments/INDEX.md
```

Risk level: medium-high.

Review notes: verify that outputs remain present, `SPEC_original.md` files are in the expected canonical directories, and BA/FA/JB indexes do not overclaim safety or theory results.

## Commit 4 - Track post-17 experiment implementations and evidence, if approved

Purpose: bring the post-17 experimental trees into version control as evidence-producing experiment packages. This is optional and should be reviewed because it may be large.

Paths to stage:

- `experiments/14_dsl_core/`
- `experiments/15_collapse_boundary/`
- `experiments/16_consequence_vs_feature/`
- `experiments/17_backbone_consequence/`
- `experiments/17A_backbone_consequence/`
- `experiments/17A.2_Semantic_Perturbation_Taxonomy/`
- `experiments/17C_interpretive_closure_test/`
- `experiments/17D_closure_metric_robustness/`
- `experiments/17E_latent_metric_geometry/`
- `experiments/17F_cross_substrate_latent_geometry/`

Commands:

```sh
git add experiments/14_dsl_core/ experiments/15_collapse_boundary/ experiments/16_consequence_vs_feature/ experiments/17_backbone_consequence/ experiments/17A_backbone_consequence/ experiments/17A.2_Semantic_Perturbation_Taxonomy/ experiments/17C_interpretive_closure_test/ experiments/17D_closure_metric_robustness/ experiments/17E_latent_metric_geometry/ experiments/17F_cross_substrate_latent_geometry/
```

Risk level: high.

Review notes: `experiments/14_dsl_core/venv/` has been removed and `.gitignore` now excludes local virtualenvs. Confirm generated outputs are intended evidence before staging this commit; do not prune outputs/results/raw as part of this pass.

## Commit 5 - Add reorganization inventory, review packets, and local ignore rules

Purpose: preserve the reorg audit trail, commit-prep plan, Claude structural review prompt, and explicit local-artifact ignore rules.

Paths to stage:

- `.gitignore`
- `repo_reorg_inventory/`

Commands:

```sh
git add .gitignore repo_reorg_inventory/
```

Risk level: low-medium.

Review notes: `repo_reorg_inventory/artifact_map.*` and `git_state.md` are intentionally stale pre-reorg evidence; `post_reorg_inventory.md` and `reorg_pass_4_commit_prep_report.md` are the current commit-prep references.

## Suggested Review Order

1. Run `git status --short`.
2. Review this plan against the current status; adjust commands if staged deletions are already present.
3. Stage one commit at a time.
4. After each staging step, inspect with `git diff --cached --stat` and `git diff --cached --check`.
5. Do not combine Commit 4 with smaller navigation commits unless the reviewer explicitly wants one large historical import commit.
