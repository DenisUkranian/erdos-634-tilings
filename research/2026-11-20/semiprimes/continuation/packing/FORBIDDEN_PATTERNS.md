# A 5063 tiling needs at least ten placements outside the signed inventory

**Theorem.** If the scale-one F2 board for $(35,13,43)$ admits a tiling, that tiling uses at most **5053** of the **5071** positive placements in the two-step signed construction. At least **ten** of its 5063 placements must be new. This bound allows all orientations, translations and T-junctions.

The [inventory packing certificate](README.md) gives maximum independent-set size 5059 for the positive contained placements, with an edge between each pair whose interiors overlap. We exhibit six pairwise disjoint forbidden groups consisting entirely of isolated vertices of this graph. Each group consists of individually legal, mutually compatible placements. It cannot occur inside any complete tiling. A tiling omits at least one member of each group. Adding those six omitted isolated vertices to its inventory intersection would still give an independent set. Hence the intersection has size at most $5059-6$.

## The six groups

Use physical axial coordinates $x+y\rho$, $\rho=e^{i\pi/3}$, with board vertices $0,1079,2135\rho$. Find each of the following three configurations first at origin $(800,302)$ and again at $(540,617)$ by translation. The [certificate](corner_trees.json) gives the first-copy indices in the zero-based [inventory](packing_replay.py), and specifies each corner test. The checker reconstructs the second copy from its exact coordinates and checks all 68 placements for isolation and disjoint group membership.

| Configuration | Tiles prescribed per copy | Nodes in its corner proof |
|---|---:|---:|
| First | 4 | 8 |
| Second | 14 | 13 |
| Third | 16 | 45 |

Here are the four placements in the first configuration, in local axial coordinates with both coordinates multiplied by 43. In the table the letter labels follow the elementary six-tile check below.

| Tile | Numerators of its three vertices |
|---|---|
| A | (1505,0), (0,0), (0,−559) |
| B | (−1505,0), (0,0), (0,559) |
| D | (817,559), (362,2239), (−262,2694) |
| F | (−93,3919), (362,2239), (986,1784) |

A and B come from the ordinary scale-11 bridge. D and F come from the outer parallelogram grid. Another four-tile certificate replaces F by E with numerators (1155,3009), (1610,1329), (2234,874). It follows that retaining A, B and D forces the omission of both E and F. The two versions overlap, so the packing bound counts only the first.

## Corner rule used in the certificates

Let $P$ be strictly inside the board. Suppose $P$ is on two directed rays enclosing an angle in $(0,\pi)$. Each ray has a positive initial segment supported by a prescribed triangle on the side *outside* this angle. A tiling must put a tile inside the sector against the specified ray. This tile has a vertex at $P$: a tile spanning $P$ with a straight angle there would enter one of the two bounding triangles. Its whole triangle lies within the sector by convexity. This argument also holds when $P$ lies in the relative interior of a previously placed edge.

There are only six metric possibilities before the sector test. Let $R$ be the side length along the specified ray, $S$ the other side at $P$, and $T$ the opposite side. The three form a permutation of $13,35,43$. Rotate the ray to the unit vector 1 and write the other vertex relative to $P$ as $x+y\rho$. Then $y=\pm455/R$ by determinant area, and $2x+y=(R^2+S^2-T^2)/R$ by the two squared-distance equations. The choice of sector fixes the sign. The checker enumerates all six, tests containment in the cone, and removes a placement only upon strict interior overlap with a prescribed triangle. Each surviving possibility is added for the next node. At every leaf there are no placements left. Every query point is checked to be strictly inside the original board in both copies.

**A short example.** Include A, B, D, E and F and the tile C with numerators (−262,2694), (193,1014), (817,559). At the local origin the east and northeast rays enclose a $60^\circ$ sector. Four of the six metric possibilities fit against its northeast ray. C excludes three and forces the triangle $(0,0),(35,13),(0,13)$. Its upper side contains $(19,13)$. At this point it and D bound a sector with rays $(1,0)$ and $(-13,48)/43$. Of the four placements fitting against the second ray, E excludes one and F excludes the other three. The shorter four-tile hypotheses follow by branching, as recorded in the certificate.

Run from this directory with Python 3 and assertions enabled.

```sh
python3 verify_pattern.py
```

The [verifier](verify_pattern.py) uses exact rational arithmetic; the [recorded output](pattern_replay.txt) includes all four proof trees. The theorem restricts the changes needed to this specified construction. Existence of an arbitrary tiling of the 5063 board remains undecided here.
