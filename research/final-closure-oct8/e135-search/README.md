# N=135: complete three-height position models, scoped solver results

8 October 2026. No construction or global nonexistence proof for N=135 was
obtained here. The all-branch reduction leaves the equilateral triangle of
side45 and tile(3,5,7); see `../class15/REDUCTION.md`.

Two prescribed direction bands were fully enumerated. With rho=exp(i*pi/3)
and z=(3+5rho)/7, the short-edge unit vectors in a central coordinate frame are

    h=-1: (8,-5)/7; h=0: (7,0)/7; h=1: (3,5)/7.

All six rotations by60degrees and both short-edge orders are included.
Their complete vertex lattice is (1/7)Z[rho], by the established bounded-band
lattice lemma. The two target representations, with integer numerators and
common denominator7, are

    center0: (0,0), (315,0), (0,315),
    center1: (0,0), (360,-225), (225,135).

The second target is the first one rotated by z^-1, so it enumerates the
original short-edge band[0,2]; the first enumerates[-1,1]. Every listed
placement lies inside the target. The generator records endpoint derivatives
of each oriented side; there are exactly six signed entries per triangle.
This is equivalent to the positioned boundary-current equations.

| Original height band | Complete placements | Variables after exact propagation | Solver result |
|---|---:|---:|---|
| [-1,1] | 1,209,510 | 126,996 | INFEASIBLE |
| [0,2] | 1,196,589 | 83,121 | INFEASIBLE |

The Boolean model includes the explicit equation `sum(x)=135`, adjusted for
any forced-one assignments. The propagator forced no ones and found no
contradiction in either case. CP-SAT was given120seconds and one worker; the
runs finished after approximately86.5 and28.6seconds including model loading.

**Evidence scope:** these are negative CP-SAT statuses, not independently
replayed negative proof certificates. They are retained as scoped search
diagnostics. In addition, three-height bands are only part of the unrestricted
N=135 problem. Nothing here justifies declaring135 impossible, or declaring
square class15 fully classified.

## Reproduction

```sh
g++ -O3 -std=c++17 research/final-closure-oct8/e135-search/full_three_level.cpp -o /tmp/erdos634-e135-full3
/tmp/erdos634-e135-full3 60 /tmp/erdos634-e135-center0 0
/tmp/erdos634-e135-full3 60 /tmp/erdos634-e135-center1 1
ERDOS_ORTOOLS_PATH=/tmp/erdos634-ortools python3 research/final-closure-oct8/e135-search/solve_model.py /tmp/erdos634-e135-center0 --seconds 120 --output /tmp/e135-center0-report.json
ERDOS_ORTOOLS_PATH=/tmp/erdos634-ortools python3 research/final-closure-oct8/e135-search/solve_model.py /tmp/erdos634-e135-center1 --seconds 120 --output /tmp/e135-center1-report.json
```

The optional environment variable points to an isolated OR-Tools installation
(the recorded runs used9.15.6755). It may be omitted if OR-Tools is installed in
the active Python environment. Matrix files are intermediate data and are
regenerated in less than a second in the recorded environment.

The generator is adapted from the earlier full three-level N=154 enumerator;
the new driver reconstructs exact coordinates for any positive solution and
rotates center1 solutions back to the canonical equilateral target. A future
positive certificate must still pass the independent exact geometric checker
before being called a tiling.
