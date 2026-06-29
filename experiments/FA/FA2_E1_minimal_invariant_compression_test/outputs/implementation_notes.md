# FA2.E1 Implementation Notes

- Input source: `experiments/FA1_E1_false_safe_witness_taxonomy/outputs/witness_taxonomy.csv`.
- No new Justitia simulation was run because FA1 already exported current collapse clauses, future collapse step, delayed observation summaries, policy-visible concentration, and allocation/control summaries.
- `I2` uses `Obs.resource_concentration` fields from FA1; it does not use reporting `resource_hhi`.
- `I3` uses compact delayed consequence flags, not raw history.
- `I4_oracle` is reported only for theoretical compressibility and is not counted as constructive refinement.
- `I4_proxy` was selected by single-threshold coverage over the R3 residual using current/delayed fields available at step time.
- The major limitation is that FA1 witness output does not include non-false-safe SAFE states, so non-oracle proxy false-positive rates cannot be estimated in this experiment.
