# No vacant ancestor in an exterior-free phase branch

20 November 2026. Continuation of the project's ordered-boundary and
phase-tree arguments, prepared with ChatGPT assistance for the Denis Paliy
research project. This is a necessary theorem for arbitrary tilings of
the two unit F2 boards. Neither board is decided here.

## 1. Statement

Use either primitive tile and its unit F2 target:

| Tile `(a,b,c)` | Tile count `N` | Target side lengths |
|---|---:|---|
| `(33,7,37)` | 3431 | 511, 1369, 1551 |
| `(35,13,43)` | 5063 | 1079, 1849, 2135 |

Put `rho=exp(i*pi/3)`, `z=(a+b rho)/c`, and place the target at

\[
  0,\qquad b(2a+b),\qquad a(a+2b)\rho.
\]

Its two axial sides have direction height 0, and the remaining side
has height 2. A direction of height `h` is `z^h rho^j`; the *short
height* of a tile is the common height of its `a` and `b` edges.
Its `c` edge has height one larger or smaller.

Fix an Eisenstein prime `pi` at which `z` has positive valuation,
and let `A` be its valuation ring. A phase node of height `h` is a
coset of `z^h A`. Its parent is its containing coset of `z^(h-1) A`.
Each tile's three vertices belong to one node at its short height;
call this its short node. Its long edge determines a node adjacent
to its short node. An *exterior-free subtree* contains none of the
three nodes assigned to the outer sides at their direction heights.

**Theorem.** If an exterior-free phase subtree contains a tile at any
short node, its root contains a tile. Consequently every
exterior-free ancestor of an occupied short node is occupied.

This strengthens the earlier phase-tree conclusion, which allowed at
most one vacant exterior-free ancestor. It is a consequence of the
earlier exclusion of every supported pure-mesh cycle, not a new
solution of either whole-board tiling problem.

## 2. Inputs

The [phase-tree population theorem](../phase-height/PHASE_BRANCHES.md)
supplies the node definition, the integral-offset lemma, and the
population statements used in Section 5. The absence of vacant
ancestors itself only needs the node definition and integral offsets.

The [ordered-boundary cycle theorem](pure_cycles/NO_REMOTE_GAPS.md)
excludes a simple polygonal loop in the skeleton of any tiling of
either target whose edges belong to one translate of a triangular
mesh with step length `c`, at any rotation. Its proof permits arbitrary
tile orientations, reflections, and T-junctions. The companion
[rational checker](pure_cycles/check_remote_cycles.py) verifies its
two numerical direction-width and thickness inequalities. The present
note proves the missing passage from an empty phase node to precisely
such a supported cycle.

## 3. Local contact lemma

Consider two tiles meeting along a positive-length interval of edges
at direction height `h`. Their edge nodes at height `h` are the same.
Indeed, on a maximal connected straight run, all endpoints of its
two banks have integral offsets in physical units from one end.
Their displacements are therefore integral multiples of `z^h rho^j`,
which belong to `z^h A`. The corresponding cosets agree. This remains
valid when the contact occupies only part of either edge.

Let `S` be a subtree with root node `v` at height `k`. Suppose one
incident tile has its short node in `S` and the other does not. Let
`e` be their common edge node. A short node equals its edge node for
a short edge, and is adjacent to it in the tree for a long edge.
The tree has a unique edge between `S` and its complement: the edge
from `v` to its parent.

If `e` is outside `S`, the inside tile must have short node `v` and
`e` must be its parent. If `e` is inside `S`, the outside tile must
have short node equal to the parent of `v`, and `e=v`.

Now assume that `v` contains no tile. The first case is impossible.
In the second case the inside tile cannot have short node `v`; it
has a child of `v` as its short node. Thus every interface contact is
between two whole-side types `c`, at common direction height `k`:
the outside short height is `k-1` and the inside short height is
`k+1`.

## 4. From an empty node to a supported simple cycle

Assume for contradiction that an exterior-free root `v` is empty
but that its subtree `S` contains at least one tile. Let `U` be the
union of all tiles whose short nodes belong to `S`. It is a bounded
finite polygonal union with positive area.

### No outer interval belongs to `U`

An outer side has an edge node outside `S`, by the exterior-free
hypothesis. A tile of `U` exposing a short edge there would have the
same short node as that outer edge. A tile of `U` exposing a long
edge there would have to cross the unique parent/root cut, so its
short node would be `v`. The former possibility is outside `S`, and
the latter contradicts emptiness of `v`. Hence `U` has no
positive-length contact with the outer boundary. Contacts at isolated
vertices cause no difficulty.

### All interface edges match whole-to-whole

By Section 3, every positive-length part of the boundary of `U` is a
contact of long edges at height `k`. Extend one such contact to its
maximal connected collinear run of tile edges. The integral-offset
lemma places every edge on that run in the same height-`k` node,
namely `v`. No short-height-`k` edge can occur there, since it would
belong to a tile in `v`. All edge intervals on the two banks thus
have length `c`.

Both banks have the same endpoints. At an interior endpoint a bank
continuing farther would extend the run; at the exterior the convex
target supplies the common endpoint. The run cannot have an outer
side interval on it because that would put an outer-side node in
`S`. The partitions into equal intervals of length `c` consequently
coincide. Each contact contributing to the boundary of `U` is one
entire long edge with one tile on either bank.

In particular no transverse boundary edge or T-junction can occur in
the relative interior of one such interface edge: the two incident
tiles fill a neighborhood of every interior point on their two
sides. The interface is a finite embedded graph with disjoint open
edges, each a vector `c z^k rho^j`.

### A simple cycle exists

