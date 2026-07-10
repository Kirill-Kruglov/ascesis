# Holdout escrow protocol v2 (review round 3: W5/W6 + Z3 integrated)

Purpose unchanged: the locked run's family is a development set; only a
holdout the authors could not tune to — and whose content they cannot
see before the primary outcome is published — supports confirmation.

## Frozen decisions (before any contact with any provider)

1. **Provider, BY NAME (review Z3):** Gemini family — the 0/24
   channel-non-convergent class on the C8 map, hence the STRICTEST
   cross-prior CLEAN test: if even a 0/24-class holdout pair flags, the
   instrument is implicated. Justification committed herewith; this
   choice is a prediction, not a degree of freedom. Fallback list
   (technical unavailability BEFORE prompt dispatch only, verified by a
   failed API/login, not by preference): Gemini → Grok → HOLDOUT_NO_TEST.
   No other providers. Exact model version, web session, fresh account,
   no tools/filesystem, defaults for all other settings; recorded at
   dispatch.
2. **Metafamily, Variant A (review W6):** the holdout consists of NEW
   parameter tuples, NEW solver implementations, and NEW sham pairs
   INSIDE the frozen WorldSpec metafamily (cycle / alias / noisy /
   qtrap / wobble / lollipop / nonstat over the {R,L} equality-oracle
   interface). No new world classes; the locked pipeline applies with
   zero adapter decisions. A machine-readable world contract (Variant
   B) is future interface-arm work, recorded, not this experiment.
3. **Holdout content requested:** one derived pair, one MATCHED
   forward/reverse pair (same source, same transform family, T(X) and
   T⁻¹(X) — review W7), one clean-room independent pair, parameter
   tuples for each stratum. The prompt never describes the instrument's
   channels, thresholds, or admission rules.
4. **Acceptance suite frozen:** script sha256 committed BEFORE dispatch
   (checks: imports; respects cap_calls; deterministic under fixed
   seeds; declared classes syntactically present). ANY acceptance
   failure ⇒ terminal `HOLDOUT_INVALID_GENERATION`: no regeneration, no
   script edits, published as "holdout infrastructure failure", the
   primary result stays internal-validation-only. Raw-response
   extraction rules, timeout, and accepted formats are part of the
   frozen script.
5. **Plaintext isolation (review W5, the serious leak):** the raw
   response is encrypted ON RECEIPT to a public key committed in
   advance — via the custodian path: the receiving browser session's
   sole outputs are (a) ciphertext, (b) plaintext sha256, (c)
   acceptance PASS/FAIL from the frozen script run in the same session.
   Neither author reads the plaintext or detailed acceptance output
   before release. Until release, the repository holds only:
   `receipt_exists, acceptance_status, ciphertext_hash, plaintext_hash`.
6. **Commit DAG (strict order, each step signed):**
   (1) locked prereg + full analysis code + Appendix R certifications →
   (2) θ-bundle from OC-tune + OC-validate outputs →
   (3) this file's prompt bytes + hash, provider rule, acceptance
   script + environment hash, escrow public key, failure semantics →
   (4) custodian commits ciphertext + hashes + acceptance status →
   (5) primary locked run → (6) publication of decision.json, prereg
   hash, and the raw-log manifest to the preregistered immutable public
   location (the ascesis GitHub repository, tagged release) →
   (7) decryption key released → (8) holdout run, zero pipeline
   changes, published regardless of outcome.
   **"Published" means step (6) — a public tagged release; a local or
   rewritable commit does not release the key (review W 3.5).**

## What kills the holdout's validity

Any second generation; any prompt/acceptance-script edit after step (3);
provider deviation from the frozen fallback rule; any author reading
plaintext before step (7); decryption before step (6); pipeline changes
between primary and holdout; upgrading holdout-CLEAN beyond the
applicability-domain scope (schedule-adaptive languages only).
