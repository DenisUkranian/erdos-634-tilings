# Endpoint cancellations and triangular subregions

For each of the two unit tiles, two nested tiled triangles cannot differ by one or two unit tiles in a dissection in which the smaller triangle is a union of whole tiles. This statement holds in the whole plane. It entails a restriction on searching the original boards by successive endpoint cancellations, without any restriction on translations, reflections, orientations or T-junctions.

## An intrinsic graph

Orient every tile counterclockwise. An oriented side from P to Q supplies two signed entries, +1 at P and −1 at Q. Its key is the point and the unoriented direction of its line. Supply the negative of the exterior polygon's entries. At each key pair positive entries with negative entries in any bijection. The entries balance because the two banks of an internal segment have opposite oriented currents, even when one edge spans several on the other bank. The derivative of the signed interval indicator on the supporting line gives the stated endpoint entries.

Let the graph vertices be tiles and one exterior vertex, and draw one abstract edge between the owners of each paired pair of entries. Multiple edges are allowed. Each tile has degree six. No intersection or unit-offset convention is required to define this graph. For every nonempty set of tiles S, its edge cut in this graph has at least six edges. Every cut of exactly six bounds a tiled triangle made of precisely the tiles of S.

To prove this, orient a coordinate on each supporting line. The endpoint jumps determine the oriented, compactly supported interval current on that line uniquely by integration. Only entries paired across the cut can contribute to the jump at any point of the tile union. Each nonzero supporting line requires at least two opposite jumps, counted with multiplicity. At least three distinct supporting lines occur. A finite nonzero polygonal 1-cycle cannot be supported on at most two lines, since splitting at all intersections gives a finite forest. The union has positive area, so its boundary current is nonzero. At cut size six there are exactly three lines, with just two unit jumps on each. Thus the support on each line is one directed segment of multiplicity one. These three segments form a nondegenerate triangle by closure. Winding number counts tile interiors off the finite set of edges, and equality extends by closure, proving the assertion. The same cut bound proves that the graph is connected.

Conversely, for any specified tiled triangular subregion one can choose a pairing that realizes it as a six-edge cut. At every key first match internally on each bank of the partition into the subregion and its complement, then match the residual entries. Only the six signed entries of its three exterior sides remain unmatched across the partition. This converse concerns the specified subregion and matching.

## Excluding very thin nested pairs

Let A be a proper triangle inside a tiled triangle B and a union of tiles of that tiling. At least one full side of A lies, apart from its endpoints, in the interior of B. Otherwise all three supporting lines of A would be the three boundary lines of B and the triangles would be identical. If B minus A consists of k tiles of diameter c, that side of A has length at most kc by coverage from the other bank.

Every angle of A is at least the smallest tile angle β. A side of length d opposite an angle at least β gives area at most d²/(4 tan(β/2)). This follows by writing the two base angles as u,v and the area as d² sin(u) sin(v)/(2 sin(u+v)), maximized for their fixed sum when u=v. The unit area is ab√3/4 and tan(β/2)=√3 b/(2c+2a+b). Consequently, if k≤2, the area of A in tile units is at most
$$
  \frac{4c^2(2c+2a+b)}{3ab^2}.
$$
The bounds are 5476/33 at 3431 and 7396/105 at 5063.

For completeness one can enumerate all candidate tiled triangles through two tile areas above these thresholds. Every corner angle has the form iα+jβ, absorbing each 120-degree tile angle as 2α+2β. Since α+β=π/3 and β/π is irrational, the three i coefficients sum to three, and so do the j coefficients. Irrationality follows because 2 cos β=(2a+b)/c is a nonintegral rational number, whereas a root of unity plus its inverse is an algebraic integer. Enumerating the two triples gives eleven distinct metric shapes. The sine rule gives a primitive integer side triple for each. Each side of a tiled triangle is an integer sum of a,b,c, so the common multiple of the primitive triple must be a positive integer. Both the side test and the sine area are computed exactly by [short_tails.py](short_tails.py).

| Tile | Maximum tested area | All surviving tile counts |
|---|---:|---|
| (7,33,37) | 167 | Squares from 1² to 12² |
| (13,35,43) | 72 | Squares from 1² to 8² |

These squares are attained by standard grids. Two distinct positive squares differ by at least three. This excludes the asserted nested pairs.

## Consequence for exhaustive coordinate search

Take graph-distance layers from the exterior. Every intermediate nonempty layer has at least three tiles. Indeed the two cuts directly before and after such a layer each have size at least six. Since each layer tile has degree six, a singleton is impossible. A two-tile layer would force both cuts to have size six. The two nonempty tails are then nested tiled triangles differing by just these two tiles, already excluded.

If there are n tiles and the last layer has index D, then n≥3(D−1)+1. Every tile in a hypothetical original tiling is reached within **1144** steps for 3431 or **1688** for 5063, regardless of which endpoint pairing is used. Each step takes one of the six signed side endpoints to a congruent tile with that same point and axis. There are at most 24 such placements before geometry and the required sign filter. Thus these radii also apply to a constructive breadth-first superset seeded at the exterior entries. They bound a complete finite coordinate search. Its full enumeration has not been executed.

## Large tiled triangles contained in the original boards

[contained.py](contained.py) gives an independent size screen. It tries every metric shape and integer dilation up to board area. Continuous rigid placement inside the board is tested exactly. For a fixed rotation of a trial triangle, with vertices v and a counterclockwise board with directed sides d, the least required dilation of the board, allowing translation, is
$$
  -\frac{\sum_d\min_v \det(d,v)}{\det(d_0,d_1)}.
$$
Indeed the containment inequalities for a translate give three lower bounds for the determinants of its translation against the three sides. Those three determinants range over the full plane of triples of sum zero. On any angular interval with fixed active vertices the displayed positive function has second derivative equal to its negative. Its minimum occurs at an endpoint, where a trial side is parallel to a board side. The checker therefore uses only finitely many rational rotations and their reflections.

The screen leaves 50 possible triangular subregion counts including the full board at 3431, and 57 at 5063. The largest possible proper counts are bounded above by 2920 and 3984. Between 1681 and 3431 the only possible proper count at 3431 is 2920, with unordered sides 511, 1221, 1480. Between 2496 and 5063 the only possible proper count at 5063 is 3984, with sides 1079, 1505, 2064. All intervals here are open. The two upper candidates fit geometrically. Whether they can occur as tile unions in a whole-board tiling is open. This result also restricts every six-edge cut in the graph.

[independent.py](independent.py) verifies the two small spectra by enumerating pairs of integer side lengths and a possible included cosine. Its maximum side follows from the two base angles being at least β, which bounds the altitude below by half the base times tan β.

Run `python3 short_tails.py`, `python3 independent.py` and `python3 contained.py`. All three use the Python standard library. These restrictions on arbitrary full tilings leave the existence question open for both counts.
