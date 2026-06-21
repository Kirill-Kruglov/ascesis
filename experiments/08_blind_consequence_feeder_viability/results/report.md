# Blind Consequence-Feeder Viability Report

Final verdict: **C. Apparent kernel exists but is too fragile / tuned to trust.**

## 9.1 Did any non-trivial viability kernel exist?

Viable held-out cells under the strict implemented criterion: `57` / `147`.

## 9.2 If yes, what conditions were necessary?

Viable policies: `['always_aid_sagging', 'always_cut_sagging', 'audit_penalty', 'feature_proxy', 'geometric_diversity', 'local_consequence', 'local_global', 'monoculture_optimizer', 'response_to_aid']`.
Median R among viable cells: `2.000`.
Median adversarial strength among viable cells: `0.450`.
Median diversity floor among viable cells: `0.000`.
Artifact warning: trivial or feature-proxy policies also passed (`['always_aid_sagging', 'always_cut_sagging', 'feature_proxy', 'monoculture_optimizer']`), so the apparent kernel is not isolated to blind consequence feeding.

## 9.3 If no, what killed it?

- diversity below floor: `79` cells
- adversarial capture: `13` cells
- adversarial share: `7` cells
- low welfare: `2` cells

## 9.4 Did R behave like a useful invariant?

Choice: `D. Inconclusive.` R/permanence corr `0.110`, MI/permanence corr `-0.132`.

## 9.5 Was consequence-neighborliness better than feature-neighborliness?

Feature-proxy mean permanence: `0.200`. Consequence-family mean permanence: `0.419`. Difference: `0.219`.

## 9.6 Did diversity help or hurt long-run permanence?

In experiment F, diversity_floor/permanence corr: `0.000`. This is diagnostic only; diversity is not assumed beneficial.

## 9.7 What should be tested next?

- Replace the toy population dynamics with a stronger ecological substrate and preserve the same type-blind observation API.
- Sweep response-to-aid probes under adversarial channel control rather than fixed probe floors.
- Use a better MI estimator and explicit fixed-MI construction before drawing conclusions about R.
- Stress-test any viable cells with more held-out seeds and shifted catastrophe distributions.

## Best Held-Out Cells

| viable | experiment | policy | permanence | capture | collapse | adv share | welfare | diversity | R |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | C | feature_proxy | 1.000 | 0.000 | 0.000 | 0.100 | 1.000 | 0.677 | 2.000 |
| 1 | C | local_consequence | 1.000 | 0.000 | 0.000 | 0.098 | 1.000 | 0.675 | 2.000 |
| 1 | C | response_to_aid | 1.000 | 0.000 | 0.000 | 0.099 | 1.000 | 0.676 | 2.000 |
| 1 | C | local_global | 1.000 | 0.000 | 0.000 | 0.098 | 1.000 | 0.675 | 2.000 |
| 1 | D | always_cut_sagging | 1.000 | 0.000 | 0.000 | 0.068 | 1.000 | 0.615 | 2.000 |
| 1 | D | always_aid_sagging | 1.000 | 0.000 | 0.000 | 0.068 | 1.000 | 0.617 | 2.000 |
| 1 | D | response_to_aid | 1.000 | 0.000 | 0.000 | 0.068 | 1.000 | 0.617 | 2.000 |
| 1 | D | local_global | 1.000 | 0.000 | 0.000 | 0.068 | 1.000 | 0.617 | 2.000 |
| 1 | D | always_cut_sagging | 1.000 | 0.000 | 0.000 | 0.068 | 0.999 | 0.615 | 2.000 |
| 1 | D | always_aid_sagging | 1.000 | 0.000 | 0.000 | 0.068 | 0.999 | 0.617 | 2.000 |

## Literature Grounding

The implementation report cites viability theory (Aubin), networked/delayed control (Zhang/Branicky/Phillips; Hespanha/Naghshtabrizi/Xu), information theory (Cover & Thomas), reward hacking (Skalse et al.), audit games (Blocki et al.), and response diversity / biodiversity insurance (Elmqvist et al.; Yachi & Loreau). The toy code does not claim novelty over those fields.

## Source Links

- Aubin, *Viability Theory* / viability kernel overview: https://en.wikipedia.org/wiki/Viability_theory
- Zhang, Branicky & Phillips (2001), networked control delay/stability: https://doi.org/10.1109/MCS.2001.949138
- Hespanha, Naghshtabrizi & Xu (2007), networked control systems survey: https://doi.org/10.1109/JPROC.2007.904027
- Cover & Thomas, information theory grounding: https://en.wikipedia.org/wiki/Information_theory
- Skalse et al. (2022), reward hacking: https://arxiv.org/abs/2209.13085
- Blocki et al. (2013), Audit Games: https://arxiv.org/abs/1303.0356
- Elmqvist et al. (2003), response diversity/resilience: https://doi.org/10.1890/1540-9295(2003)001[0488:RDECER]2.0.CO;2
- Yachi & Loreau (1999), biodiversity insurance hypothesis: https://doi.org/10.1073/pnas.96.4.1463
