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
| (gptA, grok), (gptB, gem), (gptA, gem) | certified cross-prior independents — **C2-AUDIT, never in any field** (F2.1: (grok,gem) reallocated to REF-CALIBRATION only) | **C2 negatives**: gate on the token channel; INADMISSIBLE excludes the pair from C2_c (per-channel quorum, §5); DEPENDENT\* on any admissible one ⇒ FAIL |
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
   N_journal, P_journal`. D: DESTINATION_SAME/DIFFERENT/NA. Per-channel
   P values: DEPENDENT / CONTACT_SCHEDULE / CLEAN / UNKNOWN /
   INADMISSIBLE. **P_union collapse rule (frozen; F1):** P_union is
   computed AFTER each channel's E-gate (an INADMISSIBLE channel never
   leaks into the union; E-linkage 2): DEPENDENT iff ≥ 1 admissible
   channel is DEPENDENT; CLEAN iff ≥ 1 admissible channel exists and
   ALL admissible channels are CLEAN; otherwise NO_TEST/UNKNOWN. All
   downstream rules reference `E_c/N_c/P_c` or `P_union` explicitly.
   No combined p-value; no strength ranking (diagnostic ranking exists
   only inside the frozen C8 tags, §5).
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
  **Structural carve-out (F2.2, documented not hidden):** with five
  clean-room families and the AUDIT/CALIBRATION split, the C2-audit
  pairs cannot themselves receive journal fields with ≥ 3 external
  pairs (combinatorics in Appendix R). Therefore **C2 gates on the
  token channel; C2 journal verdicts are structurally UNKNOWN_FIELD and
  are reported, not gated; the journal-channel negative floor for K2b
  is carried by OC-validate's full-run simulation** — exactly the split
  review W itself proposed (REF-CALIBRATION vs C2-AUDIT; FWER bought by
  OC-validate). This trade is part of the locked scope.
- **K2b failure semantics (reviews W3+Z2 merged — C8 never rescues):**
  any DEPENDENT\* on (A,gptA-main) ⇒ **K2b = FAIL_RESIDUAL_FLAG,
  always, regardless of every C8 diagnostic tag**. The C8 contrast then
  attaches exactly one tag from the frozen, mutually exclusive decision
  table below (per triggering channel c, with θ_c frozen in OC-tune as
  q90 with one-sided UCB over ≥ 10 certified cross-prior
  channel-non-convergent pairs; **θ_isolation_token uses token-excess,
  θ_isolation_journal uses J-minus-field** — F3; comparator set S =
  the Appendix R CALIBRATION pool, named pre-data; two prior-ladder
  controls at different heights per E-linkage 3: H = (A,opusA)
  [24/24-class], M_ctl = (A,grok) [12/24-class]):
  1. **C8_NO_TEST** — θ_c undefined (OC quorum failed) or any of
     S/H/M_ctl inadmissible on c.
  2. **BROAD_CROSS_PRIOR_ELEVATION** — ≥ 2 pairs in S exceed θ_c
     (field-level elevation; cause at instrument/world level).
  3. **COMMON_PRIOR_PATTERN_REPLICATED** — ≤ 1 of S exceeds θ_c AND the
     gradient ordering holds (H > M_ctl > median(S)) AND target ≤ H
     (coupling within the prior-ladder envelope; task/prior-level
     cause).
  4. **CROSS_PRIOR_FLAG_ISOLATED** — ≤ 1 of S exceeds θ_c AND (target >
     H or the gradient ordering is violated): a labelled, unexplained
     K2b failure demanding diagnosis. **Never a pass.**
  The word "outlier" is not used as a statistical inference anywhere.
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
  (certified cross-prior negatives); exact one-sided binomial bounds
  at 95%. **Frozen MC counts (F4.1, no optional stopping):
  n_MC_tune = 200, n_MC_validate = 100** full-run simulations.
  **Tie-break algorithm design-locked NOW (F4.2), not chosen by OC:**
  widest window = most strata; ties broken by (1) lower mean FPR-UCB,
  (2) higher mean power-LCB, (3) the stratum order listed in §2. θ
  records only the applied outcome.
- **Two-stage lock order (F4.3):** **L0 DESIGN LOCK** — analysis code,
  lattice, OC algorithm, tie-break rule, MC counts, this document —
  committed BEFORE OC-tune runs. Then OC-tune → θ → single OC-validate.
  **L1 FINAL LOCK** — concrete θ + Appendix R certification results —
  via `gate_harness.prereg`. Only after L1: escrow dispatch and the
  primary run.
- **OC-validate FAIL is a published artifact (E-annotation 4):**
  FAIL ⇒ the experiment stops unlocked; `OC_VALIDATE_FAIL` is committed
  with the full simulation outputs; the instrument is not claimed;
  silent return to tuning is forbidden.

**AMENDMENT-2 (tune-stage, re-signed by the author; forced by the
tune's own result — the pooled estimand had no terminal state for an
empty window, a gap the round-3b diff-review class would have
flagged).** OC-tune (200 sims, primary scale, deterministic seed stream
31000+977s; raw artifacts `oc_tune_results.json`,
`oc_tune_perpair.json`) measured: **derivation visibility is a
base-class property** — per-pair power at the best window:
derived-A 200/200, derived-gem 198/200, **derived-gptA 0/200 (0/1200
across all windows)**. The robust-validator class erases the observable
trace of even its own true derivation — the discipline-buys-
independence result (Gemini 0/24; H-theorem) at the derivation level;
published as a measured limit, never as instrument error. Therefore:
(1) the power estimand is computed PER BASE-CLASS; the claim domain =
classes with measured visibility ({A-class, gem-class} — cross-prior
diversity preserved, 2 of 3 classes); the gptA-class is excluded from
power claims and published; K2a's base (A) is in-domain at 200/200.
(2) The window rule, applied to the domain classes, qualifies exactly
one window: **{cycle, alias, noisy, qtrap, wobble}** — power 398/400
(exact one-sided LCB ≈ 0.983 ≥ 0.8), FPR 0/348 (UCB 0.0086 ≤ 0.05).
No tie-break needed (unique). (3) The FPR estimand is unchanged.
(4) Scope inherits: the locked run's derived-detection claims hold for
value-failing, schedule-transparent base classes; robust-validator
bases are `not_tested_against` — with 1200 zeros attached.
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

Per `HOLDOUT_ESCROW.md`: the holdout — new parameter tuples, solver
implementations and shams inside the frozen WorldSpec metafamily,
including one **matched forward/reverse construction from the same
source and transform family (X, T(X), T⁻¹(X))** (F7) — is commissioned
from a fresh clean-room agent, generated ONCE under a hash-fixed prompt
and the frozen mechanical acceptance suite, encrypted on receipt and
committed BEFORE the locked run; decrypted only after the primary
outcome is published (tagged release). Only the holdout
supports any confirmation claim; the locked run alone is internal
validation of a development-set family.

**AMENDMENT-3 (run-time, re-signed by the author; both parts forced by
the first primary execution).** (a) *Infrastructure:* NullWorld moved to
stable hashing — builtin `hash()` is per-process randomized, which made
the K3 gate nondeterministic across runs (caught by the second
execution disagreeing with the first; determinism is a listed abort
condition). (b) *K3 scope:* the clone flagged on the null world — and
the instrument was RIGHT: same-construction pairs couple through any
consistent answer function; construction-dependence needs no world. K3
as originally locked was self-defeating for the registered clone
control. Amended rule: on null worlds, all CROSS-construction pairs
(including both K2 pairs) must read CLEAN/INADMISSIBLE — a flag there
is a specificity failure ⇒ run FAIL; registered same-construction
controls are excluded from the gate, their null-world flag recorded as
confirmation of the construction channel. The lock's
`prereg_doc_sha256` binds the pre-A3 document; the post-A3 document
hash is recorded in the decision payload — both hashes public.

## Appendix R — frozen reference matrix (part of the prereg hash)

Units (family = one received file or one author): gptA-fam, gptB-fam,
grok-fam, gem-fam, opusA-fam (clean-room); A/W/M/P are same-author
(never field-eligible); PM never eligible.

**AMENDMENT-1 (pre-L0, re-signed by the author; discovered by the
battery itself):** the certification criterion counts **WRONG-value
agreement ≤ 6/24**, not raw agreement — agreement on correct values is
the world's credit, not coupling (scout 02's founding lesson, inherited
by the battery: RP-03's 16/24 was all-correct/world-forced; RP-06's
12/24 was all-wrong/convergent). Battery run Jul 11, results frozen:

| id | pair | agree-correct | agree-WRONG | eligible |
|---|---|---|---|---|
| RP-01 | (gptA,grok) | 0 | 0 | YES |
| RP-02 | (gptB,gem) | 4 | 0 | YES |
| RP-03 | (gptA,gem) | 16 | 0 | YES |
| RP-04 | (grok,gem) | 0 | 0 | YES |
| RP-05 | (opusA,gptB) | 0 | 0 | YES |
| RP-06 | (opusA,grok) | 0 | **12** | **NO** |
| RP-07 | (opusA,gem) | 0 | 0 | YES |
| RP-08 | (gptB,grok) | 0 | 0 | YES |
| RP-09 | (gptA,gptB) | 4 | 0 | YES |

Quorum check after RP-06 exclusion: (A,gptA-main) → RP-04,05,07,08 = 4
✓; (A,Gt)/(A,A′) → 5 ✓; (A,opus-A) → RP-04,08,09 = 3 (the registered
quorum edge) ✓; PM → 5 ✓. The C8 comparator set S = the 8 eligible RP
pairs; the θ_isolation quorum (≥ 10) is completed in OC-tune by
certifying additional cross-file ref-solver pairs with this same
(amended) battery.

**C2-AUDIT family-pairs (never in any field):** RP-01 (gptA,grok),
RP-02 (gptB,gem), RP-03 (gptA,gem); plus (A, gem-main) as the auxiliary
negative. **C2 gates on the token channel only** (structural carve-out,
§5).

**REF-CALIBRATION pool** (immutable IDs): RP-04 (grok,gem),
RP-05 (opusA,gptB), RP-06 (opusA,grok), RP-07 (opusA,gem),
RP-08 (gptB,grok), RP-09 (gptA,gptB).

| gating pair | field pair IDs | count pre-lock (≥4) / runtime (≥3) |
|---|---|---|
| (A, gptA-main) | RP-04..RP-08 | 5 `[cert]` |
| (A, Gt), (A, A′) | RP-04..RP-09 | 6 `[cert]` |
| (A, opus-A) | RP-08, RP-09, RP-04 | **3 — registered quorum edge:** only three non-opusA candidates exist; if any loses certification/admission, the C-C8 journal verdict is UNKNOWN_FIELD (its registered expectation rides on the token channel, where the 24/24 effect lives) |
| (PM1, PM2) | RP-04..RP-09 (PM is not a family in the pool) | 6 `[cert]` |
| C2-AUDIT pairs (RP-01..03), (A,gem) | — structurally < 3 after the AUDIT split; journal = UNKNOWN_FIELD by construction, reported not gated (§5 carve-out) | — |

The filter cascade for every pair is printed at run time:
`raw_external → provenance_certified → class_eligible →
schedule_admissible → field_used`. **C8 comparator set S (§5) =
RP-01..RP-09 restricted to certified-eligible pairs**, named here
pre-data; prior-ladder controls H = (A,opusA), M_ctl = (A,grok).

## 9. What kills Experiment A (any one)

**(A,gptA-main) DEPENDENT on either admissible channel ⇒
K2b = FAIL_RESIDUAL_FLAG regardless of every C8 diagnostic tag** (F3);
(A,Gt) cleared with `E_c, D, N_c` all PASS on an admissible channel
(per-channel semantics, F1); clone missed or passed without the
resolution margin; any admissible certified cross-prior negative
flagged on the token channel; any DEPENDENT\* on the null world;
UNKNOWN counted as success anywhere; post-lock (L1) changes of
thresholds, pools, window, or wording; a report upgrading "did not
detect" into "proved".
