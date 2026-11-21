# Remaining 5063 cells: exact reductions, cuts, and relaxation witnesses

21 November 2026. **5063 remains OPEN.** Its 215 odd-tile mode is not
excluded by this folder. All mathematical claims distinguish actual
rigid cells, positive integer endpoint kernels, and fractional periodic
endpoint models.

## Results

| File | Exact conclusion |
|---|---|
| [REDUCED_CELL_CLASSIFICATION_5063.md](REDUCED_CELL_CLASSIFICATION_5063.md) | The new physical minority and integer kernel exclusions reduce the four-cell parameter to 31 values and the containing phase/sign list to 218,905 skeletons. |
| [TWO_CELL_RATIONAL_LIMIT.md](TWO_CELL_RATIONAL_LIMIT.md) | Both native roles in the two-cell case admit strictly positive rational full-endpoint witnesses, with integer cell currents, integral complete-node charge units, exact sign masses, and gate caps. No physical or integer-column realization is asserted. |
| [SHARED_NODE_DUALS.md](SHARED_NODE_DUALS.md) | Ten new exact endpoint inequalities exclude their own recorded candidate profiles. They are not an exhaustive exclusion of the shared-node universe. |
| [FINITE_CUT_POOL_LIMIT.md](FINITE_CUT_POOL_LIMIT.md) | An explicit integer current profile passes the earlier 65-cut pool but is excluded by the first new cut. This separates a finite-pool gap from the stronger full-model limit above. |
| [PHYSICAL_PHASE_COORDINATES.md](PHYSICAL_PHASE_COORDINATES.md) | Exact standard/path coordinate conversion, phase labels, sign reversal, and native-class arithmetic. |
| [SCOPED_SEARCH_AUDIT.md](SCOPED_SEARCH_AUDIT.md) | Independent review of the physical search's scoped phase, sign-population, and cell-cap encoding; no extra discarded skeleton was found. This is not an UNSAT certificate. |

The 31 remaining four-cell parameters are
`{6} union {8,9,...,35} union {37,40}`. The one- and two-cell forms remain in
the containing list. The full fractional two-cell witnesses show why
additional linear endpoint cuts alone cannot complete this part of the
research: integer individual columns or more physical geometry must be
retained.

## Exact replay

From this directory run:

```sh
python3 verify_phase_coordinates.py
python3 verify_finite_cut_witness.py
python3 verify_reduced_skeletons.py
python3 verify_shared_profile_duals.py
python3 verify_two_cell_rational_witness.py
```

All five verifiers use only the Python standard library. They produce,
respectively, `PHASE_COORDINATES_REPLAY.json`, `FINITE_CUT_POOL_REPLAY.json`,
`REDUCED_SKELETONS_REPLAY.json`, `SHARED_PROFILE_DUALS_REPLAY.json`, and
`TWO_CELL_RATIONAL_REPLAY.json`.

The reduced skeleton verifier checks the consequence of the separately
proved cell minority and small balanced-kernel theorems and records their
replay hashes. Their own geometric and exhaustive finite-search verifiers
remain the necessary premise replays. The rational witness checker
replays the previously audited Fourier inverse bound for 43, reconstructs
all new polygon columns independently, and proves the correction margins
exactly; it does not call a numerical optimizer.

## Discovery record

`probe_joint_gate_cuts.py`, `discover_cell_cut.py`, and
`refine_joint_cut_pool.py` are optional SciPy discovery tools. They keep
cell gate vectors separate and impose full-node congruences only after
summing the incident cells. Shifted inequalities can use an exact
maximum-variable extended formulation.

`two_native_balanced_fixed_full/` and `two_native_charged_long/` contain the
floating discoveries behind the two exact rational cases. The certificate
builder packages those approximate points, while the independent verifier
is the mathematical check. Other probe JSON files preserve inconclusive
time limits and limited-pool discoveries. Their numerical statuses are
not impossibility certificates and are not used to reduce the containing
list.
