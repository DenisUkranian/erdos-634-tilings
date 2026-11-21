# The remaining one-height 215 mode has one, two, or four cells

21 November 2026. This is a structural reduction, **not an exclusion
of 215 or of 5063**. Use the path frame with `(a,b,c)=(35,13,43)`,
`z=(a+b rho)/c`, and total odd charge `+43`. Assume that all 215 odd
tiles have short height one. The established height and occupied-parent
arguments then put every tile at short height 0, 1, or 2.

The [two-block balance theorem](TWO_BLOCK_BALANCE_5063.md) shows that
every height-one exact node of size 86 is balanced, including native
nodes. At each prime the height-one partition therefore consists of
either one 215-tile node, or an 86-tile balanced node and a 129-tile
node with sign inventory `(86,43)`.

**Classification.** The native Euclidean height-one class `zR` is
occupied. The complete layer has exactly one of these forms:

| Prime partitions | Occupied joint cells | Cell sign populations |
|---|---:|---|
| `5` and `5` blocks | 1 | `(129,86)`, in `zR` |
| `5` and `2+3` blocks, in either order | 2 | `(43,43)` and `(86,43)` |
| `2+3` and `2+3` blocks | 4 | Matrix (3) below, with integer `1<=x<=42` |

Every joint cell is a positioned Euclidean class, not necessarily a
connected tile union. The native cell in the two- or four-cell cases
need not be the charged cell. No general unsigned divisibility by 43
for an individual joint cell is used.

## 1. Both native exact height-one nodes must be occupied

Consider the unique native height-one node in the increasing prime
tree, and its child containing the upper exterior branch. The full
child subtree has no odd tiles. Its signed parent-bank current is

\[
 Q_{\rm up}=86+22e,\qquad e\in\mathbb Z.             \tag{1}
\]

If the parent exact node were empty, its parent-bank count would be
zero, impossible since 22 does not divide 86. In the decreasing tree,
the corresponding native child has `Q_down=-43+22e`, which also cannot
be zero. Thus both native exact height-one nodes are occupied.

These are the same full-subtree formulas as in
[the odd-charge budget](../large-population/GLOBAL_ODD_BRANCH_BUDGET.md).
The even-core residue and exterior contribution are retained. No
terminality assumption is made.

If either prime partition has a single occupied node, it must be its
native node. Its intersection with the occupied native node of the
other partition is consequently nonempty. That intersection is `zR`.

## 2. An isolated charged 129-cell is necessarily native and impossible

Suppose a joint cell `L` has sign populations `(86,43)` and fills
its entire exact height-one node in both prime trees. Every upward
and downward child gate of these two nodes therefore counts precisely
parent tiles of this one class. All those child subtrees have zero
odd charge.

Let `I_up,I_down` be one when the corresponding parent exact node is
native, and zero otherwise. Summing every upward and downward gate
current counts each class tile once with its sign. Hence

\[
 43=86I_{\rm up}-43I_{\rm down}+22E,
 \qquad E\in\mathbb Z.                              \tag{2}
\]

Among the four possible indicator pairs, divisibility in (2) permits
only `(I_up,I_down)=(1,1)`. Thus `L=zR`.

The earlier 65-certificate profile exclusion applies to this isolated
class even though other height-one classes may be occupied. Here are
all the needed conditions and their reasons:

| Original profile premise | Reason for this class |
|---|---|
| 129 class tiles with signs `(86,43)` | Explicit hypothesis. |
| Both complete parent gate lists refer to these same 129 tiles | The class fills its exact node in each prime tree. |
| Upward currents `86 delta_0+22e`; downward currents `-43 delta_0+22e` | Native nodes from (2), and zero odd charge in every child subtree. |
| Every `e` is integral | Exact signed phase divisibility, including the even core residue. |
| `sum e=0` | The class charge is 43 and the two native offsets sum to 43. |
| Each gate current lies between `-43` and `51` | Negative sign inventory 43 and certified positive gate capacity `(8*86+35*43)/43=51`. |
| Remote `e` lies in `{-1,0,1,2}`; native upward `e` lies in `{-5,-4,-3,-2}` | The preceding integer current bounds. |
| Total positive and negative gate-current reserves are at most 86 and 43 | Every class tile belongs to exactly one hand and one gate of that hand. |
| Every translated and symmetry-transformed endpoint dual inequality holds | Its endpoint potential is supported on this class; other height-one classes contribute zero, whole long edges of height one have period-43 displacement and zero weight, and no exterior side has height one. |

Thus the class induces one of the very same profiles covered by the
verified exhaustive [minimal-mode certificate proof](../../MINIMAL_ODD_EXCLUSION_5063.md).
All those profiles were excluded. This transfer does not use a
terminal even-branch population, a branch-area cost, or absence of
other classes at height one. It uses the complete gate lists and the
class-supported endpoint identities itemized above.

Consequently no such isolated charged 129-cell occurs in the
one-height regime.

