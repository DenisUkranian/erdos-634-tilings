# Small balanced Euclidean cells: exact gaps and a rigid six-tile control

21 November 2026. **Neither 3431 nor 5063 is excluded.** This note gives
new necessary restrictions on an individual balanced Euclidean phase
class. Its conclusions do not require numerical optimization.

For either tile `(33,7,37)` or `(35,13,43)`, a nonempty balanced class
whose periodic short-edge endpoint current is zero cannot have population

\[
\boxed{2,\ 4,\ 8,\ 10,\ 14.}                         \tag{1}
\]

In particular its population is at least six. A separate exact construction
places **six integer, nonoverlapping tiles inside either target board**
with zero cylinder endpoint current and three tiles of each sign. Thus
the bound six is attained in this integer cylinder packing relaxation.
It does not exhibit a phase cell of a complete target tiling: the full
physical endpoint current and the neighboring-node gate constraints are
not satisfied or asserted by that six-tile partial packing.

The proposed stronger rule “all balanced populations below `2c` are
multiples of six” is already false for the **periodic** model at 5063:
an exact balanced sixteen-tile point is supplied below. Consequently
the finite gaps (1) must not be extrapolated to a population semigroup.

## 1. Complete residue columns for one class

Normalize the selected class to `R=Z[rho]`, where `rho=exp(i*pi/3)`.
Write `U_j=rho^j`, and let a placed tile `(q,j,s)` have acute vertices

\[
u=q-aU_j,\qquad w=q+bU_{j+s},\qquad
\epsilon=s(-1)^j.
\]

There are all `12c^2` residue columns, with `q=(x,y)` modulo `cR`,
`0<=j<6`, and `s=+1` or `-1`. A row is `(i,q)` with `i mod 3`.
The column has four endpoint terms

\[
 s(j,q)-s(j,u)+s(j+s,w)-s(j+s,q).                     \tag{2}
\]

A column means a complete rigid triangle, not independent edges.
Its coefficient is a nonnegative integer. Different actual translations
can have the same residue; **multiplicities are allowed**.

For a class with zero exterior contribution at this short height, the
sum of (2) is zero in every row. Indeed an endpoint potential supported
on the class telescopes across all actual contacts, including T-junctions.
Other short classes contribute zero. A complementary whole long edge
at this height has displacement `cU_j`, so its endpoints give equal
periodic values. This is the same class-supported identity used in
[the earlier endpoint certificates](../../gate-model/CERTIFICATES_5063.json).
In the remaining 5063 one-height regime, every height-one class has
zero exterior contribution, so the reduction applies to each separately.

Let a **positive kernel** be a nonempty multiset of these columns whose
sum is zero. Its population is the total multiplicity; its charge is
the multiplicity-weighted sum of `epsilon`.

## 2. Every small positive kernel is balanced

Let `t=(a-b)^(-1) mod c`. Give row `(i,(x,y))` the potential

\[
f_0(x,y)=t x,\qquad f_1(x,y)=-t y,\qquad
f_2(x,y)=t y \pmod c.
\]

For a unit direction `U_j`, the potential difference on its axis is
`t(-1)^j`. Applying these potentials to (2) gives

\[
s\bigl(a t(-1)^j+b t(-1)^{j+s}\bigr)
=t(a-b)s(-1)^j=\epsilon\pmod c.
\]

The zero endpoint sum of any integer positive kernel therefore gives

\[
\boxed{c\mid G.}                                    \tag{3}
\]

If its population is less than `c`, then `|G|<c`, hence `G=0`.
In particular every positive closed submultiset arising in the checks
through population fourteen is balanced and has even population.
This supplies the component argument needed by the finite search;
the same statement is not assumed for arbitrary large submultisets.

## 3. Exhaustive orientation-inventory reduction

For each short axis `i`, let `M_i` be the signed number of length-`a`
edges and `L_i` the signed number of length-`b` edges belonging to
that axis. The separate coordinate moments of (2) imply

\[
 aM_i-bL_i\equiv0\pmod c\qquad(i=0,1,2).             \tag{4}
\]

