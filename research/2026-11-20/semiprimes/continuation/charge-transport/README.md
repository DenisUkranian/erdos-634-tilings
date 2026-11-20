# Odd charge, physical contacts, and population costs

20 November 2026. Denis Paliy research project, with ChatGPT assistance.

**3431 and 5063 remain OPEN.** This continuation connects the compulsory
odd-height signed population to actual boundaries of phase-selected tile
unions. It proves transport identities, a positive cost for balanced
contacts, and a conditional description of the smallest odd population.
It also gives an exact abstract countermodel to the currently retained
population and axis-flow conditions. None of these results is an
unrestricted nonexistence certificate or a target tiling.

| Count | Tile `(a,b,c)` | `d=a-b` | Available ordinary nodes in either prime tree |
|---:|---|---:|---:|
| 3431 | `(33,7,37)` | 26 | 45 |
| 5063 | `(35,13,43)` | 22 | 58 |

The standard frame has outer vertices `0,A,H*rho`, where
`A=b(2a+b)`, `H=a(a+2b)`, `rho=exp(i*pi/3)`, and
`z=(a+b*rho)/c`. The two characters give

\[
G_{\rm odd}=-c,\qquad G_{\rm even}=-d.
\]

We retain arbitrary permitted orientations, reflections, translations,
and partial side contacts. The phase populations and pure-cycle
exclusion used below are proved in the
[vertex-phase package](../vertex-phase/README.md); joint cells and
local controls are in the
[common-obstruction package](../common-obstruction/README.md).

## 1. An exact identity on the actual contact boundary

Fix one prime tree, an edge from a parent to a root of physical height
`k`, and the full descendant subtree `S`. Select all tiles whose short
nodes lie in `S`, and let `U_S` be their union. Let `P` be the signed
number of root tiles whose long-edge node is the parent; let `Q` be
the signed number of parent tiles whose long-edge node is the root.

Write `G` and `G_*` for the ordinary and height-alternating signed
populations of the entire subtree. Let `b(S)` be the ordinary exterior
character contributed by the **whole** outer sides whose edge nodes
belong to `S`. It is not merely the exposed part of `U_S`. Then

\[
\boxed{c(P-Q)=(c-d)G+b(S),}
\]
\[
\boxed{c(-1)^k(P+Q)=(c+d)G_*-b(S).}
\]

The proof starts from an equality of geometric segment chains,
`boundary(U_S)-Gamma_S=A_e-B_e`, where the two right-hand chains
consist of complete long sides of actual crossing tiles. It therefore
accounts for partial contacts and does not infer a boundary from a
finite placement catalogue. The same chain gives exact displacement
and position-dependent area identities.

For an exterior-free subtree, `b(S)=0`, `G=cg`, and `G_*=cg_*`.
After cancellation, the two surviving boundary alphabets are at
consecutive heights. If `f_T` is the fraction of a crossing tile's
long side which lies on this real boundary, then

\[
P=\sum_{T\in P}\epsilon_T f_T,\qquad
Q=\sum_{T\in Q}\epsilon_T f_T,\qquad 0\le f_T\le1.
\]

Consequently the number of boundary-carrying unmatched tiles is at least

\[
E(S)=|P|+|Q|
 =\max\{(c-d)|g|,(c+d)|g_*|\},
\]

and `Perimeter(U_S)>=c*E(S)`. An odd number of population blocks in
the subtree forces `g_*` odd, giving at least **63** crossing tiles
at 3431 and **65** at 5063. These counts include tiles on both banks;
they are not all assigned to the selected region.

[Complete proof, exterior terms, and exact controls](flux/SIGNED_CUT_TRANSPORT.md).

## 2. A balanced contact still has a positive cost

On either target, a nonempty exterior-free cut must have actual
unmatched crossing tiles in **both** directions. Otherwise the
remaining boundary would be a supported pure-height whole-`c` cycle,
which the target geometric theorem excludes. Thus the exact root and
its immediate parent must both contain tiles.

If one directional signed flow is zero, its nonempty boundary chain
needs both signs. If `g=g_*=0`, there must be at least **four**
boundary-carrying tiles, two from each crossing class. A zero scalar
character is therefore not a free contact.

For a collection of distinct edges of one tree, these costs can be
added without counting a tile twice: each tile has exactly one
short-node to long-node transition. For example, with

\[
f(x)=|x|\quad(x\ne0),\qquad f(0)=2,
\]

every finite set of nonempty exterior-free cuts satisfies

