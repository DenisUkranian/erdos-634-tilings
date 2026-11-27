# Ordinary lift charge and two specified physical gates

Use the standard vertex-phase coordinates of the [lifted joint-cell tree](../../../2026-11-26/semiprimes/joint-cell-tree/TREE.md). At any ordinary short lift let $n$ be its tile population and $G$ its signed population. Choose any two distinct incident gates. Let $u$ count actual unmatched tiles of this short lift whose long-side gate is outside the chosen pair. The two gates can have either hand, either can be empty, and their bank signs and populations are unrestricted.

| Board | Necessary inequality | Minimum $u$ when $n=3c, \lvert G\rvert=c$ | Minimum population beyond a gate with both far parity charges nonzero |
|---|---|---:|---:|
| 3431 | $n+19u\ge(10/3)\lvert G\rvert$ | 1 | 370 |
| 5063 | $n+29u\ge(39/10)\lvert G\rvert$ | 2 | 516 |

At $u=0, G\ne0$ each inequality is strict. In particular a lift carrying a single signed block on at most two active gates needs at least five blocks. Pairing uses actual coincident opposite long sides. No assumption on the heights elsewhere in the board enters the inequalities.

## Endpoint proof

In the local short chart write $U_j=\rho^j$. A tile with obtuse corner $p$, orientation index $j$, and hand $h=\pm1$ has acute vertices $x=p-aU_j, y=p+bU_{j+h}$. Its sign is $h(-1)^j$. Assign a periodic potential on the residue torus $R/cR$ to each of the three unoriented axes. The short-side score is
$$
h\left(W_j(p)-W_j(x)+W_{j+h}(y)-W_{j+h}(p)\right)
$$
with the axis subscripts read modulo three. The sum of these scores is zero over the lift. Indeed, place each potential only on physical sides with the chosen lifted marker. Opposite subintervals of a contact cancel, including at a T-junction. Endpoint differences telescope along the whole side. A contributing complementary long side has displacement zero modulo $cR$ in this chart. The only possible ordinary exterior side is the slant, with displacement $c^2 U_j$ in its own chart. This also has zero endpoint difference.

The residue of $x=(X,Y)$ selects the long gate by $X-aY/b$ for positive hand and $X-bY/a$ for negative hand modulo $c$. Normalize the first gate to positive hand and label zero. Translation handles its label. Negative conjugation interchanges hands, maps $j$ to $3-j$, and preserves the sign. For equal hands the second label ranges from 1 to $c-1$. Project the torus to the first residue. Endpoints with the same projection have the same score. For opposite hands the two forms are independent over the prime field (their slopes are distinct), so one translation normalizes both labels to zero. Use the full two-dimensional residue torus in that case.

For each choice the [stored integer potentials and weights](TWO_CURRENT.duals) add weight $w_i$ times the sign on gate $i$ to the short-side score. Let $D$ bound the resulting score on each selected single and half the total score of every possible pair. Let $B$ bound the score on every other single. The [checker](two_current.py) enumerates every residue, orientation, and hand. The mate has obtuse corner $x+y-p$, index $j+3$, and the same hand, so paired bank weights cancel. With $L=2D, H=2\max(0,B-D), W=w_1+w_2$, and $S$ the signed count on the selected banks, these tests imply
$$
 W S\le L n+H u .
$$
For equal hands the weights are equal. For opposite hands add the inequality after interchanging the two gates by negative conjugation to the original inequality. This removes any dependence on how $S$ splits between the two banks.

Rotate all local data by a half-turn if necessary to make $G\ge0$. This preserves unmatched counts and permutes the tested labels. As $S\ge G-u$, the direct consequence for each table is $WG\le Ln+(H+W)u$. For the first two columns of the theorem write $\alpha=10/3$ or $39/10$. All tables verify $W>\alpha L$. If $G>u$, use $W(G-u)\le Ln+Hu$ to get $\alpha G<n+(\alpha+H/L)u$. For $G\le u$ the displayed bounds follow directly. The maxima of the rounded overheads are 19 and 29. At $n=3c, G=c$ the integer lower bound is the ceiling of $c(W-3L)/(H+W)$. Minimizing this ceiling over all labels gives 1 and 2. All 80 tables are checked against the full finite set of columns with integer arithmetic.

## Population of a mixed exterior-free branch

Count in blocks of $c$. The [tree theorem](../../../2026-11-26/semiprimes/joint-cell-tree/TREE.md) ensures that every occupied exterior-free branch has an occupied root, every occupied lift there costs at least two blocks, and the local block count has the parity of its signed block count. Every active gate connects toward an occupied component or toward the exterior. On a child edge with empty far population the physical cut identity pairs its entire bank into actual half-turn mates. Consequently a vertex with at most one occupied child uses at most two active gates. A charged vertex of that kind costs at least five blocks by the new inequality and parity. A charged leaf costs at least five blocks at 3431 or seven at 5063 by the one-gate inequalities $n\ge(91/22)\lvert G\rvert$ and $n\ge(83/13)\lvert G\rvert$.

Suppose the entire branch has fewer than 10 or 12 blocks respectively. Any charged lift costs at least three blocks here. A charged two-block lift is monochromatic and the [one-gate capacity](../../../2026-11-26/semiprimes/joint-cell-tree/BRANCHING.md) forces at least six gates, hence five children each costing at least two blocks. Now suppose the signed sum is nonzero on both parities. If a leaf is charged, choose an opposite-parity charged vertex. It either costs five itself, or has at least two children and costs at least three. In the latter case another child subtree disjoint from the chosen leaf costs two more. With the leaf this reaches 10 or 12. If all leaves are balanced, choose two oppositely charged internal vertices. If exactly $r$ of these have at least two children, their joint cost is at least $10-2r$. There are at least $1+r$ distinct leaves, each costing at least two, for a total of at least 12. Both cases contradict the strict budget. This proves the last column of the table.

An independent [rooted-tree calculation](branch_blocks.py) uses block parity, the monochromatic degree bound, the terminal bounds and the two-gate inequality directly on every rooted tree of at most five or six vertices. Its [equality shapes](BRANCH_BLOCKS.json) are candidates in these necessary conditions. For the 5063 mixed gate with exactly 42 owners, the earlier [area ceiling and parity](SHORT_MIXED.md) now leave only 516, 602 and 688 tiles.

## Checks and scope

Run these checks with Python assertions enabled. The coordinate control reconstructs the two complete 143 tilings, groups directed short segments by their actual ordinary lift and axis, and sums endpoint differences at every torus point. It checks the physical mate formula on all 60 pairs of each tiling. It separately verifies the directed long edge and sign of all 48 mixed owner templates against the established triangle coordinate engine.

```sh
python3 two_current.py
python3 branch_blocks.py | diff - BRANCH_BLOCKS.json
python3 endpoint_control.py | diff - ENDPOINT_CONTROL.json
```

The numerical multipliers depend on the two target tile shapes. The existence of a gate with both far parity charges nonzero has not been established for all tilings. The [positioned endpoint exclusion](MIXED_ENDPOINTS.md) uses this hypothesis to bound the whole-board unmatched population. Both original counts remain open.
