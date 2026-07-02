# CL2 Leakage Audit

- learner-visible inputs: `source_zones`, `source_mass`, `source_phase`, `action`.
- learner targets: `successor_zones`, `successor_mass`, `successor_phase`.
- forbidden fields checked: collapse labels, future outcomes, collapse mechanisms, witness classes, admission decisions, rollout results, post-hoc metrics, source-file lineage features.
- forbidden fields present in dataset rows: `False`.
- collapse labels appear in features: `False`.
- future outcomes appear in features: `False`.
- admission decisions appear in features: `False`.
- learner code imports forbidden oracle functions: `[]`.
- learner code calls forbidden oracle functions: `[]`.
- forbidden call regex hits in `learners.py`: `[]`.
- shuffled-target control passed: `False`.
- shuffled-target exact accuracy used for the gate: `0.6463414634146342`. This is the maximum exact accuracy across random, source-state, and structural test splits.
- evaluation uses target values only for metric comparison after prediction; target/successor values are not passed as learner inputs.
