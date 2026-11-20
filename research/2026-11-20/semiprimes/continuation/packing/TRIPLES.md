# Two three-tile obstructions on the 3431 board

Each of two disjoint triples of placements in the 3425-unit packing must lose at least one member in any tiling of the 3431 board by (33,7,37). The obstruction holds even if every placement outside the chosen triple is free to move. Each triple lies outside one of the two previously identified pentagons.

Use axial coordinates with common denominator 37. The table gives numerators for the first three placements. Add $(-4662,6105)$ to each numerator pair to obtain the second triple.

| Tile | First vertex | Second vertex | Third vertex |
|---|---|---|---|
| A | (14208,6105) | (12987,6105) | (12987,5846) |
| B | (12876,6105) | (14245,6105) | (13965,6336) |
| C | (14014,7425) | (14245,6105) | (14525,5874) |

On the horizontal line at height $6105/37$, B occupies the upper bank from $12876/37$ to $14245/37$. A occupies the lower bank from $12987/37$ to $14208/37$. Write $U=(14208,6105)/37$ and $V=(14245,6105)/37$. Immediately to the right of $V$, the horizontal ray enters the interior of C. The relative interior of $UV$ is strictly inside the board.

In any putative tiling retaining the three triangles, take a point in the interior of $UV$ that is not a vertex of any tile. Some tile covers its lower bank. Since B fills the upper bank, this point lies in the relative interior of a horizontal side of that tile. The side cannot extend to the left of $U$, where A already fills the lower bank. It cannot extend to the right of $V$, where the ray enters C. So this whole tile side has length at most $|UV|=1$. The shortest tile side is 7. Translation gives the identical contradiction at the second site.

The [integer checker](check_triples.py) verifies the coordinates, the two occupied banks, the open ray into C and membership of all six distinct placements in the final packing. A tiling using different placements elsewhere remains possible.

## At least nine of the 3425 placements must change

A retained edge interval facing empty space must be covered, on its other bank, by a tile outside the original packing. Count the length of all such intervals, subdividing at every old endpoint. The [exact calculation](perimeter_bound.py) gives 1618 for the 3425 packing, with zero uncovered outer boundary length. The portions exposed by A, B and C are respectively 0, 1 and 7 at both sites. These values are Euclidean lengths in the physical units of the tile sides.

Suppose a full tiling removes at most eight of the displayed tiles. Each of the two disjoint triples loses a member, accounting for at most 7 units of lost exposed length per triple representative. Each other removal accounts for at most the full tile perimeter, 77. At least $1618-2\cdot7-6\cdot77=1142$ units of the original exposed intervals still require coverage. The true tiling has at most $3431-3425+8=14$ new tiles, whose combined perimeter is only $14\cdot77=1078$. This contradiction proves the bound. It allows every new tile to take an arbitrary position and orientation and permits T-junctions.
