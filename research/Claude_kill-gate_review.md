I now have everything I need. Two of the files your prompt listed do not exist — `research/playbook/03_preservation_rule.md` and `research/playbook/04_repository_philosophy.md` are absent (the playbook dir holds only `00`, `01`, `02`, and `README`). `00_monograph_kill_gates.md` exists but is eight empty headers. I reviewed everything else against the actual evidence files. Here is the hostile review.

---

# Semantic Kill-Gate Review

## Verdict

`pause_and_reframe`

## Strongest Failure Mode

The programme has silently changed its own Goal Anchor and then claimed continuity. The *actual* original objective, recorded in `BRIDGE_MAP_18_1_TO_FA2.md:37-41`, was "to construct an analytically understandable and **safety-faithful** substrate suitable for future LLM training" — the alignment/feeder/Justitia line the root `README.md` and `status.md` describe as the telos ("build AGI/ASI and not collapse"). `substrate_discovery_v1` quietly drops both *safety* and *LLM*: `RA-0` rewrites the anchor as a learner that "acquires an internal world model by interacting with lawful structure," and `RQ0` (`01_research_question.md:74-77`) strips it further to "a computationally bounded learner," with `01_research_question.md:53-61` explicitly declaring Justitia, CEGAR, theorem proving, physics and robotics *not* the research object. The word "safety" and "alignment" effectively vanish from all nine substrate chapters. So a research line motivated by AI alignment has reframed itself into a generic question in computational learning theory — "does there exist a class of computable environments where building an internal model is information-rational" — which is system identification / model-based RL / computational mechanics under a new label. The negative results (JB0, FA2.5, 18.1) that supposedly *motivate* this pivot say nothing about world-model emergence; they close *Justitia-as-safety-abstraction*. The drift is real, it is exactly the failure `RA-0`/`09_Open_Problems.md:OP-G4` was written to prevent, and it is dressed in enough disciplined formatting (status tags, kill-gates, level discipline) to look like rigor while the load-bearing analytical work has not been done.

## Findings by Severity

### Critical

- **Goal drift, alignment → epistemology of environments.** See Strongest Failure Mode. `RA-0` (`00_research_axioms.md:36-38`) vs `BRIDGE_MAP_18_1_TO_FA2.md:37-41` vs `Door1_Extracted_Knowledge_v1.md:35-37`. Three different phrasings of the "unchanged" anchor, each dropping a different load-bearing word (safety; LLM; internet-text-imitation). An anchor that is restated three ways is not anchored.
- **Nine chapters of scaffolding written ahead of the programme's own mandated reductions.** `RA-4` ("Analytical Before Computational"), `SG-2`, `PK-3` and `DG-4` all demand that a new concept be checked against existing theory before investment. Not one such reduction has been executed. `04_Derivability.md` stamps "Needs literature review" (`:112`) and lists `DG-4` (reduce to MDL / Kolmogorov / PSR) as open — then the programme proceeds to build chapters 05–08 on top of the unreduced concept anyway. The kill-gates exist and have not been fired. This is the project's own anti-Goodhart discipline being violated in form-compliant clothing.

### High

- **"Derivability" is coined before reduction, against the project's own no-novelty genre.** `04_Derivability.md` itself admits it "overlaps with each" of prediction/compression/generalisation/planning/interpretability and may reduce to MDL/computational mechanics/PSR. The repo memory records this project as explicitly *anti-novelty* ("no novelty/credit claims"). Coining a new term while its reducibility kill-gate is open is internally inconsistent with that stance. Under their own RA-7, elegance/compactness ≠ evidence — and a compact new word is not evidence either.
- **"Necessary Properties" (chapter 06) titles 12 properties as necessary; none is established.** Every P-item is tagged "working hypothesis" or "open question" or "critical hypothesis." Calling them *necessary* in the heading while the body proves necessity for zero of them is precisely the overclaim the harness is supposed to catch. P6 (model advantage) and P10 (no dominant proxy) are not independent environment properties at all — they restate the goal ("the environment must be one where model-based beats lookup"), so they cannot be used to *screen* candidates without circularity.
- **Evidence-to-programme inference is a scope non-sequitur.** `JB0/.../final_report.md` cleanly establishes `Conservative_but_vacuous`, FPR 0.54, "Justitia should NOT remain a Door-1 substrate candidate." `FA2_5/.../final_report.md` establishes `No_discriminative_candidate`, `Equivalent_to_standard_history_refinement` (precision margin −0.084). `18_1/.../summary.md` establishes projection blindness (false-safe 0.299; 19.3% already-collapsed states labeled SAFE). All three are about **abstraction fidelity for a safety boundary**. None is evidence about **world-model emergence / derivability**. The substrate programme inherits the *prestige* of these rigorous negatives without inheriting their *scope*. `Door1_Extracted_Knowledge_v1.md:261-270` even states the experiments "did NOT falsify the original objective" — correct — but the programme then changes the objective and reuses the same negatives as motivation.

### Medium

