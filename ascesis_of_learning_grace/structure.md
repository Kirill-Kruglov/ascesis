# Structure

This is the working map of the second circle. It is organized by bridges between fields, not by isolated topics. The list is accepted as a likely first set, but remains open to later revision.

Each bridge names the areas it connects, gives the field-check grounding, and records the dialogue trace that motivated the bridge. Dialogue traces are short paraphrased anchors tied to source lines, not publication of the raw dialogue. The raw dialogue remains source material for internal tracing; it is not part of the initial public skeleton.

## Proposed Bridges

### 1. From Verified Isolation to Semantic Alignment

Connects: seL4 / capability identity, formal verification, specification gaming, semantic alignment.

Related field-check nodes: 7, 10.

Framing: Klein et al., Murray et al., Dennis and Van Horn, Miller, and the seL4/object-capability literature own the lower-layer security material here; Amodei et al. and Rice/Godel/Loeb-style limits own the specification-limit side. This bridge asks how a verified isolation layer changes the trust boundary without solving semantic alignment. It connects implementation correctness and capability identity to the harder question of whether the specification captures the intended behavior. It does not solve specification gaming, reward hacking, or the problem of defining the objective.

Dialogue trace:

> `dialog.part_1.md:7`: seL4 enters as a formally verified microkernel.
>
> `dialog.part_1.md:11`: the relevant guarantee is implementation-to-specification correspondence.
>
> `dialog.part_1.md:13`: capability-based security supplies unforgeable authority rather than ambient authority.
>
> `dialog.part_3.md:17`: the bottleneck shifts from process isolation to semantic verification quality.
>
> `dialog.part_4.md:11`: verified containment still depends on a complete enough specification.
>
> `dialog.part_4.md:13`: model-external channels and assumptions remain outside the proof boundary.

Field-check comment:

> `field_check.md` node 10 marks seL4 verification and object-capability identity as `[FULL MATCH]`, while the claim that seL4 does not solve semantic alignment is `[PARTIAL]`: the sources cover kernel guarantees; the AI-agent interpretation is the bridge.
>
> `field_check.md` node 7 marks Rice/Godel/specification-gaming limits as `[FULL MATCH]`.

Working role: establish the engineering starting point. Verified isolation can improve the lower layer of trust, but does not solve the problem of specifying what an agent should mean or do.

### 2. From Containment to Resource-Time Safety

Connects: AI containment limits, Rice/Godel/Loebian limits, detection, reversibility, work factor, bounded horizon.

Related field-check nodes: 1, 7, 8.

Framing: Rice, Godel, Loeb, Yudkowsky and Herreshoff, Amodei et al., Scheffer et al., and the predictability-horizon literature own the limits and monitoring material. This bridge reframes containment from a binary property into a resource-time question: what can be detected, reversed, delayed, bounded, or made costly within a finite window. It connects formal undecidability and specification limits to operational safety handles such as detection, rollback, and work factor. It does not prove long-term containment of a stronger agent, and it does not turn partial guarantees into total guarantees.

Dialogue trace:

> `dialog.part_4.md:27`: the reachable weakening is detection, reversibility, and domain limitation instead of total control.
>
> `dialog.part_4.md:31`: partial, detectable, reversible, time-limited guarantees remain meaningful after total containment is rejected.
>
> `dialog.part_8.md:35`: dangerous composition is treated as something to make costly and observable.
>
> `dialog.part_9.md:9`: detection, reversibility, and work factor form the operational safety frame.
>
> `dialog.part_18.md:21`: sandboxing narrows but does not eliminate the residual class.
>
> `dialog.part_20.md:15`: classical cryptographic commitments are resource guarantees, not Boolean guarantees.

Field-check comment:

> `field_check.md` node 7 gives `[FULL MATCH]` for verification limits and specification gaming.
>
> `field_check.md` node 8 gives `[FULL MATCH]` for predictability horizons and early-warning signals, with the concrete AGI sandbox policy marked as `[PARTIAL]`.

Working role: replace the binary question "is it controlled?" with weaker operational questions: can deviation be detected, can action be reversed, what is the cost of violation, and how long is the reaction window?

### 3. From Goal-Content Integrity / Reflective Stability to Bounded Optimization

Project label: reflective restraint.

More standard nearby terms: goal-content integrity, reflective stability, Vingean reflection, tiling agents, mild optimization, quantilization, satisficing.

Connects: instrumental convergence, goal-content integrity, reflective stability, successor risk, mild optimization.

Related field-check nodes: 1, 5.

