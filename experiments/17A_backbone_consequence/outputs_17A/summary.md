# Experiment 17A.1 - Adversarial Backbone Stress Test

## Decision

Classification: `Weak_backbone`.

Most analyzed classes fail under low-cost adversarial attacks.

## Run Parameters

- seed: 42
- num_dags: 500
- max_depth: 6
- max_analyzed_classes: 1200
- candidate_budget: 100
- beam_width: 8
- max_attack_budget: 4

## Required Questions

1. Can any frozen class be broken? Yes.
2. If yes, what is minimum attack cost? 1.
3. How many classes remain frozen under adversarial search? 108 / 1200.
4. Does a spectrum emerge? No.
5. Is GNS still constant? No; mean attack-AUC GNS=0.352917.
6. Which perturbation family is most destructive? P8_merge_internal_nodes.
7. Do attacks mostly break aliases or genuinely semantic classes? nontrivial broken classes=678, alias pair mean=0.345.
8. Do cross-DAG attacks behave differently? cross-DAG broken fraction=0.8591666666666666.

## Core Evidence

- analyzed classes: 1200
- broken classes: 1092
- surviving fraction: 0.09
- old GNS mean: 1
- attack-AUC GNS mean: 0.352917

## Baselines

- feature broken fraction: 1.0
- AST identity broken fraction: 0.8233333333333334
- random broken fraction: 1.0

## Minimal Broken Examples

| class_id | class_size | attack_cost | attack_auc_gns | nontrivial_pair_count | alias_pair_fraction | operators | representative |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 9e4ed1038f097ccf | 44 | 1 | 0.5 | 0 | 1 | Blocked;Independent | Blocked(N3, N2 \| N4) \|\| Independent(N3, N2 \| N4) |
| ec00257b27932151 | 45 | 1 | 0 | 2 | 0 | P_multi_do | P(N4 \| do(N0), do(N6)) |
| f2400457c55ff4a2 | 45 | 1 | 0.5 | 0 | 1 | Ancestor;Effect;Reachable | Ancestor(N3, N7) \|\| Effect(N3 -> N7) \|\| Reachable(N3, N7) |
| f937144f7ce51614 | 45 | 1 | 0.5 | 0 | 1 | Blocked;Independent | Blocked(N3, N2 \| N0) \|\| Independent(N3, N2 \| N0) |
| f96e064ba4ec3244 | 45 | 1 | 0.5 | 2 | 0 | P_multi_do | P(N1 \| do(N6), do(N4)) |
| febbbb49a55775b1 | 45 | 1 | 0.5 | 0 | 1 | Ancestor;Effect;Reachable | Ancestor(N5, N0) \|\| Effect(N5 -> N0) \|\| Reachable(N5, N0) |
| 0d94c52d6b7aa932 | 44 | 1 | 0 | 2 | 0 | P_obs | P(N0 \| N3) |
| 0ea947357d7ed7f7 | 44 | 1 | 0 | 2 | 0 | P_do | P(N4 \| do(N9)) |

## Honesty Notes

- This is adversarial search over bounded candidate sequences, not exhaustive graph-edit enumeration.
- The verifier and consequence signatures are unchanged from Experiment 16.
- Same-DAG synchronous attacks and cross-DAG one-sided attacks are both measured.