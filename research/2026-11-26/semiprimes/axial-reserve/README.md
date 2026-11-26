# Axial wall owners, signed gates and a smaller global phase budget

In any complete target F2 tiling, let $C$ be the lifted short cell carrying the two axial exterior sides. Call every other lifted short cell ordinary; this includes the middle marker $B$ and the slant marker $T$, when occupied. Only actual short tiles contribute to a population. The following bounds allow arbitrary heights, orientations, reflections, translates and T-junctions.

| Necessary condition | 3431 | 5063 |
|---|---:|---:|
| Tiles at the axial lift $C$ | at least 64 | at least 75 |
| Population of some charged ordinary lift | at least 185 | at least 215 |
| Maximum number of occupied ordinary lifts | **42** | **55** |
| Middle population if $B$ is the only charged ordinary lift | at least 333 | at least 387 |

These improve the [previous phase budgets of 45 and 58](../joint-cell-tree/TREE.md). Both original counts remain **OPEN**. In particular the new caps still leave many possible charged configurations.

## 1. Each axial wall spends tiles of specified signs

Use the **standard** frame here. The board has axial walls $0\to A$ and $B_0\rho\to0$, where $A=b(2a+b)$ and $B_0=a(a+2b)$. Their directed headings are $0,4$, both even. Each wall partitions into complete tile sides: a positive-length contact with the supporting line of the convex board places the entire tile side on that wall. A short side on either wall belongs to a tile whose short lift is $C$. The ordinary character $(-1)^j$ of a directed unit segment gives $+\epsilon$ on a tile's CCW length-$a$ side and $-\epsilon$ on its length-$b$ side. Thus each wall $a$ consumes a positive core tile, and each wall $b$ a negative one. No tile can supply two such edges: its shorter sides have opposite directed character. A tile long side on the wall has length $c$.

For $P,Q$ positive and negative tiles at $C$, record $i,j$ wall edges of lengths $a,b$ on each side. For each wall length $L$, require $L-ai-bj\in c\mathbb N_0$. Across the two walls the totals of $i,j$ are at most $P,Q$. The [lifted sign residues](../joint-cell-tree/TREE.md) at the core are $(19,8)\bmod37$ or $(5,27)\bmod43$. They follow from $n_C\equiv N$, $G_C\equiv-d\pmod c$. At 5063 there is no wall inventory with $(P,Q)=(5,27)$, whence $n_C\ge75$.

At 3431 five inventory pairs survive for $(19,8)$. Couple the *order* of the wall edges to a projected period-$c$ endpoint identity. In short coordinates write $u=q-aU_j$, $v=q+bU_{j+h}$ for an obtuse vertex $q$, heading $j$ and hand $h=\pm1$. On each axis the short-edge column is $h$ times the endpoint differences of $u\to q$ and $q\to v$ on their respective axes. Project positions by $\phi(x,y)=x+wy\bmod c$. All long sides on a selected axis have equal projected endpoints. The sum of columns of core tiles is the endpoint difference of the two complete axial sides, sorted by axis. This equality localizes to the actual lift: opposite sides at every positive contact have the same lifted edge marker, including both sides of a split contact. Use an additional row for $P-Q$.

For each wall, after ignoring length-$c$ steps, its successive states are $(i',j')$ from $(0,0)$ to its inventory $(i,j)$. Their residues are those of $p_0+(ai'+bj')U_k$, $k=0,4$. At each next short edge the clockwise choice of obtuse endpoint and the counterclockwise choice give precisely two owner columns; equivalently run over both hands. The owner pays for one directed state transition. Other core tiles use their original columns with no transition. The constant right side of the transition rows is minus one at the start and plus one at the finish. Multiplying these equations by the saved integer table bounds $n_C$ from below. The checker tests the per-tile bound on every unrestricted column and every permitted boundary column. In the inventory order of [the replay](STATUS.json) the five lower bounds are
$$
111/4,\quad317/11,\quad168/6,\quad321/11,\quad29.
$$
All exceed 27, giving $n_C\ge64$. No assumption on the heights of neighboring wall owners enters. At the first remaining core size its two sign counts are also forced: $(19,45)$ at 3431 and $(48,27)$ at 5063 in standard signs. For the other possible allocations $(56,8)$ and $(5,70)$ the same DAG has 25 and 18 inventory pairs. The [second tables](second-wall-tables.json.gz) exclude every one. Six checks at 3431 retain both coordinates modulo $c$ instead of a single projection; the endpoint proof is identical.

