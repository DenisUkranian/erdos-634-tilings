# Every two-block height-one node is balanced in the one-height regime

21 November 2026. This is a new necessary condition for a hypothetical
5063 tiling. It does **not** exclude the remaining one-height population
215, nor any larger population. It closes the native monochromatic
two-block loophole in the current structural analysis.

Use the path frame, with `(a,b,c)=(35,13,43)`, `d=22`, total odd
charge `+c`, and tile sign `epsilon=s*(-1)^j`. Assume that all odd
short heights except height one are empty. There is no exterior side
at height one. All cited population and gate statements concern the
complete physical tiling.

**Theorem.** Under these assumptions, an exact height-one node of
either prime tree containing `2c=86` tiles has sign populations
`(43,43)`. The node may be native or exterior-free. Consequently every
joint Euclidean cell inside such a node has charge zero.

The proof uses actual supporting lines as well as the certified
single-class gate capacity. The key additional incidence statement is
the following lemma.

## 1. A monochromatic 86-tile class needs at least three of each hand

**Lemma.** A single Euclidean class of 86 tiles of one sign, at a
short height with zero exterior current on its supporting lines, cannot
contain at most two tiles of either hand.

For the application the height is one, so the exterior hypothesis is
automatic. The class is a positioned set `q+zR`; it need not be a
connected tile union.

Let `r_i` count the distinct short-edge supporting lines in each of
the three unoriented axis families, and let `r=sum r_i`. On a used
line, let `M,L` count the class's length-35 and length-13 short edges.
Since every tile has the same sign, the line current gives

\[
 35M-13L\equiv0\pmod{43},\qquad
 \sum M=\sum L=86.                                      \tag{1}
\]

These are the same per-line congruences as in the
[joint-cell theorem](../../../../2026-11-20/semiprimes/continuation/common-obstruction/joint/JOINT_CELLS.md)
and [terminal-node proof](../../../../2026-11-20/semiprimes/continuation/vertex-phase/TERMINAL_NODE_BALANCE.md).
Other Euclidean classes do not affect (1): whole long edges of this
height have displacement `43 z rho^j` and either both endpoints in
the selected class or neither. Equivalently, apply the line-coordinate
endpoint potential on this class and zero on the other classes.
The short-edge contributions are `35M-13L` up to a common sign,
while the selected long-edge contributions are multiples of 43.
This argument allows separated runs, partial contacts, and T-junctions.
It requires no unsigned population divisibility for a joint cell.

Multiplying the congruence in (1) by the inverse 16 of 35 modulo 43
gives `M+7L=43k` with an integer `k>=1` on every used line. Therefore

\[
 \sum k=\frac{86+7\cdot86}{43}=16,\qquad r\le16.     \tag{2}
\]

Suppose at most `m<=2` tiles have the minority hand. At least 84
have the majority hand. For a fixed hand and sign, a pair of short
supporting lines from different axis families determines at most one
tile. Its obtuse vertex is their intersection, its two side roles are
fixed by the hand, and the two opposite 120-degree sectors have
opposite signs. Thus

\[
 84\le86-m\le r_0r_1+r_1r_2+r_2r_0
             \le\lfloor r^2/3\rfloor.
\]

Together with (2), this forces `r=16`. Each `r_i<=6`: if the largest
family had at least seven lines, the sum of pair products would be at
most `7*9+floor(9^2/4)=83`. The only possible sorted family sizes
with pair-product sum at least 84 are `(4,6,6)` and `(5,5,6)`.

For each line, at most six majority-hand tiles can use it as their
length-35 side, since their other short sides lie in the one axis
family fixed by that hand. The same holds for length-13 sides.
Adding at most two minority tiles gives `0<=M,L<=8`. In that box
the complete nonzero solution set to (1) is

\[
 (M,L)=(1,6)\quad\hbox{or}\quad(8,5).                \tag{3}
\]

The 16 lines and the two totals 86 force exactly six lines of the
first type and ten of the second. Each line with `M=8` needs at
least two minority-hand length-35 edges, because the majority hand
supplies at most six. The ten such lines therefore need at least
20 minority tiles. Each minority tile has only one length-35 edge,
so it contributes to at most one of those lines. This contradicts
`m<=2` and proves the lemma.

## 2. A monochromatic two-block exact node is one Euclidean class

