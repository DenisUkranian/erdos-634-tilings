# What follows, and does not follow, at five odd population blocks

21 November 2026. The exact exclusion of the entire `3c=129` mode at
5063 is proved in [`../MINIMAL_ODD_EXCLUSION_5063.md`](../MINIMAL_ODD_EXCLUSION_5063.md).
It gives `n_odd>=5c=215`, not impossibility of 5063. This note records
necessary structure **conditional on `n_odd=5c`**, for either target,
and explains why population bookkeeping alone does not exclude all
larger odd populations. No new LP or geometric placement search is used.

Use the path frame. The total odd charge is `G_odd=c`, so the five-block
mode has precisely `3c` positive and `2c` negative odd-height tiles.

## 1. At most two odd nodes, and at most two odd heights

Every odd exact node in either prime tree is ordinary: the exceptional
population residue occurs at an even-height core. Every occupied ordinary
node has a positive population divisible by `c`, at least `2c`.
Consequently each tree has at most two occupied odd nodes. Their block
partition is either `(5)` or `(2,3)`.

The same reasoning applies to physical heights, because a positive
population at an odd height is divisible by `c` and at least `2c`.
There are at most two occupied odd heights. If there are two, their
populations are `2c` and `3c`, and each of these heights occupies one
exact node in each tree, hence one Euclidean translate of `z^hR`.
This does not identify either translate as native.

For two occupied odd exact nodes, their possible sign-block inventories,
in the order of the `2c` node and the `3c` node, are exactly

\[
 ((2,0),(1,2)),\qquad ((1,1),(2,1)),\qquad ((0,2),(3,0)). \tag{1}
\]

They have total `(3,2)`. These are arithmetic possibilities, not a
claim that each can be realized geometrically. Counts from the two
prime trees are never added.

## 2. An initial height bound for the entire five-block mode

**Conditional height theorem.** Every complete target tiling with
`n_odd=5c` has

\[
 \boxed{\text{odd short heights in }\{-1,1,3\},\qquad
        \text{all short heights in }[-2,4].}           \tag{2}
\]

At most two of the three displayed odd heights occur. Their possible
sets are therefore

\[
 \{1\},\quad\{-1,1\},\quad\{1,3\},\quad\{-1,3\}.  \tag{3}
\]

The inputs are the already proved occupied-immediate-parent theorem
for exterior-free subtrees and the long-side-on-every-outer-side lemma
from
[`CHARGED_PARENT_TRADEOFF.md`](../../../2026-11-20/semiprimes/continuation/charge-transport/flux/CHARGED_PARENT_TRADEOFF.md).
The latter applies because each board corner is less than 120 degrees:
an outer side made only of short tile sides would require more distinct
120-degree vertices on that side than its internal subdivision points.

The outer height-zero base consequently has a supplying long tile side
whose odd short height is `-1` or `1`. An outer height-two side similarly
requires odd short height `1` or `3`.

If an odd height `h>=5` occurred, follow its increasing-tree ancestors.
All nodes above physical height 2 are exterior-free, so occupied parents
force occupied odd height 3 as well. These are already two different
odd heights, while the base independently requires `-1` or `1`.
That would give three, contradicting Section 1. The conjugate-tree
argument excludes odd `h<=-3`: occupied ancestors force `-1`, and
an outer height-two side independently requires `1` or `3`.

Finally an occupied even height `h>=6` has an exterior-free increasing
node, whose occupied parent would have excluded odd height `h-1>=5`.
An occupied even height `h<=-4` similarly forces the excluded odd parent
`h+1<=-3` in the conjugate tree. This proves (2). The two outer-side
requirements then give precisely the list (3).

This is not the old three-height localization. Heights `-2,-1,3,4`
have not been excluded here, nor have multiple height-one phases.

## 3. Every actual upper median cut has one of seven arithmetic splits

For a vertex-simple upper median path, let `D` be its genuine tiled
lower polygon and `E` the entire upper remainder. The established
[median charge identities](../../../2026-11-20/semiprimes/continuation/charge-transport/geometry/ACTUAL_MEDIAN_CHARGES.md)
are

\[
 G_{\rm odd}(D)=c(t-1),\qquad G_{\rm odd}(E)=c(2-t),
 \qquad t\in\mathbb Z.                                \tag{4}
\]

Each positive odd population on either side is divisible by `c` and
at least `2c`. Its population-block parity agrees with its charge in
units of `c`. Combining these facts with total five blocks gives:

| `t` | Odd blocks `(D,E)` | Odd sign blocks `(D+,D-)` | Odd sign blocks `(E+,E-)` |
|---:|---:|---:|---:|
| -1 | `(2,3)` | `(0,2)` | `(3,0)` |
| 0 | `(3,2)` | `(1,2)` | `(2,0)` |
| 1 | `(2,3)` | `(1,1)` | `(2,1)` |
| 2 | `(3,2)` | `(2,1)` | `(1,1)` |
| 2 | `(5,0)` | `(3,2)` | `(0,0)` |
| 3 | `(2,3)` | `(2,0)` | `(1,2)` |
| 4 | `(3,2)` | `(3,0)` | `(0,2)` |

The purely arithmetic split `(D,E)=(0,5),t=1` is impossible. In fact
the height-two path character satisfies

\[
 K=(c-d)t-dj_0,\qquad d=a-b,\qquad j_0\in\mathbb Z.
\]

If `t=1` and `K=0`, coprimality gives `d|1`, false for `d=26,22`.
Thus some actual height-two path step occurs, and its lower-bank tile
has short height one. The lower region has odd tiles, contrary to
that empty-side split.

