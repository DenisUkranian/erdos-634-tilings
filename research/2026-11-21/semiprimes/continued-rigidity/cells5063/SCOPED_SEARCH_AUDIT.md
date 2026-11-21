# Audit of the conditional physical phase and population encoding

21 November 2026. This audit concerns the necessary-model encoding in
[`scoped_physical_search.py`](../physical/scoped_physical_search.py).
It is not an infeasibility certificate. No unguarded target contradiction
was supplied by the reviewed search runs.

The audit inspected `ScopedGeometry.admissible`, `ScopedSearch.options`,
`labels`, `insert`, `cell_caps`, and `flush`, together with the inherited
`options`, `rebuild`, `insert`, `run`, and complete-row installation.
The source's initial cell parameter range is the established `1<=x<=42`;
any subsequently proved finite exclusions strengthen this containing
range but are not required for correctness of the reviewed encoding.

## Coordinate and sign restrictions

The standard/path isometry reverses tile signs and sends short height
`h` to `2-h`. It therefore preserves the support `{0,1,2}`. Standard
odd populations are `(37,74)` at 3431/111 and `(86,129)` at 5063/215.
The standard even charge is `-(a-b)`, so the four sign/parity caps
sum to the target count. Only upper bounds are imposed on selected
partial populations.

For 5063 the exact test `c*z^-1*q in R` is equivalent to the proved
vertex ideal `(z/c)R`. For 3431 the standard height-zero envelope is
`R+zR`, the height-one native class is `A+zR`, and the height-two
envelope is `A+zR+z^2R`. The canonical coordinate test for `R+zR`
accepts every integral point and precisely the denominator-c points
whose numerator lies in the kernel `a*y-b*x=0 modc`. These are the
complete classified envelopes, not arbitrary search bounds.

The standard height-one phase labels are independently checked in
[PHYSICAL_PHASE_COORDINATES.md](PHYSICAL_PHASE_COORDINATES.md) and its
exact replay. All 1849 phase representatives and 72 allowed vertex
increments pass. In particular the subtraction of `A` is required
to identify the native class correctly.

## Phase selectors and cell caps

For each prime tree the Boolean types have these complete-skeleton
meanings: `S` is one native 215-tile node, `B` is a native balanced 86-tile node
plus a remote charged 129-tile node, and `C` is a native charged 129-tile node
plus a remote balanced 86-tile node.

Exactly one type is selected. `S` is equivalent to absence of a
remote-label selector; otherwise exactly one nonzero label is
selected. Insertion of an actual height-one tile adds the permanent
implication from its selection to each nonzero phase-label selector.
Thus two different nonnative labels in the same tree cannot both
contain selected tiles. A remote selector need not already have a
selected tile: that permits a future completion to occupy its node.
Native occupancy is likewise not incorrectly required in the
current finite partial selection.

Grouping by the two native/non-native flags is therefore safe: every
selected tile in a flag group has the same actual selected node label
in each nonnative coordinate. The nine pairs of tree types produce
exactly the old one-, two-, or four-cell caps. The standard charged
two-cell inventory is `(43,86)`, while the standard charged four-cell
entry is `(x,43+x)`. The balanced entries are sign-symmetric.

Let the six bits have value `x`, with total binary weight 63. The
generated pseudo-Boolean formulas are exactly

\[
 \begin{array}{c|c}
 \text{formula}&\text{meaning}\\
 k+x\le43&k\le43-x\\
 k+(63-x)\le63&k\le x\\
 k+(63-x)\le106&k\le43+x.
 \end{array}
\]

The nonzero bit disjunction and weighted upper bound impose precisely
`1<=x<=42`. One common six-bit value is used for every cell, so the
encoding does not select incompatible independent per-cell parameters.

## Scope during solves and rebuilds

The inherited loop pushes a temporary solve scope before imposing the
global count cap. The overridden flush appends all sign/parity caps
and cell caps inside that same scope before any solver query. If a
guarded conflict has empty temporary-row core, its unguarded
confirmation is made without popping that scope, so the necessary
population constraints remain in force.

When the search expands its candidate pool, the old solve scope is
popped. The next pushed scope recomputes every cap from the expanded
pool. Rebuilding the solver context redeclares the same global
selectors, restores all permanent tile/label implications, and applies
the population caps again before solving. No old partial count is
silently frozen as a full population equality.

All incident placements admitted by these proved scope restrictions
remain candidates of a completed row. Temporary incomplete-row
equations retain their explicit guards. A timeout, a column resource
limit, or a conflict relying on such guards remains inconclusive.
The audit found no extra discarded phase skeleton in the reviewed
conditional encoding; it does not turn any recorded solver status
into an impossibility theorem.
