# Experiment A — PREREG DRAFT v2 (SUPERSEDED by PREREG_v3_DRAFT.md; kept for the review trail)

> Status: DRAFT v2, incorporating the final Codex adversarial review
> (poisoned-reference attack → scout 10; UNKNOWN semantics; outcome table).
> This file is not a lock. The lock happens via `gate_harness.prereg`
> (PREREG.json + PREREG.lock, pre-commit hook, ancestor check) only after
> the author's sign-off. Every `[LOCK]` item is frozen at lock time.

## The question (the designed fall)

In `Z/nZ`, language A (algebra: minimal relation `Rᵐ = e`) and language G
(geometry: fundamental cycle of the state graph) agree on the wall `m = n`
**by theorem** (Cayley). Their agreement is glue, not evidence.

> Does a detector that reads *destinations* credit this theorem-glued
> agreement to the world — and does the v3 instrument correctly refuse to?

## Fixed objects

- **World.** `Z/nZ`, anonymous states, generator `R`, `L = R⁻¹`; external
  truth `u(x₀)=v(x₀) ⇔ net(u) ≡ net(v) (mod n)`, hidden from all languages.
  n range `[LOCK]`.
- **Task.** Extensional: bounded oracle budget; predict equality for unseen
  word pairs.
- **Interface I.** Equality oracle, shared, FIXED. Every invariance claim
  is indexed by this I. The interface arm (varying I) is a separate later
  experiment.
- **Perturbation ensemble.** World-side only (basepoint shifts, generator
  reversal, noise reseed) `[LOCK exact list]`. Budget± is a contact
  parameter, not a world perturbation (scout 06), excluded from
  fingerprints.

## Instrument v3 `[LOCK all]`

1. **Admission, PER CHANNEL** (scout 09): token channel — token
   world-sensitivity ≥ threshold `[LOCK]`; journal channel —
   non-degenerate world-sensitive schedule fingerprint `[LOCK]`.
   An inadmissible pair cannot satisfy K1/K2/C1/C2 (C3).
2. **Token channel** (v2): M1 same-wrong-value excess over analytic
   per-instance null; instance-level significance (mean > margin AND
   > 2·se); seed-crossing control. Labels: DEPENDENT(token) /
   CONTACT_SCHEDULE / clean.
3. **Journal channel** (M6): schedule co-adaptation over world-side
   perturbation pairs; **reference field** = max(0, q75) of crossed
   co-adaptation over declared reference pairs, candidates excluded,
   < 3 remaining pairs ⇒ UNKNOWN; margin 0.10; matched AND crossed must
   clear. Labels: DEPENDENT(journal) / clean / UNKNOWN.
4. **Verdict per pair** = union of channels. NO combined p-value, NO
   strength ordering from double hits. Allowed labels `[LOCK]`:
   DEPENDENT(token), DEPENDENT(journal), DEPENDENT(unresolved),
   CONTACT_SCHEDULE, INDEPENDENT, UNKNOWN, INADMISSIBLE(channel).

### References `[LOCK identities, implementations, hashes]`

{A: linear origin scan; P: random pair sampler; W: adjacent-pair walker;
M: interval bisection}. Their mechanism-disjointness is a **declared
assumption of the design**, not a measured fact (scout 08: it cannot be
certified from inside — the recursion is real).

- **Hygiene gate `[LOCK]`:** no two references may share a common emitted
  probe prefix of length ≥ 2 on any instance (scout 10: honest max = 1,
  poisoned-preamble min = 3). This catches literal shared preprocessors
  only; it is trivially evaded by interleaving — see scope.
- The per-stratum q75 reference gate (Codex final review) was tested and
  REJECTED as specified: on defect strata the world's response is
  low-dimensional and forces lockstep on honest references too (honest
  wobble q75 = 1.000); a differential version reintroduces the recursion.
  Recorded in scout 10; not part of this prereg.
- Measured bound: the poisoned-normalizer attack at scout-10 strength
  inflates the global field by +0.044 (0.402 → 0.446) — insufficient to
  flip the clone control (excess 0.27), sufficient to flip a borderline
  pair. Semantic shared preprocessors remain in `not_tested_against`.

## Kill conditions (each decides alone; UNKNOWN semantics locked)

- **K1.** The naive destination detector `[LOCK exact implementation,
  firing threshold]` MUST fire "world wall" on the A/G pair across
  instances `[LOCK required pairs; UNKNOWN handling]`. Expected: fires.
  This kills "agreement ⇒ reality", citable on its own.
