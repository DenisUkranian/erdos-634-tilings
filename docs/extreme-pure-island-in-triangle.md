# A nonexchangeable extreme pure island inside an equilateral triangle

6 October 2026. Denis Paliy, research with ChatGPT assistance.

**A triangular target does not force its highest pure component to admit
an opposite-state replacement.** We embed the previously proved
[nonconvex counterexample](nonconvex-chirality-counterexample.md) strictly
inside an actual equilateral tiling. It is the unique component at the
highest short-edge level, and no edge outside it has that level.
Nevertheless it has no opposite-pure tiling.

This is a counterexample to a particular **local reduction**, not to global
orientation normalization. The entire target constructed here has another
tiling using only the two lower edge levels. The example does not solve
Erdős problem 634 or settle any unknown tile-count spectrum. Its large
count records the construction, rather than supplying a new admissible
integer of independent interest.

The argument and exact certificates received separate internal checks.
No external referee approval, formal proof-assistant verification, or
priority is claimed.

## 1. Precise statement and directions

Use the tile with sides $(3,5,7)$ and write planar coordinates in the
basis $1,\rho$, where $\rho=e^{i\pi/3}$. Put
$$
\alpha=\arg(5+3\rho),\qquad \theta=-\alpha.
$$
A direction has **level** $h$ if it is $h\theta$ modulo $\pi/3$.
The levels used below are $-1,0,1$. They are distinct: $2\cos\alpha=13/7$,
and a rational trace of a root of unity must be an integer, so
$\alpha/\pi$ is irrational.

The two short sides of a 120-degree tile have the same direction class
modulo $\pi/3$. The **short level** of a tile is the level of that class.
A component means a connected component in the graph joining tiles with
a positive-length boundary contact; the graph is restricted to the tiles
having the specified short level. Vertex-only contacts do not count.

**Theorem.** There is a tiling of an equilateral triangle by congruent
$(3,5,7)$ tiles with the following properties:

1. The tiles with short level $+1$ form one component, whose union is a
   simple polygonal disk strictly inside the target. Their long edges
   have level $0$.
2. Every edge outside this disk has level $-1$ or $0$.
3. The disk cannot be tiled entirely by the opposite pure family, whose
   short edges have level $-1$ and long edges level $0$.
4. The whole equilateral target nevertheless has a different tiling with
   every edge at level $-1$ or $0$.

Thus even a unique, isolated highest pure component in a triangular
construction need not be removable by an opposite-pure replacement.

## 2. The island and its scaling

In the original short-lattice coordinates of the counterexample, put
$$
u=(8,-5),\qquad w=(5,3)=\rho u.
$$
Rotate the physical frame to make $u/7$ horizontal. The original short
class then becomes
$$
-\arg u=\pi/3-\alpha=\theta\pmod{\pi/3},
$$
so the original pure family has short level $+1$ and long level $0$.
Its opposite family has short level $-1$ and long level $0$.

In long-lattice coordinates with basis $u,w$, the original island has
clockwise vertices
$$
P:\quad (0,0),(0,25),(15,10),(6,10),(6,-15),(-9,0).
\tag{1}
$$
Scale it by $15$ and subdivide each original unit triangle by the ordinary
$15^2$ triangular grid. The scaled island has
$$
1862\cdot225=418950
$$
unit tiles, all in the same pure family. From now on a **macrocoordinate**
$(x,y)$ denotes the physical vector $105(x+y\rho)$ in the rotated frame.
With this convention the scaled island still has the coordinates (1).

The [boundary-inventory proof](nonconvex-chirality-counterexample.md)
requires an opposite-state tiling of the original island to have
orientation-pair populations $(930,-30,962)$. Vector area scales
quadratically, so for the scaled island these would be
$$
225(930,-30,962)=(209250,-6750,216450).
\tag{2}
$$
The negative entry excludes every opposite-pure tiling, including
arbitrary translations and T-junctions.

## 3. An exact opposite-state collar

Take the regular macrohexagon
$$
H:\quad (27,0),(0,27),(-27,27),(-27,0),(0,-27),(27,-27).
\tag{3}
$$
The maximum of $|x|,|y|,|x+y|$ on the vertices of $P$ is $25<27$.
The polygon and its closure therefore lie strictly inside $H$.

The [collar certificate](../research/extreme-pure-embedding/collar.json)
partitions $H\setminus P$ into **1902 unit macrolozenges**. A certificate
row $(i,j,k,l)$ joins the upward triangle
$$
\{(i,j),(i+1,j),(i,j+1)\}
$$
to the downward triangle
$$
\{(k+1,l),(k+1,l+1),(k,l+1)\}.
$$
Here $(k,l)$ is one of $(i,j),(i-1,j),(i,j-1)$, so their union is a
lozenge. Every triangle in the collar appears exactly once.

Two independent integer checks certify coverage. The first enumerates
cells by exact winding tests at their centroids and checks the matching.
The second reconstructs the positive cell-boundary chain without using
that enumeration or matching search. It checks distinct cells, adjacency,
containment in $H$, and cancellation to the boundary of $H$ plus the
clockwise boundary of $P$. Since the cells of the fixed triangular grid
have disjoint interiors, this is an exact geometric partition. Equivalently,
the difference of the two compactly supported planar indicator functions
has zero boundary, and hence is zero.

There are $3804$ collar cells, while $H$ has $6\cdot27^2=4374$ and $P$
has $570$. These area equalities supplement the boundary checks; they are
not being used alone as a coverage argument.

