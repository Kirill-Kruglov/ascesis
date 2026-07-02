# CL2.1 Evaluation Integrity Audit

- target fields appear in learner features: `False`.
- test targets are used in fit: `False`.
- shuffled-control test targets remain original true targets: `True`.
- prediction is compared against original true test targets: `True`.
- forbidden fields exist in rows: `False`.
- forbidden oracle calls are imported or called: `[]`.
- independent impossible targets scored below threshold: recorded in `outputs/impossible_target_diagnostics.json`.
- evaluation mismatch found: `False`.
