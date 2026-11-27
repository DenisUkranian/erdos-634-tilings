# A five-region charge bound with the physical native cuts

In the standard vertex-phase frame let an exterior-free gate have **both** far signed parity populations nonzero, E=ce and O=co, and write d=a−b. Let Z be the sum of actual unmatched owners on all occupied exterior-free gates with both far signed totals zero. Every complete tiling must satisfy these bounds on its whole-board unmatched count M.

| N | M−Z | M−Z if also abs(e−o)=1 |
|---|---:|---:|
| 3431 | ≥173 | ≥203 |
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

Use the native slant displacement in each physical chart to bound m₁,m₂. For the mixed gate use |P|+|Q| and the [unit mixed length floors](ONE_DEFECT.md). The [integer replay](four_gates.py) minimizes the resulting expression. Below a ceiling L on M−Z, all component parity charge pairs have absolute sum at most L. Each native bank pair costs at least c by the length of the slant. The mixed gate costs at least min(2(c−d),c+d), by taking sum and difference of the bank characters and using either e=o or e≠o. The descendant costs at least c+d. These independent charges give a finite ceiling for either native inventory, implemented by enumerating physical displacement vectors with the exact native-cut helper. L=235,273 respectively suffice because all four computed lower bounds lie below their ceiling. For e=o=±1 at 3431, also impose the [proved mixed-gate minimum of 24](SHORT_MIXED.md); without that physical exclusion the first entry is 171. The minima are in a relaxation, with no assertion of geometric realizability.

```sh
python3 four_gates.py | diff - FOUR_GATES.json
python3 ../../../2026-11-26/semiprimes/joint-cell-tree/controls.py
```

The second replay measures the signed banks and their far populations from both physical 143 boards at every used cut. Neither board has a mixed remote gate, so the numerical mixed-gate conclusion has empty hypotheses there. These inequalities do not supply an upper bound on M in the unrestricted problem.

## Counting cancellations outside and inside the four named gates

The inequality also charges excess owners on **nonneutral** gates. Fix the same four edges and put sₖ equal to the sum of absolute net directed counts on the three axes in each bank of native edge k, summed across its two banks. Put Cₑ equal to the maximum of |P|+|Q| and the applicable proved length floor for the chosen mixed gate e. The descendant gate f has net bank cost (c+d)|f|, using f for its signed unit count in this expression.

Define a reserve V by adding the following four quantities:

* On every edge other than the four named gates, sum m−|P|−|Q|, taking both bank signs in the standard frame.
* On each of the two native gates, sum mₖ−sₖ.
* On the mixed gate, take mₑ−Cₑ.
* On the pure descendant gate, take its number of owners minus (c+d)|f|.

Then M−V satisfies the same four-gate minimization as M−Z, including the improved 3431 floor of [173](SHORT_MIXED.md) with the mixed 24-owner minimum included in Cₑ. In particular V includes every owner in Z. All terms are nonnegative. Outside the selected gates remove opposite standard signs in each bank: the two owners have the same short lift, so every regional signed population is preserved. On the native gates cancel only antiparallel pairs on the same heading axis in the same bank. This preserves the exact slant displacement and the character; the reduced inventory still pays at least c there by the physical chord. On the mixed edge retain Cₑ owners and on the pure descendant retain the absolute bank counts. Any removed excess is an even number of opposite signs available within the two banks. These are bookkeeping operations on disjoint owner sets. The actual physical contour is used before any removal to establish its cost. Reapplying the regional proof with the retained counts gives the assertion, including the finite charge cutoffs. The later physical argument about the shape of an equality contour at M−Z uses the actual owners on the distinguished edges and keeps its stated hypothesis.

The [bank check](bank_cancellation.py) independently measures the native sums and retained displacement on both complete 143 boards. Run `python3 bank_cancellation.py | diff - BANK_CANCELLATION.json`.
