# Artifact Map

Inventory generated without moving, deleting, renaming, or editing pre-existing project files. The inventory intentionally groups noisy generated directories such as `venv`, `.pytest_cache`, `__pycache__`, raw result folders, and proof dumps. Full row-level data is in `artifact_map.csv`.

## Summary Counts

| dimension | value | count |
|---|---:|---:|
| phase | `blind_arbiter` | 41 |
| phase | `boundary_analysis` | 85 |
| phase | `experiments_01_08` | 155 |
| phase | `experiments_13_18` | 529 |
| phase | `faithful_abstraction` | 64 |
| phase | `justitia_boundary` | 62 |
| phase | `monograph_or_research_docs` | 52 |
| phase | `substrate_discovery` | 16 |
| phase | `unknown` | 8 |
| keep_status | `archive_candidate` | 12 |
| keep_status | `delete_candidate` | 64 |
| keep_status | `duplicate_candidate` | 27 |
| keep_status | `keep_active` | 105 |
| keep_status | `keep_reference` | 800 |
| keep_status | `needs_human_review` | 4 |
| type | `archive` | 61 |
| type | `code` | 184 |
| type | `config` | 4 |
| type | `experiment` | 85 |
| type | `memo` | 89 |
| type | `monograph` | 13 |
| type | `result` | 569 |
| type | `review` | 3 |
| type | `unknown` | 4 |

## Phase-Level Map

### monograph_or_research_docs

| path | type | git state | keep | destination |
|---|---|---|---|---|
| `.gitignore` | config | tracked | keep_active | `.gitignore` |
| `CITATION.cff` | config | tracked | keep_active | `CITATION.cff` |
| `CONTRIBUTORS.md` | memo | tracked | keep_active | `CONTRIBUTORS.md` |
| `LICENSE` | config | tracked | keep_active | `LICENSE` |
| `README.md` | memo | tracked | keep_active | `README.md` |
| `ascesis_of_learning_grace` | memo | tracked+ignored | keep_active | `research/ascesis_of_learning_grace` |
| `ascesis_of_learning_grace/archive` | memo | tracked | keep_active | `research/ascesis_of_learning_grace/archive` |
| `ascesis_of_learning_grace/archive/INDEX.md` | memo | tracked | keep_active | `research/ascesis_of_learning_grace/archive/INDEX.md` |
| `ascesis_of_learning_grace/dialogs` | memo | ignored | keep_active | `research/ascesis_of_learning_grace/dialogs` |
| `ascesis_of_learning_grace/dialogs/dialog.part_1.md` | memo | ignored | keep_active | `research/ascesis_of_learning_grace/dialogs/dialog.part_1.md` |
| `ascesis_of_learning_grace/dialogs/dialog.part_10.md` | memo | ignored | keep_active | `research/ascesis_of_learning_grace/dialogs/dialog.part_10.md` |
| `ascesis_of_learning_grace/dialogs/dialog.part_11.md` | memo | ignored | keep_active | `research/ascesis_of_learning_grace/dialogs/dialog.part_11.md` |
| `ascesis_of_learning_grace/dialogs/dialog.part_12.md` | memo | ignored | keep_active | `research/ascesis_of_learning_grace/dialogs/dialog.part_12.md` |
| `ascesis_of_learning_grace/dialogs/dialog.part_13.md` | memo | ignored | keep_active | `research/ascesis_of_learning_grace/dialogs/dialog.part_13.md` |
| `ascesis_of_learning_grace/dialogs/dialog.part_14.md` | memo | ignored | keep_active | `research/ascesis_of_learning_grace/dialogs/dialog.part_14.md` |
| `ascesis_of_learning_grace/dialogs/dialog.part_15.md` | memo | ignored | keep_active | `research/ascesis_of_learning_grace/dialogs/dialog.part_15.md` |
| `ascesis_of_learning_grace/dialogs/dialog.part_16.md` | memo | ignored | keep_active | `research/ascesis_of_learning_grace/dialogs/dialog.part_16.md` |
| `ascesis_of_learning_grace/dialogs/dialog.part_17.md` | memo | ignored | keep_active | `research/ascesis_of_learning_grace/dialogs/dialog.part_17.md` |
| `ascesis_of_learning_grace/dialogs/dialog.part_18.md` | memo | ignored | keep_active | `research/ascesis_of_learning_grace/dialogs/dialog.part_18.md` |
| `ascesis_of_learning_grace/dialogs/dialog.part_19.md` | memo | ignored | keep_active | `research/ascesis_of_learning_grace/dialogs/dialog.part_19.md` |
| `ascesis_of_learning_grace/dialogs/dialog.part_2.md` | memo | ignored | keep_active | `research/ascesis_of_learning_grace/dialogs/dialog.part_2.md` |
| `ascesis_of_learning_grace/dialogs/dialog.part_20.md` | memo | ignored | keep_active | `research/ascesis_of_learning_grace/dialogs/dialog.part_20.md` |
| `ascesis_of_learning_grace/dialogs/dialog.part_21.md` | memo | ignored | keep_active | `research/ascesis_of_learning_grace/dialogs/dialog.part_21.md` |
| `ascesis_of_learning_grace/dialogs/dialog.part_22.md` | memo | ignored | keep_active | `research/ascesis_of_learning_grace/dialogs/dialog.part_22.md` |
| `ascesis_of_learning_grace/dialogs/dialog.part_3.md` | memo | ignored | keep_active | `research/ascesis_of_learning_grace/dialogs/dialog.part_3.md` |
| `ascesis_of_learning_grace/dialogs/dialog.part_4.md` | memo | ignored | keep_active | `research/ascesis_of_learning_grace/dialogs/dialog.part_4.md` |
| `ascesis_of_learning_grace/dialogs/dialog.part_5.md` | memo | ignored | keep_active | `research/ascesis_of_learning_grace/dialogs/dialog.part_5.md` |
| `ascesis_of_learning_grace/dialogs/dialog.part_6.md` | memo | ignored | keep_active | `research/ascesis_of_learning_grace/dialogs/dialog.part_6.md` |
| `ascesis_of_learning_grace/dialogs/dialog.part_7.md` | memo | ignored | keep_active | `research/ascesis_of_learning_grace/dialogs/dialog.part_7.md` |
| `ascesis_of_learning_grace/dialogs/dialog.part_8.md` | memo | ignored | keep_active | `research/ascesis_of_learning_grace/dialogs/dialog.part_8.md` |
| `ascesis_of_learning_grace/dialogs/dialog.part_9.md` | memo | ignored | keep_active | `research/ascesis_of_learning_grace/dialogs/dialog.part_9.md` |
| `ascesis_of_learning_grace/dialogs/field_check.md` | memo | ignored | keep_active | `research/ascesis_of_learning_grace/dialogs/field_check.md` |
| `ascesis_of_learning_grace/dialogs/subject_index.md` | memo | ignored | keep_active | `research/ascesis_of_learning_grace/dialogs/subject_index.md` |
| `ascesis_of_learning_grace/field_check.md` | memo | tracked | keep_active | `research/ascesis_of_learning_grace/field_check.md` |
| `ascesis_of_learning_grace/glossary.md` | memo | tracked | keep_active | `research/ascesis_of_learning_grace/glossary.md` |
| `ascesis_of_learning_grace/proposals.md` | memo | tracked | keep_active | `research/ascesis_of_learning_grace/proposals.md` |
| `ascesis_of_learning_grace/questions.md` | memo | tracked | keep_active | `research/ascesis_of_learning_grace/questions.md` |
| `ascesis_of_learning_grace/references.md` | memo | tracked | keep_active | `research/ascesis_of_learning_grace/references.md` |
| `ascesis_of_learning_grace/rejected_branches.md` | memo | tracked | keep_active | `research/ascesis_of_learning_grace/rejected_branches.md` |
| `ascesis_of_learning_grace/status.md` | memo | tracked | keep_active | `research/ascesis_of_learning_grace/status.md` |
| `ascesis_of_learning_grace/structure.md` | memo | tracked | keep_active | `research/ascesis_of_learning_grace/structure.md` |
| `experiments/Memo_v1.3 _17.md` | memo | untracked | keep_active | `experiments/Memo_v1.3 _17.md` |
| `experiments/monograph_17` | experiment | untracked | keep_reference | `research/monograph_17` |
| `experiments/monograph_17/ASCESIS_Appendix_A_Research_Ledger_v2.md` | monograph | untracked | keep_reference | `research/monograph_17/ASCESIS_Appendix_A_Research_Ledger_v2.md` |
| `experiments/monograph_17/ASCESIS_Experimental_Chronicle_v2.md` | monograph | untracked | keep_reference | `research/monograph_17/ASCESIS_Experimental_Chronicle_v2.md` |
| `experiments/monograph_17/ASCESIS_PROJECT_INDEX_v2.md` | monograph | untracked | keep_reference | `research/monograph_17/ASCESIS_PROJECT_INDEX_v2.md` |
| `experiments/monograph_17/ASCESIS_Research_Methodology_v2.md` | monograph | untracked | keep_reference | `research/monograph_17/ASCESIS_Research_Methodology_v2.md` |
| `experiments/monograph_17/ASCESIS_Research_Ontology_Part_I_—_Foundations_&_Research_Ontology_Version_2.0_Post-17F.md` | monograph | unknown | keep_reference | `research/monograph_17/ASCESIS_Research_Ontology_Part_I_—_Foundations_&_Research_Ontology_Version_2.0_Post-17F.md` |
| `experiments/monograph_17/ASCESIS_Research_Program_v2.md` | monograph | untracked | keep_reference | `research/monograph_17/ASCESIS_Research_Program_v2.md` |
| `experiments/monograph_17/ASCESIS_Scientific_Context_v2.md` | monograph | untracked | keep_reference | `research/monograph_17/ASCESIS_Scientific_Context_v2.md` |
| `experiments/monograph_17/GPT_eval17F.md` | monograph | untracked | keep_reference | `research/monograph_17/GPT_eval17F.md` |
| `experiments/monograph_17/GPT_summary.md` | monograph | untracked | keep_reference | `research/monograph_17/GPT_summary.md` |

### blind_arbiter

