# A single physical circuit at a saturated charged gate

At the first possible unmatched population with an off-spine charge, **one of the two entire outer words is impossible at 3431**. At 5063 the same word is impossible for the increasing-height terminal hand. These exclusions cover every translation of those hands. The surviving contours also have restricted counts in each of their six directions. Both original counts remain **OPEN**.

## A circuit bound for arbitrary exterior-free gates

Use the standard vertex-phase frame of the [lifted joint-cell tree](../joint-cell-tree/TREE.md). Take one edge of that tree with no exterior marker on its far side. Let its actual short-side tile populations have signed sums $E,O$ by parity on the far side. Write $m$ for the number of actual unmatched owners at the gate and $d=a-b$. The sum of their directed whole long sides, with the far bank oriented CCW and the near bank reversed, is the physical boundary of the far union. This uses the lifted cut identity. Subdivision at T-junctions is allowed.

**Circuit theorem.** This chain has an edge-disjoint decomposition into directed Jordan polygons. For each polygon let $n_i$ be its positive enclosed tile count, $q_i$ its oriented height-alternating signed tile population divided by $c$, and $m_i$ its number of whole sides. Then
$$
\sum_i q_i=(E-O)/c,\qquad c\mid n_i,\qquad n_i/c\equiv q_i\pmod 2,\qquad m_i\ge(c+d)|q_i|.
$$
Here orientation multiplies the enclosed signed population by $+1$ or $-1$. The enclosed populations need not be disjoint. If $q_i=0$, then $m_i$ is even and is at least 10 on the 3431 board or 12 on the 5063 board. In particular, a cut of net unit alternating charge with $m\le c+d+8$ or $m\le c+d+10$, respectively, is a single Jordan polygon enclosing exactly its far tiles. At saturation $m=c+d$, every one of its sides has the same sign for the directed height-alternating character.

To see the geometry, normalize the two physical cells to a translate of $R=\mathbb Z[\rho]$ and a translate of $z^{\pm1}R$, $\rho=e^{i\pi/3}$, $z=(a+b\rho)/c$. Both endpoints of every bank interval lie in their intersection. This is a translate of an index-$c$ triangular sublattice. For instance, in the increasing case the generators are $3+4\rho$ and $6+\rho$ for $c=37,43$ respectively. Their norms are $c$, and multiplication by $\bar z$ maps each into $R$. Conversely integrality of $\bar z p$ imposes a nonzero linear congruence modulo the prime $c$. Conjugation handles the other hand. A long edge is primitive on this joint lattice. In its owner's short coordinates its displacement is a unit times $(a,b)$ or $(a+b,-b)$, each primitive already in the short lattice. Two long edges from different banks have different axes. Within one bank and fixed gate a reversed whole coincidence is a half-turn pair, and equal directed copies would have the same interior. Hence the remaining edges have no coincident interiors. Transverse interior crossings would overlap two tile interiors. Primitivity rules out an endpoint in the relative interior of another retained edge. The resulting embedded graph is balanced at every endpoint. Splitting directed closed walks at repeated vertices gives Jordan polygons even at pinches.

Every polygon consists of supported sides, so its winding number selects actual whole tile interiors. The two [boundary characters](../../../2026-11-20/semiprimes/continuation/vertex-phase/pure_cycles/NO_REMOTE_GAPS.md) on its oriented edges have integer sums $cS,cD$, and
$$
 cS=(d-c)(E_i+O_i),\qquad cD=(d+c)(E_i-O_i).
$$
Here the populations include the orientation sign. The two coefficients are coprime to $c$. Thus $c$ divides both sums and differences and, as $c$ is odd, divides each signed parity population. We have $|D|\le m_i$, $D=(c+d)q_i$, and $n_i\equiv E_i-O_i\pmod2$. The doubled axial area is $abn_i$. Applying Pick's theorem **on the joint lattice** gives the more precise positional identity
$$
 ab(n_i/c)=2I_i+m_i-2,
$$
where $I_i$ counts its strictly interior gate-lattice points. In particular $c\mid n_i$, since $c$ is coprime to $ab$. If $q_i=0$, then $n_i\ge 2c$ and $m_i$ is even because $D=0$ is a sum of $m_i$ signs. The isoperimetric inequality gives $m_i^2\ge 2\pi\sqrt3\,ab/c$, which gives the displayed even lower bounds. Winding numbers of the polygons sum to the far-union indicator and yield the total charge identity. For net charge of magnitude one, two or more nonzero signed terms cost at least $3(c+d)$ altogether. A further neutral polygon would require at least 10 or 12 owners.

## Using the charged circuit at the first possible global equality

Assume the [charged-seam equality](../charge-variation/CHARGED_SEAM.md): an off-path charge exists and the total unmatched population is $M=149$ at 3431 or $M=171$ at 5063. In the standard frame the only exterior-free gate carrying unmatched tiles joins the axial vertex $C$ to its odd neighbor $v$, with short height $s=\pm1$. Its banks have exactly $d$ axial and $c$ terminal singles, all of standard sign $-1$. Each remaining tile there belongs to a whole half-turn pair. The two first-cut words are called A and C, in the order listed in the charged-seam proof. The letter C for a word is distinct from the axial vertex.

