# Questions

Durable open questions about structure, terminology, contradictions, and assumptions —
the slow-moving kind that survive across sessions. The live research frontier (current
spine, what is closed, the two successors, the next step) lives in `status.md`, not here,
so this file does not need updating every time the frontier moves.

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

## Research Frontier

The live spine, what is closed, the two successors (existence of non-tradeable axes;
detection of invalid scalarization), and the next concrete step now live in `status.md`.
They are intentionally not duplicated here, so this file does not accumulate sediment as
the frontier moves. For the experimental evidence behind the current state, see
`../experiments/validation_summary.md`. For closed branches and superseded framings, see
`rejected_branches.md` and `archive/INDEX.md`.
