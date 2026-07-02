# CL2.2 Prior Audit

- Evidence-eligible generic learner may assume only visible finite features and target rows during fit.
- It is forbidden to encode AID_i mechanics.
- It is forbidden to encode phase-indexed shock.
- It is forbidden to encode failed-zone mass drain.
- It is forbidden to encode CONSERVE restores mass.
- It is forbidden to call oracle functions.
- Encodes AID_i mechanics: `False`.
- Encodes phase-indexed shock: `False`.
- Encodes failed-zone mass drain: `False`.
- Calls oracle functions: `[]`.
- It differs from the CL2 RuleFamilyTransitionLearner because it uses generic subset tables and backoff, not a parameterized transition update family.
- The CL2 RuleFamilyTransitionLearner is diagnostic-only because CL2.1 showed it carries too much transition-family prior to support learner evidence.
