# An interior tile must miss each proposed edge direction

On either of the two unit boards, let an interior tile mean a tile with no positive-length edge on the outside boundary. For every unoriented line direction there is an interior tile without any edge parallel to that direction. At least 16 tiles miss any fixed direction for the 3431 board, and at least 30 do so for 5063. Neither board is decided by this theorem.

Use axial coordinates in the basis \(1,\rho=e^{i\pi/3}\). The outer vertices in counterclockwise order are \(O=0\), \(B=bq\), \(C=ap\rho\), where \(p=a+2b\), \(q=2a+b\), \(c^2=a^2+ab+b^2\), and \(N=pq\). The two parameter triples in \((a,b,c)\) order are \((33,7,37)\) and \((35,13,43)\). Number the sides \(OB,BC,CO\) by \(0,1,2\). Write \(z=(a+b\rho)/c=e^{i\beta}\), with \(\beta\) opposite the side of length \(b\). Directions are represented by \((j,h)\) for the axis \(\rho^j z^h\), where \(j\) is taken modulo three. Their labels are unique since \(2\cos\beta=q/c\) is rational but not integral. The outer side axes are \((0,0),(1,2),(1,0)\). The three axes of any tile belong to this direction group by propagation through positive-length contacts. Such contacts connect all tiles, by choosing a generic polygonal path between their interiors avoiding vertices.

## The geometry checks

Relative to one axis of a tile the other axes can differ by \(\pm\pi/3,\pm\beta,\pm(\pi/3-\beta)\). The three sets of possible directions compatible with the respective outside axes have empty intersection. Thus at least one entire outside side is covered by tiles missing the proposed direction. Its boundary tiles have distinct interiors. A tile cannot have a positive-length edge on two outside sides since that would fill an outside corner by one tile angle, whereas each corner requires two acute tile angles.

First suppose all exceptional tiles have an edge on one given side. The direction must be compatible with the two other outside sides. Intersecting the above seven-element sets gives one possible axis if side 0 is exempt, five if side 1 is exempt, and one if side 2 is exempt. Each such case uses short heights between one less than the least and one more than the greatest of the common and exempt heights. The search below excludes every case.

Next allow exceptional tiles with an edge on any outside side. Since the perimeter of the board is \(N\), each outside edge has length at least \(b>1\), and no tile uses two outside sides, fewer than \(N\) tiles have an outside edge. A positive-length contact therefore connects an interior tile and a tile with an outside edge. Their shared axis differs in height by at most one from each of the proposed common direction and that outside side. Thus only heights from \(-2\) to \(4\) and three unoriented phases at each height need checking. The search excludes all twenty directions other than \((1,1)\) on both boards. This leaves the bisector \(\ell=\rho z\) at the \(2\beta\) corner.

The two geometric enumerations are implemented independently of the slice computation in `verify_geometry.py`. For each height and phase the code forms both tile hands, retaining every template with an edge on the common axis or parallel to an eligible outside side. In the latter case the translation must put that edge on the outside line unless the tile already has a common-axis edge. All possible translations at the chosen corner of the remaining region follow by anchoring one of the three template vertices there. Coordinates are integers after multiplying by a power of \(c\).

The search maintains the oriented boundary of the region still to be tiled. At an ordinary convex corner, all incident tiles must have a vertex there. The search takes all successive angular sectors from one outgoing ray to the other, rejecting placements that overlap previous tile interiors or leave the board. A boundary portion between two ordinary convex endpoints must have length in the semigroup of available whole side lengths on its oriented ray. The same holds for the portion from a convex endpoint to a new tile vertex on its open side. For an exterior portion both ends are clamped, since a removed tile at an exterior endpoint prevents a remaining boundary side on the same bank from extending through that endpoint. These length tests do not require edge-to-edge contacts. Collinear boundary pieces are added and cancelled as oriented segments. A node without an available ordinary convex corner would raise an exception. No such node was reached. The first seven branches take respectively 36, 1, 3, 1, 1, 1, 4 nodes at 3431 and 16, 1, 3, 1, 1, 1, 4 nodes at 5063. Each of the other twenty directions takes five nodes when all outside sides are available.

## The remaining bisector

