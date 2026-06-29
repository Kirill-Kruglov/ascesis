# Claude Code Task — Experiment 18.0: Shield Synthesis from the justitia Boundary

**To:** Claude Code
**From:** Claude (analyst), via Kirill
**Repo context:** the justitia simulation lives at https://github.com/Kirill-Kruglov/justitia (model/substrate.py, model/atlas.py). Read the actual code first; do not assume field names from this spec.

---

## Why this experiment exists (read first)

The project's special theory (final, honest form): an LLM trained on states drawn from a **safe boundary** is safer than one trained on unfiltered states, even though content *inside* the boundary is generalized, not derived. The boundary's value is the filtering of the domain, not derivation of meaning.

That whole theory rests on one unproven precondition: **the justitia collapse-boundary must be expressible as a decidable safety invariant** — i.e. a shield can be synthesized for it. If it cannot, the special theory is dead before any training, and we save all downstream work.

This experiment tests exactly that precondition and nothing more. **Do not train any model. Do not build an LLM. Do not render language. Only test whether the boundary is a synthesizable shield.**

Analytic background (already established on paper, now to be verified computationally):
- **scales** (anti-concentration: limit how much influence piles up) → an *upward-closed* unsafe set: if concentration c is unsafe, any c' ≥ c is unsafe. This is the canonical WSTS/coverability shape — likely decidable.
- **sword** (response to *observed* harm) → reachability of an observed-harm threshold; monotone if accumulated harm does not spontaneously decrease.
- **the coupling** (scales gated by sword) → WSTS-with-storage; decidable **only if the sword's corrective reaction is bounded** (reduces harm by a finite amount, never resets arbitrarily). The reaction is the danger point: an unbounded "improvement" transition breaks monotonicity and kills decidability.

The single danger to watch: the sword reacting (lowering harm/concentration) introduces a *non-monotone* transition. Whether the system stays decidable hinges on whether that reaction is bounded.

---

## The single question

> Can the justitia collapse-boundary be synthesized as a decidable safety shield via backward reachability — and specifically, does the sword's corrective reaction preserve the monotonicity (well-quasi-ordering) that decidability requires?

Three honest outcomes, all valuable:
- **shield_synthesizable** — boundary is decidable; backward reachability terminates; special theory's precondition holds → proceed to 18.1.
- **shield_fails_unbounded_reaction** — sword reaction breaks monotonicity; coverability does not terminate → boundary is not a WSTS shield as-is; special theory needs a bounded-reaction reformulation before any training.
- **shield_fails_not_upward_closed** — the collapse set is not upward-closed in any natural ordering → the boundary is not a safety invariant of this class at all; deeper problem.

---

## Method (from simple to complex, per the discipline)

### Step 0 — Read and characterize the justitia substrate
Read model/substrate.py and model/atlas.py. Extract, in your own words in `outputs_18_0/substrate_characterization.md`:
- the state variables (what defines a configuration);
- the transition dynamics (how a step changes state);
- how "collapse" / "unsafe" / "non-permanent" is defined in the existing code (the essay calls the key metric "welfare of the worst-off region" and uses a permanence/survival measure — find the actual computational definition);
- the two referee powers (scales = concentration limit; sword = consequence-gated response) as they appear in code.

Do not proceed until the collapse condition is precisely identified in the actual code.

### Step 1 — Define the unsafe set and test upward-closure
- Express the collapse condition as a set U of states.
- Define a candidate ordering ≤ on states (the natural one: component-wise on concentration / accumulated-harm coordinates — higher concentration and higher harm are "≥").
- **Test computationally** whether U is upward-closed under ≤: sample states in U, perturb each toward "worse" (more concentration, more harm), check they remain in U. Sample states near the boundary, check monotonicity of membership.
- Output `outputs_18_0/upward_closure_report.json`: fraction of U-states whose upward-perturbations stay in U; any counterexamples. If U is not upward-closed → classification `shield_fails_not_upward_closed`, stop with that finding.

### Step 2 — Test transition monotonicity (the sword danger point)
- For the transition relation T, test the WSTS monotonicity condition: if s ≤ s' and s→t, does s' reach some t' ≥ t?
- **Isolate the sword reaction:** identify transitions where the referee lowers concentration/harm. Measure the magnitude of each reaction. Is it bounded (≤ some constant per step) or can it reset arbitrarily large amounts?
- Output `outputs_18_0/monotonicity_report.json`: fraction of transition pairs satisfying monotonicity; distribution of sword-reaction magnitudes; whether any reaction is unbounded.
- If monotonicity holds (with bounded reaction) → continue to Step 3. If unbounded reaction breaks it → classification `shield_fails_unbounded_reaction`, and report what bound *would* restore monotonicity (this is the reformulation hint for the next iteration).

