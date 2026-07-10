# Experiment A — PREREG v4 DRAFT (NOT LOCKED)

> Supersedes `PREREG_v3_DRAFT.md`. Status: DRAFT for review round 3
> (X, Y) and the author's sign-off; lock via `gate_harness.prereg`
> afterwards. Every choice below carries its provenance (scout or review
> that forced it). Proposed lock values are concrete; attack them.

## 0. Inputs from phase 0 + OC-tune (facts of the forge, not claims)

Sixteen scouts, three review rounds, six clean-room builds. Established:
the token and journal channels distinguish genealogies at scout scale
(sc.11); only correlated falls testify (sc.12); the blade —
co-adaptation surviving into correlated failure — separates ancestry
from the world's one door and passes its own validity gate (sc.13); the
common-prior effect is real and graded — **coupling follows the
converged probe channel + validation discipline, not family or declared
mechanism** (A~opusA 24/24, A~grok 12/24, A~gemini 0/24; sc.C8);
same-author pairs are not certified independent (sc.16); the channels'
applicability domain is schedule-adaptive, value-failing languages
(sc.14–15); the reference field must be adaptivity-matched (sc.15); PM
controls must be context-seeded (sc.15). The scout window is empty at
scout n by power arithmetic; window selection is delegated to the
lock-scale OC (sc.15 E5, sc.16).

## 1. Question (two axes, never merged)

> **K2.** Within the locked stress family, does the instrument assign
> different residual-dependence labels to one registered DERIVED pair
> and one registered CLEAN-ROOM CROSS-PRIOR pair, while both preserve
> destination agreement on core strata?

Claim wording locked (review Y, verbatim): *"Within the locked stress
family, v3 assigned different residual-dependence labels to one
registered derived pair and one registered clean-room pair, while
preserving destination agreement."* No "genealogies distinguished"
simpliciter; no world-credit; no construction-identity claims (C4).

## 2. Fixed objects `[LOCK]`

- **Worlds, extensional truths** (predictive adequacy over the word
  space, no language's view): cycle n∈17..40 → n; alias (n, q proper
  divisor ≥4) → n; noisy-mild ε∈0.02..0.12 → n; qtrap (q∈5..9, k∈3..5,
  frac .6) → n; wobble/lollipop/nonstat → None (abstain correct).
  Final strata set = the lock-scale OC-tune's window (§8); the lattice
  from which it selects is THIS list, fixed now.
- **Dual oracle.** Oracle-T (anonymous transition table) and Oracle-N
  (net arithmetic where defined), cross-checked on a preregistered
  finite word battery per stratum (bounded length; the word "exhaustive"
  is not used; battery sufficiency is NOT claimed beyond its bounds —
  review Y §4.6). Evaluator consumes Oracle-T. Mismatch ⇒ abort
  (infrastructure), from the pre-listed abort conditions only.
- **Interface I.** `oracle(u,v)→bool`, words over {R,L}, cap_calls=400,
  seed in / own PRNG. Perturbations (world-side only): id, bp+1, bp+3,
  rev, noise-reseed.
- **Naive destination detector** (K1 regression arm): fires iff both
  final claims are VAL with equal m (id-perturbation majority). Sees
  claims only; input signature fixed; never sees journals.
- **Null world** (K3): per-query iid Bernoulli(0.5) oracle. The
  observable that differs from real worlds: the languages' own answer
  streams (destinations do not stabilize).

## 3. Registered pairs `[LOCK]` (provenance file: PROVENANCE_PROTOCOL.md)

