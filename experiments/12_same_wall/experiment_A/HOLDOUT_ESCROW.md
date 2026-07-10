# Holdout escrow protocol (fixed BEFORE the locked run; review Y §4.5)

Purpose: the locked run's world family is a development set (16 scouts
of adaptive use). Any confirmation claim requires a holdout that the
authors could not have tuned to — and that the authors' knowledge of
the primary outcome cannot retroactively shape. Escrow closes the
adaptive-holdout leak: the holdout exists, encrypted, in git history
BEFORE the primary run.

## Steps (owner: Kirill + Claude; every step committed)

1. **Prompt freeze.** The commissioning prompt for the holdout agent is
   written and its sha256 recorded in this file BEFORE contacting any
   agent. The prompt requests: (a) a new world family in the same
   interface (words over {R,L}, equality oracle), with truth semantics
   stated per world; (b) a set of solver pairs with DECLARED classes —
   at least one derived pair, one REVERSED-derivation pair (direction-
   invariance test, review X 4b), one clean-room independent pair;
   (c) mechanical self-checks. The prompt never describes the
   instrument's channels or thresholds.
2. **Provider rule.** Fixed now: a model family NOT used for any
   registered build's main path in the primary run where available;
   fresh web session, different account where possible; zero filesystem
   access. Exactly ONE generation; no regeneration, no human veto
   (mechanical acceptance only: the file imports, respects cap_calls,
   is deterministic under fixed seeds — checked by a script committed
   before receipt).
3. **Escrow.** The received file is encrypted (age/GPG, key held by
   Kirill offline) and committed BEFORE the locked primary run. The
   plaintext sha256 is recorded at commit time.
4. **Decryption** happens only after the primary outcome (decision.json,
   harness-signed) is committed. The decrypted file's sha256 must match
   step 3.
5. **Holdout run**: the same locked pipeline, zero changes; results
   published regardless of outcome, in the same E/D/N/P vocabulary.

## What kills the holdout's validity

Any second generation; any prompt edit after step 1; human rejection of
the received world as "unsuitable" on outcome-relevant grounds;
decryption before the primary outcome is committed; pipeline changes
between primary and holdout runs.
