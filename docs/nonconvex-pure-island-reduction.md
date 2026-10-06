# Pure islands beyond convexity: lattice phases and tile-count divisibility

6 October 2026. Denis Paliy, research with ChatGPT assistance.

This note extends a necessary restriction to **all finite pure all-long-edge
regions**, allowing holes, nonconvexity, and vertex contacts. It also proves
a dissection lemma for polygonal disks and records a quantitative limit of
the earlier convex replacement theorem. General nonconvex chirality exchange
and Erdős problem 634 remain unresolved. The proofs were checked in separate
internal mathematical passes; external review or priority is not claimed.

## 1. Setting and results

Fix a primitive integral 120-degree triangle:
$$
\gcd(a,b,c)=1,\qquad c^2=a^2+ab+b^2.
$$
In short Eisenstein coordinates, with $\rho=e^{i\pi/3}$, put
$$
L=\mathbb Z[\rho],\qquad u=(a+b,-b),\qquad w=(b,a)=\rho u.
$$
The reference tile has vertices $0,u,(a,0)$. A pure tiling uses only
translations and the six rotations of this reference tile. Its short-edge
directions and long-edge directions are distinct classes modulo $\pi/3$.
Assume that every positive-length boundary segment of the tiled region
has a long-edge direction. The region need not be convex or simply connected.
All tiles have disjoint interiors; T-junctions are allowed.

**Theorem A — phase decomposition.** Partition the tiles according to the
translate of $L$ containing their vertices. Each group is itself a pure
all-long-edge region. Its long edges either match one whole long edge of
another tile in the group or lie wholly on its boundary. There is no
short-edge boundary. The group may have holes or more than one component.

**Theorem B — count divisibility.** If $N_\lambda$ is the number of tiles
in any nonempty lattice-phase group, then
$$
\boxed{2c^2\mid N_\lambda.}
$$
Consequently every finite pure all-long-edge region has
$$
\boxed{2c^2\mid N.}
\tag{1}
$$
This statement includes regions with holes and with initially incompatible
long-edge subdivisions. There are at most $N/(2c^2)$ nonempty phases.

**Theorem C — geometric dissection for disks.** If the original region is
a simple polygonal disk, straight long-direction cuts along existing tile
edges dissect it into polygonal disks with whole long-edge matching and
one short-lattice phase in each. No unit tile is cut, discarded, or replaced.
Convexity of the resulting pieces is not asserted.

Thus opposite-state replacement for simple pure disks reduces to its
nonconvex, fully matched lattice subclass. This is a reduction, not a
proof that the replacement exists.

## 2. Short contacts preserve the lattice phase

Each tile's vertices belong to one translate of $L$, since all its edge
vectors are integral short-lattice vectors. This labels a tile by a coset
$\lambda(T)\in\mathbb R^2/L$.

Consider a maximal connected collinear union of short tile edges. Every
generic point of it is internal to the original region: an exterior edge
cannot have a short direction. At such a point the opposite incident tile
must also have an edge on that line. An interior point of an opposite
triangle would overlap the first triangle; a long edge has the wrong
direction. Therefore both sides partition the same finite interval into
whole short edges of lengths $a$ or $b$.

Both partitions start at the same interval endpoint. Every endpoint in
either partition differs from that common point by an integral multiple
of the short-direction unit vector. Hence tiles with a positive-length
short contact have equal lattice cosets. This argument works separately
on each connected interval and does not use convexity, absence of holes,
or an edge-to-edge hypothesis.

It follows that all short edges cancel internally within each phase group,
after subdivision at T-junctions. Such a group has no positive-length
short-direction boundary.

## 3. Same-phase long contacts are automatically whole

Primitivity implies $\gcd(a,b)=1$, so the vector
$u=(a+b,-b)$ is primitive in $L$. Every $\rho^ju$ is primitive as well,
because rotation acts unimodularly on the short lattice.

