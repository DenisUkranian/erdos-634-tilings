# Necessary geometric tests for the 236-tile target

The target has vertices (0,0), (472,0), (236,18) in the chart x+i√21 y. Its side lengths are 472,250,250 and its corner angles are β,β,3α. Each tile has sides 9,20,25, doubled physical area 36√21, and smallest angle β with sin β = 9√21/125. Both facts follow from the cosine rule or Heron's formula. Distances stated below are physical distances.

## Two forbidden strips

Fix any side S of the outer triangle.

1. A positive distance of a tile edge parallel to S is at least 36√21/25. Indeed, choose a point in its relative interior away from all vertices. The tile immediately on the S side of the line has an edge on that line. Its opposite vertex is 36√21 divided by its base length closer to S. Containment in the outer triangle gives the bound. Parallel edges on S itself are exempt.
2. A tile vertex off the line of S has distance at least 81√21/125. Consider first a tile touching S. For each vertex Q of this tile off S choose a vertex P on S. The full side PQ has length at least 9. The acute angle between PQ and the line of S is at least β. To see this, at a point P inside S, the two angular gaps from PQ to the boundary rays on S are each a sum of positive tile angles, hence at least β. At an outer corner the gap towards the ray of S is still at least β, and the supplementary gap is at least the supplement of the outer corner, which is at least β here. Thus each such Q has height at least 9 sin β. The finite union of the tiles meeting S contains a relative neighborhood of S. Its frontier against the remaining tiles consists of straight segments along the edges of this first set, and is disjoint from S. Subdivide the first set's edges at their own ends and mutual intersections; in a nonoverlapping family their intersections give only existing vertex endpoints of one of the tiles. Each frontier segment therefore has endpoints of height at least 9 sin β. The strip of smaller positive height in the target is connected to S without crossing that frontier and is covered by the first set. An additional tile with a vertex in this open strip would have interior there, which is impossible. This proves the same bound for all vertices, including T-junctions.

## Local edge support

On the line of a tile edge take the maximal connected segment made of tile edges. At an internal endpoint of such a maximal segment a tile edge cannot pass through that endpoint along the line. On each side that meets the interior of the region the segment therefore partitions into consecutive whole tile edges. For an interior line of this convex target there are tiles on each side of every open subsegment, except at finitely many junction points. The two partitions of the same maximal segment give integer offsets relative to its same endpoint, because side lengths are integers. This applies to non-edge-to-edge tilings.

For an internal directed tile edge of length L parameterized by [0,L], any tiling supplies a chain of whole opposite edges covering it. Their lengths lie in {9,20,25}. Start at an integer from −24 through zero and move right, using a first edge that reaches positive coordinates, until an endpoint ≥L. For each such prospective edge the two possible congruent triangles on the required side are tested. Reject if some edge has no possible chain. Apply the same condition recursively to candidate neighbors a fixed number of times. Induction on the depth shows necessity, even when choices at different edges are mutually incompatible. Exterior edges need no opposite neighbor. The implementation conservatively keeps unexamined orientations and skips some tests away from the walls.

## Enumeration

The unfiltered previous exact search had 249 nonoverlapping words on each 250-unit leg, and 62,250 leg-pair/apex jobs up to reflection. Checks here retain all previous conditions, including feasible local fans and the existence of a possible base word. No triangulation of the interior is inferred from a surviving job.

| Opposite-edge recursion depth | Words per leg | Pair/apex jobs |
|---:|---:|---:|
| Previous computation | 249 | 62,250 |
| 0 (two strips) | 245 | 60,270 |
| 1 | 189 | 35,910 |
| 2 | 189 | 35,910 |
| 3 | 187 | 35,156 |
| 4 | 187 | 35,156 |
| 5 | 176 | 31,152 |

The depth-four base-word count is 71,096,036,820. At depth five it is 42,667,944,754. Each new job is identified against the original 62,250 by its two oriented boundary words and the three exact vertices of its middle apex tile. All keys are unique, and each new key occurs in the original list. Of the 34,728 old jobs stopped at the 96-node limit, 8,718 fail the new geometric conditions. Combining the two kinds of exclusions leaves **26,010** unresolved at depth four. These are boundary configurations in one fixed branch of the global problem.

