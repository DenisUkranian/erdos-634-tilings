# Two local repairs in the 5063 triangle

Use the two equal oversize steps of the [published F2 construction](../patches/PENTAGONS.md). In each positive area-$t^2-k^2$ notch, keep the entire positive scale-$t$ grid and subtract the scale-$k$ triangle at its tip. This recovers signed unit placement lists for the old construction. The new packing here removes every positive unit tile whose interior meets either negative triangle.

| Original count | Positive units | Negative units | Positive units removed at each defect | Complete units remaining |
|---:|---:|---:|---:|---:|
| 3431 | 3559 | 128 | 110, 159 | 3290 |
| 5063 | 5071 | 8 | 26, 26 | 5019 |

The two removal lists are disjoint in each row. The replay checks the side lengths, the entire signed boundary identity, containment of every retained tile, and pairwise disjointness of retained tile interiors. For 5063 it also checks that the complement consists of two translates of the following 13-sided region. Its area is 22 unit triangles. Coordinates below are axial with common denominator 43; a vector $(x,y)$ represents $(x+y e^{i\pi/3})/43$.

| Vertex | Numerators | Vertex | Numerators |
|---:|---|---:|---|
| 0 | (34400,12986) | 7 | (39299,13265) |
| 1 | (35905,12986) | 8 | (36179,15540) |
| 2 | (35905,12427) | 9 | (36634,13860) |
| 3 | (36465,12635) | 10 | (34762,15225) |
| 4 | (38337,11270) | 11 | (35217,13545) |
| 5 | (37882,12950) | 12 | (34400,13545) |
| 6 | (39754,11585) | | |

The second polygon is obtained by adding $(-11180,13545)/43$. In either polygon, two corners suffice to exclude every tiling, allowing all reflections, directions and T-junctions.

Use unscaled physical coordinates for the rest of the proof. At vertex 0, on the boundary ray toward vertex 12, some tile must have a vertex there and a side on the ray, since the polygon corner is convex. After choosing this oriented side and the side incident to its initial point, the side lengths and the interior half-plane determine the entire tile. There are six possibilities. Only one fits inside the polygon: the triangle $T$ with corners $(800,302),(835,315),(800,315)$. At vertex 10, toward vertex 11, four of the six possible tiles fit in the polygon. Three intersect the interior of $T$. The remaining tile uses a length-13 segment along the boundary from vertex 10 toward vertex 11. Call its other endpoint $Z$.

Vertex 11 is $W=(819,315)$, in the relative interior of the top edge of $T$. The boundary edge from vertex 10 to $W$ has length 35, leaving $ZW$ of length 22. On this side of the line the unfilled sector at $W$ is convex: $T$ blocks the continuation of the boundary ray beyond $W$. At $Z$ the chosen second tile blocks further continuation along the ray toward vertex 10. Thus the remaining interval must be a concatenation of whole tile sides. Its length 22 is not a nonnegative combination of 13, 35 and 43. This rules out both 22-tile repairs.

The six-candidate containment and intersection tests have a short independent [exact rational checker](two_corner_check.py). It triangulates the 13-gon and uses rational polygon clipping. The [packing replay](packing_replay.py) reconstructs both positive packings from the earlier oversize-band code and checks them directly. Run both with standard Python 3 and assertions enabled. Place this directory next to the earlier `patches` directory or place its original `notchshape.py` next to the checker.

These results concern the fixed partial packings. An alternative tiling of the complete triangle may cross the displayed polygon boundaries.
