# At 5063 all 215 odd tiles must belong to one native lift

Assume a complete 5063 tiling with $n_{\rm odd}=215=5c$. The [tree theorem](TREE.md) applies without first restricting heights. For this calculation apply the established path isometry $p\mapsto a(a+2b)z^2-\rho z^2\bar p$ to the entire tiling and its lifted graph. Physical heights become $2-h$, the hand reverses, and the sign $\epsilon$ reverses. Thus this section uses **path-frame** odd charge $+43$, even charge $+22$, and $c=43,d=22$. The standard axial core is now the exceptional outer lift at path height two, denoted $C$. The other exterior lift $T$ has path height zero; $B_1$ between them has height one. The two sides carried by $C$ have combined character $-(A+B)=-(2c^2-d^2)$, and the single side at $T$ has character $+c^2$. See the [isometry and exterior conventions](../../../2026-11-20/semiprimes/continuation/charge-transport/geometry/ACTUAL_MEDIAN_CHARGES.md).

## The complete gate equation at an odd lift

Fix an occupied odd lift $v$. Its upward and downward long sides have $c$ possible neighboring physical joint cells per hand, since the two lattice translates intersect at index $c$. The covering tree has one adjacent edge at $v$ for each such neighbor. In normalized coordinates on its physical cell these are precisely the two ordinary gate families $\phi,\psi$ of the [endpoint model](../../../2026-11-21/semiprimes/MINIMAL_ODD_EXCLUSION_5063.md). The indices can be shifted by changing the normalized origin; the shifts in the two families are independent since the two forms are linearly independent modulo 43.

For each incident edge take the component $S$ *away from $v$*. Its boundary root has even physical height. Write $I_C,I_T$ for the inclusion indicators of the two exterior lifts. Let $O$ be the odd charge of this component and $E=dI_C+ce$ its even charge. This form for $E$ follows from summing the per-lift sign congruences in the same path frame. If $Q$ is the signed count of the tiles of $v$ using the gate, subtract the two character identities in [TREE.md](TREE.md) to obtain
$$
Q=(dE-cO-b_S)/c
  =d e +2c I_C-c I_T-O.                                      \tag{1}
$$
Here $b_S=-(2c^2-d^2)I_C+c^2 I_T$. Distinct components at $v$ partition all other short lifts, so the $O$ values come from indivisible lifted populations. Equation (1) is valid even when the same projected prime node, or the same Euclidean cell, contains tiles of other lifts.

The endpoint dual inequalities localize to a single lift: assign their periodic endpoint tables to a side marker only when its lift is $v$. Opposite banks have the same lifted marker. A complementary long edge of physical height that of $v$ has length $c$ and gives zero endpoint difference. No outer side has odd height. Thus the sum of the short-side endpoint potentials over this lift is zero. Normalizing its translate and rotation gives exactly the placement columns already verified in the endpoint certificates. This proves applicability of both the single-gate capacities and the profile cuts, including when two lifts project to the same physical cell. The capacities used below are 16 for a gate of a monochromatic 86-tile lift (magnitude, either sign) and 51 for a positive gate of a lift with signs $(86,43)$. [Capacity and its sign symmetry](../../../2026-11-21/semiprimes/global-closure-next/five-block-two-heights/TWO_HEIGHT_EXCLUSION_5063.md).

## Excluding a split between odd lifts

Every occupied odd lift needs at least two $c$-blocks. The only decomposition of five blocks across more than one lift is $2+3$. At the two-block lift the signs are either balanced or all the same. If monochromatic of sign $\sigma$, the other lift has odd charge $c(1-2\sigma)$. At any gate whose far component contains neither exterior lift, (1) gives
$$
Q\equiv -O\pmod {22},\qquad O\in\{0,43(1-2\sigma)\}.
$$
For $\sigma=+1$, the residues are 0 and 21, neither represented in $[1,16]$. For $\sigma=-1$, they are 0 and 3, neither represented in $[-16,-1]$. A nonempty gate of a monochromatic lift has nonzero current, so all 86 tiles would use at most the two exterior-containing gates, of total capacity 32. This excludes monochromaticity.

The two-block lift is therefore balanced. At the three-block lift $v$, the signs are $(86,43)$ and every other odd lift is balanced. Every far component at $v$ has $O=0$. Two geometric cases exhaust the possibilities:

* If $v=B_1$, its two exterior-containing directions are distinct. The branch toward path height two has offset $+86$ in (1), the branch toward path height zero has offset $-43$, and all other offsets vanish. These are the full **two-offset** profile equations, with $\sum e=0$ since the signed population is 43. All 17,800,359 profiles passing sign reserves were excluded by the [verified two-offset inequalities](../../../2026-11-21/semiprimes/MINIMAL_ODD_EXCLUSION_5063.md).
* If $v\ne B_1$, both exterior markers lie in just one far component, since $B_1$ is the sole odd vertex on their connecting path. The exceptional gate has offset $+43$ and the other 85 gates have offset zero, again with $\sum e=0$. A translation can move that gate to residue zero. If needed, $w\mapsto-\bar w$ on the normalized lattice exchanges the hands and preserves sign. All 9,112,001 profiles passing sign reserves were excluded in the [verified single-offset calculation](../../../2026-11-21/semiprimes/global-closure-next/five-block-two-heights/TWO_HEIGHT_EXCLUSION_5063.md). The earlier application used distinct physical heights. Here the input is the profile inequality proved there, with its assumptions established by (1).

Thus the split is impossible irrespective of the heights and projections of the two lifts. The same argument excludes any isolated 129-tile odd lift of signs $(86,43)$ whenever every far component at it has zero total odd charge.

## Location of the remaining lift

If the only odd lift with short tiles were different from $B_1$, inspect the edge from $B_1$ toward $C$. Its $Q$ would be zero because the marker $B_1$ is empty. Its far component has $I_C=1,I_T=0$, with $O$ equal to 0 or 43. Equation (1), also valid for an empty near vertex, would require $22\mid86$ or $22\mid43$. This is impossible. Hence all 215 odd tiles occupy $B_1$, with signs $(129,86)$ in this path frame. Its projected class is the native $zR$ in the path coordinates, equivalently $A+zR$ in the standard frame before the isometry.

Every even short lift is then adjacent to $B_1$. Otherwise the path from $B_1$ to it would cross a different odd lift. That odd lift is empty and lies away from the two-edge exterior path, contrary to the no-empty-ancestor result in [TREE.md](TREE.md) (root the off-path branches at their attachment to the exterior path). Thus the only short heights are 0, 1 and 2.

In the [previous list](../../../2026-11-21/semiprimes/continued-rigidity/cells5063/REDUCED_CELL_CLASSIFICATION_5063.md), the four-cell matrix has a balanced cell of size $2x$ with $1\le x\le42$, already impossible by $43\mid n_L$. The two-cell alternatives require two occupied lifts and are eliminated above. This removes 218,736 four-cell and 168 two-cell schemes. The one remaining scheme fixes the odd cell, not the even populations, the contact geometry, or the existence of a complete tiling.

The surviving case now satisfies the hypotheses of the earlier single-cell even-region analysis without an extra assumption on the odd phases. If in addition every remote even node is empty, the native gate currents must be $(20,23)$ in the path frame. The full integer tiling is still undecided; an exact positive rational witness survives the corresponding periodic relaxation. [Native even-region bounds and scope](../../../2026-11-21/semiprimes/full-closure-attempt/README.md).
