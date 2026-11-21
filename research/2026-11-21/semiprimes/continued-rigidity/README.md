# Global physical reserves and the remaining semiprime cells

21 November 2026. **The original counts 3431 and 5063 remain OPEN.**
This continuation proves a stronger global completion budget, excludes
small integer cell populations, and reduces the remaining 5063 four-cell
list. It also supplies exact examples locating the limits of several
proposed rigidity arguments. No timeout or restricted optimization result
is used as a target exclusion.

## 1. A global theorem using actual contacts and cell locations

Choose any finite set of actual endpoint/direction contact rows. Enumerate
all whole contained triangles incident to those rows, and let `F(R)` be
the independent selections that satisfy every selected row exactly.
For a retained packing `I`, let `P_I,Q_I` count its odd positive and
negative tiles and let `p_max` be the largest retained positive count
in one odd joint phase cell. Define

\[
T(I)=\max\{P_I+(c+\mu-p_{\max})_+,\ Q_I+c\},\qquad
O(I)=2c\left\lceil T(I)/c\right\rceil-c,
\]

where `(c,mu)=(37,2)` for 3431 and `(43,5)` for 5063. If `n_e(I),g_e(I)`
are the retained even count and charge, every complete target tiling
satisfies

\[
\boxed{
N\ge\min_{I\in F(R),\ |I|\le N}
\left[
\operatorname{round}_{A_o}(O(I))+
\max\{b_e,n_e(I)+|a-b-g_e(I)|\}
\right].}
\]

Here `A_o` is the already proved containing set of full odd populations:
odd multiples of 37 starting at 111, or odd multiples of 43 starting at
215. The independent even lower bounds are `b_e=64,32`. Charges use
the path frame; standard-frame signs are reversed.

The added term records a physical requirement: the positive total odd
charge must occur in at least one positively charged cell. That cell
requires `c+mu` positive tiles. Retained positive tiles in other cells
cannot supply that cell's missing population. The proof couples the
actual placement choice with the cost of completing it and avoids
counting the same tile twice in the two prime trees.

The [full theorem](global/GLOBAL_PHYSICAL_CELL_RESERVE.md) also gives a
stronger node-by-node integer reserve optimization. It applies without
a fixed total odd population or a three-height assumption. No physical
row family making its minimum exceed either target has yet been found.

## 2. Proved rigid and integer cell restrictions

The [support-line theorem](global/UNIT_CHARGE_CELL_MINORITY.md) gives:

| Tile | Cell charge | Minimum minority population | Minimum cell population |
|---|---:|---:|---:|
| `(33,7,37)` | `+/-37` | 2 | 41 |
| `(35,13,43)` | `+/-43` | 5 | 53 |

The argument uses actual supporting lines and nonoverlap: for a given
sign, a pair of nonparallel lines with specified side roles determines
at most one tile. An exact finite incidence/flow check excludes all
smaller minority populations. These ordinary-cell restrictions include
every odd-height cell and do not assume that the cell fills its whole
prime-tree node.

The [independent integer kernel proof](integer3431/SMALL_BALANCED_CELLS.md)
also excludes balanced cell populations `2,4,8,10,14` for both shapes.
Its exhaustive search includes all orientation inventories and arbitrary
integer residue multiplicities. The explicit component induction is
essential because the search stops at the first closed subkernel.

## 3. The remaining 5063 four-cell list is smaller

At odd population 215, the earlier proof leaves one, two, or four cells
at height one. In the four-cell case the sign matrix is

\[
\begin{pmatrix}(x,x)&(43-x,43-x)\\
(43-x,43-x)&(43+x,x)\end{pmatrix}.
\]

The new restrictions give

\[
\boxed{x\in\{6\}\cup\{8,9,\ldots,35\}\cup\{37,40\}.}
\]

