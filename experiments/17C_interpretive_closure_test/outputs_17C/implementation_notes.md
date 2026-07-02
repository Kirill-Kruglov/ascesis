# Implementation Notes

- The DAG generator and consequence verifier are reused unchanged.
- The closure loop does not use external labels, embeddings, ontologies, internet data, or human semantic judgments.
- Interpreter state is computed from internally derivable quantities: consequence frequency, operator diversity, DAG diversity, expression depth, intervention/conditional role, and iterative reuse across operator/depth channels.
- Weak closure reweights attack summaries by interpreter score but does not forbid derivations.
- Strong closure prunes to closure-active consequence classes using the internally computed score threshold.
- Class A/Class B perturbation taxonomy is reused from 17A.2.
