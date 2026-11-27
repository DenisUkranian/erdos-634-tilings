# A physical area inequality for every subset of the lift tree

Let $N$ be either target in the standard vertex-phase frame, $a,b,c$ its tile sides and $H=\pi\sqrt3\,ab$. In physical length units the outer triangle has perimeter $N$. Define
$$
 G(n)=
 \begin{cases}
    \sqrt{Hn},&0\le n\le H,\\
    N-\sqrt{(N-H)(N-n)},& H\le n\le N .
 \end{cases}
$$
Let $S$ be **any subset** of the positioned lift tree of a complete tiling. Write $n(S)$ for the total number of tiles with short lift in $S$, and $w(S)$ for the sum of the lengths of the whole exterior sides whose marker is in $S$. On each tree edge $e$, let $m_e$ count unmatched whole long-side owners in both banks. Then
$$
 c\sum_{e\in\delta S}m_e \ \ge \max\{0,\ G(n(S))-w(S),\ G(N-n(S))-(N-w(S))\}.
$$
The subset and its complement can both be disconnected. This applies to unions of branches, intervening shells, and sets containing any subset of the exterior markers. At a selected exterior-free subtree its alternating charge also requires $m_e\ge(c+a-b)|E_e-O_e|/c$. All quantities here refer to the same unmodified tiling.

## A convex replacement inside the original triangle

For a finite polygonal union $U$ in a triangle $T$ there is a convex polygon $K\subseteq T$ with $|K|\ge |U|$ and $P(K)\le P(U)$, where the perimeter of $U$ is its full exposed boundary length. This is a geometric comparison; the replacement need not carry tiles or lift labels.

First replace each connected component by its convex hull. The projection-width argument in [the connected proof](SATURATION.md) bounds the sum of the hull perimeters by the original perimeter. If two hulls meet, merge them into their joint convex hull. Its perimeter is at most the sum of their perimeters because their projection intervals overlap in every direction. Its replacement can only enlarge the union. Merge all successive intersections.

To see that two remaining disjoint convex polygons $K_1,K_2$ can be brought into contact inside $T$, consider all translates of a single $K_i$ that lie in $T$. Their union $A_i$ is convex: the set of admissible translation vectors is an intersection of half-planes and $A_i$ is its Minkowski sum with $K_i$. Moreover $A_i$ touches all three sides of $T$. In barycentric coordinates let $m_j$ be the minimum of coordinate $j$ on $K_i$. A translation adds $(d_1,d_2,d_3)$ with sum zero. Its feasibility is precisely $d_j\ge-m_j$. Each particular lower bound can be attained by increasing one of the other coordinates, so some admissible translate meets each side.

Two compact convex subsets of a triangle which each touch all three sides must intersect. Otherwise a line separates them strictly. Perturb it slightly to miss the triangle vertices and keep strict separation. The half-plane containing just one vertex misses the opposite side of $T$, a contradiction. Hence $A_1\cap A_2$ contains a point. Choose target translates of $K_1,K_2$ containing this point. Move them on the straight paths to those translates, staying inside $T$, until the first contact with each other or another component. Before contact their union area and total perimeter are unchanged. At contact take the joint convex hull and merge any further intersections it creates. The union area never decreases, the sum of perimeters never increases and the number of components decreases. Finitely many steps yield the claimed $K$.

The disk isoperimetric bound for $K$, followed above the incircle threshold by the erosion inequality in [SATURATION.md](SATURATION.md), gives $P(U)\ge G(n)$ for any union of $n$ actual tiles. Indeed the tile area is $t=ab\sqrt3/4$, the board inradius $R=2t$, and an inscribed disk of radius $R$ has area $Ht$ and perimeter $H$. If $n>H$, isoperimetry first implies $P(U)>H$. For $P(U)\le N$ invert the erosion inequality; for larger perimeter the conclusion is immediate. Both profile branches are geometrically sharp in $T$. Disks give the first. For the second, dilate the eroded triangle $T_s$ by Minkowski addition of the radius-$s$ disk, $0\le s\le R$. The side lengths and circular arcs give perimeter $N-2Ds$ and area $Nt-Ds^2$, with $D=Nt/R^2-\pi$. These geometric extremizers make no tiling assertion.

## Assigning the physical boundary

Take the actual tile union for $S$. Its oriented boundary equals the assigned exterior sides plus the signed bank chains on $\delta S$. One can derive the identity for arbitrary $S$ from the [single-edge identity](../../../2026-11-26/semiprimes/joint-cell-tree/TREE.md): express its indicator as the root indicator value plus successive child-minus-parent indicator differences along the path to each lift. Summing the single-edge identities telescopes, including the exterior terms. Matched half-turn pairs cancel within their own bank. After subdividing at T-junctions the exposed perimeter is bounded by $w(S)+c\sum_{e\in\delta S}m_e$ by the triangle inequality for oriented segment multiplicities. Apply the geometric bound first to $S$ and then to its complement. The same owners pay on both sides, which gives the maximum in the theorem.

The inequalities also give a joint lower bound on the whole-board unmatched population $M$. Choose any cuts $S_i$ and weights $\lambda_i\ge0$ with $\sum_{i:e\in\delta S_i}\lambda_i\le 1$ for each edge. Multiply their right sides by $\lambda_i/c$ and sum. The result is at most $M$ since every unmatched tile belongs to precisely one gate. The individual signed gate bounds or the contact costs for neutral descendants can be imposed on the very same $m_e$. This accounts for common owners at nested or overlapping cuts.

For the subset consisting of all lifts off the exterior path, $w=0$. Only the edges directly leaving the exterior path appear on its cut. Thus their total number of owners is at least $\lceil G(n_{\rm off})/c\rceil$, in addition to the owners on the two native edges and all strictly deeper edges. This aggregate bound includes charged branches, without a restriction on the total unmatched count or on the number of occupied lifts.

[TRIANGLE.json](TRIANGLE.json) checks the non-disk branch on 47 and 49 genuinely disconnected physical unions in the two complete 143 boards. In addition [cuts.py](cuts.py) reconstructs the exterior, mass and unmatched owners and checks every subset of their support on each full board. Lift vertices outside that support contribute zero to these tests. Reproduce with `python3 triangle.py | diff - TRIANGLE.json` and `python3 cuts.py | diff - CUTS.json`. The tests use $5.43<\pi\sqrt3<5.45$ with exact rational rounding.
