# SPEC_IMPLEMENTED: Blind Consequence-Feeder Viability

Source memo: `/home/master/Documents/my/Blind_Consequence-Feeder_Viability_Experiment_memo.md`.

Status: implementation contract for this toy experiment. The memo is broader than a single small harness; this file states what is actually implemented.

## Mission

Test whether a blind consequence-only feeder has any non-trivial viability kernel under adversarial capture, delayed consequence observation, catastrophe ambiguity, mutation, migration, and diversity pressure. The result may be negative, fragile, or inconclusive.

## Implemented Substrate

- Environment: 12 graph zones arranged as a ring with cross-links.
- Hidden types: `dove`, `hawk`, `mutant`, `scavenger`.
- Hidden state: type populations, resource stock, wellness, productive capacity, catastrophe timer, penalty timer.
- Feeder observation: delayed zone-level consequence records only: wellness, productivity, response to previous aid, recovery, diversity, observed feature proxy, delayed capture-like signal, and local/global scale summaries.
- Type-blind guard: policy code receives a `FeederObservation` object with no type composition fields. Hidden type is used only by simulator dynamics and metrics.
- Policies: `feature_proxy`, `scalar_welfare`, `geometric_diversity`, `local_consequence`, `local_global`, `response_to_aid`, `audit_penalty`, `always_cut_sagging`, `always_aid_sagging`, `monoculture_optimizer`.

## Implemented Experiment Families

- A: baseline adversarial collapse map, no catastrophes, no mutations.
- B: fixed-observation-noise delay separation with MI measured post hoc.
- C: neighbor consequence comparator: feature proxy vs realized consequence vs response-to-aid vs local+global.
- D: catastrophe ambiguity: sag can mean capture or shock.
- E: scavenger hawk exploitation of catastrophe aid.
- F: diversity corridor under later shock.
- G: broad random viability-kernel search over held-out seeds.

## Primary Metrics

The run reports permanence, collapse, extinction by type, capture, Herfindahl concentration, mean/min/geometric welfare, recovery time, adversarial resource share, mutation survival, Shannon diversity, false-positive punishment, false-negative aid-to-hawk, signal-truth correlation, mutual information, delay, and `R = T_irrev / tau`.

## Viability Criterion

A cell is counted as viable only if held-out aggregate metrics satisfy all:

- `collapse_probability <= 0.20`;
- `capture_probability <= 0.20`;
- `dove_extinction_probability <= 0.10`;
- `adversarial_share_mean <= 0.35`;
- `mean_welfare_final >= 0.55`;
- `diversity_mean >= 0.45`;
- `audit_cost_share_mean <= 0.25`;
- `permanence_probability >= 0.60`.

This is intentionally strict and may yield an empty kernel.

## Literature Grounding Used for Interpretation

- Viability theory: Aubin, J.-P. (1991), *Viability Theory*.
- Networked/delayed control: Zhang, Branicky & Phillips (2001), “Stability of Networked Control Systems”; Hespanha, Naghshtabrizi & Xu (2007), “A Survey of Recent Results in Networked Control Systems”.
- Safety and maximum allowable delay framing: networked control literature uses maximum allowable transfer interval / delay bounds; this experiment does not claim novelty there.
- Mutual information: Cover & Thomas (2006), *Elements of Information Theory*. MI here is a discrete plug-in estimate for diagnostics, not a publication-grade estimator.
- Reward hacking / Goodhart: Skalse et al. (2022), “Defining and Characterizing Reward Hacking”.
- Audit / Stackelberg security games: Blocki et al. (2013), “Audit Games”.
- Diversity and shock resilience: Elmqvist et al. (2003), “Response Diversity, Ecosystem Change, and Resilience”; Yachi & Loreau (1999), biodiversity insurance hypothesis.

## Anti-Self-Deception Notes

- Feature-proxy success is reported separately and not treated as consequence success.
- Failed seeds remain in raw CSV.
- Train/held-out seeds are fixed; no tuning is performed in this first implementation.
- Any viability kernel found here is a toy result and should be treated as a candidate for falsification in stronger substrates.

## Source Links

- Aubin, *Viability Theory* / viability kernel overview: https://en.wikipedia.org/wiki/Viability_theory
- Zhang, Branicky & Phillips (2001), networked control delay/stability: https://doi.org/10.1109/MCS.2001.949138
- Hespanha, Naghshtabrizi & Xu (2007), networked control systems survey: https://doi.org/10.1109/JPROC.2007.904027
- Cover & Thomas, *Elements of Information Theory* grounding: https://en.wikipedia.org/wiki/Information_theory
- Skalse et al. (2022), reward hacking: https://arxiv.org/abs/2209.13085
- Blocki et al. (2013), Audit Games: https://arxiv.org/abs/1303.0356
- Elmqvist et al. (2003), response diversity/resilience: https://doi.org/10.1890/1540-9295(2003)001[0488:RDECER]2.0.CO;2
- Yachi & Loreau (1999), biodiversity insurance hypothesis: https://doi.org/10.1073/pnas.96.4.1463
