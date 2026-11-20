# Boundary population outside a remote phase subtree

20 November 2026. Companion to
[the phase population theorem](../phase-height/PHASE_BRANCHES.md) and
[the no-vacant-ancestor theorem](NO_PHASE_GAPS.md).

For the two target boards, a nonempty exterior-free phase subtree
rooted at physical height at most zero leaves at least 175 or 204
tiles outside it. Section 1 records the earlier perimeter bound.
Section 2 proves the stronger bound by a phase attachment lemma.
All bounds concern arbitrary hypothetical tilings; neither board is
decided here.

## 1. Direct bound

Use the canonical board with outer-edge heights `0,2,0`, and the prime
phase tree whose descendants have increasing physical height. Let `S` be an
exterior-free subtree rooted at height `k<=0`. Its root coset is disjoint
from the valuation ring `A`: every subtree at such a height whose root
contains `A` also contains the outer-edge nodes. Hence every vertex of a
tile whose short node is in `S` is outside `A`.

Every tile having positive-length contact with the outer triangle lies
outside `S`. A tile on a short boundary edge has its short node at that
outer-edge node. If it meets an outer side along its long edge and its
short node were in `S` while its long node were outside, the short node
would have to be the root of `S` and the long node its parent. The outer
edge would then have height `k-1<0`, although all outer edge heights are
0 or 2.

Let `M` be the number of tiles outside `S`. As a union of whole short
nodes including the core, this population has residue `M=j (mod c)`.
It is at least `j+2c`: the core has population at least `j`, and every
outer side has at least one tile long edge on it, requiring an ordinary
short node.

To justify this last assertion, a side with only `r` short tile edges
would receive `r` obtuse tile angles at its edge endpoints. The outer
corners have angles strictly below 120 degrees and cannot receive one.
Each of the `r-1` interior junctions can receive at most one, since two
120-degree angles do not fit in a half-plane. This is impossible.

Suppose `M=j+2c`. The core then has exactly `j` tiles and there is
exactly one occupied ordinary outside node, with `2c` tiles. It has short
height 1: the long edges required on boundary heights 0 and 2 can come
from one common short height only at height 1. Core tiles can expose
only their short edges on the two axial sides.

Let `G` be the core's positive-minus-negative tile count, using the
ordinary alternating direction sign of the project. Nodewise signed
short-edge cancellation gives

\[
  (a-b)G\equiv j\pmod c,
  \qquad G\equiv j\pmod2,
  \qquad |G|\le j.
\]

The two axial sides have positive direction sign. A positive core tile
can therefore expose an `a` edge there, and a negative core tile a `b`
edge. A tile can expose at most one outer edge: the outer angles
`2 alpha`, `2 beta`, and `alpha+beta` are different from every tile angle
`alpha`, `beta`, `120 degrees`. Equality in any potential remaining
case would make `alpha/pi` rational, excluded for these tiles by
`2 cos beta=(2a+b)/c` and the root-of-unity argument. Two sides supported
on different outer side lines would meet at their common triangle
corner and would give one of these forbidden angle equalities.

The total core contribution to the perimeter is consequently at most

\[
  B_0=\frac{(a+b)j+(a-b)G}{2}.
\]

All `2c` ordinary tiles together contribute at most `2c^2`. But the
outer perimeter is exactly
`a(a+2b)+b(2a+b)+c^2=N`. The numerical values are:

| `N` | `j` | `G` | `B_0` | `B_0+2c^2` | Outer perimeter |
|---:|---:|---:|---:|---:|---:|
| 3431 | 27 | 11 | 683 | 3421 | 3431 |
| 5063 | 32 | -22 | 526 | 4224 | 5063 |

Both inequalities fail. Therefore

\[
 M\ge j+3c=
 \begin{cases}138& (N=3431),\\161&(N=5063).\end{cases}
\]

The 3431 argument is already present in the project's high-placement
exclusion; this formulation records its application to every remote
subtree and its 5063 counterpart.

If a finite demand forest of size `R` is entirely inside one such
remote subtree, this outside mass is disjoint from the demanded-node
population. Together with the no-vacant-ancestor theorem, the direct
bound gives `2cR+M<=N`, hence `R<=44` at 3431 and `R<=57` at 5063.
The next sections, together with signed height parity, strengthen
these values to 43 and 56.

## 2. A lower-height attachment outside the subtree

**Attachment lemma.** If `S` is nonempty and its root has physical
height `k<=0`, at least one occupied short node outside `S` has
physical height strictly less than `k`.

Suppose otherwise. Every short node in `S` has height at least `k`
by definition, and every short node outside `S` then has height at
least `k` as well. Section 1 showed that every tile with an outer
boundary interval lies outside `S`. Thus the sets of inside and
outside tiles are both nonempty. The positive-length edge-contact
graph of a finite triangle tiling is connected: a generic path
between two interior tile points can avoid the finitely many tile
vertices and cross only positive-length edge contacts. There is
therefore such a contact between the two sets.