At an ordinary exact node the positive and negative populations are
separately divisible by 43. Thus an 86-tile node has either the
balanced inventory `(43,43)` or one common sign. In the latter case
each nonempty joint cell has positive population divisible by 43,
since its signed population is divisible by 43. A one-block
monochromatic cell is excluded by the existing line-incidence theorem.
The full node must therefore be a single 86-tile Euclidean class.

Its one-sign parent-bank count at any selected child gate is at most

\[
 \frac{8\cdot86}{43}=16,                             \tag{4}
\]

by the [single-class gate theorem](../../../../2026-11-20/semiprimes/continuation/global-closure/median/NATIVE_GATE_CAPACITY.md),
in either hand and for either sign. No opposite-sign half-turn pairs
occur in this node: the mate of one of its long sides has the same
short Euclidean class and opposite sign. Thus the signed gate counts
enumerate every actual parent tile of the corresponding hand, without
a hidden balanced-pair reserve.

## 3. Exact child-gate residues force at most two minority tiles

There are no odd tiles strictly beyond height one in either direction.
Hence every child subtree of a height-one node has zero odd charge.
The full-subtree signed transport identities give these parent-bank
currents:

\[
 \begin{aligned}
 Q_{\rm up}(g)&=86\,\delta_{\rm native}(g)+22e_g,\\
 Q_{\rm down}(g)&=-43\,\delta_{\rm native}(g)+22e_g,
 \qquad e_g\in\mathbb Z.                             \tag{5}
 \end{aligned}
\]

Here the first line concerns children in the increasing-height tree,
the second children in the decreasing-height tree. The indicator is
one only at the unique child containing the corresponding exterior
branch, when the parent is its native height-one node. It is zero at
every child of an exterior-free node. These are whole-subtree
identities, with the even core residue and exterior terms retained;
they do not presume terminal even nodes. See the derivation in
[the unrestricted odd-charge budget](../large-population/GLOBAL_ODD_BRANCH_BUDGET.md).

If the parent has common sign `sigma`, (4) says
`0<=sigma*Q(g)<=16`. Every nonnative gate in (5) therefore has
`Q(g)=0`. At a native gate the possibilities are:

| Prime tree | Common sign | Native current allowed by (4)--(5) | Number of outward-hand tiles |
|---|---:|---:|---:|
| Increasing | `+` | none (`86 mod 22 = 20`) | impossible |
| Increasing | `-` | `-2` | 2 |
| Decreasing | `+` | `1` | 1 |
| Decreasing | `-` | none (`-43 mod 22 = 1`) | impossible |

For an exterior-free node all its outward-hand counts are zero.
For a native node the only arithmetically surviving cases have one
or two outward-hand tiles. The other 84 or 85 tiles have the opposite
hand. Every case contradicts the lemma in Section 1. Hence the exact
node cannot be monochromatic and has inventory `(43,43)`.

Finally the established joint-cell reserve theorem says that a
balanced 86-tile exact node has zero charge in every cell: a nonzero
unit cell charge would exhaust one entire 43-sign bank and form an
excluded monochromatic one-block cell. This proves the stated
consequence.

## 4. Consequences for the remaining 215-tile layer

If the one-height case has 215 odd tiles, every prime partition is
either a single 215-tile node, or nodes of sizes 86 and 129. In a split
partition the 86-node is now always balanced, and the 129-node has
sign inventory `(86,43)` and charge `+43`.

If both prime partitions split, the only nonzero cell charge lies at
the intersection of their 129-nodes. Its population is not thereby
proved to be 129. Zero-charge cells can share either 129-node, and
general unsigned cell divisibility remains unproved. If one partition
has a single node, that node can likewise share several cells. Thus
this theorem alone does not transfer the earlier 129-tile endpoint
certificate to a charged subcell and does not exclude 215.

## Replay and proof scope

Run `python3 verify_two_block_balance.py`. The standard-library
checker verifies the line congruence and its line-count bound, the complete family-size
and small line-pair enumerations, the forced ten high-demand lines,
and the native and remote gate residue possibilities. Its output is
[`TWO_BLOCK_BALANCE_REPLAY.json`](TWO_BLOCK_BALANCE_REPLAY.json).
The actual-line current, rigid intersection, phase divisibility, and
gate-capacity steps are mathematical hypotheses proved in the cited
project notes; this small replay does not replace those geometric
arguments or enumerate tilings.