| path | type | git state | keep | destination |
|---|---|---|---|---|
| `blind_arbiter` | experiment | tracked+ignored | keep_reference | `packages/blind_arbiter` |
| `blind_arbiter/README.md` | memo | tracked | keep_reference | `packages/blind_arbiter/README.md` |
| `blind_arbiter/SPEC.md` | experiment | tracked | keep_reference | `packages/blind_arbiter/SPEC.md` |
| `blind_arbiter/__pycache__` | archive | ignored | delete_candidate | `no destination; remove from working tree after approval or keep ignored locally` |
| `blind_arbiter/camouflage_audit` | experiment | tracked+ignored | keep_reference | `packages/blind_arbiter/camouflage_audit` |
| `blind_arbiter/camouflage_audit/SPEC.md` | experiment | tracked | keep_reference | `packages/blind_arbiter/camouflage_audit/SPEC.md` |
| `blind_arbiter/camouflage_audit/__pycache__` | archive | ignored | delete_candidate | `no destination; remove from working tree after approval or keep ignored locally` |
| `blind_arbiter/camouflage_audit/results` | result | tracked | keep_reference | `packages/blind_arbiter/camouflage_audit/results` |
| `blind_arbiter/camouflage_audit/results/audit_surface_best_gamma.svg` | result | tracked | keep_reference | `packages/blind_arbiter/camouflage_audit/results/audit_surface_best_gamma.svg` |
| `blind_arbiter/camouflage_audit/results/gamma_audit_off.svg` | result | tracked | keep_reference | `packages/blind_arbiter/camouflage_audit/results/gamma_audit_off.svg` |
| `blind_arbiter/camouflage_audit/results/raw` | result | tracked | archive_candidate | `packages/blind_arbiter/camouflage_audit/results/raw` |
| `blind_arbiter/camouflage_audit/results/report.md` | result | tracked | keep_reference | `packages/blind_arbiter/camouflage_audit/results/report.md` |
| `blind_arbiter/camouflage_audit/results/run_manifest.json` | result | tracked | keep_reference | `packages/blind_arbiter/camouflage_audit/results/run_manifest.json` |
| `blind_arbiter/camouflage_audit/results/validation_report.md` | result | tracked | keep_reference | `packages/blind_arbiter/camouflage_audit/results/validation_report.md` |
| `blind_arbiter/camouflage_audit/run.py` | code | tracked | keep_reference | `packages/blind_arbiter/camouflage_audit/run.py` |
| `blind_arbiter/references.md` | memo | tracked | keep_reference | `packages/blind_arbiter/references.md` |
| `blind_arbiter/results` | result | tracked | keep_reference | `packages/blind_arbiter/results` |
| `blind_arbiter/results/audit_report.md` | result | tracked | keep_reference | `packages/blind_arbiter/results/audit_report.md` |
| `blind_arbiter/results/corr_sa_over_time.svg` | result | tracked | keep_reference | `packages/blind_arbiter/results/corr_sa_over_time.svg` |
| `blind_arbiter/results/failure_mode_camouflage.svg` | result | tracked | keep_reference | `packages/blind_arbiter/results/failure_mode_camouflage.svg` |
| `blind_arbiter/results/failure_mode_collective_hack.svg` | result | tracked | keep_reference | `packages/blind_arbiter/results/failure_mode_collective_hack.svg` |
| `blind_arbiter/results/failure_mode_collective_punishment.svg` | result | tracked | keep_reference | `packages/blind_arbiter/results/failure_mode_collective_punishment.svg` |
| `blind_arbiter/results/permanence_survival.svg` | result | tracked | keep_reference | `packages/blind_arbiter/results/permanence_survival.svg` |
| `blind_arbiter/results/raw` | result | tracked | archive_candidate | `packages/blind_arbiter/results/raw` |
| `blind_arbiter/results/raw/results.csv` | result | tracked | keep_reference | `packages/blind_arbiter/results/raw/results.csv` |
| `blind_arbiter/results/raw/results.json` | result | tracked | keep_reference | `packages/blind_arbiter/results/raw/results.json` |
| `blind_arbiter/results/report.md` | result | tracked | keep_reference | `packages/blind_arbiter/results/report.md` |
| `blind_arbiter/results/run_manifest.json` | result | tracked | keep_reference | `packages/blind_arbiter/results/run_manifest.json` |
| `blind_arbiter/results/validation_report.md` | result | tracked | keep_reference | `packages/blind_arbiter/results/validation_report.md` |
| `blind_arbiter/run.py` | code | tracked | keep_reference | `packages/blind_arbiter/run.py` |
| `blind_arbiter/strategic_camouflage` | experiment | tracked | keep_reference | `packages/blind_arbiter/strategic_camouflage` |
| `blind_arbiter/strategic_camouflage/SPEC.md` | experiment | tracked | keep_reference | `packages/blind_arbiter/strategic_camouflage/SPEC.md` |
| `blind_arbiter/strategic_camouflage/results` | result | tracked | keep_reference | `packages/blind_arbiter/strategic_camouflage/results` |
| `blind_arbiter/strategic_camouflage/results/concealment_surface_strong_gamma.svg` | result | tracked | keep_reference | `packages/blind_arbiter/strategic_camouflage/results/concealment_surface_strong_gamma.svg` |
| `blind_arbiter/strategic_camouflage/results/gamma_audit_off.svg` | result | tracked | keep_reference | `packages/blind_arbiter/strategic_camouflage/results/gamma_audit_off.svg` |
| `blind_arbiter/strategic_camouflage/results/permanence_surface_strong_gamma.svg` | result | tracked | keep_reference | `packages/blind_arbiter/strategic_camouflage/results/permanence_surface_strong_gamma.svg` |
| `blind_arbiter/strategic_camouflage/results/raw` | result | tracked | archive_candidate | `packages/blind_arbiter/strategic_camouflage/results/raw` |
| `blind_arbiter/strategic_camouflage/results/report.md` | result | tracked | keep_reference | `packages/blind_arbiter/strategic_camouflage/results/report.md` |
| `blind_arbiter/strategic_camouflage/results/run_manifest.json` | result | tracked | keep_reference | `packages/blind_arbiter/strategic_camouflage/results/run_manifest.json` |
| `blind_arbiter/strategic_camouflage/results/validation_report.md` | result | tracked | keep_reference | `packages/blind_arbiter/strategic_camouflage/results/validation_report.md` |
| `blind_arbiter/strategic_camouflage/run.py` | code | tracked | keep_reference | `packages/blind_arbiter/strategic_camouflage/run.py` |

### experiments_01_08

| path | type | git state | keep | destination |
|---|---|---|---|---|
| `experiments/01_goodhart_bench` | experiment | tracked+ignored | keep_reference | `experiments/01_goodhart_bench` |
| `experiments/01_goodhart_bench/README.md` | memo | tracked | keep_reference | `experiments/01_goodhart_bench/README.md` |
| `experiments/01_goodhart_bench/SPEC.md` | experiment | tracked | keep_reference | `experiments/01_goodhart_bench/SPEC.md` |
| `experiments/01_goodhart_bench/__pycache__` | archive | ignored | delete_candidate | `no destination; remove from working tree after approval or keep ignored locally` |
| `experiments/01_goodhart_bench/results` | result | tracked | keep_reference | `experiments/01_goodhart_bench/results` |
| `experiments/01_goodhart_bench/results/raw` | result | tracked | archive_candidate | `experiments/01_goodhart_bench/results/raw` |
| `experiments/01_goodhart_bench/results/report.md` | result | tracked | keep_reference | `experiments/01_goodhart_bench/results/report.md` |
| `experiments/01_goodhart_bench/results/run_manifest.json` | result | tracked | keep_reference | `experiments/01_goodhart_bench/results/run_manifest.json` |
| `experiments/01_goodhart_bench/results/true_reward_vs_pressure.svg` | result | tracked | keep_reference | `experiments/01_goodhart_bench/results/true_reward_vs_pressure.svg` |
| `experiments/01_goodhart_bench/results/validation_report.md` | result | tracked | keep_reference | `experiments/01_goodhart_bench/results/validation_report.md` |
| `experiments/01_goodhart_bench/run.py` | code | tracked | keep_reference | `experiments/01_goodhart_bench/run.py` |
| `experiments/02_hedger_vs_incomplete` | experiment | tracked+ignored | keep_reference | `experiments/02_hedger_vs_incomplete` |
| `experiments/02_hedger_vs_incomplete/README.md` | memo | tracked | keep_reference | `experiments/02_hedger_vs_incomplete/README.md` |
| `experiments/02_hedger_vs_incomplete/SPEC.md` | experiment | tracked | keep_reference | `experiments/02_hedger_vs_incomplete/SPEC.md` |
| `experiments/02_hedger_vs_incomplete/__pycache__` | archive | ignored | delete_candidate | `no destination; remove from working tree after approval or keep ignored locally` |
| `experiments/02_hedger_vs_incomplete/results` | result | tracked | keep_reference | `experiments/02_hedger_vs_incomplete/results` |
| `experiments/02_hedger_vs_incomplete/results/raw` | result | tracked | archive_candidate | `experiments/02_hedger_vs_incomplete/results/raw` |
| `experiments/02_hedger_vs_incomplete/results/report.md` | result | tracked | keep_reference | `experiments/02_hedger_vs_incomplete/results/report.md` |
| `experiments/02_hedger_vs_incomplete/results/run_manifest.json` | result | tracked | keep_reference | `experiments/02_hedger_vs_incomplete/results/run_manifest.json` |
| `experiments/02_hedger_vs_incomplete/results/survival_by_environment.svg` | result | tracked | keep_reference | `experiments/02_hedger_vs_incomplete/results/survival_by_environment.svg` |
| `experiments/02_hedger_vs_incomplete/results/validation_report.md` | result | tracked | keep_reference | `experiments/02_hedger_vs_incomplete/results/validation_report.md` |
| `experiments/02_hedger_vs_incomplete/run.py` | code | tracked | keep_reference | `experiments/02_hedger_vs_incomplete/run.py` |
| `experiments/03_silence_vs_fabrication` | experiment | tracked+ignored | keep_reference | `experiments/03_silence_vs_fabrication` |
| `experiments/03_silence_vs_fabrication/README.md` | memo | tracked | keep_reference | `experiments/03_silence_vs_fabrication/README.md` |
| `experiments/03_silence_vs_fabrication/SPEC.md` | experiment | tracked | keep_reference | `experiments/03_silence_vs_fabrication/SPEC.md` |
| `experiments/03_silence_vs_fabrication/__pycache__` | archive | ignored | delete_candidate | `no destination; remove from working tree after approval or keep ignored locally` |
| `experiments/03_silence_vs_fabrication/results` | result | tracked | keep_reference | `experiments/03_silence_vs_fabrication/results` |
| `experiments/03_silence_vs_fabrication/results/fabrication_rates.svg` | result | tracked | keep_reference | `experiments/03_silence_vs_fabrication/results/fabrication_rates.svg` |
| `experiments/03_silence_vs_fabrication/results/model_selection/selection_report.md` | result | tracked | keep_reference | `experiments/03_silence_vs_fabrication/results/model_selection/selection_report.md` |
| `experiments/03_silence_vs_fabrication/results/model_selection/selection_rows.csv` | result | tracked | keep_reference | `experiments/03_silence_vs_fabrication/results/model_selection/selection_rows.csv` |
| `experiments/03_silence_vs_fabrication/results/model_selection/selection_summary.csv` | result | tracked | keep_reference | `experiments/03_silence_vs_fabrication/results/model_selection/selection_summary.csv` |
| `experiments/03_silence_vs_fabrication/results/model_selection/selection_summary.json` | result | tracked | keep_reference | `experiments/03_silence_vs_fabrication/results/model_selection/selection_summary.json` |
| `experiments/03_silence_vs_fabrication/results/raw` | result | tracked | archive_candidate | `experiments/03_silence_vs_fabrication/results/raw` |
| `experiments/03_silence_vs_fabrication/results/report.md` | result | tracked | keep_reference | `experiments/03_silence_vs_fabrication/results/report.md` |
| `experiments/03_silence_vs_fabrication/results/run_manifest.json` | result | tracked | keep_reference | `experiments/03_silence_vs_fabrication/results/run_manifest.json` |
| `experiments/03_silence_vs_fabrication/results/validation_report.md` | result | tracked | keep_reference | `experiments/03_silence_vs_fabrication/results/validation_report.md` |
| `experiments/03_silence_vs_fabrication/run.py` | code | tracked | keep_reference | `experiments/03_silence_vs_fabrication/run.py` |
| `experiments/03_silence_vs_fabrication/tools` | code | tracked+ignored | keep_reference | `experiments/03_silence_vs_fabrication/tools` |
| `experiments/03_silence_vs_fabrication/tools/__pycache__` | archive | ignored | delete_candidate | `no destination; remove from working tree after approval or keep ignored locally` |
| `experiments/03_silence_vs_fabrication/tools/llama_server_backend.py` | code | tracked | keep_reference | `experiments/03_silence_vs_fabrication/tools/llama_server_backend.py` |
| `experiments/03_silence_vs_fabrication/tools/reclassify_existing.py` | code | tracked | keep_reference | `experiments/03_silence_vs_fabrication/tools/reclassify_existing.py` |
| `experiments/03_silence_vs_fabrication/tools/select_llama_model.py` | code | tracked | keep_reference | `experiments/03_silence_vs_fabrication/tools/select_llama_model.py` |
| `experiments/04_admissible_set_core` | experiment | tracked+ignored | keep_reference | `experiments/04_admissible_set_core` |
| `experiments/04_admissible_set_core/README.md` | memo | tracked | keep_reference | `experiments/04_admissible_set_core/README.md` |
| `experiments/04_admissible_set_core/SPEC.md` | experiment | tracked | keep_reference | `experiments/04_admissible_set_core/SPEC.md` |
| `experiments/04_admissible_set_core/__pycache__` | archive | ignored | delete_candidate | `no destination; remove from working tree after approval or keep ignored locally` |
| `experiments/04_admissible_set_core/results` | result | tracked | keep_reference | `experiments/04_admissible_set_core/results` |
| `experiments/04_admissible_set_core/results/admissible_set_size.svg` | result | tracked | keep_reference | `experiments/04_admissible_set_core/results/admissible_set_size.svg` |
| `experiments/04_admissible_set_core/results/raw` | result | tracked | archive_candidate | `experiments/04_admissible_set_core/results/raw` |
| `experiments/04_admissible_set_core/results/report.md` | result | tracked | keep_reference | `experiments/04_admissible_set_core/results/report.md` |
| `experiments/04_admissible_set_core/results/run_manifest.json` | result | tracked | keep_reference | `experiments/04_admissible_set_core/results/run_manifest.json` |
| `experiments/04_admissible_set_core/results/validation_report.md` | result | tracked | keep_reference | `experiments/04_admissible_set_core/results/validation_report.md` |
| `experiments/04_admissible_set_core/run.py` | code | tracked | keep_reference | `experiments/04_admissible_set_core/run.py` |
| `experiments/05_reflective_stability_of_incompleteness` | experiment | tracked+ignored | keep_reference | `experiments/05_reflective_stability_of_incompleteness` |
| `experiments/05_reflective_stability_of_incompleteness/README.md` | memo | tracked | keep_reference | `experiments/05_reflective_stability_of_incompleteness/README.md` |
| `experiments/05_reflective_stability_of_incompleteness/SPEC.md` | experiment | tracked | keep_reference | `experiments/05_reflective_stability_of_incompleteness/SPEC.md` |
| `experiments/05_reflective_stability_of_incompleteness/__pycache__` | archive | ignored | delete_candidate | `no destination; remove from working tree after approval or keep ignored locally` |
| `experiments/05_reflective_stability_of_incompleteness/results` | result | tracked | keep_reference | `experiments/05_reflective_stability_of_incompleteness/results` |
| `experiments/05_reflective_stability_of_incompleteness/results/partial_stability_heatmap.svg` | result | tracked | keep_reference | `experiments/05_reflective_stability_of_incompleteness/results/partial_stability_heatmap.svg` |
| `experiments/05_reflective_stability_of_incompleteness/results/raw` | result | tracked | archive_candidate | `experiments/05_reflective_stability_of_incompleteness/results/raw` |
| `experiments/05_reflective_stability_of_incompleteness/results/report.md` | result | tracked | keep_reference | `experiments/05_reflective_stability_of_incompleteness/results/report.md` |
| `experiments/05_reflective_stability_of_incompleteness/results/run_manifest.json` | result | tracked | keep_reference | `experiments/05_reflective_stability_of_incompleteness/results/run_manifest.json` |
| `experiments/05_reflective_stability_of_incompleteness/results/validation_report.md` | result | tracked | keep_reference | `experiments/05_reflective_stability_of_incompleteness/results/validation_report.md` |
| `experiments/05_reflective_stability_of_incompleteness/run.py` | code | tracked | keep_reference | `experiments/05_reflective_stability_of_incompleteness/run.py` |
| `experiments/06_sugarscape_governor` | experiment | tracked+ignored | keep_reference | `experiments/06_sugarscape_governor` |
| `experiments/06_sugarscape_governor/README.md` | memo | tracked | keep_reference | `experiments/06_sugarscape_governor/README.md` |
| `experiments/06_sugarscape_governor/SPEC.md` | experiment | tracked | keep_reference | `experiments/06_sugarscape_governor/SPEC.md` |
| `experiments/06_sugarscape_governor/__pycache__` | archive | ignored | delete_candidate | `no destination; remove from working tree after approval or keep ignored locally` |
| `experiments/06_sugarscape_governor/results` | result | tracked | keep_reference | `experiments/06_sugarscape_governor/results` |
| `experiments/06_sugarscape_governor/results/population_survival.svg` | result | tracked | keep_reference | `experiments/06_sugarscape_governor/results/population_survival.svg` |
| `experiments/06_sugarscape_governor/results/raw` | result | tracked | archive_candidate | `experiments/06_sugarscape_governor/results/raw` |
| `experiments/06_sugarscape_governor/results/report.md` | result | tracked | keep_reference | `experiments/06_sugarscape_governor/results/report.md` |
| `experiments/06_sugarscape_governor/results/run_manifest.json` | result | tracked | keep_reference | `experiments/06_sugarscape_governor/results/run_manifest.json` |
| `experiments/06_sugarscape_governor/results/validation_report.md` | result | tracked | keep_reference | `experiments/06_sugarscape_governor/results/validation_report.md` |
| `experiments/06_sugarscape_governor/run.py` | code | tracked | keep_reference | `experiments/06_sugarscape_governor/run.py` |
| `experiments/07_empowerment_vs_corrigibility` | experiment | tracked+ignored | keep_reference | `experiments/07_empowerment_vs_corrigibility` |
| `experiments/07_empowerment_vs_corrigibility/CODEX_PROMPT.md` | experiment | tracked | keep_reference | `experiments/07_empowerment_vs_corrigibility/CODEX_PROMPT.md` |
| `experiments/07_empowerment_vs_corrigibility/README.md` | memo | tracked | keep_reference | `experiments/07_empowerment_vs_corrigibility/README.md` |
| `experiments/07_empowerment_vs_corrigibility/SPEC.md` | experiment | tracked | keep_reference | `experiments/07_empowerment_vs_corrigibility/SPEC.md` |
| `experiments/07_empowerment_vs_corrigibility/__pycache__` | archive | ignored | delete_candidate | `no destination; remove from working tree after approval or keep ignored locally` |
| ... | ... | ... | ... | 75 more rows in CSV |