All displayed rows are necessary possibilities only. In particular
the five-block mode does **not** inherit the three-block conclusion
`t=2` for every path or that every odd tile lies below every path.
If height one is absent, every upper path has only height-one steps,
so `K=0`; the table and `d|t` then force `t=0`, `j_0=0`, and `J=d`.
Section 4 excludes that alternative using the real parent contact.

## 4. Height one is unavoidable at five blocks

**Stronger five-block theorem.** In fact height one must be occupied.
The only possible odd-height sets are

\[
 \boxed{\{1\},\qquad\{-1,1\},\qquad\{1,3\}.}          \tag{5}
\]

Consequently all short heights lie in one of the intervals `[-2,2]`
or `[0,4]`; when the only odd height is 1, all short heights lie in
`{0,1,2}`. Multiple odd-height phases have not been excluded.

Suppose height one were absent. Section 2 forces precisely the two
odd heights `-1,3`. Every upper median step must then have long
height one, because a height-two step would have a height-one bank
tile below it. Thus `K=0`. Section 3 gives `t=0`, and hence

\[
 G_{\rm odd}(D)=-c,\qquad G_{\rm odd}(E)=2c.
\]

The sidewise population minimum and sign parity force at least `3c`
odd tiles in `D` and at least `2c` in `E`. They exhaust the five-block
total, so these are equalities. Each region can contain only one
occupied odd height, because each such height in that region requires
at least `2c` tiles.

An actual long-side supplier on the base has short height `-1` and
lies in `D`: the median path has no open-base contact and cuts only
along tile edges. An actual long-side supplier on an outer height-two
side has short height 3 and lies in `E`: the path has only height-one
edges and cannot overlap that outer side in positive length. Therefore
all height-minus-one tiles lie in `D`, and all height-three tiles lie
in `E`. In particular

\[
 n_3=2c,\qquad n_3^+=2c,\qquad n_3^-=0.              \tag{6}
\]

At this height the ordinary-node lower bound permits only one occupied
node in each tree, hence one Euclidean class. Every occupied height-four
node would be exterior-free and terminal in the increasing tree:
Section 2 excludes every short height above 4. Its immediate parent is
the unique occupied height-three node.

By bidirectional physical transport, that child has at least one
unmatched parent tile. All parent signs are positive, so its signed
parent crossing count `Q` is strictly positive. Terminal transport and
ordinary-node charge integrality give

\[
 Q=dg,\qquad g\in\mathbb Z,\qquad Q\ge d.             \tag{7}
\]

Those parent tiles use one upward gate of the single height-three
Euclidean class. There is no exterior side at height 3. The global
[single-class gate capacity](../../../2026-11-20/semiprimes/continuation/global-closure/median/NATIVE_GATE_CAPACITY.md)
therefore bounds the entire positive gated population, hence also `Q`, by

\[
 Q\le \frac{43(2\cdot37)}{222}=\frac{43}{3}<26=d
       \quad(3431),
\]
\[
 Q\le \frac{8(2\cdot43)}{43}=16<22=d
       \quad(5063).                                  \tag{8}
\]

This contradicts (7). No height-four node is occupied. The height-three
node is now itself exterior-free and terminal, with exactly `2c` tiles
all of one sign. This contradicts the established
[terminal two-block balance theorem](../../../2026-11-20/semiprimes/continuation/vertex-phase/TERMINAL_NODE_BALANCE.md).
Height one must therefore occur, proving (5).

This argument uses actual bank populations and the occupied-parent
theorem. It does not apply the isolated-gate branch inequality beyond
its hypotheses, and does not assert that any of the remaining sets in
(5) is realizable. It also does not exclude the five-block mode itself.

## 5. Why a population-only argument cannot close every larger mode

The existing exact
[two-tree axis-flow countermodel](../../../2026-11-20/semiprimes/continuation/charge-transport/joint/ABSTRACT_AXIS_FLOW.md)
at 5063 has `K=17`, hence `n_odd=731>=215`. In its standard frame:

| Population | Positive | Negative | Total |
|---|---:|---:|---:|
| Even core | 2,155 | 2,177 | 4,332 |
| Odd middle spine | 344 | 387 | 731 |
| Total | 2,499 | 2,564 | 5,063 |

It satisfies the existing integer phase populations, both prime-tree
balances, joint-cell sign reserves, all three joint-cell axis currents,
boundary-length port inventories, closed-gate pair requirements, and
the older conditional native two-height population lower bounds.
It has **no occupied exterior-free short node**, so bounds on charged
or balanced terminal branches impose no additional cost on this support.
The newly excluded 129-tile mode is absent as well.

This is an exact abstract inventory, **not a geometric tiling**: it has
no common vertex coordinates, per-supporting-line endpoint realization,
nonoverlap, or planar coverage. It demonstrates the limitation of those
population and axis equations, not the existence of a 5063 tiling. A
successful global exclusion must add a condition that this abstract
assignment does not already satisfy, or independently rule out its
geometric realization. There is no justified operation that removes
balanced pairs from an arbitrary positive tiling while preserving its
region and thereby reduces every larger odd population to 129.

## 6. Exact arithmetic control

`verify_five_block_scope.py` checks the node sign allocations, all median
split possibilities, the boundary-supplier height sets in a displayed
finite control range, the strict parent-gate inequalities (8), and the
exact `K=17` inventory arithmetic. The
unbounded height conclusion is proved in Section 2; it is not inferred
from the finite enumeration. The existing `abstract_flow.py` remains
the full replay of the axis-flow countermodel.

```sh
python3 verify_five_block_scope.py
```

The output is `FIVE_BLOCK_SCOPE_REPLAY.json`. Neither this note nor that
arithmetic control excludes the five-block mode or either entire target.