## 2. A charged lift can cost five blocks even with balanced branches attached

At an ordinary lift write $G$ for its signed short population. Suppose just one incident gate has nonzero **signed** outgoing population. That gate carries $G$. The other gates may have arbitrarily many physical owners of both signs. The following estimates hold for either height parity:
$$
 n\ge (3810/1002)|G|\quad(3431),\qquad
 n\ge (4304/1001)|G|\quad(5063).
$$
In particular a charged lift of this kind requires at least $5c$ tiles. For unit charge use $n/c\equiv G/c\pmod2$; for larger magnitude the inequalities alone suffice. The earlier [terminal bound](../joint-cell-tree/TREE.md#unit-charge-terminal-cost-at-arbitrary-heights-and-odd-populations) at 5063 remains stronger under its physical single-access hypothesis.

Here are the certificates' conventions. Normalize coordinates within the lift, conjugate and use a half-turn as necessary so the selected hand is negative and its signed population positive. Translate the gate to residue zero. Use $\phi(x,y)=x-ba^{-1}y\bmod c$. This is the normalized gate form for the negative hand since the real coordinate of $(a+b\rho)u$ is $au_x-bu_y$. For negative-hand tiles record the signed populations separately at every gate $\phi(u)$. For positive-hand tiles retain just their total signed population. The projected short endpoint rows have zero source; even at $T$ its full slant has length $c^2$ and returns to its starting residue. These are identities at a single lift. The gate certificate assigns integer weights to these rows so every tile scores at most $D$, including all rotations of both hands at every residue. Its target in the one-nonzero-gate case is the displayed numerator times $|G|$. No tile on another gate is deleted.

For the other use of these tables, adopt the **reflected path frame** for all signed cut equations. Here the total even and odd charges are $d,c$. If $B$ is the only charged ordinary lift, the axial and slant gate currents at $B$ are $2c,-c$, with zero signed current elsewhere. This follows from the [odd-lift gate equation](../charge-variation/README.md); the core carries the entire even charge. Normalize the axial gate to the negative hand preserving the positive sign by combining conjugation with a half-turn if necessary. The two gates have opposite hands. The target of the second projected table gives
$$
 n_B\ge 296555/1002\quad(3431),\qquad n_B\ge372251/1001\quad(5063).
$$
Since $G_B/c=1$, $n_B/c$ is odd. This gives $n_B\ge9c$ on both boards. These bounds concern $B$ alone; they do not assume that it contains all odd tiles.

Finally a nonempty zero-source lift cannot have every positive tile using one gate and every negative tile using an opposite-hand gate on these boards. Normalize both gates to residue zero. Their defining linear forms modulo $c$ are independent (the two eigendirections of the split prime; directly their determinant is nonzero modulo 37 and 43). The full short currents on $(\mathbb Z/c)^2$ vanish separately on all three axes. For a row having only positive or only negative coefficients, every contributing column must have multiplicity zero. For either choice of the positive hand the counts of remaining residue columns are $222,6,0$ or $258,6,0$. This uses actual sign exclusivity on these gates, a stronger input than vanishing signed totals elsewhere.

## 3. A heavy charged vertex in the actual tree

Mark $C,T$ and every charged ordinary lift. Take the smallest subtree containing the marks. If it extends off the exterior path $C,B,T$, any off-path leaf is charged and all directions away from its entering gate have zero signed outgoing count. Each such far component has neither an exterior marker nor any signed charge, so this follows from the complete gate equations. It remains true if there are occupied balanced descendants. Section 2 gives a charged ordinary lift with at least $5c$ tiles. If all charges lie on the exterior path and $T$ is charged, apply the same argument at $T$; all other marks lie toward $B$ and the slant has zero periodic source. Otherwise $B$ is the only charged ordinary lift, and needs at least $9c$ by Section 2.

## 4. Five extra blocks across the ordinary lifts

With $R$ occupied ordinary lifts, the following stronger global population inequality holds on **both** boards:
$$
 N\ge n_C+2cR+5c.
$$
To prove it, write $K=(N-n_C)/c-2R$ for the number of blocks beyond two per occupied ordinary lift. Section 3 gives $K\ge3$. Suppose $K\le4$. There is exactly one heavy charged lift (population at least $5c$). Every leaf of the marked subtree other than $C,T$ is heavy. Thus the subtree has at most three leaves and degree at most three. A monochromatic ordinary lift cannot occur in it: all its tiles use gates in the marked subtree, because every outside direction has zero signed count. Each such gate holds at most $\alpha n$ tiles by the [localized gate capacity](../joint-cell-tree/BRANCHING.md), where $\alpha=43/222$ or $8/43$, and $3\alpha<1$. Every charged lift is marked. In particular all $2c$ lifts are balanced and a charged $3c$ lift has charge of magnitude $c$.

If $K=3$, only the heavy lift has more than $2c$ tiles. The total odd charge forces it to be odd with charge $+c$ in the path frame. Call it $v$. If $v=B$, the $9c$ bound excludes it. Otherwise the axial gate of $B$ has signed count $2c-c\mathbf1_{v\in A_0}$, where $A_0$ is the component containing $C$ after removing $B$. This positive count forces $B$ to be occupied and balanced of size $2c$. It cannot exceed the $c$ positive tiles. Thus $v\in A_0$ and the native counts at $B$ are $c,-c$. All positive tiles must use the axial gate and all negative tiles the slant gate. Section 2 excludes that support.

If $K=4$, an isolated size $6c$ with all others $2c$ is impossible: the sum of the block counts on odd lifts is odd. The only other partition has one size $5c$ and one size $3c$, one of each height parity by the same parity argument. Write $v$ for the odd one, $w$ for the even one. The odd charge is $c$. The even charge is $ec$ for $e=\pm1$. Indeed if $w$ has $3c$ tiles this follows from nonmonochromaticity. If $w$ has $5c$ tiles and there is an off-path mark, then $w$ is the only possible off-path leaf, since it alone is heavy. If all marks are on the exterior path then $w=T$. In either case $w$ has just one nonzero signed gate; Section 2 excludes $|e|\ge2$ at $5c$. The core has corrected even charge $-ec$.

If $v=B$, then $w$ has only one signed outgoing gate and must be heavy, leaving $n_B=3c$. The axial gate at $B$ requires at least $2c-d$ signed positive tiles. This is 48 or 64, strictly above the positive gate capacity $(1+\alpha)c$ of this $(2c,c)$ inventory. If $v\ne B$, the middle vertex has at most $c$ tiles of either sign. Its axial signed count is
$$
 2c+d e(\mathbf1_{w\in A_0}-1)-c\mathbf1_{v\in A_0}.
$$
If $v\notin A_0$ this exceeds $c$. The expression is always positive. If $v,w\in A_0$ then $B$ is occupied with native counts $c,-c$, again impossible. Otherwise $v\in A_0$ and $w\notin A_0$. At $v$ all other marks lie toward $C$, and at $w$ all other marks lie in one direction as well: it is either $T$, or an off-path vertex outside the axial component. Thus both need at least $5c$, exceeding the four extra blocks. This proves the five-block inequality.

## 5. A sixth block is necessary

In fact $N\ge n_C+2cR+6c$. To verify the last step assume $K\le5$. There is again just one heavy charged vertex, and at most one off-path leaf in the marked subtree. Every off-spine charge therefore lies on one simple branch attached to $C$, $B$ or $T$. Every ordinary charged lift is nonmonochromatic by the same degree-three argument. At most three off-path charged vertices are possible: the terminal one spends at least three extra blocks and each further one spends at least one. Suppress all intervening balanced off-path vertices. Each surviving vertex still has a distinct original gate for each adjacent retained direction. The physical heights of the intermediate vertices may increase or decrease.

The [finite census](short_tree.py) allows either parity at each suppressed-path successor. It assigns zero to five extra blocks to each of $B,T$ and the retained vertices, with sum at most five. An empty $B$ or $T$ is relaxed to a balanced two-block capacity at no excess cost. Every off-path retained charge is nonzero. The allowed charge in a size-$nc$ ordinary lift is $gc$ with $|g|<n$ and $g\equiv n\pmod2$. The total odd charge fixes its sum to one in blocks; the corrected even charge at $C$ is fixed by the other even charges, without assuming a core sign profile.

For each direction of a retained ordinary lift let $e,o$ be its far corrected-even and odd charge in blocks, and $I_C,I_T$ its exterior indicators. Its signed outgoing current is $de-co+2cI_C-cI_T$ at odd parity and $do-ce-dI_C$ at even parity, directly from the path-frame equations. Test the two sign budgets, the individual unsigned gate capacities, and the single-gate bound of Section 2. At $B$, if only the axial and slant signed currents are nonzero, use the $9c$ bound for $(2c,-c)$. For $(c,-c)$ a further projected dual of exactly the same form gives $n_B>4c$, hence $n_B\ge6c$ by balance. The replay verifies each dual on every column.

Four relaxed configurations remain at 3431 and two at 5063. Two per board have balanced $B$ of size $4c$ with currents $(2c,-2c)$ or $(2c,-c,-c)$, in axial, slant and possible extra-gate order. All positive tiles use the axial gate. All negative tiles use the slant or the one extra gate. In the two-gate case Section 2 already excludes this. For the three-gate case run the full endpoint support elimination for each of the $2c-2$ extra labels. In every case it removes **all negative columns at the slant gate**, contradicting its required negative current. For three extra-label choices on each board some other columns remain; their removal is unnecessary.

The two further 3431 cases have a four-block ordinary lift with two positive signed currents 48 and 26 and every other gate signed zero. Normalize the 48-gate to the selected negative hand. The 26-gate can occupy any of the 36 nonzero residues of that hand, or the opposite hand. In each of the 37 cases an integer table gives $n>4c$. The [tables](short-tree-duals.json) and [enumeration output](SHORT_TREE.json) reproduce all these exclusions. Consequently the maximum ordinary-lift counts are $\lfloor(3431-64-6\cdot37)/74\rfloor=42$ and $\lfloor(5063-75-6\cdot43)/86\rfloor=55$.

## 6. Remaining population in the positioned A seam

Under the much narrower [charged equality hypothesis](../charged-contour/README.md), the A word leaves 465 or 925 tiles after removing the fixed axial seam owners. Each remaining axial tile is either among $d$ negative singles at the terminal gate or in an axial parallelogram pair. On the full two-dimensional period-$c$ torus the terminal singles have long sides of length $c$ on axial axes, with zero endpoint difference. The residual axial boundary is the source. Translate by $-(t,0)$ so all $d$ axial singles use the zero gate, and translate the source by the same amount.

For each integer table the [checker](seam_population.py) bounds the weight of every possible pair by $2D$ and the weight of each axial single, including a common inventory multiplier, by $D$. It evaluates the actual boundary source at every translation, separately for both hands. At least 135 or 195 of these remaining tiles are axial. Since the terminal count is an odd multiple of $c$ and is at least $5c$ or $7c$, the only remaining terminal populations on word A are $185,259$ at 3431 and $301,387,473,559,645$ at 5063. The [budgets](SEAM_BUDGET.json) are separately reproducible with `python3 seam_population.py | diff - SEAM_BUDGET.json`.

## Replay

Run `python3 reserve.py | diff - STATUS.json` and `python3 short_tree.py | diff - SHORT_TREE.json` with NumPy. [The integer tables](duals.json) are verified on every column by the [checker](reserve.py). The [coordinate controls](control143.py) reconstruct both complete 143 tilings, their edge lifts, every short current, their signed gate totals and the full ordered partitions of both axial walls. The 143-specific phase populations and gate coefficients are not replaced by the target constants. These results strengthen necessary conditions for the F2 boards; the classification reduction and the original existence questions are unchanged.
