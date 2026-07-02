# Experiment 17A.2: Semantic Perturbation Taxonomy

Experiment 17A showed that the backbone is weak under adversarial perturbations, but it mixed two categories: representation-preserving graph rewrites and theory-changing edits.

17A.2 exists only to resolve that ambiguity. It does not add a generator, does not redesign the verifier, and does not strengthen the consequence relation. It classifies perturbation operators, audits which ones are representation-preserving under the current verifier, then reruns attacks separately for representation-only and theory-changing edits.
