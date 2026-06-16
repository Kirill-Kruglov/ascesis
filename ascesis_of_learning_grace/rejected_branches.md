# Rejected Branches

Closed branches are retained as part of the research map. A closed branch is not treated as useless material; it records a path that was checked and a reason it should not lead the current public spine.

| branch | reason closed | evidence |
|---|---|---|
| Optimizing/maximizing core + non-optimizing wrapper (shell/container) | Closed as the main design direction. If the wrapper is inside the optimization loop, proxy pressure can drive toward constrained-optimization corners and bypass the intended shell. If the wrapper sits outside inference, it is not itself Goodharted in the same way, but becomes vulnerable to masking, test awareness, and strategic silence. | `field_check.md` node 11; Skalse et al. 2022; Gao, Schulman, Hilton 2022; Karwowski et al. 2023; Wang et al. 2026. |
| Search for a better optimizer / better container around an optimizing model | Closed for the current spine. It keeps the maximizing core as the object to be rescued, while the active spine moves the pressure point to training a non-maximizing core. | `field_check.md` node 11; `structure.md` active-spine candidate. |
| seL4-as-containment-for-superintelligence | Closed as a containment claim. seL4 and capability security can improve implementation isolation and authority boundaries, but they do not specify semantic alignment or contain an unbounded stronger agent. | `field_check.md` nodes 7 and 10; `structure.md` bridge 1. |
| paradox-cage | Closed as a control mechanism. Contradiction or paradox is not a reliable cage for a stronger reasoner; it can be bypassed, reframed, or treated as an input-domain defect. | `field_check.md` node 7; dialogue trace around `dialog.part_4.md:23` and `dialog.part_16.md:25`. |
| pure-faith-as-foundation | Closed as a technical foundation. Trust, commitment, or method discipline may matter socially, but they do not replace field ownership, verification limits, incentive design, or explicit guarantees. | `field_check.md` nodes 1, 3, and 7; `glossary.md` definition of `Ascesis`. |
| natural-language-as-core | Closed as a core specification strategy. Natural language remains useful at the expressive boundary, but the core safety claims require formal or executable representations plus explicit loss/refusal handling. | `field_check.md` nodes 6 and 9; `structure.md` bridges 5 and 6. |
| all-seeing-sandbox | Closed as a total-oracle claim. Sandboxing has a finite predictability horizon; more simulation does not remove chaotic divergence, undecidability, or specification limits. | `field_check.md` node 8; `structure.md` bridge 9. |
| quantum-as-general-answer | Closed as a general alignment answer. No-cloning and quantum-token work can support narrow unforgeable-state questions, not behavior, cognition, correctness, or alignment. | `field_check.md` node 4; `structure.md` bridge 8. |

## Current Replacement Spine

The current active spine is `non-maximizing core with incomplete preferences` in a bottom-up AGI governor. This is not a claimed result. It is a working direction produced by the convergence of social-choice impossibility and Goodhart/reward-hacking limits, with the main open question left explicit: how to train a non-maximizer rather than wrap a maximizer.