For a tile `(j,s)`, its contribution is `a epsilon` on axis `j mod3`
and `-b epsilon` on axis `(j+s) mod3`. There are six positive
orientations and six negative ones. The negative orientation with
the same ordered side axes is the positive one's half-turn.

For population `2k`, enumerate all weak compositions of `k` into
the six positive orientation counts and independently all compositions
of `k` into the six negative counts. Group each composition by its
three moments modulo `c`. A pair is allowed by (4) exactly when its
positive and negative moment signatures agree. This enumerates the
entire containing inventory set, with no individual-placement cutoff.

Rotations and reflections act by

\[
(q,j,s)\mapsto(\rho^r q,j+r,s),\qquad
(q,j,s)\mapsto(\overline q,-j,-s).
\]

They preserve the zero endpoint equations and balanced population.
The checker verifies the two generating column actions and checks all
twelve transforms of every accepted inventory. Choosing one canonical
inventory per orbit consequently loses no kernel.

| Population | Compatible labeled inventories | Dihedral inventory orbits |
|---:|---:|---:|
| 2 | 6 | 1 |
| 4 | 21 | 5 |
| 8 | 138 | 25 |
| 10 | 294 | 47 |
| 14 | 1086 | 161 |

These counts agree for the two target shapes; that agreement is checked,
not used to transfer one target's endpoint search to the other.

## 4. Exact residual search and its quantifiers

Fix one accepted orientation inventory. Choose any orientation with
positive prescribed population and translate one of its selected tiles
to anchor `(0,0)`. Translation modulo `cR` preserves every endpoint
equation. Every kernel in this inventory therefore has such a normalized
representative.

Starting with this tile, record the exact integer residual at every row.
At a nonzero residual row, every completion must contain a column with
the opposite coefficient there. Enumerate **every** such column whose
orientation count is still available. All incident columns come from
the complete `12c^2` catalogue. A residual with absolute sum greater
than four times the remaining population cannot be repaired; neither
can a single residual of magnitude greater than that population.

The independent C++ implementation partitions the branches by the first
eligible column: after exploring one candidate, it excludes that candidate
from subsequent sibling branches. Repeated copies remain allowed within
the candidate's own branch. Every completion has a first eligible column,
so these branches are exhaustive and disjoint. The original Python
discovery instead memoizes sorted selected multisets.

Both searches stop when the residual first becomes zero. Thus their
direct output concerns **first-return kernels**, not every decomposable
multiset at an arbitrary exact size. In particular a search stopped this
way would not enumerate two separate six-tile wheels as a size-twelve
configuration. That limitation is accounted for as follows.

**Component induction.** Every positive kernel can be decomposed into
inclusion-minimal positive kernels by repeatedly removing a nonempty
minimal closed submultiset. For total population below `c`, each such
piece is balanced by (3). Suppose all smaller even populations not
divisible by six have already been excluded. Any decomposition of a
kernel at the next nonmultiple-of-six population either contains a
smaller forbidden piece, or all proper pieces have populations divisible
by six, which cannot sum to that population. It would therefore require
an indecomposable kernel of the full population. The residual search
contains every such kernel, because none of its proper selected prefixes
can already be closed.

Apply this induction successively at `2,4,8,10,14`. At each step the
complete inventory search returns no first-return kernel. The intervening
populations six and twelve need not be excluded or exhaustively classified.
This proves (1) for all positive kernels, including decomposable ones.

The independent C++ replay uses these exact state counts:

| Population | `(33,7,37)` states | `(35,13,43)` states |
|---:|---:|---:|
| 2 | 2 | 2 |
| 4 | 30 | 30 |
| 8 | 2908 | 2908 |
| 10 | 26223 | 26213 |
| 14 | 4491576 | 4496003 |

The differently organized original Python searches also find no size-four,
size-eight, size-ten or size-fourteen kernels. The proof relies on the
complete integer replays and the stated reduction, not on an optimizer's
infeasibility status.

