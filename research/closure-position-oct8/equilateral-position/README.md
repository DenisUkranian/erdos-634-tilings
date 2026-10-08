# Direct placement search for ideal trapezoids

Exact positive result, 8 October 2026: **T(30,30) is tiled by 180 copies of
(3,5,7)**. The CP-SAT search certificate is
`cpsat/T30_30_0-1_certificate.json`. Both the rational clipping checker and
the separate integer separating-axis/boundary checker have verified it.
The earlier unsuccessful attempts below are retained as search history.

The tile has sides (3,5,7). Coordinates (u,v) mean
(u+v/2, sqrt(3)v/2). T(x,h) has vertices
(0,0),(x+h,0),(x,h),(0,h), so it requires h(2x+h)/15 tiles.
In particular T(30,45) requires 315 tiles. A positive construction of this
trapezoid would complete the proposed three-trapezoid route to an
equilateral triangle of side 120 (960 tiles).

`search.py` enumerates placements, applies exact integer 0/1 bound
propagation to oriented atomic boundary equations, then calls a numerical
MILP or LP solver. The default placement set uses short-edge levels 0 and 1
on the lattice (i+j rho)/7, i=2j mod 7. All six rotations and both tile
orders are included. Solver-reported infeasibility is labelled
`RESTRICTED_SOLVER_INFEASIBLE_UNCERTIFIED`; it is not an exact proof and
does not concern other placement sets.

The alternative `--macro` search permits integer translations of level-0
unit tiles, two different 35-tile nonconvex pentagons from the previously
proved smaller-trapezoid constructions, and 49-tile triangular grids.
Both reflected copies and all six rotations of each block are included.
The macros use short-edge levels -1 and 1 as well as level 0. This is a
constructive search family, not a normal-form theorem.

Any integral numerical solution is rounded and then checked against the
original full boundary equations using exact integers before it is
written. `verify.py` separately checks every tile side, containment,
total area, and every pairwise intersection using rational arithmetic.
It imports no code from the placement generator.

## Recorded outcomes

* Known positive control T(29,15): 73 tiles found in both models, with all
  2628 pairwise intersection tests passing independently. This construction
  is a rediscovery of the existing `group2-trapezoids` seed, not a new theorem.
* T(30,15), two-level model: 52,238 placements, 3,654 remaining after exact
  propagation; numerical solver reports infeasibility. No exact negative
  certificate has been extracted.
* T(30,45), two-level model: 314,678 placements and 175,964 equations;
  208,994 variables remain after exact propagation. The process terminated
  with exit code 137 during root processing. Status: **INCOMPLETE**. The
  precise cause of the termination was not established.
* T(30,45), macro model: 29,272 placements, 17,166 remaining after exact
  propagation. Numerical solver reports infeasibility for this limited
  family only.
* T(30,30), two-level CP-SAT: **positive certificate found**; 180 tiles,
  all 16,110 pairs independently checked. `independent_audit.py` also
  verifies exact cancellation on 98 supporting lines and 327 intervals.
* Earlier T(30,30), two-level MILP: 164,558 placements, 83,817 remaining after
  propagation. The 120-second solver limit was reached without a solution.
  Status: **INCOMPLETE**. The separate LP attempt is recorded in its own log.

Example reproduction (Python, NumPy, SciPy):

```sh
python search.py 29 15 --seconds 60
python verify.py T29_15_0-1_certificate.json
python search.py 29 15 --macro --seconds 60
python verify.py T29_15_0-1_macro_certificate.json
python search.py 30 45 --macro --seconds 150
```

Do not interpret a resource limit or a numerical solver status as a
certificate. The positive CP-SAT output is justified by its explicit
coordinates and exact verifiers, independently of the solver's reliability.
Three cyclic copies of T(30,30) provide the side-90 equilateral construction;
the resulting larger constructions are documented separately.
