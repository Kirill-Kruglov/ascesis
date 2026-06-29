# Reorg Pass 2 Report

Date: 2026-06-29

Scope: cleanup after safe reorganization pass 1. This pass removed the extracted local blind-arbiter package, generated local caches/tooling state, and the confirmed duplicate BA2 dotted output tree. BA/FA/JB evidence, `research/`, old tracked experiments, `experiments/14_dsl_core/`, `experiments/ascesis_17.zip`, outputs, results, raw folders, and `venv/` were preserved.

## 1. Files Changed

- `README.md`
  - Removed the local `blind_arbiter/` current-active package reference.
  - Added the external Justitia repository link: <https://github.com/Kirill-Kruglov/justitia>.
  - Changed the old current-direction heading to an extracted-line heading.
- `experiments/README.md`
  - Replaced the local `../blind_arbiter/` extracted-package link with the external Justitia repository link.
- `research/substrate_discovery_v1/project_names.md`
  - Added working project-name note with candidate names `Limes`, `Methodus`, and `Disciplina`.
- `research/playbook/README.md`
  - Added playbook skeleton README.
- `research/playbook/00_monograph_kill_gates.md`
  - Added checklist headings for monograph kill-gates.
- `research/playbook/01_playbook_extraction_plan.md`
  - Added future extraction source list.
- `repo_reorg_inventory/reorg_pass_2_report.md`
  - This report.

## 2. Files Deleted

### Extracted Package

Deleted `blind_arbiter/` via `git rm -r`, then removed ignored leftovers from the same directory.

Tracked deleted files staged by git:

```text
blind_arbiter/README.md
blind_arbiter/SPEC.md
blind_arbiter/camouflage_audit/SPEC.md
blind_arbiter/camouflage_audit/results/audit_surface_best_gamma.svg
blind_arbiter/camouflage_audit/results/gamma_audit_off.svg
blind_arbiter/camouflage_audit/results/raw/per_seed.csv
blind_arbiter/camouflage_audit/results/raw/results.json
blind_arbiter/camouflage_audit/results/raw/surface.csv
blind_arbiter/camouflage_audit/results/report.md
blind_arbiter/camouflage_audit/results/run_manifest.json
blind_arbiter/camouflage_audit/results/validation_report.md
blind_arbiter/camouflage_audit/run.py
blind_arbiter/references.md
blind_arbiter/results/audit_report.md
blind_arbiter/results/corr_sa_over_time.svg
blind_arbiter/results/failure_mode_camouflage.svg
blind_arbiter/results/failure_mode_collective_hack.svg
blind_arbiter/results/failure_mode_collective_punishment.svg
blind_arbiter/results/permanence_survival.svg
blind_arbiter/results/raw/results.csv
blind_arbiter/results/raw/results.json
blind_arbiter/results/report.md
blind_arbiter/results/run_manifest.json
blind_arbiter/results/validation_report.md
blind_arbiter/run.py
blind_arbiter/strategic_camouflage/SPEC.md
blind_arbiter/strategic_camouflage/results/concealment_surface_strong_gamma.svg
blind_arbiter/strategic_camouflage/results/gamma_audit_off.svg
blind_arbiter/strategic_camouflage/results/permanence_surface_strong_gamma.svg
blind_arbiter/strategic_camouflage/results/raw/calibration_per_seed.csv
blind_arbiter/strategic_camouflage/results/raw/per_seed.csv
blind_arbiter/strategic_camouflage/results/raw/results.json
blind_arbiter/strategic_camouflage/results/raw/surface.csv
blind_arbiter/strategic_camouflage/results/report.md
blind_arbiter/strategic_camouflage/results/run_manifest.json
blind_arbiter/strategic_camouflage/results/validation_report.md
blind_arbiter/strategic_camouflage/run.py
```

### Generated Local Artifacts

Deleted generated local-only artifacts:

- `.claude/`
- `57` cache directories matching `__pycache__` or `.pytest_cache` outside `venv/`

`venv/` was explicitly preserved.

### Duplicate BA2 Dotted Outputs

Deleted:

```text
experiments/BA2.E1_Semantic_benefit_vs_structural_cost_map/
```

This was done only after `diff -qr` confirmed that its `outputs/` tree was identical to:

```text
experiments/BA/BA2_E1_semantic_benefit_vs_structural_cost_map/outputs/
```

## 3. Reason For Deleting `blind_arbiter/`

The blind-arbiter/Justitia line has been extracted and completed separately at:

<https://github.com/Kirill-Kruglov/justitia>

