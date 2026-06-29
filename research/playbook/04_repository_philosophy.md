# Repository Philosophy

Ascesis is the research archive. It preserves the evolution of ideas, experiments, negative results, review packets, and reorganization history.

The intended architecture is:

```text
Ascesis
  -> Research Archive
  -> Playbook (future extraction)
  -> Justitia Runtime (external repository)
  -> Empirical Evidence
```

## Ascesis

Ascesis keeps the record of how research questions were formed, narrowed, rejected, and reorganized. It is not only a clean presentation layer; it is also the evidence trail.

## Research Archive

The research archive holds monograph material, postmortems, faithful-abstraction notes, substrate-discovery notes, and historical sandbox material. It preserves the evolution of ideas.

## Playbook

The playbook is a future extraction target. It should preserve reusable research procedure: pre-registration discipline, kill-gates, evidence ledgers, negative-result handling, review packets, and decision schemas.

The playbook is not yet a finished method.

## Justitia Runtime

The Justitia runtime line is external: <https://github.com/Kirill-Kruglov/justitia>.

Ascesis may preserve reports and evidence derived from Justitia, but the runtime implementation itself belongs in the external repository.

## Empirical Evidence

Experiment outputs, reports, decision JSON files, and raw/result folders are evidence artifacts. They should not be pruned during navigation work. Any future archive/delete policy should treat them as research evidence, not disposable build products.
