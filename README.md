# Ascesis

`Ascesis` is a working code name. The final name may change.

This repository is a research trail for AI-alignment thinking, organized as honest bridges
between areas usually discussed as separate bodies of work (formal verification, capability
security, instrumental convergence, corrigibility, selective prediction, social choice,
Goodhart/reward hacking, evolutionary dynamics, mechanism design, and related fields). It is
not a scientific paper, not a claim of contribution, and not a claim of novelty. The value, if
any, is in the proposed bridges and in the honest path — both of which live in the commit
history as much as in the current files. Every field is credited to its originators before any
local label is used.

## How the repository is organized

- **Sandbox — the working trail.** This is where the trial-and-error research happens.
  - [`ascesis_of_learning_grace/`](ascesis_of_learning_grace/): the map and research memos.
    Start with [status.md](ascesis_of_learning_grace/status.md) for the current frontier and the
    standing discipline; [field_check.md](ascesis_of_learning_grace/field_check.md) is the
    field-ownership layer. The sandbox is kept lean: stale material is deleted rather than
    tidied, since the full record stays in git history.
  - [`experiments/`](experiments/): small, reproducible toy tests, each pre-registered with a
    `SPEC.md` before running. Negative results and calibration failures are valid outputs.
- **Extracted directions — focused packages.** When a direction passes a minimal proof
  threshold in the sandbox, it is pulled into its own self-contained package (narrative, spec,
  field references, test, results) so it can be developed in focus and read on its own.
  - [`blind_arbiter/`](blind_arbiter/): the current active direction (below).

## Current direction: the blind arbiter

Can an AGI/ASI, modelled as an active **feeder** for a population rather than an optimizer of
"the good," keep that population in equilibrium when part of it is adversarial and actively
games the signals the feeder can see (reward hacking under hard optimization)?

Current result (a weak but real toy demonstration): an active, type-blind arbiter holds the
population's true permanence above a boundary `R* = horizon_harm / horizon_observation`,
**even when its observable signal has decoupled from the true types** — it defends the true
floor through its lagged reaction to consequences, not by reading the signal. Defending the
floor under this Goodhart pressure requires active intervention; a passive keeper does not hold
it. The boundary is the safety/development trade-off curve, and it holds in a majority (~0.6) of
held-out seeds, not always. See [`blind_arbiter/`](blind_arbiter/) for the spec, caveats, and
how to reproduce.

## Contributors

Kirill Kruglov (author and maintainer, who does the core work — proposing and testing
hypotheses by mind and intuition), Claude (Opus 4.8), and Codex (GPT-5.5). The two assistants'
contribution to the sandbox trail counts as much as to the extracted packages. See
[CONTRIBUTORS.md](CONTRIBUTORS.md) for roles.

## License

MIT. See [LICENSE](LICENSE).
