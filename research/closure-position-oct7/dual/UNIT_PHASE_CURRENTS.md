# Compressing positioned currents to unit segments

7 October 2026. This is an exact representation lemma. It is not a new
154 impossibility certificate and no three-band matrix has been solved.

For a finite complete dictionary of placements of an integer-sided tile
inside a convex target, a positioned-current matrix need not split every
edge at every intervening point of the full vertex lattice. Under the
project's integer-atom theorem, it suffices to split each individual tile
edge into consecutive length-one segments from its own endpoint. Equal
positioned segments are one row, with signs from their orientation. The
target boundary is treated in the same way from its vertices.

**Necessity.** On each maximal straight seam of an actual tiling, its two
banks are whole-edge partitions from common endpoints. Every vertex on
that seam is an integer distance from its initial endpoint. Thus overlapping
tile sides have the same phase modulo unit length along that line. Their
unit-segment subdivisions agree wherever they overlap. Internal rows cancel
and the surviving rows are exactly the subdivided target boundary.

**Integer sufficiency.** A nonnegative integer solution in these rows is
also a solution in ordinary geometric boundary currents: just forget the
unit-phase labels and sum the associated oriented segments. The existing
compact-support, degree-one current argument then gives coverage exactly
one and disjoint interiors. Hence the unit-phase formulation is equivalent
to existence of an actual tiling from the supplied dictionary. As usual,
a fractional feasible solution does not by itself give a tiling.

This unit-phase matrix may have a stronger fractional relaxation than the
matrix obtained by splitting all intersecting collinear segments into the
smallest geometric atoms. A genuine tiling passes the stronger condition
because its phases must agree on contacts. No guessed phase restriction is
being placed on individual placements: the dictionary remains complete.

For `(8,7,13)` this uses exactly 28 unit rows per tile column before any
additional extreme-edge compression. It avoids the factor 13 introduced
by subdividing some directions into length-1/13 atoms in a three-band
lattice.

For short heights `{-1,0,1}`, the exact vertex lattice is `(1/13)Z[rho]`.
A size-only enumeration gives 729,821 gamma anchors in the target and
17,013,246 contained placements in the 36 orientation variants. A full
unit-phase matrix would therefore have 476,370,888 signed entries.
These figures are stored in `threeband_size.json`. No such large matrix
was allocated or declared infeasible in this investigation.

The data size explains why simply expanding the supplied two-band matrix
is not an adequate all-height strategy. Endpoint-current compression or
implicit interval updates may reduce memory further, but those are separate
implementation choices requiring a complete correctness argument.
