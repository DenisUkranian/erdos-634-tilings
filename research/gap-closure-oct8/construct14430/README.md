# Bounded constructive searches for 14430 and its adjacent family

8 October 2026. **14430 remains OPEN.** No positive tiling certificate
was obtained, and no unrestricted nonexistence theorem is claimed.
All searches in this directory have stopped. The recorded outcomes
are finite-pool diagnostics or **INCOMPLETE**, as indicated below.

The family tested is

```
a=q(3q+2), b=2q+1, c=3q²+3q+1.
```

The desired member is q=4, tile (56,9,61), ordered F3 count 14430.
The smaller q=2 member has tile (16,5,19) and F3 count 1638. We used it
to test the same geometric idea without launching a large general SAT
enumeration for 14430.

## Sufficient geometric targets

The existing positive three-grid fan leaves a pentagon with
`3b(2a+b)` tile areas. Four further ordinary grids leave the nonconvex
hexagon

```
H=[(2A,-2A),(A,-A),(A+B,-A),(A+B,0),(B,A),(2A,A)],
A=ab, B=b²,
```

with `2b(3a-2b)` tile areas. Coordinates are Eisenstein coordinates
with squared metric `x²+xy+y²`. These are sufficient targets only;
an arbitrary F3 tiling need not contain the fixed fan.

The companion [hexagon decomposition](../f3-general/HEXAGON_STRUCTURE.md)
splits H into two equilateral triangles of side ab and a directly
tileable parallelogram. Consequently an equilateral tiling E504 by
504 copies of (56,9,61) would suffice for 14430. It was also searched.
Failure of this smaller sufficient route would not exclude 14430.

## Recorded outcomes

Here a short-height band means the explicitly enumerated placement
lattice used by the search. “Conflict” is an internal exact propagation
diagnostic for that pool, **not** a separately replayed refutation or
an unrestricted geometric result.

| Target / restriction | Initial contained placements | Outcome |
| --- | ---: | --- |
| q=1 fan pentagon, heights 0,1 | 76,690 | Pool conflict |
| q=1 fan pentagon, heights -1,0 | 76,400 | Pool conflict |
| q=2 hexagon, heights 0,1 | 4,988,624 | Pool conflict |
| q=2 hexagon, heights -1,0 | 4,988,624 | Pool conflict |
| q=2 fan pentagon, heights 0,1 | 7,673,629 | Pool conflict |
| q=2 fan pentagon, heights -1,0 | 7,661,003 | 1,699,522 survive zero-support propagation |
| q=2 pentagon with first acute-corner choice, equality compression and CP-SAT | 1,683,232 unknowns before compression | **INCOMPLETE: UNKNOWN**, 30-second solver budget |
| E504, heights 0,1 | 140,493,903 | 5,108,139 survive; no tiling obtained |
| E504 plus corner-fan choice 0 | 5,108,139 | 5,064,963 unknowns remain |
| E504 plus corner-fan choice 1 | 5,108,139 | 4,965,088 unknowns remain |
| E504 plus corner-fan choice 2 | 5,108,139 | Pool conflict |
| E504 with **all height-zero gamma anchors integral** | 71,114,343 | Pool conflict; extra coordinate restriction is essential |
| q=4 hexagon, heights 0,1 | 870,547,980 | **INCOMPLETE**, stopped at 45 seconds |
| q=4 hexagon, heights -1,0 | 870,547,980 | **INCOMPLETE**, stopped at 45 seconds |

The two q=4 hexagon runs stopped with 428,781,524 and 393,109,617
positions respectively; they were not continued into SAT. The E504
pool was not submitted wholesale to a large solver. The q=2 CP-SAT
run exhausted its budget during preprocessing. Its total time including
model parsing was about 44.8 seconds; no search result is promoted to a
mathematical impossibility assertion.

The small JSON records in `reports/` preserve the original statuses,
counts and run times. Large temporary placement lists, model text and
partial propagation logs are not needed as evidence of a theorem and
are not included. `trace_records` records the number of propagation
events, even when trace-file output was disabled; it does not promise
an accompanying replay certificate.

## Exact candidate geometry and its audit

`bitmap_fan.cpp` extends the earlier convex-target bitmap code to the
nonconvex fan residues. Simply testing three vertices against all
polygon half-planes would have been wrong here. Instead:

1. Candidate triangles must lie in the convex hull of the residual.
2. The interiors of the already filled fan/grid triangles are forbidden
   convex obstacles.
3. A separating-axis test excludes exactly the candidate triangles
   whose interiors overlap an obstacle; touching its boundary is allowed.

For a translated candidate triangle `anchor+t` and an obstacle P,
the strict-overlap test is a finite list of integer linear inequalities
in the anchor. For each candidate edge `p -> p+d`, it requires

```
cross(d,anchor) < max_{z in P} cross(d,z-p).
```

For each obstacle edge `p -> p+d`, it requires

```
cross(d,anchor) > cross(d,p)-max_{z in t} cross(d,z).
```

At fixed y their conjunction is an integer x interval, so it can be
removed from a bitmap without visiting every placement. Strict
integer inequalities are converted using an offset of one.

`check_candidate_geometry.py` compares this filter against independently
implemented exact rational polygon clipping for 3000 deterministic
random examples across q=1,2,4, including 395 positive-area intersections.
All comparisons and template metric checks passed. This audits the
new candidate-obstacle geometry; it is not a complete audit of every
search run or a proof of tiling existence.

A positive control used a three-fold ordinary (16,5,19) triangle.
The full candidate pool of 6224 positions reduces to exactly the nine
ordinary-grid placements, without a conflict.

## Programs and reproduction

```
g++ -std=c++17 -O3 bitmap_fan.cpp -o /tmp/fan-bitmap
g++ -std=c++17 -O3 packed_fan.cpp -o /tmp/fan-packed
g++ -std=c++17 -O3 compress_fan.cpp -o /tmp/fan-compress
python check_candidate_geometry.py
```

The bitmap arguments are

```
L U prefix seconds save_trace control_scale family_q target_mode [integral_height_zero]
```

Modes 0,1,2 select the hexagon, fan pentagon and equilateral of side ab.
Positive `control_scale` instead selects an ordinary triangle grid.
For example, the small positive control is

```
/tmp/fan-bitmap 0 1 /tmp/fan-control 30 0 3 2 0
```

`packed_fan.cpp` reads the surviving positions and applies ordinary
zero/one endpoint row bounds. Its optional arguments are a seed file,
geometric-overlap flag, family q, and target mode. `compress_fan.cpp`
joins exactly equal variables and exports the remaining Boolean model.
`solve_compressed.py` uses OR-Tools when available, optionally via
`ERDOS_ORTOOLS_PATH`; a positive solver response would still require a
separate exact geometric certificate check. None occurred here.

`equilateral_corner_seeds.py` reads an equilateral pool and lists its
available two-tile alpha/beta corner fans. The three saved E504 choices
are in `reports/fan_q4_equilateral.corner_fans.json`.

No conclusion in this directory assumes that every tiling has few
direction classes, a fixed fan, integral height-zero anchors, or the
macro topology of an earlier construction.
