# Independent audit of the eleven-patch seed construction

8 October 2026. Internal mathematical and exact-coordinate review, not
external peer review or proof-assistant verification.

Reviewed file: `../seed-generalization/macro_seed.py`.

## Mathematical argument

For each patch the program specifies a translation o and basis vectors
u,v with squared physical lengths 9 and 25 and squared difference 49.
The vectors have common coordinate denominator 7, so the integer norm
checks are 441,1225,2401. The unit triangles `(o,o+u,o+v)` and their
translates and half-turns therefore have exactly the required side
lengths `(3,5,7)`.

Every macrovertex has integer coordinates in this basis; the divisibility
checks use its nonzero determinant exactly. Every macroedge lies on one
of the grid lines i=integer, j=integer, or i+j=integer. These are precisely
the edges of the triangular subdivision of the u,v parallelogram lattice.
Consequently no grid triangle is cut through its interior by a macroedge.
Selecting exactly those elementary triangles whose centroids have
nonzero winding number selects the macroregion. A centroid cannot lie
on any of these grid lines: its local coordinates have residues 1/3 or
2/3, and their sum has residue 2/3 or 1/3. Thus there is no boundary
ambiguity in that test.

The code checks that the eleven listed polygons are simple, oriented
counterclockwise, and contained in the convex trapezoid. It independently
checks that each patch's selected triangle boundaries sum to its own
boundary, and that the eleven macro boundaries sum to the target's
boundary, after splitting at incident vertices. The atom check does not
need extra intersection vertices: splitting collinear overlaps at all
endpoints suffices for equality of oriented line measures. Non-collinear
crossings are isolated points and cannot create or cancel a nonzero
segment measure.

Every small triangle is oriented counterclockwise before its current
is added. Hence the signed coverage difference between the triangles
and target has zero distributional boundary and compact support; it is
zero outside the arrangement and thus zero in every two-dimensional
arrangement cell. The coverage multiplicity is exactly one inside the
target. This proves absence of positive-area overlaps and gaps. Closedness
of the finite union supplies all boundary points. No prior nonoverlap
assumption or numerical tolerance is used in this implication.

## Exact reconstruction comparison

I ran the macro constructor separately, loaded its output and the
previous frozen 180-tile certificate, and compared normalized sets of
unordered coordinate triples. Both use denominator 7. Each set contains
180 distinct triangles, and the sets are exactly equal: no old triangle
is missing and no new triangle is added.

Thus the compact construction reconstructs the previously independently
checked geometric seed, rather than merely giving the same area or
orientation inventory. Its discovery history still includes the solver;
its reproduction and mathematical verification no longer require that
solver or the old unit-coordinate file.

## Verification-program requirement

The initially reviewed implementation used Python assertions for its
critical checks. I requested either explicit checks or rejection of
optimized Python execution before its report is treated as a verifier.
The constructor now rejects `python -O` and `python -OO`; the rejection
was separately replayed. The updated constructor and both certificate
hashes are recorded in `macro_seed_audit.json`. The ordinary exact run
and written geometric argument were unaffected.

## Propagation audit

The independent [propagation proof](TRAPEZOID_PROPAGATION.md) gives two
fully positive operations: append a tiled short-grid parallelogram and
stack trapezoids along a full horizontal side. It yields the domains
`x>=29,n>=2` and, using the later independently checked 240-tile
equilateral seed, `x in <3,5>,n>=4` for T(x,15n). Both operations explicitly
fill their added regions; neither relies on subtracting a tiled region
from a different tiling.
