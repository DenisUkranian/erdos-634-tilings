# Grid-block construction search for the 3431 and 5063 boards

20 November 2026. Exploratory construction work. **Neither target was tiled by this search.** No impossibility conclusion follows from a beam-search failure.

## Search space and exact arithmetic

The search grows a partition of the whole primitive F2 board. Its pieces are:

- A tile-similar triangle at a positive integer scale `k`, filled by its usual `k*k` grid.
- A parallelogram with `m` by `n` cells, each cell split into two copies of the tile. The program permits any pair of tile sides and either applicable cell diagonal; its area is `2*m*n` tiles.

Thus contacts may be proper T-junctions between blocks. The old obstruction to a *conforming* macrotriangle partition does not exclude this search space. Blocks can be placed in different direction heights and phases.

All coordinates during the construction are integers in units `1/c^5`. Directions are generated as `rho^j*z^h`, where `z=(a+b*rho)/c`, `rho=exp(i*pi/3)`. The code generates triangle templates with short heights `-4` through `4` and their long-edge headings through `-5` and `5`. This is a constructive restriction, not a theorem restricting every tiling. Norms and determinants use 128-bit integers. It tests board containment, separating axes for block interiors, physical integral offsets at collinear contacts, and necessary convex-corner angle and boundary-length conditions. Subtracting each block updates the remaining oriented boundary by exact endpoint events on its supporting lines.

The beam heuristic is deliberately not exhaustive: it retains finitely many states, may omit narrow parallelogram dimensions via `rectangle_tail`, and stops at a time or block budget. Its `NO IN THIS SEARCH` terminal line means only that the retained search did not produce a certificate. The optional diverse version preserves a separate beam for every first-block position and scale.

## A verified positive control

Starting only with tile `(5,3,7)` and its F2 board, the search found a partition into **14** grid blocks. Two independently scored searches gave two such partitions. The first consists of eight tile-similar triangles and six parallelograms. It expands to exactly 143 unit tiles.

`verify_macro.py` independently expands every positive block. It checks every unit triangle's three squared side lengths and its positive doubled axial area. It then checks equality of the sum of their oriented boundary chains to the outer triangle boundary, including all T-junction subdivisions. Because all triangle indicators are nonnegative, the chain equality proves one-fold coverage and absence of interior overlap by winding numbers. No search predicate is used in this verification.

```
python3 verify_macro.py control143_compact.txt 5 3 7 macro143_certificate.json
python3 verify_macro.py control143_perimeter.txt 5 3 7
```

Both calls pass. The known count 143 is only a control; it is not progress toward deciding the two target counts by itself.

## Exact obstruction to lifting this particular control topology

`lift_macro.py` keeps the 14-block incidence pattern, shared vertices, and its ten interior vertex-on-side contacts. It transfers every cell direction to the requested tile, introduces block origins and integer grid dimensions, and solves the resulting exact rational linear equations. Additional inequalities retain the incidences and board containment. This yields 48 scalar variables and exact rank 44 in each target case. The integer feasibility solver returned infeasible for both targets, but the following simpler exact argument proves the relevant obstruction without relying on that solver status.

Use the variable names printed by `inspect_lift.py`. In both cases the exact elimination includes

```
k2 = k3 = (A-y13)/c
k9 = b*k2/a
k12 = b*l13/a
k10 = (A-y13)/a-l13
k11 = b*l13/a-(a-b)
```

Here `A=a*(a+2*b)` is the vertical outer side, `y13>=0` is an actual block vertex ordinate, and all the displayed `k` and `l` grid dimensions must be positive integers. Coprimality of `a,b` forces `a` to divide both `k2` and `l13`.

For `(33,7,37)`, `k2<=1551/37<66`; for `(35,13,43)`, `k2<=2135/43<70`. In both cases `0<k2<2*a`, so `k2=a`. The equation for `k10` now reads `k10=c-l13`. Its positivity and `a<c<2*a` imply `l13=a`. Consequently the required parallelogram width is `k11=2*b-a`, equal to **-19** and **-9**, respectively. This contradicts positivity.

This excludes exactly the transferred 14-block topology, with arbitrary allowed integer dimensions and origins. It is not an obstruction to a different topology, to subdivisions that change its incidence pattern, or to the original unit board. A signed transfer with coincident unit placements cancelled gave worse negative counts than the earlier project constructions; it did not provide a completion.

## Commands and reproducibility

C++20 and Python 3 with SymPy, NumPy and SciPy are used. A positive certificate checker needs only Python's standard library.

```
g++ -O3 -std=c++20 beam_macro.cpp -o beam_macro
g++ -O2 -std=c++20 diverse_macro.cpp -o diverse_macro
./beam_macro 35 13 43 50 40 0 40 1500 1
./diverse_macro 35 13 43 60 40 0 8 40 1
python3 lift_macro.py control143_compact.txt 35 13 43 lifted5063
python3 inspect_lift.py control143_compact.txt 35 13 43 inspect5063
```

The executable arguments are `a b c seconds max_blocks corner_mode rectangle_tail beam_width score_style`. Corner mode 0 uses a smallest-candidate-count rule; mode 1 favors the largest available block area. Score styles 0, 1 and 2 favor filled area, remaining-region compactness, and perimeter plus boundary complexity, respectively. In the diverse program `beam_width` is per first-block group.

The exact boundary subtraction and corner geometry were developed from the project's earlier physical corner-search code. The block search, heuristic diversity, topology lifting, and separate certificate expansion in this directory are new exploratory implementations. The authoritative conclusion of this work remains: no positive coordinate certificate for 3431 or 5063 was obtained.
