# Tile cost of sending signed current outside the odd charge subtree

The odd charge variation $V$ of any full F2 tiling satisfies $V\le45$ at 3431 and $V\le63$ at 5063. Both original counts remain open. The proof charges an extra pair of $c$-tile blocks on each branch carrying current away from the subtree spanned by the exterior and the odd charges. It applies with arbitrary heights, translations, reflections and split contacts.

## A disjoint reserve beyond the two banks

Use the reflected path frame, the lifted tree, and the notation of the [gate variation theorem](README.md). The hull $H$ spans both exterior markers and all odd lifts with nonzero charge. For an odd charged vertex $v$, let $G_v=\sigma ck$, let $m=cx$ be its minority population, and let $l$ be its degree in $H$. Each incident edge outside $H$ cuts off a component containing no exterior marker and no nonzero odd charge. These components are pairwise disjoint, even when taken at different charged vertices. A short-to-long edge from such a component can reach a charged odd vertex only across the entering edge at $v$.

On each outward gate let $\sigma Q_i=d j_i$ and $\sigma P_i=c j_i$ denote the signed odd and even owners. This follows from the cut characters with zero odd and exterior terms. For each $j_i\ne0$, the component needs at least $|c j_i|$ even tiles just to supply the even bank. It needs **at least another $2c$ tiles**, as follows.

