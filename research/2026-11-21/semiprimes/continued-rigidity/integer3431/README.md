# Integer phase cells and the limits of cylinder rigidity

21 November 2026. **3431 and 5063 remain OPEN.**

## Proved results

[`SMALL_BALANCED_CELLS.md`](SMALL_BALANCED_CELLS.md) excludes balanced
Euclidean-cell populations **2, 4, 8, 10 and 14** for both target shapes,
under the class-supported zero-endpoint-current hypothesis used in the
established phase framework. The finite search permits arbitrary integer
residue multiplicities and all orientations. It checks the component-size
induction needed to interpret a first-return search as a full population
exclusion.

This removes additional parameters from the remaining 5063 four-cell
matrix. The combined classification with the independently proved charged
cell restrictions is recorded separately in the neighboring continuation.

The same note constructs six whole, nonoverlapping, strictly contained
tiles with exactly balanced signs and zero **actual cylinder** currents
for each target board. This is a positive partial-packing control, not
a complete tiling or a compatible neighboring-node configuration. It
shows why a general balanced-cell minimum of `2c` cannot be inferred
from integer cylinder currents and physical nonoverlap alone.

At 5063 an exact balanced sixteen-column periodic point also disproves
the proposed `6/2c` population-semigroup rule for that periodic model.
The broader physical analysis of that point is carried out in the
parallel global continuation. No conjectural semigroup is asserted here.

[`UNIFORM_CHARGED_CYLINDER_CONTROL.md`](UNIFORM_CHARGED_CYLINDER_CONTROL.md)
constructs a whole-tile, pairwise nonoverlapping **charged** cylinder
packing in the unbounded plane with population exactly `3c` and charge
`c`. Its gate currents are uniformly `2` upward and `-1` downward, so it
fails the required neighboring-node remote-gate divisibility. Target-board
containment is not claimed. This isolates an explicit limitation of
integrality plus nonoverlap when the gate and board conditions are omitted.

## Exact independent replay

```sh
python3 research/2026-11-21/semiprimes/continued-rigidity/integer3431/verify_small_balanced_cells.py
```

This uses the Python standard library and C++17. The Python wrapper
reconstructs counterclockwise polygons, charge potentials, coordinate
moments, dihedral actions and inventory coverage. The independent
[`verify_balanced_kernels.cpp`](verify_balanced_kernels.cpp) uses a
disjoint-branch residual search rather than the memoized Python discovery
search. The required positive search control is a six-tile kernel.
The replay also checks the two rigid contained six-tile packings and the
sixteen-column periodic countercontrol. Output:
[`SMALL_BALANCED_CELLS_REPLAY.json`](SMALL_BALANCED_CELLS_REPLAY.json).

The charged cylinder construction has a separate standard-library replay:

```sh
python3 research/2026-11-21/semiprimes/continued-rigidity/integer3431/verify_uniform_charged_cylinder.py
```

It reconstructs all actual triangles, checks every cylinder row, verifies
all pairwise separating inequalities, and checks the failed remote-gate
congruences. Output:
[`UNIFORM_CHARGED_CYLINDER_REPLAY.json`](UNIFORM_CHARGED_CYLINDER_REPLAY.json).

## Discovery provenance and limited scopes

* `small_balanced_kernel.py` is the first memoized residue search. Its
  saved `SMALL_BALANCED_*` files concern first-return kernels. The written
  component induction is essential; arbitrary decomposable exact-size
  multisets are not enumerated by this script alone.
* `probe_balanced_inventories.py` and `probe_fixed_inventory.py` perform
  the original inventory reduction and exact prescribed-inventory search.
  Both complete size-fourteen discovery runs are saved in
  `BALANCED_37_14_INVENTORIES.json` and `BALANCED_43_14_INVENTORIES.json`.
* `CPP_BALANCED_43_16.jsonl` contains the sixteen-column positive periodic
  countercontrol. The separate 37/16 scan is exploratory and is not
  included among the theorem's asserted gaps.
* `INITIAL_INTEGER_TORUS_PROBE.json` records an inconclusive 180-second
  all-integer 3431/111 fixed-profile solve. `probe_1d.py` and its output
  record inconclusive thirty-second one-coordinate projections.
* `probe_cylinder_integer.py` finds an exact 21-column integer cylinder
  point for the small control tile `(5,3,7)`, without nonoverlap.
  `probe_packed_cylinder.py` adds actual point cliques and exact pair
  separation to finite anchor windows; its first packed 7/21 run timed
  out without a feasible point. Neither finite-window solver status is
  an unrestricted mathematical exclusion.
* `probe_translation_orbits.py` found the compact integer torus form of
  the charged `3c` construction. The three `TRANSLATION_ORBITS_*_3.json`
  files contain full positive supports and exact endpoint checks. The
  proved cylinder lift and nonoverlap are supplied by the separate replay.
* `JOINT_MARGINAL_3431_FIXED.json` and `JOINT_MARGINAL_3431_FREE.json`
  record inconclusive 45-second integer solves of the neighboring joint
  marginal model. The continuous fixed-profile counterpart is feasible,
  consistently with the previously proved rational projection barrier.
  `probe_moment_joint_marginal.py` exposes three necessary first-moment
  integer quotients; both 45-second augmented runs also timed out without
  a primal. These are diagnostics, not infeasibility certificates.
* `NONZERO_AXIS_PROBES_43.json`, the modular-image checks, and the minimum
  marginal-population optimization are exploratory records. No general
  zero-axis theorem, integer marginal feasibility, or target exclusion is
  inferred from them.

Numerical discovery programs require NumPy/SciPy. They are not dependencies
of the exact replay or the new theorem.
