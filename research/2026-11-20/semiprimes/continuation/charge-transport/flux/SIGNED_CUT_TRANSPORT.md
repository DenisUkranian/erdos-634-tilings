# Exact signed transport across physical phase cuts

20 November 2026. These are necessary identities and population bounds
for complete tilings with arbitrary permitted orientations, reflections,
positions, and partial edge contacts. The bidirectional-gate strengthening
uses the supported pure-cycle exclusion for the 3431 and 5063 targets.
Neither target is decided here.

The relevant inputs are the phase-node and integral-offset statements,
the signed population theorem, and the supported-cycle theorem in the
project's `vertex-phase` package. The existing `common-obstruction`
package treats unmatched edges and closed child gates. The present note
records the exact signed transport, including exterior terms, and proves
that a nonempty exterior-free cut has unmatched tiles in both directions.

## 1. Signs, nodes, and physical long edges

Put `d=a-b`, `rho=exp(i*pi/3)`, and `z=(a+b*rho)/c`. The canonical
board has vertices

\[
 0,\quad X=b(2a+b),\quad Y=a(a+2b)\rho.
\]

Write `A=b(2a+b)` and `B=a(a+2b)`, so `X=A`, `Y=B*rho`, and
`AB=abN`.

Its two axial sides have height 0; the remaining side has height 2.
For a CCW tile `T=(q,h,j,s)`, write `epsilon(T)=s*(-1)^j`.
The ordinary and alternating characters of a directed length-`L`
segment with heading `z^r rho^j` are `L*(-1)^j` and
`L*(-1)^(r+j)`. On a tile, its short sides contribute `d*epsilon`
to the first character, its long side contributes `-c*epsilon`, and

\[
 C(T)=(d-c)\epsilon(T),\qquad
 C_*(T)=(d+c)(-1)^h\epsilon(T).                         \tag{1}
\]

Fix either prime tree. Write `s(T)` for the tile's short node and
`l(T)` for its long-edge node. These are adjacent nodes. Physical
heights increase toward children in one tree and decrease in the
other; their parity changes across an edge in both cases.

A tile is **unmatched** if its full long side does not have the
actual half-turn mate in the complete tiling. A half-turn pair has
opposite signs, the same short node, and the same long-edge node.
Removing such pairs therefore preserves every signed count used below.
An absent catalogue entry is not evidence of an unmatched physical edge.

## 2. The exact node equation

For any node `v` define

\[
 G_v=\sum_{s(T)=v}\epsilon(T),\qquad
 H_v=\sum_{l(T)=v}\epsilon(T).
\]

Let `b_v` be the ordinary character of the outer sides whose edge
node is `v`. Nodewise cancellation of directed intervals gives

\[
 \boxed{dG_v-cH_v=b_v.}                                 \tag{2}
\]

The short sides at `v` contribute `dG_v`; all other sides at `v`
are complete long sides and contribute `-cH_v`. The integral-offset
lemma justifies cancellation separately in the phase node even when
the contacts are partial. This equation is an equality, not merely
the previously used congruence modulo `c`.

The only nonzero exterior contributions in the canonical frame are

\[
 b_{\rm core}=b(2a+b)+a(a+2b),\qquad b_{\rm outer\;2}=-c^2.
\tag{3}
\]

The alternating exterior character has the same values because all
outer heights are even. Summing (2) and its height-parity counterpart
recovers `G_odd=-c` and `G_even=-d`.

## 3. The cut chain, with exterior terms retained

Let `v` be a node of physical height `k`, `p` its parent, and `S`
the subtree rooted at `v`. Let `U_S` be the union of tiles whose
short nodes belong to `S`, and put

\[
 G_S=\sum_{s(T)\in S}\epsilon(T),\qquad
 G_{*,S}=\sum_{s(T)\in S}(-1)^{h(T)}\epsilon(T).
\]

There are two crossing populations:

