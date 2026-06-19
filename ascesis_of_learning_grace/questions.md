# Questions

Open questions found after rebuilding `structure.md` and checking it for integrity, completeness, and noncontradiction.

## Structural Questions

1. Should the project keep nine technical bridges as the public structure, or should bridge 8 be visually marked as "technical appendix candidate" even while remaining in the first arc?

2. Should `From Verified Isolation to Semantic Alignment` be the first chapter, or should `From Containment to Resource-Time Safety` come first and use seL4 as a motivating case inside it?

3. Should the repository metadata bridge eventually become a preface, an afterword, or a separate document about method?

## Terminology Questions

1. `Reflective Restraint` is clear as a local working title, but it overlaps with standard terms without being identical to them. The closest standard terms are `goal-content integrity`, `reflective stability`, `Vingean reflection`, `tiling agents`, `mild optimization`, `quantilization`, and `satisficing`. Which of these should be named first when the bridge becomes prose?

2. The term `ascesis` is operationally defined in `glossary.md`, but it can still read as religious or poetic. Should public-facing chapter titles use `restraint`, `bounded optimization`, or `reflective restraint` first, with `ascesis` reserved for the glossary and later interpretive sections?

3. The term `seam` is useful locally, but it maps onto several fields: semantic parsing, formal specification, selective prediction, reconstruction error, and verifier-in-the-loop translation. Should `seam` remain the main term, or should chapters use field-standard names and introduce `seam` as the project label?

## Potential Contradictions

1. README says the raw dialogue is not published in the initial commit, while `structure.md` now contains dialogue inserts. This is not a direct contradiction if the inserts are treated as short internal anchors, but it weakens the clean boundary. Decide whether short excerpts are acceptable public material or whether they should be paraphrased without quoting.

2. The project discipline says no claims of novelty. `structure.md` says bridges connect areas that are usually separate. This should remain phrased as a working organization choice, not as a claim that no literature connects them.

3. Bridge 8 stays in the first public arc, but the README says not to introduce quantum material first. This is consistent as long as bridge 8 appears late and remains narrow, but it should not be moved earlier.

4. `field_check.md` uses some sources that may need stricter verification later, especially recent arXiv entries and project repositories. This does not block the skeleton, but it should be tracked before a public release beyond the first map.

## Naive Assumptions To Watch

1. That explicit refusal always transfers safely from classifiers to agentic systems. The transfer depends on refusal happening before action and on defaults being inert.

2. That round-trip consistency measures semantic preservation strongly enough for safety. It can miss meaning-preserving-looking substitutions.

3. That sandbox horizons can be measured well enough for real agent decisions. The dialogue itself flags recursion: simulating a stronger agent may require a simulator of comparable capability.

4. That commitments solve correctness. They preserve or authenticate a reference; they do not establish that the reference is aligned.

5. That language-of-thought or Paninian grammar gives access to an LLM's actual internal representation. The current realistic target is a protocol of self-description, not direct control of internal cognition.

## Active Spine Questions

1. How to train a non-maximizer, not wrap a maximizer?

This is the central unresolved question of the current spine. Quantilizers, satisficers, incomplete preferences, and social-choice correspondences provide theory-side handles, but the project does not yet have a method for training an LLM/agent core whose learned policy is non-maximizing rather than externally constrained at inference time.

2. Can incomplete preferences remain stable under learning, reflection, and deployment pressure?

The current spine uses incomplete preferences / incommensurability as the design direction, but field completeness has not been manually verified. The open issue is whether incompleteness can be maintained as an operational property rather than collapsing into an implicit scalar proxy.

3. Bottom-up vs top-down governor: does the governor grow the constraint frame or impose it?

The active spine requires a bottom-up AGI governor: a constraint-framed trajectory explorer shaped by plural feedback and oversight incentives. The unresolved question is how to prevent the frame from becoming a top-down hidden utility function under another name.

4. Which bridges should be marked closed rather than open?

Bridge 8 remains `[OPEN QUESTION]` in `structure.md` because the narrow unforgeable-state role is not the same as the rejected branch `quantum-as-general-answer`. A human review should decide whether that narrow bridge belongs in the main public arc, a technical appendix, or only in `rejected_branches.md`.

## Bet-Hedging Challenge

1. Does geometric-mean optimization (bet-hedging) make incomplete preferences unnecessary?

This is now a central challenge to the active spine. Bet-hedging is mature and still scalar: it replaces arithmetic-mean maximization with geometric-mean / log-growth optimization under non-stationarity. The open question is whether incomplete preferences add anything operationally beyond what a well-specified growth optimizer already gives.

2. Is there an environment class where incompleteness strictly wins?

Answered negatively for the emergent case. Test 06 asked the reproduction floor to emerge from demography rather than from a stipulated label, and the corrected geometric-mean hedger survived strictly longer than the incomplete-preference governor on held-out seeds (median collapse 180 vs 119; pairwise win rate 0.23 against a pre-registered 0.55 threshold). Test 02 only diverges where the environment declares no valid currency, which is stipulation rather than dynamics. Per the project harness this negative is not to be reversed by searching for a friendlier ecology profile; it is published as a real finding. The performance question is therefore closed; what remains is existence and detection, not superiority.


## Narrowed Active Spine After Experiment Validation

After Test 02 (toy) and Test 06 (emergent witness), the branch is no longer "incomplete beats hedging." That performance claim is closed: the hedger wins or ties where a scalar is available (Test 02) and wins where the floor must emerge from dynamics (Test 06). The remaining work splits into an existence question (about humans) and a detection question (about the agent), neither of which is a survival contest.

1. Existence: which value structures are genuinely non-scalarizable?

The live claim is only "some value structures have no valid scalar currency," not "a non-scalar agent survives longer." Sacred/protected values (Tetlock, Baron) are the first candidate class, but their use as benchmark floors requires human review, and a negative answer — that apparent sacred values bend under tragic or secular framing — is publishable. This question must not become a runway back to an agent-superiority benchmark.

2. Detection / discipline: can an agent recognize a non-scalarizable regime and refuse to scalarize?

This is the agent-side successor, framed as reject-option correctness rather than performance: does the agent abstain when scalarization is invalid, and avoid over-abstaining when it is valid, measured against ground-truth validity labels rather than survival. It routes onto the project's existing selective-prediction spine (`field_check.md` node 2, bridge 4) and keeps detection separate from alignment (node 13).

3. How fragile is non-scalar behavior under instruction pressure and self-modification?

Experiment 03 suggests instruction-following models prioritize forced-choice framing over preserving incomparability. Experiment 05 suggests partiality may survive when maintaining a complete order is costly, so the earlier collapse was partly sensitive to the free-tie-breaker assumption.
