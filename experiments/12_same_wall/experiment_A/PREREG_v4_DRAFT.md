# Experiment A — PREREG v4.1 (NOT LOCKED; review series CONVERGED)

> Supersedes `PREREG_v3_DRAFT.md`. Round-3 reviews (W, Z) declared the
> series converged: signable under a finite list, no round 4. All
> conditions are integrated here; the mapping is in
> `REVIEW_ROUND3_RESOLUTION.md`. Remaining: mechanical diff-check,
> author signature, OC runs producing the frozen θ-bundle, escrow
> execution, `gate_harness.prereg` lock.

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

Claim wording locked (review Y, verbatim; v3→v4 corrected per W7):
*"Within the locked stress family, the v4 instrument assigned different
residual-dependence labels to one registered derived pair and one
registered clean-room pair, while preserving destination agreement."* No "genealogies distinguished"
simpliciter; no world-credit; no construction-identity claims (C4).

## 2. Fixed objects `[LOCK]`

- **Worlds, extensional truths** (predictive adequacy over the word
  space, no language's view): cycle n∈17..40 → n; alias (n, q proper
  divisor ≥4) → n; noisy-mild ε∈0.02..0.12 → n; qtrap (q∈5..9, k∈3..5,
  frac .6) → n; wobble/lollipop/nonstat → None (abstain correct).
  Final strata set = the lock-scale OC-tune's window (§7); the lattice
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