| pair | class (provenance) | registered expectation |
|---|---|---|
| (A, A′) | clone (same code + padding) | C1 positive: DEPENDENT\*; UNKNOWN = FAIL |
| (A, Gt) | derived (Cayley translation) | **K2a**: DEPENDENT\* |
| (A, gptA-main) | clean room, cross-prior (0/24 channel overlap) | **K2b/C7**: CLEAN + destination-same ≥ 6/8 core-cycle instances |
| (A, opus-A) | clean room, common-prior, channel-convergent (24/24) | **C8 positive**: DEPENDENT\* with diagnosis COMMON_PRIOR/CHANNEL_CONVERGENT — never counted as FPR, never called clone |
| (gptA, grok), (gptB, gem), (grok, gem) | certified cross-prior independents | **C2 negatives**: CLEAN or channel-INADMISSIBLE for a preregistered mechanical reason; DEPENDENT\* on any admissible one ⇒ FAIL |
| (A, gem-main) | clean room, cross-prior (0/24) | C2-auxiliary negative (same treatment) |
| (PM1, PM2) | context-seeded marginal-matched wrappers over independent bases | C-PM negative: CLEAN (validated sc.15) |
| (gptA-main, gptA-ref1) | shared helpers, decorrelated surface | REPORTED only (measured blind spot, sc.11–12); a flag = surprise requiring diagnosis |
| same-author pairs (A,W),(A,P),(W,M)… | NOT certified independent (sc.16) | excluded from FPR; reported |

Direction-invariance registered (review X 4b): verdicts are claimed
invariant to derivation direction; the holdout includes one
reversed-derivation pair to test this.

## 4. Instrument v4 `[LOCK]`

1. **Admission, per channel and per pair.**
   - Token: token-world-sensitivity ≥ 0.30 AND informative support
     N_informative ≥ Nmin (instances where both members give ≥ 3
     value-failure cells; Nmin from OC-tune, proposed 4 per stratum-mix).
   - Journal: world-sensitive fingerprint AND **schedule-adaptivity**
     (fingerprint variation across world-side perturbation pairs ≥
     threshold from OC-tune) — sc.14–15: static-schedule languages are
     outside the channels' domain; their pairs are
     INADMISSIBLE(channel), never counted in power/FPR.
2. **Token channel:** M1 same-wrong-value excess over the analytic
   per-instance null; instance-level significance (mean > 0.05 AND
   > k·se, k from OC); matched AND crossed seeds.
