# Navigation Polish Report

Date: 2026-06-29

Scope: final navigation polish before the first reorganization commit. No directories were moved, no experiments were renamed, and no evidence artifacts were deleted.

## Files Updated

- `ascesis_of_learning_grace/status.md`
- `ascesis_of_learning_grace/field_check.md`
- `experiments/validation_summary.md`
- `experiments/INDEX.md`
- `research/substrate_discovery_v1/project_names.md`

## Files Created

- `research/playbook/03_preservation_rule.md`
- `research/playbook/04_repository_philosophy.md`
- `repo_reorg_inventory/navigation_polish_report.md`

## Historical Banners Added

- Added a `Historical Sandbox` banner to `ascesis_of_learning_grace/status.md`.
- Added a `Historical Sandbox Field Check` banner to `ascesis_of_learning_grace/field_check.md`.

The banners mark both files as historical documents, point to the external Justitia repository, and identify `research/README.md` as the current active research entry point.

## Navigation Fixes

- Replaced the removed local `../blind_arbiter/` reference in `status.md` with <https://github.com/Kirill-Kruglov/justitia>.
- Replaced removed local `../../blind_arbiter/references.md` references in `field_check.md` with the external Justitia repository.
- Live navigation references in `README.md`, `experiments/README.md`, `research/README.md`, and `experiments/INDEX.md` already pointed to current locations or external Justitia where appropriate.

## Validation Summary

- Changed `experiments/validation_summary.md` title and audience wording to state that it summarizes experiments 01-06.
- Added a short historical note pointing readers to later experiment families in `experiments/INDEX.md`.
- Did not expand the summary to cover later experiments.

## Index Fixes

- Reworked `experiments/INDEX.md` to avoid overlap between the old 13-17F row and the 14-17 sequence row.
- Split experiment 13 into its own row and pointed to `experiments/13_evolvable_action_strategies/SPEC_IMPLEMENTED.md`, since no README exists there.
- Added a note that experiments 09-12 are historically contained inside `experiments/08_blind_consequence_feeder_viability/`.

## Project-Name Updates

- Kept stable candidates in `research/substrate_discovery_v1/project_names.md`:
  - `Limes`
  - `Methodus`
  - `Disciplina`
- Added an `Experimental Candidates` section with:
  - `Popperside`
  - `Poppercide`
- No ranking was added.

## Historical Text Rewrite Check

No historical body text was rewritten except for narrow navigation fixes replacing removed local blind-arbiter paths with the external Justitia repository. Historical framing was added through banners rather than body modernization.

Navigation polish complete.

Historical integrity preserved.

Repository ready for first commit unless reviewer requests additional changes.
