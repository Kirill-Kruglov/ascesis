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

Current result, after a strict audit: the non-spatial toy does **not** reliably hold
permanence. An earlier draft claimed an active blind arbiter "holds permanence above a boundary
R*"; the audit withdrew that — the permanence curve is non-monotonic and near coin-flip for the
best regime (geometric), with wide overlapping confidence bands and no sustained boundary, and
the signal is fully decoupled where it matters. What survives is an ordering of arbiter rules
(scalar < lexicographic < geometric): active balancing and reacting to lagged consequences help,
but do not amount to holding equilibrium. This is a weak/negative result — the harness catching
and correcting an overstated headline. See [`blind_arbiter/`](blind_arbiter/) for the corrected
spec, the audit, and how to reproduce.

## Contributors

Kirill Kruglov (author and maintainer, who does the core work — proposing and testing
hypotheses by mind and intuition), Claude (Opus 4.8), and Codex (GPT-5.5). The two assistants'
contribution to the sandbox trail counts as much as to the extracted packages. See
[CONTRIBUTORS.md](CONTRIBUTORS.md) for roles.

## Citation

If you draw on this repository, please cite it via the "Cite this repository" button
(generated from [CITATION.cff](CITATION.cff)). It is a research trail, not a peer-reviewed
publication; the most useful material for a researcher is often in the commit history.

Keywords: AI alignment, AI safety, AGI, ASI, Goodhart's law, reward hacking, corrigibility,
value pluralism, mechanism design under hidden types, replicator dynamics, permanence,
type-blind arbiter.

## License

MIT. See [LICENSE](LICENSE).