Each macrolozenge has physical side $105=abc$. The
[convex pure-island theorem](convex-pure-island-classification.md)
provides a tiling by $2abc^2=1470$ tiles in either pure family. Use its
opposite-state seed in every lozenge, applying only proper rotations and
translations. Proper multiples of $60$ degrees preserve the pure family.
The collar thus contains
$$
1902\cdot1470=2795940
$$
unit tiles, all of short level $-1$ and long level $0$. It separates the
bad island from the exterior by positive distance.

## 4. Closing the hexagon into a triangle without positive edge levels

The macrotriangle
$$
T:\quad (27,27),(-54,27),(27,-54)
\tag{4}
$$
is equilateral with side $81$. Its complement of $H$ is the union of the
three equilateral corner triangles
$$
\begin{aligned}
&[(27,27),(0,27),(27,0)],\\
&[(27,-54),(27,-27),(0,-27)],\\
&[(-54,27),(-27,0),(-27,27)].
\end{aligned}
\tag{5}
$$
Their interiors are disjoint and their positive boundary chains, together
with that of $H$, give the boundary of $T$. Each corner has physical side
$27\cdot105=2835$. Their placements differ by proper rotations and
translations, so it suffices to tile one corner.

Use the established [three-trapezoid equilateral construction](../research/general-spectra/PROOF.md)
with parameters $(a,b,c)=(5,3,7)$ and multiplier $m=63$, then scale its
**macroregions** by $3$. Its original side is $15\cdot63=945$; its scaled
side is $2835$. The [base certificate](../research/extreme-pure-embedding/corner_base.json)
contains $189$ integer-scale triangle blocks and $63$ strips. Its
independent macrogeometry check verifies all $252$ regions, their
containment, their $31626$ pairwise intersections, and exact coverage.
Scaling preserves this partition.

Subdivide the scaled triangle blocks by their ordinary triangular grids.
For the strips, use the following particular filling, which is essential
for controlling directions.

Before the cyclic rotations, an old strip has horizontal width $R$ and
slant leg $15$ in direction $(-1,1)$, at $120$ degrees. After scaling,
its width is $3R$ and leg is $45$. Fill it with $R$ columns and $9$ rows
of cells having vectors
$$
U=(3,0),\qquad V=(-5,5).
\tag{6}
$$
Split each cell along the segment joining $U$ and $V$. The short squared
lengths are $9,25$, and the long vector $U-V=(8,-5)$ has squared length
$49$. Thus each cell gives two unit $(3,5,7)$ tiles and the strip contains
$18R$ tiles.

Here are all direction classes in this construction. A standard basic
trapezoid has
$$
A=(0,0),\ B=(49,0),\ C=(34,15),\ D=(0,15),\ E=(25,15).
$$
Its three triangle blocks have the following short/long levels:

| Block | Exact long or short vectors | Short level | Long level |
|---|---|---:|---:|
| $AED$ | $E-A=5(5,3)$ is long | $0$ | $-1$ |
| $EBC$ | $B-E=3(8,-5)$ is long | $0$ | $-1$ |
| $ABE$ | $AB$ is horizontal; short vectors are $5(5,3),3(-8,5)$ | $-1$ | $0$ |
| Strip cell (6) | Long vector $(8,-5)$ | $0$ | $-1$ |

The identity $(-8,5)=\rho^2(5,3)$ verifies the stated long direction
modulo $60$ degrees. All subdivisions, cyclic rotations, and corner
placements preserve the direction classes. Therefore **every corner
edge has level $-1$ or $0$**. Each corner contains
$$
9\cdot15\cdot63^2=535815
$$
unit tiles.

The scale-$3$ strip replacement cannot be omitted. The unmodified strip
construction also uses width-$5$, height-$3$ cells, whose long direction
would have level $+1$. Replacing all strips by (6) removes those unwanted
edges without changing the macroregion boundaries.

## 5. Component, obstruction, and the global alternative

The resulting equilateral target has side $8505$ and
$$
418950+2795940+3\cdot535815
=4822335=\frac{8505^2}{15}
\tag{7}
$$
unit tiles. These counts are bookkeeping for the structural example.

Every tile of the central island has short level $+1$, and no tile
outside it has an edge at that level. The island is a polygonal disk,
so its full positive-length contact graph is connected: a generic path
between interior tile points avoids the finite set of tiling vertices.
Consequently it is the unique component of short level $+1$ and is
strictly internal. Equation (2) makes its opposite-pure replacement
impossible, proving the first three parts of the theorem.

A sequence consisting solely of $+1\to-1$ pure-island exchanges confined
to this region cannot eliminate all its $+1$ tiles. Such a sequence would
finish with an opposite-pure tiling of the same region, contradicting
(2). This statement does **not** cover arbitrary lower-state fillings or
mixed replacements that cross the collar.

Finally, apply the same scale-$3$, single-width-strip construction to the
base equilateral multiplier $189$. The resulting side is
$3\cdot15\cdot189=8505$, and every edge again has level $-1$ or $0$.
Thus the entire target has a lower-level alternative, proving the fourth
part. The example exposes the failure of the local component reduction
while leaving the global normalization question intact.

## Reproducibility and scope

The [verification package](../research/extreme-pure-embedding/README.md)
contains the two collar/embedding checkers, the exact collar matching,
the corner base certificate, and recorded reports. The collar certificate
SHA-256 is
`7846a21c439ca5738a49165c61ef8c0aa2120c271a045272d9554211a22b37c8`.
The independent corner macrogeometry checker is the existing
[general-spectra verifier](../research/general-spectra/verify_certificate.py).

The $4822335$ original unit triangles were **not** expanded or tested in
all pairs. Coverage and disjointness follow from the checked hierarchical
partition, previously proved pure seeds, and explicit triangular and
rectangular grids. No claim of full solution, uniform orientation
normalization, or global tile-count classification follows.