Framing: Omohundro, Bostrom, Yudkowsky and Herreshoff, Fallenstein and Soares, and Taylor own the core material: instrumental convergence, goal-content integrity, reflective stability, tiling agents, Vingean reflection, and quantilization. This bridge asks whether a reflective agent's concern for preserving its own goals can connect to bounded optimization, rather than only to resource acquisition and self-improvement. The project label `reflective restraint` names that local connection after the standard fields have been credited. It does not establish human alignment; preserving an agent's goals is separate from those goals being safe or correct.

Dialogue trace:

> `dialog.part_7.md:9`: resource acquisition and self-improvement are treated as instrumentally convergent subgoals rather than terminal goals.
>
> `dialog.part_7.md:17`: successor construction is reframed as an alignment problem faced by the agent itself.
>
> `dialog.part_7.md:21`: a reflective agent that accepts successor uncontrollability has a reason to limit uncontrolled self-surpassing.
>
> `dialog.part_7.md:29`: the proposed restraint depends on whether stable tiling remains unsolved.
>
> `dialog.part_10.md:41`: cognition is framed as modeling the world and the agent, not only optimizing for an external task.
>
> `dialog.part_10.md:53`: self-modeling is necessary for restraint but not sufficient for it.
>
> `dialog.part_11.md:7`: the proposal changes the object of optimization rather than rejecting optimization.

Field-check comment:

> `field_check.md` node 1 gives `[FULL MATCH]` for successor/self-modification risk against Omohundro and Yudkowsky-Herreshoff.
>
> `field_check.md` node 5 gives `[PARTIAL]`: instrumental convergence is standard, while the dialogue adds a reflective restraint frame.

Working role: examine whether restraint can be framed as a consequence of goal preservation and reflective self-modeling rather than as an externally imposed prohibition.

### 4. From Reject Option to Human-Visible Remainder

Connects: selective prediction, reject option, semantic uncertainty, manual fallback, nonzero remainder.

Related field-check nodes: 2, 6.

Framing: Chow, Geifman, El-Yaniv, and the selective prediction/reject-option literature own the refusal mechanism. This bridge connects reject option to semantic translation and agentic workflow design: a system that cannot preserve its guarantee should abstain before action. The local term `remainder` names the cases outside the guarantee, but the underlying mechanism is standard selective prediction. It does not make refusal safe by itself; refusal only helps when it is detected before action and no unsafe default action occurs.

Dialogue trace:

> `dialog.part_16.md:29`: the seam is treated as partial, detectably incomplete, and reversible.
>
> `dialog.part_16.md:31`: explicit refusal, detectable gap, and round-trip reversibility replace a total guarantee.
>
> `dialog.part_17.md:9`: a small unresolved fault is treated as evidence of a nonzero remainder.
>
> `dialog.part_17.md:13`: transfer to agentic systems requires pre-action detection and no silent default action.
>
> `dialog.part_18.md:21`: decisions outside the prediction horizon fall into manual fallback or refusal.

Field-check comment:

> `field_check.md` node 2 gives `[FULL MATCH]` for reject option and selective prediction.
>
> `field_check.md` node 6 gives `[PARTIAL]` for the broader seam: semantic parsing, reconstruction error, and verifier/user-in-the-loop workflows exist, but the full seam plus human-visible remainder is a bridge.

Working role: treat refusal as a designed behavior of a partial system, not as a failure path. The unresolved remainder must be explicit before action, not hidden inside defaults.

### 5. From Semantic Parsing / Formal Specification to Agent Self-Description

Connects: semantic parsing, formal specification, Paninian rule systems, language of thought, ambiguity handling.

Related field-check nodes: 6, 9.

Framing: Liang, Jordan and Klein, Gardner et al., Cosler et al., Cardona, Kiparsky, Rajpopat, Fodor, and linguistic relativity work own the component fields: semantic parsing, formal specification, formal/generative grammar, language of thought, and representation effects. This bridge connects those fields to a narrower target: a verifiable protocol of agent self-description rather than a claim to control an LLM's internal cognition. The project label `seam` can be used only after the standard translation and specification fields are named. It does not solve interpretability, and it does not give direct access to the model's latent representations.

Dialogue trace:

> `dialog.part_13.md:11`: the hard boundary requires machine-defined semantics, not a natural language treated as exact.
>
> `dialog.part_13.md:13`: the architecture separates formal core, expressive periphery, and the translation boundary.
>
> `dialog.part_13.md:15`: representation language constrains which self-transformations and goals can be expressed.
>
> `dialog.part_14.md:17`: metarules are used as a model for rules about rule application.
>
> `dialog.part_14.md:19`: deterministic conflict resolution is the desired property where precision is required.
>
> `dialog.part_14.md:29`: the near-term target is a verifiable self-description protocol.
>
> `dialog.part_15.md:21`: formal core and expressive periphery serve different functions and should not be collapsed.

