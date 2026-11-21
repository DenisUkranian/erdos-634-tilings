# Rigid placements: exact criteria and inconclusive integer search

21 November 2026. **3431 and 5063 remain open.**

The proposed hard-body condition is mathematically necessary, but adding
it to a formulation is not an infeasibility proof. The existing full
physical endpoint model already uses actual Boolean triangle placements.
Once all their physical currents close, nonoverlap and coverage follow.
The separate [current theorem and model audit](../global-strengthening/FULL_CURRENT_AND_NONOVERLAP.md)
give the proof and distinguish full closure from temporary partial rows.

[The physical charge-budget theorem](PHYSICAL_CHARGE_BUDGET.md) now gives
one finite global criterion combining integer rigid placements, actual
contact equations, overlap incompatibilities, residual odd/even charges,
and the total tile budget. It also proves finite-depth completeness of
the physical incident expansion, without claiming a feasible search
runtime or an exclusion of either target.

The [independent mathematical audit](../global-strengthening/PHYSICAL_BUDGET_AUDIT.md)
checks the complete-row quantifier, residual charge counts, finite-depth
argument, and monotonicity under adding complete physical rows.

## Exact controls

Run from the repository root:

```sh
python3 research/2026-11-21/semiprimes/global-closure-next/rigid-body/verify_rigid_body.py
```

The standard-library checker writes [RIGID_BODY_REPLAY.json](RIGID_BODY_REPLAY.json).
It checks two small Cartesian four-triangle tilings, their fractional
average with overlapping support, and four distinct contained integer
triangles with correct total area and periodic currents which still
overlap and leave a hole. These are logical controls, not configurations
of the 3431 or 5063 tile.

It also independently rechecks the project's actual 143-tiling and
projects its native path-frame middle layer into the integer torus
model. That layer has 105 tiles, signs 56/49, and 92 occupied residue
columns. Its largest residue multiplicity is **3**. Therefore a Boolean
variable per *residue type* would incorrectly remove a verified tiling.
Boolean choices belong to distinct **actual placements**; an aggregated
residue variable must allow nonnegative integer multiplicities.

## Integer probe at 3431

`integer_torus_probe.py` makes every tile multiplicity integral in the
existing all-residue middle-layer projection. This goes beyond the old
model, which made only neighboring gate charges integral. The default
3431 run fixes the previously feasible native profile

\[
 n_+=74,\quad n_-=37,\quad Q_+(0)=22,\quad Q_-(0)=15,
\]

with zero remote gate currents. Its result is recorded in
[TORUS_INTEGER_3431_FIXED.json](TORUS_INTEGER_3431_FIXED.json).
The run reached its 55-second resource limit without an integer primal
point or an infeasibility certificate. **There is no mathematical verdict
from this run.** It tests one profile, not all minimal-mode profiles.

```sh
python3 research/2026-11-21/semiprimes/global-closure-next/rigid-body/integer_torus_probe.py \
  33 7 37 --seconds 55 \
  --out research/2026-11-21/semiprimes/global-closure-next/rigid-body/TORUS_INTEGER_3431_FIXED.json
```

This optional search needs NumPy and SciPy. A returned integer point is
checked by exact integer matrix arithmetic. No numerical infeasibility
status is accepted as a proof. The optional `--binary-residues` restriction
is a narrower exploratory search and is **not** a complete necessary
model; the 143 control above explains why. Target-specific gate capacity
certificates are used only for `(33,7,37)` and `(35,13,43)`; other parameters
receive only their trivial sign-population gate caps.

Even a certified integer torus point would not be a tiling. The remaining
geometric gap is made precise by the
[3431 cylinder and packing lift](../exact-lines-3431/README.md): linear
physical packing information and periodic contact equations can hold in
an average without holding in any one integer configuration.
