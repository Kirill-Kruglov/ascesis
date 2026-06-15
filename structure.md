# Structure

This is a proposed map of the second circle. It is organized by bridges between fields, not by isolated topics. The list is a draft for human approval, not a final table of contents.

Each bridge names the areas it connects and points back to the field-check nodes and dialogue locations that motivated it. The raw dialogue is source material for internal tracing; it is not part of the initial public skeleton.

## Proposed Bridges

### 1. From Verified Isolation to Semantic Alignment

Connects: seL4 / capability identity, formal verification, specification gaming, semantic alignment.

Related field-check nodes: 7, 10.

Related dialogue anchors: `dialog.part_1.md:7`, `dialog.part_1.md:11`, `dialog.part_1.md:13`, `dialog.part_3.md:13`, `dialog.part_3.md:17`, `dialog.part_4.md:11`, `dialog.part_4.md:13`, `dialog.part_4.md:23`.

Working role: establish the engineering starting point. Verified containment can improve the lower layer of trust, but does not solve the problem of specifying what an agent should mean or do.

### 2. From Containment to Resource-Time Safety

Connects: AI containment limits, Rice/Godel/Lobian limits, detection, reversibility, work factor, bounded horizon.

Related field-check nodes: 1, 7, 8.

Related dialogue anchors: `dialog.part_4.md:27`, `dialog.part_4.md:31`, `dialog.part_8.md:35`, `dialog.part_9.md:9`, `dialog.part_18.md:21`, `dialog.part_20.md:15`.

Working role: replace the binary question "is it controlled?" with weaker operational questions: can deviation be detected, can action be reversed, what is the cost of violation, and how long is the reaction window?

### 3. From Instrumental Convergence to Reflective Restraint

Connects: instrumental convergence, goal-content integrity, reflective stability, successor risk, mild optimization.

Related field-check nodes: 1, 5.

Related dialogue anchors: `dialog.part_7.md:3`, `dialog.part_7.md:9`, `dialog.part_7.md:17`, `dialog.part_10.md:41`, `dialog.part_10.md:43`, `dialog.part_10.md:53`, `dialog.part_11.md:7`.

Working role: examine whether restraint can be framed as a consequence of goal preservation and reflective self-modeling rather than as an externally imposed prohibition.

### 4. From Reject Option to Human-Visible Remainder

Connects: selective prediction, reject option, semantic uncertainty, manual fallback, nonzero remainder.

Related field-check nodes: 2, 6.

Related dialogue anchors: `dialog.part_16.md:29`, `dialog.part_16.md:31`, `dialog.part_17.md:9`, `dialog.part_17.md:13`, `dialog.part_18.md:21`.

Working role: treat refusal as a designed behavior of a partial system, not as a failure path. The unresolved remainder must be explicit before action, not hidden inside defaults.

### 5. From Natural Language to Formal Specification

Connects: semantic parsing, formal specification, Paninian rule systems, language of thought, ambiguity handling.

Related field-check nodes: 6, 9.

Related dialogue anchors: `dialog.part_13.md:11`, `dialog.part_13.md:13`, `dialog.part_13.md:15`, `dialog.part_14.md:17`, `dialog.part_14.md:19`, `dialog.part_14.md:23`, `dialog.part_14.md:29`, `dialog.part_15.md:21`.

Working role: frame the language layer as a boundary between expressive reasoning and machine-checkable specification, with conflict resolution and explicit translation loss.

### 6. From Round-Trip Consistency to a Measured Seam

Connects: autoencoders, reconstruction error, round-trip consistency, semantic parsing, verifier/user-in-the-loop workflows.

Related field-check nodes: 2, 6, 7.

Related dialogue anchors: `dialog.part_16.md:13`, `dialog.part_16.md:15`, `dialog.part_16.md:19`, `dialog.part_16.md:25`, `dialog.part_16.md:29`, `dialog.part_17.md:27`.

Working role: propose the seam as a partial translation process whose failures are measured through reconstruction, verification, and explicit refusal rather than hidden in silent coercion.

### 7. From Oversight Regress to Commitment

Connects: corrigibility, oversight, cryptographic commitments, self-checking, committed reference.

Related field-check nodes: 3, 4.

Related dialogue anchors: `dialog.part_19.md:27`, `dialog.part_19.md:31`, `dialog.part_19.md:33`, `dialog.part_19.md:35`, `dialog.part_19.md:37`, `dialog.part_20.md:15`.

Working role: explore the shift from an external checker regress to checks against a prior commitment, while keeping separate the preservation of a commitment from the correctness of what was committed.

### 8. From Commitment to Unforgeable State

Connects: cryptographic commitment, quantum money, no-cloning, quantum tokens, identity/state rather than behavior.

Related field-check nodes: 4.

Related dialogue anchors: `dialog.part_4.md:25`, `dialog.part_11.md:25`, `dialog.part_20.md:19`, `dialog.part_20.md:23`, `dialog.part_20.md:31`, `dialog.part_21.md:13`.

Working role: keep the quantum layer narrow. The bridge concerns physical unforgeability of a committed state, not quantum explanations of cognition or alignment.

### 9. From Sandbox Prediction to Speed Limits

Connects: sandboxing, chaos, Lyapunov time, critical transitions, early-warning signals.

Related field-check nodes: 8.

Related dialogue anchors: `dialog.part_9.md:23`, `dialog.part_9.md:31`, `dialog.part_18.md:3`, `dialog.part_18.md:13`, `dialog.part_18.md:17`, `dialog.part_18.md:21`, `dialog.part_18.md:27`.

Working role: make sandboxing a finite-horizon instrument. The policy question becomes how to keep action within the measured horizon of prediction and rollback.

### 10. From First Circle to Second Circle

Connects: raw dialogue, field check, public map, glossary discipline, publication form.

Related field-check nodes: all nodes, especially the final summary.

Related dialogue anchors: `dialog.part_21.md:3`, `dialog.part_21.md:9`, `dialog.part_21.md:13`, `dialog.part_21.md:15`, `dialog.part_22.md:3`, `dialog.part_22.md:9`, `dialog.part_22.md:11`, `dialog.part_22.md:15`.

Working role: explain why the published work starts from the second circle: not to hide the path, but to avoid making the raw path itself carry claims it was not designed to carry.

## Decisions for Human Approval

- Whether these ten bridges are the right first set.
- Whether bridge 8 belongs in the first public arc or should remain a later technical appendix.
- Whether bridge 10 should be part of the main structure or remain only repository metadata.
- Whether bridge 3 should use the working term "reflective restraint" or a more standard field term.