Take two collinear long edges in one phase and orient both with displacement
$u$ after a permitted rotation. Their starting-point difference is $tu$
for a real $t$, and belongs to $L$. Thus
$$
t(a+b)\in\mathbb Z,\qquad tb\in\mathbb Z.
$$
Bezout's identity gives $t\in\mathbb Z$. Positive-length overlap between
two intervals of unit length in this parametrization requires $|t|<1$.
Therefore $t=0$: the whole edges coincide.

There can be only one tile on each side of such a whole edge, since tile
interiors are disjoint. If a tile's long edge has any positive-length
internal contact within its phase group, that contact is whole. Otherwise
the entire edge belongs to the group's boundary. This proves Theorem A.
In particular, arbitrary offsets between different phases do not invalidate
the theorem: they are precisely the interfaces separated by the grouping.

## 4. Count divisibility without topological assumptions

Fix one phase group. Sum the counterclockwise boundaries of its tiles.
Short edges cancel by section 2, and internal long edges cancel in whole
pairs by section 3. What remains is a balanced directed graph of **whole**
long edges. Its incidence boundary is zero. It decomposes into finitely
many closed directed whole-edge walks, including multiplicities.

Each walk, after translating its initial vertex to zero, belongs to
$\mathbb Zu+\mathbb Zw$. Different walks may use different translates;
they need not be simple, and they need not have positive signed area.
The determinant of $u,w$ in short coordinates is $c^2$. The shoelace
formula therefore makes each walk's signed Euclidean area an integer
multiple of $c^2\sqrt3/4$.

Signed-area cancellation identifies the sum of these walk areas with
the actual sum of the tile areas. Holes contribute with the appropriate
opposite orientation; vertex contacts cause no problem. For an integer $K$,
$$
N_\lambda\frac{ab\sqrt3}{4}=K\frac{c^2\sqrt3}{4}.
$$
Since $\gcd(ab,c^2)=1$, this proves $c^2\mid N_\lambda$.

There is also an independent parity restriction. Assign a directed long
edge of direction $\rho^ju$ the value $(-1)^j$ times its length, and a
short edge of direction $\rho^j$ the value $(-1)^jz$ times its length.
The reference triangle's boundary has formal value $c+(b-a)z$; rotating
it through $\pi/3$ changes its sign. Internal overlaps cancel, whereas the
group boundary has only long directions. Since $a\ne b$, the coefficient
of $z$ forces equal numbers of even- and odd-rotation tiles. Thus
$N_\lambda$ is even.

Finally $c$ is odd: for coprime $a,b$, the value of $a^2+ab+b^2$ is odd
modulo 2. Combining parity and $c^2\mid N_\lambda$ proves Theorem B.
The same proof applies to each positive-length contact component inside a
phase, since its boundary also consists of whole long edges.

**Small-count consequence.** If a nonempty pure region has $N<4c^2$,
then $N=2c^2$, it has only one phase and one positive-length contact
component, and all its internal long edges match whole-to-whole.
Existence of an island with $2c^2$ tiles is not asserted.

## 5. Straight crosscuts preserve disks and whole tiles

For a simple polygonal disk one can strengthen the algebraic grouping to
an actual finite dissection into disks. This part does not require an
initial common lattice.

On a long-direction line, take the finite union of positive-length
internal long-edge contacts, restrict it to the interior of the current
polygon, and split at all boundary points. Consider a maximal nonempty
interval $I$. On each side of the line the contacting edges form a
partition with constant endpoint phase modulo $c$. Only the initial and
terminal edge can extend past an endpoint of $I$ on the polygon boundary.

If an endpoint $z$ of $I$ is interior to the polygon, both side partitions
must end there. If one edge continued past $z$, its opposite side would
still be internal. At generic nearby points an opposite triangle would
need a collinear edge, necessarily a long edge, extending the contact
chain. This contradicts maximality. Thus an interior endpoint is a common
endpoint of both partitions and forces equal phases modulo $c$.

An unequal-phase contact chain consequently has **both endpoints on the
polygon boundary**. Its closure is a nondegenerate straight proper
crosscut: its interior is internal and it follows tile edges throughout.
The Jordan crosscut property yields two polygonal disks. The open interior
of any original triangle is connected and avoids the crosscut, so the
entire triangle is inherited by exactly one piece. New boundary portions
still have long directions.