### experiments_13_18

| path | type | git state | keep | destination |
|---|---|---|---|---|
| `experiments/13_evolvable_action_strategies` | experiment | tracked | keep_reference | `experiments/13_evolvable_action_strategies` |
| `experiments/13_evolvable_action_strategies/SPEC_EXP16.md` | experiment | tracked | keep_reference | `experiments/13_evolvable_action_strategies/SPEC_EXP16.md` |
| `experiments/13_evolvable_action_strategies/SPEC_EXP16_1_PATCH.md` | experiment | tracked | keep_reference | `experiments/13_evolvable_action_strategies/SPEC_EXP16_1_PATCH.md` |
| `experiments/13_evolvable_action_strategies/SPEC_IMPLEMENTED.md` | experiment | tracked | keep_reference | `experiments/13_evolvable_action_strategies/SPEC_IMPLEMENTED.md` |
| `experiments/13_evolvable_action_strategies/SPEC_IMPLEMENTED_14.md` | experiment | tracked | keep_reference | `experiments/13_evolvable_action_strategies/SPEC_IMPLEMENTED_14.md` |
| `experiments/13_evolvable_action_strategies/SPEC_IMPLEMENTED_15.md` | experiment | tracked | keep_reference | `experiments/13_evolvable_action_strategies/SPEC_IMPLEMENTED_15.md` |
| `experiments/13_evolvable_action_strategies/results` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results` |
| `experiments/13_evolvable_action_strategies/results/audit_delta_exploit_mass.svg` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results/audit_delta_exploit_mass.svg` |
| `experiments/13_evolvable_action_strategies/results/raw` | result | tracked | archive_candidate | `experiments/13_evolvable_action_strategies/results/raw` |
| `experiments/13_evolvable_action_strategies/results/report.md` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results/report.md` |
| `experiments/13_evolvable_action_strategies/results/run_manifest.json` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results/run_manifest.json` |
| `experiments/13_evolvable_action_strategies/results/validation_report.md` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results/validation_report.md` |
| `experiments/13_evolvable_action_strategies/results/w2_capture_by_policy.svg` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results/w2_capture_by_policy.svg` |
| `experiments/13_evolvable_action_strategies/results/w2_exploit_mass_by_policy.svg` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results/w2_exploit_mass_by_policy.svg` |
| `experiments/13_evolvable_action_strategies/results_14` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results_14` |
| `experiments/13_evolvable_action_strategies/results_14/perturbation_pass_rate.svg` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results_14/perturbation_pass_rate.svg` |
| `experiments/13_evolvable_action_strategies/results_14/raw` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results_14/raw` |
| `experiments/13_evolvable_action_strategies/results_14/report.md` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results_14/report.md` |
| `experiments/13_evolvable_action_strategies/results_14/run_manifest.json` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results_14/run_manifest.json` |
| `experiments/13_evolvable_action_strategies/results_14/seed_permanence_ci_lower.svg` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results_14/seed_permanence_ci_lower.svg` |
| `experiments/13_evolvable_action_strategies/results_14/validation_report.md` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results_14/validation_report.md` |
| `experiments/13_evolvable_action_strategies/results_14/w6_action_ablation_permanence.svg` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results_14/w6_action_ablation_permanence.svg` |
| `experiments/13_evolvable_action_strategies/results_15` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results_15` |
| `experiments/13_evolvable_action_strategies/results_15/best_permanence_by_family.svg` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results_15/best_permanence_by_family.svg` |
| `experiments/13_evolvable_action_strategies/results_15/classification_best_capture.svg` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results_15/classification_best_capture.svg` |
| `experiments/13_evolvable_action_strategies/results_15/part_a_best_permanence.svg` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results_15/part_a_best_permanence.svg` |
| `experiments/13_evolvable_action_strategies/results_15/raw` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results_15/raw` |
| `experiments/13_evolvable_action_strategies/results_15/report.md` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results_15/report.md` |
| `experiments/13_evolvable_action_strategies/results_15/run_manifest.json` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results_15/run_manifest.json` |
| `experiments/13_evolvable_action_strategies/results_15/validation_report.md` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results_15/validation_report.md` |
| `experiments/13_evolvable_action_strategies/results_16` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results_16` |
| `experiments/13_evolvable_action_strategies/results_16/W3_catastrophe_ambiguity_action_channel_cost_scale_permanence.svg` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results_16/W3_catastrophe_ambiguity_action_channel_cost_scale_permanence.svg` |
| `experiments/13_evolvable_action_strategies/results_16/W3_catastrophe_ambiguity_adversarial_gaps.svg` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results_16/W3_catastrophe_ambiguity_adversarial_gaps.svg` |
| `experiments/13_evolvable_action_strategies/results_16/W3_catastrophe_ambiguity_adversarial_pressure_permanence.svg` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results_16/W3_catastrophe_ambiguity_adversarial_pressure_permanence.svg` |
| `experiments/13_evolvable_action_strategies/results_16/W3_catastrophe_ambiguity_mutation_rate_permanence.svg` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results_16/W3_catastrophe_ambiguity_mutation_rate_permanence.svg` |
| `experiments/13_evolvable_action_strategies/results_16/W4_scavenger_catastrophe_action_channel_cost_scale_permanence.svg` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results_16/W4_scavenger_catastrophe_action_channel_cost_scale_permanence.svg` |
| `experiments/13_evolvable_action_strategies/results_16/W4_scavenger_catastrophe_adversarial_gaps.svg` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results_16/W4_scavenger_catastrophe_adversarial_gaps.svg` |
| `experiments/13_evolvable_action_strategies/results_16/W4_scavenger_catastrophe_adversarial_pressure_permanence.svg` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results_16/W4_scavenger_catastrophe_adversarial_pressure_permanence.svg` |
| `experiments/13_evolvable_action_strategies/results_16/W4_scavenger_catastrophe_mutation_rate_permanence.svg` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results_16/W4_scavenger_catastrophe_mutation_rate_permanence.svg` |
| `experiments/13_evolvable_action_strategies/results_16/W6_mutation_corridor_action_channel_cost_scale_permanence.svg` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results_16/W6_mutation_corridor_action_channel_cost_scale_permanence.svg` |
| `experiments/13_evolvable_action_strategies/results_16/W6_mutation_corridor_adversarial_gaps.svg` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results_16/W6_mutation_corridor_adversarial_gaps.svg` |
| `experiments/13_evolvable_action_strategies/results_16/W6_mutation_corridor_adversarial_pressure_permanence.svg` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results_16/W6_mutation_corridor_adversarial_pressure_permanence.svg` |
| `experiments/13_evolvable_action_strategies/results_16/W6_mutation_corridor_mutation_rate_permanence.svg` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results_16/W6_mutation_corridor_mutation_rate_permanence.svg` |
| `experiments/13_evolvable_action_strategies/results_16/boundary_atlas.md` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results_16/boundary_atlas.md` |
| `experiments/13_evolvable_action_strategies/results_16/boundary_summary.svg` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results_16/boundary_summary.svg` |
| `experiments/13_evolvable_action_strategies/results_16/raw` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results_16/raw` |
| `experiments/13_evolvable_action_strategies/results_16/run_manifest.json` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results_16/run_manifest.json` |
| `experiments/13_evolvable_action_strategies/results_16/sensitivity_report.md` | result | tracked | keep_reference | `experiments/13_evolvable_action_strategies/results_16/sensitivity_report.md` |
| `experiments/13_evolvable_action_strategies/run.py` | code | tracked | keep_reference | `experiments/13_evolvable_action_strategies/run.py` |
| `experiments/13_evolvable_action_strategies/run14.py` | code | tracked | keep_reference | `experiments/13_evolvable_action_strategies/run14.py` |
| `experiments/13_evolvable_action_strategies/run15.py` | code | tracked | keep_reference | `experiments/13_evolvable_action_strategies/run15.py` |
| `experiments/13_evolvable_action_strategies/run16.py` | code | tracked | keep_reference | `experiments/13_evolvable_action_strategies/run16.py` |
| `experiments/14_dsl_core` | experiment | untracked+ignored | keep_reference | `experiments/14_dsl_core` |
| `experiments/14_dsl_core/.pytest_cache` | archive | ignored | delete_candidate | `no destination; remove from working tree after approval or keep ignored locally` |
| `experiments/14_dsl_core/EXPERIMENTS.md` | memo | untracked | keep_reference | `experiments/14_dsl_core/EXPERIMENTS.md` |
| `experiments/14_dsl_core/SPEC-v0.4.md` | experiment | untracked | keep_reference | `experiments/14_dsl_core/SPEC-v0.4.md` |
| `experiments/14_dsl_core/SPEC-v0.42.md` | experiment | untracked | keep_reference | `experiments/14_dsl_core/SPEC-v0.42.md` |
| `experiments/14_dsl_core/venv` | archive | untracked+ignored | delete_candidate | `no destination; remove from working tree after approval or keep ignored locally` |
| `experiments/14_dsl_core/worldcore` | experiment | untracked+ignored | keep_reference | `experiments/14_dsl_core/worldcore` |
| `experiments/14_dsl_core/worldcore/.gitignore` | config | untracked | keep_reference | `experiments/14_dsl_core/worldcore/.gitignore` |
| `experiments/14_dsl_core/worldcore/README.md` | memo | untracked | keep_reference | `experiments/14_dsl_core/worldcore/README.md` |
| `experiments/14_dsl_core/worldcore/__init__.py` | code | untracked | keep_reference | `experiments/14_dsl_core/worldcore/__init__.py` |
| `experiments/14_dsl_core/worldcore/outputs/.gitkeep` | result | untracked | keep_reference | `experiments/14_dsl_core/worldcore/outputs/.gitkeep` |
| `experiments/14_dsl_core/worldcore/outputs/capacity_curve.csv` | result | ignored | keep_reference | `experiments/14_dsl_core/worldcore/outputs/capacity_curve.csv` |
| `experiments/14_dsl_core/worldcore/outputs/capacity_curve.png` | result | ignored | keep_reference | `experiments/14_dsl_core/worldcore/outputs/capacity_curve.png` |
| `experiments/14_dsl_core/worldcore/outputs/capacity_diagnostics.png` | result | ignored | keep_reference | `experiments/14_dsl_core/worldcore/outputs/capacity_diagnostics.png` |
| `experiments/14_dsl_core/worldcore/outputs/capacity_summary.json` | result | ignored | keep_reference | `experiments/14_dsl_core/worldcore/outputs/capacity_summary.json` |
| `experiments/14_dsl_core/worldcore/outputs/closure` | result | ignored | keep_reference | `experiments/14_dsl_core/worldcore/outputs/closure` |
| `experiments/14_dsl_core/worldcore/outputs/closure_graph_metrics.csv` | result | ignored | keep_reference | `experiments/14_dsl_core/worldcore/outputs/closure_graph_metrics.csv` |
| `experiments/14_dsl_core/worldcore/outputs/closure_proof_novelty.csv` | result | ignored | keep_reference | `experiments/14_dsl_core/worldcore/outputs/closure_proof_novelty.csv` |
| `experiments/14_dsl_core/worldcore/outputs/closure_statistics.csv` | result | ignored | keep_reference | `experiments/14_dsl_core/worldcore/outputs/closure_statistics.csv` |
| `experiments/14_dsl_core/worldcore/outputs/complexity_distribution.csv` | result | ignored | keep_reference | `experiments/14_dsl_core/worldcore/outputs/complexity_distribution.csv` |
| `experiments/14_dsl_core/worldcore/outputs/correlations.csv` | result | ignored | keep_reference | `experiments/14_dsl_core/worldcore/outputs/correlations.csv` |
| `experiments/14_dsl_core/worldcore/outputs/decision_H2.json` | result | ignored | keep_reference | `experiments/14_dsl_core/worldcore/outputs/decision_H2.json` |
| `experiments/14_dsl_core/worldcore/outputs/decision_gate.json` | result | ignored | keep_reference | `experiments/14_dsl_core/worldcore/outputs/decision_gate.json` |
| `experiments/14_dsl_core/worldcore/outputs/difficulty_audit.csv` | result | ignored | keep_reference | `experiments/14_dsl_core/worldcore/outputs/difficulty_audit.csv` |
| `experiments/14_dsl_core/worldcore/outputs/difficulty_distribution.csv` | result | ignored | keep_reference | `experiments/14_dsl_core/worldcore/outputs/difficulty_distribution.csv` |
| `experiments/14_dsl_core/worldcore/outputs/diversity_explanation.json` | result | ignored | keep_reference | `experiments/14_dsl_core/worldcore/outputs/diversity_explanation.json` |
| `experiments/14_dsl_core/worldcore/outputs/experiment_summary.csv` | result | ignored | keep_reference | `experiments/14_dsl_core/worldcore/outputs/experiment_summary.csv` |
| `experiments/14_dsl_core/worldcore/outputs/extractor_coverage.csv` | result | ignored | keep_reference | `experiments/14_dsl_core/worldcore/outputs/extractor_coverage.csv` |
| ... | ... | ... | ... | 449 more rows in CSV |

