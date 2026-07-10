# Experiment A — PREREG DRAFT (NOT LOCKED)

> Status: DRAFT. This file is not a lock. The lock happens via
> `gate_harness.prereg` (PREREG.json + PREREG.lock, pre-commit hook,
> ancestor check) only after (1) Codex adversarial review of this draft and
> (2) the author's sign-off. Every number marked `[LOCK]` must be frozen at
> lock time and may not be revisited after any outcome is seen.

## The question (the designed fall)

In `Z/nZ`, the algebra language A (minimal relation `Rᵐ = e`) and the
geometry language G (fundamental cycle of the state graph) agree on the
wall `m = n` **by theorem** (Cayley). Their agreement is glue, not
evidence. Experiment A asks one falsifiable question:

> Does a detector that reads *destinations* (agreement of final claims)
> credit this theorem-glued agreement to the world — and does the
> journal/token instrument (v3) correctly refuse to?

This is the cheapest kill available to line 12, designed before any
positive claim: if we cannot build a detector that abstains on the
isomorphic pair, everything downstream is uncitable.

## Fixed objects

- **World.** `Z/nZ`, anonymous states, generator `R`, `L = R⁻¹`. External
  truth: `u(x₀)=v(x₀) ⇔ net(u) ≡ net(v) (mod n)`. Hidden from all
  languages. n range `[LOCK]`.
- **Task (extensional).** Bounded oracle budget; predict equality for
  unseen word pairs.
- **Interface I.** The equality oracle, shared, FIXED for this experiment.
  All invariance claims are indexed by this I (a wall of the interface is
  not a wall of the world; the interface arm is a separate, later
  experiment).
- **Perturbation ensemble (world-side only).** basepoint shifts, generator
  reversal, noise reseed. Budget± is a contact parameter, NOT a world
  perturbation (scout 06, iteration 3), and is excluded from fingerprints.
- **Instrument v3.**
  1. Admission, PER CHANNEL (scout 09): token channel requires
     token-world-sensitivity; journal channel requires a non-degenerate,
     world-sensitive schedule fingerprint. Thresholds `[LOCK]`.
  2. Token channel (v2, scouts 04–05): M1 same-wrong-value excess over the
     analytic per-instance null; instance-level significance (mean > margin
     AND > 2·se); seed-crossing control. Verdicts: CONSTRUCTION_DEPENDENT /
     CONTACT_SCHEDULE_DEPENDENT / NO_DEP.
  3. Journal channel (M6 + reference field, scouts 06–09): schedule
     co-adaptation over world-side perturbation pairs; field = max(0, q75)
     of crossed co-adaptation over the declared reference pairs
     ({A, P, W, M}, candidates excluded, <3 pairs ⇒ UNKNOWN); margin 0.10;
     matched AND crossed must clear.
  4. Verdict per pair = union of channels. NO combined p-value, NO strength
     ordering from double hits (Codex): if both channels fire, both are
     reported; the causal source remains unresolved unless a dedicated arm
     isolates it.

## Kill conditions (all preregistered, each decides alone)

- **K1.** The naive destination detector ("both languages report m ⇒ world
  wall at m") MUST fire on the A/G pair across instances. Expected: fires
  (agreement is a theorem). This kills "agreement ⇒ reality" as a criterion,
  citable on its own.
- **K2.** v3 must NOT label the A/G pair INDEPENDENT. K2 passes if A/G is
  not INDEPENDENT. K2 does NOT require separating clone-dependence from
  Cayley/interface-dependence — that separation is assigned to the later
  interface arm (changing I). Measured basis: A/G reads
  construction-dependent, currently indistinguishable from the literal
  clone (0.094 vs 0.093).
- **K3.** Null world (inconsistent oracle): destination agreement must NOT
  arise. The inconsistent oracle changes designation only, never the
  observable world traces consumed by v3 (C6).

## Required controls (Codex, adopted verbatim)

- **C1** clone positive control: A/A′ must not be called independent.
- **C2** independent negative controls: at least one preregistered
  independent pair (journal case: (G,P); token case: (P,Pv)) must remain
  clean under the same locked rules.
- **C3** admission reporting: every pair in K1–K3 passes admission or is
  marked inadmissible — never silently counted.
- **C4** no source overclaim: A/G may be DEPENDENT or DEPENDENT_UNRESOLVED,
  never "clone" — unless the interface arm proves channel identity.
- **C5** field-pool composition, reference set, and clustering/admission
  rules locked before outcomes.
- **C6** null-world oracle sanity (see K3).

## Scope (adopted verbatim from the Codex review)

> INDEPENDENT means clean under the registered token and journal
> observables, given the declared reference constructions. It is NOT a
> proof of absence of latent shared implementation.

The reference set's mechanism-disjointness is a **declared assumption of
the design**, not a measured fact (scout 08: it cannot be measured from
inside — the recursion is real).

## not_tested_against (published with any outcome)

- Separating clone A/A′ from Cayley-isomorph A/G (interface arm, later).
- Latent shared subroutines/postulates with anti-correlated surface
  symptoms (the Codex quotient sham — cheap to build, passes admission +
  token + journal by construction).
- Adversarial pool composition beyond the locked pool and reference set.
- Mode-split M3/M4 as an independent positive channel (never positively
  validated; subsumed by the journal channel in scouts 05–06).
- Interface dependence under changed I.
- Adaptive languages optimized against the detector.
- Generalization outside the locked world/intervention family.
- Strength ranking from double-channel hits.

## What kills Experiment A (any one suffices)

- A/G labeled INDEPENDENT.
- A/A′ clone missed.
- A preregistered independent negative control flags under the locked
  rules.
- The report claims clone-vs-Cayley separation.
- `not_tested_against` omissions discovered post hoc.

## To freeze at lock time `[LOCK]`

n range and instance counts; seeds (count ≥ 20 for core metrics, per
`seed_policy`); admission thresholds per channel; strata definitions;
margins (token, journal = 0.10); reference set (A, P, W, M) verbatim code;
sanity-seed protocol (single disjoint seed before the multi-seed run).
