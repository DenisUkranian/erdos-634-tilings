# Independent review of unmatched nodes, gates, and strip lowering

20 November 2026. Reviewed
[UNMATCHED_NODES_AND_GATES.md](UNMATCHED_NODES_AND_GATES.md),
SHA-256 `4867f2a9724527acbab08b357bcbdffd7e609db55a395849e6ee3622518460da`.
This is a proof review. No new computational search was performed.

**Assessment.** I found no gap in the stated unmatched-node theorem,
closed-gate lemma, population accounting, or the no-lowering argument
for the displayed balanced `2c` strip. The distinction between a
complete tiling and a partial packing is essential and is maintained.
These results do not prove impossibility of either full F2 target.

## Whole-edge matching and completeness

At an exterior-free empty child `w`, the no-vacant-ancestor theorem
removes all occupied descendants. Every tile meeting the maximal
height-`w` run has its edge node at `w`, by the integral-offset lemma.
Its short node is `w` itself or adjacent to it. The only occupied
possibility is the parent `v`; thus every bank interval has length
`c`. Exterior-freeness removes a one-bank outer interval. In a
complete finite tiling both banks cover the same entire run and have
common endpoints, so their equal-length partitions coincide.

No absence of ungenerated placements or local catalogue completeness
is used here. Completeness is the explicit hypothesis of the full
hypothetical tiling. The note correctly refuses to infer an unmatched
edge from an ungenerated mate.

In the unmatched-node theorem, cancellation of the node's paired
long edges leaves its complete short-edge boundary chain. Nodewise
cancellation then replaces this chain by whole neighboring `c`-edges
at the one fixed height. The resulting closed chain has nonzero
signed area, rather than merely nonzero formal edge multiplicity.
This excludes a decomposition consisting only of backtracks. Within
one endpoint component, all vertices lie on one translated unit
`c`-mesh, so a simple supported cycle can be extracted. Partial
overlaps with another translated component do not invalidate the
cycle in the chosen component.

## Population accounting

The bounds `U_v>=|G_v|` and `U_v=n_v (mod 2)` follow from removing
half-turn pairs of opposite signs. For an odd number of `c`-blocks,
the signed quotient is odd, so `|G_v|>=c`; for an even population,
the positive unmatched count is at least two.

An activated exterior-free child costs its own population of at
least `2c`. The note charges distinct nodes only, uses unions of
required-node lists, and reserves outside populations separately.
It also correctly keeps the two prime-tree budgets separate. No
unjustified count of distinct edges as distinct gate populations
appears.

## The balanced strip cannot be lowered

In any replacement using only short heights at most `-1`, each
height-zero outer side must be covered by whole length-`c` edges
from short-height-`-1` tiles. Containment prevents a boundary edge
from extending past the side's endpoints. Hence the `a` equal base
intervals on each long side, and the corresponding inward teeth,
are forced; this step does not assume a particular interior mesh.

On each intermediate chord `P_iQ_i`, the left tooth in cell `i`
and the right tooth in cell `i-1` occupy opposite banks. Their edge
fractions `[0,a/c]` and `[1-a/c,1]` cover the whole chord because
`2a>c`. A remaining tile interior cannot cross any point of this
barrier: crossing would put a positive neighborhood inside one of
the forced teeth. Since the chord connects the two outer sides,
every remaining tile is confined to a single closed cell.

The two forced teeth in a cell have disjoint interiors and each
has unit area. The cell area is `2c/a`, leaving
`2(c-a)/a` tile units. This quantity is positive and below one for
all three listed shapes. Thus the positive remainder in a cell
cannot contain even one whole remaining tile. This argument needs
no assumption that the remainder is connected, nor any bound on its
number of components: all components together have area below one.

The strip is therefore a valid obstruction to the proposed local
lowering operation. Its existence as a partial packing, or its
failure to admit that particular replacement, establishes no full
F2 completion or nonexistence claim.
