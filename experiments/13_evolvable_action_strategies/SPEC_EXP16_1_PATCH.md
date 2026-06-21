# SPEC_EXP16.1 (PATCH): Fix marginal metric + decide dual-lever vs coupled mechanism

Status: patch on Experiment 16. Two jobs:
1. **Fix the marginal-gap bug** (gap_AC ≡ gap_CG artifact).
2. **Run the one ablation** that decides whether the working mechanism is two
   independent levers (AC + CG) or a single *consequence-gated* anti-concentration
   response. This is the honest crux; do not skip it.

Same constraints as Exp16: no new substrate dynamics; reuse existing flags,
seeds, CI helpers; deterministic; `--smoke` supported.

---

## A. Fix the marginal gap (bug)

`paired_gap` currently differences `is_viable_run(r)` — a strict 9-condition
binary that requires `permanence == 1.0`. Because A (`anti_hhi_allocator`) and
B (`delayed_harm_throttle`) almost never reach perfect viability, both gaps
collapse to `mean(is_viable(C))`, so `gap_AC ≡ gap_CG` and they read ≈0 wherever
even C rarely hits perfect viability. This is a metric bug, not a finding.

Fix: compute the paired gap on the **continuous per-run `permanence`** value, not
on `is_viable_run`.

```python
def paired_gap(rows, world, axis, axis_label, va, vb):
    a = {r["seed"]: r["permanence"] for r in rows if r["world"]==world and r["axis"]==axis
         and r["axis_label"]==axis_label and r["policy15"]==va}
    b = {r["seed"]: r["permanence"] for r in rows if r["world"]==world and r["axis"]==axis
         and r["axis_label"]==axis_label and r["policy15"]==vb}
    seeds = sorted(set(a) & set(b))
    diffs = [a[s] - b[s] for s in seeds]
    lo, hi = normal_ci(diffs)
    return safe_mean(diffs), lo, hi, len(diffs)
```

- `gap_CG = perm(C) - perm(A_rep)` (value of consequence feedback over static caps)
- `gap_AC = perm(C) - perm(B_rep)` (value of the concentration limit over pure CG)

This is an analysis-only change: re-run with `--analyze-existing` (A/B/C boundary
runs already exist; no new simulations needed for Part A).

**Acceptance:** `gap_AC` and `gap_CG` are no longer identical row-by-row; report
both with CIs. Update the verdict's `pos_ac`/`pos_cg` checks to use the new
values (CI-lo > 0 somewhere).

---

## B. The deciding ablation: is anti-concentration consequence-gated?

In this substrate the load-bearing AC (the dynamics `anti_concentration` lever)
only acts inside a `containment` episode, and containment is triggered by
`_bad_consequence`. So AC may be **structurally unable to act without CG**. If so,
"AC + CG both required" is partly tautological and must be reframed.

Add one variant, **`C_dyn_no_consequence`**, built from existing flags only:

- caps OFF (`use_caps=False`, like `C_dyn_only`)
- dynamics `ablation = "full"` (anti_concentration lever available)
- **consequence machinery removed**: do not fire the `_bad_consequence`-triggered
  containment in `choose_alloc`, and use an allocation score with the
  anti-concentration + `need` terms only (drop the `delayed_harm` throttle term,
  i.e. no `-bad` penalty, no consequence-weighted neighbor term).

Run on the 3 robust worlds (W6, W3, W4) at default **and** along
`adversarial_pressure`, with the core boundary seed set.

Instrument and report, per cell:
- `permanence`, `robust`, `capture`, `welfare` for `C_dyn_no_consequence`
  alongside `C_dyn_only` and `C_full`.
- `containment_events` and `containment_timer` activity for
  `C_dyn_no_consequence`. Derive the analysis flag:

  `structural_ac_requires_consequence_gate = (mean containment_events for
  C_dyn_no_consequence ≈ 0)` — i.e. the dynamics anti_concentration lever never
  engages without a consequence trigger.

---

## C. Interpretation / verdict

Extend the verdict logic and report with the coupling finding:

- If `C_dyn_no_consequence` **collapses** (not robust) **and**
  `structural_ac_requires_consequence_gate` is True →
  **`BE: the working mechanism is consequence-gated anti-concentration (a single
  coupled lever), not two independent levers.`** State plainly that AC here is a
  consequence-triggered structural response; static always-on caps are redundant
  (Exp16 BD) and pure consequence throttling without the structural response also
  fails (Exp15 Part B).
- If `C_dyn_no_consequence` **stays robust** → the dynamics AC works without any
  consequence trigger → CG is **not** necessary given dynamics AC; report
  **`BG: anti-concentration alone (dynamics form) is sufficient; re-open Part A.`**
  (Surprising; would partly reverse Exp15 — flag loudly if seen.)
- Otherwise keep `BD` and append: "CG-necessity-given-AC not cleanly isolable in
  this substrate; see coupling analysis."

Keep all Exp16 validation gates. Add gate
`coupling_question_answered = True` (the C_dyn_no_consequence cells exist and the
flag is computed).

---

## D. Outputs

- `raw/cg_ablation.csv` — `C_dyn_no_consequence` / `C_dyn_only` / `C_full` per cell
  with `permanence`, `robust`, `capture`, `welfare`, `containment_events`.
- `raw/marginal.csv` — regenerated with the permanence-based gaps.
- `sensitivity_report.md` — add a **## Lever Coupling** section: the ablation
  table + `structural_ac_requires_consequence_gate` + the chosen verdict.
- `run_manifest.json` — add `structural_ac_requires_consequence_gate`,
  `coupling_question_answered`, and the (possibly updated) `final_verdict`.

## Notes

- Part A is pure re-analysis (no sims). Part B adds only the one new variant on a
  small grid (3 worlds × adversarial grid × core seeds). Print `num_cases` first.
- Do not soften an honest `BE`/`BG`. A reframed thesis is more valuable than a
  defended one — this patch exists precisely to find out which thesis is true.
