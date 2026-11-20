# Direct polygonal construction targets for 3431

A tiling of the hexagon below by 538 triangles of side lengths 7, 33, 37 gives a tiling of the original 3431 board. Every rotation, reflection and translation is allowed, including T-junctions. No conditions on specified placements in the hexagon are required. A second sufficient target is one simple, connected nine-sided polygon of area 337 tile units. Neither polygon has a known filling in this archive.

The outer triangle has axial coordinates (0,0), (511,0), (0,1551) in a basis at 60 degrees. The integer coordinates in the following table are physical coordinates multiplied by 37. Polygons are listed counterclockwise. The second copy of each polygon is the first translated by (−4662,6105) in these scaled coordinates.

| Data file | Vertices of the first free region | Fixed unit triangles | Free region |
|---|---|---:|---|
| hex538.json | (4662,0), (18907,0), (16863,6204), (13223,9207), (14245,6105), (4662,6105) | 2355 | Hexagon of area 538, one reflex corner |
| region337.json | (4662,0), (9324,0), (9324,2738), (16485,4257), (17885,3102), (16863,6204), (13223,9207), (14245,6105), (4662,6105) | 2757 | Nine-sided polygon of area 337, three reflex corners |
| oct538.json | (4662,0), (9324,0), (9324,2738), (16485,4257), (17885,3102), (16863,6204), (11823,10362), (4662,8843) | 2355 | Alternative octagon of area 538, two reflex corners |

Each file contains every vertex of every fixed triangle. In each dissection the fixed cells and the two polygon copies have pairwise disjoint interiors. Their closed union is the entire board. In particular the nine-sided polygon is one simple Jordan polygon with connected interior. Each dissection leaves two translated copies to be filled.

## Verify or construct

With Python 3.10 or later, use the following commands from this directory. No external package, prior packing certificate or orientation theorem is required.

```sh
python3 verify_538.py hex538
python3 verify_538.py region337
python3 verify_538.py oct538
```

A candidate JSON object has an integer `denominator` and a list `triangles`. Each triangle is an array of three [x,y] integer pairs in any vertex order, representing physical axial coordinates divided by the given denominator. Supply 538 triangles for either area-538 polygon, or 337 triangles for the nine-sided polygon. The output path must be new.

```sh
python3 verify_538.py hex538 candidate538.json --output full3431.json
python3 verify_538.py region337 candidate337.json --output full3431.json
```

The program first checks each fixed placement and the two-copy board dissection. It then checks the proposed region filling, builds the two translated copies, and verifies the full result afresh. The produced file uses the same input format with 3431 triangles.

## Direct proof

The norm of an axial vector (x,y) is x²+xy+y². The checker verifies the squared edge lengths of every fixed triangle with integer arithmetic. For each free polygon it checks simplicity, counterclockwise orientation, the area in tile units and the exact number of reflex vertices. No nonadjacent edges touch. A simple positively oriented polygon bounds a connected bounded interior.

For the fixed triangles and both free polygons, sum the counterclockwise boundary chains and subtract the counterclockwise outer boundary. On every individual supporting line compare the integer jumps at every segment endpoint. They all cancel in the supplied data. The chain itself therefore vanishes on the complement of the endpoints. At a point off all the boundary segments, winding numbers say that the sum of the polygon and triangle indicators equals the outer indicator. Every summand is nonnegative. Thus each interior point off the segments is covered exactly once and the interiors do not overlap. Passing to closures gives coverage on the segments as well.

Inserting a genuine region tiling and its translate consequently gives 2355 + 2·538 = 3431 or 2757 + 2·337 = 3431 placements. The complete coordinate data provide a self-contained proof of these sufficient implications. Failure to tile one of these particular polygons would leave other possible tilings of the original board.

## Origin of the shells

Start from the 3399 exterior cells of the established 3427 packing, with two translated area-16 holes. The previously identified convex 739 target contains 723 eligible old cells. Its 201 constrained pairs collect into two disjoint convex pentagons, each already tiled by 201 old unit cells. The first pentagon has cyclic scaled vertices (9324,2738), (9324,0), (18907,0), (17885,3102), (16485,4257); its mate is its translate by (−4662,6105). Both have physical side lengths 74, 259, 74, 35, 217. Keep the second pentagon, the first pentagon, or both. This respectively leaves the hexagon, the octagon, or the nine-sided polygon in the table.

The free area-538 region consists of the area-16 initial hole and 522 old cells. Remove these 522 cells and their 522 partners from the original exterior. The remaining 2355 cells are the reported fixed shell. Keeping both pentagons instead uses 321 removable cells and their 321 partners, leaving 2757. This derivation explains the construction; the direct checks above do not depend on it. [Earlier geometry and packings](https://github.com/DenisUkranian/erdos-634-tilings)
