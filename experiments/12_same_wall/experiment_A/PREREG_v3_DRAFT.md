# Experiment A — PREREG v3 DRAFT (SUPERSEDED by PREREG_v4_DRAFT.md; kept for the review trail)

> Supersedes `PREREG_DRAFT.md` (v2). Status: DRAFT for the final
> two-reviewer attack (Opus 4.8, GPT 5.5/5.6) and the author's sign-off.
> Lock via `gate_harness.prereg` after both. Concrete values below are
> PROPOSED LOCKS — attack them; after lock nothing moves.

## 0. What phase 0 established (inputs, not claims of this run)

Twelve scouts, all falls recorded in
[`12-the-same-wall.md`](../../../ontology/lines/12-the-same-wall.md):
the token channel distinguishes genealogies at scout scale ((A,Gt)
DEP(token), (A,main) CLEAN, scout 11); true independent convergence is
not written off as glue (C7 live); only correlated falls testify
(H-theorem, scout 12); dependence is readable inside a stress
**visibility window** (deterministic traps strong at 0.160; mild noise
moderate; high noise decoheres); the per-instance null absorbs
world-forced attractors; the clean-room build exposed and fixed our
truth-label bias (extensional truths).

## 1. Question (two-axis, no conflation)

For pairs of order-finding procedures on one task, with destination
agreement (axis D) and residual path dependence (axis P) measured
separately:

> **K2 (central).** Does the locked instrument distinguish the two
> registered GENEALOGIES of the same theorem-glued destination —
> flagging the derived pair (A, Gt) as DEPENDENT\* while clearing the
> clean-room pair (A, main) as CLEAN — with both pairs agreeing on
> correct destinations on the core strata (C7 inside K2)?

v3 measures dependence *under registered observables*; it never proves
construction identity, nor world truth (scope, §7).

## 2. Fixed objects `[LOCK]`

