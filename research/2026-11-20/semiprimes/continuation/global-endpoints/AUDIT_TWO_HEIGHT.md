# Independent audit of the full two-height catalogue

20 November 2026. Audited files: `two_height/make.py`, `check.cpp`,
`corner_fans.hpp`, `control143.py`, and `check_native.cpp` in the current
workspace. This is a code and mathematical-scope audit, not a report of a
completed exclusion computation.

## Scope of the full catalogue

Write R=Z[rho], rho=exp(i*pi/3), z=(a+b*rho)/c. The outer triangle has
vertices 0, H=b(2a+b), and V*rho with V=a(a+2b). In this frame its side
heights are 0, 0, and 2. Height means the exponent of z modulo powers of
rho. The two short edges of a tile have a common height h, and its long
edge has height h-1 or h+1.

In fact **every tiling using at most two short heights must use exactly
the heights 0 and 1** in this frame. The two exterior sides at height zero
have lengths ap and bq, neither divisible by c: the sides are pairwise
coprime, 3 does not divide c, and p²=4c²-3a² and q²=4c²-3b². If short
height zero were absent, those sides would consist entirely of c-edges,
contradicting their lengths. Hence short height zero occurs.

Every exterior side has at least one long c-edge. Otherwise each of its
r short boundary edges places an obtuse 120-degree corner at one of only
r-1 internal joins; no two such corners fit at one join, and all three
outer corners are below 120 degrees. On the exterior side of height two,
a long edge requires short height one or three. A two-height support of
{0,3} is impossible because the positive-length contact graph is connected,
and adjacent tiles have short-height difference at most two. Thus {0,1}
is the only possible two-height support.

## All real translations are represented

The generator uses eta=(7,-4), (7,-1), and (3,-2) respectively for the
3431, 5063, and 143 cases. Each has Eisenstein norm c, and both eta and
eta*z have integral Eisenstein coordinates. Therefore multiplying every
point by eta makes every available short edge at height zero or one
integral. A long edge is the difference of the two short side vectors,
so it is integral too.

The graph joining tiles that share an actual corner is connected even
with T-junctions. Indeed every maximal connected collinear component of
tile sides has full-side partitions on both banks and common endpoints;
consecutive tiles on a bank share a corner and the two banks meet at the
first endpoint. This puts every positive-length contacting pair in the
same corner-connected component. Positive-length contacts connect the
whole finite tiling. Starting from the exterior corner 0 now proves that
all transformed tile vertices lie in R. This includes arbitrary real
translations before the transformation; no original integral-anchor
assumption is needed.

For each height the generator takes six rotations and both hands, anchors
at the obtuse corner, and orders the other vertices counterclockwise.
These are the full 24 congruent templates. Containment of all three
vertices is equivalent to containment of a triangular tile in this convex
outer triangle. Consequently `check.cpp` begins with an exhaustive
placement catalogue for every tiling with at most two short heights.

## Safety of the deletions

The angular filter is a relaxation of the necessary vertex condition.
At an interior tile vertex, the other tiles either partition a full turn,
or partition a half-turn while another tile passes through that point
along a side. Its directed reachability tests admit both possibilities.
At a boundary point the available sector is exactly the polygon sector.
Every triangle that occurs in an actual tiling therefore belongs to an
accepted fan. Repetition or incompatible choices in a relaxed fan can
only retain extra placements; they cannot remove a real tiling placement.

The line filter considers each primitive lattice line intersecting the
convex board. An actual maximal connected straight side component has
two full-edge partitions with the same starting and ending point. Its
bank paths are among the forward interval paths enumerated by the code.
The forward/reverse reachability calculation retains every edge belonging
to such a pair of paths. Exterior sides enter as a virtual edge with
reversed bank sign. Candidate incompatibilities and cached candidates
that have just been removed elsewhere can only make this relaxation
weaker. A reported missing exterior bank or outer corner is therefore a
sound exclusion for the catalogue.

The two filters do not constitute an exact-cover solver. A nonempty fixed
point is correctly printed as OPEN; it must not be called a tiling.

## Integer and bit-width audit for the supplied instances

| N | Bounding box | Integer anchor slots | Distinct oriented rays | Fan maximum index |
|---:|---:|---:|---:|---:|
| 143 | 118 by 134 | 15,812 | 24 | 60 |
| 3431 | 6,205 by 6,698 | 41,561,090 | 24 | 60 |
| 5063 | 7,554 by 13,890 | 104,925,060 | 24 | 60 |

All 24 placement bits fit in uint32_t. Ray jumps fit in the 32-entry
array. Antipodal rays differ by 12 positions, and the 64-bit reachability
arrays and shifts stay within the index bound 60. Bounding-box indices,
template offsets, and translated coordinates fit in signed 32-bit
integers on these generated inputs. The cross product casts before
multiplication and is safe in int64_t. These checks are instance-specific;
the program is not claimed safe for arbitrary unvalidated input sizes.

The control generator expands the known 143 construction to exact
individual coordinates and matches all 143 to these templates. Their
preservation is a useful positive control, in addition to the direct
reasoning above. It is not by itself a proof that arbitrary deletions are
sound.

## Native-phase variant

With `NATIVE_PHASES` enabled, `check_native.cpp` deliberately removes
anchors outside one specified linear residue class for each height.
This is a proper additional restriction. A NO from that run rules out
only tilings that simultaneously obey those chosen phase classes. It
does not rule out all two-height tilings, nor all full-board tilings.
The unfiltered `check.cpp` has no such phase restriction.

## Conditional consequences of a full-catalogue exclusion

If the unrestricted two-height catalogue returns NO, then every full
tiling of that board must use at least three distinct short heights.
Moreover, at least 2c tiles would have short height outside {0,1}, namely
at least 74 for 3431 or 86 for 5063. The latter follows from the existing
whole-board level theorem: every occupied nonexceptional height contains
at least 2c tiles, and the exceptional height in this frame is zero.

Neither conclusion follows from a native-phase-only NO. Even a genuine
full-catalogue NO does not exclude tilings with three or more heights,
so it cannot by itself settle either original semiprime.
