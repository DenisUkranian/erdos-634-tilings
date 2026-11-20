# Searching larger dissections for an intact unit copy

Each input is an exact triangulation represented by triangular or
parallelogram grid blocks in the basis $(1,\rho)$, with a common
coordinate denominator. The [grid checker](controls/verify_grids.py)
verifies triangular cell metrics, convex containment, pairwise
interior disjointness of the blocks and total area using exact arithmetic.
The search examines every isometric placement of the requested board
inside that one source, including translations, rotations and reflections.

The [scanner](scan_patches.py) combines collinear elementary edges into
maximal closed intervals, including edges extended across grid blocks.
For efficiency a block supplies entire rows in its two coordinate
directions and in its diagonal direction. On the 143 board and the
two scale-2 controls the maximal intervals are independently reproduced
by expanding each individual grid cell.

The $60^\circ$ corner of an extracted board must be a genuine mesh vertex:
two noncollinear supported segments cannot meet only in the interiors
of mesh edges. The same applies to its other corners, including at
T-junctions. In these certified grids every vertex has integral axial
coordinates after clearing the specified denominator. The scanner takes
each observed orientation of the short side, both turns by $60^\circ$
to the long side, and every intersection of sufficiently long runs
on those two axes. It requires the three exact segments to be contained
in the corresponding merged intervals. A supported closed triangle
inside the convex source bounds a union of whole tiles: no tile
interior can cross its boundary. No step assumes that an extracted
patch has the same orientation as its enclosing board.

## Result

For each of the seven listed unit boards, one explicit larger dissection
was checked at each of scales 3, 4, 5 and 6. The supplied scale-2
examples for 3431 and 5063 give two additional searches. Across these
**30 fixed source tilings**, there was no intact unit copy.
The larger-scale grids use the source package's constructions and
choices of load order; [sweep_dilations.py](sweep_dilations.py)
regenerates and verifies them. This test says nothing about layouts
outside the given sources.

The scanner recovers each of the two entire scale-2 source boards at
its own scale. It also finds all four known unit copies inside a
572-tile assembly made from four copies of the 143 dissection. A
reflected and translated version gives the corresponding four transformed
coordinates.

An unrestricted transfer run on each of the two leading boards was
also attempted with a 45-second time limit. The 3431 run reported cut
28 of 574 with 960 states. The 5063 run reported cut 16 of 467 with
220 states. Both processes exited with timeout code 124. These runs
supply no answer for either board.
