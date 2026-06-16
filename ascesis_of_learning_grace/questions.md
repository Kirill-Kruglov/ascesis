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
