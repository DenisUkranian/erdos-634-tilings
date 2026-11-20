# Two short-edge heights cannot tile the small F1 triangle for 5063

**Theorem.** Let the unit tile have side lengths 35, 13 and 43. Any tiling of the triangle with vertices $0,455,624\rho$, where $\rho=e^{i\pi/3}$, uses at least three distinct short-edge heights. The same conclusion holds for an equilateral triangle of side 455. Both statements allow arbitrary real translations, reflections and T-junctions.

A height is measured modulo rotations by $\pi/3$. If $z=(35+13\rho)/43$, directions have the form $\rho^j z^h$ and the height of a tile is the common $h$ of its two shorter edges. This follows by propagation across positive-length overlaps and the irrationality of the angle of $z$, as in the [cut theorem](../README.md). The F1 triangle has sides $455,559,624$ and area equal to 624 tiles.

## The two bands

The [height-divisibility lemma](../../../../../i120-global-oct7/HEIGHT_LEVELS.md) gives $43\mid n_h$ for $h\ne0$ and $n_0\equiv624\equiv22\pmod {43}$. In particular height 0 is occupied. There is no empty height separating it from another occupied height. Indeed, the outer sides of F1 have heights $0,0,-1$. Let a vacant $k>0$ separate a nonempty positive tail, or a vacant $k<0$ separate a nonempty negative tail. Subtracting the exterior chain on the far side of that cut, which is empty in both cases, expresses that tail's boundary as whole 43-edges of height $k$. For the negative tail the cut is between $k-1$ and $k$. This also applies when $k=-1$. The endpoints of each closed walk in this signed boundary chain lie in a translate of $43z^k\mathbb Z[\rho]$. Its determinant area in axial coordinates is an integer multiple of $43^2$. Since one tile has determinant area 455, coprime to 43, a nonempty tail would contain at least $43^2=1849$ tiles. This exceeds 624. See the [whole-edge cut identity](../../../../../../docs/height-cut-area.md).

Thus every tiling with at most two heights fits in $[-1,0]$ or $[0,1]$. To obtain the equilateral corollary, place the side-455 equilateral triangle at $0,455,455\rho$. Complete it to F1 with the grid triangle $455,455\rho,624\rho$. The grid has scale 13 and short-edge height zero. An equilateral tiling has $n_0\equiv455\equiv25\pmod {43}$ by the same divisibility lemma, so adding the grid preserves its set of occupied heights.

## Consequence for the 5063 board

**Corollary.** Every one of the 27 small distinguished polygons in the [5063 certificate](../README.md) requires at least three distinct short-edge heights in any tiling. Therefore, in every two-height tiling of the 5063 board, every maximal straight-cut decomposition has an unsliceable member of area 1820, 2567, 3383 or 5063 tiles. More generally, if every final member has area below 1820, one of the final members alone uses at least three heights.

Indeed, the [existing geometric checker](../verify.py) embeds each of the other 26 shapes into F1 with a single complementary tile grid of scale $1\le j\le13$. All $j^2$ added tiles have the same short height $t$. Suppose this height were absent in an actual tiling of the embedded polygon. Its completion to F1 would have $n_t=j^2$. The required residue modulo 43 is either 0 or 22, according as $t\ne0$ or $t=0$. The actual residues $j^2$ for these 13 scales are
$$
1,4,9,16,25,36,6,21,38,14,35,15,40.
$$
Consequently the grid adds no new height to any such tiling. The F1 theorem therefore applies to every one of the embedded polygons, including the equilateral member. Euclidean reorientation merely shifts or reverses the indexing of the height set. The four claimed large areas are precisely the other members of the verified family. This implication does not assume that a tiling of the full board contains an F1 triangle.

## Integral coordinates for arbitrary translations

Write $\eta=6+\rho$ and $\bar\eta=7-\rho$. Their product is 43 and $z=\eta/\bar\eta$. For a band $[L,U]$ listed above multiply the plane by $\eta^{-L}\bar\eta^U$. Every tile edge displacement is then integral in the basis $1,\rho$, and so are the target vertices. Each triangle's three vertices belong to one translation coset modulo $\mathbb Z[\rho]$.

Consider any one nonintegral coset. Along each supporting line, take the signed sum of oriented tile-edge intervals from that coset. Its endpoint distribution is zero. Indeed the full tiling has the target endpoint distribution on that line, and restrictions to disjoint endpoint cosets are independent. All target endpoints are integral. A compactly supported sum of intervals with zero endpoint distribution is identically zero as a current. The oriented boundaries of all triangles in the coset therefore sum to zero. Integrating $x\,dy-y\,dx$ gives zero total area, which is impossible for any nonempty collection of counterclockwise tiles. Consequently every tile translation is integral after normalization.

## Two partitions on each line

Fix the supporting line of a candidate edge. Record the intervals that available placements induce on its two sides, with the reversed outer edge as an extra interval on the opposite side at the boundary. In an actual tiling each connected component of their selected union has exactly one interval partition on each side. This follows by examining regular points of the line: an edge on one side must meet another edge on the other, and same-side interiors cannot overlap. The two partitions may have different interior division points.

Orient each available interval from its smaller to its larger coordinate on the line. Each side now supplies a directed acyclic graph. A necessary condition for an interval $[x,y]$ on a particular side is the existence of a common source $s$ and common sink $t$ with a path through $[x,y]$ from $s$ to $t$ on that side and a path from $s$ to $t$ on the other. Both endpoints of that component and all subdivision points are among the listed endpoints. Thus an edge failing this test eliminates its entire placement. Losing a target edge proves infeasibility. The calculation only uses this necessary test, never a sufficiency inference from survivors.

## Certificate and replay

For each band the endpoint generator enumerates 24 oriented templates and every integral translation in the target. Its endpoint implications delete placements. A separate verifier checks the packed implications in order, using three half-plane inequalities for containment, and compares *every* surviving placement with the exported list. The line checker processes these survivors. Its two implementations scan one source at a time or pack 64 sources into each word. Both identify the same failed interval. The computational replay is internal to this project.

| Band | Contained placements | After endpoint replay | Contradicted physical outer side | First failed sweep |
|---|---:|---:|---:|---:|
| $[-1,0]$ | 120,242,057 | 5,450,803 | 455 | 6 |
| $[0,1]$ | 119,919,047 | 3,826,933 | 624 | 6 |

Run the following in this directory on little-endian Linux with a C++17 compiler, standard shell tools and 0.6 GB of scratch disk.

```sh
sh replay.sh
```

[Recorded output](replay.txt), [line-partition checker](check_lines.cpp), [endpoint source changes](target.patch), and [survivor digests](SHA256SUMS). As a positive control the replay checks all four specific placements in a twice-enlarged copy of the tile in both orientations of the band.

Tilings of the original board using additional heights remain possible under these tests.