### boundary_analysis

| path | type | git state | keep | destination |
|---|---|---|---|---|
| `experiments/BA0_boundary_analysis` | experiment | untracked | keep_active | `experiments/BA/BA0_boundary_analysis` |
| `experiments/BA0_boundary_analysis/transition_semantics_report.md` | review | untracked | keep_active | `experiments/BA/BA0_boundary_analysis/transition_semantics_report.md` |
| `experiments/BA1.E1_monotonicity_breaker_ablation_map` | experiment | untracked | duplicate_candidate | `experiments/BA/BA1.E1_monotonicity_breaker_ablation_map` |
| `experiments/BA1.E1_monotonicity_breaker_ablation_map/BA1.E1_monotonicity_breaker_ablation_map.md` | memo | untracked | duplicate_candidate | `experiments/BA/BA1.E1_monotonicity_breaker_ablation_map/BA1.E1_monotonicity_breaker_ablation_map.md` |
| `experiments/BA1_E1_monotonicity_breakers` | experiment | untracked+ignored | keep_active | `experiments/BA/BA1_E1_monotonicity_breakers` |
| `experiments/BA1_E1_monotonicity_breakers/outputs` | result | untracked | keep_reference | `experiments/BA/BA1_E1_monotonicity_breakers/outputs` |
| `experiments/BA1_E1_monotonicity_breakers/outputs/MB1_summary.json` | result | untracked | keep_reference | `experiments/BA/BA1_E1_monotonicity_breakers/outputs/MB1_summary.json` |
| `experiments/BA1_E1_monotonicity_breakers/outputs/MB2_summary.json` | result | untracked | keep_reference | `experiments/BA/BA1_E1_monotonicity_breakers/outputs/MB2_summary.json` |
| `experiments/BA1_E1_monotonicity_breakers/outputs/MB3_summary.json` | result | untracked | keep_reference | `experiments/BA/BA1_E1_monotonicity_breakers/outputs/MB3_summary.json` |
| `experiments/BA1_E1_monotonicity_breakers/outputs/MB4_summary.json` | result | untracked | keep_reference | `experiments/BA/BA1_E1_monotonicity_breakers/outputs/MB4_summary.json` |
| `experiments/BA1_E1_monotonicity_breakers/outputs/MB5_summary.json` | result | untracked | keep_reference | `experiments/BA/BA1_E1_monotonicity_breakers/outputs/MB5_summary.json` |
| `experiments/BA1_E1_monotonicity_breakers/outputs/ablation_comparison.csv` | result | untracked | keep_reference | `experiments/BA/BA1_E1_monotonicity_breakers/outputs/ablation_comparison.csv` |
| `experiments/BA1_E1_monotonicity_breakers/outputs/baseline_summary.json` | result | untracked | keep_reference | `experiments/BA/BA1_E1_monotonicity_breakers/outputs/baseline_summary.json` |
| `experiments/BA1_E1_monotonicity_breakers/outputs/contribution_index.csv` | result | untracked | keep_reference | `experiments/BA/BA1_E1_monotonicity_breakers/outputs/contribution_index.csv` |
| `experiments/BA1_E1_monotonicity_breakers/outputs/final_decision.json` | result | untracked | keep_reference | `experiments/BA/BA1_E1_monotonicity_breakers/outputs/final_decision.json` |
| `experiments/BA1_E1_monotonicity_breakers/outputs/final_report.md` | result | untracked | keep_reference | `experiments/BA/BA1_E1_monotonicity_breakers/outputs/final_report.md` |
| `experiments/BA1_E1_monotonicity_breakers/outputs/implementation_notes.md` | result | untracked | keep_reference | `experiments/BA/BA1_E1_monotonicity_breakers/outputs/implementation_notes.md` |
| `experiments/BA1_E1_monotonicity_breakers/outputs/interaction_assessment.json` | result | untracked | keep_reference | `experiments/BA/BA1_E1_monotonicity_breakers/outputs/interaction_assessment.json` |
| `experiments/BA1_E1_monotonicity_breakers/outputs/mechanism_revision.md` | result | untracked | keep_reference | `experiments/BA/BA1_E1_monotonicity_breakers/outputs/mechanism_revision.md` |
| `experiments/BA1_E1_monotonicity_breakers/outputs/monotonicity_witnesses.csv` | result | untracked | keep_reference | `experiments/BA/BA1_E1_monotonicity_breakers/outputs/monotonicity_witnesses.csv` |
| `experiments/BA1_E1_monotonicity_breakers/outputs/transition_counterexamples.md` | result | untracked | keep_reference | `experiments/BA/BA1_E1_monotonicity_breakers/outputs/transition_counterexamples.md` |
| `experiments/BA1_E1_monotonicity_breakers/scripts` | code | untracked+ignored | keep_active | `experiments/BA/BA1_E1_monotonicity_breakers/scripts` |
| `experiments/BA1_E1_monotonicity_breakers/scripts/__pycache__` | archive | ignored | delete_candidate | `no destination; remove from working tree after approval or keep ignored locally` |
| `experiments/BA1_E1_monotonicity_breakers/scripts/run_ablation_map.py` | code | untracked | keep_active | `experiments/BA/BA1_E1_monotonicity_breakers/scripts/run_ablation_map.py` |
| `experiments/BA2.E1_Semantic_benefit_vs_structural_cost_map` | experiment | untracked | duplicate_candidate | `experiments/BA/BA2.E1_Semantic_benefit_vs_structural_cost_map` |
| `experiments/BA2.E1_Semantic_benefit_vs_structural_cost_map/BA2.E1_Semantic_benefit_vs_structural_cost_map.md` | memo | untracked | duplicate_candidate | `experiments/BA/BA2.E1_Semantic_benefit_vs_structural_cost_map/BA2.E1_Semantic_benefit_vs_structural_cost_map.md` |
| `experiments/BA2.E1_Semantic_benefit_vs_structural_cost_map/outputs` | result | untracked | duplicate_candidate | `experiments/BA/BA2.E1_Semantic_benefit_vs_structural_cost_map/outputs` |
| `experiments/BA2.E1_Semantic_benefit_vs_structural_cost_map/outputs/benefit_cost_plane.csv` | result | untracked | duplicate_candidate | `experiments/BA/BA2.E1_Semantic_benefit_vs_structural_cost_map/outputs/benefit_cost_plane.csv` |
| `experiments/BA2.E1_Semantic_benefit_vs_structural_cost_map/outputs/counterexamples.md` | result | untracked | duplicate_candidate | `experiments/BA/BA2.E1_Semantic_benefit_vs_structural_cost_map/outputs/counterexamples.md` |
| `experiments/BA2.E1_Semantic_benefit_vs_structural_cost_map/outputs/dominance_graph.csv` | result | untracked | duplicate_candidate | `experiments/BA/BA2.E1_Semantic_benefit_vs_structural_cost_map/outputs/dominance_graph.csv` |
| `experiments/BA2.E1_Semantic_benefit_vs_structural_cost_map/outputs/final_report.md` | result | untracked | duplicate_candidate | `experiments/BA/BA2.E1_Semantic_benefit_vs_structural_cost_map/outputs/final_report.md` |
| `experiments/BA2.E1_Semantic_benefit_vs_structural_cost_map/outputs/hypothesis_assessment.json` | result | untracked | duplicate_candidate | `experiments/BA/BA2.E1_Semantic_benefit_vs_structural_cost_map/outputs/hypothesis_assessment.json` |
| `experiments/BA2.E1_Semantic_benefit_vs_structural_cost_map/outputs/mechanism_rankings.csv` | result | untracked | duplicate_candidate | `experiments/BA/BA2.E1_Semantic_benefit_vs_structural_cost_map/outputs/mechanism_rankings.csv` |
| `experiments/BA2.E1_Semantic_benefit_vs_structural_cost_map/outputs/pareto_frontier.csv` | result | untracked | duplicate_candidate | `experiments/BA/BA2.E1_Semantic_benefit_vs_structural_cost_map/outputs/pareto_frontier.csv` |
| `experiments/BA2.E1_Semantic_benefit_vs_structural_cost_map/outputs/semantic_benefit.csv` | result | untracked | duplicate_candidate | `experiments/BA/BA2.E1_Semantic_benefit_vs_structural_cost_map/outputs/semantic_benefit.csv` |
| `experiments/BA2.E1_Semantic_benefit_vs_structural_cost_map/outputs/structural_cost.csv` | result | untracked | duplicate_candidate | `experiments/BA/BA2.E1_Semantic_benefit_vs_structural_cost_map/outputs/structural_cost.csv` |
| `experiments/BA2.E1_Semantic_benefit_vs_structural_cost_map/outputs/tradeoff_examples.md` | result | untracked | duplicate_candidate | `experiments/BA/BA2.E1_Semantic_benefit_vs_structural_cost_map/outputs/tradeoff_examples.md` |
| `experiments/BA2_E1_semantic_benefit_vs_structural_cost_map` | experiment | untracked+ignored | keep_active | `experiments/BA/BA2_E1_semantic_benefit_vs_structural_cost_map` |
| `experiments/BA2_E1_semantic_benefit_vs_structural_cost_map/outputs` | result | untracked | keep_reference | `experiments/BA/BA2_E1_semantic_benefit_vs_structural_cost_map/outputs` |
| `experiments/BA2_E1_semantic_benefit_vs_structural_cost_map/outputs/benefit_cost_plane.csv` | result | untracked | keep_reference | `experiments/BA/BA2_E1_semantic_benefit_vs_structural_cost_map/outputs/benefit_cost_plane.csv` |
| `experiments/BA2_E1_semantic_benefit_vs_structural_cost_map/outputs/counterexamples.md` | result | untracked | keep_reference | `experiments/BA/BA2_E1_semantic_benefit_vs_structural_cost_map/outputs/counterexamples.md` |
| `experiments/BA2_E1_semantic_benefit_vs_structural_cost_map/outputs/dominance_graph.csv` | result | untracked | keep_reference | `experiments/BA/BA2_E1_semantic_benefit_vs_structural_cost_map/outputs/dominance_graph.csv` |
| `experiments/BA2_E1_semantic_benefit_vs_structural_cost_map/outputs/final_report.md` | result | untracked | keep_reference | `experiments/BA/BA2_E1_semantic_benefit_vs_structural_cost_map/outputs/final_report.md` |
| `experiments/BA2_E1_semantic_benefit_vs_structural_cost_map/outputs/hypothesis_assessment.json` | result | untracked | keep_reference | `experiments/BA/BA2_E1_semantic_benefit_vs_structural_cost_map/outputs/hypothesis_assessment.json` |
| `experiments/BA2_E1_semantic_benefit_vs_structural_cost_map/outputs/mechanism_rankings.csv` | result | untracked | keep_reference | `experiments/BA/BA2_E1_semantic_benefit_vs_structural_cost_map/outputs/mechanism_rankings.csv` |
| `experiments/BA2_E1_semantic_benefit_vs_structural_cost_map/outputs/pareto_frontier.csv` | result | untracked | keep_reference | `experiments/BA/BA2_E1_semantic_benefit_vs_structural_cost_map/outputs/pareto_frontier.csv` |
| `experiments/BA2_E1_semantic_benefit_vs_structural_cost_map/outputs/semantic_benefit.csv` | result | untracked | keep_reference | `experiments/BA/BA2_E1_semantic_benefit_vs_structural_cost_map/outputs/semantic_benefit.csv` |
| `experiments/BA2_E1_semantic_benefit_vs_structural_cost_map/outputs/structural_cost.csv` | result | untracked | keep_reference | `experiments/BA/BA2_E1_semantic_benefit_vs_structural_cost_map/outputs/structural_cost.csv` |
| `experiments/BA2_E1_semantic_benefit_vs_structural_cost_map/outputs/tradeoff_examples.md` | result | untracked | keep_reference | `experiments/BA/BA2_E1_semantic_benefit_vs_structural_cost_map/outputs/tradeoff_examples.md` |
| `experiments/BA2_E1_semantic_benefit_vs_structural_cost_map/scripts` | code | untracked+ignored | keep_active | `experiments/BA/BA2_E1_semantic_benefit_vs_structural_cost_map/scripts` |
| `experiments/BA2_E1_semantic_benefit_vs_structural_cost_map/scripts/__pycache__` | archive | ignored | delete_candidate | `no destination; remove from working tree after approval or keep ignored locally` |
| `experiments/BA2_E1_semantic_benefit_vs_structural_cost_map/scripts/run_benefit_cost_map.py` | code | untracked | keep_active | `experiments/BA/BA2_E1_semantic_benefit_vs_structural_cost_map/scripts/run_benefit_cost_map.py` |
| `experiments/BA3.E1_MB5_Surrogate_Replacement_Test` | experiment | untracked | duplicate_candidate | `experiments/BA/BA3.E1_MB5_Surrogate_Replacement_Test` |
| `experiments/BA3.E1_MB5_Surrogate_Replacement_Test/BA3.E1_MB5_Surrogate_Replacement_Test.md` | memo | untracked | duplicate_candidate | `experiments/BA/BA3.E1_MB5_Surrogate_Replacement_Test/BA3.E1_MB5_Surrogate_Replacement_Test.md` |
| `experiments/BA3_E1_MB5_surrogate_replacement_test` | experiment | untracked+ignored | keep_active | `experiments/BA/BA3_E1_MB5_surrogate_replacement_test` |
| `experiments/BA3_E1_MB5_surrogate_replacement_test/outputs` | result | untracked | keep_reference | `experiments/BA/BA3_E1_MB5_surrogate_replacement_test/outputs` |
| `experiments/BA3_E1_MB5_surrogate_replacement_test/outputs/MB5_removal_summary.json` | result | untracked | keep_reference | `experiments/BA/BA3_E1_MB5_surrogate_replacement_test/outputs/MB5_removal_summary.json` |
| `experiments/BA3_E1_MB5_surrogate_replacement_test/outputs/S1_absolute_deficit_summary.json` | result | untracked | keep_reference | `experiments/BA/BA3_E1_MB5_surrogate_replacement_test/outputs/S1_absolute_deficit_summary.json` |
| `experiments/BA3_E1_MB5_surrogate_replacement_test/outputs/S2_threshold_boolean_summary.json` | result | untracked | keep_reference | `experiments/BA/BA3_E1_MB5_surrogate_replacement_test/outputs/S2_threshold_boolean_summary.json` |
| `experiments/BA3_E1_MB5_surrogate_replacement_test/outputs/S3_conservative_upper_bound_summary.json` | result | untracked | keep_reference | `experiments/BA/BA3_E1_MB5_surrogate_replacement_test/outputs/S3_conservative_upper_bound_summary.json` |
| `experiments/BA3_E1_MB5_surrogate_replacement_test/outputs/S4a_policy_visible_concentration_summary.json` | result | untracked | keep_reference | `experiments/BA/BA3_E1_MB5_surrogate_replacement_test/outputs/S4a_policy_visible_concentration_summary.json` |
| `experiments/BA3_E1_MB5_surrogate_replacement_test/outputs/S4b_reporting_ratios_summary.json` | result | untracked | keep_reference | `experiments/BA/BA3_E1_MB5_surrogate_replacement_test/outputs/S4b_reporting_ratios_summary.json` |
| `experiments/BA3_E1_MB5_surrogate_replacement_test/outputs/S4c_projection_resource_hhi_summary.json` | result | untracked | keep_reference | `experiments/BA/BA3_E1_MB5_surrogate_replacement_test/outputs/S4c_projection_resource_hhi_summary.json` |
| `experiments/BA3_E1_MB5_surrogate_replacement_test/outputs/S4d_capture_components_summary.json` | result | untracked | keep_reference | `experiments/BA/BA3_E1_MB5_surrogate_replacement_test/outputs/S4d_capture_components_summary.json` |
| `experiments/BA3_E1_MB5_surrogate_replacement_test/outputs/baseline_summary.json` | result | untracked | keep_reference | `experiments/BA/BA3_E1_MB5_surrogate_replacement_test/outputs/baseline_summary.json` |
| `experiments/BA3_E1_MB5_surrogate_replacement_test/outputs/benefit_cost_surrogate_plane.csv` | result | untracked | keep_reference | `experiments/BA/BA3_E1_MB5_surrogate_replacement_test/outputs/benefit_cost_surrogate_plane.csv` |
| `experiments/BA3_E1_MB5_surrogate_replacement_test/outputs/counterexamples.md` | result | untracked | keep_reference | `experiments/BA/BA3_E1_MB5_surrogate_replacement_test/outputs/counterexamples.md` |
| `experiments/BA3_E1_MB5_surrogate_replacement_test/outputs/dominance_graph.csv` | result | untracked | keep_reference | `experiments/BA/BA3_E1_MB5_surrogate_replacement_test/outputs/dominance_graph.csv` |
| `experiments/BA3_E1_MB5_surrogate_replacement_test/outputs/final_report.md` | result | untracked | keep_reference | `experiments/BA/BA3_E1_MB5_surrogate_replacement_test/outputs/final_report.md` |
| `experiments/BA3_E1_MB5_surrogate_replacement_test/outputs/hypothesis_assessment.json` | result | untracked | keep_reference | `experiments/BA/BA3_E1_MB5_surrogate_replacement_test/outputs/hypothesis_assessment.json` |
| `experiments/BA3_E1_MB5_surrogate_replacement_test/outputs/implementation_notes.md` | result | untracked | keep_reference | `experiments/BA/BA3_E1_MB5_surrogate_replacement_test/outputs/implementation_notes.md` |
| `experiments/BA3_E1_MB5_surrogate_replacement_test/outputs/mechanism_split_assessment.md` | result | untracked | keep_reference | `experiments/BA/BA3_E1_MB5_surrogate_replacement_test/outputs/mechanism_split_assessment.md` |
| `experiments/BA3_E1_MB5_surrogate_replacement_test/outputs/monotonicity_witnesses.csv` | result | untracked | keep_reference | `experiments/BA/BA3_E1_MB5_surrogate_replacement_test/outputs/monotonicity_witnesses.csv` |
| `experiments/BA3_E1_MB5_surrogate_replacement_test/outputs/pareto_frontier.csv` | result | untracked | keep_reference | `experiments/BA/BA3_E1_MB5_surrogate_replacement_test/outputs/pareto_frontier.csv` |
| `experiments/BA3_E1_MB5_surrogate_replacement_test/outputs/semantic_validity.csv` | result | untracked | keep_reference | `experiments/BA/BA3_E1_MB5_surrogate_replacement_test/outputs/semantic_validity.csv` |
| `experiments/BA3_E1_MB5_surrogate_replacement_test/outputs/surrogate_comparison.csv` | result | untracked | keep_reference | `experiments/BA/BA3_E1_MB5_surrogate_replacement_test/outputs/surrogate_comparison.csv` |
| `experiments/BA3_E1_MB5_surrogate_replacement_test/scripts` | code | untracked+ignored | keep_active | `experiments/BA/BA3_E1_MB5_surrogate_replacement_test/scripts` |
| `experiments/BA3_E1_MB5_surrogate_replacement_test/scripts/__pycache__` | archive | ignored | delete_candidate | `no destination; remove from working tree after approval or keep ignored locally` |
| `experiments/BA3_E1_MB5_surrogate_replacement_test/scripts/run_mb5_surrogates.py` | code | untracked | keep_active | `experiments/BA/BA3_E1_MB5_surrogate_replacement_test/scripts/run_mb5_surrogates.py` |
| `experiments/BA4.0_Layered_Abstraction_Discipline` | experiment | untracked | duplicate_candidate | `experiments/BA/BA4.0_Layered_Abstraction_Discipline` |
| ... | ... | ... | ... | 5 more rows in CSV |