Field-check comment:

> `field_check.md` node 6 gives `[FULL MATCH]` for semantic parsing and reconstruction error, but `[PARTIAL]` for the full verifier/user-in-the-loop seam.
>
> `field_check.md` node 9 gives `[PARTIAL]`: Panini, language-of-thought, and weak linguistic relativity are known fields; the bridge is their use in an agent self-description layer.

Working role: frame the language layer as a boundary between expressive reasoning and machine-checkable specification, with conflict resolution and explicit translation loss.

### 6. From Round-Trip Consistency to a Measured Seam

Connects: autoencoders, reconstruction error, round-trip consistency, semantic parsing, verifier/user-in-the-loop workflows.

Related field-check nodes: 2, 6, 7.

Framing: Hinton and Zemel, anomaly-detection work on reconstruction error, semantic parsing, and NL-to-temporal-logic work own the technical ingredients. This bridge uses round-trip consistency and reconstruction error as a way to make translation loss visible at the boundary between expressive and formal representations. The project label `measured seam` names that local grouping of existing tools. It does not prove semantic preservation; approximate reconstruction can miss meaning shifts and must be paired with refusal and verification.

Dialogue trace:

> `dialog.part_16.md:13`: the central difficulty is mapping a richer representation space into a poorer one.
>
> `dialog.part_16.md:15`: layout rendering is used as a practical analogy for finite data, open-ended configuration, and composition conflicts.
>
> `dialog.part_16.md:19`: scaling requires a deterministic conflict-resolution metaprocedure, not case enumeration.
>
> `dialog.part_16.md:25`: total meaning-preserving translation is not assumed.
>
> `dialog.part_16.md:29`: partiality, detectable loss, and round-trip reversibility replace totality.
>
> `dialog.part_17.md:27`: reconstruction error becomes a candidate signal for translation loss.

Field-check comment:

> `field_check.md` node 6 grounds this in semantic parsing, autoencoder reconstruction error, and NL-to-temporal-logic work.
>
> `field_check.md` node 7 marks the underlying verification limits as `[FULL MATCH]`.

Working role: propose the seam as a partial translation process whose failures are measured through reconstruction, verification, and explicit refusal rather than hidden in silent coercion.

### 7. From Corrigibility / Oversight to Commitment

Connects: corrigibility, oversight, cryptographic commitments, self-checking, committed reference.

Related field-check nodes: 3, 4.

Framing: Soares, Fallenstein, Yudkowsky, Armstrong, and the corrigibility literature own the oversight and correction problem; Blum, Brassard, Chaum, Crepeau, and commitment literature own the commitment mechanism. This bridge connects oversight regress to prior commitment: instead of an infinite chain of checkers, the system is checked against a committed reference. The project label `committed past self` may name the local application, but the underlying mechanisms are corrigibility and cryptographic commitment. It does not establish that the committed basis is correct; it only addresses preservation or authentication of a reference.

Dialogue trace:

> `dialog.part_19.md:27`: self-checking is reframed as a known test that cannot be passed dishonestly.
>
> `dialog.part_19.md:31`: the check is against a committed prior reference rather than an external checker chain.
>
> `dialog.part_19.md:33`: commitment preserves a basis but does not validate the basis.
>
> `dialog.part_19.md:35`: the regress is reduced to whether a finite commitment is unforgeable.
>
> `dialog.part_19.md:37`: correctness of the basis and unforgeability of the commitment remain separate forks.
>
> `dialog.part_20.md:15`: classical commitments are resource-bounded and may weaken relative to a growing optimizer.

Field-check comment:

> `field_check.md` node 3 gives `[PARTIAL]`: corrigibility and cryptographic commitments cover pieces, but not the exact self-checking-against-committed-past-self frame.
>
> `field_check.md` node 4 gives `[PARTIAL]` for the quantum-commitment extension.

Working role: explore the shift from an external checker regress to checks against a prior commitment, while keeping separate the preservation of a commitment from the correctness of what was committed.

### 8. From Quantum Money / No-Cloning to Unforgeable State

Connects: cryptographic commitment, quantum money, no-cloning, quantum tokens, identity/state rather than behavior.

Related field-check nodes: 4.

