# Equilateral caps and a simple central polygon of any size

Neither the side-462 cap for (33,7,37) nor the side-910 cap for (35,13,43) can be tiled by this construction. Choose any simple central polygon with at least three sides strictly inside the cap, with positive area and no degenerate or straight-through corners. Its corners may be reflex. Each side line also carries a separating arm to a distinct exterior boundary anchor. Each surrounding cell is convex and consists of an exterior arc between successive boundary anchors and two straight segments from those anchors to their intersection at the associated central corner. Require the central polygon and every surrounding cell to be individually tileable. Their individual tilings may include arbitrary rotations, reflections and T-junctions.

| Cap side | Central triangles | Central quadrilaterals | Five or more sides |
|---:|---:|---:|---:|
| 462 | 35 | 40 | 0 |
| 910 | 137 | 440 | 0 |

Counts are distinct multisets of cell shapes after the necessary arithmetic tests. Every listed multiset contains a shape from the independently proved local exclusions of the triangular-cap search, including the 480 quadrilateral. There are 75 such multisets on the small cap and 577 on the large one. The result covers the stated family. It leaves the existence of an unrestricted tiling of either cap open.

## Replay

Run `python3 replay_rings.py /path/to/windmill`. The windmill directory supplies its existing `ears.cpp`, `replay.py` and `local/cases_3431.json`, `local/cases_5063.json`. The local certificates for those cases and the 480 certificate may be replayed separately.

The first enumerator constructs every individually admissible exterior cell in precisely the same way as the triangular-center certificate. Its directed nodes specify an exterior anchor and the inward ray direction. A directed edge records two such nodes, two integral distances and the interior point where their rays meet. It tests true exterior boundary partitions, integral area, and the ordinary and alternating signed boundary identities.

The second enumerator traverses cycles in this directed graph. Its first boundary anchor is the least anchor in cyclic boundary order, and successive anchors strictly increase until the final return. Differences of the two distances attached to a common anchored ray give the signed central side lengths. Their magnitudes must be positive sums of complete unit side lengths. Each completed central corner requires a fan of tile angles. Exact orientation and segment-intersection tests require the core to be simple. They permit a reflex corner and reject intersections between nonconsecutive edges. The open-path tests impose only those same necessary conditions already determined by that partial path. A reverse reachability pass discards nodes that cannot return to the start in the number of remaining steps.

The maximum cycle size comes from the count of distinct boundary anchors present in the graph, since the scheme uses different anchors for different arms. There is no prescribed cutoff on the central polygon size. The search reached at most eight edges in any open path on either cap. The closing area and every individual cell area are recomputed exactly. The verified cells' signed boundaries cancel to the boundary of the original cap, and every multiset is compared against the independent local exclusions. Central triangles reproduce the earlier counts as a control.


## Original boards

The same enumeration on the two full boards yields the following counts before any geometric exclusions of cells. These counts leave possible constructions on both boards. Append `--boards` to the replay command to regenerate them.

| Full board area | Three sides | Four sides | Five sides | Six sides | Seven sides | Eight or more |
|---:|---:|---:|---:|---:|---:|---:|
| 3431 | 111 | 950 | 642 | 232 | 3 | 0 |
| 5063 | 200 | 1603 | 962 | 509 | 77 | 0 |