\[
 P_e=\sum_{s(T)=v,\ l(T)=p}\epsilon(T),\qquad
 Q_e=\sum_{s(T)=p,\ l(T)=v}\epsilon(T).                 \tag{4}
\]

Here `e` is the parent/child edge. `P_e` counts signs of root tiles
whose long edge points toward the parent; `Q_e` counts signs of parent
tiles whose long edge points toward the root. These are signed tile
counts, not lengths of unmatched portions of partially covered edges.

Let `Gamma_S` be the sum of the complete CCW outer sides whose edge
nodes lie in `S`. It is not generally the part of the outer boundary
actually exposed by `U_S`. If `A_e` and `B_e` are the whole CCW long-
edge chains from the two tile classes in (4), nodewise cancellation
gives the exact geometric-chain identity

\[
 \partial U_S-\Gamma_S=A_e-B_e.                         \tag{5}
\]

Every term on the right is a whole side of an actual tile. Formula
(5) permits cancellation of overlapping subsegments and does not
assume whole-to-whole matching of the interface.

Write `b(S)=C(Gamma_S)=C_*(Gamma_S)`. Explicitly,

\[
 b(S)=[b(2a+b)+a(a+2b)]\delta_0-c^2\delta_2,            \tag{6}
\]

where `delta_0` indicates that the height-zero core edge node lies
in `S`, and `delta_2` indicates the outer height-two edge node.
The two axial sides have the same core node and enter together.

Applying the characters to (5) proves

\[
 \boxed{c(P_e-Q_e)=(c-d)G_S+b(S),}                       \tag{7}
\]
\[
 \boxed{c(-1)^k(P_e+Q_e)=(c+d)G_{*,S}-b(S).}             \tag{8}
\]

For (8), the root-to-parent long edges have parity opposite to `k`,
whereas parent-to-root long edges have parity `k` and enter (5) with
a minus sign. Both terms consequently have coefficient `c*(-1)^k`.
The formulas are unchanged in the conjugate tree when `k` remains
the physical height.

Equations (6)–(8) explicitly include exterior-containing cuts. Dropping
`b(S)` at the distinguished height-one node would create a false
obstruction: its subtree contains the outer height-two edge node.

### The same cut also preserves physical displacement and area

For a directed segment from axial coordinates `u` to `w`, write
`Vec(u,w)=w-u` and `Det(u,w)=det(u,w)`. Extend both operations
additively to chains. Subdivision on a supporting line preserves
both values, so (5) also gives the exact identities

\[
 \boxed{\operatorname{Vec}(A_e)-\operatorname{Vec}(B_e)
       =-\operatorname{Vec}(\Gamma_S),}                 \tag{8a}
\]
\[
 \boxed{ab\,n_S=\operatorname{Det}(\Gamma_S)
       +\operatorname{Det}(A_e)-\operatorname{Det}(B_e).}\tag{8b}
\]

Here `n_S` is the actual number of selected tiles. A positive tile
has axial determinant sum `ab`; rotations and reflections, with
counterclockwise orientation restored, preserve this sum. In the
canonical frame, the two axial outer sides have determinant zero,
and the height-two side has determinant `AB=abN`. Thus the exterior
term in (8b) is `abN*delta_2`.

Whole long-edge half-turn pairs cancel in (8a) and (8b), as they do
in the characters. These equalities retain the actual coordinates
of the contacts. They do not follow from a list of scalar signed
populations alone; a formal scalar solution is not a certificate
that these geometric constraints can be realized.

## 4. Actual unmatched crossing populations and global transport cost

Let `u_e^P,u_e^Q` count actual unmatched tiles in the two classes (4).
Half-turn pairs cancel separately within those classes. Therefore

\[
 u_e^P\ge|P_e|,\quad u_e^Q\ge|Q_e|,\qquad
 u_e^P\equiv P_e\pmod2,\quad u_e^Q\equiv Q_e\pmod2.
\tag{9}
\]

