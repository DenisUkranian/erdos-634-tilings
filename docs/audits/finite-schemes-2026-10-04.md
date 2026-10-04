# Finite-scheme continuation: scope and remaining implication

4 October 2026. Denis Paliy, research with ChatGPT assistance.
The requested completion of the broad finite-recipe hypothesis was not
obtained. Erdős 634 also remains unresolved by this investigation.

## Corrections to the route

The 3 October finite-scheme note incompletely described the earlier
archive. The 1 October unbounded-blocks manuscript already refutes a
universal bound on ordinary triangular/parallelogram grid blocks, even
when the tile and target may change with the count. The earlier
[archive reconciliation](research-2026-10-03.md) had recorded this.
The finite-scheme note now explicitly incorporates that negative result.

The selected broader proposal allows explicit parametric repetitions.
An unbounded number of flat grid regions does not refute it. Moreover,
a finite recursive description does not, by itself, bound its number
of orientations: a repeated operation can introduce further rotations.
The orientation test is necessary only for the subclass of recipes
with a uniform orientation bound. These quantifiers are now explicit.

## Separately checked deductions

The [capacity extension](../grid-capacity-and-orientations.md) proves
an unbounded lower bound for convex single-grid regions, and for
nonconvex single-grid regions with bounded boundary complexity. The
same explicit equilateral pairs have constructions with at most 18
rigid orientations. The positive band construction and the lower
bound were independently reconstructed, including the cyclic target
partition and all orientation prototypes. This separates block count
from orientation count; it does not settle the broad conjecture.

The [median-cut identity and area theorem](../height-cut-area.md) use
actual positive unions of tiles. The exact Group-1 direction subgroup
was retained: replacing it by an unrestricted Gaussian module would
give only an overapproximation. The exact cut lattice, chain signs,
closed-walk areas, and theta closure edges were separately checked.
T-junctions, different lattice cosets for different components, and
self-intersecting graph walks do not invalidate the area argument.

For consecutive theta parameters the resulting bound is 8t²
orientations in every existing tiling. It is uniform in the shape
parameter, but not in the scale t. Arithmetic endpoint tests alone
pass every integer theta scale and therefore cannot prove sufficiency.

## Other routes examined without a completion claim

Allowing the shape to change was checked against the complete candidate
overlist. There are arithmetic families with only one W candidate or
two difference-family candidates. This rules out an automatic overlap
shortcut, but does not by itself show that those candidates are
geometrically realizable. In particular an arithmetic overlist must not
be described as an unbounded family of unresolved geometric instances
without also applying the archived necessary seam-length bounds.

The source-to-relation argument in the separate density-zero manuscript
was reconstructed with protected whole-edge runs and unique incoming
links. That is an internal review of earlier material, not a newly
invented seam theorem. This publication does not change the scope of
the previously published density statement or import a full density
package under the cover of this continuation.

For pure inward islands, the natural continuous interchange of the two
short sides fails: with a fixed polygon and fixed c, area fixes ab and
c²=a²+ab+b² fixes their unordered pair. A successful chirality switch
would require a discrete retiling with new incidences. No such universal
retiling theorem or valid counterexample was obtained.

The [pure-island exchange argument](../pure-island-exchange.md) makes
that obstruction precise. In a convex pure island it also forces a
short-edge overlap interval with unequal separate a/b counts, of length
at least ab/gcd(a,b). The formal edge assignment at T-junctions,
integration on a disk, and signed-area contradiction were independently
checked. This identifies a necessary arithmetic exchange; it does not
perform the required chirality switch. Convexity must not be removed
when applying that theorem to the generally nonconvex cut regions.

## Exact unresolved implication

Neither the positive cut identity, the area congruences, nor a bound
depending on t supplies an alternative tiling with an absolute number
of orientations. Nor has a sequence been found for which every
alternative tiling requires unboundedly many orientations. Even settling
that intermediate question would not establish completeness for every
finite parametric recipe.

No new isolated count is presented as completion. No exhaustive search,
timeout, or manuscript title is used as proof of a missing implication.
The repository's `full_Erdos634_solved` status remains false.