- **"Computable environment" definition partitions nothing.** `03_Computability_of_Environment.md:80-103` defines environment = computable generator of observations/interventions/consequences, then `:59-72` concedes every candidate considered already satisfies it. A definition that excludes no candidate does no analytical work; it is a relabeling of POMDP / interactive transition system. The 11-class taxonomy (`C1–C11`) is explicitly "not a partition" and "descriptive" — i.e., it cannot reject anything.
- **Interaction/identifiability chapter is textbook causal inference re-derived.** `05_Interaction_and_Identifiability.md:140-157` ("observational equivalence does not imply computational equivalence; intervention distinguishes them") is the standard interventional-identifiability result (Pearl do-calculus, optimal experimental design, system identification). The chapter admits the relation (`:201-216`) but treats these fields as "sources of tools" rather than as prior art that may already answer RQ2/RQ3. The reduction is acknowledged, never performed.
- **Playbook is at risk of becoming ritual, and there is already one instance.** `00_monograph_kill_gates.md` is eight headers, zero content. The substrate corpus is the cautionary example: it carries every ritual marker (Status, RA-axioms, kill-gates, level discipline) yet defers all substance. Form is being mistaken for the work.

### Low

- **Two referenced playbook files do not exist** (`03_preservation_rule.md`, `04_repository_philosophy.md`); `00_monograph_kill_gates.md` is an empty skeleton. Fine as scaffolding, but nothing should cite them as if they constrain anything.
- **`RA-12`/Level discipline is asserted but unused.** The five-level hierarchy (`00_research_axioms.md:175-197`) is restated in `07` and `08` but no actual candidate has been run through it, so its value is unproven.

## Concept Kill Table

| concept                                   | risk                                                                                                                       | kill condition                                                                                       | recommendation                                                                                                            |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| internal model                            | Defined via "generalises beyond memorisation" — the entire open problem (`OP-A1`,`OP-A4`); circular with substrate success | No implementation-independent measure of "internal model" is ever produced                           | Block as success criterion until `OP-A4` (measurement) is solved; until then the programme has no definable win condition |
| computable environment                    | Restates POMDP / interactive TM; excludes no candidate (`03:59-72`)                                                        | Show the definition rejects at least one candidate class                                             | Demote to "working vocabulary," not a result                                                                              |
| derivability                              | Load-bearing novelty; admitted overlap with MDL/Kolmogorov/PSR/computational mechanics (`04`)                              | `DG-4`: reduces to an existing quantity                                                              | **Run DG-4 now.** Prefer existing math (computational mechanics ε-machines, MDL, PSR) unless a residual is proven         |
| lawful interaction / lawful stochasticity | "Stable computational structure" = stationarity + realizability; not new                                                   | Show a case the classical stationary/realizable framing cannot express                               | Reduce to existing terms                                                                                                  |
| necessary properties (P1–P12)             | None proven necessary; titled "necessary" anyway; P6/P10 circular with goal                                                | Demonstrate necessity for ≥1 property (a substrate violating it that provably cannot induce a model) | Rename "Conjectured Desiderata"; block from monograph as "necessary"                                                      |
| model advantage (P6)                      | Strongest/most testable, but is model-based-vs-memorization regret gap — standard                                          | `NP-2`: memorization matches model-based given budget (often provable)                               | Keep, but frame explicitly as environment+budget-relative, citing model-based RL                                          |
| proxy-world failure (RA-10, P10)          | The real, sharp idea — but asserted as axiom, not shown                                                                    | `IG-1`/`IG-3`: rich passive observation yields equal interventional generalization                   | Convert RA-10 from axiom to a falsifiable empirical claim and test it in one toy                                          |

## Evidence Assessment

| claim                                                                         | evidence                                                                                               | weakness                                                                                                        | verdict                   |
| ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- | ------------------------- |
| Justitia is not a usable Door-1 safety substrate                              | `JB0` Conservative_but_vacuous, FPR 0.54; `FA2.5` No_discriminative_candidate; `18.1` false-safe 0.299 | None — pre-registered, honest, clean                                                                            | **Strong / supported**    |
| Compression ≠ discrimination; complexity ≠ fidelity; layer discipline matters | `FA2/FA2.5`, `BA2`, `BA4` layer audit                                                                  | None of substance; well-supported                                                                               | **Strong / supported**    |
| Justitia investigation "significantly narrowed the search space"              | claimed in `01_research_question.md:30-32`, `09_Open_Problems.md:42-66`                                | Narrowed the space *for Justitia-as-safety-abstraction*; does not transfer to world-model-inducing environments | **Overinterpreted**       |
| These negatives motivate a substrate-discovery / derivability programme       | `01_research_question.md`, `RA-*`                                                                      | Scope leap: fidelity-of-safety-abstraction evidence ≠ world-model-emergence evidence                            | **Unsupported inference** |
| Substrate programme preserves the original goal                               | `RA-0`, `Door1:263`                                                                                    | Anchor restated three ways, each dropping safety / LLM / imitation; alignment telos absent from all 9 chapters  | **Weak / drifted**        |
| The 12 properties are necessary                                               | `06_Necessary_Properties.md`                                                                           | Zero proven necessary; two are circular restatements of the goal                                                | **Unsupported**           |

