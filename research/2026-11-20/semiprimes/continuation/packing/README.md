# Packing the two original F2 triangles at scale one

In the triangle for 3431 we can place 3421 complete congruent tiles with disjoint interiors. In the triangle for 5063 we can place 5059. These are constructive lower bounds at the original scale. The existence of either full tiling remains open.

| Original board | Tile sides | Candidates inside the board | Matched pairs of overlapping candidates | Exact maximum from the candidate list | Packing after other placements |
|---:|---|---:|---:|---:|---:|
| 3431 | 7, 33, 37 | 3485 | 70 | 3415 | 3421 |
| 5063 | 13, 35, 43 | 5071 | 12 | 5059 | 5059 |

## Constructing and checking the sets of tiles

The [two-step construction](../patches/PENTAGONS.md) has respectively 3559 and 5071 positive unit placements. Candidate indices in this note start at zero in the order returned by [the inventory generator](packing_replay.py). For 3431 it discards 74 placements extending outside the board. The [certificate](inventory_certificate.json) lists deletion indices and pairs of indices. The remaining triangles lie within the board and have disjoint interiors. Each indicated pair has a positive-area overlap, with no index reused between pairs. Any packing chosen from the same list therefore loses at least one triangle per pair. The constructed subset attains the resulting upper bound. The proof needs only side lengths, determinant signs, and the recorded matching.

For 3431 an [explicit exchange](exchange_3431.json) removes eight placements and inserts fourteen. The [geometric replay](check_boards.py) recomputes the three squared lengths and the board containment of every final triangle. It tests all possible overlaps with integer orientation predicates on both triangles, using a bounding-box sweep. Reflections and edge contacts are permitted.

For the 5059 packing the complement has two congruent hexagons, each of area **two** tiles. The longest straight segment in either one has length **1289/35**, strictly less than the longest tile side, 43. Thus the packing is saturated even under arbitrary real rotations, reflections and translations. [Elementary proof, diagram and sharp bound](LONGEST_SEGMENT.md) · [Independent verification over all rotations](SATURATED_HEXAGON.md).

More generally, any actual 5063 tiling must use **at least ten placements outside the list of 5071 positive candidates**, even if every placement in the list may be exchanged. The proof uses six disjoint sets of individually legal placements. At least one tile from each set must move because an enclosed angle cannot be filled. [Proof and exact corner certificates](FORBIDDEN_PATTERNS.md). A [simpler deletion scheme](REPAIR.md) exhibits two larger polygonal regions of area 22 and explains the first local repair obstruction.

Run in this directory with Python 3.10 or later, assertions enabled, and the adjacent project directory named `patches`.

```sh
python3 check_boards.py
python3 diameter.py
python3 verify_pattern.py
python3 packing_replay.py
python3 two_corner_check.py
python3 verify_free_angle.py
python3 replay_clipping.py
```

All calculations in these replays use integer or rational arithmetic. Independent mathematical refereeing and proof-assistant formalization remain outstanding.
