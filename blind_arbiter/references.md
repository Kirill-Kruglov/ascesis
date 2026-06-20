# References — Blind Type-B Arbiter

Field ownership for this direction. The substantive content belongs to these fields and their
originators; this package only proposes one bridge between them (an active, type-blind arbiter
defending true permanence under signal-gene decoupling) and tests it in a toy. No novelty is
claimed.

## Population dynamics, equilibria, and permanence

- Maynard Smith, John. 1982. *Evolution and the Theory of Games* (ESS; Hawk-Dove).
- Hofbauer, Josef, and Karl Sigmund. 1998. *Evolutionary Games and Population Dynamics*
  (permanence in replicator dynamics).
- Nowak, Martin A., and Karl Sigmund. 2005. "Evolution of indirect reciprocity." *Nature* 437.

## Mechanism design under hidden types / monitoring

- Myerson, Roger B. 1981. "Optimal Auction Design" / mechanism design under private types.
- Holmstrom, Bengt. 1979. "Moral Hazard and Observability" (reacting to outcomes, not types).
- von Stackelberg, Heinrich. 1934. *Marktform und Gleichgewicht* (leader-follower commitment;
  the arbiter commits to a dispensing rule, the population best-responds).

## Goodhart, reward hacking, and the safety/liveness frame (shared with the trail)

- Manheim, David, and Scott Garrabrant. 2018. ["Categorizing Variants of Goodhart's Law"](https://arxiv.org/abs/1803.04585).
- Lamport, Leslie. 1977. "Proving the Correctness of Multiprocess Programs"; Alpern, Bowen, and
  Fred B. Schneider. 1985. "Defining Liveness" (non-collapse = safety; progress = liveness;
  liveness needs a fairness assumption — here, `R > R*`).
- Aubin, Jean-Pierre. 1991. *Viability Theory* (the largest set from which collapse is avoidable
  for all time — the formal home of the permanence floor).

## Telos and value pluralism (why a keeper, not an optimizer)

- Arrow, Kenneth (1951) and Sen, Amartya (1970) — no clean scalar aggregation of plural values.
- Sen, Amartya. 1999. *Development as Freedom* (progress as expansion of capabilities/freedoms,
  not maximization of a scalar).
- Ord, Toby. 2020. *The Precipice* (the long reflection: do not lock in a value target).
- Baron & Spranca (1997); Tetlock et al. (2000) — protected / sacred values (non-tradeable
  axes; the adversarial vs protected structure modelled here as a toy).

The shared Goodhart, safety/liveness, and telos fields are recorded with thesis-to-source
flags in `../ascesis_of_learning_grace/field_check.md` (nodes 11-30). The population-dynamics
and mechanism-design entries (Maynard Smith, Hofbauer & Sigmund, Nowak & Sigmund, Myerson,
Holmstrom, Stackelberg) are credited here in this self-contained package and are not yet in the
sandbox field_check; adding them there is a pending step before any publication-grade use.
