# A single lattice path and an explicit nonstraight interface patch

Under the hypotheses of [the full-board theorem](FULL_BOARD.md), suppose
height 1 is absent. Divide coordinates by $cz$, so $O=(0,0)$ and
$B=(a+b,-b)$ in the basis $(1,\rho)$. The entire interface is a
**single simple path in the triangular lattice $R$ based at $O$**.
There are no unidentified phases or components to enumerate. Each
directed edge from $O$ toward $B$ fixes one actual tile on each bank.

## Why every interface edge belongs to this path

Each interface edge is a whole $c$-edge paired on the two banks. Orient
the chain from $O$ to $B$ with the low tiles to the right. Its signed
endpoint boundary is $B-O$. At a vertex global degree is even except
at $O,B$. Two interface edges cannot cross in their open interiors:
the tiles on both banks fill a neighborhood of every such point.

Suppose the interface graph contained a simple cycle. Choose one of
least enclosed area. Its closed interior is in the convex board;
neither extreme vertex $O,B$ can be strictly inside. No interface
edge can be strictly inside that cycle. Indeed an interior cycle would
give a smaller one. In the absence of such a cycle, any nonempty
interior edge set is a forest. Its interior vertices have even degree,
so a tree must attach at least twice to the enclosing cycle. A path
between attachments cuts off a smaller cycle. Two attachments to the
same vertex would already give a cycle. Equivalently one may first
split at every attachment and apply the leaf count.

The open disk inside the chosen cycle would therefore be tiled wholly
by one of the two height groups, by following generic paths that avoid
vertices. Its boundary consists entirely of whole $c$-edges at height
1. The [whole-$c$ boundary bound](../../gap-closure-oct8/structure/WHOLE_C_BOUNDARY.md)
requires at least $2c^2$ tiles inside. Each group in the entire board
has fewer. Thus the interface is a forest. The only possible leaves
are $O,B$. A finite forest with edges and only these two leaves is a
single unbranched path. Each step lies in $R$ in the displayed frame.

In particular the only possible additional contact with the exterior is
$J=(a,b)$ on $OC$. The vector to $B$ is primitive. The vector $B C$
is $(bq/c^2)(-b,a+b)$ with $bq<c^2$ and primitive integral direction.
Also $OC=(ap/c^2)(a,b)$ with $1<ap/c^2<2$. These facts exclude every
other lattice point on the three open sides.

If the path meets $J$, its $O$ to $J$ portion cuts off a high pocket
against the straight segment $OJ$. Its count is a multiple of $c^2$:
in the current frame the closing segment has integral displacement
$(a,b)$, and the interface is a lattice path. The pocket has positive
area and the entire high group has fewer than $2c^2$ tiles, so the
pocket uses exactly $c^2$. The remaining high part then uses $3ab$.

## An exact necessary graph for the complete board

Use axial integer points satisfying
$$
 (a+b)y\ge-bx,\quad ay\le bx,\quad (a+b)x+by\le a(a+2b).
$$
For an oriented unit lattice step $e=\rho^j$ from $P$ to $P+e$, the two
forced apex positions in complex coordinates are
$$
 P+e\,(a/c)\bar z,qquad P+e\,(a/c)z .
$$
The first is on the right, has short height 0 in the original frame,
and makes angle $\beta$ at the start. The other is its mirror on the
left, of short height 2. The second placement on either fixed bank
interchanges those short heights and would put the tile in the wrong
group. Keep the directed edge precisely when both apexes and its two
ends belong to the board. This gives the finite graph in
[interface_graph.py](interface_graph.py). For each surviving simple
$O$ to $B$ path one can test the area and three signed direction totals
of the full-board theorem before attempting either interior.

| Product | Board lattice points | Directed edges after fitting both tiles | Forced straight initial edges |
|---:|---:|---:|---:|
| 3431 | 291 | 1,530 | 5 |
| 5063 | 625 | 3,465 | 3 |

The two tiles fit together along every path edge. In fact once the
path is simple, has its interior off $OB$, and stays in this graph,
all prescribed tiles have disjoint interiors. Each half-pair is inside
the unit equilateral cell adjacent to the segment on its side: its two
base angles are strictly below $60^\circ$. The open part of such a cell
inside the board is connected and contains no path edges. Thus the cell
is on one side of the path closed by $BO$, even when the path touches
$J$. If two path edges touch that cell, their tile sectors at their common
corner have angles $\alpha$ and $\beta$. The orientations of the two edges
agree around the cell and $\alpha+\beta=60^\circ$. The common ray of those
sectors separates their tile interiors. This argument also handles three
edges on a cell and unequal lengths on the common ray.

## Partial tilings beyond the shortest path at scale one

For every remaining odd unit-staircase candidate the detour
$$E^{a-2}\, US\, E\, S\,(-U)E\,S^{b-2}$$
in [the area calculation](FULL_BOARD.md) gives **$2(a+b+2)$ actually
placed tiles** in disjoint interiors. Their shared path has the exact
required area on each side. This construction prescribes the tiles
touching the path; both intervening tile populations still need to be
completed.

To verify containment uniformly, the incenter $W=(a,0)$ has distance
$\sqrt3 ab/(2c)>b/2$ from each board side, since $c<\sqrt3 a$.
For $b\ge7$ the entire radius-3 disk about $W$ is in the board. On the
reference path $E^a S^b$, both half-pairs for the first edge fit at
$O$ along its two bounding rays, and the last pair fits at $B$ along its
two rays. The apex distances on those boundary rays are $a/c$ at $O$
and $b/c$ at $B$, both less than 1, whereas each incident board side is
longer than 1 in these units. For either straight run the pair adjacent
to $W$ is in its radius-2 disk. By convexity of the board, all integer
translates between the end pairs of each run fit. For the changed edges
of the detour the endpoints are within distance 2 of $W$ and each
apex is within distance 1 of its start. These pairs fit as well.
For odd primitive shapes $b=1$ cannot occur. For $b=3,5$ the
parametrization $b=v(2u+v)/g$ gives only the ordered odd triple
$(5,3,7)$, already inside the unit staircase; the checker also verifies
both paths there. Thus the uniform argument covers every residual
mixed-semiprime shape.

For the two first unresolved boards the detour gives **84** and **100**
placed triangles respectively. The replay separately checks every triangle
against the outer half-planes, all three squared edge lengths and every
pair of tile interiors at these two instances. At the two $120^\circ$ turns, an $a$-edge and a $b$-edge share their initial segment; the shorter ends in the interior of the longer. The coordinates exhibit these T-junctions. No interior completion
is inferred from these partial certificates.