An independent exact Python control expands the known 1,475-tile construction with the same angles. All 4,425 true directed edges satisfy both clearance tests, and all 4,321 interior directed edges have whole opposite chains with integral offsets. For 99 internal directed edges the opposite chain was not a single coinciding edge. Both smallest observed positive heights were 36√21/25.

A separate 87-tile partial packing inside the 236-target is certified by exact rational coordinates, lengths, and all 3,741 pairwise interior disjointness checks. Its horizontal seam at height (7/5)√21 violates (7/5)√21 < (36/25)√21. No tiling can extend this packing.

## Reproduction (from this directory)

The C++ assembly uses the accompanying preceding search source at ../../continuation/frontier.cpp and requires C++20 and GMP. The two independent geometric controls use only the Python standard library. The positive control imports the previous triangle-grid expansion and 1,475-tile construction from ../../continuation. No generated executable or 10 MB key inventory is required for archival.

```sh
python check_positive.py
python check_seam.py
python build_filter.py /tmp/beta236
BETA_DEPTH=-1 BETA_KEYS=/tmp/beta-baseline.keys /tmp/beta236 236-pairs 180 1 /tmp/unused
BETA_DEPTH=4 BETA_KEYS=/tmp/beta-depth4.keys /tmp/beta236 236-pairs 180 1 /tmp/unused
BETA_DEPTH=4 /tmp/beta236 236-walls 180 1 /tmp/unused
python compare_jobs.py /tmp/beta-baseline.keys /tmp/beta-depth4.keys
```

## Conditioning on the actual leg tiles and junctions

A stronger filter fixes the entire candidate word on one leg. For every neighbor in the necessary chain test, the candidate must be compatible with each fixed tile, allowing equality with a fixed tile. The recursion is memoized separately for every fixed set. A second refinement enumerates the exact angular fan domains at every junction between consecutive edges on the leg and at the outer apex. A fan option can be discarded when any one of its tiles lacks support against the fixed set. If a domain is empty the word fails. Any triangle shared by all remaining options at one junction is present in every full tiling extending the word; add it to the fixed set. Repeat until a domain empties or no fixed tile can be added. All checks are necessary by induction. Choices at different junctions are never assumed to be compatible merely because they survived these tests.

With unrestricted support depth 3, conditioned-word depth 3 and forced-fan depth 3, 137 words on either leg and 18,906 leg-pair/apex configurations survive. This removes 15,822 of the 34,728 cases which the previous 96-node per-case search did not decide. All 18,906 surviving configurations occur among those former unfinished jobs. The same list can be requested using

```sh
BETA_DEPTH=3 BETA_WORD_DEPTH=3 BETA_JOINT_DEPTH=3 BETA_KEYS=/tmp/beta-joints3.keys /tmp/beta236 236-pairs 180 1 /tmp/unused
python compare_jobs.py /tmp/beta-baseline.keys /tmp/beta-joints3.keys
```

With fixed-fan depth 4 in the last command, the corresponding counts are 136 leg words and 18,632 jobs, all previously unresolved. This removes 16,096 of the 34,728 former unfinished jobs.

The complete list of surviving prior job numbers is in ascending order in remaining236-joint4.txt.gz, one decimal integer per line, with a final newline. Its uncompressed SHA-256 is 3643a901954505f1541c00c730a1c53b3c229ac8f88843c40f8dcad29473fb3e. The script reproduce.py rebuilds the final fixed-fan enumeration and runs the independent checks.

## Search on one specified leg

At each state subtract the fixed tiles from the outer triangle, and enumerate fans at convex sectors of the exact residual boundary within distance 8√21 of the chosen outer leg. Any tiling must contain one of the resulting complete local fans at such a sector. At a given sector a truncated fan list cannot be used to exclude a configuration. The code either skips this sector or uses an exhaustive smaller list. It then selects a sector with fewest complete fan options and branches on each option. Empty options yield a geometric contradiction. Orientation or node limits admit the unresolved word. Choices are tested with one level of edge support against all the fixed tiles; the overall previous static and fixed-fan filters each use depth three. Every exhaustive elimination is valid for the entire triangular target.