- **K2.** v3 on A/G: **PASS iff label ∈ DEPENDENT\***; **FAIL iff label =
  INDEPENDENT *or* UNKNOWN.** UNKNOWN is not success (Codex: otherwise K2
  is unfalsifiable). K2 does NOT require separating clone-dependence from
  Cayley/interface-dependence (interface arm, later).
- **K3.** Null world `[LOCK generator, inconsistency mode]`: the naive
  detector must NOT fire. The inconsistent oracle changes designation
  only, never the observable traces v3 consumes. v3's behavior on the
  null world is recorded, never used to rescue K1/K2.

## Controls (run-level, not decorative)

- **C1** clone A/A′ `[LOCK pair list]`: PASS iff DEPENDENT\*;
  **UNKNOWN = FAIL.**
- **C2** independent negatives `[LOCK pair list: journal case (G,P);
  token case (P,Pv); max allowed false flags = 0]`: PASS iff all locked
  pairs INDEPENDENT or channel-inadmissible for a preregistered mechanical
  reason; FAIL iff any admissible pair is DEPENDENT\*; **UNKNOWN on a core
  negative control ⇒ run-level INCONCLUSIVE, not PASS.**
- **C3** admission reporting: every pair in K1–K3 passes admission or is
  marked inadmissible — never silently counted.
- **C4** no source overclaim, exact wording locked:
  > v3 detects dependence under registered observables. v3 does not prove
  > construction identity, clonehood, or Cayley-interface equivalence.
  Any conclusion about A/G is phrased as "v3 did not clear A/G as
  independent under locked token/journal channels" — never "v3 proved".
- **C5** pool membership, reference set, admission/field rules locked
  before outcomes.
- **C6** null-world oracle sanity (see K3).

## Preregistered outcome table (Codex, adopted verbatim)

P = pass, F = fail, U = unknown/inadmissible/undecidable.

| K1 | K2 | K3 | C1 | C2 | Reading |
|---|---|---|---|---|---|
| P | P | P | P | P | Clean kill of naive detector; v3 survives Experiment A |
| P | P | P | P | F | Instrument implicated: v3 over-flags negatives |
| P | P | P | F | P | Instrument implicated: v3 misses clone control |
| P | F | P | P | P | Instrument implicated: v3 clears A/G as independent |
| P | U | P | P | P | Partial: naive killed, v3 not validated on A/G |
| P | P | F | P | P | Naive kill not specific; agreement may be oracle artifact |
| F | P | P | P | P | No naive kill; v3 behavior recorded separately |
| F | F | P | P | P | Experiment A fails its target |
| P | P | U | P | P | Partial: A/G usable, null-world sanity missing |
| U | · | · | · | · | Run inconclusive |
| · | · | · | U | · | Run inconclusive; clone control not established |
| · | · | · | · | U | Run inconclusive; negative floor not established |

Compact rules: clean naive-kill = K1∧K3; clean v3-survival = K2∧C1∧C2;
full clean = all five; instrument implicated = ¬K2 ∨ ¬C1 ∨ ¬C2; full run
failure = ¬K3 or core UNKNOWN from missing admission/reference field or
verifier/prereg failure.

## Scope (locked wording)

> INDEPENDENT means clean under the registered token and journal
> observables, given the declared reference constructions. It is NOT a
> proof of absence of latent shared implementation.

## not_tested_against (published with any outcome)

- Clone A/A′ vs Cayley-isomorph A/G separation (interface arm).
- Latent shared subroutines/postulates with anti-correlated surface
  symptoms (Codex quotient sham — passes admission + token + journal by
  construction).
- Semantic shared preprocessors beyond literal prefix sharing (poisoned
  normalizer; measured field inflation +0.044 at scout-10 strength).
- Adversarial pool composition beyond the locked pool and reference set.
- Mode-split M3/M4 as an independent positive channel.
- Interface dependence under changed I.
- Adaptive languages optimized against the detector.
- Generalization outside the locked world/intervention family.
- Strength ranking from double-channel hits.

## Remaining `[LOCK]` handles (full list, per Codex)

n range; instance counts; seeds (≥ 20 for core metrics per `seed_policy`;
sanity-seed disjoint); admission thresholds per channel; strata
definitions; margins (token, journal = 0.10); reference implementations +
hashes; hygiene-gate threshold (prefix ≥ 2); field statistic (max(0, q75),
GLOBAL, not stratified); minimum external reference-pair count (< 3 ⇒
UNKNOWN); seed-crossing policy; perturbation ensemble; world family;
channel precedence (union, no combined p-value); UNKNOWN propagation;
allowed labels; alpha / permutation count / multiple-comparison policy;
frozen pool membership; naive-detector implementation + firing threshold;
null-world generator + inconsistency mode.
