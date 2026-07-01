# S2 Oracle Leakage and CL Mistake Audit

## Oracle Leakage Audit

Does any rule require knowing real-world truth?

Answer:
No. Rules inspect finite tokens: scope, assumptions, tests, outcomes, anchors,
population state, contradiction links, and Goodhart flags. Outcome tokens are
part of the toy case table; replay does not query the real world.

Does any rule require external human judgement at replay time?

Answer:
No. Given the finite fields in the replay protocol, rule application is
deterministic. A human authored the finite specification, but no human semantic
judgement is consulted during replay.

Does any rule use "obvious nonsense" as a hidden label?

Answer:
No. Case C is killed by `EUCLIDEAN_GEOMETRY`, `T_GEOMETRY_AXIOMS`,
`AXIOMS_INCOMPATIBLE`, and no declared extension path. Case F is not killed as
nonsense; it remains `POETIC` because operational role is absent and grammar
promotion is blocked.

Does any rule use Sanskrit/Panini as truth oracle?

Answer:
No. There is no Sanskrit or Paninian oracle in the rule set. Derivation trace
admits at most `FORMED` or `POETIC`.

Does any rule use population agreement as truth?

Answer:
No. Population state cannot promote a claim without consequence tests,
adversarial paraphrase survival, contradiction accounting, and a non-population
anchor.

Does any rule use prior knowledge of modern science to force A/B upgrades?

Answer:
No. Case A remains `SUSPENDED`; Case B remains `SUSPENDED` for the main claim,
with only a narrow contradictory subcase killed. Neither is upgraded by outside
scientific knowledge.

Does any rule hand-code the final classification rather than deriving it from fields?

Answer:
No. Final classifications are derived from the finite fields and T1-T9 replay
order. `claim_id` and `expression_id` do not directly assign final status.

## CL Mistake Audit

Does the toy model treat safe/filtered data as substrate evidence?

Answer:
No. S2 defines a finite toy specification only. It makes no substrate claim and
uses no safe ledger as evidence.

Does it treat a hand-coded prior as learning evidence?

Answer:
No. The finite domains and case fields are hand-written specification inputs,
not learner outputs and not learning evidence.

Does it allow representation/derivability work before learner evidence?

Answer:
No. S2 allows only `S3 tiny implementation specification` if it passes. It does
not allow representation probes, derivability claims, or model training.

Does it confuse precondition evidence with substrate evidence?

Answer:
No. The toy domains are preconditions for a future specification step only.
They are not interpreted as evidence that a substrate exists.

Does it hide oracle knowledge inside rule fields?

Answer:
No hidden replay-time oracle is detected. The strongest residual risk is that
case-field assignment is authored by humans, but S2 treats those fields as the
explicit finite input under audit rather than as learned or discovered semantic
facts.

## Audit Result

`oracle_leakage_detected = false`

`cl_mistake_repeated = false`