Keeping the old local package in this repo would preserve a stale duplicate implementation. The Ascesis repository now keeps the research trail and the emerging Substrate Discovery / playbook work; the extracted Justitia line points to the external repository.

## 4. README Changes

Top-level `README.md` now states that the blind-arbiter/Justitia line has been extracted into the external Justitia repository and that Ascesis preserves the research trail plus Substrate Discovery / playbook work.

`experiments/README.md` now points to the external Justitia repository rather than `../blind_arbiter/`.

No broad framing rewrite was performed.

## 5. Generated Caches Removed

Removed generated caches/tooling state only:

- `.claude/`
- `__pycache__/` directories outside `venv/`
- `.pytest_cache/` directories outside `venv/`

Not removed:

- `experiments/14_dsl_core/venv/`
- any `outputs/`
- any `results/`
- any `raw/`
- `experiments/ascesis_17.zip`

## 6. BA2 Duplicate Handling

`diff -qr` returned no differences between the dotted BA2 outputs and the canonical BA2 outputs under `experiments/BA/`. The dotted duplicate directory was therefore deleted as allowed by the pass 2 instructions.

No BA/FA/JB/Justitia evidence outputs were deleted.

## 7. Git Status After Pass

```text
 M README.md
D  blind_arbiter/README.md
D  blind_arbiter/SPEC.md
D  blind_arbiter/camouflage_audit/SPEC.md
D  blind_arbiter/camouflage_audit/results/audit_surface_best_gamma.svg
D  blind_arbiter/camouflage_audit/results/gamma_audit_off.svg
D  blind_arbiter/camouflage_audit/results/raw/per_seed.csv
D  blind_arbiter/camouflage_audit/results/raw/results.json
D  blind_arbiter/camouflage_audit/results/raw/surface.csv
D  blind_arbiter/camouflage_audit/results/report.md
D  blind_arbiter/camouflage_audit/results/run_manifest.json
D  blind_arbiter/camouflage_audit/results/validation_report.md
D  blind_arbiter/camouflage_audit/run.py
D  blind_arbiter/references.md
D  blind_arbiter/results/audit_report.md
D  blind_arbiter/results/corr_sa_over_time.svg
D  blind_arbiter/results/failure_mode_camouflage.svg
D  blind_arbiter/results/failure_mode_collective_hack.svg
D  blind_arbiter/results/failure_mode_collective_punishment.svg
D  blind_arbiter/results/permanence_survival.svg
D  blind_arbiter/results/raw/results.csv
D  blind_arbiter/results/raw/results.json
D  blind_arbiter/results/report.md
D  blind_arbiter/results/run_manifest.json
D  blind_arbiter/results/validation_report.md
D  blind_arbiter/run.py
D  blind_arbiter/strategic_camouflage/SPEC.md
D  blind_arbiter/strategic_camouflage/results/concealment_surface_strong_gamma.svg
D  blind_arbiter/strategic_camouflage/results/gamma_audit_off.svg
D  blind_arbiter/strategic_camouflage/results/permanence_surface_strong_gamma.svg
D  blind_arbiter/strategic_camouflage/results/raw/calibration_per_seed.csv
D  blind_arbiter/strategic_camouflage/results/raw/per_seed.csv
D  blind_arbiter/strategic_camouflage/results/raw/results.json
D  blind_arbiter/strategic_camouflage/results/raw/surface.csv
D  blind_arbiter/strategic_camouflage/results/report.md
D  blind_arbiter/strategic_camouflage/results/run_manifest.json
D  blind_arbiter/strategic_camouflage/results/validation_report.md
D  blind_arbiter/strategic_camouflage/run.py
 M experiments/README.md
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
?? experiments/BA/
?? experiments/FA/
?? experiments/JB/
?? experiments/ascesis_17.zip
?? repo_reorg_inventory/
?? research/
```

## 8. Recommended Next Pass

1. Review and commit pass 1 + pass 2 together or as two explicit commits.
2. Regenerate `repo_reorg_inventory/artifact_map.*` after accepting the new structure, because the old inventory still references pre-pass paths.
3. Decide whether to add `.gitignore` rules for generated caches and local tooling state now that they have been removed.
4. Decide separately whether `experiments/14_dsl_core/venv/` should be removed in a later explicit approval pass.
5. Decide separately whether `experiments/ascesis_17.zip` should be archived or deleted after confirming its contents.
6. Normalize links inside older reports/specs only if those documents are intended to be live navigation, not immutable historical evidence.

Reorg pass 2 complete; extracted Justitia/blind-arbiter line now points to external repository.
