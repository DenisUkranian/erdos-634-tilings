# Independent audit of the two-tree spine reduction

21 November 2026. Mathematical and source review, with no new search or
solver run. The existing exact positive-control report was inspected.

| Reviewed proof note | SHA256 |
|---|---|
| `SPINE_DICHOTOMY.md` | `dcd6c05222e84f624b8a819c6b07fa179bfd6b1e037714e726f14a9b75d72072` |
| `NATIVE_ENDPOINT_COMPLETENESS.md` | `9f893587a0feae27437dcfc9cf8fd3f664c111c9b70adf3cb8735e1917e27ea2` |
| `CLOSED_GATES_AND_NATIVE_THROUGH.md` | `006e7ab8ad2222c2d7c1a2a88359ace51b1f4ebd8792f7df8a21b9adcbec7650` |

**Assessment:** no mathematical defect was found in the three stated
reductions. They classify and exactly model one exhaustive branch of
the global dichotomy. They do not establish that this branch is
infeasible or remove the occupied-exterior-free branch.

## Exact classification in both trees

In the increasing-height tree, the exterior nodes lie on the chain
ending at the height-two outer node represented by `A`. In the other
tree they lie on the chain ending at the height-zero core. Requiring
both short nodes to be non-free gives `h<=2` and `h>=0` respectively.
The two valuation inequalities then give `q-A in z^h R`; at height
zero, translation by integral `A` has no effect. Conversely each of
the three displayed cells satisfies both inequalities.

This proves the exact equivalence with the cells `R,A+zR,A+z^2R`.
It uses the established global inclusion of vertices in `R[1/c]` to
exclude denominators at other primes. It does not presume occupied
intermediate nodes, a height bound, or the no-gap theorem. The same
classification of exterior-containing edge nodes is available when
checking a long gate.

## Catalogue and endpoint equivalence

The three containment inequalities follow directly by requiring all
three translated native offsets to satisfy `x>=0`, `y>=0`, and
`Bx+Ay<=AB`. Their signs, minimum/maximum choices and denominator
factors are consistent. Exact integer points in these bounded
template triangles enumerate the whole classified class. The row
interval enumeration is a finite completeness method; the catalogue
counts alone have no implication of tileability.

For sufficiency of the full endpoint system, the distributional
derivative of the signed interval function is zero on every supporting
line. Compact support removes the possible constant. The resulting
zero oriented boundary current makes the sum of tile indicators equal
to the board indicator almost everywhere. Nonnegative integrality
then forces multiplicity one, disjoint interiors, closed coverage and
exactly `N` selected placements. No separate edge-to-edge or pairwise
overlap assumption is required for this **full** system.

A partial set of complete rows remains only necessary. The note
correctly distinguishes a certified unguarded permanent-model UNSAT
from guarded UNSAT, timeouts and incomplete incident lists. The native
condition is applied in `Geometry.admissible`, so it persists in later
incident and corner expansions.

## Closed gates

If a long joint cell is outside the three native edge cells, its exact
node is exterior-free in at least one tree. Its adjacent non-free
short node must be its parent: the reverse relation would make the
long node an ancestor of an exterior node. The spine hypothesis leaves
the entire descendant subtree empty of short nodes.

On the corresponding maximal supporting run, every contributor must
therefore be a length-`c` side with that same parent short node. There
are no short-side contributors, occupied child contributors, or outer
intervals. Both banks partition the same finite run into equal lengths
`c`, starting at the same endpoint. Full matching follows, and the
same short height and hand identify the half-turn mate. Formula (1)
for the mate agrees with the midpoint half-turn of the obtuse vertex.

The implementation registers a placement before inserting its mate,
so the reciprocal insertion terminates. It imposes equality of their
selection variables, or excludes the original placement when its mate
is inadmissible. An open gate is not forced unmatched.

## Native through-tiles

At a T-junction the corner point is also an endpoint on the other
bank of the through-side's maximal supporting run. The common
integer-offset coordinate therefore makes its offset from a through-
side endpoint an integer strictly between zero and the side length.
Intersecting the exact containment interval with `1,...,L-1`, then
applying native admissibility, retains every actual through-tile.
Allowing a half-fan whenever one candidate survives is a necessary
relaxation; it does not assert that the surviving tile is selected.

The saved positive-control report checks all 26,654 native contained
143 placements against both phase trees, 120 actual closed-gate tiles
against their mates, and 38 actual through-contacts against the integer
and native tests. These checks support the implementation and preserve
the known full tiling. They do not replace the unrestricted proofs or
give a target verdict.

No residual proof error was identified. A future closing result must
still supply either a verified decision of the complete spine class
or a separate global argument; the other branch of the dichotomy
requires its own treatment.