Direction-invariance (review X 4b; wording downgraded per review Z,
matched design per review W7): the holdout includes one MATCHED
forward/reverse pair — same source X, same transform family, T(X) and
T⁻¹(X). Outcome status: direction-invariance is thereby *tested once,
not certified*; the claim is scoped accordingly.

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
   the pair's failure-class instances — minus the field: max(0, q75) of
   J_fail over external reference pairs that are schedule-adaptive
   (sc.15) AND **leave-CONVERGENCE-out** (review Z blocker 1: C8 proved
   the coupling mechanism is not familial, so leave-family-out does not
   isolate the field from the signal): every field pair must be
   certified cross-prior AND channel-non-convergent (0/24-class), never
   same-author, never PM, never a registered C8-positive. The frozen
   pair-specific reference matrix (Appendix R) lists exact
   `reference_pair_id`s per gating pair — ≥ 4 eligible before lock (one
   spare), ≥ 3 at runtime else UNKNOWN_FIELD; the filter cascade
   `raw_external → provenance_certified → class_eligible →
   schedule_admissible → field_used` is printed per pair (review W2).
   OC-tune runs the two-way construction check (family-leave-out vs
   convergence-leave-out on a known-effect derived pair); if thresholds
   differ, only convergence-leave-out is valid. Margin 0.10, matched
   AND crossed. Success-only co-adaptation is never flagged (the
   world's-one-door case; sc.13).
4. **Axes — per channel, never one scalar (review W, structural):**
   each pair carries `E_token, N_token, P_token` and `E_journal,
   N_journal, P_journal`; `P_union` is a derived quantity only. D:
   DESTINATION_SAME/DIFFERENT/NA. Per-channel P values: DEPENDENT /
   CONTACT_SCHEDULE / CLEAN / UNKNOWN / INADMISSIBLE. No combined
   p-value; no strength ranking (diagnostic ranking exists only inside
   the frozen C8 tags, §5).
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
- **C1** clone; **C-C8** (A,opus-A) DEPENDENT\* with the registered
  diagnosis; **C-PM** clean; **C3** admission reported for every pair;
  **C4** wording lock (§1); **C5** pool/references/rules locked herein
  (incl. Appendix R); **C6** oracle sanity.
- **C2 with per-channel quorum (review W1, verbatim rule):** for each
  channel c on which K2b is admissible, C2_c = {preregistered C2 pairs
  with E_c = N_c = PASS}. C2_c = PASS only if |C2_c| ≥ 3 and every pair
  in C2_c has P_c = CLEAN. INADMISSIBLE is not a C2 success and does not
  enter the denominator; |C2_c| < 3 ⇒ NO_TEST_C2_QUORUM (run
  INCONCLUSIVE), never PASS. C2 admission (E-axis only) is verified on
  the outcome-blind sanity seed BEFORE the locked run (review Z).
- **K2b failure semantics (reviews W3+Z2 merged — C8 never rescues):**
  any DEPENDENT\* on (A,gptA-main) ⇒ **K2b = FAIL_RESIDUAL_FLAG,
  always**. The C8 contrast then attaches exactly one frozen diagnostic
  tag — COMMON_PRIOR_PATTERN_REPLICATED / CROSS_PRIOR_FLAG_ISOLATED /
  BROAD_CROSS_PRIOR_ELEVATION / C8_NO_TEST — and no tag converts FAIL
  into PASS. CROSS_PRIOR_FLAG_ISOLATED requires: the exact comparator
  set named pre-data (Appendix R), all comparators admissible on the
  triggering channel, the target the sole flagged pair, per channel
  separately, AND the target's statistic above θ_isolation — frozen in
  OC-tune as q90 (with one-sided UCB) of the J-minus-field distribution
  over ≥ 10 certified cross-prior channel-non-convergent pairs. The
  word "outlier" is not used as a statistical inference anywhere.
- **Outcome reading** per review Y: every K/C row resolves into
  per-channel E/D/N/P sub-states; terminal states OPPOSITE /
  NO_INFORMATION / UNKNOWN_FIELD / INADMISSIBLE / COMPETENCE_FAIL /
  INFRASTRUCTURE_FAIL / NO_TEST_C2_QUORUM. `K2a=F` is readable ONLY
  when E,D,N all PASS and P=CLEAN ("registered derived pair not
  detected"); otherwise NO_TEST. `P/F/F` reads "target contrast not
  reproduced; no causal interpretation assigned."

## 6. Scope and `not_tested_against` (published with any outcome)

Scope sentence (locked): **CLEAN/INDEPENDENT means clean under the
registered token and journal observables, given the declared reference
constructions, this world family, and the locked window. It is not
proof of absence of latent shared implementation, channel convergence
below the instrument's resolution, or world truth.** The holdout tests
generalization WITHIN the instrument's applicability domain
(schedule-adaptive, value-failing languages); static-schedule holdout
worlds are outside the test (review Z, scope). Appendix R (the frozen
reference matrix) is part of this prereg's hash.

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
- **OC-tune → one frozen parameter bundle θ (review W4):**
  θ = {window, significance multiplier k, clone/derived resolution
  factor, Nmin, schedule-adaptivity threshold, field construction rule
  (incl. the two-way leave-out check, review Z1), θ_isolation (≥ 10
  cross-prior non-convergent pairs), tie-break order for "widest
  window"}. sha256(θ) committed. Bank: bases from ≥ 3 priors with C8
  labels inherited ((A,opusA)-class = positive examples of their own
  class, never FPR). Selection rule: widest contiguous region with
  power-LCB ≥ 0.8 (admissible derived pairs) and FPR-UCB ≤ 0.05
  (certified cross-prior negatives); exact one-sided binomial bounds at
  95%; MC full-run simulations ≥ 59 (zero-error UCB ≤ 0.05 requires
  n ≥ 59); all counts recorded in θ.
- **OC-validate**: a fresh synthetic bank; a SINGLE evaluation of the
  frozen θ — no reselection of anything (review W4); acceptance by the
  same bounds; FAIL ⇒ the experiment stops, retune forbidden.
- **REF-CALIBRATION vs C2-AUDIT split (review W, free attack):** pairs
  used in any gating pair's field never serve as C2-audit pairs; the
  run-level FWER claim is carried by OC-validate's full-run simulation,
  and C2 is named as what it is — a reference-integrity audit.
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

## Appendix R — frozen reference matrix (part of the prereg hash)

Units: gptA-fam, gptB-fam, grok-fam, gem-fam, opusA-fam (clean-room);
A/W/M/P are same-author (never field-eligible); PM never eligible.
Pair-level certification = the 24-cell value-agreement battery run
BETWEEN the pair's members pre-lock (mechanical, before OC-tune);
eligible iff cross-prior AND agreement ≤ 6/24 (channel-non-convergent).

**C2-AUDIT pairs (never in any field):** (gptA, grok), (gptB, gem),
plus (A, gem-main) as the auxiliary negative.

**REF-CALIBRATION candidates per gating pair** (need ≥ 4 certified
pre-lock, ≥ 3 admissible at runtime):

| gating pair | candidate field pairs (pending certification battery) |
|---|---|
| (A, gptA-main) | (grok,gem), (opusA,gptB), (opusA,grok), (opusA,gem), (gptB,grok) |
| (A, Gt), (A, A′) | the five above + (gptA,gptB), (gptA,gem) |
| (A, opus-A) | (gptA,gptB), (gptA,gem), (gptB,grok), (grok,gem) |

The filter cascade for every pair is printed at run time:
`raw_external → provenance_certified → class_eligible →
schedule_admissible → field_used`.

## 9. What kills Experiment A (any one)

(A,gptA-main) flagged without the C8 contrast resolving it; (A,Gt)
cleared with E/D/N all PASS; clone missed or passed without the
resolution margin; any certified cross-prior negative flagged; any
DEPENDENT\* on the null world; UNKNOWN counted as success anywhere;
post-lock changes of thresholds, pools, window, or wording; a report
upgrading "did not detect" into "proved".
