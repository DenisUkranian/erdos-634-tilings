# Full physical currents already enforce nonoverlap with integer multiplicities

21 November 2026. Independent mathematical audit of the proposed claim
that the 3431 case would be immediately excluded by adding rigid tile
geometry, integrality, and nonoverlap. The first two conditions already
occur in the project's whole-board model. At full physical current
closure the third is a consequence. None of these facts proves that
the resulting model is infeasible.

**Conclusion.** A finite positive integer family of actual, counterclockwise
polygon placements with exactly the board's full physical boundary current
is already an exact tiling. Explicit overlap inequalities can strengthen
an incomplete search model and its propagation, but do not add a missing
logical condition to the fully closed integer current system. A periodic
residue current is a different and substantially weaker object.

## 1. Precise theorem

Let `B` be a bounded, nondegenerate, closed simple polygon, and let
`P_1,...,P_m` be finitely many nondegenerate closed simple polygons in
the Euclidean plane. Orient every boundary counterclockwise. Triangles
are the application here. Let `x_i` be nonnegative integers. A polygon
with `x_i=0` is ignored.

Write `[[partial P]]` for its full oriented boundary as a one-dimensional
current. This records the actual position and orientation of every
segment, and permits subdivision at T-junctions and partial contacts.
Suppose

\[
 \sum_{i=1}^m x_i [[\partial P_i]]=[[\partial B]].       \tag{1}
\]

Then the selected polygons have pairwise disjoint interiors, every
selected physical placement has multiplicity one, their union is `B`,
and none extends outside `B`. Conversely an exact finite tiling with
disjoint interiors satisfies (1).

For congruent triangular placements of area `Delta` and a board of
area `N Delta`, the theorem also gives `sum_i x_i=N`. Thus the systems

\[
 \text{full physical currents equal,}\quad x_i\in\mathbb Z_{\ge0}
\]

and

\[
 \text{exact positive tiling by the selected actual triangles}
\]

are equivalent. It is harmless to impose `x_i` Boolean from the start.
If two different catalogue keys describe the same physical polygon,
their total multiplicity is at most one; a canonical catalogue avoids
this duplication altogether.

## 2. Proof through winding number and multiplicity

Away from the finite union of polygon sides, define

\[
 f(p)=\sum_i x_i\mathbf1_{\operatorname{int}P_i}(p)
                    -\mathbf1_{\operatorname{int}B}(p).
\]

The winding number of a counterclockwise simple polygon is its interior
indicator at every point not on the boundary. Winding is linear in the
oriented boundary chain. Taking winding numbers in (1) therefore gives
`f(p)=0` at all such points.

An equivalent proof avoids a winding integral. The finite side arrangement
partitions the plane into open cells, on each of which `f` is constant.
At a generic crossing of an arrangement segment, the jump of `f` is
the coefficient of that oriented boundary segment. Equation (1) makes
every such jump zero. A generic path from any cell to the unbounded
outside cell avoids the finitely many crossing vertices and shows that
its value equals the outside value zero. In distributional language,
the boundary equality says that the distributional gradient of the
compactly supported function `f` vanishes, so `f=0` almost everywhere.

If `x_i>=2`, a generic point of the nonempty interior of `P_i` has
multiplicity at least two, contradicting `f=0`. If two selected polygon
interiors overlap, their intersection is a nonempty open set; a generic
point in that set gives the same contradiction. An interior point outside
the closed board would have positive multiplicity where the board
indicator is zero, also impossible. These facts establish disjoint
interiors, multiplicity one, and containment.

Finally the finite selected union is closed and covers almost every
point in the board's interior. A missing point of a regular closed
polygon would have a relative neighborhood containing positive interior
area missing from that closed union. Hence no point of `B` is missing.
The converse follows by cancellation of the two opposite banks at every
generic interior point of a segment. This permits T-junctions and does
not assume an edge-to-edge dissection.

## 3. Why physical endpoint equations determine the full current

For a directed side `u->v`, use its exact physical, unoriented supporting
direction `d`, and add `+1` at `(u,d)` and `-1` at `(v,d)`.
At each actual point the direction identifies a unique supporting line.
Rows at different parallel lines are not identified.

Fix one such line and an arbitrary orientation along it. The signed
interval function on that line is `+1` on an edge traversed in the
chosen direction and `-1` on an oppositely traversed edge, with the
specified multiplicities. Its distributional derivative is precisely
the sum of the endpoint deltas just defined. Thus equality of every
physical endpoint row makes the difference of the tile and board
interval functions constant on the line. It has compact support, so
the constant is zero. Doing this on every actual supporting line
proves the full current identity (1).

An exact rational representation is sufficient; a numerical tolerance
is not an equality certificate. Opposite global sign conventions for
all tile and board rows are equivalent. In the present repository the
independent verifier and the search use opposite global row signs;
both compare the tile sum with the same-sign board current.

## 4. Conditions that cannot be discarded