Orient interface edges as the boundary of `U`. At every vertex the
number of entering and leaving edges agrees, since it is the
boundary of a finite union of tiles. The graph is nonempty because
`U` is bounded and has positive area. A finite nonempty balanced
directed graph contains a directed cycle; removing repeated vertices
from a closed walk gives a simple cycle. Its embedded polygon has
positive enclosed area. This argument does not assume that `U` is
connected, simply connected, or free of vertex contacts.

Following the cycle from one starting vertex shows that all its
vertices lie in one translate of `c z^k Z[rho]`. It is a supported
simple cycle of the type excluded by the ordered-boundary theorem.
For completeness, the disk it encloses lies in the convex outer
triangle. No open tile interior crosses its boundary, which is in
the tile skeleton, so that disk is itself a union of complete tiles.
This gives the required contradiction and proves the theorem.

Notice that the passage to a supported cycle did not use a
classification of equality at `2c^2`, convexity of `U`, or a replacement
of its tiling. Those additional assertions are unnecessary.

## 5. Strict finite-demand and weighted population bounds

Take any finite set of placements required to occur in a completion.
Let `F` be any finite set of distinct exterior-free ancestors of their
short nodes, including the short nodes themselves when exterior-free.
Each node in `F` has a prescribed tile at or below it. The theorem
forces every node of `F` to be occupied.

The earlier population theorem gives a positive multiple of `c`, at
least `2c`, in each of these nodes. Here a node's population counts
only tiles having **that exact short node**, not the entire population
of its descendant subtree. Populations of distinct nodes are disjoint,
even when one node is an ancestor of another.

The height-zero core node `A` is not exterior-free. Its population is
congruent to `j=N mod c`, with `0<j<c`, so it contributes at least `j`
tiles outside `F`. Consequently

\[
 \boxed{2c|F|+j\le N.}
\]

There is no exceptional empty-node allowance. This replaces the
weaker 47/59 bounds obtained by permitting one empty root.

The [signed population theorem](SIGNED_PHASE_POPULATIONS.md) gives
one further block in the full ordinary population. Its odd-height
signed total is `-c`, so some ordinary node has an odd number of
`c`-blocks and therefore at least three. As the signed core minima
for these two boards equal `j`, the number `R_all` of all occupied
ordinary nodes satisfies `2cR_all+j+c<=N`. Since `|F|<=R_all`,

\[
 \boxed{2c|F|+j+c\le N.}
\]

The extra-block node need not belong to `F`; the upper bound on the
total ordinary-node count also bounds any subset of required nodes.

| Board | `c` | Core residue `j` | Bound from no gaps alone | Bound including signed parity |
|---:|---:|---:|---:|---:|
| 3431 | 37 | 27 | 46 | **45** |
| 5063 | 43 | 32 | 58 | **58** |

More generally, let `s(v)` distinct prescribed tiles have exact short
node `v` in `F`, and put

\[
 L(v)=c\max\{2,\lceil s(v)/c\rceil\}.
\]

If `B` is any independently justified lower bound for the number of
tiles outside all exact nodes in `F`, then

\[
 \boxed{B+\sum_{v\in F} L(v)\le N.}
\]

The default is `B=j`. If `s_0` selected tiles are in the core, it can
be increased to the least number at least `s_0` congruent to `j`
modulo `c`. Counts of other known outside placements or a boundary
argument may give a stronger `B`, provided their populations are not
counted twice. One cannot automatically add two lower bounds on the
same outside set.

For example, in the increasing-physical-height prime tree, if all
demanded nodes lie inside one spatially remote exterior-free subtree
rooted at height at most 0, the attachment argument in
[the boundary budget note](REMOTE_BOUNDARY_BUDGET.md) gives `B>=175`
or `B>=204`. It forces a negative-height ordinary node outside the
subtree, as well as an ordinary node supplying a long edge on the
outer side of height 2. The two nodes are distinct and outside `F`,
so `|F|+2<=R_all`. Together with signed parity, the node limits within
that one subtree are **43 and 56**. The boundary note proves the same
bounds for the conjugate, decreasing-physical-height tree when the
remote root has physical height at least 2.

## 6. Population projection for a solver

For each ordinary node `v` introduce its actual exact-node population
`n_v` and an occupancy indicator `y_v`. Necessary constraints include

\[
 n_v\in c\mathbb Z_{\ge0},\qquad
 2c y_v\le n_v\le N y_v.
\]

If a selected tile has short node `w`, every exterior-free ancestor
`v` of `w` has `y_v=1`. Equivalently, along an ancestor edge whose
parent is exterior-free, child occupancy implies parent occupancy.
The selected tiles at exact node `v` also satisfy `s(v)<=n_v`.
For any finite list of distinct nodes, the sum of their `n_v` and a
valid outside bound is at most `N`.

These are projections of necessary conditions on an arbitrary full
tiling. They do not require that a finite catalogue already contains
every possible completion placement. A failed inequality therefore
excludes the simultaneous selected placements even in the unrestricted
geometric problem. A successful inequality proves no completion.

One may impose the conditions from both conjugate prime trees, using
their respective direction of descent. Their population costs must
not be added as if disjoint: each tile has a node in both trees.

## 7. Reproduction and scope

Run, with Python assertions enabled:

```sh
python3 pure_cycles/check_remote_cycles.py
python3 verify_no_phase_gaps.py
```

The first command checks the exact geometric inequalities used by
the earlier supported-cycle theorem. The second checks the new
integer population bounds. The topological passage and its geometric
hypotheses are proved in Sections 3 and 4, not inferred from those
numerical replays.

The theorem is a necessary restriction on all tilings, including
arbitrary positions and orientations. It supplies neither a complete
3431/5063 construction nor an exhaustive impossibility certificate.