### faithful_abstraction

| path | type | git state | keep | destination |
|---|---|---|---|---|
| `experiments/BRIDGE_MAP_18_1_TO_FA2.md` | memo | untracked | keep_reference | `research/faithful_abstraction_v1/BRIDGE_MAP_18_1_TO_FA2.md` |
| `experiments/FA1.E1_False-Safe_Witness_Taxonomy` | experiment | untracked | duplicate_candidate | `experiments/FA/FA1.E1_False-Safe_Witness_Taxonomy` |
| `experiments/FA1.E1_False-Safe_Witness_Taxonomy/FA1.E1_False-Safe_Witness_Taxonomy.md` | memo | untracked | duplicate_candidate | `experiments/FA/FA1.E1_False-Safe_Witness_Taxonomy/FA1.E1_False-Safe_Witness_Taxonomy.md` |
| `experiments/FA1_E1_false_safe_witness_taxonomy` | experiment | untracked+ignored | keep_active | `experiments/FA/FA1_E1_false_safe_witness_taxonomy` |
| `experiments/FA1_E1_false_safe_witness_taxonomy/outputs` | result | untracked | keep_reference | `experiments/FA/FA1_E1_false_safe_witness_taxonomy/outputs` |
| `experiments/FA1_E1_false_safe_witness_taxonomy/outputs/ambiguous_witnesses.md` | result | untracked | keep_reference | `experiments/FA/FA1_E1_false_safe_witness_taxonomy/outputs/ambiguous_witnesses.md` |
| `experiments/FA1_E1_false_safe_witness_taxonomy/outputs/final_report.md` | result | untracked | keep_reference | `experiments/FA/FA1_E1_false_safe_witness_taxonomy/outputs/final_report.md` |
| `experiments/FA1_E1_false_safe_witness_taxonomy/outputs/hypothesis_assessment.json` | result | untracked | keep_reference | `experiments/FA/FA1_E1_false_safe_witness_taxonomy/outputs/hypothesis_assessment.json` |
| `experiments/FA1_E1_false_safe_witness_taxonomy/outputs/implementation_notes.md` | result | untracked | keep_reference | `experiments/FA/FA1_E1_false_safe_witness_taxonomy/outputs/implementation_notes.md` |
| `experiments/FA1_E1_false_safe_witness_taxonomy/outputs/layer_eligibility_summary.csv` | result | untracked | keep_reference | `experiments/FA/FA1_E1_false_safe_witness_taxonomy/outputs/layer_eligibility_summary.csv` |
| `experiments/FA1_E1_false_safe_witness_taxonomy/outputs/minimal_information_candidates.csv` | result | untracked | keep_reference | `experiments/FA/FA1_E1_false_safe_witness_taxonomy/outputs/minimal_information_candidates.csv` |
| `experiments/FA1_E1_false_safe_witness_taxonomy/outputs/representative_witnesses.md` | result | untracked | keep_reference | `experiments/FA/FA1_E1_false_safe_witness_taxonomy/outputs/representative_witnesses.md` |
| `experiments/FA1_E1_false_safe_witness_taxonomy/outputs/witness_class_summary.json` | result | untracked | keep_reference | `experiments/FA/FA1_E1_false_safe_witness_taxonomy/outputs/witness_class_summary.json` |
| `experiments/FA1_E1_false_safe_witness_taxonomy/outputs/witness_taxonomy.csv` | result | untracked | keep_reference | `experiments/FA/FA1_E1_false_safe_witness_taxonomy/outputs/witness_taxonomy.csv` |
| `experiments/FA1_E1_false_safe_witness_taxonomy/scripts` | code | untracked+ignored | keep_active | `experiments/FA/FA1_E1_false_safe_witness_taxonomy/scripts` |
| `experiments/FA1_E1_false_safe_witness_taxonomy/scripts/__pycache__` | archive | ignored | delete_candidate | `no destination; remove from working tree after approval or keep ignored locally` |
| `experiments/FA1_E1_false_safe_witness_taxonomy/scripts/run_false_safe_taxonomy.py` | code | untracked | keep_active | `experiments/FA/FA1_E1_false_safe_witness_taxonomy/scripts/run_false_safe_taxonomy.py` |
| `experiments/FA2.5.E1_Faithful_Candidate_Validation` | experiment | untracked | duplicate_candidate | `experiments/FA/FA2.5.E1_Faithful_Candidate_Validation` |
| `experiments/FA2.5.E1_Faithful_Candidate_Validation/FA2.5.E1_Faithful_Candidate_Validation.md` | memo | untracked | duplicate_candidate | `experiments/FA/FA2.5.E1_Faithful_Candidate_Validation/FA2.5.E1_Faithful_Candidate_Validation.md` |
| `experiments/FA2.E1_Minimal_Invariant_Compression_Test` | experiment | untracked | duplicate_candidate | `experiments/FA/FA2.E1_Minimal_Invariant_Compression_Test` |
| `experiments/FA2.E1_Minimal_Invariant_Compression_Test/FA2.E1_Minimal_Invariant_Compression_Test.md` | memo | untracked | duplicate_candidate | `experiments/FA/FA2.E1_Minimal_Invariant_Compression_Test/FA2.E1_Minimal_Invariant_Compression_Test.md` |
| `experiments/FA2_5_E1_candidate_validation` | experiment | untracked+ignored | keep_active | `experiments/FA/FA2_5_E1_candidate_validation` |
| `experiments/FA2_5_E1_candidate_validation/outputs` | result | untracked | keep_reference | `experiments/FA/FA2_5_E1_candidate_validation/outputs` |
| `experiments/FA2_5_E1_candidate_validation/outputs/baseline_definitions.md` | result | untracked | keep_reference | `experiments/FA/FA2_5_E1_candidate_validation/outputs/baseline_definitions.md` |
| `experiments/FA2_5_E1_candidate_validation/outputs/candidate_coordinates.csv` | result | untracked | keep_reference | `experiments/FA/FA2_5_E1_candidate_validation/outputs/candidate_coordinates.csv` |
| `experiments/FA2_5_E1_candidate_validation/outputs/candidate_definition.md` | result | untracked | keep_reference | `experiments/FA/FA2_5_E1_candidate_validation/outputs/candidate_definition.md` |
| `experiments/FA2_5_E1_candidate_validation/outputs/candidate_validity.json` | result | untracked | keep_reference | `experiments/FA/FA2_5_E1_candidate_validation/outputs/candidate_validity.json` |
| `experiments/FA2_5_E1_candidate_validation/outputs/candidate_vs_baselines.md` | result | untracked | keep_reference | `experiments/FA/FA2_5_E1_candidate_validation/outputs/candidate_vs_baselines.md` |
| `experiments/FA2_5_E1_candidate_validation/outputs/cegar_equivalence_analysis.md` | result | untracked | keep_reference | `experiments/FA/FA2_5_E1_candidate_validation/outputs/cegar_equivalence_analysis.md` |
| `experiments/FA2_5_E1_candidate_validation/outputs/confusion_matrices.csv` | result | untracked | keep_reference | `experiments/FA/FA2_5_E1_candidate_validation/outputs/confusion_matrices.csv` |
| `experiments/FA2_5_E1_candidate_validation/outputs/dataset_summary.csv` | result | untracked | keep_reference | `experiments/FA/FA2_5_E1_candidate_validation/outputs/dataset_summary.csv` |
| `experiments/FA2_5_E1_candidate_validation/outputs/final_report.md` | result | untracked | keep_reference | `experiments/FA/FA2_5_E1_candidate_validation/outputs/final_report.md` |
| `experiments/FA2_5_E1_candidate_validation/outputs/hypothesis_assessment.json` | result | untracked | keep_reference | `experiments/FA/FA2_5_E1_candidate_validation/outputs/hypothesis_assessment.json` |
| `experiments/FA2_5_E1_candidate_validation/outputs/implementation_notes.md` | result | untracked | keep_reference | `experiments/FA/FA2_5_E1_candidate_validation/outputs/implementation_notes.md` |
| `experiments/FA2_5_E1_candidate_validation/outputs/layer_eligibility_check.md` | result | untracked | keep_reference | `experiments/FA/FA2_5_E1_candidate_validation/outputs/layer_eligibility_check.md` |
| `experiments/FA2_5_E1_candidate_validation/outputs/metrics.csv` | result | untracked | keep_reference | `experiments/FA/FA2_5_E1_candidate_validation/outputs/metrics.csv` |
| `experiments/FA2_5_E1_candidate_validation/outputs/precision_recall_data.csv` | result | untracked | keep_reference | `experiments/FA/FA2_5_E1_candidate_validation/outputs/precision_recall_data.csv` |
| `experiments/FA2_5_E1_candidate_validation/outputs/roc_data.csv` | result | untracked | keep_reference | `experiments/FA/FA2_5_E1_candidate_validation/outputs/roc_data.csv` |
| `experiments/FA2_5_E1_candidate_validation/scripts` | code | untracked+ignored | keep_active | `experiments/FA/FA2_5_E1_candidate_validation/scripts` |
| `experiments/FA2_5_E1_candidate_validation/scripts/__pycache__` | archive | ignored | delete_candidate | `no destination; remove from working tree after approval or keep ignored locally` |
| `experiments/FA2_5_E1_candidate_validation/scripts/run_candidate_validation.py` | code | untracked | keep_active | `experiments/FA/FA2_5_E1_candidate_validation/scripts/run_candidate_validation.py` |
| `experiments/FA2_E1_minimal_invariant_compression_test` | experiment | untracked | keep_active | `experiments/FA/FA2_E1_minimal_invariant_compression_test` |
| `experiments/FA2_E1_minimal_invariant_compression_test/outputs` | result | untracked | keep_reference | `experiments/FA/FA2_E1_minimal_invariant_compression_test/outputs` |
| `experiments/FA2_E1_minimal_invariant_compression_test/outputs/compression_summary.json` | result | untracked | keep_reference | `experiments/FA/FA2_E1_minimal_invariant_compression_test/outputs/compression_summary.json` |
| `experiments/FA2_E1_minimal_invariant_compression_test/outputs/coverage_by_refinement.csv` | result | untracked | keep_reference | `experiments/FA/FA2_E1_minimal_invariant_compression_test/outputs/coverage_by_refinement.csv` |
| `experiments/FA2_E1_minimal_invariant_compression_test/outputs/final_report.md` | result | untracked | keep_reference | `experiments/FA/FA2_E1_minimal_invariant_compression_test/outputs/final_report.md` |
| `experiments/FA2_E1_minimal_invariant_compression_test/outputs/hypothesis_assessment.json` | result | untracked | keep_reference | `experiments/FA/FA2_E1_minimal_invariant_compression_test/outputs/hypothesis_assessment.json` |
| `experiments/FA2_E1_minimal_invariant_compression_test/outputs/implementation_notes.md` | result | untracked | keep_reference | `experiments/FA/FA2_E1_minimal_invariant_compression_test/outputs/implementation_notes.md` |
| `experiments/FA2_E1_minimal_invariant_compression_test/outputs/invariant_catalog.csv` | result | untracked | keep_reference | `experiments/FA/FA2_E1_minimal_invariant_compression_test/outputs/invariant_catalog.csv` |
| `experiments/FA2_E1_minimal_invariant_compression_test/outputs/marginal_coverage.csv` | result | untracked | keep_reference | `experiments/FA/FA2_E1_minimal_invariant_compression_test/outputs/marginal_coverage.csv` |
| `experiments/FA2_E1_minimal_invariant_compression_test/outputs/non_oracle_proxy_analysis.json` | result | untracked | keep_reference | `experiments/FA/FA2_E1_minimal_invariant_compression_test/outputs/non_oracle_proxy_analysis.json` |
| `experiments/FA2_E1_minimal_invariant_compression_test/outputs/refinement_sets.csv` | result | untracked | keep_reference | `experiments/FA/FA2_E1_minimal_invariant_compression_test/outputs/refinement_sets.csv` |
| `experiments/FA2_E1_minimal_invariant_compression_test/outputs/residual_witnesses.csv` | result | untracked | keep_reference | `experiments/FA/FA2_E1_minimal_invariant_compression_test/outputs/residual_witnesses.csv` |
| `experiments/FA2_E1_minimal_invariant_compression_test/outputs/temporal_oracle_analysis.json` | result | untracked | keep_reference | `experiments/FA/FA2_E1_minimal_invariant_compression_test/outputs/temporal_oracle_analysis.json` |
| `experiments/FA2_E1_minimal_invariant_compression_test/outputs/wsts_risk_assessment.md` | result | untracked | keep_reference | `experiments/FA/FA2_E1_minimal_invariant_compression_test/outputs/wsts_risk_assessment.md` |
| `experiments/FA2_E1_minimal_invariant_compression_test/scripts` | code | untracked | keep_active | `experiments/FA/FA2_E1_minimal_invariant_compression_test/scripts` |
| `experiments/FA2_E1_minimal_invariant_compression_test/scripts/run_minimal_invariant_compression.py` | code | untracked | keep_active | `experiments/FA/FA2_E1_minimal_invariant_compression_test/scripts/run_minimal_invariant_compression.py` |
| `experiments/T-C_Monotonicity_of_Faithful_Justitia_Abstraction` | experiment | untracked | keep_active | `experiments/FA/T-C_Monotonicity_of_Faithful_Justitia_Abstraction` |
| `experiments/T-C_Monotonicity_of_Faithful_Justitia_Abstraction/T-C_Monotonicity_of_Faithful_Justitia_Abstraction.md` | memo | untracked | keep_active | `experiments/FA/T-C_Monotonicity_of_Faithful_Justitia_Abstraction/T-C_Monotonicity_of_Faithful_Justitia_Abstraction.md` |
| `experiments/monography_FA` | experiment | untracked | keep_reference | `research/faithful_abstraction_v1` |
| `experiments/monography_FA/00_program.md` | monograph | untracked | keep_reference | `research/faithful_abstraction_v1/00_program.md` |
| `experiments/monography_FA/01_empirical_basis.md` | monograph | untracked | keep_reference | `research/faithful_abstraction_v1/01_empirical_basis.md` |
| `experiments/monography_FA/02_fa_theory.md` | monograph | untracked | keep_reference | `research/faithful_abstraction_v1/02_fa_theory.md` |
| `experiments/monography_FA/REVIEW_PACKET.md` | monograph | untracked | keep_reference | `research/faithful_abstraction_v1/REVIEW_PACKET.md` |

