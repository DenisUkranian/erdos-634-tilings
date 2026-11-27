# Common phase constraints for the two unresolved F2 boards

20 November 2026. Denis Paliy research project, with ChatGPT assistance.

**3431 and 5063 remain OPEN.** The objective of this continuation is a
single nonexistence argument covering both original boards, with arbitrary
translations, orientations, reflections and T-junctions. This package gives
new necessary theorems, exact conditional bounds, and geometric controls
that rule out several proposed shortcuts. It contains no unrestricted
impossibility certificate and no complete tiling of either target.

The [exterior-free contact reserve](../../../../2026-11-26/semiprimes/terminal-contact/REMOTE_BOUNDARY.md) charges at least 16 unmatched owners per occupied neutral branch plus two per such branch with occupied descendants, in addition to the signed exterior budget. It covers nested branches. The [one-bank area congruence](../../../../2026-11-26/semiprimes/charge-variation/AREA_RESIDUE.md) recovers the slant-side tile count modulo 2c² from the separation of two unmatched middle owners when exactly two remain.

The [native interface theorem](../../../../2026-11-26/semiprimes/charge-variation/CANONICAL_SEAM.md) determines the exact slant region when either middle bank cancels. Its opposite bank then has precisely the two canonical straight runs, with 40 or 48 unmatched owners. Without a cancellation assumption, each native middle bank whose signed current is nonzero modulo three requires at least seven unmatched owners.

The [rooted population and native cancellation theorem](../../../../2026-11-26/semiprimes/charge-variation/ROOTED.md) bounds the absolute even-minus-odd imbalance by **14 and 18** on either native sector and **17 and 23** on any exterior-free branch. If a middle bank cancels as an oriented chain, the slant side of that cut contains exactly **1369 or 1849** tiles. Every occupied middle lift has a physically unmatched owner at a native gate. [Exact replay](../../../../2026-11-26/semiprimes/charge-variation/ROOTED.json).

The [corrected even charge theorem](../../../../2026-11-26/semiprimes/charge-variation/EVEN_VARIATION.md) bounds total even variation by **38 and 58**. Every exterior-free lifted branch has absolute even-minus-odd signed imbalance at most **18 and 25** long-side blocks, respectively.

The [disjoint branch and exterior bank bound](../../../../2026-11-26/semiprimes/charge-variation/EXTERIOR_RESERVE.md) limits the total absolute odd charge in long-side blocks to **39 and 59**. At either upper bound at least one exterior marker must be a leaf in the subtree spanned by the exterior and the charged odd lifts.

The [physical slant and axial wall theorem](../../../../2026-11-26/semiprimes/slant-flux/README.md) reduces the maximum number of occupied ordinary lifts to **41 and 53**. It proves eight excess blocks at 5063 and couples signed gate currents on the two actual banks to the displacement of a whole board side. [Exact replay](../../../../2026-11-26/semiprimes/slant-flux/STATUS.json).

The [axial wall and signed-gate bounds](../../../../2026-11-26/semiprimes/axial-reserve/README.md) require at least 64 or 75 core tiles and six extra blocks among the ordinary lifts, reducing their maximum number to 42 or 55, respectively, for arbitrary complete tilings.

The [charged-circuit theorem](../../../../2026-11-26/semiprimes/charged-contour/README.md) decomposes exterior-free physical gates into Jordan polygons. At the minimum unmatched count with an off-spine charge, it excludes the entire second first-cut word at 3431 and its increasing terminal hand at 5063.

| Tile `(a,b,c)` | Count | Outer side lengths | Status |
|---|---:|---|---|
| `(33,7,37)` | 3431 | 511, 1369, 1551 | OPEN |
| `(35,13,43)` | 5063 | 1079, 1849, 2135 | OPEN |

The standard frame has vertices `0`, `b(2a+b)`, and `a(a+2b)rho`, where
`rho=exp(i*pi/3)` and `z=(a+b*rho)/c`. A tile's short height `h` is
the common exponent in its two short-side directions. The two prime
phase trees are those of the
[preceding package](../vertex-phase/README.md). An exact node counts
only tiles whose own short node equals that node. An exterior-free node
has no outer-edge node anywhere in its descendant subtree. Terminality
means that no strict descendant contains tiles in the full tiling.

