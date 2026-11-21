# Internal proof and implementation audit

21 November 2026. This records independent internal reviews and exact
replays. It is not a formal proof-assistant verification or external
peer review. Both original target counts remain open.

## Unit-charge support-line theorem

The root reviewer checked the actual-line congruence hypothesis, the
one-placement-per-ordered-line-pair argument, all candidate line types
for minority at most five at 5063, the exclusion of type F, the treatment
of zero-net lines, and the safe relaxation of additional sources and
targets. The grouped capacities are necessary images of a real simple
incidence graph, so a failed integer maximum flow excludes the original
cell as well. The finite enumeration and matching minimum cuts were
replayed independently. The 3431 minority-one argument was also checked.

The 25 remaining relaxed 5063 networks at minority five are not geometric
witnesses. The explicit signed incidence example at that boundary does
not give line coordinates or full endpoint closure.

## Global physical completion theorem

The proof retains exactly the full tiling's triangles incident to a
complete physical-row catalogue. All omitted triangles have zero
coefficient on those rows. The retained set is consequently feasible
without assuming that the current finite pool contains the rest of
the tiling.

The root reviewer checked the implication
`P>=P_I+(c+mu-p_max)_+`, the independent bound `P>=Q_I+c`, and rounding
`P` to a multiple of `c`. The even charge-repair bound is combined by
addition only with the disjoint odd population; alternative even bounds
are combined by a maximum. The known odd-population restrictions are
applied at the final rounding step, without importing minimal-mode
height localization into the unrestricted theorem.

The optional node optimization received a separate review from the
5063 investigator. Aggregate hidden cells of unit charge retain a
minority reserve; canceling larger opposite charges cannot evade it.
The sum of balanced reserves at an ordinary node is divisible by `c`,
and unseen unit-charge nodes need at least `3c` tiles. Both node costs
have the correct charge parity. The two prime-tree estimates are
combined by a maximum, avoiding duplicate population charges.

The arithmetic replay compares the formulas in finite abstract
inventories. It does not establish that any physical row family attains
the displayed sufficient thresholds.

## Small integer balanced cells

The root reviewer read both independent implementations and replayed
the C++17 verification for both targets. Orientation coverage uses a
complete stars-and-bars enumeration, exact first-moment residues, and
all twelve verified dihedral actions. Translation normalizes a tile
of an orientation that must be present.

At a nonzero endpoint row every completion contains a column with the
opposite coefficient. Partitioning branches by the first eligible
column retains repeated copies in that column's own branch. The exact
residual bounds and complete incident catalogue therefore lose no
first-return kernel.

The audit identified that first-return enumeration alone does not
enumerate arbitrary decomposable populations. The final proof and
checker explicitly repair that issue: an integer row potential proves
`c` divides the charge of every closed submultiset, and every submultiset
below `c` is balanced. Induction at `2,4,8,10,14` excludes decompositions
into smaller admissible sizes. No general population-semigroup rule
is inferred. The 16-tile countercontrol prevents that extrapolation.

## Rational two-cell witnesses and duals

The full endpoint matrices are reconstructed from exact counterclockwise
triangles. The ten dual certificates are verified with integer arithmetic
on every one of their 22,188 columns. A cut's recorded profile is checked
separately; the finite set of profiles is not asserted exhaustive.

For the positive rational witnesses the root reviewer checked that the
reused Fourier bound concerns the identical matrix, independently of
the right-hand side. Its only missing endpoint modes vanish identically,
and every new target has zero endpoint entries, so the range condition
holds. The pseudoinverse correction is rational and preserves every
equation. Integer squared-norm bounds establish coordinate positivity
and both sign-specific gate capacities. The exact checker replays all
1,849 Fourier blocks and all four new approximate points.

The shared-node equations are imposed on sums of cell currents. Individual
cell lists are never given the native offset of an entire node. Both
native roles pass the exact replay, which proves a limitation of the
continuous periodic model. It supplies neither integer individual tile
multiplicities nor physical placements.

## Physical searches and countercontrols

The separate [phase/search audit](cells5063/SCOPED_SEARCH_AUDIT.md)
checks the proved coordinate envelopes and partial sign caps. The full
143-tile certificate passes the independent metric, containment, area,
and physical-current checker. The six- and sixteen-tile cylinder
controls have explicit exact nonoverlap and board-containment checks;
the charged `3c` control has no claimed board containment and fails
the required gate congruences.

Every recorded target solver status is a resource stop or an inconclusive
answer. A conflict using temporary unfinished rows is not an impossibility
certificate. The new package asserts no unguarded target contradiction.