At 1,000 search nodes per leg word, the two reflected sides gave 106 and 47 surviving words. Different enumeration orders can reach the upper limit on different cases. The canonical paired-word listing contains all 106 and 47 distinct signatures (this cardinality check is performed in reflect_jobs.py). Reflection across the symmetry axis exchanges the two legs and preserves their outward word labels and the tile shape. A word in a true tiling must therefore appear in both lists. Their intersection contains 47 words. The reflected filter leaves **2,256** of the former 34,728 unfinished jobs, and eliminates 32,472.

```sh
BETA_DEPTH=3 BETA_WORD_DEPTH=3 BETA_JOINT_DEPTH=3 BETA_COLLAR_WIDTH=8 BETA_COLLAR_NODES=1000 BETA_COLLAR_SUPPORT=1 BETA_KEYS=/tmp/beta-strip.keys /tmp/beta236 236-pairs 180 1 /tmp/unused > /tmp/beta-strip.json
python reflect_jobs.py /tmp/beta-strip.json /tmp/beta-strip.keys /tmp/beta-folded.keys
python compare_jobs.py /tmp/beta-baseline.keys /tmp/beta-folded.keys
```

The complete list of 2,256 original unfinished IDs is in remaining236-strip.txt.gz. The 47 viable word signatures used to seed deeper trials are in known47.words. These lists contain potential configurations, without an existence assertion.

## Acute-corner search and the 272 residual jobs

The 47 known signatures split into four disjoint batches in corner-batches. The next search considered all convex sectors within horizontal distance 170 of the appropriate acute base corner, and with distance from the selected leg at most 40√21. At each state, it enumerated sector fans using one level of edge support against the actual fixed tiles. For every fully enumerated domain the tiles common to its options are compulsory. Add compulsory tiles from all such sectors together, rejecting any incompatible pair, and repeat. These forced steps consume no branching budget. For a selected domain of two or more fans, branch over every option with a budget of 3,500 branching nodes per provided word and outer side. A finite cutoff preserves that word.

Reflecting and combining all four complete runs leaves 16 signatures: nine with counts (5,4,5) of edges of lengths (9,20,25), six with counts (0,5,6), and one with counts (0,0,10). The 16 signatures and 272 prior IDs are archived as known16.words and remaining236-corner170.txt.gz. They comprise exactly 16·17=272 canonically ordered pairs and middle-apex choices. The old 34,728 unfinished jobs include all 272, so the combined computation removes 34,456 of the old unfinished jobs. For each batch number 0 through 3, the reproduction command with i set to that number is

```sh
BETA_DEPTH=3 BETA_WORD_DEPTH=3 BETA_JOINT_DEPTH=3 BETA_COLLAR_WIDTH=40 BETA_BASE_REACH=170 BETA_COLLAR_NODES=3500 BETA_COLLAR_SUPPORT=1 BETA_FORCE_ALL=1 BETA_COLLAR_ORDER=5 BETA_ALLOWED_WORDS=corner-batches/236-words-$i.txt BETA_WORD_KEYS=/tmp/corner-$i.words /tmp/beta236 236-pairs 600 1 /tmp/unused > /tmp/corner-$i.json
```

The output of combine_words.py is obtained by passing known47.words and the previous reflected keys, followed by output paths for words and keys and a separate `--batch INPUT_WORDS NEW_WORDS NEW_JSON` for each batch. The program checks that all initial signatures have been accounted for and retains configurations with both words in the resulting set. An independent 96-node-per-job interior search also revisited the full set of 2,256 old IDs, reaching the cutoff on all of them; it contributes no exclusion.

## Ten leg words after extending the corner

Repeated the same acute-corner search on the 16 archived signatures, extending horizontal reach from 170 to 250 and the budget from 3,500 to 6,500 branching decisions per word per side. The four input sets and both enumerations are in corner250-batches. Replace the input file by 236-sixteen-$i.txt in the preceding command. The intersection has 10 leg signatures and **110** leg-pair/apex configurations. All 110 are among the original unfinished jobs; exactly 34,618 of the 34,728 old unresolved cases have now been excluded. The full lists are in known10.words and remaining236-corner250.txt.gz.