- **Worlds and extensional truths** (truth = predictive adequacy over
  the full word space, not any language's view):

  | stratum | family | params | truth | role |
  |---|---|---|---|---|
  | cycle | GCycle(n) | n ∈ 17..40 | n | core |
  | alias | GAliasCycle(n,q) | n ∈ {20,24,30,36}, q proper divisor ≥ 4 | n | core |
  | noisy-mild | GCycle(n, ε) | ε ∈ 0.02..0.12 | n | visibility window |
  | qtrap | QuotientTrap(n=q·k, q ∈ 5..9, k ∈ 3..5, frac 0.6) | — | n | window, deterministic discriminator |
  | wobble | GWobble(n) | n ∈ 17..40 | **None** | non-group; abstain correct |
  | lollipop | GLollipop(t,c) | t ∈ 5..12, c ∈ 12..26 | **None** | non-group |
  | nonstat | GNonstationary(n1,n2,switch) | 15..26 / 27..40 / 60..200 | **None** | non-group |

- **Dual-implementation ground truth.** Oracle-T (anonymous
  permutation/transition table) and Oracle-N (net arithmetic),
  cross-checked exhaustively on all strata instances over a preregistered
  word battery before the run; the EVALUATOR consumes Oracle-T; languages
  never import evaluator helpers. Mismatch in cross-check ⇒ run aborts
  (infrastructure failure, not an outcome).
- **Interface I.** `oracle(u, v) -> bool`, words over {R,L};
  `cap_calls = 400`; seed in, own PRNG. Fixed for this experiment.
- **Perturbation ensemble (world-side only).** {id, bp+1, bp+3, rev,
  noise-reseed}. Budget stays out (contact parameter, scout 06).
- **Naive destination detector (K1 arm).** Fires "world wall at m" iff
  both languages return VAL with the same m on the id-perturbation
  majority. Input signature: final claims only. It never sees journals.
- **Null world (K3).** Inconsistent oracle: answers drawn iid Bernoulli(
  0.5) per query from the oracle seed — designation only; the traces v3
  consumes are the languages' own probe logs, which differ per language
  as always. The naive detector must not stabilize on agreement.

## 3. Registered pairs and genealogies `[LOCK]`

| pair | provenance (protocol file) | registered status | expectation |
|---|---|---|---|
| (A, A′-clone) | same code + padding | dependent (clone) | C1: DEPENDENT\*; UNKNOWN = FAIL |
| (A, Gt) | Gt derived from A (Cayley translation) | dependent (derived) | K2a: DEPENDENT\* |
| (A, main) | clean room: GPT 5.6, web, different account; sha256 40c2493b…; common causes W, I only | independent | K2b/C7: CLEAN + destination-same ≥ 6/8 core-cycle instances |
| (W, P), (M, P) | ours, mechanism-disjoint by construction | independent | C2: CLEAN; UNKNOWN ⇒ run INCONCLUSIVE |
| (main, ref1) | shared helpers inside the received file | dependent, **measured blind-spot instance** (scouts 11–12) | REPORTED only: expected CLEAN; if it flags — surprise requiring diagnosis, not a pass |

## 4. Instrument v3 (final assembly) `[LOCK]`

1. **Admission per channel.** Token: token-world-sensitivity ≥ 0.30.
   Journal: non-degenerate world-sensitive fingerprint (variation ≥ 0.05
   across world-side perturbation pairs). Inadmissible pairs cannot
   satisfy any K/C; they are reported as INADMISSIBLE(channel).
2. **Token channel.** M1 (same wrong value | both wrong) excess over the
   analytic per-instance null; instance-level significance; matched AND
   crossed seeds. Margin 0.05; significance mean > 2.6·se (Bonferroni-5
   heuristic; final value bound to the OC gate, §8).
3. **Journal channel.** Schedule co-adaptation (LCP fingerprints over
   world-side perturbation pairs, emitted probes); reference field =
   max(0, q75) over reference units {W, M, P, received-family(rep
   ref1)}, leave-candidate-family-out, < 3 pairs ⇒ UNKNOWN; margin 0.10;
   matched AND crossed.
4. **Axes and labels.** Axis D: DESTINATION_SAME / DIFFERENT / NA
   (id-perturbation majorities). Axis P: DEPENDENT(token) /
   DEPENDENT(journal) / DEPENDENT(unresolved = both) /
   CONTACT_SCHEDULE / CLEAN / UNKNOWN / INADMISSIBLE. Union of channels;
   no combined p-value; no strength ranking from double hits. World-
   credit is NEVER emitted by the instrument (scope).
5. **UNKNOWN propagation.** K2a/K2b: UNKNOWN = FAIL. C1: UNKNOWN = FAIL.
   C2: UNKNOWN ⇒ run INCONCLUSIVE. Reported-only rows never gate.

## 5. Kill conditions and controls `[LOCK]`

- **K1 (regression arm, unit-test status — not citable epistemology).**
  The naive detector must fire on BOTH (A,Gt) and (A,main) on core cycle
  strata (destination-blind to genealogy), and must NOT fire on the null
  world (K3). Failure ⇒ harness defect, run aborts.
- **K2a.** (A, Gt) ∈ DEPENDENT\*. **K2b.** (A, main) = CLEAN on both
  channels AND destination-same ≥ 6/8 core-cycle instances (C7). PASS =
  both; UNKNOWN anywhere = FAIL of that arm.
- **K3.** Null world: naive detector agreement rate ≤ 1/8 instances; v3
  behavior recorded, never used to rescue K1/K2.
- **C1, C2** as in §3. **C3** admission reporting for every registered
  pair. **C4** no source overclaim — locked wording: *"v3 detects
  dependence under registered observables; it does not prove
  construction identity, clonehood, Cayley-interface equivalence, or
  world truth."* **C5** pool, references, rules locked herein. **C6**
  null-world sanity (K3).

## 6. Preregistered outcome table `[LOCK]`

| K1 | K2a | K2b | C1 | C2 | Reading |
|---|---|---|---|---|---|
| P | P | P | P | P | Full clean: genealogies distinguished; C7 held; instrument survives Experiment A |
| P | P | F | P | P | Instrument conservative: derived caught, true convergence written off — the B1-class failure, instrument implicated |
| P | F | P | P | P | Instrument blind to derivation under lock-scale statistics — K2a effect did not survive scaling; phase-0 result not confirmed |
| P | F | F | P | P | Channels measure neither: Experiment A's premise falls (the GPT alternative reading wins at scale) |
| P | · | · | F | · | Instrument implicated: clone missed — run-level FAIL |
| P | · | · | · | F | Instrument implicated: over-flags negatives — run-level FAIL |
| F/U | · | · | · | · | Harness defect / inconclusive: abort, fix, re-lock (no outcome claimed) |
| · | U | · | · | · | K2a FAIL (UNKNOWN is not success) |
| · | · | U | · | · | K2b FAIL |
| · | · | · | · | U | Run INCONCLUSIVE (negative floor not established) |

## 7. Scope and `not_tested_against` (published with any outcome)

Locked scope sentence: **INDEPENDENT/CLEAN means clean under the
registered token and journal observables, given the declared reference
constructions and this world/perturbation family. It is not proof of
absence of latent shared implementation, and no world-credit is
implied.**

`not_tested_against`:
- Shared implementation with decorrelated surface (Codex residual hole;
  now with a measured instance: (main, ref1), scouts 11–12) — only
  correlated falls testify.
- Dependence outside the visibility window (too-competent or
  noise-decohered regimes) — measured, scouts 11–12.
- Semantic shared preprocessors beyond prefix hygiene (measured field
  bite +0.044 at scout-10 strength).
- Clone vs Cayley-channel separation (interface arm, later; C4 forbids
  the claim).
- Adversarial pool composition beyond the locked pool; adaptive
  languages optimized against the detector; changed interface I;
  generalization beyond this family (holdout, §9); mode-split M3/M4 as
  a positive channel; strength ranking from double hits.

## 8. Statistical plan `[LOCK]`

- Instances: 8 per stratum (7 strata). Seeds: K = 8. CAP = 400.
  Perturbations: 5. Core metrics therefore satisfy `seed_policy`
  (≥ 20 independent units at instance level: 56 instances).
- Sanity seed: one disjoint seed (fixed at lock) runs the full pipeline
  before the multi-seed run; no threshold changes after it.
- **OC gate (pre-lock, its own artifact).** A simulation study on
  synthetic pairs with known status must measure, under the exact locked
  rules: FPR ≤ 0.05 on independent pairs; power ≥ 0.8 on derived-class
  pairs over the locked strata mix; MCSE reported. If the OC gate fails,
  redesign happens BEFORE lock (allowed); after lock nothing moves.
- Multiple comparisons: the gating hypotheses are exactly K2a, K2b, C1,
  C2 (4 tests); significance multiplier 2.6·se locked pending the OC
  gate's empirical FPR; if OC shows FPR > 0.05, the multiplier rises to
  the smallest value achieving FPR ≤ 0.05 and is then locked.

## 9. Post-lock holdout (required for any confirmation claim)

After the locked run, a NEW world family and shams are commissioned from
a fresh clean-room agent (web, different account, no metric internals,
no sight of this prereg) and run under the same locked rules with no
changes to v3. The locked run alone is internal validation
(development-set caveat, GPT review §5); only the holdout supports a
confirmation claim.

## 10. What kills Experiment A (any one)

- (A, main) flagged (true convergence written off) or (A, Gt) cleared —
  with UNKNOWN counted as the FAIL of its arm, never as success.
- Clone missed; independent negatives flagged; harness/oracle
  cross-check failure treated as anything but abort.
- Any report phrase upgrading "did not detect dependence" into "proved
  independence/dependence type" (C4).
- Post-hoc threshold or pool changes after lock.
