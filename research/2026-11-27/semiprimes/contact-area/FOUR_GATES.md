# A five-region charge bound with the physical native cuts

In the standard vertex-phase frame let an exterior-free gate have **both** far signed parity populations nonzero, E=ce and O=co, and write d=a−b. Let Z be the sum of actual unmatched owners on all occupied exterior-free gates with both far signed totals zero. Every complete tiling must satisfy these bounds on its whole-board unmatched count M.

| N | M−Z | M−Z if also abs(e−o)=1 |
|---|---:|---:|
| 3431 | ≥171 | ≥203 |
| 5063 | ≥213 | ≥229 |

The extra condition in the last column concerns this same mixed gate. A gate with E=O nonzero counts as mixed. All bounds allow intermediate lifts with zero short charge and arbitrary translated branches.

Choose a deepest nonzero short charge in the far subtree. It can be chosen strictly below the far root because both parities occur. Its entering gate has charge cf on its own parity h and zero on the other. The four distinguished edges are the two native edges, the mixed gate and this descendant gate. On the descendant edge the far and near banks have signed counts cf,df. On the mixed edge write i for the parity of its far root, and let s,t be e,o in the order own parity, opposite parity. Its far and near counts are P=cs−dt and Q=ds−ct by the two [cut identities](../../../2026-11-26/semiprimes/joint-cell-tree/TREE.md).

Every neutral bank in Z has zero standard signed count at its short lift, including when two neutral banks lie in different regions. Remove exactly those owners from the accounting; all regional signed sums are unchanged. M−Z remains an upper bound on the absolute signed population in any collection of subtrees, counted on disjoint parity parts. Half-turn pairs cancel at their own short lift.

Start with the residual six-vector for the three native regions from the [physical charged-seam bound](../../../2026-11-26/semiprimes/charge-variation/CHARGED_SEAM.md),
$$D=(-d-E_1-q_1,-c-O_1,E_1-E_2,O_1-O_2-p_1-q_2,E_2-p_2,O_2).$$
The two coordinates of each region are even then odd. In the native region of attachment subtract (ce,co) and subtract Q on parity 1−i, giving D′. The signed remainder of the shell between the two nested gates is
$$R=(ce,co)-P{\bf e}_i-cf{\bf e}_h-df{\bf e}_{1-h}.$$
The innermost region has zero residual after removing its far bank. This partition gives
$$M-Z\ \ge\ m_1+m_2+m_{\rm mixed}+(c+d)|f|+\|D'\|_1+\|R\|_1.$$
Each owner has precisely one long side and pays on only one gate. No intervening or balanced branch is deleted from the tiling.

Use the native slant displacement in each physical chart to bound m₁,m₂. For the mixed gate use |P|+|Q| and the [unit mixed length floors](ONE_DEFECT.md). The [integer replay](four_gates.py) minimizes the resulting expression. Below a ceiling L on M−Z, all component parity charge pairs have absolute sum at most L. Each native bank pair costs at least c by the length of the slant. The mixed gate costs at least min(2(c−d),c+d), by taking sum and difference of the bank characters and using either e=o or e≠o. The descendant costs at least c+d. These independent charges give a finite ceiling for either native inventory, implemented by enumerating physical displacement vectors with the exact native-cut helper. L=235,273 respectively suffice because all four computed lower bounds lie below their ceiling. The minima are in a relaxation, with no assertion of geometric realizability.

```sh
python3 four_gates.py | diff - FOUR_GATES.json
python3 ../../../2026-11-26/semiprimes/joint-cell-tree/controls.py
```

The second replay measures the signed banks and their far populations from both physical 143 boards at every used cut. Neither board has a mixed remote gate, so the numerical mixed-gate conclusion has empty hypotheses there. These inequalities do not supply an upper bound on M in the unrestricted problem.
