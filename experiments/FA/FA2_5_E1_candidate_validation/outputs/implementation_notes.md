# Implementation Notes

- Replayed the unchanged BA1 baseline grid via the FA1 extractor.
- Population A uses all false-safe witnesses.
- Population B samples an equal number of SAFE-and-remain-SAFE states with seed `2525`.
- Models are pure-Python logistic discriminators over fixed coordinate sets, trained on trajectory-group split and evaluated on held-out trajectory groups.
- No oracle variables, future collapse labels, `capture_index`, permanence, or reporting-only metrics are used as candidate coordinates.
- T-C is treated as downstream monotonicity testing and is not executed here.
