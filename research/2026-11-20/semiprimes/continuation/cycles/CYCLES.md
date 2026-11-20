# How a region bounded by one triangular mesh can fit in the unit F2 triangle

Consider a primitive odd tile with sides $a>b>0$ and $c^2=a^2+ab+b^2$.
Write $p=a+2b$, $q=2a+b$, $d=a-b$, $\rho=e^{i\pi/3}$ and
$z=(a+b\rho)/c$. The scale-one F2 triangle $T$ has vertices $O=0$,
$B=c^2$, $C=apz^2$. Its third side vector is $C-B=bq\rho z^2$ and
its tile count is $N=pq=2c^2+3ab=3c^2-d^2$. The results below apply
whether or not $p,q$ are prime.

Fix a translated triangular grid of mesh $c$ and an orientation
$z^h$ relative to the board, for any integer $h$. A **supported cycle**
is a simple polygonal loop made of unit grid edges contained in the
union of tile boundaries. Consecutive collinear steps are merged when
counting angles. The rest of the tiling can use any orientations,
reflections or T-junctions. Neither corner patches nor a prescribed
central hole are assumed.

**Results.** Every supported cycle encloses exactly $2c^2$ tiles and is
nonconvex. For the unit triangles at $3431$ and $5063$ it must have at
least two reflex vertices (interior angles greater than $180^\circ$).
In fact the following numbers are sharp *geometric* capacities. Here
$K$ denotes the number of upward grid cells inside the polygon, equal
to the number of downward cells. The capacity allows any rotation and
translation of the grid and requires only the direction balance proved
below. The extremizing polygons are not asserted to be tiled.

| $N$ | $(a,b,c)$ | Tiles a cycle encloses | Required $K$ | Largest $K$ with at most one reflex vertex |
|---:|---:|---:|---:|---:|
| 3431 | (33,7,37) | 2738 | 231 | 193 |
| 5063 | (35,13,43) | 3698 | 455 | 432 |

There are two general consequences. On thin boards the necessary number
of reflex vertices grows with $a/b$. Also, a supported open path from
$O$ to $B$ in the middle grid rules out every noncentral orientation
gap. The existence of a supported *cycle*, or of an entirely middle-grid
path, is not assumed for every tiling. Both original semiprimes are open
in this work.

## Whole-board pairings and constructive limits

The [whole-board theorem](LONG_EDGE_PAIRS.md) gives at least
$4c-2(a-b)+1$ tiles without a long-edge parallelogram mate when
$a\ge2b$, even if no supported cycle exists. The first two bounds are 97
and 129. A [separate modular bound](WHOLE_BOARD_PAIRS.md) remains valid
when the selected pairs may also use one of the shorter sides.

Conversely, every odd F2 board admits an abstract balanced contour of
the required area. For 5063 every mesh rotation and translation works,
and the least number of reflex corners across all placements is exactly
two. For 3431 the minimum is between two and four. [Universal
construction and rational witnesses](BOUNDARY_WITNESSES.md). The
side-aligned rhombus outlines at $a\ge2b$ require tiles outside every
complete parallelogram pairing along $b$ or $c$, even with mixed tile
orientations. [Row obstruction and individual defects](PAIRING.md).

## Area, the three directions, and central symmetry

A supported cycle bounds a union of whole tiles since no tile interior
meets its boundary. The [single-height boundary theorem](../../../../gap-closure-oct8/structure/WHOLE_C_BOUNDARY.md)
applies even when the grid steps are subdivided by tile vertices. It gives
a positive multiple $m$ of $c^2$ with $m\ge2c^2$. The full board has
$N<3c^2$, so $m=2c^2$. In its notation the alternating boundary sum in
units of $c$ is $M=3ab t$, where $t\equiv m\pmod2$ and
$c(c+d)|t|\le m$. As $c+d>c$, the only possible even $t$ is zero.

Let $v_0,v_1,v_2$ be the signed numbers of steps on the axes
$1,\rho,\rho^2$, after removing the common rotation. Closure gives
$(v_0,v_1,v_2)=s(1,-1,1)$ and the alternating sum gives $3s=M=0$.
Thus **each direction occurs as often as its opposite**. Equivalently,
adding the CCW boundaries of all elementary grid triangles in the
polygon gives $M=3(U-D)$, up to the convention for upward triangles.
The area equality gives $U+D=2ab$, since one cell has area
$c^2\sqrt3/4$ and one tile has area $ab\sqrt3/4$. Hence $U=D=ab$.