## 3. Both split partitions give a one-parameter matrix

Suppose both prime partitions split into 86 and 129. Put the balanced
86-node first in each partition. Every joint cell incident with either
balanced 86-node has zero charge, by the joint-cell reserve theorem.
The sole possible nonzero charge is therefore `+43` in the
129-by-129 intersection.

Writing each cell as `(positive population,negative population)`,
the complete sign matrix must be

\[
 \boxed{
 \begin{pmatrix}
 (x,x)&(43-x,43-x)\\
 (43-x,43-x)&(43+x,x)
 \end{pmatrix}.}                                    \tag{3}
\]

The row and column sums force this form. Nonnegativity gives
`0<=x<=43`. At `x=0`, the charged lower-right cell is a monochromatic
43-cell, excluded by the existing joint line-incidence theorem. At
`x=43`, the off-diagonal cells are empty and the lower-right cell
fills both exact 129-nodes. Section 2 excludes that case. Therefore

\[
 \boxed{1\le x\le42.}                               \tag{4}
\]

All four entries of (3) then have positive population. Since both
native exact nodes are occupied by Section 1, their intersection is
one of these four occupied cells. This proves the native-cell claim
also when both partitions split.

The charged cell in (3) contains between 45 and 127 tiles, with charge
43. Its gate currents are not the full exact-node currents: balanced
cells share both its parent nodes. Section 2 and the original
129-tile exclusion therefore do not apply to it. This is the
remaining coupling problem, rather than an overlooked unsigned
cell-divisibility assertion.

## 4. Finite ambient phase support

The [occupied-parent theorem](../../../../2026-11-20/semiprimes/continuation/charge-transport/flux/SIGNED_CUT_TRANSPORT.md)
also gives a finite phase envelope for these configurations. A
height-zero increasing-tree node must be the unique exterior-chain
node, since an occupied exterior-free height-zero node would force
an occupied parent at absent height -1. Dually every height-two
decreasing-tree node is its unique exterior-chain node.

Every occupied height-one node is therefore a child of the relevant
native even node: an exterior-free node has an occupied parent, and
the native exterior-chain node has the native parent already. Thus
there are at most 43 possible height-one exact nodes in each prime
tree, and at most `43^2=1849` possible joint height-one classes.

In the path coordinates the common vertex ideal is

\[
 I=R+z^2R=(z/c)R.
\]

For completeness this applies to all three short heights, not only
height one. Every occupied height-two node in the increasing tree is
native or has an occupied height-one parent; its height-zero ancestor
is therefore the native node just identified. Dually each occupied
height-zero node in the decreasing tree reaches the native height-two
ancestor, through an occupied height-one parent whenever exterior-free.
Thus every tile vertex has `v_pi>=0` and `v_barpi>=-2`, with
integrality at the other primes supplied by the existing vertex-lattice
theorem.

It has prime exponents `(0,-2)`. The subideal `zR` has exponents
`(1,-1)`, so `I/zR` has exactly `c^2` classes. Complete convenient
representatives are `(z/c)(u+v rho)` with `0<=u,v<43`. This envelope
follows from the actual phase framework; it is not a guessed
denominator cutoff. It supplies finite candidate phases, but does not
assert a geometric realization of any matrix in (3).

## 5. A finite containing list of 296,521 phase and sign skeletons

Label the 43 possible height-one nodes in each prime tree with native
label zero. A split partition chooses one nonnative node among the
other 42 and chooses whether its native node has size 86 or 129.
The complete containing case count before geometric symmetries is:

| Form | Number of phase and sign skeletons |
|---|---:|
| Single node in both trees | `1` |
| One split partition | `2*2*42 = 168` |
| Both partitions split, including the 42 values of `x` | `4*42^2*42 = 296352` |
| Total | **`296521`** |

The first factor two in the middle row chooses the split tree; the
second chooses whether its native node is balanced or charged. In
the last row there are two native-size choices independently in each
tree. The paired prime labels determine a unique Euclidean phase
class in `I/zR`, and (3) fixes every cell's sign populations.

This is a finite exhaustive **containing** list for the stated
one-height mode. It does not assert that the skeletons satisfy the
remaining gate, supporting-line, physical current, area, or packing
conditions. No placements or even-height populations are supplied by
this count, and no exhaustive infeasibility check of these 296,521
skeletons is claimed here.

## Replay and scope

`python3 verify_one_height_cells.py` checks the exact native-indicator
arithmetic and all 44 candidate matrices, retaining precisely the
42 interior integer parameters after the explicitly identified
endpoint exclusions, as well as the finite skeleton count. The mathematical transfer in Section 2 relies
on the already verified 65 certificates and their complete profile
enumeration; this small checker does not substitute for that replay.
The recorded output is
[`ONE_HEIGHT_CELL_CLASSIFICATION_REPLAY.json`](ONE_HEIGHT_CELL_CLASSIFICATION_REPLAY.json).
