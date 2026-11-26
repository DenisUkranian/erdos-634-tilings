# At least 175 or 217 unmatched owners in the minimum odd population

A full 3431 tiling with 111 odd tiles requires at least **175** tiles without a whole-long-side half-turn mate. A full 5063 tiling with 215 odd tiles requires at least **217**. If any remote even lift is charged, the two floors rise to **181** and **235**. No upper bound on the unmatched population sufficient to contradict these floors is known.

At 3431 the three odd blocks must be in one lift by [lift divisibility](../joint-cell-tree/TREE.md). This lift must be the middle spine vertex $B$. Otherwise the empty $B$ has zero signed gate current on the axial cut. The path-frame axial formula would require $d\mid 2c$ or $d\mid c$, depending on which side contains the unique odd charge. Both are impossible. At 5063 all 215 odd tiles are already [proved to occupy $B$](../joint-cell-tree/FIVE_BLOCKS.md). Every even short lift must then be adjacent to $B$, since any farther occupied branch would have an empty off-path odd ancestor. Every occupied even neighbor other than the two exterior markers is terminal and exterior-free.

Use standard signs. Write the even charges as $-d+cs$ at the axial marker, $ct$ at the slant marker, and $c h_i$ at the other even neighbors. Then $S=\sum h_i=-s-t$ and $R=\sum |h_i|$. The odd-bank standard currents toward the axial and slant markers are $p=-2c+ds$ and $q=c+dt$, respectively, by the complete gate equations. A remote gate has signed odd current $dh_i$ and signed even current $ch_i$. The four spine counts in high/low order are $(p,-d+cs,ct,q)$. These signed counts follow from the cut characters, including at a neighbor that has paired tiles on other edges. Thus the spine direction-inventory bound of [the three-cut proof](CHARGED_SEAM.md) can be added to $(c+d)R$, using disjoint edges.

For $n_{\rm odd}=kc$, let $u=(k-1)c/2$, $v=(k+1)c/2$ be the positive and negative odd populations. Both $p,q$ lie between $-\lfloor\alpha v+(1-\alpha)u\rfloor$ and $\lfloor\alpha u+(1-\alpha)v\rfloor$ by the ordinary gate certificate. These bounds imply $|s|,|t|<3c$ for both targets. Also $|S|\le R\le kc/d$, $R\equiv S\pmod2$, and
$$
p_++q_++d(R+S)/2\le u,\qquad (-p)_++(-q)_++d(R-S)/2\le v .
$$
Here the subscript denotes positive part. These are reserves of real tiles in disjoint gates.

For 5063 with $R\le1$, apply the [verified periodic endpoint tables](../../../2026-11-21/semiprimes/MINIMAL_ODD_EXCLUSION_5063.md#4-an-exact-dual-inequality-valid-for-every-physical-placement) to the actual population **215**. The per-column inequality is independent of population. In the path frame the two native entries are $-p,-q$; if $R=1$ there is one further entry $-dS$ at one of the 84 nonnative gate labels. The checker scans both hands and all admissible residues, allowing every profile satisfying the translated inequalities. It checks the maximum over shifts for each hand separately, as justified by the invertible pair of residue forms. In particular the two-native profile $(64,-21)$ fails already at 215. A rational periodic witness still survives for $(42,1)$.

If $R=0$, two possibilities need to be distinguished. With every remote even lift physically empty, the [two-native-gate lower bound](../../../2026-11-20/semiprimes/continuation/global-closure/README.md) excludes 111 odd tiles at 3431. At 5063 the [actual-pair certificate](../../../2026-11-21/semiprimes/full-closure-attempt/target5063/README.md) permits only $(20,23)$ in path signs, i.e. $s=3$. For the other profiles a remote terminal is physically occupied. Its cut is separate from the spine and needs at least 16 unmatched owners by the [terminal boundary proof](../terminal-contact/TERMINAL.md). The transfer to one lifted terminal uses the same whole two-bank contour: every outward tile at that terminal is paired, all inward owners have one hand, and all parent owners on the other bank have the complementary hand. These are precisely the inputs of the word and strip exclusion there. This extra cost is added only when $R=0$, so the ledger has not already counted any signed remote owners.

| Total absolute remote even charge in $c$-blocks | 3431, $n_{\rm odd}=111$ | 5063, $n_{\rm odd}=215$ |
|---:|---:|---:|
| 0 | 175 | 217 |
| 1 | 181 | 235 |
| 2 | 233 | 279 |
| 3 | 307 | 323 |
| 4 | Excluded | 409 |
| 5 | Excluded | 495 |
| 6 | Excluded | 581 |
| 7 | Excluded | 677 |
| 8 | Excluded | 773 |

Larger variations are excluded by the same sign and gate reserves. These are lower bounds. The displayed positive entries make no existence claim. Run `python3 minimum_odd.py | diff - MINIMUM_ODD_STATUS.json` with NumPy. The arithmetic and the translated certificate evaluations use integers. [Replay](minimum_odd.py) and [recorded bounds](MINIMUM_ODD_STATUS.json).