There are **31** remaining parameters, and **218,905** containing phase
and sign skeletons, down from 296,521. Thus 77,616 skeletons are removed.
The [exact reduction](cells5063/REDUCED_CELL_CLASSIFICATION_5063.md)
retains both possible native roles and all nonnative labels. These
numbers count containing schemes, not realizable tilings or an exhaustive
placement search. One- and two-cell forms remain open.

## 4. What integrality and nonoverlap do and do not settle

Several exact controls prevent unwarranted extrapolation:

* Six whole nonoverlapping tiles fit strictly inside either board and
  satisfy all actual-transverse cylinder rows with zero charge. Thus
  those conditions alone do not force a balanced cell to have `2c` tiles.
* [Sixteen whole nonoverlapping tiles](global/BALANCED_CYLINDER_COUNTERCONTROL.md)
  fit strictly inside the 5063 board and satisfy the same cylinder rows.
  Hence small balanced populations need not be multiples of six in
  that model.
* [A universal charged cylinder control](integer3431/UNIFORM_CHARGED_CYLINDER_CONTROL.md)
  has `3c` integer nonoverlapping tiles and charge `c` in the plane,
  including 111 tiles at 3431. It fails the neighboring-node gate
  congruences and is not a board tiling. These missing conditions
  cannot be discarded in a claimed impossibility proof.

There is also a [specific board-containment obstruction](global/UNIFORM_FAN_BOARD_OBSTRUCTION.md)
for that last construction: integer spacing between the `c` rigid fans
forces a common-carrier span strictly greater than the board's maximum
chord in every allowed height-one carrier direction. This excludes the
displayed fan family, not all charged integer kernels of population `3c`.

The [two-cell continuous endpoint theorem](cells5063/TWO_CELL_RATIONAL_LIMIT.md)
gives another precise limitation. Both native roles in the 5063 two-cell
form admit strictly positive rational solutions of every full periodic
endpoint equation, with exact populations 86 and 129, the correct sign
masses, integer cell currents, and the complete-node charge equations.
All sign-specific gate capacities hold. Therefore more linear cuts from
this same continuous model cannot exclude those two profiles.

Ten [new exact dual inequalities](cells5063/SHARED_NODE_DUALS.md) do
exclude their earlier individual profiles. The first forces at least
145 tiles, by charge parity, in a cell assigned only 129. The later
rational witnesses show that this successful separation does not
extend to the whole two-cell mode.

The complete physical Boolean model already selects whole triangles
and retains actual endpoint coordinates. Full nonnegative integer
boundary-current equality implies nonoverlapping exact coverage.
Adding the words "rigid body" therefore does not supply a new missing
axiom to that complete model. The task is to obtain a verified global
contradiction from it. The new [scoped physical searches](physical/README.md)
have not produced such a contradiction; their portable row snapshots
and honest resource-stop reports are preserved.

## 5. Reproduce the new exact package

From the repository root, with assertions enabled:

```sh
python3 research/2026-11-21/semiprimes/continued-rigidity/replay.py
```

The replay uses Python's standard library and a C++17 compiler. It checks
the new line-incidence exclusions, completion-budget arithmetic, integer
kernel exclusions, packing controls, phase coordinates, reduced containing
list, ten exact duals, both rational two-cell witnesses, and the full
143-tile physical positive control. It does not rerun numerical target
searches. Each theorem states which part is a written universal proof
and which part is an exhaustive finite check or a positive control.

The [internal audit](INTERNAL_AUDIT.md) records the key completeness and
scope checks. The prior 5063 minimal-mode and two-height exclusions remain
dependencies and have their own full replays in the root coordinator.
No formal proof-assistant verification or external review is asserted.

## Remaining original questions

3431 is still open at odd population 111 and at the larger allowed
populations. At 5063 the complete `n_odd=129` exclusion remains in force;
the remaining one-height 215 forms and all larger odd populations are
still open. A complete positive tiling or a certified impossibility
argument for all remaining cases is required to decide an original count.
