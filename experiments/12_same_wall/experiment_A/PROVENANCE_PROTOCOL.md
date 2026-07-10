# C7 provenance protocol (registered BEFORE receiving any external code)

Purpose: make "independent build" a checkable construction, not an
assigned label. This file is committed before the independently-built
implementations exist; their arrival must not modify it.

## Registered builds and authors

| Build | Author | Channel | Status |
|---|---|---|---|
| A (algebra, origin scan) | Claude (this repo) | existing `lang_A` | registered |
| A/G-translated | Claude | to be DERIVED from A via the Cayley map — the registered DEPENDENT sham | to build |
| **G-independent** | **Codex GPT 5.5, FRESH SESSION (no history)** | spec-only (see `CODEX_SPEC.md`); never sees this repo's code | commissioned |
| References W, M | Claude (scout 09) | existing | registered |
| New references (2–3) | Codex, same fresh session | spec-only | commissioned |

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