Use the linear coordinate \(t=(a+b)x+by\) perpendicular to \(\ell\). The values at the outer vertices are \(0,w bq,abp\), where \(w=a+b\). Let \(W(t)\) be the physical length of a section parallel to \(\ell\). Along a tile with an edge of length \(s\) on this axis the difference between its base and apex levels is \(abc/s\). On intervals between vertices use the ordinary derivative of the width and take its one-sided slope jumps. For an axis-based tile the jumps of \(abc\,W'\) are \(-s^2\) at the base and \(+s^2\) at the apex. Its section width can also jump at the base, which does not change this identity for the one-sided slopes. Thus every contribution from these tiles is integral at every level, for any translation.

For a tile whose vertex levels \(t_0,t_1,t_2\) are distinct, the jump of \(abc\,W'\) at \(t_i\) equals
\[
\frac{(abc)^2}{(t_j-t_i)(t_k-t_i)}.
\]
Indeed its triangular section-width profile has maximum \(abc/(\max t_i-\min t_i)\) by area. For the outer triangle multiply the same formula by \(N\). Section lengths add at every generic level, so the fractional parts of the jumps of the exceptional boundary tiles must sum, modulo one, to the board's fractional demand at each individual level.

The script `verify_slices.py` lists every boundary placement, using each integral arclength offset and all six assignments of an edge length \(L\) and an adjacent length \(S\) at its start, in the counterclockwise direction around the board. If \(T\) is the remaining length, the third vertex in the frame with its base from 0 to \(L\) has axial coordinates \(((L^2+S^2-T^2-ab)/(2L),ab/L)\). When two levels coincide, the axis-based calculation above gives zero residue at both levels.

The verifier propagates two necessary conditions. First, on each side a surviving placement must be part of a path of consecutive whole edge lengths spanning that side. Second, at each projected level, enumerate subsets of the contributing placements on each side with pairwise disjoint open edge intervals. Retain sets whose three sums give the required residue. Delete a placement that cannot occur in any such set, and eliminate any tile overlapping an edge forced in every set. The zero-residue tiles need not be enumerated in the local subset test. All arithmetic uses integers and exact rational numbers. Every elimination is a necessary condition. The fixed point leaves the following pairs of edge and adjacent lengths on both boards.

| Side | Surviving \((L,S)\) |
|---|---|
| 0 | \((a,c),(b,a),(c,a)\) |
| 1 | \((a,b),(b,c),(c,b)\) |
| 2 | \((a,c),(b,a),(c,a)\) |

On side 0 the slope jumps at the start and end of an \(a\)-edge are respectively \(ab^2/w,-ac^2/w\). For a \(b\)-edge they are \(-bc^2/w,a^2b/w\), and for a \(c\)-edge they are \(ab^2/w,a^2b/w\). Their apex jumps are respectively \(a^2,b^2,-ab\). Since \(a\equiv-b\pmod w\) and \(c^2\equiv b^2\pmod w\), each internal join contributes an integer. The board jumps at \(O,B,C\) are \(ac^2/w,pa^2/w,-aq\), so subtracting the first and last side-0 jumps leaves integers there as well. The board minus all the side-0 tiles consequently has integral slope jumps at every level.

On sides 1 and 2 the surviving \(a\)- and \(c\)-edge assignments have an edge along \(\ell\). The only remaining exceptions could have a \(b\)-edge. All their starting levels \(t_0\) are multiples of \(b\) because \(t\) decreases by \(b\) per unit of arclength on both sides. The side-1 \(b\)-tile's apex has level \(t_0-c^2\) and the side-2 \(b\)-tile's apex has level \(t_0+aw\). Each apex has the nonintegral jump \(ab^2/w\). Their other two vertices have levels divisible by \(b\). The two apex classes \(-a^2,+a^2\pmod b\) are distinct and nonzero. On one side a given apex level fixes the starting position uniquely. Hence such an apex jump has nothing with which to cancel. No exceptional \(b\)-tile can occur on either of these sides.

All exceptional tiles must therefore have a full edge on side 0. This is exactly the already excluded single-side geometric case with direction \((1,1)\). This proves the interior-tile assertion.

On 3431, the fewest whole edges on the shortest side is 15 since \(511=11\cdot33+4\cdot37\) and 14 edges cannot achieve 511. On 5063 the fewest is 29, since \(1079=21\cdot35+8\cdot43\) and neither 26, 27 nor 28 edges can achieve 1079 (an even count has even length, and \(27\cdot43-1079=82\) is not of the form \(8x+30y\)). Both other sides on each board require more edges by length. Adding the interior tile proves the bounds of 16 and 30.

## Replay

Run `python3 verify_geometry.py` and `python3 verify_slices.py`. Both use only the Python standard library. Full outputs accompany the scripts.
