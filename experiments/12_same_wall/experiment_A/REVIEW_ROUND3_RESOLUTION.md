# Review round 3 → v4.1 resolution map (for the mechanical diff-review)

Both reviewers declared the series CONVERGED ("достаточно"): W — signable
under 7 conditions; Z — signable under 3 blockers + 3 scope notes; no
round 4. Every condition below maps to an exact v4.1 change.

| # | condition (source) | resolution in v4.1 |
|---|---|---|
| W1 | channel-specific E/N/P; C2 quorum ≥3 admissible per channel; INADMISSIBLE ≠ C2-pass; else NO_TEST_C2_QUORUM | §4.4 axes split per channel (E_t/N_t/P_t, E_j/N_j/P_j; P_union derived only); §5 C2 quorum rule verbatim |
| W2 | frozen pair-specific reference matrix; filter cascade printed; ≥4 eligible ref-pairs pre-lock, ≥3 at runtime | §4.3 + Appendix R (frozen matrix); cascade raw→certified→class→admissible→used printed per pair |
| W3 + Z2 | C8 never rescues K2b; DEPENDENT\* ⇒ K2b = FAIL_RESIDUAL_FLAG; diagnostic tags only; θ_outlier = q90(UCB) on ≥10 cross-prior non-convergent pairs frozen in OC; UNEXPLAINED/ISOLATED is a labelled FAIL, never a pass; "outlier" as statistical term removed | §5 K2b rewritten; tags COMMON_PRIOR_PATTERN_REPLICATED / CROSS_PRIOR_FLAG_ISOLATED / BROAD_CROSS_PRIOR_ELEVATION / C8_NO_TEST; θ_isolation frozen in OC-tune on ≥10 pairs |
| W4 | OC bundle θ frozen (window, k, resolution factor, Nmin, adaptivity threshold, field rule, tie-breaks); hash(θ); validate applies only; FAIL ⇒ stop; α, bound method, MC ≥ 59 stated | §7 rewritten: θ-bundle with sha256; exact one-sided binomial bounds, 95%, MC counts stated; no reselection; retune forbidden |
| W5 + Z3 | escrow: authors never see plaintext pre-publication (encrypt-on-receipt to committed public key / custodian); provider fixed BY NAME with C8-map justification; fallback list with exact IDs; acceptance script sha256 frozen; acceptance-failure = HOLDOUT_INVALID_GENERATION, abort-and-report, no regeneration; commit DAG; key released only after publication to immutable public location | HOLDOUT_ESCROW.md v2 (rewritten); provider = Gemini-family by name (0/24-class = strictest cross-prior test, per Z's argument); DAG order enumerated |
| W6 | holdout adapter: fixed metafamily OR machine-readable world contract | HOLDOUT_ESCROW.md v2: Variant A adopted — holdout = new parameter tuples, solver implementations and shams within the frozen WorldSpec metafamily (cycle/alias/noisy/qtrap/wobble/lollipop/nonstat interface); Variant B recorded as future interface-arm work |
| W7 | claim wording v3→v4; §8→§7 window reference; forward/reverse matched (same transform family, same source) | §1, §2 fixed; holdout includes matched T(X)/T⁻¹(X) pair |
| Z1 | field leave-CONVERGENCE-out, not leave-family-out; OC check: field built both ways on a known-effect derived pair must agree, else only convergence-leave-out valid | §4.3 rewritten: field pairs must be certified cross-prior AND channel-non-convergent (0/24-class); OC-tune runs the two-way construction check |
| Z-scope-4 | C2 admission checked on outcome-blind sanity (E-axis only) before the locked run | §7 sanity checklist extended |
| Z-scope-5 | holdout tests generalization WITHIN the applicability domain (schedule-adaptive); named in scope | §6 scope sentence extended |
| Z-scope-6 + W7 | direction-invariance: matched pair AND wording downgraded to "tested once, not certified" | §3 + §6 |

Remaining before lock (mechanical only): reviewers' diff-check of this
map; the author's signature; OC-tune/OC-validate runs producing θ;
escrow execution per HOLDOUT_ESCROW v2; `gate_harness.prereg` lock.