## 1. Necessary conditions without a height or phase restriction

### A small terminal node uses one Euclidean translate

Inside an exterior-free terminal node at height `h`, partition tiles by
the translates `L=q+z^h Z[rho]` containing their vertices. Each occupied
translate contains a multiple of `c` tiles, at least `2c`; its positive
and negative direction-sign counts are separately divisible by `c`.
Therefore a terminal node with fewer than `4c` tiles occupies exactly
one such translate. Together with the earlier terminal balance theorem,
a node of population `2c` has exactly `c` tiles of each sign.

Thus the single-translate thresholds are **148** tiles at 3431 and
**172** at 5063, with strict inequality. The minimal terminal populations
are 74 and 86, respectively, split as `(37,37)` and `(43,43)`.
[Proof and the limits of lowering a branch](terminal/TERMINAL_TRANSLATES.md).

The argument retains every tile of the selected translate. Only the
outward matched long sides cancel; all their short sides remain. After
the short-edge current is replaced by complementary whole long edges,
the boundary lies in a lattice of axial covolume `c`. Area gives the
divisibility. Discarding the paired tiles themselves would invalidate
this proof.

### Every exterior-free node has an unmatched long edge

Let `U_v` count tiles in one occupied exterior-free exact node without
a half-turn mate across their complete side of length `c`. Then

\[
 U_v>0,\qquad U_v\ge |G_v|,\qquad U_v\equiv n_v\pmod2,
\]

where `G_v=n_v^+-n_v^-`. In particular `U_v>=2` for an even population,
and `U_v>=c` for an odd number of `c`-blocks. Terminality is unnecessary.

If all long sides paired, the remaining short-side boundary could be
replaced by whole `c` edges at one height. Its positive area would force
a supported simple cycle in one triangular mesh, excluded by the
previous whole-board geometric theorem. This proves the new assertion.

An unmatched long edge entering an exterior-free child also forces that
child to be occupied, costing at least `2c` tiles. Costs apply once per
distinct exact node. Two prime-tree costs, or multiple edges using the
same node, cannot be added as if their tiles were disjoint.
[Theorem, gate cost and exact controls](boundary/UNMATCHED_NODES_AND_GATES.md).

### Joint charges constrain both prime partitions simultaneously

At a fixed height, the intersection of one node from each prime tree is
exactly a Euclidean translate `L=q+z^h Z[rho]`. Its signed population
`G_L` is divisible by `c`, except for the single height-zero core cell
`L=Z[rho]`, whose residue is `-(a-b)`. This divisibility holds for
individual intersections, not merely the separate row and column sums.
Unsigned population divisibility is not asserted for a general cell.

For an ordinary node, write `n_v^+=cp`, `n_v^-=cq`, and `g_L=G_L/c`.
Let `P` and `Q` be the positive and negative variations of these cell
charges, and let `m` count cells with `|g_L|=1`. Then

\[
 p\ge P+\lceil m/c\rceil,\qquad
 q\ge Q+\lceil m/c\rceil.
\]

A cell of charge `c` cannot consist of just `c` equal-sign tiles, by
the supporting-line incidence theorem. It must use both signs. The
extra minority populations sum to a multiple of `c` at node level,
which proves the two reserves above.

Consequently a balanced `2c` node has no charged joint cell. Every
ordinary node of population `2c` or `3c` has degree at most one in the
bipartite graph of nonzero joint charges. A cycle whose vertices are
all ordinary requires at least `4c` tiles at each of its nodes; an
ordinary four-cycle requires at least `8c` tiles at that height.
[Full proof and exact controls](joint/JOINT_CELLS.md).

No proof identifies a cycle in this abstract charge graph with a
supported geometric cycle. Making that identification without a further
argument would leave a gap in a proposed nonexistence proof.

## 2. Stronger bounds in an explicitly restricted model

In the older path frame, suppose that the only short heights are 1 and
2, and that every tile at those heights belongs to the native meshes
`z Z[rho]` and `z^2 Z[rho]`, respectively. These are additional
hypotheses; they have not been proved for every tiling of either board.

A finite endpoint projection on `Z[rho]/c Z[rho]` retains both prime
residues. A long edge whose residue cannot meet the other mesh must
have a whole-edge half-turn mate. The resulting dual bounds are
certified by integer inequalities:

