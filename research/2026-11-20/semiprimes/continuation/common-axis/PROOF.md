# An interior tile must miss each proposed edge direction

On either of the two unit boards, let an interior tile mean a tile with no positive-length edge on the outside boundary. For every unoriented line direction there is an interior tile without any edge parallel to that direction. At least 31 tiles miss any fixed direction for the 3431 board, and at least 45 do so for 5063. Neither board is decided by this theorem.

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

## Two separated pairs of exceptional tiles

The two longer outside sides have just one compatible direction in common, namely \((1,1)\). For every other direction, one of the two sides consists entirely of exceptional tiles. The shorter of these longer sides has length \(c^2\), so it takes at least \(c\) tiles.

For the remaining direction \((1,1)\), all tiles on side 0 are exceptional. At *each* endpoint of side 0 an exceptional tile off side 0 must have a vertex at distance at most 50 from the endpoint. To prove this, run the same exact corner search, now choosing only ordinary convex pivots inside the closed radius-50 disk at the given endpoint. If there is no such pivot, return “possible.” For every anchored tile, a vertex is already in this disk, so failing the assertion requires it to have a side on the common axis or a full edge on side 0. These placements have short heights from −1 to 2. Tiles elsewhere may have arbitrary directions: all semigroup tests now allow all three lengths on every ray. Exhaustion takes 33 and 9 nodes at the two endpoints for 3431, and 11 and 8 nodes for 5063.

Every exceptional tile off side 0 has a positive-length contact with another exceptional tile off side 0. To see this, use the same \((j,h)\) coordinates as above. Let \(U\) be the axes compatible with \((1,1)\), and \(V\) the axes compatible with side 0's axis \((0,0)\). Their lists are
\[
U=\{(1,0),(2,0),(0,1),(1,1),(2,1),(0,2),(1,2)\},
\quad
V=\{(0,-1),(1,-1),(0,0),(1,0),(2,0),(0,1),(2,1)\}.
\]
No exceptional tile has all three axes in \(U\cup(V\setminus\{(0,0)\})\). Indeed, the possible tile triples are \((j,h),(j+s,h),(j,h+s)\) with \(s=\pm1\) and phase modulo three. Only \(-1\le h\le2\) could have all three axes in this displayed set, and listing the three phases and both signs verifies the claim. Take an edge on an axis outside this union. The two longer outside sides belong to \(U\), and the chosen tile has no edge on side 0, so the chosen edge has an interior contact. Its neighbor misses the common direction. If its axis is \((0,0)\), the supporting line is parallel to and different from side 0, so its neighbor cannot also have an edge on side 0. For any other axis outside the union, a tile on side 0 cannot have such an edge because the axis lies outside \(V\).

Both members of each resulting pair lie in the disk of radius \(50+2c\) at the corresponding endpoint. These two disks are disjoint since \(bq>2(50+2c)\) on both boards. This gives four exceptional tiles off side 0.

On 3431, side 0 needs at least 15 whole edges since \(511=11\cdot33+4\cdot37\) and 14 edges cannot achieve 511. On 5063 it needs at least 29, since \(1079=21\cdot35+8\cdot43\) and neither 26, 27 nor 28 edges can achieve 1079 (an even count has even length, and \(27\cdot43-1079=82\) is not of the form \(8x+30y\)). Adding the four exceptional tiles off side 0 proves the bounds of 19 and 33.

## Bounds using the orientation levels

For 5063, every direction other than \((1,1)\) already needs at least 45 exceptions. Indeed at least 43 tiles on a long outside side miss the given direction, and the interior-tile theorem supplies one more. For a non-outer direction the signed total of lengths of all tile edges on that direction is zero. Each tile has at most one such edge and all edge lengths are odd, so the number missing the direction is odd. This raises 44 to 45. For direction BC both other outside sides are incompatible and together already need over 45 exceptions. For direction OB, the tile on CO at its endpoint C has the axes of CO and the 2β bisector, respectively \((1,0),(1,1)\), so the third tile axis cannot be OB: the possible third axes are \((2,0),(0,1)\). For direction CO, the tile on OB at endpoint B has the axes \((0,0),(2,1)\) (the 2α bisector), with third axis \((2,0)\) or \((0,1)\); again CO is absent. In the last two cases this is an exterior exception distinct from the 43 on BC and from the required interior exception.