\[
\sum_e\bigl(f(P_e)+f(Q_e)\bigr)\le N.
\]

The corresponding sums for the two prime trees cannot be added directly.
Per-node positive and negative crossing requirements can additionally
be rounded up to multiples of `c`, with the prescribed residues at
the exceptional core. The
[charged-parent tradeoff](flux/CHARGED_PARENT_TRADEOFF.md) records those
bounds and the extra costs of unit-charge terminal children.

For an exterior-free terminal child attached directly to the core,
charge `-c` forces at least `5c` odd tiles in the whole board, while
charge `+c` forces at least `7c` and a larger even population. The
resulting necessary whole-board counts are:

| Count | With a core-attached `-c` leaf | With a core-attached `+c` leaf |
|---:|---:|---:|
| 3431 | 249 | 397 |
| 5063 | 247 | 419 |

These are lower bounds under that leaf hypothesis, not minima attained
by actual tilings. No bound obtained here exceeds either target count.

The complete 143 control gives total ordinary transport cost 23 in
each tree, exactly its 23 actual unmatched tiles. Local balanced-strip
controls have zero signed flux and nonzero contact. These checks help
separate an exact transport law from an unjustified extra cost.

## 3. Actual median cuts localize the smallest odd population

The [median-cut note](geometry/ACTUAL_MEDIAN_CHARGES.md) uses the older
path frame, whose whole-board odd charge is `+c`. For any actual upper
median path, two direction counts determine an integer `t`. The genuine
tiled regions below and above it have odd charges

\[
G_{\rm odd}(\text{below})=c(t-1),\qquad
G_{\rm odd}(\text{above})=c(2-t).
\]

The canonical path has `t=0`, but a full tiling need not choose that
path. Both complete 143 controls have `t=2`; the entire odd charge
is below the path and the upper region has none.

For either target, a hypothetical total odd population of exactly
`3c` is now constrained as follows. Every upper median path has
`t=2`; all odd tiles have short height 1, belong to the native
translate `zR`, and lie below every such path. Only short heights
`0,1,2` occur, the upper remainder contains only native height-2 tiles,
and height 0 must occur below. This is a conditional theorem, not an
exclusion of the `3c` case.

The remaining height-zero contact has an extra whole-edge chain of
height 0. It cannot be discarded by treating all remaining contacts
as height 1. An exact even-height two-tile corner packing also shows
why the corner alone does not force an odd-height base tooth.

## 4. The present count and flow conditions still fit inside both budgets

The [abstract axis-flow model](joint/ABSTRACT_AXIS_FLOW.md) gives a
direct integer assignment with the following populations:

| Count | Core population | Middle height-one population | Middle signs `(+,-)` | Occupied ordinary nodes per tree |
|---:|---:|---:|---|---:|
| 3431 | 2876 | 555 | `(259,296)` | 1 |
| 5063 | 4332 | 731 | `(344,387)` | 1 |

Both assignments have the required odd charge `-c`, all core residues,
the joint-cell reserves, and all three axis currents at every used
joint cell. They also admit whole-side exterior length partitions,
designated closed-gate half-turn pairs, and a connected abstract
contact-port graph. There is no occupied exterior-free branch: the
entire charge stays at the node linked to the outer sides.

This is **not a tiling or a partial geometric packing**. The model has
no common endpoint coordinates, supporting-line placement, cyclic
sector order, planar embedding, nonoverlap, or coverage. It establishes
the precise limitation of the listed relaxation: those count and
current conditions alone cannot force more than `N` tiles or more than
45/58 nodes. The new exterior-free cut costs do not eliminate this
particular support.

The missing global step must constrain the actual positions and areas
of the contacts, or exclude their simultaneous planar realization.
Neither an abstract current assignment nor a local packing decides
that question. Both original counts remain OPEN.

## Reproduce and review

Run from this directory with ordinary Python 3 and assertions enabled:

```sh
python3 replay.py
```

The replay uses only the standard library and existing exact project
geometry. It checks full-tiling transport, two actual median cuts,
the even corner controls, and the integer axis-flow countermodels.
It does not rerun an optimizer or infer a target decision from a timeout.
The [machine-readable report](REPLAY.json) records the exact scope.

Internal reviews separately cover the
[physical flux proof](flux/AUDIT_JOINT.md) and the
[median-cut geometry](geometry/AUDIT_GEOMETRY.md). They are internal
mathematical reviews and finite exact checks, not external refereeing
or proof-assistant formalization.