The cut cost is

\[
 E_e=|P_e|+|Q_e|
 =\max\left\{
 \left|\frac{(c-d)G_S+b(S)}c\right|,
 \left|\frac{(c+d)G_{*,S}-b(S)}c\right|
 \right\}.                                             \tag{10}
\]

For any collection of distinct edges of one prime tree,

\[
 \boxed{\sum_e E_e\le U_{\rm all}\le N,}                 \tag{11}
\]

where `U_all` is the number of actual unmatched tiles. This sum does
not double-count tiles: every tile has exactly one short-node to
long-node transition and belongs to exactly one parent/child edge
in the chosen tree. Summing over both prime trees would count every
tile twice and is not permitted.

### Reading the transport on the physical contact

For an exterior-free cut, the two alphabets in (5) have different
heights. After interval cancellation, `A_e` is precisely the part of
`partial U_S` at the parent height, and `-B_e` is precisely its part
at the root height. Let `f_T` be the fraction of a crossing tile's
long side that survives on this physical boundary. For the `P`
class this includes any exposed outer-board interval; for the `Q`
class it is contact of an outside parent tile with `U_S`. Then
`0<=f_T<=1`, and character cancellation on internal intervals gives

\[
 P_e=\sum_{T\in P}\epsilon(T)f_T,\qquad
 Q_e=\sum_{T\in Q}\epsilon(T)f_T.                       \tag{11a}
\]

Here is the bank argument without an assumption of whole-side
matching. At a generic point of a `P` long side, its edge node is
the parent `p`. If the opposite tile also belongs to `U_S`, that
tile cannot have short node `p`, which lies outside `S`. Its edge
there must be a long side, and its short node must be the root `v`:
no other node of `S` is adjacent to `p`. Thus the opposite tile is
also in the `P` class. Their CCW characters cancel pointwise on
the shared interval, including when it covers only part of either
long side. Removing all such internal intervals leaves exactly
the exposed fractions used in the first equality of (11a).

For a `Q` long side, the edge node is `v`. If its opposite tile
also lies outside `U_S`, it cannot have short node `v` or a child
of `v`; those nodes belong to `S`. The only remaining adjacent
short node is `p`, so this opposite tile also belongs to `Q`.
Their internally covered fractions cancel by the same argument.
Because the cut is exterior-free, a whole `Q` edge cannot supply
an outer interval whose edge node is `v`. All surviving fractions
therefore contact `U_S`. This proves the second equality. Endpoints
and isolated junctions have zero length and do not affect either
calculation.

A tile with `f_T>0` cannot have its full half-turn mate: that mate
has the same short node and would put both banks on the same side
of the selected union. Thus the absolute-value bounds also count
genuine boundary-carrying unmatched tiles, not just formal node
transitions. In addition,

\[
 \operatorname{Perimeter}(U_S)/c
   =\sum_{T\in P\cup Q}f_T\ge E_e.                     \tag{11b}
\]

The perimeter includes every component and hole boundary. Individual
long sides may be only partly exposed. The parity statements in (9)
apply to the complete unmatched crossing classes, not to arbitrary
subsets of boundary-carrying tiles. The positive zero-flow correction
below is a tile-count bound; it is not a lower bound of two full
edge lengths when the surviving fractions are small.

For an exterior-free cut, `b(S)=0`; all selected exact nodes are
ordinary. Hence `G_S=c*g_S` and `G_{*,S}=c*g_{*,S}`, with integers
of the same parity as the subtree population in `c`-blocks. Thus

\[
 P_e-Q_e=(c-d)g_S,\qquad
 P_e+Q_e=(c+d)(-1)^k g_{*,S},
\]
\[
 E_e=\max\{(c-d)|g_S|,(c+d)|g_{*,S}|\}.                \tag{12}
\]

