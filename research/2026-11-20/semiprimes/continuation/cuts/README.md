# Straight cuts in the 3431 and 5063 triangles

Consider the two scale-one F2 boards in the [prime-product reduction](../../README.md). A cut of a tiled convex polygon is a full straight chord from boundary to boundary in the union of tile edges. There may be arbitrarily many T-junctions on the chord. A cut is proper if both resulting regions have positive area. Reflections and all tile directions are allowed.

**Theorem.** Given any tiling of either board, make proper cuts in its tile edges in any order until every remaining piece admits no proper cut. For **3431**, at least one remaining piece is one of four specific convex polygons, of area **924, 2111, 2311 or 3431** in tile units. For **5063**, a remaining piece has at least **455** tile areas. If all remaining pieces have fewer than 1820 tile areas in the latter case, a particular triangle with sides 455, 559 and 624 must itself admit a tiling by (35,13,43). Neither whole board can be produced by cutting down to individual tiles. The theorem includes the possibility that the board itself admits no proper cut.

| Board | Fixed tile | Shapes in the initial certificate | Physical chords checked over the family | Lower bound on an uncuttable piece |
|---:|---|---:|---:|---:|
| 3431 | (33, 7, 37) | 19 | 76 | 924 |
| 5063 | (35, 13, 43) | 31 | 224 | 455 |

Existence of an unrestricted unit tiling of either board remains open in this work.

## Six possible first cuts

Use coordinates in the basis $1,\rho$, with $\rho=e^{i\pi/3}$. The 60-degree corner is the origin, and the two sides issuing from it have lengths $a(a+2b)$ and $b(2a+b)$. The third side has length $c^2$. The following are necessary possibilities for a proper first cut. Every cut joins interior points of the two sides incident to the 60-degree corner. No cut starts at a vertex or touches the opposite side.

| 3431 distances from the corner (longer side, shorter side) | Tiles cut off | 5063 distances (longer side, shorter side) | Tiles cut off |
|---|---:|---|---:|
| (231, 231) | 231 | (455, 455) | 455 |
| (231, 280) | 280 | (455, 624) | 624 |
| (280, 231) | 280 | (624, 455) | 624 |
| (462, 462) | 924 | (910, 910) | 1820 |
| (560, 462) | 1120 | (1248, 910) | 2496 |
| (1320, 231) | 1320 | (1680, 455) | 1680 |

For 3431, the [unrestricted fixed-tile exclusion at 280](f1_280/PROOF.md) removes the first three rows. The 280-tile triangles in the two orientations are congruent to that excluded triangle. The 231-tile equilateral triangle extends to the excluded triangle by adding one ordinary scale-7 tile grid, as checked below. An [earlier certificate](../../../../2026-11-19/nov19/equilateral231/cert/README.md) already excluded that equilateral case independently. The three remaining chords cut off areas 924, 1120 or 1320. A tiling could also have no proper chord.

## Why the chord list is exhaustive

Write $z=(a+b\rho)/c=e^{i\beta}$, where $\alpha+\beta=\pi/3$ and $2\pi/3$ is the third tile angle. The rational number $2\cos\beta=(2a+b)/c$ lies strictly between 1 and 2. If $\beta/\pi$ were rational this number would be a rational algebraic integer, which is impossible. Hence $\alpha,\beta$ are linearly independent over the rationals. Every corner of a tiled convex polygon has angle $m\alpha+n\beta$ for nonnegative integers $m,n$, because $2\pi/3=2\alpha+2\beta$.

The outer angles are $2\alpha,2\beta,\alpha+\beta$. At an interior point of a side, a cut divides $\pi=3\alpha+3\beta$. At an existing corner it divides that corner's angle. Uniqueness of the two integer coefficients shows inductively that every corner angle of a piece obtained by cutting has $0\le m,n\le3$. Its exterior turn has the same bounds, by subtraction from $(3,3)$. Relative to one of its boundary sides the direction of a cut must therefore be among the directions obtained by rotating through one of these angles. This argument uses only the angles at endpoints.

Each side of a tiled convex polygon is a union of whole unit-tile sides with disjoint relative interiors. Its length belongs to the additive semigroup $S=\langle a,b,c\rangle$. For a cut endpoint in the interior of a side, both offsets to the ends of that side belong to $S$. The chord length also belongs to $S$. Endpoints lying at old vertices are included.

Use the oriented edge notation $(L,h,j)$ for the vector $Lz^h\rho^j$, with $j$ modulo 6. Tile directions belong to this group after fixing one reference edge, because a path through the interior can be perturbed to cross shared segments away from vertices. The height and phase are unique by irrationality. Two further integer tests follow from boundary addition. Give an oriented segment of length $L$ the respective values
$$
 L(-1)^j,\qquad L(-1)^{j+h}.
$$
Opposite directions have opposite values and splitting a segment preserves its value. A standard tile has counterclockwise sides $(a,0,0),(c,-1,3),(b,0,5)$. Its values are $a-b-c$ and $a-b+c$. Rotation or reflection can change the signs of these values. For a polygon of area $M$ in tile units the two boundary sums divided by the respective tile values must thus be integers of absolute value at most $M$ and parity $M$. Internal contributions cancel even on partial side contacts. The area $M$ itself must be a positive integer, obtained by dividing the axial shoelace sum by $ab$.