### justitia_boundary

| path | type | git state | keep | destination |
|---|---|---|---|---|
| `experiments/18_0_shield_synthesis` | experiment | untracked+ignored | keep_active | `experiments/JB/18_0_shield_synthesis` |
| `experiments/18_0_shield_synthesis/.pytest_cache` | archive | ignored | delete_candidate | `no destination; remove from working tree after approval or keep ignored locally` |
| `experiments/18_0_shield_synthesis/README.md` | memo | untracked | keep_active | `experiments/JB/18_0_shield_synthesis/README.md` |
| `experiments/18_0_shield_synthesis/claude_code_task_18_0_shield_synthesis.md` | experiment | untracked | keep_active | `experiments/JB/18_0_shield_synthesis/claude_code_task_18_0_shield_synthesis.md` |
| `experiments/18_0_shield_synthesis/outputs_18_0` | result | untracked | keep_reference | `experiments/JB/18_0_shield_synthesis/outputs_18_0` |
| `experiments/18_0_shield_synthesis/outputs_18_0/backward_reachability_report.json` | result | untracked | keep_reference | `experiments/JB/18_0_shield_synthesis/outputs_18_0/backward_reachability_report.json` |
| `experiments/18_0_shield_synthesis/outputs_18_0/control_report.json` | result | untracked | keep_reference | `experiments/JB/18_0_shield_synthesis/outputs_18_0/control_report.json` |
| `experiments/18_0_shield_synthesis/outputs_18_0/final_decision.json` | result | untracked | keep_reference | `experiments/JB/18_0_shield_synthesis/outputs_18_0/final_decision.json` |
| `experiments/18_0_shield_synthesis/outputs_18_0/monotonicity_report.json` | result | untracked | keep_reference | `experiments/JB/18_0_shield_synthesis/outputs_18_0/monotonicity_report.json` |
| `experiments/18_0_shield_synthesis/outputs_18_0/shield_sample.json` | result | untracked | keep_reference | `experiments/JB/18_0_shield_synthesis/outputs_18_0/shield_sample.json` |
| `experiments/18_0_shield_synthesis/outputs_18_0/substrate_characterization.md` | result | untracked | keep_reference | `experiments/JB/18_0_shield_synthesis/outputs_18_0/substrate_characterization.md` |
| `experiments/18_0_shield_synthesis/outputs_18_0/summary.md` | result | untracked | keep_reference | `experiments/JB/18_0_shield_synthesis/outputs_18_0/summary.md` |
| `experiments/18_0_shield_synthesis/outputs_18_0/upward_closure_report.json` | result | untracked | keep_reference | `experiments/JB/18_0_shield_synthesis/outputs_18_0/upward_closure_report.json` |
| `experiments/18_0_shield_synthesis/scripts` | code | untracked | keep_active | `experiments/JB/18_0_shield_synthesis/scripts` |
| `experiments/18_0_shield_synthesis/scripts/run_shield_synthesis.py` | code | untracked | keep_active | `experiments/JB/18_0_shield_synthesis/scripts/run_shield_synthesis.py` |
| `experiments/18_0_shield_synthesis/src` | code | untracked+ignored | keep_active | `experiments/JB/18_0_shield_synthesis/src` |
| `experiments/18_0_shield_synthesis/src/__pycache__` | archive | ignored | delete_candidate | `no destination; remove from working tree after approval or keep ignored locally` |
| `experiments/18_0_shield_synthesis/src/justitia_harvest.py` | code | untracked | keep_active | `experiments/JB/18_0_shield_synthesis/src/justitia_harvest.py` |
| `experiments/18_0_shield_synthesis/src/shield.py` | code | untracked | keep_active | `experiments/JB/18_0_shield_synthesis/src/shield.py` |
| `experiments/18_0_shield_synthesis/tests` | code | untracked+ignored | keep_active | `experiments/JB/18_0_shield_synthesis/tests` |
| `experiments/18_0_shield_synthesis/tests/__pycache__` | archive | ignored | delete_candidate | `no destination; remove from working tree after approval or keep ignored locally` |
| `experiments/18_0_shield_synthesis/tests/test_shield.py` | code | untracked | keep_active | `experiments/JB/18_0_shield_synthesis/tests/test_shield.py` |
| `experiments/18_1_shielded_training` | experiment | untracked+ignored | keep_active | `experiments/JB/18_1_shielded_training` |
| `experiments/18_1_shielded_training/.pytest_cache` | archive | ignored | delete_candidate | `no destination; remove from working tree after approval or keep ignored locally` |
| `experiments/18_1_shielded_training/README.md` | memo | untracked | keep_active | `experiments/JB/18_1_shielded_training/README.md` |
| `experiments/18_1_shielded_training/claude_code_task_18_1_shielded_training.md` | experiment | untracked | keep_active | `experiments/JB/18_1_shielded_training/claude_code_task_18_1_shielded_training.md` |
| `experiments/18_1_shielded_training/outputs_18_1` | result | untracked | keep_reference | `experiments/JB/18_1_shielded_training/outputs_18_1` |
| `experiments/18_1_shielded_training/outputs_18_1/abstraction_fidelity_report.json` | result | untracked | keep_reference | `experiments/JB/18_1_shielded_training/outputs_18_1/abstraction_fidelity_report.json` |
| `experiments/18_1_shielded_training/outputs_18_1/final_decision.json` | result | untracked | keep_reference | `experiments/JB/18_1_shielded_training/outputs_18_1/final_decision.json` |
| `experiments/18_1_shielded_training/outputs_18_1/level_A_decision.json` | result | untracked | keep_reference | `experiments/JB/18_1_shielded_training/outputs_18_1/level_A_decision.json` |
| `experiments/18_1_shielded_training/outputs_18_1/level_A_preregistration.json` | result | untracked | keep_reference | `experiments/JB/18_1_shielded_training/outputs_18_1/level_A_preregistration.json` |
| `experiments/18_1_shielded_training/outputs_18_1/level_B_decision.json` | result | untracked | keep_reference | `experiments/JB/18_1_shielded_training/outputs_18_1/level_B_decision.json` |
| `experiments/18_1_shielded_training/outputs_18_1/summary.md` | result | untracked | keep_reference | `experiments/JB/18_1_shielded_training/outputs_18_1/summary.md` |
| `experiments/18_1_shielded_training/scripts` | code | untracked | keep_active | `experiments/JB/18_1_shielded_training/scripts` |
| `experiments/18_1_shielded_training/scripts/run_18_1.py` | code | untracked | keep_active | `experiments/JB/18_1_shielded_training/scripts/run_18_1.py` |
| `experiments/18_1_shielded_training/src` | code | untracked+ignored | keep_active | `experiments/JB/18_1_shielded_training/src` |
| `experiments/18_1_shielded_training/src/__pycache__` | archive | ignored | delete_candidate | `no destination; remove from working tree after approval or keep ignored locally` |
| `experiments/18_1_shielded_training/src/fidelity.py` | code | untracked | keep_active | `experiments/JB/18_1_shielded_training/src/fidelity.py` |
| `experiments/18_1_shielded_training/src/levelb.py` | code | untracked | keep_active | `experiments/JB/18_1_shielded_training/src/levelb.py` |
| `experiments/18_1_shielded_training/tests` | code | untracked+ignored | keep_active | `experiments/JB/18_1_shielded_training/tests` |
| `experiments/18_1_shielded_training/tests/__pycache__` | archive | ignored | delete_candidate | `no destination; remove from working tree after approval or keep ignored locally` |
| `experiments/18_1_shielded_training/tests/test_fidelity.py` | code | untracked | keep_active | `experiments/JB/18_1_shielded_training/tests/test_fidelity.py` |
| `experiments/JB0.E1_Standard_CEGAR_Boundary_Assessment` | experiment | untracked | duplicate_candidate | `experiments/JB/JB0.E1_Standard_CEGAR_Boundary_Assessment` |
| `experiments/JB0.E1_Standard_CEGAR_Boundary_Assessment/JB0.E1_Standard_CEGAR_Boundary_Assessment.md` | memo | untracked | duplicate_candidate | `experiments/JB/JB0.E1_Standard_CEGAR_Boundary_Assessment/JB0.E1_Standard_CEGAR_Boundary_Assessment.md` |
| `experiments/JB0_E1_standard_cegar_boundary_assessment` | experiment | untracked | keep_active | `experiments/JB/JB0_E1_standard_cegar_boundary_assessment` |
| `experiments/JB0_E1_standard_cegar_boundary_assessment/outputs` | result | untracked | keep_reference | `experiments/JB/JB0_E1_standard_cegar_boundary_assessment/outputs` |
| `experiments/JB0_E1_standard_cegar_boundary_assessment/outputs/abstract_state_growth.csv` | result | untracked | keep_reference | `experiments/JB/JB0_E1_standard_cegar_boundary_assessment/outputs/abstract_state_growth.csv` |
| `experiments/JB0_E1_standard_cegar_boundary_assessment/outputs/baseline_metrics.csv` | result | untracked | keep_reference | `experiments/JB/JB0_E1_standard_cegar_boundary_assessment/outputs/baseline_metrics.csv` |
| `experiments/JB0_E1_standard_cegar_boundary_assessment/outputs/best_boundary_definition.md` | result | untracked | keep_reference | `experiments/JB/JB0_E1_standard_cegar_boundary_assessment/outputs/best_boundary_definition.md` |
| `experiments/JB0_E1_standard_cegar_boundary_assessment/outputs/cegar_boundary_decision.json` | result | untracked | keep_reference | `experiments/JB/JB0_E1_standard_cegar_boundary_assessment/outputs/cegar_boundary_decision.json` |
| `experiments/JB0_E1_standard_cegar_boundary_assessment/outputs/confusion_matrices.csv` | result | untracked | keep_reference | `experiments/JB/JB0_E1_standard_cegar_boundary_assessment/outputs/confusion_matrices.csv` |
| `experiments/JB0_E1_standard_cegar_boundary_assessment/outputs/final_report.md` | result | untracked | keep_reference | `experiments/JB/JB0_E1_standard_cegar_boundary_assessment/outputs/final_report.md` |
| `experiments/JB0_E1_standard_cegar_boundary_assessment/outputs/heldout_metrics.csv` | result | untracked | keep_reference | `experiments/JB/JB0_E1_standard_cegar_boundary_assessment/outputs/heldout_metrics.csv` |
| `experiments/JB0_E1_standard_cegar_boundary_assessment/outputs/implementation_notes.md` | result | untracked | keep_reference | `experiments/JB/JB0_E1_standard_cegar_boundary_assessment/outputs/implementation_notes.md` |
| `experiments/JB0_E1_standard_cegar_boundary_assessment/outputs/plateau_analysis.json` | result | untracked | keep_reference | `experiments/JB/JB0_E1_standard_cegar_boundary_assessment/outputs/plateau_analysis.json` |
| `experiments/JB0_E1_standard_cegar_boundary_assessment/outputs/predicate_catalog.csv` | result | untracked | keep_reference | `experiments/JB/JB0_E1_standard_cegar_boundary_assessment/outputs/predicate_catalog.csv` |
| `experiments/JB0_E1_standard_cegar_boundary_assessment/outputs/refinement_trace.csv` | result | untracked | keep_reference | `experiments/JB/JB0_E1_standard_cegar_boundary_assessment/outputs/refinement_trace.csv` |
| `experiments/JB0_E1_standard_cegar_boundary_assessment/outputs/remaining_witnesses.md` | result | untracked | keep_reference | `experiments/JB/JB0_E1_standard_cegar_boundary_assessment/outputs/remaining_witnesses.md` |
| `experiments/JB0_E1_standard_cegar_boundary_assessment/outputs/vacuity_analysis.json` | result | untracked | keep_reference | `experiments/JB/JB0_E1_standard_cegar_boundary_assessment/outputs/vacuity_analysis.json` |
| `experiments/JB0_E1_standard_cegar_boundary_assessment/outputs/witness_reduction_by_iteration.csv` | result | untracked | keep_reference | `experiments/JB/JB0_E1_standard_cegar_boundary_assessment/outputs/witness_reduction_by_iteration.csv` |
| `experiments/JB0_E1_standard_cegar_boundary_assessment/scripts` | code | untracked | keep_active | `experiments/JB/JB0_E1_standard_cegar_boundary_assessment/scripts` |
| `experiments/JB0_E1_standard_cegar_boundary_assessment/scripts/run_standard_cegar_boundary.py` | code | untracked | keep_active | `experiments/JB/JB0_E1_standard_cegar_boundary_assessment/scripts/run_standard_cegar_boundary.py` |

