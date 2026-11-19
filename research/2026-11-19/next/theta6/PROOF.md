# The 180-tile theta triangle is impossible

A triangle of sides \(90,90,60\) cannot be tiled by congruent triangles of sides \(6,5,9\). This is a fixed-tile geometric exclusion, also called \(\Theta_6(2,3)\). The count 180 itself occurs in other shapes. Combined with the known unit extension and construction at every scale from seven onwards, this also [determines the complete scale spectrum](SPECTRA.md). The following proof admits all real positions, orientations, reflections and T-junctions.

### All true placements occur in a finite pool

Use coordinates \(x+i\sqrt2 y\), outer vertices \((0,0),(60,0),(30,60)\), and \(z=(-1+2i\sqrt2)/3\). The length-five side has direction \(\pm z^h\) in any tiling. All its other sides have direction exponents differing by at most two. The [hand proof](../alpha280mesh/HEIGHT.md) gives the unconditional input bound \(|h|\le80\). Its determinant-divisibility argument uses complete side chains, so it applies to arbitrary T-junctions.

From this bound the successive exact, conservatively rounded cell computations give the following results. A cell records the two coordinate floors of an anchor at mesh \(Q\) divided into \(Q\) parts per unit in each axial coordinate. The programs retain every true tile, even when the two floors admit mutually incompatible witnesses that do not form an actual tile.

| Initial bound \(|h|\) | Mesh \(Q\) | Last pass | Surviving shape/anchor cells | Largest remaining \(|h|\) |
|---:|---:|---:|---:|---:|
| 80 | 3 | 19 | 921,492 | 30 |
| 30 | 18 | 26 | 3,761,162 | 15 |
| 15 | 36 | 40 | 405,450 | 7 |
| 7 | 54 | 21 | 183,706 | 6 |
| 6 | 81 | 18 | 148,725 | 6 |

Each stage regenerates all candidate cells for its entire stated band. Every stage disables both positive-distance clearance conditions. The three rules are (i) closure of the sectors at a tile vertex, allowing straight angles from through-edges; (ii) an opposite edge at each half-integer unit sample on each interior tile side; and (iii) survival of some cell that could contain the anchor of the mirrored placement, since reflection of any true tiling is another true tiling. For (ii), both banks of every full straight contact use integer lengths from a common endpoint, so their half-integer sampling points coincide. For (iii), both possible x cells after reversing and shifting the real point are included, as are both y cells after translation. The reflected tiling need not be identical to the first one. [Vertex-star derivation](../beta/MESH_PROOF.md) · [Mirror rounding audit](../audit/HEIGHT280_REVIEW.md). No cap on incenter packing and no linear programming inequalities enter these five runs.

**Exact lattice.** Write \(O=\mathbb Z[i\sqrt2]\). For \(|h|\le6\), all whole tile-side displacements are in \(3^{-6}O\). For the length-five side this follows from \(3z,3\bar z\in O\). A length-six side may require one extra factor of three in the denominator, absorbed by 6; a length-nine side may require two extra factors, absorbed by 9. All corners are reachable from the origin by a walk along whole sides. Indeed both banks of a maximal straight contact have the same end points, and each of the two banks is partitioned into complete tile sides. A T-joint on either bank connects to the common end by such a walk. Finally the graph of tile interiors connected across positive-length contacts is connected. Thus every anchor and vertex lies in \(729^{-1}O\).

**Exact enumeration.** Inside each surviving \(Q=81\) floor cell, the program enumerates all \(D=729\) anchors. If a run of permitted coarse x indices is \(i,\ldots,j\), the corresponding fine x indices include exactly
\[
\lceil iD/Q\rceil,\ldots,\lceil(j+1)D/Q\rceil-1.
\]
Use \(\lfloor yQ/D\rfloor\) to pick the coarse y row, and intersect with exact containment of all three vertices. Both counterclockwise templates and both signs are enumerated at each height. This gives 11,948,973 placements. For each undirected edge direction, a start event of a selected counterclockwise tile side at any point needs an end event at that point, or the correct target-boundary event; the converse holds for an end. This is cancellation of the oriented subdivided boundary along that line. Applying these necessary constraints removes placements monotonically. At pass 11 exactly 146,434 remain. This is an exhaustive overlist of every individual placement that could occur in a true tiling. [Scanline enumeration](lift_cells.cpp) · [Enumeration trace](lift.log) · [Compressed final pool](../theta6lp/candidates.dat.gz).

### Exact contradiction

The target area is 180 tile areas. The target charge is 180,902,886. No single candidate in the complete pool has score greater than 1,001,552. Even 180 times this maximum gives only 180,279,360. Alternatively, the 180 largest individual scores sum to 180,130,676, which is 772,210 below the target charge. Both computations use integer arithmetic. [Independent vertex-by-vertex checker](../audit/theta6_top_scores.py).

The original threshold version is equivalent as an obstruction. The signed endpoint weights assign the target charge \(180902886\). If \(s(T)\) denotes the score of one placement, the sum of \(\max(0,s(T)-10^6)\) across the entire pool is \(892648\). Any 180 different placements therefore have total charge at most \(180892648\). In a tiling all internal endpoint weights cancel, so the shortfall **10,238** is a contradiction. The floating-point search for weights is dispensable for verification. [Integer weights, verifier and complete calculation](../theta6lp/RESULT.md).

### Consequence for the 280 target

The only triangle left by the arithmetic reduction of \(N=280\) has sides \(90,90,140\) and tile \(6,5,9\). A straight tile-edge segment joining a vertex to the interior of the opposite side would partition that tiling into two tiled triangles, also if the segment contains T-junctions. The base angles are each one tile angle \(\alpha\); only the apex, with angles \(\alpha+\beta+\beta\), can initiate such a cut. One side of the cut has either the single apex sector \(\alpha\), or the single apex sector \(\beta\).

In the first case that subtriangle is similar to the 280 target, with base 90 instead of 140. Its area would equal \(280(90/140)^2=810/7\) tile areas, impossible. In the second case it is a copy of the tile enlarged by ten, which occupies 50 units along the original base and has a cut of length 60. The complement is the \(90,90,60\) theta triangle just excluded. Thus **every** tiling of the 280 target, if one exists, must have no complete straight vertex-to-opposite-side seam. There is no general reason a tiling must have such a seam. [Angular proof](../alpha/VERTEX_SEAMS.md).

Run the Python weight checker alone for the finite inequality, or regenerate the complete geometric pool and compare its digest using C++20 and GMP:

~~~sh
python3 reproduce.py
python3 reproduce.py --rebuild
~~~

[Independent pointwise reconstruction of the complete pool](../audit/THETA6_AUDIT.md). The independently implemented point enumeration agrees on every placement and on every population in the lifting trace.
