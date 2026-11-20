# Exact unrestricted pentagon sweep

The control boards are the convex pentagons in [the construction](../PENTAGONS.md).
In the physical Eisenstein basis, let
X=(0,sc), Y=X+(0,tb), W=Y+(ta-kc,0),
D=X+(ta,tb)-k(a²,ab)/c, and V=(ab,b²)/c-(0,c).
The polygon runs from (0,(s−1)c) through Y,W,D,D+V.
The doubled coordinate area relative to one tile is
t²−k²+2a−2s+1 for the supplied parameters.

## Reproduction

    g++ -std=c++20 -O3 pentsearch.cpp -lgmpxx -lgmp -o sweep
    ./sweep 33 7 37 tri 10000
    ./sweep 33 7 37 pent 500000 2 13 8

The triangle control has a 4-tile tiling. The second command returns
`NO 3246`. This excludes the *given pentagon* on 168 tiles of sides
(33,7,37). The rest of the 3431-tile board could still be tiled using
different internal cuts. Reflection, off-lattice positions and T vertices
are all allowed in the search.

## Why a negative is an exhaustive certificate

Coordinates and lengths use GMP rationals; oriented cross products are
exact. A new triangle is positioned at a convex vertex of the residual
polygonal region which has precisely two incident boundary rays and no
through-segment. Such a vertex cannot have a tile edge running through
its tip. On each incident ray one tile must start there with a complete
edge along that ray. For either selected ray, all six assignments of the
three side lengths are generated on the interior side. Their third
vertices lie in the Eisenstein rational field; for adjacent side lengths
r,s and opposite side length v, the coordinates of the third vertex in
the oriented unit frame are ((r²+s²−v²−ab)/(2r),ab/r).
The algorithm can choose the ray having fewest possibilities, since in a
tiling every ray must have one. It recurses one tile at a time.

The separation test for two convex triangles uses each oriented edge
of either as candidate separating axis. All vertices of the new triangle
must lie geometrically inside or on the fixed convex board. Boundary
updates cancel exactly the collinear overlapping portions of opposite
directed segments and merge consecutive segments. They retain both
endpoints when a boundary line changes direction. A zero residue angle
and every possible nonnegative sum of the tile's angles up to 180° are
allowed: the 120° angle is 2α+2β, so enumerating nonnegative sums of α
and β less than or equal to 180° suffices. Both angles lie strictly
between 0° and 60°, giving a finite enumeration by exact cross-products.

Two extra pruning rules use collinear whole edges. First, along a
connected maximal interior segment of tile edges, both banks partition
the segment into complete tile edges. Indeed a bank ending earlier in
the interior of the other bank would have the remaining segment covered
by tiles on only one side. Any point strictly inside that remaining
interval other than the finitely many tile vertices would then have to
intersect the interior of an edge on the missing side. Thus the two
banks start at the same endpoint, and every vertex offset on the segment
is an integer. If a vertex of one tile lies in the relative interior of
another tile's edge, the offset from that edge's endpoint is integral.
The same holds on the outside boundary by its single whole-edge bank.

Second, along an exposed residual segment starting at an ordinary
strictly convex tip the future tiling cannot overhang that tip. If one
of its vertices touches the open segment, it is an edge endpoint on the
free side: a through-edge there would leave no angle for another
tile. Its distance from the tip must therefore be a nonnegative
integer combination of a,b,c. With two such ends the segment's entire
length must likewise be representable. The same statements hold along
an original polygon side, starting at either original endpoint.
All lengths ever tested against the coin table are bounded by the board
diameter; the limit 8(c²+ab) exceeds the diameter of all the control
boards reproduced in this file.

The code stops with INCONCLUSIVE if any visited nonempty residual has
no admissible convex tip. It signals a separate budget exit on exhausting
the requested node count. Neither event is counted as a negative.
There is no angle height palette or mesh assumed by this implementation.

## Independent fixed-palette enumeration