| Count | Exact lower bound for the height-one population | After divisibility and odd parity |
|---:|---:|---:|
| 3431 | `518127703/1000001` | **555 = 15c** |
| 5063 | `693711126/1000001` | **731 = 17c** |

The checks cover 8,436 and 11,352 single-tile or paired-tile columns.
The complete known 143 tiling satisfies the projection exactly, with
105 tiles at height one and 38 at height two. These bounds strengthen
the native model; they do not exceed either whole-board population.
[Certificates, proof, scope and exploratory coupled projection](joint/NATIVE_GATE_BOUND.md).

The coupled 3431 LP remains numerically feasible far below the available
population. The coupled 5063 calculation and the two small terminal
integer searches reached their time limits. A timeout, including one
whose log describes an infeasible current iterate, proves no exclusion.

## 3. Exact local controls prevent false global deductions

The [mixed-cycle controls](boundary/UNMATCHED_NODES_AND_GATES.md) place a
tiled parallelogram and its supporting teeth strictly inside each board.
The interior has `2c` tiles, balanced signs, and exactly two unmatched
long sides. Its boundary is a directed cycle of actual whole long sides
at two heights. The target controls use 140 and 156 tiles in all.

Thus the pure-height hypothesis in the earlier cycle exclusion is
essential: local containment and a tiled interior do not exclude a
mixed-height long-edge cycle. These are partial packings, with no claimed
completion to a tiling of the board.

The terminal results also do not permit removing balanced pairs and
retile the resulting region at a lower height. A single such pair is a
parallelogram whose sides are shorter than `c`; lower-height tiles would
need long sides on that boundary, which do not fit.

The larger balanced `2c` strip has the same obstruction. Its long
boundary sides force `2a` lower-height teeth, which separate the
remaining space into cells of area `2(c-a)/a` in tile units: `8/33`
and `16/35` on the targets. Each is positive but smaller than one tile.
Thus even this minimal balanced terminal pattern has no replacement
using only smaller short heights.

There is also an exact
[charged terminal polygon](terminal/CHARGED_TERMINAL_PATCH.md). A standard
`c`-grid triangle and `a+b` parent teeth form a positively tiled polygon
whose exterior-free terminal node contains `c^2` tiles with signed
population `-c`. The entire polygon fits inside each target, using 1,409
and 1,897 tiles respectively. This refutes a zero-charge lemma for
general terminal polygons even with the two target tile shapes. In a
completion of either F2 board, more same-node tiles or descendants could
appear, so it is not a counterexample to a theorem using the entire
completed board.

## 4. The remaining global step

The previously proved budgets still allow at most **45** occupied
ordinary nodes for 3431 and **58** for 5063 in either prime tree.
The whole-board odd-height signed population is `-c`. None of the new
conditions proves that every permitted placement of this charge violates
those budgets or the board's geometry.

In particular, the distinguished height-one node linked to the outer
height-two side is not exterior-free. Even a valid balance statement for
every exterior-free terminal node would not by itself eliminate the
charge in that distinguished node. Nor has a positive, boundary-preserving
operation removing arbitrary terminal branches been established.

An unrestricted exclusion needs a further theorem connecting the joint
charges, the physical attachment boundaries and the available population,
or another exact certificate applying to all placements. The numerical
classifications and partial packings here do not supply that theorem.
The status of each target therefore remains OPEN.

## Reproduce and review

Run `python3 replay.py` from this directory with standard Python and
assertions enabled. The default checks exact certificates and finite
arithmetic; optional LP and MILP generators require NumPy/SciPy. Numerical
optimization is not rerun or used as an acceptance criterion by the
default replay.

The proofs are internally reviewed research claims. Exact finite checks
verify their stated arithmetic and geometric controls; they do not
constitute an external referee report or a proof-assistant formalization.
The separate internal reviews cover the
[terminal chain replacement](boundary/AUDIT_TERMINAL_TRANSLATES.md)
and [whole-run pairing and strip argument](boundary/AUDIT_TERMINAL_REVIEW.md).
A second [terminal and charged-polygon review](terminal/AUDIT.md) records
the corrected containment expression and confirms its unchanged conclusion.