3. **Journal channel (the blade):** J_fail — schedule co-adaptation on
   the pair's failure-class instances — minus the **adaptivity-matched
   field**: max(0, q75) of J_fail over external reference pairs drawn
   from schedule-adaptive families only (sc.15), leave-candidate-family-
   out, ≥ 3 external pairs else UNKNOWN (mechanical check printed per
   pair — the v3 formal bug stays closed). Margin 0.10, matched AND
   crossed. Success-only co-adaptation is never flagged (the
   world's-one-door case; sc.13).
4. **Axes.** D: DESTINATION_SAME/DIFFERENT/NA. P: DEPENDENT(token) /
   DEPENDENT(journal) / DEPENDENT(unresolved) / CONTACT_SCHEDULE /
   CLEAN / UNKNOWN / INADMISSIBLE(channel). E (eligibility/admission)
   and N (informative support) reported per pair (review Y §3). Union
   of channels; no combined p-value; no strength ranking.
5. **Null-world gate (review X 4a):** on K3 worlds every pair must read
   CLEAN or INADMISSIBLE; any DEPENDENT\* there ⇒ channel specificity
   failure ⇒ run-level FAIL.
6. **UNKNOWN semantics:** K2a/K2b/C1: UNKNOWN = FAIL of that arm. C2:
   UNKNOWN ⇒ run INCONCLUSIVE. Reported-only rows never gate.

## 5. Kill conditions, controls, outcome axes `[LOCK]`

- **K1** (regression, unit-test status): naive detector fires on (A,Gt)
  AND (A,gptA-main) on core cycles; does not fire on the null world
  (agreement ≤ 1/8 instances). Failure ⇒ harness defect ⇒ abort.
- **K2a** (A,Gt) ∈ DEPENDENT\*. **K2b** (A,gptA-main) CLEAN on both
  channels + destination-same ≥ 6/8 core-cycle instances.
- **K3** null world as §2/§4.5.
- **C1** clone; **C2** certified cross-prior negatives; **C-C8**
  (A,opus-A) DEPENDENT\* with the registered diagnosis; **C-PM** clean;
  **C3** admission reported for every pair; **C4** wording lock (§1);
  **C5** pool/references/rules locked herein; **C6** oracle sanity.
- **Outcome reading** per review Y: every K/C row resolves into
  E/D/N/P sub-states; terminal states OPPOSITE / NO_INFORMATION /
  UNKNOWN_FIELD / INADMISSIBLE / COMPETENCE_FAIL / INFRASTRUCTURE_FAIL.
  `K2a=F` is readable ONLY when E,D,N all PASS and P=CLEAN ("registered
  derived pair not detected"); otherwise it is NO_TEST. `K2b=F` via
  P=DEPENDENT\* triggers the C8 contrast before any interpretation:
  if the common-prior controls are also elevated ⇒ TASK/PRIOR
  dependence, never "instrument conservative"; only an (A,gptA) flag
  that is an OUTLIER against all clean-room cross-prior pairs reads
  UNEXPLAINED_RESIDUAL_DEPENDENCE. `P/F/F` reads "target contrast not
  reproduced; no causal interpretation assigned."

## 6. Scope and `not_tested_against` (published with any outcome)

Scope sentence (locked): **CLEAN/INDEPENDENT means clean under the
registered token and journal observables, given the declared reference
constructions, this world family, and the locked window. It is not
proof of absence of latent shared implementation, channel convergence
below the instrument's resolution, or world truth.**

`not_tested_against`: shared implementation with decorrelated surface
(measured instance: gptA-main/ref1); dependence outside the visibility
window (too-competent / noise-decohered; sc.11–12); static-schedule
languages (outside the admission domain, sc.14–15); semantic shared
preprocessors beyond prefix hygiene (+0.044 measured); clone vs
Cayley-channel separation (interface arm); adaptive languages optimized
against the detector; changed I; generalization beyond the locked
family (holdout only); strength ranking from double hits; channel
convergence as a HIDDEN cause in pairs never run through the C8
contrast (the gradient 24/12/0 shows declared mechanism does not
predict it).

## 7. Statistical plan `[LOCK]`

- Scale: instances ≥ 8 per stratum, K = 8 seeds, 5 perturbations
  (≥ 56 instance-units; `seed_policy` satisfied at instance level).
- **OC-tune** (synthetic bank; bases from ≥ 3 priors; derived/clone/
  certified-independent/PM classes with C8 labels inherited — (A,opusA)-
  class pairs are POSITIVE examples of their own class, never FPR):
  selects the window (widest region with power-LCB ≥ 0.8 on admissible
  derived pairs and FPR-UCB ≤ 0.05 on certified cross-prior negatives,
  one-sided bounds, fixed MC count), the significance multiplier k, and
  the clone/derived resolution factor (review X: C1 must be passed with
  a margin exceeding the derived effect size, else `P|F|…` rows are
  unreadable and the run is NO_TEST for K2a).
- **OC-validate**: a fresh synthetic bank, single frozen evaluation of
  the full pipeline including window selection; acceptance by the same
  confidence bounds; no changes after it.
- FPR is run-level family-wise: P(≥1 false flag among K2b + all C2
  negatives under the full union pipeline), estimated by simulating the
  entire run in OC-validate.
- **Sanity seed: outcome-blind** (hashes, oracle cross-check, schema,
  determinism, non-NaN; pair labels and excesses hidden; abort
  conditions pre-listed; review Y §4.4).
- Scout instances/seeds/parameter tuples excluded from the locked run.

## 8. Holdout (escrow BEFORE the locked run — review Y §4.5)

Per `HOLDOUT_ESCROW.md`: the holdout world family + shams (including
one reversed-derivation pair) are commissioned from a fresh clean-room
agent, generated ONCE under a hash-fixed prompt and mechanical
acceptance tests, encrypted and committed BEFORE the locked run;
decrypted only after the primary outcome is published. Only the holdout
supports any confirmation claim; the locked run alone is internal
validation of a development-set family.

## 9. What kills Experiment A (any one)

(A,gptA-main) flagged without the C8 contrast resolving it; (A,Gt)
cleared with E/D/N all PASS; clone missed or passed without the
resolution margin; any certified cross-prior negative flagged; any
DEPENDENT\* on the null world; UNKNOWN counted as success anywhere;
post-lock changes of thresholds, pools, window, or wording; a report
upgrading "did not detect" into "proved".