An odd number of population blocks forces `g_{*,S}` odd. Such a cut
therefore has at least `c+d` unmatched crossing tiles: **63 at 3431**
and **65 at 5063**. This counts tiles on both sides of the cut.
It does not place all of them in the subtree or give the same bound
for an arbitrary finite selection of columns.

For a terminal exterior-free node with `G_v=cg`, equations (7)–(8)
specialize to

\[
 P_e=cg,\qquad Q_e=dg.                                  \tag{13}
\]

Thus a charged terminal node forces actual signed transport from its
immediate parent, not only unmatched sides belonging to the node.

## 5. Both directions are active at every nonempty exterior-free cut

This strengthening uses the supported pure-`c`-cycle exclusion for
the two target boards.

**Bidirectional-cut theorem.** If `S` is exterior-free and contains
at least one tile, then

\[
 \boxed{u_e^P>0\quad\hbox{and}\quad u_e^Q>0.}             \tag{14}
\]

For an exterior-free cut, (5) reads `partial U_S=A_e-B_e`.
The two chains use single, consecutive physical heights: `A_e`
has the parent height and `B_e` the root height. If every tile of
one class had its half-turn mate, that whole chain would cancel
pairwise, because the mate remains in the same exact short node
and crosses the same cut in the same direction. The remaining
boundary would be a whole-`c` chain at one height.

Its signed area is the positive area of `U_S`. A balanced whole-edge
chain of nonzero area contains a supported simple pure-`c`-mesh
cycle, by the same endpoint-component argument as in the published
no-gap proof. That cycle is excluded in both target boards.
Neither crossing class can therefore be fully paired, proving (14).

In particular, **both the root and its immediate parent are occupied**.
The parent conclusion still holds when that parent contains exterior
nodes. It is stronger than merely finding some lower-height tile
outside a remote branch.

Combining (9) and (14), define

\[
 f(t)=\begin{cases}|t|,&t\ne0,\\2,&t=0.\end{cases}
\]

At every active exterior-free cut,

\[
 u_e^P+u_e^Q\ge f(P_e)+f(Q_e).                            \tag{15}
\]

In particular a subtree with `g_S=g_{*,S}=0` has `P_e=Q_e=0`
but still requires **at least four unmatched crossing tiles**, two
on each side. Each side then supplies at least one tile of each sign.
This is stronger than a zero scalar-current cost.

This conclusion also holds for boundary-carrying crossing tiles:
each of the two surviving chains is nonzero, whereas (11a) has
zero signed weighted sum. Both signs must therefore occur with
positive surviving fractions in that class.

For a finite collection of edges, replace `E_e` in (11) by
`f(P_e)+f(Q_e)` at its nonempty exterior-free cuts, leaving the
ordinary value elsewhere. The resulting sum still counts each
actual unmatched tile at most once.

## 6. Per-node signed rounding strengthens the population projection

At a node `v`, each incident tree edge has one signed outgoing tile
count `t_{v,e}`: it is `P_e` if `v` is the child and `Q_e` if `v`
is the parent. Take any finite set of incident edges. Put

\[
 R_v^+=\sum_e\max(t_{v,e},0)+Z_v,\qquad
 R_v^-=\sum_e\max(-t_{v,e},0)+Z_v,                        \tag{16}
\]

where `Z_v` counts the selected active exterior-free cuts for which
this node's signed outgoing count is zero. At each such zero-flow
cut, (14) requires at least one unmatched tile of each sign.
The tile classes at different incident edges are disjoint, so

\[
 n_v^+\ge R_v^+,\qquad n_v^-\ge R_v^-.
\]

At an ordinary node, signed divisibility upgrades these to

\[
 n_v^+\ge c\lceil R_v^+/c\rceil,\qquad
 n_v^-\ge c\lceil R_v^-/c\rceil.                         \tag{17}
\]

Retain the separate `n_v>=2c` lower bound when occupancy is required.
For the core, replace each right side by the least integer at least
`R_v^+` or `R_v^-` in its prescribed residue class `r_+` or `r_-`.
Summing the resulting bounds over distinct exact nodes, plus any
separately justified outside population, gives a valid lower bound
for `N`.

