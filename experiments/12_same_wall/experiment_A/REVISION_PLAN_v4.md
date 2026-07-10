# PREREG v4 — revision plan after the second two-review attack (Jul 11)

v3 is NOT signed. Review X (Opus-line) and review Y (GPT-line) in
`/home/master/Documents/my/dialogs/PREREG_v3_DRAFT_review_by_{X,Y}.md`.
Y found one FORMAL BUG that structurally guarantees INCONCLUSIVE (C2
pairs are reference units; leave-family-out leaves 1 < 3 external pairs
— verified independently before acceptance). Every item below is
accepted; owners assigned. v4 is written only after the new artifacts
exist.

## Accepted changes

| # | change | source | owner |
|---|---|---|---|
| 1 | **Reference bank rebuilt**: C2 candidates leave the bank; ≥ 5–6 external reference units so every gating pair keeps ≥ 3 external pairs; mechanical prereg check `n_external_pairs >= 3` per comparison | Y §4.1 (blocker) | Claude + commissions (#10) |
| 2 | **Success/failure split for the journal channel**: DEPENDENT(journal) only if co-adaptation survives the success→failure transition; OC must show the CLONE retains co-adaptation across the split (else the split is not a discriminator and is dropped with a record) | X §1 | Claude (scout 13) |
| 3 | **Window frozen by admission-quantities** on C1/C2 + synthetic banks; both K2 pairs excluded from the window definition; K2 pair outside the window ⇒ INADMISSIBLE (not FAIL/PASS). Alternative kept open per Y: fixed stress lattice + band-pass contrast statistic, null calibrated for the whole selection procedure | X §2 + Y §2 | Claude (OC design) |
| 4 | **Clone/derivation resolution factor** preregistered: OC must demonstrate separation between clone-class effect and derivation-class effect (phase-0 sizes 0.5 vs 0.053); without it `K2a=F` rows are unreadable | X §3 | Claude (OC) |
| 5 | **v3 gated on the null world**: any DEPENDENT verdict on Bernoulli-oracle worlds ⇒ channel specificity failure ⇒ run FAIL (the instrument finally gets its own null arm at run level) | X §4a | Claude |
| 6 | **Direction-invariance preregistered**: v3 verdicts claimed invariant to derivation direction; holdout includes a reversed-derivation pair to test it | X §4b | Claude + holdout |
| 7 | **C8 common-prior ladder**: factorial clean-room family — spec encoding (original / reformatted-B) × builder prior (GPT-family / other-provider / human if available) × provenance (derived / clean). Registered diagnoses: SPECIFICATION_FORMAT_DEPENDENCE / COMMON_PRIOR_DEPENDENCE / TASK_BUDGET_FORCED_DEPENDENCE / UNEXPLAINED_RESIDUAL_DEPENDENCE. No K2b=F reading as "instrument conservative" without this contrast | Y §1 | **Kirill commissions** (#10) |
| 8 | **Outcome table split into axes** E (eligibility) / D (destination) / N (informative support) / P (verdict) per pair; terminal states OPPOSITE / NO_INFORMATION / UNKNOWN_FIELD / INADMISSIBLE / COMPETENCE_FAIL / INFRASTRUCTURE_FAIL; `P/F/F` row reworded to "target contrast not reproduced; no causal interpretation assigned" | Y §3 | Claude |
| 9 | **Performance-matched independent control**: independent wrappers corrupting answers to registered marginal error profiles matching (A,Gt)'s — CLEAN expected; plus informative-support minimum `N_both_wrong ≥ Nmin` (from OC) per key stratum | Y §4.2 | Claude (scout 13) |
| 10 | **OC split**: OC-tune (window/multiplier selection) / OC-validate (single frozen evaluation); acceptance by one-sided confidence bounds (FPR UCB ≤ 0.05, power LCB ≥ 0.8); fixed MC replication count; FPR defined as run-level family-wise event over the full pipeline | Y §4.3 | Claude |
| 11 | **Sanity seed outcome-blind**: infrastructure checks only (hashes, oracle cross-check, schema, determinism); all pair labels and excess scores hidden until the full run completes; abort conditions listed in advance | Y §4.4 | Claude |
| 12 | **Holdout escrow**: generated and encrypted-committed BEFORE the locked run; prompt hash, provider rule, single generation, mechanical acceptance tests, no human veto | Y §4.5 | Kirill + Claude |
| 13 | **Truth semantics per stratum**: latent-structural vs observable-predictive stated per stratum; finite equivalence criterion; word-length bound; "exhaustive" dropped unless sufficiency is proven; Oracle-T/N behavior defined on stochastic/nonstationary strata | Y §4.6 | Claude |
| 14 | **Claim wording** (adopted verbatim): "Within the locked stress family, v3 assigned different residual-dependence labels to one registered derived pair and one registered clean-room pair, while preserving destination agreement." | Y §9 | — |

## Line-level note (X's closing lever, recorded)

The first rock now has measured structure: two paths converge either
because they SHARE AN ANCESTOR (genealogy) or because THE TASK HAS ONE
GOOD SOLUTION (world-forced competence). The co-adaptation detector
conflates them; the success/failure split is the first tool that cuts
between them — *co-adaptation that survives into correlated failure is
ancestry; co-adaptation that lives only in success is the world's one
door.* If the split survives OC (clone retains, competents lose), the
line has an operationalization of the question it was opened for.

## Commissions needed from Kirill (C8 ladder, #7)

Cells wanted (each: clean room, web, no filesystem, fresh account where
possible; returns one file per CODEX_SPEC interface):
1. **encoding-B × GPT-family** — same task, reformatted spec
   (`SPEC_ENCODING_B.md`), GPT web session (may be the same account
   class as before, different session).
2. **encoding-A × other-provider** — original spec, non-GPT builder
   (Gemini / Grok / other; whatever is available).
3. *(optional but valuable)* **encoding-B × other-provider**, and/or a
   human-written solver if one volunteers.

## Order of work

1. Scout 13: success/failure split on existing data (clone must retain);
   performance-matched wrappers; reference bank candidates.
2. Commissions return → provenance-register → first contact.
3. OC-tune / OC-validate design + run.
4. PREREG v4 written with all artifacts in hand → third review round →
   sign → lock (escrowed holdout already committed).
