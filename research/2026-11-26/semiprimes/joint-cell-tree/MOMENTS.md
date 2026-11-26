# Independent unsigned-divisibility proof in the physical plane

This proof works on an ordinary Euclidean joint cell $L$, without lifting the tiling to a covering tree. It also gives a gate test on the coordinates of the unmatched owners.

Translate an origin in $L$ to zero and rotate its short height $h$ to zero. Write a lattice point as $x+y\rho$. In $\mathbb F_c$ put $r=-a/b$, $s=1-r$. The two are distinct roots of $t^2-t+1$ for both targets. Use coordinates
$$
u=x+ry,\qquad v=x+sy .
$$
Their determinant in the axial basis is $s-r\ne0$. The original height-$h+1$ long vectors in these coordinates have $\Delta u=0$, since $a+b\rho$ vanishes in the first factor. Height-$h-1$ long vectors have $\Delta v=0$, since $a+b\bar\rho$ vanishes in the second.

**A vector congruence at each gate of each ordinary cell.** Fix the increasing prime and a child of the positive-prime node containing $L$. Use the physical subtree cut identity in the [single-prime transport theorem](../../../2026-11-20/semiprimes/continuation/charge-transport/flux/SIGNED_CUT_TRANSPORT.md). Its crossing edges are the CCW long sides from the two banks, with opposite coefficients. In the normalized parent frame their steps have the forms $c\rho^j$ and $(a+b\rho)\rho^j$. Every one has both endpoints in a single parent Euclidean translate. Thus endpoint divergence can be restricted to the specific translate $L$, even if the prime node contains many other translates. After taking displacement in this restricted divergence, the $c\rho^j$ bank vanishes modulo $cR$.

Here are all possible exterior endpoint terms. An empty or complete exterior chain has zero endpoint divergence even before restricting it. A separating cut has the slant, or the two axial walls together, as its exterior term. Both choices have just $X,Y$ as nonzero endpoint contributions, up to reversal. Separation occurs only between physical heights 0 and 1 or 1 and 2, since the exterior prime nodes lie on that two-edge path. The points $X,Y$ belong to the same parent Euclidean translate. Their normalized difference is a unit times $c^2 z^{2-h}$. It vanishes modulo $cR$ when $h=1$ or $2$. For $h=0$ it can contribute only to the axial core $R$. This verifies that the sum of the CCW long vectors of the height-$h$ tiles of the ordinary cell at this specific gate vanishes modulo $cR$. Repeating with the decreasing prime gives the other hand. Whole half-turn pairs cancel in their original gate.

For the increasing prime within $L$, fixing a child is exactly fixing $u$ modulo $c$, by evaluation at the root of $a+b\rho$. For the decreasing prime it is fixing $v$. With upward and downward long sides oriented as parts of their owner's CCW boundary, put
$$
V_t=\sum_{u=t,\ \mathrm{up}}\Delta v,\qquad
H_t=\sum_{v=t,\ \mathrm{down}}\Delta u .
$$
Every $V_t$ and every $H_t$ is zero at an ordinary cell. Individual gate cancellation is stronger than vanishing of the total vector from each hand.

**Area from either set of contact positions.** The boundary of the union of all short tiles of $L$ is the sum of their long sides, the exterior sides with this short-edge cell, and the negatives of all complementary long sides of height $h$ with this edge cell. This follows by cancellation of the short sides along the actual supporting runs. The complementary long sides have displacement zero modulo $cR$ in this frame. Integrate the affine one-forms $2u\,dv$ and $-2v\,du$ over the boundary, first with integer representatives for $r,s$, then reduce modulo $c$. On a segment $p\to q$ these integrals are $(u(p)+u(q))\Delta v$ and $-(v(p)+v(q))\Delta u$. Both give the transformed doubled area over a closed chain. At an ordinary cell the exterior contributes zero, including the possible slant of length $c^2$. Consequently
$$
(s-r)ab\,n_L=2\sum_t tV_t=-2\sum_t tH_t\quad\text{in }\mathbb F_c .
$$
The just-proved gate congruences and $\gcd((s-r)ab,c)=1$ give $c\mid n_L$. The exceptional core residue follows by subtracting the ordinary cells from the board. The [joint sign congruence](../../../2026-11-20/semiprimes/continuation/common-obstruction/joint/JOINT_CELLS.md) then separates the two sign populations. This proof uses only true physical boundaries. There is no separate-placement assumption for disconnected pieces of the cell.

**Checks.** [moments.py](moments.py) uses the CCW long edges reconstructed from the original triangles. Both 143 tilings pass both area formulas, including their explicit axial wall terms. The ordinary height-one gate vectors vanish individually in both tilings. The earlier [16-tile cylinder packing](../../../2026-11-21/semiprimes/continued-rigidity/global/BALANCED_CYLINDER_COUNTERCONTROL.md) illustrates the distinction between periodic cancellation and a completed tiling. In its normalized coordinates the nonzero upward fluxes are $V_{35}=22,V_{38}=21$ and the downward ones are $H_{13}=40,H_{35}=3$ modulo 43. Both moments give the area residue for 16 tiles. Such a packing cannot be the *entire* population of an ordinary cell in a full tiling. Adding further tiles in its cell can change these residues.
