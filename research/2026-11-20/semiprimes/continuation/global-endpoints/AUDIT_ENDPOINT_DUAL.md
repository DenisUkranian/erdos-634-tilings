# Independent audit of finite-support endpoint duals

20 November 2026. Audited `global_obstruction/verify_endpoint_dual.py`
and `construct_5063/global_signed_pricing.py` in the current workspace.
No nonexistence certificate is asserted by this audit.

## The global certificate principle is valid

For each unoriented axis ell and point P assign a rational weight w(P,ell),
zero except at a finite set of pairs. An oriented edge P->Q on ell has
score w(P,ell)-w(Q,ell). This definition reverses sign under edge reversal
and telescopes under arbitrary subdivision. Hence in every actual tiling,
including T-junctions, the sum of tile scores equals the outer boundary
score B. A support point in the interior of a through-edge introduces no
extra term: the two subdivision terms there cancel.

If a tile has nonzero score, at least one of its vertices P and one
incident side axis ell must be a nonzero support row. For a specified
P and ell, all placements of a fixed scalene triangle are determined by
choosing its side length on ell (three choices), the length of the other
side at P (two), the direction along ell (two), and the half-plane for its
third vertex (two). There are exactly 24 placements. No orientation-height
cutoff or translation lattice is used in this argument. In particular,
arbitrary real rotations and translations of a hypothetical tiling are
covered: a tile avoiding all support pairs has score zero.

Let M be the maximum of zero and the scores of all these contained
candidates. If the target has area N times the tile area, then

    B > N*M

is an unrestricted nonexistence certificate for this target and tile.
The case B>0 and M=0 is its simpler special case. N must be computed from
the exact target area and tile metric, or otherwise checked exactly.
Zero must be included in M because placements avoiding the support score
zero even when every explicitly enumerated score is negative.

The updated verifier also uses a valid stronger bound: sort all positive
candidate scores and sum the largest N, padding with zeros if necessary.
An actual tiling uses N distinct geometric placements, so this bounds its
score sum even without checking mutual non-overlap among those maximizers.
The canonical sorted vertex triples correctly deduplicate placements.
For the intended boards N is an integer; a noninteger exact area ratio
already prevents a tiling by itself.

## Metric and catalogue check

In axial coordinates x+y*rho, squared Euclidean norm is x²+xy+y².
For a unit vector u=(x,y), the vector (-x-2y,2x+y) is perpendicular to u
and has squared norm three. With a chosen edge length L and adjacent
length A, the projection of the third vertex is

    (L²+A²-B²)/(2L),

where B is the remaining tile length. The perpendicular coefficient is
ab/(2L), because a 120-degree (a,b,c) tile has area ab*sqrt(3)/4.
These are the formulas used by the independent verifier.

I also extracted the engine's helper functions without running its LP
and compared its inverse-row catalogue to this independent metric
catalogue. For all three triples (33,7,37), (35,13,43), and (5,3,7), at
heights -2, 0, and 3, all three unoriented phases, and a nonintegral
rational anchor, the sets agreed exactly and contained 24 placements.
The six endpoint rows agreed exactly up to the sign convention below.

## Sign convention must be converted

The engine's `tile_rows` and `needs` are the negatives of the verifier's
counterclockwise `rows`. To preserve a positive boundary score when
converting an engine dual into the verifier's input format, negate all
endpoint weights. This was confirmed by the exact catalogue comparison.

## Boundary arithmetic is an optional, justified strengthening

The engine's `legal` predicate also imposes integer side-distance and
nonnegative a,b,c coin-sum conditions on vertices lying on exterior sides.
The initial verifier uses pure containment instead. A certificate passing
the latter stronger test is valid without this extra input; an engine
candidate can fail that stronger test despite being valid with the
additional boundary restrictions.

The restrictions are necessary for a tile that actually appears in a
tiling. A tile vertex on an exterior side cannot be strictly inside the
side of a different boundary tile: that other tile would occupy the
entire inward half-disk and overlap the first tile near the point.
Thus the vertex is an endpoint of the exterior full-edge partition.
The distances to both exterior corners are sums of a,b,c side lengths.
For a certificate using this restriction it must be stated and checked
explicitly, rather than calling the reduced set all physically contained
placements.

## LP limitations

The restricted-master optimum, initially eight negative units at 5063,
is not a lower bound for the unrestricted problem before exact global
pricing establishes the certificate inequality. New positive columns can
lower it. Finite-support duals need not exist merely because an integral
tiling is impossible: the LP also permits fractional tile coefficients.
No termination or completeness of the column-generation search is claimed.

A floating zero objective gives a candidate fractional solution. It is
not an exact geometric tiling without exact reconstruction, integrality,
and appropriate coverage verification. Conversely, an exact dual
certificate does not depend on LP optimality or numerical tolerances:
only the exact finite-support maximum and strict final inequality matter.

The engine's precomputed powers through c^256 are an implementation
resource limit, not a proof restriction; deeper coordinates would raise
an indexing error. The inverse-row pricing rule itself has no fixed
orientation-height cutoff. The finite seed lookup through heights -60 to
60 is only a seed parser, not the global pricing catalogue.

## Remaining validation

A proposed final certificate must be passed through the independent exact
checker using the agreed sign convention and explicit boundary mode.
Until that succeeds, no claim of nonexistence for 5063 or 3431 follows.

The updated checker's self-tests passed. I additionally used the exact
143-tile positive control, transformed back out of the eta coordinate
scaling, with six deterministic random finite-support endpoint weight
assignments. Three tests used pure containment, three used the additional
boundary arithmetic. All six correctly rejected the putative obstruction,
including under the stronger top-N score bound.