Now suppose the direction is \((1,1)\), and the total number of exceptions is less than 31 at 3431 or less than 45 at 5063. Every tile outside short heights 0, 1 and 2 is exceptional. The two tails of short heights \(h<0\) and \(h>2\) each have tile counts divisible by \(c\). At 3431 the exception budget is smaller than \(c\) itself. At 5063 there must be at least two exceptions on side 0 with edge length other than \(c\), since \(1079\bmod43=4\) differs from \(0,13,35\). Those tiles have short height zero, inside the central band. Thus even one nonempty tail would yield at least \(43+2=45\) exceptions at 5063. Both tails must be empty.

Here is the short tail-divisibility argument, following the earlier orientation-cut theorem of Denis Paliy. For the low or high tail, subtract from the counterclockwise boundary of each tile, weighted by its membership in the tail, its individual edges weighted by whether their heights are in the tail. When summed, the individual-edge terms cancel on interior contacts and no exterior term survives, because all exterior heights are 0 or 2. For each tile the difference is zero or a whole long side of length \(c\) with either sign. These selected long sides have heights \(k,k+1\), where \(k=-1\) or \(2\) at the respective cut. Their displacements belong to the rotated lattice
\[
z^k\bigl(c\mathbb Z[\rho]+(a+b\rho)\mathbb Z[\rho]\bigr).
\]
The axial generators before rotation are \((c,0),(0,c),(a,b),(-b,a+b)\). The gcd of their pairwise determinants is \(c\), so the fundamental area is \(c\sqrt3/2\). The selected signed edges form the boundary of the tail, and decompose into closed directed walks; hence the shoelace formula puts its area in \((c\sqrt3/4)\mathbb Z\). Each tile has area \(ab\sqrt3/4\) with \(\gcd(ab,c)=1\). This proves divisibility for both tails.

With heights restricted to 0, 1, 2, enumerate local completions at the endpoints of side 0 again. Count a defect if it is exceptional, off side 0 and has a vertex in the chosen disk (radii 75 and 85 at O and B on 3431, and 140 and 175 at O and B on 5063). This time allow a specified number of defects. The following upper limits all exhaust without a feasible local continuation.

| Board | Endpoint O | Nodes | Endpoint B | Nodes |
|---|---:|---:|---:|---:|
| 3431 | 3 | 17,842 | 10 | 35,755 |
| 5063 | 6 | 15,258 | 7 | 4,609 |

The verifier `verify_budgets.cpp` generates all 36 oriented placements up to translation, accounting for the choice of height, rotation and reflection. Its exact convex-corner recursion uses the same disjointness, semigroup and fan tests as above. It also checks the angular feasibility at a reflex vertex. For a complete straight segment with two convex endpoints it checks whether a sequence of tile sides can bridge the segment with feasible angle gaps at both ends and at the internal joins. It allows arbitrary overlaps of collinear edges along the two banks, enforcing integral distance only between vertices on a common maximal straight edge run: both banks start at the same endpoint and partition the run into whole tile sides of integer length. The solver can declare local continuation possible when no pivot remains in the disk; none of the enumerations above reaches that outcome.

The tiles counted at each endpoint lie within its chosen radius plus \(c\). The two inflated disks are disjoint on each board. At 3431 there are therefore at least \(15+4+11=30\) exceptional tiles. At 5063 there are at least \(29+7+8=44\), and the odd parity of the number of exceptions for the non-outer direction \((1,1)\) improves the two bounds to 31 and 45. This finishes both bounds.

## Replay

Run `python3 verify_geometry.py` and `python3 verify_slices.py`. Both use only the Python standard library. For the orientation-level bounds compile and run `c++ -std=c++20 -O2 verify_budgets.cpp -o verify_budgets && ./verify_budgets`. Full outputs accompany the sources.