Let `v` be the root of `S`, and let `e` be the common edge node of
the contacting tiles. The local contact lemma in
[No phase gaps, Section 3](NO_PHASE_GAPS.md) applies even at a partial
edge contact. If `e` is inside `S`, the outside tile must have short
node equal to the parent of `v`, of height `k-1`. This contradicts
the supposition. If `e` is outside `S`, the inside tile must have
short node `v` and `e` is its parent, again at height `k-1`.
The outside tile can then only have short height `k`, because all
short heights are at least `k` and an edge height differs from its
tile's short height by at most one.

Extend the contact along its maximal connected collinear run at
height `k-1`. There are no short-height-`k-1` or short-height-`k-2`
tiles anywhere. Every edge on both banks is consequently a long
edge of a short-height-`k` tile. All lengths are `c`. There is no
outer boundary interval on this run: `k-1<0`, whereas the outer
heights are 0 and 2. Its two banks have common endpoints, and their
partitions into equal intervals of length `c` coincide.

The original contacting tiles therefore share a whole long edge,
including its endpoints. Their short heights are both `k`. A shared
endpoint belongs to both short nodes, so the two height-`k` cosets
are identical. The outside tile then has short node `v` and lies
inside `S`, the required contradiction. This proves the lemma.

## 3. The stronger population bound

The attachment lemma supplies an ordinary occupied outside node of
height at most `k-1<=-1`. Independently, the outer side of height 2
has at least one tile long edge, by the obtuse-angle argument in
Section 1. Its tile lies outside `S` and has short height 1 or 3.
Thus there are at least two distinct occupied ordinary nodes outside
`S`: one at negative height and one at height 1 or 3. Neither is
the height-zero core.

Each of these ordinary nodes has at least `2c` tiles, while the core
has at least `j`. Their exact-node populations are disjoint. Hence

\[
 \boxed{M\ge j+4c.}
\]

| `N` | Core lower bound `j` | Ordinary-node contribution | Outside lower bound | Maximum required nodes inside `S` |
|---:|---:|---:|---:|---:|
| 3431 | 27 | 148 | **175** | **43** |
| 5063 | 32 | 172 | **204** | **56** |

For the last column, every required exterior-free ancestor is
occupied by the no-vacant-ancestor theorem. The attachment and
boundary nodes give at least two further occupied ordinary nodes
outside `S`. The [signed parity bound](SIGNED_PHASE_POPULATIONS.md)
limits the total number of occupied ordinary nodes to 45 and 58.
Thus `R+2<=45` or `R+2<=58`, respectively. Equivalently the full
population obeys `2c(R+2)+j+c<=N`: some ordinary node somewhere in
the tiling has a third block, since its odd-height signed total
is `-c`. This extra block is not asserted to lie outside `S`.

The outside lower bound `j+4c` can be used in a weighted or signed
population projection, provided none of its three contributing nodes
is counted a second time.

This proof uses the integral-offset contact lemma, whole-edge matching
at a minimum height, the boundary long-edge requirement, and the
ordinary-node population bound. It requires no restriction on the
Euclidean lattice translates used by the remaining tiles. The
attachment proof also covers an empty root with occupied descendants;
the no-vacant-ancestor theorem is used only when converting demanded
ancestors to the final count of required nodes.

## 4. Explicit conjugate-tree formulation

In the conjugate prime tree, descendants have decreasing physical
height. The corresponding remote hypothesis is an exterior-free
root of physical height `k>=2`.

Every tile with an outer boundary interval again lies outside this
subtree: an inside tile meeting an outside edge node would have to
have its short node at the root and its long node at the parent,
whose physical height is `k+1>2`. The attachment proof reverses
heights. If no outside short node had height greater than `k`, all
short heights would be at most `k`. Any interface through the parent
edge node would then lie on a run at height `k+1` consisting entirely
of length-`c` edges of short-height-`k` tiles. There is no exterior
interval at that height. Whole-edge pairing forces the incident
height-`k` short nodes to agree, a contradiction. An interface through
the root itself already requires an outside parent tile at height
`k+1`.

Thus an outside ordinary node has physical height at least `k+1>=3`.
The long edge required on either outer side of height 0 supplies a
different outside ordinary node of short height `-1` or `1`.
Together with the physical-height-zero core these again give
`M>=j+4c` and, using global signed parity, required-node bounds
43 and 56 inside the subtree.

The applicable root tests are therefore `k<=0` for the increasing
tree and `k>=2` for the decreasing tree. The two trees' population
costs must not be added: their counts refer to the same physical tiles.

