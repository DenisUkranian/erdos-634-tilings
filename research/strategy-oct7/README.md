# Three routes to a complete classification: execution and decision gates

7 October 2026. Research directed by Denis Paliy, with ChatGPT assistance.

The task is a necessary-and-sufficient structural criterion for every
positive tile count N. Fixed-N decidability, verification of a supplied
placement, and sufficient tails are already available and are not the
missing classification. **This continuation does not solve the full task.**

## What was tested

| Route | Decisive proposed step | Result of this execution | Remaining obligation |
| --- | --- | --- | --- |
| A: global geometric normalization | Replace a whole tiling, preserving the unit tile, target and scale, by an explicitly constructible parameterized form | [Audit](plan-a.md): one short height is impossible in I120. A bounded height window gives a precise finite lattice, but does not ensure positive completion. No valid global replacement was established | Prove an actual replacement operation and completeness of its constructive forms. A bound on heights alone leaves a second major theorem |
| B: same-count parameter descent | Move each hard candidate to another primitive tile or branch with an existing construction | [Arithmetic audit](plan-b.md): 4830 is F3-only, scale one, and has exactly one ordered primitive tile, `(24,11,31)`. The F2/beta coefficient identity transfers the small-scale problem rather than resolving it | A conditional reduction restricted to actual tilings would require a new geometric obstruction; unconditional arithmetic reassignment cannot handle all candidates |
| C: geometric positivity | Detect or forbid every positive-area overlap by a uniform tractable condition | [Moment theorems](plan-c.md): every fixed moment degree fails even with distinct contained placements. Degree 2N does certify a given N-placement | Find a uniform positive obstruction or an ordered-seam theorem controlling existence across the unresolved parameter families. Increasing a fixed moment order is not enough |

The proofs in the three notes were separately reconstructed and checked
internally. This is not external peer review or proof-assistant verification.

## New general conclusions from route C

For every d there is a contained collection of `(d+3)^2` **distinct**
congruent triangles which matches every area moment and every directional
boundary moment through degree d, while having positive-area overlaps.
The construction uses exact algebraic translations and Newton identities.
An additional grid construction gives rational-coordinate counterexamples
at `4^(d+1)` tiles. Both preserve the exact orientation inventory.
The target in each case also has a genuine tiling: these are failures to
certify the proposed placement, not examples of untileable counts.

Conversely, for a specified collection of N positively counted triangles,
matching every signed directional boundary moment through degree 2N is
sufficient for a genuine tiling. Isolating each supporting line and using
the Vandermonde matrix proves equality of boundary measures; the compactly
supported coverage discrepancy then has zero distributional gradient and
vanishes. No prior nonoverlap, area, or containment assumption is needed
for this sufficiency implication.

The growing bound is an exact verification theorem. It does not choose
the unknown placements and therefore does not classify N.

## The next two or three research turns: realistic milestones

1. **Primary effort: a constructive global form, not another scalar
   invariant.** Work first in an indispensable unresolved branch, F3 or W.
   Require an explicit replacement preserving the unit scale and the
   ambient boundary. Test its universal statement against the existing
   nonconvex-island and gamma-partition counterexamples before building a
   proof around it. Stop the route if the proposed move needs unjustified
   purity, convexity, or extraction of a chosen macro region.
2. **Prove positive completion as part of the same theorem.** Every
   admitted parameter must come with a disjoint covering construction;
   every rejected parameter must be excluded for arbitrary T-junctions.
   If the first step yields only a height bound or another finite search,
   the classification milestone has not been reached.
3. **Audit all-branch coverage.** Use route B to check alternative tiles
   before calling any count impossible. Use route C and the disk checker
   to certify actual constructions. A solved branch must still be joined
   to the other necessary rows, including the infinite primitive F3 front
   and the unresolved small Group-1 and double-angle scales.

Route A has the broadest possible payoff but currently lacks its decisive
geometric operation. Route B should remain a limited arithmetic audit.
Route C is a verification tool unless a new parameter-uniform inequality
is found. No successful proof chain presently makes completion in two or
three more turns predictable. The unresolved examples 154 and 4830 remain
useful tests, but resolving those two alone would not settle the infinite
remaining families.

## Exact supplementary checks

Run from the repository root:

```sh
python research/strategy-oct7/check_plan_b.py
python research/strategy-oct7/check-plan-c.py
```

The first checks the exhaustive 4830 divisor list and 4578 primitive
ordered arithmetic samples. The second checks exact bivariate moment
integration for degrees 0 through 6 and root isolation/Newton identities
for degrees 0 through 20. The proofs of the universal assertions are
written in the notes; their validity is not inferred from the samples.