For a second enumeration, [the height budgets](SMALL_HEIGHT_BUDGETS.md)
proves that the union of the palettes [-1,1] and [0,2] covers every
possible tiling of either small pentagon. The finite engine indexes
the twelve translated/rotated/reflected oriented tile shapes for each
height, with all three possible anchor vertices. It works on the exact
integer-coordinate grid with denominator c raised to the largest
absolute height (at least one). This denominator is sufficient because
each new tile grows from an actual existing exposed corner, with all
its relative vertex displacements in the indicated group. No
coordinate assumption about a preexisting global tiling is needed.
Instead of one edge candidate it recursively enumerates all complete
tile fans in the selected convex wedge. Scalar height-count residues
and an integer coin table for each directed bank give extra necessary
tests. Occupied large-angle fans in a trial are bounded to lie inside
the remaining board; partial failure, singularity and budget limits
cannot be returned as NO. Exact integer products use 128-bit storage
for cross-products and norms; for the displayed control scales, all
coordinate products in 64-bit intermediate steps remain in range.

    g++ -std=c++20 -O3 pentfinite.cpp -o pentfinite
    ./pentfinite 33 7 37 4 0 -1 1 500000 2 0
    ./pentfinite 33 7 37 13 8 -1 1 500000 2
    ./pentfinite 33 7 37 13 8 0 2 500000 2
    ./pentfinite 35 13 43 11 2 -1 1 500000 4
    ./pentfinite 35 13 43 11 2 0 2 500000 4

The positive control returns a 16-tile tiling. The four complete
negative fixed-palette counts, in command order, are 3281, 3378, 19305,
17680 nodes. Therefore the 168 and 180 pentagons in these two
sufficient reductions are both untileable. Their original unit F2
triangles remain undecided by this exclusion.

## The maximal symmetric extension for 3431

For step data s=2,t=13,k=8 absorb both available rows, so j=2.
The vertices are (0,(s−j)c),Y,W,D,D+jV and the area in tiles
is t²−k²+2j(a−s)+j²=233. The same two-bank cut gives n0≡21
and n1≡27 modulo 37: compare the records t² on short height 0
and −k²+2j(a−s)+j² on short height 1. There are at most 185
units to use outside, and each extra height costs at least 74;
at most two such heights occur. The 2c² bound precludes gaps
toward either tail. The ranges [-2,1], [-1,2] and [0,3] therefore
cover all possibilities. In this order the following three exact
exhaustions return NO with 40421, 45274 and 42690 nodes:

    ./pentfinite 33 7 37 13 8 -2 1 1500000 2 2
    ./pentfinite 33 7 37 13 8 -1 2 1500000 2 2
    ./pentfinite 33 7 37 13 8 0 3 1500000 2 2

This excludes every positive integer row extension of this fixed symmetric
3431 notch: the only positive choices are one or two rows. In particular,
even the maximal row extension, which permits a pure-a representation
on the long side, does not suffice. Other macrodissections are still
available, including an asymmetric 233-tile pentagon of different shape.

## The asymmetric maximal extension with the same area

For the different 3431 template s=j=1, t=23, k=19, n0≡11 and
n1≡0 modulo 37. Moreover n1>0: the actual outer side from D
to D+V has height 1 and length a=33<c. If all edges on that side
were long their lengths would sum to a multiple of c. It follows that
n1≥37, leaving at most 185 outside and giving the same three-palette
coverage. The replay commands are those immediately above with
parameters 33 7 37 23 19 and terminal arguments 1 1. Their respective
negative counts are 54397, 69938, and 59154. More generally the same
argument proves n1>0 whenever 0<j<c, since the side length is ja
and gcd(a,c)=1. The exterior side of length ta−kc similarly forces
n0>0 whenever c does not divide t.

## The single 206-tile pentagon for 3431

With s=4,t=26,k=23,j=1, the residue pair is 10,11 modulo 37.
The minimum off-pair cost of 74 again allows at most two external
heights (206−10−11=185). Consecutivity gives the same three ranges.
The replay commands replace 33 7 37 13 8 by 33 7 37 26 23 and use
terminal arguments 4 1. The complete negative counts are 92005,
58633, and 57626, respectively. Thus the particular single-hole
206-tile shortcut fails for arbitrary tilings of its prescribed hole.

### Additional optional pruning

With REFLEX_FILTER enabled, the finite solver considers all oriented
rays of the supplied palette. For each ray it sweeps once around the
circle and marks every direction reachable by a sequence of actual
tile angles or a straight through-edge. Every isolated residual corner,
including a reflex corner, must have its sector in this set. A corner
with another residual edge passing through its vertex is skipped.
SPAN_FILTER also checks both ends of each exposed segment clamped by
ordinary convex corners. Its opposite bank is a word of whole tile
sides of the segment's total length. At a join, the preceding tile's
backward apex ray and the next tile's forward apex ray must enclose a
nonnegative realizable angle; an overlap fails. At each true endpoint
the gap up to the actual incident boundary ray must be realizable
as well. Dynamic programming enumerates these words. These optional
flags change node counts. The numerical counts above use neither.

