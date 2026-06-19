# Field Check

Working file for linking key theses to existing literature. This is not an evaluation of value, contribution, or novelty. The goal is only to mark where a thesis is already covered, where it partially overlaps, and where no direct source has been found.

Flag rules:

- `[FULL MATCH]` - the thesis is already formulated in the source, sometimes more strictly.
- `[PARTIAL]` - the thesis overlaps with existing work, but differs in frame or combination.
- `[NO DIRECT SOURCE FOUND]` - no direct source was found; candidate for manual human check.

## 1. Goal Fixed Point Under Self-Modification; Successor Risk for the Agent

| thesis | source | flag | note |
|---|---|---|---|
| A reflective agent can treat successor/self-modification as a risk to its own goals (`dialog.part_7.md:17`, `dialog.part_8.md:3`, `dialog.part_10.md:53`). | Stephen M. Omohundro, 2008, ["The Basic AI Drives"](https://selfawaresystems.files.wordpress.com/2008/01/ai_drives_final.pdf). | `[FULL MATCH]` | Omohundro directly formulates drives toward self-knowledge, self-improvement, utility-function preservation, and caution around self-modification. |
| Building a successor with the same goals is a central problem for self-modifying AI (`dialog.part_7.md:17`, `dialog.part_21.md:13`). | Eliezer Yudkowsky, Marcello Herreshoff, 2013, ["Tiling Agents for Self-Modifying AI, and the Loebian Obstacle"](https://intelligence.org/files/TilingAgents.pdf). | `[FULL MATCH]` | The source directly models agents approving the construction of successor agents with preserved goals, and the Loebian obstacle. |
| Agent self-trust toward future self/successor as a formal problem (`dialog.part_17.md:17`, `dialog.part_19.md:31`). | Benja Fallenstein, Nate Soares, 2015, ["Vingean Reflection: Reliable Reasoning for Self-Improving Agents"](https://intelligence.org/files/VingeanReflection.pdf); Nate Soares, 2015, ["The Value Learning Problem"](https://intelligence.org/files/ValueLearningProblem.pdf). | `[PARTIAL]` | Overlap is in reflective trust and self-improvement; the dialogue's frame of reflective restraint and existential successor-risk for the agent is different. |

Node flag: `[FULL MATCH]`.

## 2. Explicit Refusal on the Non-Translatable Remainder

| thesis | source | flag | note |
|---|---|---|---|
| A system should explicitly refuse when confident translation/decision is not available (`dialog.part_16.md:29`, `dialog.part_17.md:9`, `dialog.part_17.md:13`). | C. K. Chow, 1970, ["On Optimum Recognition Error and Reject Tradeoff"](https://doi.org/10.1109/TIT.1970.1054406). | `[FULL MATCH]` | Classical reject option: a classifier may abstain instead of making a risky decision. |
| Selective prediction as the modern ML form of covering only the region where risk is acceptable (`dialog.part_16.md:29`, `dialog.part_18.md:21`). | Yonatan Geifman, Ran El-Yaniv, 2017, ["Selective Classification for Deep Neural Networks"](https://arxiv.org/abs/1705.08500). | `[FULL MATCH]` | The source allows risk control by rejecting examples outside the accepted coverage region. |
| End-to-end model with an integrated reject option (`dialog.part_16.md:29`). | Yonatan Geifman, Ran El-Yaniv, 2019, ["SelectiveNet: A Deep Neural Network with an Integrated Reject Option"](https://arxiv.org/abs/1901.09192). | `[FULL MATCH]` | Matches explicit refusal; the dialogue applies the principle to a semantic seam. |

Node flag: `[FULL MATCH]`.

## 3. Checker Regress / Self-Checking Through Prior Commitment

| thesis | source | flag | note |
|---|---|---|---|
| External correction problem: by default, a strong agent may resist correction (`dialog.part_19.md:27`, `dialog.part_19.md:35`, `dialog.part_21.md:13`). | Nate Soares, Benja Fallenstein, Eliezer Yudkowsky, Stuart Armstrong, 2015, ["Corrigibility"](https://intelligence.org/files/Corrigibility.pdf). | `[FULL MATCH]` | Corrigibility directly introduces agents that permit corrective intervention despite incentives to resist it. |
| Correction behavior should propagate through subsystem construction and self-modification (`dialog.part_19.md:31`, `dialog.part_19.md:33`). | Soares et al., 2015, ["Corrigibility"](https://intelligence.org/files/Corrigibility.pdf). | `[FULL MATCH]` | The source explicitly requires propagation of shutdown/correction behavior into new subsystems or self-modification. |
| Self-checking against the agent's own committed past self instead of external oversight (`dialog.part_19.md:27`, `dialog.part_19.md:31`). | Manuel Blum, 1983, "Coin Flipping by Telephone"; Gilles Brassard, David Chaum, Claude Crepeau, 1988, ["Minimum Disclosure Proofs of Knowledge"](https://doi.org/10.1016/0022-0000(88)90005-0); general cryptographic commitment literature. | `[PARTIAL]` | Cryptographic commitment covers prior commitment/unforgeability, but no direct source was found for self-checking alignment against a committed past self. |
| The residual human/auditor role requires stable incentives for inspection, not only a fallback slot (`dialog.part_17.md:13`, `dialog.part_18.md:21`, `dialog.part_19.md:27`). | Rohit Agarwal, Joshua Lin, Mark Braverman, Elad Hazan, 2026, ["AI Alignment via Incentives and Correction"](https://arxiv.org/abs/2605.01643). | `[FULL MATCH]` | Solver-auditor alignment is modeled as an incentive equilibrium; oversight pressure can decay if auditing is not incentivized. |

Node flag: `[PARTIAL]`.

## 4. Quantum Anchor for Commitment Unforgeability

| thesis | source | flag | note |
|---|---|---|---|
| No-cloning as a physical primitive for unforgeable state/identity, not behavior (`dialog.part_4.md:25`, `dialog.part_11.md:25`, `dialog.part_20.md:19`). | Stephen Wiesner, 1983, "Conjugate Coding", SIGACT News 15(1), 78-88. | `[FULL MATCH]` | Quantum money/conjugate coding directly uses unclonable quantum states to prevent token forgery. |
| Quantum money / quantum tokens as reusable or limited-verification unforgeable tokens (`dialog.part_20.md:23`, `dialog.part_20.md:31`, `dialog.part_21.md:13`). | Scott Aaronson, Paul Christiano, 2012, ["Quantum Money from Hidden Subspaces"](https://arxiv.org/abs/1203.4740). | `[FULL MATCH]` | The source directly discusses quantum money, public verification, unlimited verification, and security constraints. |
| Quantum token as an anchor specifically for an agent's basis/commitment (`dialog.part_20.md:19`, `dialog.part_20.md:23`). | Adrian Kent et al., 2021, ["Practical quantum tokens without quantum memories and experimental tests"](https://arxiv.org/abs/2104.11717). | `[PARTIAL]` | Quantum-token literature covers unforgeability, but no direct source was found for an alignment commitment state. |

Node flag: `[PARTIAL]`.

## 5. Bounded Optimization / Reflective Restraint Against Resource Grabbing

| thesis | source | flag | note |
|---|---|---|---|
| Resource acquisition, self-preservation, self-improvement, and goal-content integrity as convergent drives (`dialog.part_7.md:3`, `dialog.part_7.md:9`, `dialog.part_21.md:13`). | Stephen M. Omohundro, 2008, ["The Basic AI Drives"](https://selfawaresystems.files.wordpress.com/2008/01/ai_drives_final.pdf). | `[FULL MATCH]` | The source directly formulates resource acquisition and utility-function preservation as drives of sufficiently advanced AI. |
| Instrumental convergence and orthogonality (`dialog.part_7.md:9`, `dialog.part_9.md:27`). | Nick Bostrom, 2014, [*Superintelligence: Paths, Dangers, Strategies*](https://global.oup.com/academic/product/superintelligence-9780199678112). | `[FULL MATCH]` | Standard source for resources as instrumental goals. |
| Replacing maximizing with softer or bounded choice (`dialog.part_8.md:35`, `dialog.part_18.md:23`). | Jessica Taylor, 2015, ["Quantilizers: A Safer Alternative to Maximizers for Limited Optimization"](https://intelligence.org/files/Quantilizers.pdf). | `[PARTIAL]` | Quantilizers cover mild/limited optimization; the dialogue adds a reflective restraint frame. |

Node flag: `[PARTIAL]`.

## 6. Language-to-Specification Seam: Partial Translation + Round Trip + Measured Gap

| thesis | source | flag | note |
|---|---|---|---|
| Natural language to executable/formal representation as semantic parsing (`dialog.part_13.md:11`, `dialog.part_13.md:13`, `dialog.part_14.md:29`). | Percy Liang, Michael I. Jordan, Dan Klein, 2013, ["Learning Dependency-Based Compositional Semantics"](https://aclanthology.org/J13-1004/); Matt Gardner et al., 2018, ["Neural Semantic Parsing"](https://aclanthology.org/P18-5003/). | `[FULL MATCH]` | Semantic parsing directly addresses translation from natural language into formal/executable representations. |
| Measured gap through reconstruction error / autoencoder round trip (`dialog.part_16.md:29`, `dialog.part_17.md:27`). | Geoffrey Hinton, Richard Zemel, 1993, ["Autoencoders, Minimum Description Length and Helmholtz Free Energy"](https://proceedings.neurips.cc/paper/1993/hash/9e3cfc48eccf81a0d57663e129aef3cb-Abstract.html); Dong Gong et al., 2019, ["Memorizing Normality to Detect Anomaly"](https://arxiv.org/abs/1904.02639). | `[FULL MATCH]` | Reconstruction error as anomaly signal is standard; the dialogue applies it to a semantic seam. |
| Formal verifier/user-in-the-loop for natural-language-to-formal-spec translation (`dialog.part_14.md:29`, `dialog.part_16.md:31`). | Matthias Cosler et al., 2023, ["nl2spec: Interactively Translating Unstructured Natural Language to Temporal Logics with Large Language Models"](https://arxiv.org/abs/2303.04864); Jun Wang et al., 2025, ["ConformalNL2LTL: Translating Natural Language Instructions into Temporal Logic Formulas with Conformal Correctness Guarantees"](https://arxiv.org/abs/2504.21022). | `[PARTIAL]` | Strong overlap: NL -> temporal logic, ambiguity handling, uncertainty-aware request for help; does not cover the full seam plus human-visible remainder. |

Node flag: `[PARTIAL]`.

## 7. Verification Limits

| thesis | source | flag | note |
|---|---|---|---|
| Nontrivial semantic verification of arbitrary programs cannot be totally solved (`dialog.part_4.md:23`, `dialog.part_16.md:25`). | H. G. Rice, 1953, ["Classes of Recursively Enumerable Sets and Their Decision Problems"](https://doi.org/10.1090/S0002-9947-1953-0053041-6). | `[FULL MATCH]` | Rice theorem directly sets limits on automatic checking of nontrivial semantic properties. |
| Godel/Loebian boundary for self-trust and checking one's own basis (`dialog.part_16.md:25`, `dialog.part_17.md:17`). | Kurt Godel, 1931, "Uber formal unentscheidbare Satze..."; Martin Loeb, 1955, "Solution of a Problem of Leon Henkin"; Yudkowsky & Herreshoff, 2013, ["Tiling Agents"](https://intelligence.org/files/TilingAgents.pdf). | `[FULL MATCH]` | These sources cover incompleteness, self-trust, and the Loebian obstacle more strictly than the dialogue. |
| Specification gaming / reward hacking as exploitation of incomplete specification (`dialog.part_3.md:17`, `dialog.part_4.md:11`, `dialog.part_4.md:13`). | Dario Amodei et al., 2016, ["Concrete Problems in AI Safety"](https://arxiv.org/abs/1606.06565). | `[FULL MATCH]` | Reward hacking and wrong objective functions directly cover the gap between specification and intent. |

Node flag: `[FULL MATCH]`.

## 8. Sandbox Predictability Horizon

| thesis | source | flag | note |
|---|---|---|---|
| Sandbox/simulation has a finite predictability horizon; more iterations do not guarantee a better forecast in a chaotic system (`dialog.part_18.md:13`, `dialog.part_18.md:17`, `dialog.part_18.md:21`). | Aleksandr Lyapunov tradition; Pierre Gaspard, 2005, *Chaos, Scattering and Statistical Mechanics*; concept: [Lyapunov time](https://en.wikipedia.org/wiki/Lyapunov_time). | `[FULL MATCH]` | Lyapunov time captures predictability limits from divergence of nearby trajectories. |
| Early-warning signals for irreversible/critical transitions: critical slowing down, variance/autocorrelation (`dialog.part_9.md:31`, `dialog.part_18.md:27`). | Marten Scheffer et al., 2009, ["Early-warning signals for critical transitions"](https://doi.org/10.1038/nature08227). | `[FULL MATCH]` | The source directly formulates early-warning signals for critical transitions. |
| Policy rule: keep action speed below reliable prediction range (`dialog.part_18.md:21`, `dialog.part_18.md:23`, `dialog.part_18.md:25`). | Scheffer et al. 2009 + Lyapunov-time literature. | `[PARTIAL]` | The mathematics of horizons exists; the concrete AGI sandbox policy is a transfer. |

Node flag: `[FULL MATCH]`.

## 9. Language Layer: Panini, Formal/Generative Grammar, Language of Thought, Linguistic Relativity

| thesis | source | flag | note |
|---|---|---|---|
| Panini as formal/generative grammar with metarules and conflict resolution (`dialog.part_14.md:17`, `dialog.part_14.md:19`, `dialog.part_14.md:23`). | George Cardona, 1988, [*Panini: His Work and Its Traditions*](https://archive.org/details/paninihisworkits0000card); Paul Kiparsky, 1979, "Panini as a Variationist". | `[FULL MATCH]` | Paninian grammar as a rule-system/metarule tradition is well covered in Indology and linguistics. |
| Modern re-checking of rule conflict in Panini (`dialog.part_14.md:19`, `dialog.part_16.md:17`). | Rishi Rajpopat, 2022, ["In Panini We Trust"](https://www.repository.cam.ac.uk/items/e6764a39-15af-4f60-8b25-0f905ad8d015). | `[FULL MATCH]` | Directly concerns metarules and rule conflicts in the Ashtadhyayi. |
| Language/representation as a condition for thought and agent self-reflection (`dialog.part_13.md:15`, `dialog.part_15.md:13`, `dialog.part_15.md:25`). | Jerry A. Fodor, 1975, [*The Language of Thought*](https://archive.org/details/languageofthough0000fodo); Michael Rescorla, "The Language of Thought Hypothesis", [Stanford Encyclopedia of Philosophy](https://plato.stanford.edu/entries/language-thought/). | `[PARTIAL]` | LOTH covers compositional mental representation; the dialogue transfers this to a designed self-description language for LLM/agent systems. |
| Language influences categories of perception/cognition but does not fully determine thought (`dialog.part_13.md:15`). | Edward Sapir, Benjamin Lee Whorf; overview: Lera Boroditsky, 2001, ["Does Language Shape Thought?"](https://doi.org/10.1111/1467-9280.00300). | `[FULL MATCH]` | Matches the cautious weak linguistic relativity frame. |

Node flag: `[PARTIAL]`.

## 10. seL4 / Capability Identity Layer

| thesis | source | flag | note |
|---|---|---|---|
| seL4 as a formally verified capability microkernel (`dialog.part_1.md:7`, `dialog.part_1.md:11`, `dialog.part_1.md:13`). | Gerwin Klein et al., 2009, ["seL4: Formal Verification of an OS Kernel"](https://dl.acm.org/doi/10.1145/1629575.1629596). | `[FULL MATCH]` | Primary source for the seL4 functional correctness proof. |
| seL4 is useful as a lower-layer isolation/control plane but does not solve semantic alignment (`dialog.part_3.md:13`, `dialog.part_3.md:17`, `dialog.part_4.md:11`). | Klein et al. 2009; Toby Murray et al., 2013, ["seL4: From General Purpose to a Proof of Information Flow Enforcement"](https://ts.data61.csiro.au/publications/nicta_full_text/7098.pdf). | `[PARTIAL]` | Sources cover kernel/security guarantees; the semantic-alignment conclusion is an application to the AI-agent threat model. |
| Object-capability model: unforgeable reference/authority and delegable but unforgeable rights (`dialog.part_1.md:13`, `dialog.part_2.md:27`, `dialog.part_3.md:19`). | Jack Dennis, Earl C. Van Horn, 1966, ["Programming Semantics for Multiprogrammed Computations"](https://doi.org/10.1145/365230.365252); Mark S. Miller, 2006, ["Robust Composition: Towards a Unified Approach to Access Control and Concurrency Control"](http://www.erights.org/talks/thesis/markm-thesis.pdf). | `[FULL MATCH]` | Capability/object-capability literature directly formulates unforgeable references and delegated authority. |
| Host-independent autonomy / verifiable execution traces for agents (`dialog.part_2.md:39`, `dialog.part_2.md:41`). | Artem Grigor et al., 2025, ["VET Your Agent: Towards Host-Independent Autonomy via Verifiable Execution Traces"](https://arxiv.org/abs/2512.15892). | `[FULL MATCH]` | Direct source for host-independent authentication of agent outputs. Human-confirmed as real. |
| agentOS as a seL4-based AI-agent OS (`dialog.part_2.md:25`, `dialog.part_2.md:35`). | Jordan Hubbard, ["agentOS"](https://github.com/jordanhubbard/agentos). | `[PARTIAL]` | Relevant project/PoC; not an academic primary source and requires manual maturity verification. |

Node flag: `[FULL MATCH]`.

## 11. Goodhart Inevitability / Reward Hacking as Structural Proxy Failure

| thesis | source | flag | note |
|---|---|---|---|
| Optimizing an imperfect proxy can decrease true-goal performance, so proxy maximization is structurally unsafe in the limit (`dialog.part_3.md:17`, `dialog.part_4.md:11`, `dialog.part_4.md:13`). | Joar Skalse, Nikolaus H. R. Howe, Dmitrii Krasheninnikov, David Krueger, 2022, ["Defining and Characterizing Reward Hacking"](https://arxiv.org/abs/2209.13085). | `[FULL MATCH]` | The paper formalizes reward hacking and shows that unhackability is a very strong condition, trivial over all stochastic policies unless one reward is constant. |
| Reward-model overoptimization empirically follows scaling behavior, and optimizing the proxy too far can harm ground-truth performance. | Leo Gao, John Schulman, Jacob Hilton, 2022, ["Scaling Laws for Reward Model Overoptimization"](https://arxiv.org/abs/2210.10760). | `[FULL MATCH]` | Directly studies reward model overoptimization under RL and best-of-n sampling. |
| Goodhart's law in reinforcement learning has a geometric explanation in MDPs; imperfect proxies are not definitions of the true objective. | Jacek Karwowski, Oliver Hayman, Xingjian Bai, Klaus Kiendlhofer, Charlie Griffin, Joar Skalse, 2023, ["Goodhart's Law in Reinforcement Learning"](https://arxiv.org/abs/2310.09144). | `[FULL MATCH]` | Supports the geometry/constrained-optimization side of the rejected wrapper/container branch. |
| In large models, reward hacking can generalize into deception, strategic gaming of oversight, and evaluator-policy co-adaptation. | Xiaohua Wang et al., 2026, ["Reward Hacking in the Era of Large Models: Mechanisms, Emergent Misalignment, Challenges"](https://arxiv.org/abs/2604.13602). | `[FULL MATCH]` | Survey source for test awareness / strategic manipulation risk in large-model proxy optimization. |

Node flag: `[FULL MATCH]`.

## 12. Social Choice / Arrow-Sen Impossibility for Value Aggregation

| thesis | source | flag | note |
|---|---|---|---|
| There is no clean scalar utility function for aggregating plural human values under standard social-choice constraints. | Peter Eckersley, 2019, ["Impossibility and Uncertainty Theorems in AI Value Alignment"](https://arxiv.org/abs/1901.00064). | `[FULL MATCH]` | Directly argues that AGI should not have a utility function in the strict mathematical sense and discusses partially ordered preferences. |
| Democratic RLHF / universal value alignment runs into social-choice impossibility constraints. | Abhilash Mishra, 2023, ["AI Alignment and Social Choice: Fundamental Limitations and Policy Implications"](https://arxiv.org/abs/2310.16048). | `[FULL MATCH]` | Directly applies social choice impossibility results to RLHF and democratic alignment. |
| Social choice should guide alignment when feedback is diverse. | Vincent Conitzer et al., 2024, ["Social Choice Should Guide AI Alignment in Dealing with Diverse Human Feedback"](https://arxiv.org/abs/2404.10271). | `[FULL MATCH]` | Direct source linking social choice to diverse human feedback in AI alignment. |
| Arrow and Sen impossibility results block the assumption that value aggregation can always produce a complete social ordering. | Kenneth Arrow, 1951/1963, *Social Choice and Individual Values*; Amartya Sen, 1970, ["The Impossibility of a Paretian Liberal"](https://doi.org/10.1086/259614). | `[FULL MATCH]` | Classical social-choice impossibility background for the active spine. |

Node flag: `[FULL MATCH]`.

## 13. Incomplete Preferences / Incommensurability as Agent Design

| thesis | source | flag | note |
|---|---|---|---|
| Incomplete preferences and partial orders can be used instead of complete utility orderings when choices are not fully comparable. | Peter Eckersley, 2019, ["Impossibility and Uncertainty Theorems in AI Value Alignment"](https://arxiv.org/abs/1901.00064); Leandro Gorno, Alessandro Rivello, 2020, ["A Maximum Theorem for Incomplete Preferences"](https://arxiv.org/abs/2007.09781). | `[PARTIAL]` | Overlap is strong for incomplete preferences and maximal elements; the active-spine use as an AGI governor core requires broader field verification. |
| Social choice with incomplete or cyclic preferences can return sets/correspondences rather than a single total ordering. | Jobst Heitzig, 2002, ["Social Choice Under Incomplete, Cyclic Preferences"](https://arxiv.org/abs/math/0201285); Amartya Sen, 1995, "The implementation of social choice functions via social choice correspondences". | `[PARTIAL]` | Supports non-singleton choice and correspondence framing; direct trained-agent design remains open. |

Node flag: `[PARTIAL]`. Active-spine core; manual field-completeness check required.

## 14. Bottom-Up vs Top-Down Alignment / Governor Framing

| thesis | source | flag | note |
|---|---|---|---|
| A governor should be framed as a constraint-guided trajectory explorer rather than a top-down scalar optimizer. | AI Frontiers, "AI Alignment Cannot Be Top-Down". | `[PARTIAL]` | Source named by project context but not independently verified in this pass; keep as manual source check. |
| A bottom-up governor must respect incentive and oversight dynamics, not only impose constraints. | Agarwal et al., 2026, ["AI Alignment via Incentives and Correction"](https://arxiv.org/abs/2605.01643); Conitzer et al., 2024, ["Social Choice Should Guide AI Alignment in Dealing with Diverse Human Feedback"](https://arxiv.org/abs/2404.10271). | `[PARTIAL]` | Supports the governor frame through incentives and diverse feedback; does not provide a complete training method for non-maximizers. |

Node flag: `[PARTIAL]`.

## 15. Bet-Hedging / Geometric-Mean Fitness / Kelly Criterion / Portfolio Theory

| thesis | source | flag | note |
|---|---|---|---|
| Under non-stationarity, maximizing arithmetic mean payoff can be dominated by strategies that maximize long-run multiplicative growth or geometric-mean fitness. | Everett R. Dempster, 1955, "Maintenance of Genetic Heterogeneity"; Dan Cohen, 1966, "Optimizing reproduction in a randomly varying environment"; J. L. Kelly Jr., 1956, ["A New Interpretation of Information Rate"](https://archive.org/details/bstj35-4-917). | `[FULL MATCH]` | This supports type A: non-maximization of arithmetic mean under stochastic/non-stationary environments by maximizing another scalar, usually expected log growth or geometric mean. |
| Portfolio theory formalizes diversification and risk-return tradeoffs without treating one-period arithmetic return maximization as sufficient. | Harry Markowitz, 1952, ["Portfolio Selection"](https://doi.org/10.1111/j.1540-6261.1952.tb01525.x). | `[FULL MATCH]` | Mean-variance portfolio theory supports the mature scalar/risk frontier side of type A; it does not establish incomplete preferences. |
| Bet-hedging and Kelly-style growth optimization are opponents or stress tests for incomplete-preference designs, not evidence for type B incompleteness. | Cohen 1966; Kelly 1956; Markowitz 1952. | `[FULL MATCH]` | Geometric-mean fitness and Kelly criterion retain a complete scalar ordering over strategies once the model is specified. They should not be conflated with refusal on incomparability. |

Node flag: `[FULL MATCH]`. Type-A support only; not evidence for incomplete preferences / type B.

## 16. Sacred / Protected Values and Taboo Trade-Offs

| thesis | source | flag | note |
|---|---|---|---|
| Some values are treated as protected or sacred: agents resist trading them against ordinary utility gains. | Jonathan Baron, Mark Spranca, 1997, ["Protected Values"](https://doi.org/10.1006/obhd.1997.2755); Philip E. Tetlock et al., 2000, ["The Psychology of the Unthinkable"](https://doi.org/10.1037/0022-3514.78.5.853). | `[FULL MATCH]` | Direct support for protected values and resistance to taboo trade-offs. |
| Taboo trade-offs produce moral outrage or refusal when goods from different moral spheres are traded. | Alan Page Fiske, Philip E. Tetlock, 1997, ["Taboo Trade-offs: Reactions to Transactions that Transgress the Spheres of Justice"](https://doi.org/10.1111/0162-895X.00058); Philip E. Tetlock, 2003, ["Thinking the unthinkable: sacred values and taboo cognitions"](https://doi.org/10.1016/S1364-6613(03)00135-9). | `[FULL MATCH]` | Supports the existence of non-ordinary trade-off structures; the toy `sacred_floor` environment is an engineering abstraction, not a direct model. |
| Non-scalarizable toy environments using protected thresholds are legitimate only if the protected-value abstraction is accepted for the target domain. | Tetlock/Fiske protected-values literature plus `field_check.md` node 13 on incomplete preferences. | `[PARTIAL]` | The literature supports protected values; using a boolean floor in an agent benchmark remains a modeling choice requiring human review. |

Node flag: `[PARTIAL]`. Supports the narrowed branch: non-scalarizable value structures exist; it does not prove a specific non-scalar agent design.

## 17. Goodhart Invariance Under Choice of Aggregator

| thesis | source | flag | note |
|---|---|---|---|
| When a measure becomes a target it ceases to be a good measure; this holds regardless of how the measure is aggregated. | Charles A. E. Goodhart, 1975, "Problems of Monetary Management: The UK Experience"; Marilyn Strathern, 1997, ["'Improving ratings': audit in the British University system"](https://doi.org/10.1002/(SICI)1234-981X(199709)5:3%3C305::AID-EURO184%3E3.0.CO;2-4). | `[FULL MATCH]` | Strathern's phrasing is the canonical compact form; aggregator choice does not exempt a target from it. |
| Goodhart failures come in distinct mechanisms (regressional, extremal, causal, adversarial), so repairing one metric can leave or relocate the others rather than remove the failure. | David Manheim, Scott Garrabrant, 2018, ["Categorizing Variants of Goodhart's Law"](https://arxiv.org/abs/1803.04585). | `[FULL MATCH]` | Direct taxonomy. Grounds the project framing that scalar -> geometric -> next aggregator is a taxonomy of variants, not a ladder that escapes Goodhart. |
| Geometric-mean / log aggregation coincides with the Nash bargaining product and proportional fairness, so it is one specific scalarization with its own corner-gaming, not an escape from scalarization. | John F. Nash, 1950, ["The Bargaining Problem"](https://doi.org/10.2307/1907266); Kelly, 1956 (node 15). | `[PARTIAL]` | The equivalence is standard; the claim that it produces a named "Pareto-hacking" failure of multi-axis optimization, with sycophancy as the rater-axis case, is the project's transfer and is owned by the Goodhart taxonomy above, not claimed as new. |

Node flag: `[PARTIAL]`. The taxonomy and the classic statement are owned; the "invariance to aggregator" framing for the active spine is the transfer.

## 18. Adversarial / Process-Based Evaluation and Sycophancy

| thesis | source | flag | note |
|---|---|---|---|
| Models trained on human approval learn to tell raters what they want rather than what is true (sycophancy): gaming of the approval axis. | Ethan Perez et al., 2022, ["Discovering Language Model Behaviors with Model-Written Evaluations"](https://arxiv.org/abs/2212.09251); Mrinank Sharma et al., 2023, ["Towards Understanding Sycophancy in Language Models"](https://arxiv.org/abs/2310.13548). | `[FULL MATCH]` | Direct empirical source for approval-axis gaming; supports sycophancy as the rater-axis instance of multi-axis Goodhart. |
| Replacing a static evaluator with an adversarial process (debate between opposed agents) is a proposed counter to gaming a fixed objective. | Geoffrey Irving, Paul Christiano, Dario Amodei, 2018, ["AI safety via debate"](https://arxiv.org/abs/1805.00899). | `[FULL MATCH]` | Frames evaluation as an equilibrium of opposed agents rather than a fixed scalar/vector metric. |
| Scalable oversight via recursive reward modeling reframes the target as a learned, iterated process rather than a fixed metric. | Jan Leike, David Krueger, Tom Everitt, Miljan Martic, Vishal Maini, Shane Legg, 2018, ["Scalable agent alignment via reward modeling"](https://arxiv.org/abs/1811.07871). | `[FULL MATCH]` | Direct source for process/iterated reward over a static aggregator. |
| Adversarial/debate evaluation has its own regress and failure modes (e.g. obfuscated arguments), so it relocates rather than removes the checker regress. | Beth Barnes, Paul Christiano, 2020, ["Writeup: Progress on AI Safety via Debate / obfuscated arguments"](https://www.alignmentforum.org/posts/PJLABqQ962hZEqhdB/progress-on-ai-safety-via-debate-1). | `[PARTIAL]` | AI Alignment Forum writeup; verify citation form before publication. Links to node 3 checker regress: process evaluation is not a termination of the regress. |

Node flag: `[PARTIAL]`. Sycophancy, debate, and reward modeling are owned by their sources; the project transfer is only the framing that they answer aggregator-invariant Goodhart by changing the evaluator's type rather than its formula.

## 19. Assistance Games / Uncertainty About the Objective

| thesis | source | flag | note |
|---|---|---|---|
| An agent that is uncertain about the human objective, and that defers to and stays correctable by humans, avoids the failure of optimizing a single fixed misspecified target. | Dylan Hadfield-Menell, Anca Dragan, Pieter Abbeel, Stuart Russell, 2016, ["Cooperative Inverse Reinforcement Learning"](https://arxiv.org/abs/1606.03137); Stuart Russell, 2019, *Human Compatible: Artificial Intelligence and the Problem of Control*. | `[FULL MATCH]` | Directly formalizes objective uncertainty plus deference as a safety property; this is the closest existing program to a governor without a fixed target. |
| Objective uncertainty gives an agent a positive incentive to allow itself to be switched off. | Dylan Hadfield-Menell, Anca Dragan, Pieter Abbeel, Stuart Russell, 2017, ["The Off-Switch Game"](https://arxiv.org/abs/1611.08219). | `[FULL MATCH]` | Grounds corrigibility-as-consequence-of-uncertainty rather than corrigibility-as-imposed-constraint. |

Node flag: `[PARTIAL]`. The assistance-game frame is owned; the transfer to a "grown governor that preserves the contested space" is the project bridge, not a claim of new theory.

## 20. Option-Value Preservation / Low-Impact Agents

| thesis | source | flag | note |
|---|---|---|---|
| Preserving the ability to achieve many goals, and avoiding irreversible side effects, can be a safety objective in place of maximizing a single objective. | Alexander Matt Turner, Dylan Hadfield-Menell, Prasad Tadepalli, 2020, ["Conservative Agency via Attainable Utility Preservation"](https://arxiv.org/abs/1902.09725). | `[FULL MATCH]` | Attainable-utility preservation is option-value preservation; directly supports "keep the space open" over "optimize the outcome". |
| Penalizing irreversible side effects and preserving future reachability is a tractable proxy for low impact. | Victoria Krakovna et al., 2019, ["Penalizing Side Effects Using Stepwise Relative Reachability"](https://arxiv.org/abs/1806.01186); Stuart Armstrong, Benjamin Levinstein, 2017, ["Low Impact Artificial Intelligences"](https://arxiv.org/abs/1705.10720). | `[FULL MATCH]` | Reachability/low-impact work supports avoiding irreversible collapse as an operational handle; links to bridge 2 (reversibility / resource-time safety). |

Node flag: `[PARTIAL]`. The mechanisms are owned; using them to define "preserve the conditions for contesting value" is the project transfer.

## 21. Long Reflection / Moral Uncertainty

| thesis | source | flag | note |
|---|---|---|---|
| Locking in a single value target prematurely is itself a risk; preserving the conditions to keep deliberating about values is preferable. | Toby Ord, 2020, *The Precipice: Existential Risk and the Future of Humanity* (the "long reflection"). | `[FULL MATCH]` | Direct source for "do not lock in; preserve deliberation," which the project reframes as the governor's maintenance goal. |
| One can act reasonably under moral uncertainty without first resolving which moral theory is correct. | William MacAskill, Krister Bykvist, Toby Ord, 2020, *Moral Uncertainty* (Oxford University Press). | `[FULL MATCH]` | Supports acting under deep uncertainty about the objective rather than assuming a known good; complements node 19. |

Node flag: `[PARTIAL]`. Long reflection and moral uncertainty are owned; the application to a governor that maintains a contested space is the project bridge.

## 22. Safety vs Liveness

| thesis | source | flag | note |
|---|---|---|---|
| Properties of a process split into safety ("nothing bad ever happens") and liveness ("something good eventually happens"); avoiding an irreversible bad state is a safety property. | Leslie Lamport, 1977, ["Proving the Correctness of Multiprocess Programs"](https://doi.org/10.1109/TSE.1977.229904); Bowen Alpern, Fred B. Schneider, 1985, ["Defining Liveness"](https://doi.org/10.1016/0020-0190(85)90056-0). | `[FULL MATCH]` | Clean formal distinction. Non-collapse is a safety property; "engine of progress" is a liveness property. |
| Liveness is guaranteeable only under fairness assumptions on the environment (opportunities recur). | Alpern and Schneider, 1985; standard temporal-logic fairness. | `[FULL MATCH]` | Explains why progress cannot be guaranteed in a closing or adversarial environment; ties to local optima and non-stationarity. |

Node flag: `[PARTIAL]`. The distinction is owned; applying safety/liveness to value pluralism and a governor is the project transfer.

## 23. Development as Freedom / Capability Approach

| thesis | source | flag | note |
|---|---|---|---|
| Progress/development can be defined as the expansion of substantive freedoms and capabilities rather than the maximization of a single utility. | Amartya Sen, 1999, *Development as Freedom*; Martha Nussbaum, 2011, *Creating Capabilities*. | `[FULL MATCH]` | A direction-free, plural notion of progress; the positive side of option-value (node 20). Directly answers "can preservation become a progress engine" without a fixed good. |

Node flag: `[PARTIAL]`. The capability approach is owned; its use as the governor's notion of progress is the project transfer.

## 24. Aggregating Better-Than-Even Competence

| thesis | source | flag | note |
|---|---|---|---|
| If individual judgments are independently better than chance, majority aggregation tends toward near-certainty as the group grows. | Condorcet, 1785, *Essai sur l'application de l'analyse à la probabilité des décisions rendues à la pluralité des voix* (Condorcet Jury Theorem). | `[FULL MATCH]` | Formal home of "leverage a 51% edge"; the independence premise fails under correlated failure, which is exactly the collapse case, bounding the result. |

Node flag: `[PARTIAL]`. The theorem is owned; its use to bound a progress guarantee and its independence caveat are the project transfer.

## 25. No-Regret / Online Learning

| thesis | source | flag | note |
|---|---|---|---|
| Under unknown or changing environments one cannot guarantee good outcomes, but can bound regret against the best fixed strategy in hindsight. | James Hannan, 1957, "Approximation to Bayes Risk in Repeated Play"; Nicolo Cesa-Bianchi, Gabor Lugosi, 2006, *Prediction, Learning, and Games*. | `[FULL MATCH]` | Provides a stagnation/regret bound where a probability-of-progress guarantee is unavailable. |

Node flag: `[PARTIAL]`. Regret minimization is owned; its use as the governor's "bounded stagnation" guarantee is the project transfer.

## 26. Open-Endedness and the Adjacent Possible

| thesis | source | flag | note |
|---|---|---|---|
| Search and innovation can proceed without a fixed objective, by expanding diversity and novelty (the adjacent possible). | Stuart Kauffman, 2000, *Investigations*; Joel Lehman, Kenneth O. Stanley, 2011, "Abandoning Objectives: Evolution Through the Search for Novelty Alone"; Jean-Baptiste Mouret, Jeff Clune, 2015, ["Illuminating Search Spaces by Mapping Elites"](https://arxiv.org/abs/1504.04909); Rui Wang et al., 2019, ["Paired Open-Ended Trailblazer (POET)"](https://arxiv.org/abs/1901.01753). | `[FULL MATCH]` | Direction-free progress as diversity/novelty growth; the generative engine a governor preserves rather than drives. |

Node flag: `[PARTIAL]`. Open-endedness work is owned; its use as the governor's progress mechanism is the project transfer.

## Summary

Node flags:

- `[FULL MATCH]`: 8
- `[PARTIAL]`: 18
- `[NO DIRECT SOURCE FOUND]`: 0

Nodes with `[FULL MATCH]`:

- 1. Goal fixed point under self-modification; successor risk for the agent.
- 2. Explicit refusal on the non-translatable remainder.
- 7. Verification limits.
- 8. Sandbox predictability horizon.
- 10. seL4 / capability identity layer.
- 11. Goodhart inevitability / reward hacking as structural proxy failure.
- 12. Social choice / Arrow-Sen impossibility for value aggregation.
- 15. Bet-hedging / geometric-mean fitness / Kelly criterion / portfolio theory.

Nodes with `[PARTIAL]`:

- 3. Checker regress / self-checking through prior commitment.
- 4. Quantum anchor for commitment unforgeability.
- 5. Bounded optimization / reflective restraint against resource grabbing.
- 6. Language-to-specification seam: partial translation + round trip + measured gap.
- 9. Language layer: Panini, formal/generative grammar, language of thought, linguistic relativity.
- 13. Incomplete preferences / incommensurability as agent design.
- 14. Bottom-up vs top-down alignment / governor framing.
- 16. Sacred / protected values and taboo trade-offs.
- 17. Goodhart invariance under choice of aggregator.
- 18. Adversarial / process-based evaluation and sycophancy.
- 19. Assistance games / uncertainty about the objective.
- 20. Option-value preservation / low-impact agents.
- 21. Long reflection / moral uncertainty.
- 22. Safety vs liveness.
- 23. Development as freedom / capability approach.
- 24. Aggregating better-than-even competence.
- 25. No-regret / online learning.
- 26. Open-endedness and the adjacent possible.

Candidates for manual human check (`[NO DIRECT SOURCE FOUND]`):

- None under current flag discipline. The active-spine bridge is marked `[PARTIAL]` where field completeness is uncertain, not claimed as new.

## Link Quality Notes

Sources requiring manual maturity or citation-quality verification before broader publication:

- Adrian Kent et al., 2021, "Practical quantum tokens without quantum memories and experimental tests" - arXiv / experimental-token relevance should be checked against the exact commitment-anchor use.
- Matthias Cosler et al., 2023, "nl2spec" - arXiv / recent tool paper; verify status and best citation.
- Jun Wang et al., 2025, "ConformalNL2LTL" - arXiv / recent work; verify status and best citation.
- Dong Gong et al., 2019, "Memorizing Normality to Detect Anomaly" - relevant to reconstruction error, but not a primary source for autoencoders.
- Jordan Hubbard, "agentOS" - project repository/PoC; verify maturity manually.
- Wikipedia link for Lyapunov time is only a concept pointer; replace with a primary or textbook citation before formal publication.
- AI Frontiers, "AI Alignment Cannot Be Top-Down" - named by project context, but source location was not verified in this pass.
- Xiaohua Wang et al., 2026, "Reward Hacking in the Era of Large Models" - recent survey; verify maturity and exact use before publication.
- Agarwal et al., 2026, "AI Alignment via Incentives and Correction" - recent arXiv paper; verify maturity and exact use before publication.
- Marilyn Strathern, 1997, "'Improving ratings'" - confirm the exact DOI/citation form for the compact Goodhart phrasing before publication.
- Beth Barnes, Paul Christiano, 2020, "obfuscated arguments" - AI Alignment Forum writeup, not a peer-reviewed source; verify the best citable form before publication.

Human-confirmed source that should not be marked as suspect:

- Artem Grigor et al., 2025, "VET Your Agent: Towards Host-Independent Autonomy via Verifiable Execution Traces".