A convex polygon with this balance is centrally symmetric. Its merged
edge vectors occur in opposite pairs of equal length, and convexity
puts them in cyclic order. The half-turn taking one vertex to the
vertex halfway around the boundary then pairs all the vertices.
Any centrally symmetric set in a triangle occupies at most $2/3$ of
its area. To see this, let $s=(s_1,s_2,s_3)$ denote the barycentric
coordinates of its center. The overlap of the triangle with its
reflection consists of the points $0\le x_i\le2s_i$, $\sum x_i=1$.
If all $s_i\le1/2$, its relative area is
$1-\sum(1-2s_i)^2\le2/3$ by subtracting the three corner triangles
and applying Cauchy's inequality. If $s_1\ge1/2$ after relabeling,
the overlap in $(x_2,x_3)$ is a rectangle of relative area
$8s_2s_3\le1/2$. A center outside the triangle gives empty overlap.
Our region occupies $2c^2/N>2/3$ and must be nonconvex.

More quantitatively, for *any* proposed center at least $2d^2/3$
tile-areas of the region have no reflected mate in the region. This is
$2c^2-2N/3$. If the half-turn preserves the grid, unmatched cells occur
in equal numbers of the two colors, so at least
$2\lceil ab d^2/(3c^2)\rceil$ cells are unmatched. These bounds give
78 and 80 whole cells on the two controls.

## Consequences for entire tilings

1. On any fixed grid the graph of supported unit segments has at most
   one independent cycle. Each bounded face has positive area and
   consists of whole tiles. Its oriented boundary is a union of closed
   grid walks, with possible bridges occurring in both directions.
   The area and boundary theorem applies with these walks, including
   holes, so the face contains at least $2c^2$ tiles. Two bounded faces
   cannot fit. Euler's formula with all connected components included
   gives the claim.
2. If a short height $k\le0$ is missing between occupied heights, its
   lower tail has a supported cycle. If $k\ge3$ is missing between
   occupied heights the same holds for its upper tail. The tail has
   exactly $2c^2$ tiles by [FULL_BOARD.md](../../FULL_BOARD.md). Every
   interface has the missing height. All incident sides along such a
   line are long: on a maximal straight run of the tile skeleton the
   two banks partition the same interval into lengths $c$ from its
   endpoints. Only one bank is needed on a board side of that height.
   All exterior edges of the far tail, if any, have the missing height
   (only the base can occur, when $k=0$). Thus its nonzero outer boundary
   contains a simple supported cycle of that height. A boundary walk
   stays in a single translate of the grid even if other walks use
   other translates. In particular the geometric restrictions above
   apply to an arbitrarily positioned far tail.
3. Suppose there is any simple supported path of whole middle-grid
   steps from $O$ to $B$ (height 1). It has no open-base contacts:
   in the $cz$ frame the base vector is the primitive lattice vector
   $(a+b,-b)$ and is not a grid direction. The path and the base
   enclose a tiled polygon. Its complementary area is positive since the
   extreme point $C=(ap/c^2)(a,b)$ in this frame is not a lattice point:
   $\gcd(a,b)=1$ and $1<ap/c^2<2$. The population proof for the middle
   cut in [FULL_BOARD.md](../../FULL_BOARD.md) uses only these boundary
   data. Explicitly, area gives $m=tc^2$, $t=1,2$. The two boundary
   characters give $D_L=-c[1+(c+d)r]$, $t\equiv1+r\pmod2$, and
   $D_{\rm all}=c+d$. If $t=2$, then $r$ is odd and the remaining
   $3ab$ tiles would have absolute character at least
   $c(c+d)-(2c+d)>3ab$, since $d\ge2$. Hence the two populations are
   $c^2$ and $c^2+3ab$, both less than $2c^2$.

   A remote gap is now impossible on either side of this path. For
   $k\le0$ cut the low tiles at $k-1$ in each of the two regions.
   Neither exterior has edges below height 0. For $k\ge3$ cut the
   high tiles at $k$; neither exterior has edges above 2. By the
   [whole-edge cut identity](../../../../../docs/height-cut-area.md),
   with height $k$ vacant any nonempty such portion would have a
   boundary chain of whole $c$-edges of height $k$, requiring at least
   $2c^2$ tiles. The identity adds over components, including along
   any arcs of the other board sides visited by the path.

   In addition the middle grid based at $O$ has no supported cycle when
   it contains this path. Otherwise the planar union of cycle and path
   would have a bounded face lying on one side of the path. Its entire
   boundary uses the same grid, requiring at least $2c^2$ tiles in that
   side. In particular the supported middle-grid path is unique.

   Every tiling has an [upper median path](../paths/TWO_PATHS.md) of
   height-1 and height-2 steps. In the presence of a remote gap it must
   actually use **both** heights. An all-height-1 path was just excluded.
   For all-height-2 steps the required displacement $B/(cz^2)=c\bar z^2$
   has second axial coordinate $-bq/c$, which is not integral:
   $q^2=4c^2-3b^2$ and $\gcd(c,3b)=1$. In the residual semiprime domain
   the [shortest-path theorem](../paths/UPPER_RIGIDITY.md) therefore
   raises the minimum from $a+b$ to $a+b+2$ whenever a remote gap occurs.

The [capacity proof and exact computation](ONE_REFLEX.md) classify the
one-reflex boundary shapes. The [thin-board estimate](THIN_BOARDS.md)
gives a uniform bound with no enumeration.
