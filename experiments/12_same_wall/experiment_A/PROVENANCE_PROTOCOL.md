# C7 provenance protocol (registered BEFORE receiving any external code)

Purpose: make "independent build" a checkable construction, not an
assigned label. This file is committed before the independently-built
implementations exist; their arrival must not modify it.

## Registered builds and authors

| Build | Author | Channel | Status |
|---|---|---|---|
| A (algebra, origin scan) | Claude (this repo) | existing `lang_A` | registered |
| A/G-translated | Claude | to be DERIVED from A via the Cayley map — the registered DEPENDENT sham | to build |
| **G-independent** (`find_order_main`) | **GPT 5.6 high — WEB session, DIFFERENT ACCOUNT** (stronger than commissioned: zero filesystem access; different model version than the reviewer sessions) | spec-only (see `CODEX_SPEC.md`) | **received Jul 10**: `received/find_order_solvers.py`, sha256 `40c2493bf9837ded01137ccd5b8b62d8879065859db4e33ed0e13b1cc22ed44c` |
| References W, M | Claude (scout 09) | existing | registered |
| **gpt-B family** (`find_order_spec_encoding_b.py`: main linear+votes, ref1 gcd-ladders, ref2 random-pairs, ref3 Brent-like) | GPT family, WEB clean session | **encoding B** (`SPEC_ENCODING_B.md`) | **received Jul 11**: sha256 `4a9592e6…5ba48ca` |
| **opus-A family** (`find_order.py`: main linear+final-vote, ref1 R^k~R^2k gcd, ref2 random pairs, ref3 Brent+rho-AB) | **Opus 4.8 (Anthropic)**, clean session | encoding A (`CODEX_SPEC.md`) | **received Jul 11**: sha256 `e8a6f191…c57698f`. Declared: ref1 jitter is a stub (deterministic), stated in the author's memo |

**C8 factorial now covered:** (main, gpt-B) = same prior family ×
different encoding (SPEC_FORMAT axis); (A, opus-A) = same provider
family (Anthropic siblings: Fable authored A, Opus authored opus-A) ×
clean room (COMMON_PRIOR axis); (main, opus-A) = different prior × same
encoding; (gpt-B, opus-A) = both different. Registered NOTE: opus-A
sharing the Anthropic prior with A's author is the deliberate
common-prior cell, not a protocol violation. Reference bank now has 6
provenance units: W, M, P, GPT-A family, gpt-B family, opus-A family —
satisfying the review-Y minimum (≥ 5–6 external units).
| New references (`find_order_ref1/2/3`: Brent; birthday+gcd; divisibility lattice) | same GPT 5.6 session | spec-only | received (same file) |

**Recorded on receipt (before any run):** the four received solvers share
internal helpers (`_difference_pair`, `_model_screen`,
`_validate_candidate`, `_finalize`) — within the received file they form
ONE provenance family. For reference-field purposes their pairwise
co-adaptations are grouped as one construction, never counted as
independent edges (per the GPT review, §5). Against Claude's builds the
shared-code set is empty: common causes are W and I only, as required.
The isolation actually achieved exceeds the spec: web session (no
filesystem), different account, different model version — mechanical
enforcement of the clean room, replacing the declared-trust variant.

## Allowed common causes (exhaustive)

- **W** — the world itself (via the oracle's answers).
- **I** — the interface contract: `oracle(u: str, v: str) -> bool` over
  words in {R, L}; call budget `cap_calls`; return protocol
  `('VAL', m, confident) | ('AB',) | ('TO',)`; seed passed in, own PRNG.

Anything else shared is a protocol violation.

## Forbidden sharing

- Helper code, libraries beyond Python stdlib, probe-encoding conventions
  beyond the interface strings.
- PRNG streams, salts, seed schedules (each build seeds its own
  `random.Random(seed)` and nothing else).
- Sight of this repository: worlds, existing languages, detector
  internals, scouts, reviews.
- Tuning to the detector: the spec describes the TASK only, never the
  dependence metrics.

## Integration rule

Claude writes only a thin adapter (string words → world simulation) and
may not edit the received logic. The received file is committed verbatim
(hash recorded) before the adapter; any needed fix is requested from the
author, not applied locally.

## Causal graph (registered claim)

```
        W
        |
        I
      / | \
   pi_A |  pi_G-independent      A/G-translated: C --> both
      \ |
       C?   <- the experiment's question: is there a C edge
              between A and G-independent? The protocol asserts
              its absence by construction; v3 tests whether the
              channels report one anyway.
```

## Declared residual risks (published with any outcome)

1. Both authors are large language models; same-family training may carry
   correlated blindness (Fable review 2: "a thousand walkers with one
   brain"). Not removable at current team size; declared.
2. The Codex *reviewer* sessions saw detector internals. Mitigation: the
   builder session is fresh and spec-only. Residual: same underlying
   model as the reviewer. Declared.
3. The spec itself is authored by Claude and could leak design bias in
   wording. Mitigation: the spec describes task and interface only, and
   is committed for audit alongside this protocol.