When SIGN_FILTER is enabled, the solver reads each directed outer side
in its exact height h and rotation exponent e and forms the external
weight E_h by adding (−1)^e times its length. With d=a−b and G_h the
signed tile population, the short edges contribute d G_h, while the long
edges each have weight ±c. If U_h and L_h sum the signs of height-h tiles
whose long edge is respectively one height higher or lower, the exact
chain identity is E_h = d G_h − c(U_{h−1}+L_{h+1}). Its ordinary and
alternating sums determine the total and alternating sums of G_h.
The optional filter enumerates integer budgets satisfying these relations,
the parity and magnitude bounds from the ordinary area budgets, and
checks that unplaced tiles could still complete the partial signed counts.

## A full hexagon exclusion with a 60-degree corner

For the 3431 tile (33,7,37) and the asymmetric single-hole scheme
s=j=l=1,t=23,k=19, take P=(0,0), T=(a²b,ab²)/c and
U=(b(a+b),−ab)/c. In the shifted coordinates used above the
hexagon is P,Y,W,D+lU,T+lU,P+(lc,0). The area is 248 tiles.
The new l(2b−l+2s) tiles in the formal dissection are all at short
height 1, so n0≡11, n1≡15 and the rest vanish modulo 37.
The board has only exterior heights 0 and 1. Since 248−11−15=6c,
at most three outside heights occur, and gap exclusion (248<2c²)
places all of them in [-3,4]. In particular this new tip geometry
fails even with arbitrary orientations and T-junctions in the hole.

    g++ -std=c++20 -O3 -DREFLEX_FILTER -DSPAN_FILTER -DSIGN_FILTER pentfinite.cpp -o hexsweep
    ./hexsweep 33 7 37 23 19 -3 4 25000000 1 1 1

The full superpalette returns NO in 241575 nodes. The catalog of signed
counts is computed from the actual oriented exterior edges.

The optional LOCATED_SPANS test also requires every tile proposed in a
boundary word to lie in the actual board and clear all previously placed
tiles. BANK_PROBES may choose a single tile incident to a specified
noninteger offset (an integer plus 1/2) in a segment with two convex
ends. Every tiling then has exactly one free-side edge covering that
offset. Its start lies an integral distance from the initial endpoint.
The solver generates all such candidates whose prefix and suffix pass
the angular word test. This provides a second complete branching rule.
LOOP_FILTER can reject any closed walk of current boundary edges whose
coordinate area is not an integer multiple of tile area: the winding
number of the walk is constant on every prospective tile interior.

## The 250-tile pentagon for 5063

Here s=8,t=22,k=17,j=1 and the tile is (35,13,43). The exact
signed-population and boundary argument for this board gives the
[complete middle palette](../../notches/NOTCH_ENUMERATION.md) [-1,2]. For a first negative computation use
the [forced 120-degree corner at Y](P250_APEX.md). Its two other vertices are
Y+(0,−35), Y+(13,0); no D- or D'-corner placement is prescribed.

    python3 replay_p250.py --shards 12 --jobs 12 --seed-y

The twelve recorded NO verdicts in pentagon_250_seed_y.log total
1,188,501 visited nodes (common shallow nodes are counted by each
worker). When more than one admissible fan or bank tile is available,
the consecutive children have fixed indices. At the first eight
branching decisions compute the unsigned 32-bit recurrence
Hnew = 16777619 Hold + (child index starting at one), starting from
zero. The branch belongs to shard H modulo the shard count. A branch
ending before its eighth decision is examined by every worker. Thus
the shards cover all branches. A positive or an inconclusive exit
cannot be converted by the driver into a negative.

As an independent unrestricted rational check of the 180-tile ordinary
pentagon, with no finite palette theorem or orientation-count lemma:

    ./sweep 35 13 43 pent 500000 4 11 2

This returns NO in exactly 19999 nodes.

**Unseeded certificate.** The completed independent calculation starts
with the five bare outer sides. It prescribes no corner tile or internal
cut. From each ordinary ray/fan choice, all possible tile placements
are considered as above; signed population counts come directly from
the bare exterior. For the sharp middle palette, see the signed
three-wall count in the project's NOTCH_ENUMERATION.md, section
“A side-count bound removes the remote heights on the 250 pentagon”.
A cover of the 16 primary search partitions consists of 31 recorded
terminal partitions with a total of 5,331,660 node visits; this includes
shared search prefixes. Some primary partitions are split further at
branching depths 14 and 20. The same unsigned hash is carried forward.
The complete prefix-tree cover and every node count are independently
checked by the replay driver:

    python3 replay_p250.py --ledger pentagon_250_unseeded.json --jobs 16

The result is NO for this specified 250-tile pentagon with reflected
tiles, arbitrary real placements, and non-edge-to-edge contacts.