## 5. Six rigid nonoverlapping tiles survive every cylinder row

Put `L=2c` and take these six anchors relative to a common center:

\[
(-L,L),\ (0,L),\ (L,0),\ (L,-L),\ (0,-L),\ (-L,0).
\]

Use orientations, in the same order,

\[
(j,s)=(0,+1),(0,-1),(4,+1),(4,-1),(2,+1),(2,-1).
\]

The cylinder rows retain the actual transverse coordinate and only reduce
the coordinate along the supporting line modulo `c`:

| Axis | Actual transverse coordinate | Longitudinal residue |
|---:|---|---|
| 0 | `y` | `x mod c` |
| 1 | `x` | `y mod c` |
| 2 | `x+y` | `y mod c` |

Each length-`a` side is paired, with the opposite current, to the same
side of the opposite-hand tile translated by `L` along that side's
axis. The six length-`b` sides pair in the same way around the hexagon.
Since `L` is a multiple of `c`, every cylinder endpoint row cancels
exactly. There are three positive and three negative signs.

The anchor distance between any two tiles is at least `2c`. Each entire
triangle lies in the radius-`a` disk about its obtuse vertex, because
`a>b` for both targets. As `a<c`, these disks are disjoint. The six
tiles therefore have pairwise disjoint interiors without any numerical
tolerance.

They also fit strictly inside their respective target boards. Use the
path frame divided by `z`, with center `(800,0)` for 3431 and `(1000,0)`
for 5063. With `B=a(a+2b)`, the board's exact inequalities are

\[
 bx+(a+b)y\ge0,\quad bx-ay\ge0,\quad
 (a+b)x+by\le cB.
\]

All eighteen tile vertices satisfy them strictly. The minimum positive
halfplane values are 1551 and 7647, respectively. The replay records
all placements and checks those values with integers.

There are nevertheless 24 nonzero **physical short-endpoint** rows.
The cylinder has identified endpoints separated along their line.
No full tiling or consistent surrounding even population is supplied.
Thus this construction prevents replacing (1) by a claim that physical
nonoverlap and integer cylinder equations alone force a balanced
population of at least `2c`.

## 6. A sixteen-tile periodic countercontrol

At 5063, the exact discovery file
[`CPP_BALANCED_43_16.jsonl`](CPP_BALANCED_43_16.jsonl) contains a positive
sixteen-column point with eight signs of each kind and zero periodic
endpoint current. The standard-library checker independently rebuilds
its polygons and checks every endpoint coefficient. This is already
enough to refute an unrestricted `6/2c` population-semigroup assertion
for the periodic model. Its physical completion is not asserted here.

## 7. Consequence for the remaining 5063 four-cell matrix

In the previously proved
[one-height classification](../../global-closure-next/global-strengthening/ONE_HEIGHT_CELL_CLASSIFICATION_5063.md),
the balanced cell populations are `2x` and `2(43-x)`. Applying (1)
excludes

\[
x\in\{1,2,4,5,7,36,38,39,41,42\}.                   \tag{5}
\]

This is a new necessary restriction. The six-tile control does not show
that any remaining matrix or gate system can be realized in a complete
tiling. Other independent restrictions can be combined with (5), with
their separate hypotheses and proof dependencies retained.

## Reproduction

From the repository root, run

```sh
python3 research/2026-11-21/semiprimes/continued-rigidity/integer3431/verify_small_balanced_cells.py
```

The verifier uses the Python standard library and a C++17 compiler. It
reconstructs CCW polygon columns independently, checks all charge and
moment identities, verifies the dihedral generators, regenerates every
orientation inventory, checks the component-size induction, and compiles
and runs the independent exact search. It also requires a positive
six-tile search control and checks the contained rigid six-tile packing.
The deterministic output is
[`SMALL_BALANCED_CELLS_REPLAY.json`](SMALL_BALANCED_CELLS_REPLAY.json).

Other scripts and logs in this directory are separately scoped discovery
diagnostics. Time limits and finite anchor windows in those diagnostics
are not impossibility certificates for either original target.
