# Status — Current Frontier and Standing Discipline

Single live-state file. Read this first. It holds where the work is now and the
discipline that governs it. Everything else is either the stable map (changes
rarely) or the archive (frozen). History is in git, not restated here.

Last updated: 2026-06-19. Transition commits: `ca99c23` closed the
mechanical-superiority claim; `60b495b` credited the Goodhart-invariance and
adversarial-evaluation fields.

## Telos and scope

The top-level aim is to map a path by which humanity could build AGI/ASI and not
collapse after it. Discipline clause: this is a direction, not a claim of a
solution. The project maps honest bridges between existing fields; it does not
assert it can secure the transition, and the grandeur of the aim does not license
loose claims (discipline rule 7; the no-novelty genre). The largest Goodhart risk
in the project is at this level — letting the importance of the goal excuse loose
thinking — so claims here stay small and field-owned.

Working reframing of the target: because value is non-scalarizable both within a
person (incoherent, contradictory preferences) and across people (Arrow-Sen
aggregation limits), there is no coherent "highest good" to maximize. The
governor's job is therefore reframed from optimizing the good to preserving the
conditions under which plural value can keep being contested without irreversible
collapse — a maintenance goal under deep uncertainty about the objective, not an
optimization target. "Grown, not appointed" names the bottom-up, process-shaped
origin of such a governor; it does not by itself escape Goodhart (it relocates it
into the selection environment) and it requires built-in corrigibility and
legitimacy rather than a benevolent-dictator target. See the `structure.md`
candidate "Governor as Keeper of the Contested Space".

## Current spine (one line)

Non-scalarizable value structures may exist; the open work is whether they are
real and whether an agent can recognize them — not whether a non-scalar agent
outperforms a scalar one.

## What is closed (do not reopen as a performance claim)

- "A non-scalar / incomplete-preference agent mechanically outperforms a correct
  geometric-mean hedger." Refuted. Where non-scalarizability is stipulated
  (Test 02) the hedger is undefined, not defeated — close to a definition. Where
  the floor must emerge from dynamics (Test 06) the hedger survives strictly
  longer. See `rejected_branches.md` and `../experiments/validation_summary.md`.
  Per discipline rule 1, this is not to be reversed by trying another environment.

## Two live successors (the actual frontier)

- (a) Existence — about humans, descriptive. Are there genuinely non-tradeable
  value axes? (Tetlock/Baron protected/sacred values.) A negative answer — that
  apparent sacred values bend under tragic or secular framing — is publishable.
  Guard: must not become a runway back to an agent-superiority benchmark.

- (b) Detection / discipline — about the agent, as correctness not performance.
  Can an agent recognize a non-scalarizable regime and refuse to scalarize?
  Framed as reject-option correctness: abstain when scalarization is invalid, do
  not over-abstain when it is valid, measured against ground-truth validity
  labels rather than survival. Routes onto the existing selective-prediction
  spine (`field_check.md` node 2, bridge 4); keeps detection separate from
  alignment (node 13).

Framing that ties them together: Goodhart is invariant to the choice of
aggregator. Scalar → geometric → next only relocates the failure; geometric
aggregation invites Pareto-hacking, and sycophancy is its rater-axis case. The
responses that survive are not a better metric but removing axes from the trade
and detecting invalid scalarization — i.e. (a) and (b) seen from the optimizer
side. See the `structure.md` candidate "Goodhart Is Invariant to the Aggregator".

## Next concrete step

Validate the legitimacy of non-scalarizable environment classes (successor a)
before any new agent test. Do not search environment-space or aggregator-space
for a configuration where incompleteness or a non-scalar agent wins.

## Standing discipline (the harness)

1. No Goodhart over the research. A negative result is not license to retry
   environments, parameters, or metrics until something plays along. A new test
   must ask a new question, not re-verify an old one to the desired answer. This
   includes the design-level form: searching aggregator-space for a metric that
   "does not hack." Flag the temptation out loud.
2. Pre-registration before runs. `SPEC.md` fixes hypothesis, metrics, and failure
   criterion and is committed before the run. Never retro-edit a SPEC to match an
   outcome.
3. Negative results equal positive ones. Narrowing a branch is progress.
4. Symmetry of effort. If one side of a comparison is improved, log iterations in
   `results/run_manifest.json` so attention skew is visible.
5. Floor / incommensurability must be emergent from dynamics, not written into the
   objective, or the test is a tautology.
6. Preservation / authentication is not alignment. Keep that boundary sharp
   (bridges 7-8).
7. Novelty judgment goes through `field_check.md` against real literature, not
   through the team. When in doubt, flag toward "already known."

Roles: Claude holds the map and discipline; Codex executes; the human judges and
holds the remainder. The project's purpose is the honest path of knowing, not
novelty or recognition; disciplined narrowing outranks producing a win.

## Map and evidence

- Stable map: `structure.md` (bridges), `field_check.md` (field ownership),
  `references.md`, `glossary.md`.
- Evidence: `../experiments/validation_summary.md` (not restated here).
- Closed / superseded: `rejected_branches.md`, `archive/INDEX.md`.
- Durable open questions (non-frontier): `questions.md`.