Equal phases, conversely, imply whole matching along the chain. At a
boundary endpoint, coincident long edges cannot both continue through
that point: their opposite triangle half-neighborhoods would make it an
interior point of the polygon. This also handles the ends of a chain.

Repeat a cut whenever a piece has a non-whole long contact. The number of
unordered pairs of original tiles having such a contact inside one piece
strictly decreases. No new contacting pair can be created. Thus the process
terminates with whole matching, retaining simple disks and all original
unit tiles. Short-chain phase propagation then places every connected
terminal disk in one short-lattice coset. This proves Theorem C.

The number of terminal disks is at most $N/(2c^2)$ by Theorem B.

## 6. Why side-by-side divisibility does not extend

Let $M=ab$ and take two of the positively tiled seed rhombi from the
[convex theorem](convex-pure-island-classification.md), of side counts
$(M,M)$. In coordinates along $u,w$, their regions can be placed as
$$
[0,M]\times[0,M],\qquad
[\delta,M+\delta]\times[-M,0],\qquad 0<\delta<M.
$$
Their interiors are disjoint, and they meet along a nonzero boundary
interval. Their union is a simple nonconvex pure all-long-edge polygon.

For $\delta=1/2$, the two phases are distinct because $u$ is primitive;
the long-edge subdivisions along the interface do not match whole.
This disproves an unqualified extension of the old common-lattice
argument to nonconvex regions. The straight-crosscut lemma separates
the two original rhombi exactly.

For $\delta=1$, the phases and all internal long edges agree, but the
union has genuine external side segments of length $c$, rather than a
multiple of $abc$. Thus even within the fully matched lattice subclass,
the convex theorem's divisibility of each side cannot simply be retained.
Both examples have opposite-state fillings by replacing their two rhombi
separately; neither is a chirality counterexample.

## 7. The convex move is absent from the small equilateral residual

The convex classification gives the sharp minimum size
$$
N_{\min}^{\mathrm{convex\ pure}}=2abc^2.
\tag{2}
$$
Indeed the side counts are $abx,aby,abz$ with nonnegative integers
$x,y,z$ and at least two positive, and the count is
$2abc^2(xy+xz+yz)$. A seed rhombus attains equality.

For the 120-degree equilateral branch, the
[necessary spectrum](../research/general-spectra/PROOF.md) is
$N=abm^2$, with positive integral $m$. The existing
[constructive tail](../research/group2-trapezoids/PROOF.md) covers every
$$
m\ge T=3\left\lceil\frac{c}{\min(a,b)}\right\rceil.
$$
Every primitive integral norm triple has $a,b\ge3$ and $c\ge7$. Hence
$$
T\le3\lceil c/3\rceil\le c+2<\sqrt2\,c.
$$
For every $m\le T$ this gives $N=abm^2<2abc^2$. Therefore **no tiling
in the entire small interval not covered by this tail contains any
convex pure all-long-edge island at all**. This is true for every tiling,
not just for one chosen construction or an energy minimizer.

For $(a,b,c)=(3,5,7)$, the minimum such island has 1470 tiles, while
$T=9$ and the guaranteed $m=9$ target has only 1215 tiles.

This comparison does not invalidate the convex exchange theorem. It shows
that repeatedly applying that particular local move cannot itself settle
the small equilateral residual. A useful continuation must handle mixed
or nonconvex regions, prove an independent extraction theorem that rules
out high directions, or attack the small-scale existence question directly.

## 8. Exact remaining obligation

Theorems A--C remove incompatible lattice phases as an independent
obstacle, and (1) applies even with holes. They do not make the resulting
pieces convex or supply opposite-state fillings. Neither $2abc^2$ as a
lower bound for arbitrary nonconvex islands nor a convex inherited
dissection has been proved here. Mixed extreme components and the separate
Group-1 angle family also remain outside the present replacement results.

In particular, (2) must not be substituted for the weaker nonconvex bound
(1). The conclusion that the small equilateral interval has no convex
pure islands does not say that it has no nonconvex pure islands.
