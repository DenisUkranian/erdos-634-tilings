# Independent review of the one-level remainder obstruction

8 October 2026. Reviewed `../4830/ONE_LEVEL_OBSTRUCTION.md` directly.
The proposition is valid as a restricted obstruction. It does not
exclude arbitrary 4830-tile F3 tilings.

## Direction and uniqueness check

Put \(\rho=e^{i\pi/3}\) and \(Z=a+b\rho\), with \(a>b>0\). Then
\(0<\arg Z<\pi/6\). Thus no possible c-edge in the stated orientation
class is parallel to a short axis. The long directions are the two
distinct classes \(\pm\arg Z\pmod{\pi/3}\); these classes could coincide
only at the excluded endpoints 0 or pi/6. Consequently a directed long
edge, its bank, and the prescribed short-axis class determine its tile
uniquely. On the opposite bank the unique tile is its half-turn partner,
so the two triangles form a parallelogram.

This uniqueness needs the hypothesis a>b (a!=b would also suffice with
an appropriate relabeling). It is not a statement about unrestricted
tile orientations.

## Whole c-seams and T-junctions

The quadrilateral Q in the proposition is convex for a>b. Its two
non-axis boundary sides are therefore genuine supporting-line segments.
An internal c-seam cannot continue into an exterior boundary c-segment:
their common supporting line would be a supporting line of Q and would
contain no internal segment.

Take a maximal connected collinear union of internal long tile edges.
On either bank, every positive-length contact is a whole c-edge: no
short edge has this direction. A bank cannot stop while the opposite
bank continues, because that would put a tile interior across an actual
edge. At a maximal endpoint no constituent edge can overrun. Thus the
two banks are partitions of the same segment into equal lengths c,
beginning at the same endpoint. Their endpoints coincide one by one.

Every internal c-edge therefore has exactly one full c-edge partner.
Short-edge T-junctions elsewhere on a paired parallelogram do not change
its signed directional current; one may split all such edges into
atomic intervals before cancelling.

## Removing the forced boundary tiles

Each long boundary side has length bc and consists of b whole c-edges.
The two lists of forced tiles cannot identify the same tile, since a
triangle has only one c-edge and the two boundary directions differ.
If any of these forced placements overlap or exit Q, nonexistence is
already established.

Otherwise remove the 2b forced tiles. Every tile that remains had an
internal c-edge in the original tiling. Its partner also remains:
a removed tile's sole c-edge was exterior. Hence **all** remaining tiles
partition into the parallelogram pairs proved above. No convexity of
the resulting remainder is assumed.

## Current calculation

In the ordered signed axes \((1,\rho,\rho^2)\), Q contributes

\[
(b(2a+b),-b(a-b),0).
\]

The short edges of the boundary tiles on \(-bZ\) contribute
\((ab,b^2,0)\). Those on \(b\rho^2 Z\) contribute
\((b^2,0,-ab)\). Subtraction leaves exactly

\[
\boxed{(ab,-ab,ab)\ne(0,0,0).}
\]

A parallelogram has zero current in each signed axis separately. The
remaining tiles cannot therefore be the required pairs. This proves
the proposition with arbitrary T-junctions.

The vector sum of this current happens to be zero, because
\(1-\rho+\rho^2=0\). That does not invalidate the argument: the invariant
records the three directional currents separately, not merely their
ordinary vector sum.

## Numerical certificate check

The stored 22 forced triangles for (a,b,c)=(24,11,31) were independently
read without importing the constructor. Integer calculations checked
all squared side lengths \(121,576,961\), positive doubled coordinate
area 264, containment in Q, and all 231 pairs by separating-axis tests.
All checks passed. The doubled coordinate area of Q is 209088, giving
792 tiles. This corroborates the concrete example; the general proof
above does not depend on this finite check.

The underlying pairing and directional-current principles are already
used elsewhere in the project. This review makes no originality claim
for those principles. Its conclusion concerns the stated fixed-axis
remainder only; it neither forces that remainder in every F3 tiling
nor excludes fillings with additional direction classes.