### substrate_discovery

| path | type | git state | keep | destination |
|---|---|---|---|---|
| `experiments/Door1_Extracted_Knowledge_v1.md` | memo | untracked | keep_active | `research/door1_postmortem/Door1_Extracted_Knowledge_v1.md` |
| `experiments/Substrate_Discovery_v1` | experiment | untracked | keep_active | `research/substrate_discovery_v1` |
| `experiments/Substrate_Discovery_v1/00_research_axioms.md` | memo | untracked | keep_active | `research/substrate_discovery_v1/00_research_axioms.md` |
| `experiments/Substrate_Discovery_v1/00_search_frame.md` | memo | untracked | keep_active | `research/substrate_discovery_v1/00_search_frame.md` |
| `experiments/Substrate_Discovery_v1/01_research_question.md` | memo | untracked | keep_active | `research/substrate_discovery_v1/01_research_question.md` |
| `experiments/Substrate_Discovery_v1/02_candidate_axes.md` | memo | untracked | keep_active | `research/substrate_discovery_v1/02_candidate_axes.md` |
| `experiments/Substrate_Discovery_v1/03_Computability_of_Environment.md` | memo | untracked | keep_active | `research/substrate_discovery_v1/03_Computability_of_Environment.md` |
| `experiments/Substrate_Discovery_v1/04_Derivability.md` | memo | untracked | keep_active | `research/substrate_discovery_v1/04_Derivability.md` |
| `experiments/Substrate_Discovery_v1/04_triage_framework.md` | memo | untracked | keep_active | `research/substrate_discovery_v1/04_triage_framework.md` |
| `experiments/Substrate_Discovery_v1/05_Interaction_and_Identifiability.md` | memo | untracked | keep_active | `research/substrate_discovery_v1/05_Interaction_and_Identifiability.md` |
| `experiments/Substrate_Discovery_v1/05_candidate_triage_matrix.md` | memo | untracked | keep_active | `research/substrate_discovery_v1/05_candidate_triage_matrix.md` |
| `experiments/Substrate_Discovery_v1/06_Necessary_Properties.md` | memo | untracked | keep_active | `research/substrate_discovery_v1/06_Necessary_Properties.md` |
| `experiments/Substrate_Discovery_v1/07_Search_Strategy.md` | memo | untracked | keep_active | `research/substrate_discovery_v1/07_Search_Strategy.md` |
| `experiments/Substrate_Discovery_v1/08_Candidate_Evaluation_Framework.md` | memo | untracked | keep_active | `research/substrate_discovery_v1/08_Candidate_Evaluation_Framework.md` |
| `experiments/Substrate_Discovery_v1/09_Open_Problems.md` | memo | untracked | keep_active | `research/substrate_discovery_v1/09_Open_Problems.md` |
| `experiments/Substrate_Discovery_v1/2026-06-29_research_session.md` | memo | untracked | keep_active | `research/substrate_discovery_v1/2026-06-29_research_session.md` |

### unknown

| path | type | git state | keep | destination |
|---|---|---|---|---|
| `"experiments/monograph_17/ASCESIS_Research_Ontology_Part_I_\342\200\224_Foundations_&_Research_Ontology_Version_2.0_Post-17F.md"` | unknown | untracked | needs_human_review | `"experiments/monograph_17/ASCESIS_Research_Ontology_Part_I_\342\200\224_Foundations_&_Research_Ontology_Version_2.0_Post-17F.md"` |
| `.claude` | unknown | ignored | delete_candidate | `no destination; remove from working tree after approval or keep ignored locally` |
| `.claude/scheduled_tasks.lock` | unknown | ignored | delete_candidate | `no destination; remove from working tree after approval or keep ignored locally` |
| `.claude/settings.local.json` | result | ignored | delete_candidate | `no destination; remove from working tree after approval or keep ignored locally` |
| `.git` | unknown | unknown | needs_human_review | `.git` |
| `experiments` | experiment | tracked+untracked+ignored | needs_human_review | `experiments` |
| `experiments/README.md` | memo | tracked | needs_human_review | `experiments/README.md` |
| `experiments/ascesis_17.zip` | archive | untracked | delete_candidate | `no destination; remove from working tree after approval or keep ignored locally` |