For example, a balanced node serving more than `c` distinct active
zero-flow child cuts requires more than `c` unmatched tiles of each
sign, hence at least `4c` tiles after rounding. This inference uses
actual cuts and their full-tiling signed counts. Unknown completion
tiles can change the charge of a partially enumerated subtree;
selected-catalogue charge must not be substituted for `G_S`.

## 7. Complete 143 control and the exterior-spine limitation

`verify_flux.py` checks every realized tree edge of the previously
verified complete 143 tiling, in both prime trees. It verifies (2),
(7)–(10), the displacement and area identities (8a)–(8b), matching
parity, and exact long-edge mates. The full tiling
has 60 half-turn pairs and **23 unmatched tiles**.

In the increasing tree its only nonzero cuts are:

| Physical root height | Subtree population | `G_S` | `G_{*,S}` | `b(S)` | `P_e` | `Q_e` |
|---:|---:|---:|---:|---:|---:|---:|
| 1, distinguished | 105 | -7 | 7 | -49 | -14 | -2 |
| 2, outer-edge node | 0 | 0 | 0 | -49 | 0 | 7 |

The transport costs sum to `14+2+7=23=3c+d`, exactly the actual
unmatched count. The conjugate tree gives the same equality.
The exterior terms are necessary, including at the empty node
containing the outer height-two side.

The scalar spine pattern generalizes formally to

`core -> height1: -d`, `height1 -> core: -2c`,
`height1 -> outer-height2: +c`.

It carries the whole `G_odd=-c` and has total cost `3c+d`, namely
137 and 151 at the two targets. This is not a minimum of the scalar
relaxation. For example, the formal assignment

\[
 G_0=c-d,\quad G_1=-c,\quad G_2=-c,
\]

with signed transitions

\[
 H_{0\to1}=c-d,\quad H_{2\to1}=-c,\quad
 H_{1\to2}=c-d,\quad H_{1\to0}=-(2c-d)
\]

satisfies the scalar node equations and has cost `5c-3d`, namely
107 and 149. No placement, physical area certificate, or complete
axis-current check is asserted for that lower-cost assignment.

The scalar signed identities and population rounding alone do not
exclude the original
`3c+d` pattern. Even assigning `9c` tiles to the distinguished
height-one node, with `4c` positive and `5c` negative, leaves
nonnegative core populations with the correct residues at both
targets. Additional tiles may be represented algebraically by
balanced pairs. This is only a formal population/transport pattern,
not a placement or completion certificate.

The previously proved two-height exclusion uses additional geometric
information and does not apply automatically to a three-height
formal spine. The abstract axis-flow model in `../joint` likewise
has no occupied exterior-free nodes; the new active-cut and charged-
leaf costs do not apply to it. Neither model is a positive tiling.
No new unrestricted geometric correction exceeding the 3431/5063
population or the 45/58 node budget is proved here.

The companion `CHARGED_PARENT_TRADEOFF.md` applies per-node rounding
to actual charged terminal branches and their parents. Its costs
are genuine necessary conditions, but remain well below `N`.

The saved balanced-strip controls separately check `P_e=Q_e=0`
with actual crossing unmatched counts `2` on the inside and `2a`
on the parent side. They illustrate why zero signed flux need not
mean no physical contact. Those controls remain partial F2 packings;
the new bidirectional theorem is asserted for the two target boards,
not universally for all shapes such as the 143 control.

## Reproduction

```sh
python3 verify_flux.py --out FLUX_REPLAY.json
```

The script locates the existing exact geometry, phase arithmetic,
complete 143 certificate, and mixed-cycle controls. Explicit
`--continuation` and `--patch-dir` arguments may be supplied if the
files are installed elsewhere. It performs exact integer and
rational phase/count checks and no search for a tiling.
