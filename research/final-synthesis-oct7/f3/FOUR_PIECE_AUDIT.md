# Independent audit of the four-piece obstruction

7 October 2026. Independent internal review by a separate assistant agent.
This is not external human review or formal verification.

**Verdict: PASS, including positive real scales.** The reduction to rational
scales is valid in the stated rational-coordinate setting. Restricting the
theorem to integer scales is unnecessary.

## Integer and rational scales

For primitive c²=a²+ab+b² with a even, b and c are odd. Reduction modulo8
then gives 8|a. The displayed quadrilateral is convex: its four consecutive
edge determinants are positive for a>b>0. Its area is 3ab tile areas, and
the side lengths b(2a+b),bc,bc,b(a−b) are all odd integers.

A sum of at most four integer squares divisible by8 has no odd base.
Indeed, with h odd bases the residue is h+4k modulo8; for 1≤h≤4 and
0≤k≤4−h it is never zero. Iteration of this fact forces each macrotriangle
scale to be divisible by 2^(v_2(m)+1).

Convexity justifies the boundary step even with T-junctions. A tile has a
positive-length contact with a supporting line only along one of its
whole sides. That side cannot extend outside the polygon's boundary
segment, since the entire tile is contained in the polygon. Thus each
exterior side is a concatenation of whole macrotriangle sides. Its odd
part contradicts the common extra power of2. Clearing rational scale
denominators is consequently valid.

## Real scales and rational orientations

Write ρ=exp(iπ/3). The reference side vectors belong to Q(ρ), and their
lengths are rational. Thus their normalized unit vectors also belong to
Q(ρ). The same is true for Q's boundary side directions. Multiplication
by a unit element of Q(ρ), and complex conjugation, have rational matrices
in the basis (1,ρ).

A boundary-adjacent tile therefore has a rational orientation matrix.
Across a positive-length side contact, the relative orientation is a
rotation or reflection taking one rational reference unit vector to
another, hence also has a rational matrix. The edge-contact adjacency
graph is connected: a polygonal path between generic tile-interior points
inside Q can avoid the finite set of tile vertices and cross edges
transversely. This remains true with T-junctions. Hence all orientation
matrices propagate rationally.

With those matrices fixed, the complete subdivided incidence structure
is described by rational affine equations: tile corners depend linearly
on translation and scale, and intermediate side points depend linearly
on a distance parameter along a fixed rational unit direction. Endpoint
conditions and strict ordering of all side parameters are also linear.
The positive-scale conditions are strict linear inequalities.

A rational affine system with a real solution has a rational parametrization
by Gaussian elimination. Its rational points are dense in its real affine
solution space, so the finite strict inequalities can be retained. The
rational solution may be chosen arbitrarily close to the original one.
If exact preservation of all nonincidences is desired, choose it sufficiently
close to preserve the positive distances between disjoint, nonincident
closed pieces; there are only finitely many such pairs.

## Geometric sufficiency of the incidence realization

The winding-number argument supplies the required global step. Give each
triangle its counterclockwise boundary orientation and subdivide each side
at every incidence vertex. Paired internal atomic edges are the same
straight segments with opposite orientations, so they cancel as chains.
The remaining chain is exactly the boundary of Q traversed once.

At any point outside all developed edges, each positively oriented
triangle contributes its indicator, zero or one. Their sum is the winding
number of Q's boundary, namely one in its interior and zero outside.
Positive-area overlaps and outside protrusions are therefore impossible.
Taking closures supplies the entire polygon, including its edges.

One minor interpretive detail: the corner triangle itself is a similarity
image of the original triangle, but intermediate T-junction parameters may
move along its sides. The continuous map of the *subdivided* face need not
be that single similarity. It can instead be made piecewise affine by
joining every ordered boundary subdivision point to an interior point,
such as the triangle centroid. All resulting face orientations stay
positive. The chain/winding proof does not depend on this choice, so this
detail does not create a gap in the argument.

The conclusion excludes at most four similar macrotriangles. It does not
exclude a dissection into five or more such pieces, a unit-tile dissection,
or a complete F3 tiling. In particular, 4830 remains unresolved.