The checker enumerates every allowed offset on every side. For each allowed **unoriented** line direction it groups all candidate boundary points by the integer determinant with that direction. Pairs in the same group are collinear. It discards tangents, checks the Euclidean chord length, reconstructs both polygons and applies the necessary conditions above. The coordinates are rational in the axial basis. All collinearity tests use a common integer denominator. Translations and rotations of whole polygons are unrestricted.

## The finite proof

The two JSON files list cyclic sequences of oriented edge triples. A polygon is identified up to translation, rotation, reflection and cyclic relabelling. Each list ends with the original board. The verifier checks strict convexity, area, and the following property for every polygon in order.

*For each chord passing the necessary tests, at least one of its two children occurs earlier in the list.*

In an actual tiling, follow this child whenever the distinguished piece is cut. Cuts of other pieces do not affect it. Each such step lowers its index, so a maximal sequence of cuts leaves an uncuttable member of the list. All listed areas are at least $ab$. This proof works for any order of geometrically possible cuts, including configurations involving orientations absent from the outside of the board. The counts in the table count all physical chords on the chosen representatives, including symmetry-related chords.

More precisely, set $N=(a+2b)(2a+b)$. The distinguished piece has an area in
$$
\{N,\ N-a(a+b),\ N-4b(a+b),\ 4ab\}
\ \cup\ \{b(a+b)-k^2:0\le k\le b\}.
$$
At the minimum $ab$, the family contains two shapes. One is equilateral of side $ab$. The other has counterclockwise edges
$$
(bd,0,0),\quad(ab,0,2),\quad(ab-bd,-1,4),\quad(ab,-1,0),
\qquad d=a+b-c.
$$
Neither of these two polygons admits a proper chord passing the tests. Consequently any actual tiling that can be separated into pieces of at most $ab$ tiles must contain a copy of at least one of these two specific shapes. This statement concerns one distinguished leaf. It does not classify every possible piece of area $ab$.

## Removing all the small members on the 3431 board

Let $F$ have vertices $0,ab,b(a+b)\rho$. Its sides are $ab,bc,b(a+b)$, its area in tiles is $b(a+b)$, and it is one of the listed family members. Every other listed member of area at most $b(a+b)$ is a child of a straight cut of $F$ whose **other child is an integer-scale copy of the original tile**. The checker locates the actual cut for every such member and verifies the complementary triangle up to rigid motion and reflection. Consequently a tiling of any one of the smaller shapes would extend to a tiling of $F$.

For (33,7,37), [three exact endpoint proofs](f1_280/PROOF.md) exclude every tiling of $F$, including nonslicing tilings. This rules out all 15 smaller members. The four remaining areas are 924, 2111, 2311 and 3431. At area 924 the shape is the side-462 equilateral triangle. The two quadrilaterals are complements of the corner triangles on 1320 and 1120 tiles, respectively. The final member is the complete original board.

For (35,13,43), 27 of the 31 members extend to its 624-tile $F$. Deciding this fixed triangle would determine whether this whole group can be excluded by the same argument. The remaining four areas are 1820, 2567, 3383 and 5063.

## A constructive complement

In the reflected coordinate system with board vertices $(0,0),(a(a+2b),0),(0,b(2a+b))$, put $s=ab$. Cut off the equilateral triangle with vertices $(0,0),(2s,0),(0,2s)$. Its far side contains $(s,s)$. Joining that point to both far board vertices divides the complement into ordinary tile-similar triangles of scales $a,b,c$. Their standard grids give $a^2+b^2+c^2$ unit tiles. Thus a tiling of the equilateral triangle of side $2ab$ by the specified tile would complete the original board. Its required counts are 924 and 1820. The verifier checks every block's metric, containment, pairwise separation and total area.

Dividing that equilateral region into four congruent equilateral triangles of side $ab$ gives a straight-cut geometric partition into pieces with at most $ab$ tile areas, after subdividing the three grids. This attains the bound for the relaxation that tests area, angles, side lengths and the two boundary sums. For the 3431 board the fixed-tile exclusion at 280 precludes filling any of those four equilateral pieces. For 5063 their actual tileability is undecided here.

## Reproduce

Run from any directory with standard Python 3 and assertions enabled.

```sh
python3 verify.py
```

The unrestricted 280 exclusion has its own [C++ replay](f1_280/PROOF.md). The lists are proof inputs. Search logs and a solver installation are unnecessary. The checker also replays cuts of a twice-enlarged tile and a basic trapezoid tiled by grids of scales $a,b,c$. The finite families were found by a separate depth-limited search using ray and side intersections. The supplied verifier instead groups boundary points on lines. This gives a separate computational replay, without a claim of external peer review or a proof-assistant build.

[Additional tests on the 624-tile triangle and a limit of direction-only group invariants](RESEARCH_NOTES.md).
