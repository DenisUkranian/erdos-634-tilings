# Independent audit of the one-height 215 cell classification

21 November 2026. Reviewed
[`ONE_HEIGHT_CELL_CLASSIFICATION_5063.md`](../global-strengthening/ONE_HEIGHT_CELL_CLASSIFICATION_5063.md),
SHA-256
`bafea7702e54775454eb17e3957b7737b2773c09b8772e7091ca6debcb8896a5`.
The author and this auditor developed the geometric reductions separately
from the exact profile enumerator.

**Result: PASS.** The native height-one cell is occupied. The complete
215-tile height-one layer has one, two, or four occupied Euclidean
cells with the sign inventories stated in the proof. The 296,521
phase and sign skeletons are an exhaustive containing list; their
geometric feasibility has not been established or excluded.

## Native nodes and the isolated 129-cell

With every odd tile at height one, all even-root child subtrees of a
height-one node have zero odd charge. The native offsets `86` upward
and `-43` downward retain the even-core residue and the appropriate
exterior sides. Neither is divisible by 22, so their parent currents
cannot vanish if their parent exact node were empty. Both native
height-one exact nodes are occupied.

If a `(86,43)` joint cell fills both its exact nodes, summing all its
gate currents gives

\[
43=86 I_{\rm up}-43 I_{\rm down}+22E.
\]

An independent check of the four indicator pairs leaves only `(1,1)`.
The cell is consequently native. The transfer table in Section 2
correctly verifies all hypotheses of the existing 65-certificate
profile exclusion: complete parent populations, integral child
charges, both offsets, zero total charge integers, sign reserves,
single-gate capacities, and the universal endpoint identities.

In particular, the presence of another height-one class causes no
missing descendant odd charge: the cut roots are at heights two or
zero, so their descendants exclude every height-one tile. Endpoint
potentials supported on the selected Euclidean class vanish on other
height-one classes, and each complementary long side of height one
has period-43 displacement. The selected class therefore satisfies
the same endpoint cuts. No deletion of balanced tiles, terminality
claim, or replacement of a whole-node current by a proper-cell
current is used. The isolated 129-cell is rigorously excluded.

## Four-cell matrix and endpoint exclusions

The independently audited two-block balance theorem makes every
86-node balanced. The joint-cell reserve theorem then makes every
cell incident with such a node have charge zero. When both prime
partitions split, their row and column sign totals force

\[
\begin{pmatrix}
(x,x)&(43-x,43-x)\\
(43-x,43-x)&(43+x,x)
\end{pmatrix}.
\]

The `x=0` endpoint contains the previously excluded monochromatic
43-cell. The `x=43` endpoint contains precisely the isolated charged
129-cell just excluded. Thus `1<=x<=42`; all four cells are occupied.
Their native row and native column intersect in an occupied cell.
When either prime partition consists of one node, it is necessarily
native, and its intersection with the other native node is occupied
as well. This covers all one-, two-, and four-cell possibilities.

The charged cell in a four-cell matrix has population from 45 through
127, not automatically 129. Its proper-cell gate currents are not
whole-node currents. The proof correctly leaves this coupling problem
open and does not assert unsigned divisibility for every joint cell.

## Ambient lattice and finite count

The absence of odd heights other than one gives short heights
`0,1,2`. Every occupied increasing-tree node at height zero is its
native exterior-chain node; otherwise its occupied parent would
have height minus one. The decreasing-tree counterpart holds at
height two. Following the actual parent chain through height one
places every tile vertex at valuations `v_pi>=0`, `v_barpi>=-2`.
The existing vertex-lattice theorem supplies integrality away from
these primes. Thus all vertices lie in

\[
I=R+z^2R=(z/c)R.
\]

The ideal equalities agree at both split primes and all other primes.
Since `zR=(z/c)cR`, its quotient in `I` has `c^2=1849` classes,
with the representatives stated in the proof. Equivalently each
prime permits 43 height-one children, with native child label zero.

A split partition chooses one of the other 42 children and which of
its two nodes is balanced. This gives `1` single/single skeleton,
`2*2*42=168` one-split skeletons, and
`4*42^2*42=296352` both-split skeletons including `x`. The total is
296,521 before symmetries. This count fixes phases and sign masses;
it does not enumerate positions or even-height populations.

## Replay record

Ran the author's `verify_one_height_cells.py` independently after the
final ancestry clarification and count were included. It returned
`finite_arithmetic: PASS`, checked all 44 candidate matrices and the
four native-indicator pairs, and recorded precisely the 42 interior
parameters and the skeleton counts above. The prior full 65-certificate
replay and profile enumeration remain the exact inputs to the isolated
129-cell transfer; this small arithmetic replay is not substituted
for them.

Neither 215 nor 5063 is excluded by this classification or audit.
