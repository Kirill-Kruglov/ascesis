# Archive Index

Frozen pointers to closed branches and superseded framings. Nothing here is live.
Full texts live in git history; this index gives the reason and the commit to
retrieve them from. Keep this file thin: add a row when something is closed or
superseded, do not paste the old text back in.

## Closed branches

The canonical list, with reasons and evidence, is `../rejected_branches.md`. Most
recent closure: `non-scalar-agent-mechanically-outperforms-hedger` (closed in
commit `ca99c23` after Tests 02 and 06).

## Superseded framings

| superseded framing | replaced by | retrieve from |
|---|---|---|
| Active spine "non-maximizing core with incomplete preferences wins" | narrowed spine, then two successors (existence / detection) in `status.md` | `structure.md`, `questions.md` at or before commit `5fcc1e2` (2026-06-18) |
| "incompleteness beats hedging" as a performance claim | closed; see `status.md` "What is closed" | `structure.md`, `experiments/validation_summary.md` before commit `ca99c23` |
| `questions.md` three active-spine strata (Active Spine Questions / Bet-Hedging Challenge / Narrowed Active Spine After Experiment Validation) | consolidated into `status.md` frontier; `questions.md` keeps only durable questions | `questions.md` before the 2026-06-19 consolidation commit |

## How to read a superseded version

```sh
git show <SHA>:ascesis_of_learning_grace/<file>
```
