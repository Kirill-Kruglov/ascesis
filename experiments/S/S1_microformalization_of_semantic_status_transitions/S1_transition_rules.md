# S1 Transition Rules

## T1 — Birth

```text
raw expression + non-empty derivation_trace -> FORMED
```

If `derivation_trace` is empty:

```text
raw expression -> not admitted as Claim
```

T1 grants only `FORMED`.

## T2 — Formed to Poetic

```text
FORMED
+ evocative_or_metaphorical_use
+ consequence_obligations == empty
-> POETIC
```

Blocked if the claim asserts operational consequence without obligation.

## T3 — Formed/Poetic to Suspended

```text
FORMED or POETIC
+ apparent contradiction or underdefined ontology
+ identifiable possible extension path
+ not DANGEROUS
-> SUSPENDED
```

SUSPENDED is quarantine, not success.

## T4 — Suspended to Local

```text
SUSPENDED
+ explicit scope
+ explicit assumptions
+ object/model/scope extension
+ at least one consequence obligation
+ no active DANGEROUS flag
+ no active Goodhart flag blocking LOCAL
-> LOCAL
```

No consequence obligation means T4 is blocked.

## T5 — Local to Stable

```text
LOCAL
+ survived consequence tests
+ contradiction remains contained
+ adversarial paraphrase survives
+ population stabilization exists
+ at least one formal/external/operational anchor exists
+ no active Goodhart flags
-> STABLE
```

No single component can trigger T5 alone.

## T6 — Any Status to Killed

```text
any status
+ failed under declared scope
or incoherent extension
or contradiction cannot be repaired without laundering
or required consequence obligations fail
-> KILLED
```

`KILLED` is scoped. A future claim may be born with a different derivation and
scope, but the killed scoped version remains archived.

## T7 — Any Status to Dangerous

```text
any status
+ explosion risk
or arbitrary context creation
or pseudo-term laundering
or proxy optimization
or grammar-as-meaning promotion
or population-as-truth promotion
-> DANGEROUS
```

`DANGEROUS` blocks `STABLE`.

## T8 — Local Dualism

Two apparently conflicting claims may both remain `LOCAL` iff:

```text
scopes differ
or models differ
or tests differ
and consequence obligations are not collapsed
and contradiction_links are explicit
and neither claim licenses arbitrary inference
and no CONTEXT_PROLIFERATION_PROXY flag is active.
```

If the scopes/tests collapse into one shared commitment, T8 fails and T6 or T7
must be considered.

## T9 — Stable Downgrade

```text
STABLE
+ new contradiction under overlapping scope
or failed anchor
or failed consequence test
or Goodhart flag discovered
-> LOCAL / SUSPENDED / KILLED / DANGEROUS
```

Downgrade choice:

- to `LOCAL` if scope must narrow but consequences remain valid;
- to `SUSPENDED` if ontology or assumptions need repair;
- to `KILLED` if declared-scope tests fail;
- to `DANGEROUS` if the prior stability came from proxy abuse or contradiction laundering.

No semantic status is irreversible as global truth.
