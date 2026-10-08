# Equilateral side 45 by the (3,5,7) tile: unresolved

This directory records a bounded follow-up to the verified 154 exclusion.
It does **not** prove or disprove the existence of a 135-tile equilateral
triangle, and does not establish a global height bound for that problem.

The same exact lattice enumeration and nonnegative endpoint-current
zero-elimination are used, now with `eta=2+rho`, `bar(eta)=3-rho`,
`z=(3+5rho)/7`, and target vertices `0,45,45rho`. The optional coordinate
rotation minimizes bitmap storage.

The following complete *specified-band* models were reduced to fixed points:

| Band | All contained tile placements | Surviving placements |
|---|---:|---:|
| `[0,3]` | 11,154,753 | 83,163 |
| `[-1,2]` | 11,156,376 | 186,756 |
| `[0,4]` | 97,417,539 | 83,163 |
| `[-1,3]` | 97,518,171 | 186,798 |
| `[-2,2]` | 97,508,922 | 246,516 |
| `[-2,3]` | 818,334,435 | 246,558 |
| `[-3,3]` | 6,685,554,804 | 246,600 |

The surviving placements at height 3, whenever present, number only 42; the
same is true at height -3. This observed stabilization is not a proof that
larger bands add no new possible placements.

CP-SAT reported `INFEASIBLE` for the `[0,3]` and `[-2,2]` residual Boolean
models in approximately 14 and 76 seconds. These are scoped solver diagnostics,
**not independently replayed negative certificates**. A 30-second floating-point
LP attempt on the second residual reached its time limit and decided nothing.
No positive 135-tiling was found.

A four-tile positive control was checked independently using exact lengths,
containment, area, all six pairs, and endpoint currents; deleting or duplicating
a tile is rejected. See `positive_control_verified.json`.

Example reproduction from the repository root:

```sh
g++ -O3 -std=c++17 research/final-closure-oct8/e135-bitmap/bitmap_equilateral135.cpp -o /tmp/e135-bitmap
/tmp/e135-bitmap -2 2 /tmp/e135-k5-center 90 1 0
/tmp/e135-bitmap -3 3 /tmp/e135-k7-center 180 1 0
/tmp/e135-bitmap -1 2 /tmp/e135-control 30 1 2
python3 research/final-closure-oct8/e135-bitmap/check_positive.py /tmp/e135-control
```

`solve_residual.py` builds a Boolean endpoint-current model for the surviving
placements and optionally searches it using OR-Tools CP-SAT. It reuses the
`154-cpsat/endpoint_pool.cpp` reducer, checks its accepted height range, and
explicitly marks every solver status as scoped. `probe_lp.py` is only a
floating-point diagnostic.

The `summary.json` and per-band reports preserve the exact finite scope and
surviving populations. There are no active searches associated with these
reports.