Let $U_j=\rho^j$. The directed terminal circuit uses $c$ low vectors $cU_j$ with $j=0,2,4$ from the terminal bank, and $d$ high vectors $(a+bU_s)U_j$ with $j=1,3,5$ from the axial bank. Indeed a tile with short hand $h$ and index $k$ has sign $h(-1)^k$. For $s=1$ both effective banks traverse the short broken path's displacement $aU_k+bU_{k+h}$ forwards in their own chart. For $s=-1$ both traverse it backwards. This gives the stated parities. The terminal short lattice has the form $(t,0)+z^sR$, $0\le t<c$, since the joint lattice has index $c$ and contains no shorter horizontal period than $c$. Exclude $(s,t)=(1,0)$, the actual middle neighbor of $C$. A total displacement of zero allows only nine direction inventories per hand at 3431 and six at 5063.

Remove the known axial owners along the first path. In $C$ coordinates the five letters of that path then give, in order of letter number, $cU_0,cU_5,cU_4,(aU_5,bU_0),(aU_4,bU_5)$. Reverse the path and close on the axial sides to obtain the region still covered by axial and terminal tiles. Only its two-dimensional support matters. The checker includes the boundary and tests all three vertices of each candidate bank owner. This is an outer bound on the true owner set even at concave corners. Its signed area in tile units independently equals the board count minus the known middle population and the $2l$ removed axial owners.

## Ordered paths with a fixed direction inventory

Use the [ordered boundary quotient](../../../2026-11-20/semiprimes/continuation/vertex-phase/pure_cycles/NO_REMOTE_GAPS.md) of three cyclic factors of order $a$. Every supported closed walk in the tiled disk has identity word. On this gate a low vector has factor $j\bmod3$ and a high vector has factor $(j+s)\bmod3$. In either case the exponent in that factor equals its physical displacement along the factor axis modulo $a$. This follows from $cz^s=a+bU_s$. In the basis $U_0,U_1,U_2$, use the first coordinate on axis 0 and the second on axes 1 and 2. Intermediate collinear subdivisions give the same product.

For each subinventory $w$ and factor $k$, store the possible start points of a path whose reduced product belongs to factor $k$. Its displacement $D(w)$ depends only on $w$. The empty path is available at all permitted vertices. Use the following two concatenations:

* A single $k$ letter followed by a path with product in factor $k$.
* A nonempty shorter identity path followed by a nonempty path with product in factor $k$.

In a free product, if a path with product in factor $k$ begins with a different factor, the initial syllable has to disappear. At its first disappearance the prefix is the identity: before then any nonempty suffix above that syllable must reduce away to allow the cancellation. If this first return is the last letter, the full identity path is also generated using the factor of its *first* letter. When all three abelian residues vanish, any product in one factor is already the identity. Union the three provisional lists and use the result in every factor for longer paths. Discard states with nonzero abelian residue outside their factor, and proper nonempty states with $D(w)=0$, since they would repeat a point on a Jordan circuit. These operations retain every actual circuit and every parse needed to generate it.

For a split with children $u,v$, intersect the left child's start set with the right child's set shifted back by $D(u)$. The same program computes an upper bound on the doubled signed area at each start. The two child areas, each closed by its chord, add with the correction $[D(u),D(v)]$. Maximize over the same splits. All determinants are integral multiples of $ac$: both displacements lie in the index-$c$ lattice and lie along one common axis modulo $a$ (possibly zero). Store the area divided by $ac$. For the complete positively oriented circuit this value is $b n_v/c$. This sign uses the physical terminal boundary, not a reflected-frame sign convention.

Every original circuit vertex can start a cyclic rotation of the same word inventory. Repeatedly discard vertices failing the full closed-word test. For word C also discard vertices where the maximum area is below the terminal lower bound $n_v\ge185,301$ from the [single-access lifted terminal theorem](../joint-cell-tree/TREE.md). All remaining vertices of an actual circuit survive each pass. The final maximum bounds $n_v/c$, an odd integer, from above.

## Simultaneous currents at actual positions

The residual consists of the singles of the two banks and parallelogram pairs in their respective short cells. On each chart, axis and torus of period $aR$ or $bR$, the signed endpoint differences of each pair vanish. One pair of sides closes on the torus, and the opposite sides of the other pair are translates by a period. Thus the endpoint differences of the singles equal those of the known residual boundary, supported only in the axial chart. In addition, the long edges of the chosen singles conserve flow at each individual physical vertex of the terminal circuit, and their six populations equal the specified inventory.

For word C the program assembles these equations as $Ax=r$ on only those owners whose two endpoints survive the area and ordered tests. Each placement has $0\le x_j\le1$ since its interior can occur only once. A row multiplier $y$ with
$$
 y^Tr > \sum_j\max(0,(A^Ty)_j)
$$
excludes the profile. Numerical optimization may suggest a multiplier; only a strict **integer** inequality excludes a case. A failed optimization or an inconclusive multiplier retains the case.

The [recorded census](STATUS.json) gives every translation, surviving profile and tested population ceiling. The proof uses neither a two-height restriction on the original board nor the native 555/731 bounds. The global equality hypothesis is essential to the census. The circuit theorem itself applies to all exterior-free lifted gates, including cuts containing balanced branches. No contradiction has been obtained for larger $M$ or for the remaining equality cases.

## Replay

Run `python3 replay.py | diff - STATUS.json` with NumPy, SciPy and a C++17 compiler. [Independent checks](review.py) reconstruct both complete 143 coordinate tilings, verify both ordered vertex potentials throughout their unit skeletons and compare the actual pair currents to their exteriors. They also check all 24 directed owner templates against the pre-existing triangle geometry, compare a small grammar calculation at every start against exhaustive ordered words, and count the strict lattice points directly in both previously known positive charged polygons. The 143 tilings do not meet the target equality hypothesis.
