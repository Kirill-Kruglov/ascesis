# Reorganization Plan

No repository files were moved or deleted in this pass.

## Recommended Order

1. Commit or otherwise preserve this inventory so later changes have a stable audit point.
2. Decide canonical naming for dotted-vs-underscore experiment pairs. Recommendation: keep implementation directories with snake/underscore names and move spec markdown into them as `SPEC.md` or `SPEC_original.md`.
3. Move research-only material from `experiments/` to `research/`: `monograph_17`, `monography_FA`, `Substrate_Discovery_v1`, `Door1_Extracted_Knowledge_v1.md`, and `BRIDGE_MAP_18_1_TO_FA2.md`.
4. Move `blind_arbiter/` to `packages/blind_arbiter/` only if the top-level README links are updated in the same pass.
5. Normalize BA/FA/JB experiment families under `experiments/BA/`, `experiments/FA/`, and `experiments/JB/`.
6. Add ignore rules for `venv/`, `.pytest_cache/`, and local tooling state if the project wants git to stop surfacing them.
7. In a separate approval-gated cleanup pass, remove generated caches and local virtualenvs.
8. In another approval-gated pass, archive or prune reproducible raw outputs while preserving cited reports, summaries, manifests, and final decision artifacts.

## Preservation Rules

- Preserve negative-result evidence. Many old results are scientifically active because README/status use them to justify closed branches.
- Preserve final reports and decision JSON for BA/FA/JB because they form the post-Justitia evidence chain.
- Do not let reporting-only artifacts become safety evidence during reorganization; keep layer-audit distinctions visible.
- Do not delete old tracked material solely because git history exists until the human approves that exact deletion set.

## Safe next actions

These commands are safe candidates for the next pass, but were not run:

```sh
git status --short
mkdir -p research packages experiments/BA experiments/FA experiments/JB archive/deprecated_specs archive/old_outputs archive/binary_snapshots
git diff -- repo_reorg_inventory/
git add repo_reorg_inventory/
git commit -m "Add repository artifact inventory"
```

After the inventory is committed, safe inspection commands:

```sh
find experiments -maxdepth 2 -type d | sort
find experiments -maxdepth 3 -type f -name '*final*' -o -name '*summary*' -o -name '*report*'
git ls-files --others --exclude-standard | sed -n '1,200p'
```

## Dangerous actions requiring confirmation

- Deleting `experiments/14_dsl_core/venv/`.
- Deleting any `__pycache__/` or `.pytest_cache/` tree, even though these are generated.
- Deleting or archiving `experiments/ascesis_17.zip` before confirming its contents are duplicated elsewhere.
- Merging dotted spec directories into underscore implementation directories.
- Moving `blind_arbiter/` to `packages/blind_arbiter/`, because README and links must change at the same time.
- Moving `experiments/monograph_17`, `experiments/monography_FA`, or `experiments/Substrate_Discovery_v1` into `research/` before agreeing on final naming.
- Pruning raw outputs, proof dumps, PNG/SVG figures, or CSV files that may be cited by monographs or reports.
- Changing `.gitignore` to hide currently visible untracked artifacts without deciding whether they should be committed first.

Inventory classification complete; no repository files were moved or deleted.