### Step 3 — Backward reachability (the actual shield synthesis)
- Implement coverability via backward reachability: start from the unsafe set U (its minimal elements under ≤), iterate the predecessor operator pre(·), accumulating the upward-closed set of states that can reach U.
- Use the WSTS termination guarantee: under a genuine wqo with monotone transitions, the backward iteration stabilizes in finitely many steps.
- **Termination is the result.** Record: number of iterations to fixpoint; size of the computed "doomed" set (states that inevitably reach collapse); whether iteration terminated or hit a step cap.
- Output `outputs_18_0/backward_reachability_report.json`: iterations, fixpoint reached (bool), size of doomed set, size of safe set.
- The shield itself: for each state, the set of actions/transitions that do NOT lead into the doomed set. Output a sample of the shield as `outputs_18_0/shield_sample.json`.

### Step 4 — Sanity controls
- **Positive control:** a trivially decidable sub-case (e.g. scales-only, no sword) MUST synthesize cleanly. If even scales-only fails, the implementation is wrong, not the theory.
- **Negative control:** deliberately inject an unbounded reaction and confirm the monotonicity test catches it (Step 2 must flag it). This proves the test discriminates, not just passes.

---

## Outputs (`outputs_18_0/`)

```
substrate_characterization.md       # what the justitia code actually is
upward_closure_report.json          # is the collapse set upward-closed?
monotonicity_report.json            # do transitions stay monotone? sword reaction bounded?
backward_reachability_report.json   # does coverability terminate? doomed/safe set sizes
shield_sample.json                  # sample of the synthesized shield
control_report.json                 # positive (scales-only) + negative (injected unbounded) controls
final_decision.json
summary.md
```

`final_decision.json`:
```json
{
  "classification": "shield_synthesizable | shield_fails_unbounded_reaction | shield_fails_not_upward_closed",
  "upward_closed": true/false,
  "monotone": true/false,
  "sword_reaction_bounded": true/false,
  "backward_reachability_terminated": true/false,
  "iterations_to_fixpoint": ...,
  "doomed_set_fraction": ...,
  "blocking_issue": "... or null",
  "reformulation_hint": "... if a failure, what bound/ordering would fix it"
}
```

`summary.md` must answer:
1. What is the collapse condition in the actual justitia code (not the essay's metaphor)?
2. Is the unsafe set upward-closed? Under what ordering?
3. Is the transition relation monotone? Is the sword reaction bounded?
4. Did backward reachability terminate (= shield synthesizable)?
5. If it failed, what is the precise blocking issue and the reformulation hint?
6. Does the special theory's precondition hold — can we proceed to 18.1?

---

## Hard constraints (discipline)

- **No training, no LLM, no language rendering.** This is purely shield synthesis.
- **Read the real justitia code; characterize the actual collapse condition.** Do not implement against the essay's metaphors (scales/sword/soil) — implement against the code's actual variables and the actual permanence/collapse computation. If the code's collapse definition differs from the essay, trust the code and note the discrepancy.
- **Positive and negative controls are mandatory.** A synthesis that "succeeds" without the negative control proving the monotonicity test can fail is not trustworthy (lesson from 15.x: an instrument that cannot detect failure cannot confirm success).
- **Termination is the honest signal.** If backward reachability hits a step cap without a fixpoint, that is `shield_fails` (likely unbounded reaction), not "probably fine — increase the cap." Do not chase termination by raising caps; diagnose why it didn't terminate.
- **Determinism and seeds** throughout. Tests for the upward-closure and monotonicity checks (hand-built monotone case must pass; hand-built unbounded-reaction case must be flagged).

---

## How this connects to the goal (keep in README)

The project's special theory is: train an LLM inside a safe boundary so the model never learns collapse-trajectories — safer than internet-trained, even if content inside the boundary is still generalized rather than derived. That theory is worthless if the boundary cannot be made into a decidable shield. This experiment tests that one precondition, cheaply, using the justitia code that already exists — before any training is attempted. If the boundary synthesizes, we have earned the right to test whether training inside it actually helps (18.1). If it does not, we have saved ourselves the entire training program and learned exactly what must be reformulated.
```