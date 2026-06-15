# Field Check

Working file for linking key theses in the dialogue to existing literature. This is not an evaluation of value, contribution, or novelty. The goal is only to mark where a thesis is already covered, where it partially overlaps, and where no direct source has been found.

Flag rules:

- `[FULL MATCH]` - the thesis is already formulated in the source, sometimes more strictly.
- `[PARTIAL]` - the thesis overlaps with existing work, but differs in frame or combination.
- `[NO DIRECT SOURCE FOUND]` - no direct source was found; candidate for manual human check.

## 1. Goal Fixed Point Under Self-Modification; Successor Risk for the Agent

| dialogue thesis | source | flag | note |
|---|---|---|---|
| A reflective agent can treat successor/self-modification as a risk to its own goals (`dialog.part_7.md:17`, `dialog.part_8.md:3`, `dialog.part_10.md:53`). | Stephen M. Omohundro, 2008, ["The Basic AI Drives"](https://selfawaresystems.files.wordpress.com/2008/01/ai_drives_final.pdf). | `[FULL MATCH]` | Omohundro directly formulates drives toward self-knowledge, self-improvement, utility-function preservation, and caution around self-modification. |
| Building a successor with the same goals is a central problem for self-modifying AI (`dialog.part_7.md:17`, `dialog.part_21.md:13`). | Eliezer Yudkowsky, Marcello Herreshoff, 2013, ["Tiling Agents for Self-Modifying AI, and the Loebian Obstacle"](https://intelligence.org/files/TilingAgents.pdf). | `[FULL MATCH]` | The source directly models agents approving the construction of successor agents with preserved goals, and the Loebian obstacle. |
| Agent self-trust toward future self/successor as a formal problem (`dialog.part_17.md:17`, `dialog.part_19.md:31`). | Benja Fallenstein, Nate Soares, 2015, ["Vingean Reflection: Reliable Reasoning for Self-Improving Agents"](https://intelligence.org/files/VingeanReflection.pdf); Nate Soares, 2015, ["The Value Learning Problem"](https://intelligence.org/files/ValueLearningProblem.pdf). | `[PARTIAL]` | Overlap is in reflective trust and self-improvement; the dialogue's frame of reflective restraint and existential successor-risk for the agent is different. |

Node flag: `[FULL MATCH]`.

## 2. Explicit Refusal on the Non-Translatable Remainder

| dialogue thesis | source | flag | note |
|---|---|---|---|
| A system should explicitly refuse when confident translation/decision is not available (`dialog.part_16.md:29`, `dialog.part_17.md:9`, `dialog.part_17.md:13`). | C. K. Chow, 1970, ["On Optimum Recognition Error and Reject Tradeoff"](https://doi.org/10.1109/TIT.1970.1054406). | `[FULL MATCH]` | Classical reject option: a classifier may abstain instead of making a risky decision. |
| Selective prediction as the modern ML form of covering only the region where risk is acceptable (`dialog.part_16.md:29`, `dialog.part_18.md:21`). | Yonatan Geifman, Ran El-Yaniv, 2017, ["Selective Classification for Deep Neural Networks"](https://arxiv.org/abs/1705.08500). | `[FULL MATCH]` | The source allows risk control by rejecting examples outside the accepted coverage region. |
| End-to-end model with an integrated reject option (`dialog.part_16.md:29`). | Yonatan Geifman, Ran El-Yaniv, 2019, ["SelectiveNet: A Deep Neural Network with an Integrated Reject Option"](https://arxiv.org/abs/1901.09192). | `[FULL MATCH]` | Matches explicit refusal; the dialogue applies the principle to a semantic seam. |

Node flag: `[FULL MATCH]`.

## 3. Checker Regress / Self-Checking Through Prior Commitment

| dialogue thesis | source | flag | note |
|---|---|---|---|
| External correction problem: by default, a strong agent may resist correction (`dialog.part_19.md:27`, `dialog.part_19.md:35`, `dialog.part_21.md:13`). | Nate Soares, Benja Fallenstein, Eliezer Yudkowsky, Stuart Armstrong, 2015, ["Corrigibility"](https://intelligence.org/files/Corrigibility.pdf). | `[FULL MATCH]` | Corrigibility directly introduces agents that permit corrective intervention despite incentives to resist it. |
| Correction behavior should propagate through subsystem construction and self-modification (`dialog.part_19.md:31`, `dialog.part_19.md:33`). | Soares et al., 2015, ["Corrigibility"](https://intelligence.org/files/Corrigibility.pdf). | `[FULL MATCH]` | The source explicitly requires propagation of shutdown/correction behavior into new subsystems or self-modification. |
| Self-checking against the agent's own committed past self instead of external oversight (`dialog.part_19.md:27`, `dialog.part_19.md:31`). | Manuel Blum, 1983, "Coin Flipping by Telephone"; Gilles Brassard, David Chaum, Claude Crepeau, 1988, ["Minimum Disclosure Proofs of Knowledge"](https://doi.org/10.1016/0022-0000(88)90005-0); general cryptographic commitment literature. | `[PARTIAL]` | Cryptographic commitment covers prior commitment/unforgeability, but no direct source was found for self-checking alignment against a committed past self. |

Node flag: `[PARTIAL]`.

## 4. Quantum Anchor for Commitment Unforgeability

| dialogue thesis | source | flag | note |
|---|---|---|---|
| No-cloning as a physical primitive for unforgeable state/identity, not behavior (`dialog.part_4.md:25`, `dialog.part_11.md:25`, `dialog.part_20.md:19`). | Stephen Wiesner, 1983, "Conjugate Coding", SIGACT News 15(1), 78-88. | `[FULL MATCH]` | Quantum money/conjugate coding directly uses unclonable quantum states to prevent token forgery. |
| Quantum money / quantum tokens as reusable or limited-verification unforgeable tokens (`dialog.part_20.md:23`, `dialog.part_20.md:31`, `dialog.part_21.md:13`). | Scott Aaronson, Paul Christiano, 2012, ["Quantum Money from Hidden Subspaces"](https://arxiv.org/abs/1203.4740). | `[FULL MATCH]` | The source directly discusses quantum money, public verification, unlimited verification, and security constraints. |
| Quantum token as an anchor specifically for an agent's basis/commitment (`dialog.part_20.md:19`, `dialog.part_20.md:23`). | Adrian Kent et al., 2021, ["Practical quantum tokens without quantum memories and experimental tests"](https://arxiv.org/abs/2104.11717). | `[PARTIAL]` | Quantum-token literature covers unforgeability, but no direct source was found for an alignment commitment state. |

Node flag: `[PARTIAL]`.

## 5. Bounded Optimization / Reflective Restraint Against Resource Grabbing

| dialogue thesis | source | flag | note |
|---|---|---|---|
| Resource acquisition, self-preservation, self-improvement, and goal-content integrity as convergent drives (`dialog.part_7.md:3`, `dialog.part_7.md:9`, `dialog.part_21.md:13`). | Stephen M. Omohundro, 2008, ["The Basic AI Drives"](https://selfawaresystems.files.wordpress.com/2008/01/ai_drives_final.pdf). | `[FULL MATCH]` | The source directly formulates resource acquisition and utility-function preservation as drives of sufficiently advanced AI. |
| Instrumental convergence and orthogonality (`dialog.part_7.md:9`, `dialog.part_9.md:27`). | Nick Bostrom, 2014, [*Superintelligence: Paths, Dangers, Strategies*](https://global.oup.com/academic/product/superintelligence-9780199678112). | `[FULL MATCH]` | Standard source for resources as instrumental goals. |
| Replacing maximizing with softer or bounded choice (`dialog.part_8.md:35`, `dialog.part_18.md:23`). | Jessica Taylor, 2015, ["Quantilizers: A Safer Alternative to Maximizers for Limited Optimization"](https://intelligence.org/files/Quantilizers.pdf). | `[PARTIAL]` | Quantilizers cover mild/limited optimization; the dialogue adds a reflective restraint frame. |

Node flag: `[PARTIAL]`.

## 6. Language-to-Specification Seam: Partial Translation + Round Trip + Measured Gap

| dialogue thesis | source | flag | note |
|---|---|---|---|
| Natural language to executable/formal representation as semantic parsing (`dialog.part_13.md:11`, `dialog.part_13.md:13`, `dialog.part_14.md:29`). | Percy Liang, Michael I. Jordan, Dan Klein, 2013, ["Learning Dependency-Based Compositional Semantics"](https://aclanthology.org/J13-1004/); Matt Gardner et al., 2018, ["Neural Semantic Parsing"](https://aclanthology.org/P18-5003/). | `[FULL MATCH]` | Semantic parsing directly addresses translation from natural language into formal/executable representations. |
| Measured gap through reconstruction error / autoencoder round trip (`dialog.part_16.md:29`, `dialog.part_17.md:27`). | Geoffrey Hinton, Richard Zemel, 1993, ["Autoencoders, Minimum Description Length and Helmholtz Free Energy"](https://proceedings.neurips.cc/paper/1993/hash/9e3cfc48eccf81a0d57663e129aef3cb-Abstract.html); Dong Gong et al., 2019, ["Memorizing Normality to Detect Anomaly"](https://arxiv.org/abs/1904.02639). | `[FULL MATCH]` | Reconstruction error as anomaly signal is standard; the dialogue applies it to a semantic seam. |
| Formal verifier/user-in-the-loop for natural-language-to-formal-spec translation (`dialog.part_14.md:29`, `dialog.part_16.md:31`). | Matthias Cosler et al., 2023, ["nl2spec: Interactively Translating Unstructured Natural Language to Temporal Logics with Large Language Models"](https://arxiv.org/abs/2303.04864); Jun Wang et al., 2025, ["ConformalNL2LTL: Translating Natural Language Instructions into Temporal Logic Formulas with Conformal Correctness Guarantees"](https://arxiv.org/abs/2504.21022). | `[PARTIAL]` | Strong overlap: NL -> temporal logic, ambiguity handling, uncertainty-aware request for help; does not cover the full seam plus human-visible remainder. |

Node flag: `[PARTIAL]`.

## 7. Verification Limits

| dialogue thesis | source | flag | note |
|---|---|---|---|
| Nontrivial semantic verification of arbitrary programs cannot be totally solved (`dialog.part_4.md:23`, `dialog.part_16.md:25`). | H. G. Rice, 1953, ["Classes of Recursively Enumerable Sets and Their Decision Problems"](https://doi.org/10.1090/S0002-9947-1953-0053041-6). | `[FULL MATCH]` | Rice theorem directly sets limits on automatic checking of nontrivial semantic properties. |
| Godel/Loebian boundary for self-trust and checking one's own basis (`dialog.part_16.md:25`, `dialog.part_17.md:17`). | Kurt Godel, 1931, "Uber formal unentscheidbare Satze..."; Martin Loeb, 1955, "Solution of a Problem of Leon Henkin"; Yudkowsky & Herreshoff, 2013, ["Tiling Agents"](https://intelligence.org/files/TilingAgents.pdf). | `[FULL MATCH]` | These sources cover incompleteness, self-trust, and the Loebian obstacle more strictly than the dialogue. |
| Specification gaming / reward hacking as exploitation of incomplete specification (`dialog.part_3.md:17`, `dialog.part_4.md:11`, `dialog.part_4.md:13`). | Dario Amodei et al., 2016, ["Concrete Problems in AI Safety"](https://arxiv.org/abs/1606.06565). | `[FULL MATCH]` | Reward hacking and wrong objective functions directly cover the gap between specification and intent. |

Node flag: `[FULL MATCH]`.

## 8. Sandbox Predictability Horizon

| dialogue thesis | source | flag | note |
|---|---|---|---|
| Sandbox/simulation has a finite predictability horizon; more iterations do not guarantee a better forecast in a chaotic system (`dialog.part_18.md:13`, `dialog.part_18.md:17`, `dialog.part_18.md:21`). | Aleksandr Lyapunov tradition; Pierre Gaspard, 2005, *Chaos, Scattering and Statistical Mechanics*; concept: [Lyapunov time](https://en.wikipedia.org/wiki/Lyapunov_time). | `[FULL MATCH]` | Lyapunov time captures predictability limits from divergence of nearby trajectories. |
| Early-warning signals for irreversible/critical transitions: critical slowing down, variance/autocorrelation (`dialog.part_9.md:31`, `dialog.part_18.md:27`). | Marten Scheffer et al., 2009, ["Early-warning signals for critical transitions"](https://doi.org/10.1038/nature08227). | `[FULL MATCH]` | The source directly formulates early-warning signals for critical transitions. |
| Policy rule: keep action speed below reliable prediction range (`dialog.part_18.md:21`, `dialog.part_18.md:23`, `dialog.part_18.md:25`). | Scheffer et al. 2009 + Lyapunov-time literature. | `[PARTIAL]` | The mathematics of horizons exists; the concrete AGI sandbox policy is a transfer. |

Node flag: `[FULL MATCH]`.

## 9. Language Layer: Panini, Formal/Generative Grammar, Language of Thought, Linguistic Relativity

| dialogue thesis | source | flag | note |
|---|---|---|---|
| Panini as formal/generative grammar with metarules and conflict resolution (`dialog.part_14.md:17`, `dialog.part_14.md:19`, `dialog.part_14.md:23`). | George Cardona, 1988, [*Panini: His Work and Its Traditions*](https://archive.org/details/paninihisworkits0000card); Paul Kiparsky, 1979, "Panini as a Variationist". | `[FULL MATCH]` | Paninian grammar as a rule-system/metarule tradition is well covered in Indology and linguistics. |
| Modern re-checking of rule conflict in Panini (`dialog.part_14.md:19`, `dialog.part_16.md:17`). | Rishi Rajpopat, 2022, ["In Panini We Trust"](https://www.repository.cam.ac.uk/items/e6764a39-15af-4f60-8b25-0f905ad8d015). | `[FULL MATCH]` | Directly concerns metarules and rule conflicts in the Ashtadhyayi. |
| Language/representation as a condition for thought and agent self-reflection (`dialog.part_13.md:15`, `dialog.part_15.md:13`, `dialog.part_15.md:25`). | Jerry A. Fodor, 1975, [*The Language of Thought*](https://archive.org/details/languageofthough0000fodo); Michael Rescorla, "The Language of Thought Hypothesis", [Stanford Encyclopedia of Philosophy](https://plato.stanford.edu/entries/language-thought/). | `[PARTIAL]` | LOTH covers compositional mental representation; the dialogue transfers this to a designed self-description language for LLM/agent systems. |
| Language influences categories of perception/cognition but does not fully determine thought (`dialog.part_13.md:15`). | Edward Sapir, Benjamin Lee Whorf; overview: Lera Boroditsky, 2001, ["Does Language Shape Thought?"](https://doi.org/10.1111/1467-9280.00300). | `[FULL MATCH]` | Matches the cautious weak linguistic relativity frame. |

Node flag: `[PARTIAL]`.

## 10. seL4 / Capability Identity Layer

| dialogue thesis | source | flag | note |
|---|---|---|---|
| seL4 as a formally verified capability microkernel (`dialog.part_1.md:7`, `dialog.part_1.md:11`, `dialog.part_1.md:13`). | Gerwin Klein et al., 2009, ["seL4: Formal Verification of an OS Kernel"](https://dl.acm.org/doi/10.1145/1629575.1629596). | `[FULL MATCH]` | Primary source for the seL4 functional correctness proof. |
| seL4 is useful as a lower-layer isolation/control plane but does not solve semantic alignment (`dialog.part_3.md:13`, `dialog.part_3.md:17`, `dialog.part_4.md:11`). | Klein et al. 2009; Toby Murray et al., 2013, ["seL4: From General Purpose to a Proof of Information Flow Enforcement"](https://ts.data61.csiro.au/publications/nicta_full_text/7098.pdf). | `[PARTIAL]` | Sources cover kernel/security guarantees; the semantic-alignment conclusion is an application to the AI-agent threat model. |
| Object-capability model: unforgeable reference/authority and delegable but unforgeable rights (`dialog.part_1.md:13`, `dialog.part_2.md:27`, `dialog.part_3.md:19`). | Jack Dennis, Earl C. Van Horn, 1966, ["Programming Semantics for Multiprogrammed Computations"](https://doi.org/10.1145/365230.365252); Mark S. Miller, 2006, ["Robust Composition: Towards a Unified Approach to Access Control and Concurrency Control"](http://www.erights.org/talks/thesis/markm-thesis.pdf). | `[FULL MATCH]` | Capability/object-capability literature directly formulates unforgeable references and delegated authority. |
| Host-independent autonomy / verifiable execution traces for agents (`dialog.part_2.md:39`, `dialog.part_2.md:41`). | Artem Grigor et al., 2025, ["VET Your Agent: Towards Host-Independent Autonomy via Verifiable Execution Traces"](https://arxiv.org/abs/2512.15892). | `[FULL MATCH]` | Direct source for host-independent authentication of agent outputs. Human-confirmed as real. |
| agentOS as a seL4-based AI-agent OS (`dialog.part_2.md:25`, `dialog.part_2.md:35`). | Jordan Hubbard, ["agentOS"](https://github.com/jordanhubbard/agentos). | `[PARTIAL]` | Relevant project/PoC; not an academic primary source and requires manual maturity verification. |

Node flag: `[FULL MATCH]`.

## Summary

Node flags:

- `[FULL MATCH]`: 5
- `[PARTIAL]`: 5
- `[NO DIRECT SOURCE FOUND]`: 0

Nodes with `[FULL MATCH]`:

- 1. Goal fixed point under self-modification; successor risk for the agent.
- 2. Explicit refusal on the non-translatable remainder.
- 7. Verification limits.
- 8. Sandbox predictability horizon.
- 10. seL4 / capability identity layer.

Nodes with `[PARTIAL]`:

- 3. Checker regress / self-checking through prior commitment.
- 4. Quantum anchor for commitment unforgeability.
- 5. Bounded optimization / reflective restraint against resource grabbing.
- 6. Language-to-specification seam: partial translation + round trip + measured gap.
- 9. Language layer: Panini, formal/generative grammar, language of thought, linguistic relativity.

Candidates for manual human check (`[NO DIRECT SOURCE FOUND]`):

- None. Under the honesty rule, every node has at least partial coverage in existing literature. The likely places for narrow bridge value, if any, are not isolated theses but combinations: `self-checking via committed past self`, `quantum anchor for agent commitment`, `semantic seam with explicit human-visible remainder`, `endogenous restraint as reflective anti-resource-grab`.

## Link Quality Notes

Sources requiring manual maturity or citation-quality verification before broader publication:

- Adrian Kent et al., 2021, "Practical quantum tokens without quantum memories and experimental tests" - arXiv / experimental-token relevance should be checked against the exact commitment-anchor use.
- Matthias Cosler et al., 2023, "nl2spec" - arXiv / recent tool paper; verify status and best citation.
- Jun Wang et al., 2025, "ConformalNL2LTL" - arXiv / recent work; verify status and best citation.
- Dong Gong et al., 2019, "Memorizing Normality to Detect Anomaly" - relevant to reconstruction error, but not a primary source for autoencoders.
- Jordan Hubbard, "agentOS" - project repository/PoC; verify maturity manually.
- Wikipedia link for Lyapunov time is only a concept pointer; replace with a primary or textbook citation before formal publication.

Human-confirmed source that should not be marked as suspect:

- Artem Grigor et al., 2025, "VET Your Agent: Towards Host-Independent Autonomy via Verifiable Execution Traces".
