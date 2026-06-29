# FA1.E1 Implementation Notes

- Replayed the BA1 baseline Justitia grid with `mode='governance'` only.
- The transition loop mirrors `EvolvableStrategyModel.step` but exposes delayed observation, allocation, and control summaries per step.
- Shield projection uses 18.0 `ShieldParams(A_collapse=40, trig=34, K=1, Rc=1, Ra=2, Cmax=44, Amax=44)` and `compute_doomed(..., 'bounded')` unchanged.
- Concrete collapse predicate is unchanged: mean zone welfare `< 0.32`, or failed-zone count `>= 4` using zone welfare `< 0.20`, or total mass `< 35`.
- Classification is conservative: current omitted collapse clauses are assigned first; future-collapse cases are assigned to history/control/concentration only when explicit BA4.1 policy/control signals are active.
- `capture_index` and reporting `resource_hhi` are treated as low-confidence layer-confusion evidence, not as transition mechanisms.

## Run Configuration

- worlds: `all`
- policies: `all`
- seeds: `9600..9607`
- steps: `100`

## BA1 Consistency

- Extracted false-safe count: `5839`.
- Extracted shield acceptance rate: `0.690125`.
- Extracted future collapse rate: `0.553167`.
