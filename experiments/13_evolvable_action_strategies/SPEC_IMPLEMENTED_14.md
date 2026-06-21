# SPEC_IMPLEMENTED_14: Robustness and Ablation of the Evolvable-Strategy Kernel

Source memo: `/home/master/Documents/my/Experiment-14_Robustness_and_Ablation_of_the_Evolvable-Strategy_Kernel.md`.

Status: robustness follow-up on Experiment 13. This runner imports the Experiment 13 evolvable-strategy substrate and does not add a new governance mechanism. It stress-tests the three Experiment 13 viable cells and writes outputs to `results_14/`.

## Seed Cells

The original viable cells under test are:

1. `W6_mutation_corridor` + `action_channel_containment`
2. `W6_mutation_corridor` + `consequence_plus_diversity`
3. `W1_proxy_goodhart` + `consequence_plus_diversity`

## Test Families

- Seed robustness: 100 held-out seeds per seed cell.
- Parameter neighborhood: adversarial pressure, mutation rate, delay, containment strength, catastrophe severity, initial exploitative mass, and initial resource concentration.
- Ablations: no containment, no diversity, no response-to-aid, no anti-concentration, no aid escrow, no migration friction, no replication throttle, no neighbor consequence, feature-proxy only, random allocation.
- R/delay sweep: delay and `T_irrev` grid, with MI band reported but no fixed-MI claim unless achieved.
- W2 pure-capture boundary search: exploitative mass, payoff pressure, mutation bias, containment strength, action-channel cost, and delay.

## Verdict Options

A. At least one Experiment 13 kernel is robust.

B. Kernels reproduce but are fragile/narrow.

C. Kernels fail under seed robustness.

D. Result invalid due to failed validation.