## First Five Programme Kill-Gates

**KG-1 — Derivability reduction gate.**
- *Hypothesis attacked:* derivability is a genuinely new concept (`04`).
- *Failure condition:* it is expressible as MDL / algorithmic statistics / computational-mechanics causal states (ε-machines) / PSR with no measurable residual.
- *Required evidence:* a written reduction against each named formalism, plus one toy where derivability and the closest existing measure are computed and shown to differ.
- *Consequence if failed:* drop the term; rewrite chapters 04–08 in existing vocabulary. No new substrate chapters until this is run.

**KG-2 — Goal-anchor identity gate.**
- *Hypothesis attacked:* the programme still serves the alignment telos.
- *Failure condition:* the operative object is generic "does an environment induce a world model," with no decision that depends on safety/corrigibility.
- *Required evidence:* a single sentence anchor, and a derivation showing at least one programme decision changes if the safety clause is removed.
- *Consequence if failed:* either re-anchor to alignment, or explicitly declare the pivot to "epistemology of model-inducing environments" and stop importing the alignment framing and the Justitia negatives as if they transfer.

**KG-3 — Internal-model measurability gate.**
- *Hypothesis attacked:* programme success is definable (`OP-A4`).
- *Failure condition:* no implementation-independent measure of "internal model" exists.
- *Required evidence:* an operational measure that distinguishes Learner A (10M memorized trajectories) from Learner B (100 rules) in `04`'s own thought experiment, on held-out interventions.
- *Consequence if failed:* the success criterion is vacuous; freeze the programme until a measure exists.

**KG-4 — Proxy-world discriminability gate (tests RA-10 itself).**
- *Hypothesis attacked:* "learning descriptions is fundamentally different from learning lawful structure" (`RA-10`).
- *Failure condition:* in one minimal toy, a learner on rich passive/description data matches an interaction learner on interventional generalization.
- *Required evidence:* the toy, pre-registered, both learners, an interventional held-out test.
- *Consequence if failed:* RA-10 is downgraded from axiom to refuted-in-this-regime; the central LLM motivation needs requalification.

**KG-5 — Necessity gate.**
- *Hypothesis attacked:* the P-properties are necessary, not merely desirable (`06`).
- *Failure condition:* no property can be shown necessary (no substrate exists that violates it yet still induces a model — or the converse cannot be argued).
- *Required evidence:* one constructive necessity argument for one property.
- *Consequence if failed:* retitle to "Conjectured Desiderata"; block the word "necessary" from the monograph.

## What To Preserve

- The **BA/FA/JB evidence chain and decision JSONs** — genuinely rigorous, pre-registered, honest negatives. First-class.
- **`Door1_Extracted_Knowledge_v1.md`** FACT/INFERENCE/HYPOTHESIS discipline and the empirical design checklist (`:237-256`).
- The **BA4 layer audit** — concrete, code-grounded, transferable beyond Justitia.
- **`RA-3` / RA-5 / RA-6** (negative knowledge, status-tagging, mandatory kill-gates) — keep as method.
- The **proxy-world question** (RA-10) — the one sharp, alignment-relevant, sharpenable idea — but as a *falsifiable claim*, per KG-4, not an axiom.
- The **methodological inversion** (necessary-properties-before-implementations, `07`) — defensible even if generic.

## What To Downgrade

- **`03`, `06`, `07`, `08`** → from "active charter / framework" to **speculative pre-reduction notes**, blocked from monograph inclusion until KG-1/KG-2 fire. `03` and `06` carry the least irreducible content.
- **`04_Derivability.md`** → marked speculative; the term must not enter the monograph as established.
- **`06` title** → "Conjectured Desiderata"; strip "necessary."
- **`00_research_axioms.md` RA-0** → rewrite to a single unambiguous anchor that states whether safety/alignment is in or out.
- **`00_monograph_kill_gates.md`** → mark explicitly as empty skeleton; nothing may cite it as a live constraint.

## What To Do Next

1. Fire **KG-2** (one sentence: is this still alignment, or is it now computational-learning epistemology?). Everything downstream depends on the answer; do not write another chapter first.
2. Fire **KG-1** and **KG-3** as desk work (no engineering): the literature reduction of derivability, and an operational internal-model measure. These are exactly the `RA-4` analytical steps the programme owes itself.
3. Only after 1–3, run **KG-4** as the first cheap toy — it is the one experiment that directly tests the load-bearing RA-10 thesis and ties back to the LLM motivation.
4. Stop expanding the chapter set. The corpus is currently form-rich and substance-deferred; adding chapters deepens the sunk cost in possibly-redundant concepts.

The discipline here is real and the negatives are excellent. The problem is not sloppiness — it is that a disciplined harness has been pointed at a target that quietly moved, and the programme wrote its kill-gates without firing them. Pause, fire KG-1 through KG-3, and re-anchor before continuing.

Semantic kill-gate review complete.