**Nonnegative integrality.** With nonnegative real weights, (1) still
gives weighted coverage one, but permits overlapping placements with
fractional weights. For example, average two different exact tilings
of the same region: every current equation holds, and a tile present
only in one tiling has weight one half. Oppositely chosen diagonals
of an interior unit square give explicit overlaps in such an average.
With negative weights, signed cancellation can hide overlaps and holes.

**Physical positions and lines.** Identifying endpoint coordinates
modulo `cR` forgets which translates and supporting lines carry the
currents. A periodic solution can cancel terms from different locations.
It supplies no finite physical boundary equality of the form (1).
Even integer periodic weights do not repair that lost information.

**All selected physical rows.** A solution of only finitely many chosen
endpoint equations can have uncanceled current at its other physical
endpoints. Such a solution is not a tiling certificate, whether its
variables are integer or Boolean.

**Actual congruent placement geometry.** A column must describe the
three sides of one rigidly placed congruent triangle at common vertices.
An abstract inventory of side directions, lengths, charges, or separate
contact ports is not such a column. The theorem does not glue these
abstract ports into common physical coordinates.

These distinctions do not weaken the following elementary alternative:
if one actually exhibits `N` contained congruent triangles with pairwise
disjoint interiors and total area equal to the board, they necessarily
tile it, by the same closed-union and area argument. This is a criterion
for validating an exhibited solution, not an argument that no solution
can exist.

## 5. Audit of the existing whole-board formulation

The implementation already contains these features:

| Component | Existing meaning |
|---|---|
| `Geometry.vertices()` and `Geometry.admissible()` | One actual congruent triangle at exact rational coordinates, with exact board containment and necessary boundary arithmetic |
| `Search.insert()` | A Boolean variable for each distinct placed triangle |
| `Geometry.rows()` | All six exact endpoint/direction contributions of that physical triangle |
| `Geometry.incident()` / row completion | All potentially incident rigid placements at one physical row, before exact containment filtering |
| Complete physical residual check | Exact boundary-current equality, which already gives nonoverlap and coverage |
| Wedge and interior-point at-most-one clauses | Valid additional propagation and necessary constraints while the physical model is incomplete |

See the existing
[whole-board model](../../../../2026-11-20/semiprimes/continuation/global-endpoints/integer/global_core_sat.py),
[its quantifier and temporary-row explanation](../../../../2026-11-20/semiprimes/continuation/global-endpoints/integer/README.md),
[independent positive-current verifier](../../../../2026-11-20/semiprimes/continuation/global-endpoints/verify_endpoint_tiling.py),
and [complete finite spine-class model](../../../../2026-11-20/semiprimes/continuation/global-closure/spine/NATIVE_ENDPOINT_COMPLETENESS.md).

There are two different uses of the word complete:

1. A **complete individual row** has all admissible columns that can
   affect that particular physical endpoint. Imposing a finite set of
   such rows gives a necessary projection of every full tiling. It need
   not make every endpoint of a selected placement balance.
2. A **fully closed selected physical current** has zero residual at
   every endpoint/direction of every selected triangle and of the board.
   It gives (1), and the theorem applies even if the unused candidate
   catalogue was never fully enumerated.

An independently certified infeasibility of the permanent complete-row
necessary projection can exclude all tilings in the proven scope of
its incident oracle. A satisfiable assignment of only those rows is
not yet a tiling. Conversely, a finite selected list accepted by the
independent full-current verifier is already a positive solution.

Temporary equations use only the current finite pool at an unfinished
row. They can wrongly exclude a real tiling whose missing column would
balance that row. An UNSAT result using such guards calls for expansion;
it is not a global impossibility result. A timeout without a feasible
point or an exact infeasibility certificate is likewise inconclusive.

Explicit overlap clauses are always legitimate for actual placements:
overlapping interiors cannot be repaired by adding other positive tiles.
They therefore help an incomplete necessary model. In the fully closed
nonnegative integer current system, however, they follow from Sections
1--3 and do not alter its set of solutions.

## 6. Consequence for the asserted immediate exclusion

The statement that *the periodic fractional witness has not enforced
integral physical nonoverlap* is correct. The inference that *3431
therefore becomes impossible as soon as those conditions are added*
does not follow. It requires a proof of infeasibility of the resulting
physical integer system, with an exhaustive placement scope or a valid
complete-row quantifier argument.

Neither the endpoint equivalence theorem nor the exact abstract contact
graph calculations supplied beside this note provide that proof. They
also provide no full tiling of 3431 or 5063. Both original questions
remain open in these results.

## Exact logical controls

`verify_current_controls.py` supplies deterministic rational controls
of the hypotheses on a nine-tile right-isosceles triangular board.
It checks two full integer tilings by exact physical currents and
separating-axis nonoverlap. Their fractional average preserves the
full current and has weighted coverage one despite overlapping
selected interiors. A different list of nine distinct contained
congruent placements preserves area and all currents modulo the
integer lattice, but has both a hole and an overlap. Its full
physical current has 12 nonzero residual rows.

These are general logical controls, not computations on the target
boards. Run `python3 verify_current_controls.py`; the saved exact
output is [`CURRENT_CONTROLS_REPLAY.json`](CURRENT_CONTROLS_REPLAY.json).