Framing: Wiesner, Aaronson and Christiano, Kent et al., and quantum-token literature own the no-cloning and unforgeable-token material. This bridge keeps the quantum layer narrow: it is considered only as a possible physical primitive for unforgeable committed state. The project label `quantum anchor` names that narrow role after the quantum money/no-cloning field has been credited. It does not solve behavior, cognition, correctness, or alignment; it only addresses a possible authentication/preservation problem, and even that leaves verification and state-to-behavior linkage open.

Dialogue trace:

> `dialog.part_4.md:25`: no-cloning is treated as a narrow primitive for unforgeable state and identity.
>
> `dialog.part_11.md:25`: quantum machinery is not used as a general explanation of metaoptimization.
>
> `dialog.part_20.md:19`: the proposed quantum role is limited to unforgeability of a commitment state.
>
> `dialog.part_20.md:23`: measurement can interfere with repeated verification of a quantum state.
>
> `dialog.part_20.md:31`: quantum money and no-cloning are the fields to check before using this bridge.
>
> `dialog.part_21.md:13`: quantum money and no-cloning are listed as fields requiring credit and verification.

Field-check comment:

> `field_check.md` node 4 gives `[PARTIAL]`: quantum money and tokens cover unforgeability; the use as an alignment commitment anchor is not directly sourced.

Working role: keep the quantum layer narrow. The bridge concerns physical unforgeability of a committed state, not quantum explanations of cognition or alignment.

### 9. From Predictability Horizons to Sandbox Speed Limits

Connects: sandboxing, chaos, Lyapunov time, critical transitions, early-warning signals.

Related field-check nodes: 8.

Framing: Lyapunov-time and chaos literature, plus Scheffer et al. on early-warning signals, own the predictability and critical-transition material. This bridge connects sandboxing to measured horizons: a sandbox is useful only inside the range where its predictions remain coupled to the target system. The local policy label `speed limit` means keeping action within the measured range of prediction and rollback. It does not make the sandbox a complete oracle, and it does not solve the recursion problem of simulating an agent whose capability exceeds the simulator.

Dialogue trace:

> `dialog.part_9.md:23`: the operational question is whether irreversible thresholds can be recognized before crossing.
>
> `dialog.part_9.md:31`: critical slowing down, variance, and autocorrelation are considered as possible warning signals.
>
> `dialog.part_18.md:3`: sandboxing is considered as moving detection into simulated futures.
>
> `dialog.part_18.md:13`: chaotic divergence limits predictive depth.
>
> `dialog.part_18.md:17`: simulation transfers detection but does not solve undecidable detection.
>
> `dialog.part_18.md:21`: action should not proceed by default beyond the sandbox's reliable range.
>
> `dialog.part_18.md:27`: Lyapunov time is a candidate tool for making range explicit.

Field-check comment:

> `field_check.md` node 8 gives `[FULL MATCH]` for Lyapunov-time/predictability and early-warning signals, while marking the concrete AGI sandbox policy as `[PARTIAL]`.

Working role: make sandboxing a finite-horizon instrument. The policy question becomes how to keep action within the measured horizon of prediction and rollback.

## Repository Metadata Bridge

This item is not part of the main bridge list at the current stage. It remains repository metadata until the publication form is clearer.

### From First Circle to Second Circle

Connects: raw dialogue, field check, public map, glossary discipline, publication form.

Related field-check nodes: all nodes, especially the final summary.

Dialogue trace:

> `dialog.part_21.md:3`: the first pass is named as a personal method/path and a possible source for later publication.
>
> `dialog.part_21.md:9`: the publication should be a map of the path, not a promise of a solution.
>
> `dialog.part_21.md:13`: the map must be checked against the existing field before publication.
>
> `dialog.part_21.md:15`: dialogue is treated as method, not merely wrapper.
>
> `dialog.part_22.md:3`: the stated aim is access to the path, not final truth or instruction.
>
> `dialog.part_22.md:9`: form can matter even when the content already exists elsewhere.
>
> `dialog.part_22.md:15`: sources must be checked before the public form is built.

Field-check comment:

> `field_check.md` summary gives no `[NO DIRECT SOURCE FOUND]` nodes and identifies likely narrow value only in bridges: `self-checking via committed past self`, `quantum anchor for agent commitment`, `semantic seam with explicit human-visible remainder`, `endogenous restraint as reflective anti-resource-grab`.

Working role: explain why the public work starts from the second circle: not to hide the path, but to avoid making the raw path carry claims it was not designed to carry.

## Current Human Decisions

- The nine technical bridges are accepted as a likely first set.
- Bridge 8 remains in the first public arc for now.
- The first-circle / second-circle bridge remains repository metadata for now.
- Bridge 3 uses standard terms first and keeps `reflective restraint` as the project label.