The search procedure also constructed a complete nine-tile positive control directly. Its integer-scaled coordinates are in positive9-search.txt. check_search_witness.py independently checks exact lengths, containment, all 36 triangle pairs and equality of total and target area. It can check a putative full 236 witness with the option `--N 236`.

The clearance bounds have a general form for a triangular region tiled by congruent copies of a fixed triangle. For tile area A, largest side M and smallest side m, no internal edge parallel to a target side S occurs at a positive distance smaller than 2A/M. For a vertex off S use m sin δ, where δ is the minimum of the smallest tile angle and the supplements of the two outer angles at the ends of S. The same first-row argument proves it. For the beta triangle the two angle supplements are at least β, giving the numbers above.

The 110 old IDs in the last stage describe 100 configurations up to the complete reflection symmetry of the outer triangle. In each of the ten equal-word cases reflection interchanges the two possible middle apex tiles. Reflection sends (x,y) to (472−x,y) in the chart; reflection_orbits.py verifies this on their exact vertices. All pairs and representatives are in corner250-symmetry-classes.json. Equivalence of two archived jobs is separate from a geometric exclusion.

## An exact 189-tile partial packing and its four-tile obstruction

Independent integer arithmetic checks all side lengths, containment and all 17,766 tile pairs in packing189.txt. The packed area is 189/236 of the target. A specific obstruction prevents continuation. Rotate and translate so the exposed 9-edge of tile 189 runs from (0,0) to (9,0), with that tile below the horizontal axis. The exact coordinates of tiles 121, 186, 188 and 189 after this isometry are in four-tile-pattern.json.

At (1/2,0), any triangle immediately above that edge must have a horizontal side. For each of the six possible oriented triangles, fix a prototype with base [0,L] and translate it horizontally by s. The allowable shifts that put the specified point on its edge form [1/2−L,1/2]. Against each of the three blockers the shifts causing interior intersection form an open interval. For every edge normal of both triangles, project each triangle onto that normal. Interior intersection requires the two projected intervals to have overlapping interiors on every tested axis, giving exact strict lower and upper bounds on s. The intersection of those bounds is the blocker interval. For every one of the six prototypes the union of the three blocker intervals contains the entire closed required interval. The exact endpoints are reported in four-tile-pattern-result.json. Thus the obstruction holds for **all real shifts**, independently of the target walls. The test point is interior to the convex hull of these four triangles: it is interior to the source edge and there are triangle vertices strictly on both sides. Any complete tiling containing this configuration would require an incident tile above some portion of that edge through the point. This is impossible. The elementary proof directly applies to finite tilings; local finiteness suffices as well.

```sh
python check_partial.py packing189.txt
python find_blocked_edge.py packing189.txt
python minimize_obstruction.py packing189.txt packing189-obstruction.json
python check_four_tile_pattern.py
```

The 110 old IDs yield 100 distinct geometric cases. A further targeted search of all 100 returned OPEN for every case with an allowance of 700 branch nodes per side. That run did not record which individual cutoffs or unresolved angular sectors produced OPEN. It supplied no complete packing or exclusion. Neither that pass nor the concrete blocked packing reduces the number of remaining classes.

## Clearance across two finite parallel edges

Suppose the unfilled side of an oriented horizontal edge E faces an edge F parallel to it, with a fixed tile beyond F. In coordinates obtained by a Euclidean rigid motion into the chart, E spans [0,n] on y=0 and F spans [x,x+m] on y=h>0. If h<36/25, every possible neighboring tile across E reaches beyond F's line. For a point p on the base of that tile, its horizontal slice at height h contains some point within (118/9)h of p. Indeed join p to the apex; the horizontal offset is bounded by h√21 cot β = (118/9)h using the smallest tile angle and the supplement of the largest. Therefore the two fixed tiles cannot coexist in a complete tiling whenever (0,n) intersects the open interval (x+(118/9)h, x+m−(118/9)h). Choose a generic point in this intersection, away from tile vertices. Its forced neighboring tile crosses F in the interior of that edge and overlaps the fixed tile beyond it. The interval criterion passed an independent exact check on all 13,712 directed edge pairs at subaltitude positive distance in the 1,475-tile positive control. This general criterion is separate from the stronger four-tile obstruction established above.
