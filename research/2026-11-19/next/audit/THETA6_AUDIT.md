# Exact check of the 180-tile auxiliary triangle

For sides \((90,90,60)\) and tile \((6,5,9)\), every putative tiling has 180 tiles by area. Its outer axial coordinates for \(d=i\sqrt2\) are \((0,0),(60,0),(30,60)\).

The absolute short-edge exponent starts at 80 by the [hand-count argument](../alpha280mesh/HEIGHT.md). Four outward-rounded necessary mesh calculations bound it successively by 30, 15, 7 and 6 at mesh factors 3, 18, 27 and 54. They use vertex stars, half-unit contact checks and vertical reflection with both floor/ceiling alternatives. All four work with both terminal-incenter pruning and clearance disabled. The [height-30 replay](theta6-h30-q18-nopacking.log) retains 3,761,162 shape/cell pairs between −15 and 15, and the [height-15 replay](theta6-h15-q27-nopacking.log) ends with 201,821 between −7 and 7. Re-running the bounded calculation at height six and mesh 81 retains 148,725 shape/cell pairs. Its complete cell file has SHA-256 `dc13cdb5664929dbea8c1c59e70cc5688d19debe224957d5806677a8d6c5b075`.

All three vertices of every one of the 52 permitted templates have coordinates in \(3^{-6}\mathbb Z[d]\) relative to their anchor. On a maximal connected straight segment of tile sides within the target, the two banks are each partitioned by whole edges and have the same endpoints. Vertices on either bank thus belong to the same graph component when only whole tile sides may be traversed. On an exterior side there is one bank. Positive-length contacts connect all tiles, and the origin is a tile vertex. Consequently *all* absolute tile vertices lie on this lattice, including endpoints of T-junctions.

The [independent enumerator](replay_theta_lift.cpp) visits the 81 individual denominator-729 anchors in every surviving denominator-81 cell and tests each translated triangle by the three exact half-plane inequalities \(y\ge0,\ y\le 2x,\ y\le 2(60D-x)\). It starts with 11,948,973 placements. For every line direction, a directed edge start or end requires an opposite endpoint at the same point or its prescribed outer incidence. This is the derivative along that line of signed boundary cancellation and also holds at T-junctions. Repeated deletions leave the same 146,434 placements as the scanline implementation, with an element-by-element set comparison and agreement of every intermediate population. The [pointwise replay](theta6-point-lift.log) uses a sparse array of exact point bits and no scanline interval merging.

There is a short independent integer score check. A placement contributes the weight in its outgoing direction less the weight in its incoming direction at each of its three positively ordered vertices. In any tiling the sum equals the outer score by cancellation. Summing the **180 largest** individual scores in the whole pool gives the strongest upper bound available from these individual scores and the tile count alone.

| Quantity | Integer value |
|---|---:|
| Outer triangle score | 180,902,886 |
| Sum of 180 largest candidate scores | 180,130,676 |
| Strict gap | 772,210 |
| Largest single candidate score | 1,001,552 |
| 180th candidate score | 1,000,424 |

The [independent score verifier](theta6_top_scores.py) reads the [geometry and weights](../theta6lp/RESULT.md). The positive gap excludes the auxiliary triangle.

For the 280 target use its actual side lengths \((90,90,140)\). Its base corners receive only \(\alpha\), and its apex receives exactly \(\alpha,\beta,\beta\). These inventories follow from the irrational ratio of the two angles and \(3\alpha+2\beta=\pi,\ \gamma=2\alpha+\beta\). A complete straight seam from a vertex to the opposite open side can therefore start only at the apex. A split \(\alpha\mid2\beta\) creates a subtriangle with base angles \(\alpha\), now with base 90. Its equal sides would have length \(90^2/140=405/7\), incompatible with a sum of whole tile sides. A split \(\beta\mid\alpha+\beta\) creates a scale-ten copy of the original tile. Its seam has length 60 and its portion of the 140-base has length 50. The complementary triangle has sides \((90,90,60)\), which the preceding certificate excludes. This rules out every complete vertex seam for this 280 target. It leaves tilings with no such seam undecided.
