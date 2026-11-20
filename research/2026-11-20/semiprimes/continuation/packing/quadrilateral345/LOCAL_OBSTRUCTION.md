# Independent finite exclusions of the 345 and 480 quadrilaterals and the equilateral of side 455

The (35,13,43) tile cannot tile the 345 quadrilateral, the 480 quadrilateral, or an equilateral triangle of side 455. These independent checks use the polygon sides, the tile angles, disjoint interiors and complete coverage. They allow reflections, arbitrary translations and partial-edge contacts.

Build and replay with GNU C++20.

```sh
g++ -std=c++20 -O2 check_runs.cpp -o check_runs
for shape in 345 455 480; do
  ./check_runs "$shape" > actual.txt
  gzip -dc "runs${shape}.txt.gz" | cmp - actual.txt
done
```

| Shape | Tested side | Physical run cases | Largest search tree | Unresolved |
|---|---:|---:|---:|---:|
| 345 quadrilateral | 260 | 812 | 29 | 0 |
| Equilateral of side 455 | 455 | 12,356 | 215 | 0 |
| 480 quadrilateral | 455 | 12,356 | 235 | 0 |

Each case specifies a physical offset, c-edge orientations and adjacent stopping tiles. The output word OPEN means that a resource or inference limit was reached. Its appearance prevents the certificate from succeeding.

The exact 480 polygon in axial coordinates is (0,0), (455,0), (420,48), (0,468), in counterclockwise order. The short 43 edge joins the second and third vertices. The tested 455 side has corner angles α+β and α+2β. Both exclude γ. The code uses all four true walls of this convex polygon in its containment, endpoint and coverage tests. It uses the actual corner sectors when a selected tile meets either end. It needs no lower length bound on the short edge. The equilateral triangle uses all three of its true length-455 walls and 60-degree endpoint sectors.

## Exhaustion of the starting cases

Write a = 35, b = 13, c = 43, with opposite angles α, β, γ. Then γ = 120° and α+β = 60°. The three supporting sides have γ-free endpoints. Their angles on the 345 quadrilateral are 60° and 2α. Every boundary tile contributes a whole a, b or c edge. Its offset from a side endpoint is a nonnegative integer sum of tile lengths. Every non-c edge contributes one γ angle to an endpoint of that edge. At most one such γ can occur at a single point of the supporting line.

Consequently at least one c edge occurs, since a side consisting of m non-c edges has only m−1 available interior vertices for m obtuse angles. Among the maximal blocks of c edges, at least one is stopped at both ends. A stop is an outer endpoint or an adjacent non-c edge with γ meeting the block. Each gap between consecutive c blocks has at least one stop, by counting γ angles in the gap. At each extreme, the outside gap gives a stop by the same count, including the empty gap at an outer endpoint. There are more stops than blocks.

The 260 side has at most three c edges and each 455 side at most five, by the integer partitions verified in check_345.py. The code enumerates every block size up to the corresponding bound, every possible offset, every one of the two orientations of each c tile and both permissible adjacent non-c side lengths. The γ requirement fixes the orientation of each adjacent non-c tile. The tests on the two remaining boundary lengths and total a, b and c counts are necessary. They may admit additional cases.

## Exact inferences in the search

Coordinates use the axial basis 1, ρ, where ρ = exp(iπ/3). An oriented unit heading is ρ^j z^h with z = (35+13ρ)/43. An increment of mα+nβ takes (j,h) to (j+m,h+n−m). The verifier represents headings with |h|≤8 exactly after multiplication by 43^8. When any otherwise eligible next direction exceeds the represented range, the entire associated branching constraint is skipped. Every search bound produces OPEN.

At a selected tile vertex, and at any genuine polygon vertex in the work area, record the already occupied angular sectors. A point strictly inside a known tile edge occupies an entire half-plane on its tile's side. The exterior angle is included at polygon boundary points. Angular sorting, strict separation of tile interiors, line collinearity and polygon containment all use integer determinants. Tile vertices are enumerated with coordinate differences from a common point to avoid numerical angle computations.

Every true interior vertex has angular inventory (6,6) in the basis α,β. The equality 2 cos β = 83/43 excludes rational β/π, since twice the cosine of a rational multiple of π is an algebraic integer. Thus the coefficients are unique. True boundary angles in the work area also have nonnegative inventories at most (6,6). Every unoccupied sector must admit such an inventory. A sector that can contain a tile edge passing straight through its vertex is skipped unless an actual vertex is forced. In every other sector the two bounding rays independently require a whole tile with a vertex at the point. There are six choices of its two distinct incident side lengths. The code branches over all remaining options on one constrained ray and prunes only when a necessary condition is impossible.

For a straight interval backed continuously by edges of selected tiles on one side, the facing tile edges cover the interval. If both endpoints are known vertices of tiles on the facing side, the interval length is a sum of 13, 35 and 43. A known candidate first edge must leave such a sum to the next known facing vertex. Along a true polygon side its exterior also provides continuous backing. Conversely, if an interior point P is connected along a continuously backed interval to a facing vertex V, and the length PV is outside that semigroup, P lies inside one facing tile edge. The facing half-plane at P is then fully occupied by that tile. This implication is implemented by virtualThrough. The argument allows a T-junction at P. It uses no general premise about integral T-junction offsets.

The code selects a finite set of query points for each run. For every boundary c tile and each of its ends U, define C as the length-c vector into that tile's base from U and A as the vector from U to its third vertex. Test the grid points U+jA+kC over nonnegative j,k with j+k no larger than the number of c edges available from U towards that end of the run. This choice reduces the branching and only omits constraints. A selected tile still has to obey containment and disjointness. A vertex with insufficient other information for a contradiction leaves that search branch OPEN. All three shapes finish with zero such branches.

On the 345 quadrilateral all queried grid points have axial height at most 3·35·13/43 < 32. This follows by equating the axial doubled area of one tile to c times the axial height over its horizontal c edge. Every incident tile has axial diameter at most 2·43/√3 < 50. Below height 315 the polygon agrees with the intersection of its true bottom and its two adjacent boundary half-planes. Its reflex vertex and fourth side lie above this entire work area. The local half-plane containment tests are therefore necessary even for this nonconvex polygon. For the other two shapes the complete domain is convex and all side half-planes are used.

The [packing certificate](placements345.json.gz) and verify_packing.py separately reproduce the 4,373 disjoint tiles in the proposed shell and both translated holes. The local exclusion applies to that shell construction. The original 5,063-area board remains a separate case.