* If the component contains an odd tile, its short lift is ordinary and balanced. Its two signs are separately divisible by $c$. It therefore contributes at least $2c$ additional odd tiles.
* Otherwise the only occupied short lift in the component is the even root. Any occupied lift farther away would lie beyond an empty odd ancestor, excluded by the [physical mesh-cycle theorem on this tree](../joint-cell-tree/TREE.md). The even root is terminal, with charge $\sigma c j_i$. Its actual size is at least $(91/22)c|j_i|$ or $(83/13)c|j_i|$ on the two boards, respectively, by the [localized single-access bound](../joint-cell-tree/TREE.md#unit-charge-terminal-cost-at-arbitrary-heights-and-odd-populations). Both multipliers exceed three. The root supplies the even bank and the extra reserve from its own population.

Here a branch can contain a balanced population and can carry zero gate current. Gates with $j_i=0$ incur no extra cost in this argument.

Set $p=\lfloor\alpha ck\rfloor+m$, where $\alpha=43/222$ or $8/43$. Write $u=\lfloor p/d\rfloor$. The signed current aligned with $\sigma$ at an individual gate is at most $p$ by the single-gate bound, hence each $j_i\le u$. With $J=\max(0,\lceil(ck-lp)/d\rceil)$, at least $g=\lceil J/u\rceil$ outside gates must carry positive current if $J>0$. When $J=0$ set $g=0$. A positive $J$ with $u=0$, or $g+l>2c$, is impossible.

For a direct accounting check let $t=\sum_i j_i$ over the outward gates. The signed even bank total aligned at $v$ is $dk$. Its remaining gates therefore require at least $|dk-ct|$ even owners. Together with the outward components one must pay at least
$$
\sum_i c|j_i|+|dk-ct|+2cg\ \ge\ dk+2\max(0,cJ-dk)+2cg .
$$
For $J>0$ this uses $t\ge J$. For $J=0$ use the triangle inequality regardless of the sign of $t$. The remaining even owners have their unique long marker at $v$ on an edge of $H$. They belong to none of the counted outward components. The $ck+2m$ short tiles at $v$ are disjoint from all these charges. Summing over charged odd lifts proves
$$
(N-(c+d)V)/2\ \ge\ \sum_v [m+cg+\max(0,cJ-dk)] .
$$
The same vertices satisfy $\sum_v(2-l)\ge0$ by the degree sum of $H$. This accounts simultaneously for the exterior, physical contact and balanced branches.

## Unit charge at a leaf at 5063

A charged odd leaf of $H$ with $|G_v|=43$ needs at least 215 tiles. The previous lift congruences allow 129 as the only smaller size. Suppose it had 129. Choose the charge-positive normalization (a half-turn on the normalized columns negates every sign, retaining the transformed gate labels). Every outward current is divisible by 22. The one gate toward $H$ consequently has current $43\bmod 22$. The currents sum to 43. This is exactly the single distinguished gate, with signs $(86,43)$, of the [exhaustive endpoint certificate](../../../2026-11-21/semiprimes/global-closure-next/five-block-two-heights/TWO_HEIGHT_EXCLUSION_5063.md#5-the-entire-single-offset-profile-universe). The endpoint tables apply to this odd lift by [localization](../joint-cell-tree/FIVE_BLOCKS.md). A translation places the distinguished residue at zero and the normalized reflection can exchange hands. Neither operation changes the column inequalities. All 9,112,001 profiles fail. This transfer uses only the one-gate congruences, without requiring every outward component to be empty or terminal.

## Finite check

Start from the previously verified bounds 51 and 71. For each odd $V$ tested, the charge totals in the two signs are $(V+1)/2$ and $(V-1)/2$. For both signs, accumulate the maximum of $\sum(2-l)$ with those charge totals and the shared half-excess budget above. The checker enumerates integral $x$, including $x\ge1$ for a unit charge, $x\ge1$ for $k=2$ at 5063, and $x\ge2$ for the unit-charge 5063 leaf. It computes the options by degree and independently by outward current. In the second calculation, setting negative net outward current to zero enlarges the relaxation and gives the same minimum degree for the best allowed option or a smaller one. At fixed nonnegative outward allowance $j$, the least required degree is $\max(1,\lceil(ck-dj)/p\rceil)$, with the unit-charge leaf restriction imposed separately.

| Board | Variation values in descending order | Maximum degree surplus in the relaxation |
|---|---|---|
| 3431 | 51, 49, 47, 45 | −6, −4, −2, 1 |
| 5063 | 71, 69, 67, 65, 63 | −4, −3, −2, −1, 0 |

A negative maximum contradicts the hull degree sum. Passing a row does not give an embedding or a tiling.

## A zero-bank test for both parities

Correct the even charge at the axial marker $C$ by subtracting $d$ and put $e_v=(G_v-d\mathbf1_C)/c$ on even short lifts. Then $\sum e_v=0$. The signed odd tiles with long marker at each even $v$ sum to
$$
d e_v+2c\mathbf1_C-c\mathbf1_T ,
$$
with $T$ the slant marker. Indeed on each far component rooted at odd height the cut identities give $P=O-dE/c+b_S/c$, where $b_S=-(2c^2-d^2)I_C+c^2 I_T$. Summing at $v$ and subtracting its own exterior marker gives the stated formula, including at an empty even lift. Thus $W=\sum|e_v|$ satisfies $n_{\rm even}\ge cW-d$ and $n_{\rm odd}\ge dW-3c$. In particular $W\le56,80$ on the respective boards, since $W$ is even.

On a tree edge take the far side containing its even endpoint. Write $e=(E-d I_C)/c$, $o=O/c$ on that side. Then
$$
P=c e+d(I_C-o),\qquad Q=d e-c(o-2I_C+I_T).
$$
Here $|e|\le W/2<c$ and $|o-I_C|\le(V+1)/2+1<c$. Since $c,d$ are coprime, $Q=0$ forces $e=0$ and $o=2I_C-I_T$, while $P=0$ forces $e=0$ and $o=I_C$. In particular **on any edge off the exterior path, either signed bank vanishes exactly when both corrected branch charges vanish** (use $I_C=I_T$ and the complementary exterior-free component). On the exterior path both banks cannot vanish together. These statements concern signed populations. They leave room for occupied balanced branches with nonempty physical contacts.

Run `python3 branch_reserve.py | diff - BRANCH_STATUS.json` here. On the two exact complete 143 controls, the checker reconstructs both banks, the signed receiving populations at all even and odd markers, and the branch partition. Neither control has tiles in an exterior-free component at a charged odd vertex. The quantitative terminal cost in the new reserve uses the target-specific certificates. [Code](branch_reserve.py) and [recorded calculations](BRANCH_STATUS.json).
