# The three-row pentagon for 5063 cannot be tiled

Use the same Eisenstein frame and tile (35,13,43) as for the two-row pentagon. Let t=11, k=2, s=4 and j=3. In physical coordinates set X=(0,sc), Y=X+(0,tb), W=Y+(ta−kc,0), D=X+(ta,tb)−k(a²,ab)/c and V=(ab,b²)/c−(0,c). Use the five boundary points (0,(s−j)c), Y, W, D, D+jV. Its area equals t²−k²+2j(a−s)+j² = 312 tiles. Substituting j=2 gives the 245-tile pentagon.

## Direction and position bounds

The high/low cut at short height 0 and area of its two-edge exterior arc give n0≡t²≡35 modulo 43. The only other exceptional short height is 1, where n1≡312−35≡19 modulo 43. Everywhere else each occupied height costs at least 86 tiles. The allowance for other heights is at most 258. For these small regions a gap separating occupied heights from the two exterior heights is impossible, since a tail across a missing height would have positive area divisible by 43². Four intervals suffice, each containing 0 and 1 and three additional heights.

Apply the two valuation trees of the published phase-branch argument with z=(35+13ρ)/43. In the tree of increasing height choose the 43-adic root ρ≡37. In the tree of decreasing height take ρ≡7. At up to level 1 in the first tree, or down to level 0 in the second, the only possible subtree containing an exterior edge is the ball about zero. Both height-zero sides have integral vertices. The endpoints of the remaining exterior sides lie in zZ[ρ], since the first such endpoint (0,(s−j)c) does and consecutive displacements have integer lengths and height 1. Thus all relevant exterior nodes occur in the central branches at the exceptional heights. At other nodes the area argument counts a multiple of 43, and the signed line identity counts a signed multiple of 43. Because 2 is invertible modulo 43, positive- and negative-sign populations are separately multiples of 43. At an exceptional core node subtracting the other nodes gives the same two sign residues as for that entire height. A nonempty ordinary node costs at least 86 by the supporting-line exclusion of 43. An exterior-free ancestor of a used node cannot be empty within 312 tiles, since its subtree area would be a positive multiple of 43². Each distinct such node therefore costs at least 86.

The search checks these necessities after placing completed fans. For coordinates scaled by 43^H, two anchors have the same phase at height h when x+r y agrees modulo 43^(H+h) at the increasing prime, or 43^(H−h) at the decreasing prime. Here r is the chosen Hensel lift of ρ. A state stores the marked signs and occupied descendants in each visited ball. It checks the two valuation trees separately against every signed height inventory which remains possible. The positive 16-tile similar-triangle control returns YES.

| Height interval | Exact DFS nodes | Verdict |
|---|---:|---|
| [-3,1] | 330044 | NO |
| [-2,2] | 340375 | NO |
| [-1,3] | 340378 | NO |
| [0,4] | 313078 | NO |

This excludes the pentagon with arbitrary translations, reflections and non-edge-to-edge contacts. In the 5059-tile reference packing it contains 310 full reference triangles and one two-tile hole, with no reference triangle crossing its perimeter. Each of the 128 enumerated paired convex repair cavities of area at most 300 passing the orientation and boundary tests is contained inside this pentagon. For every one the part between the two perimeters is tiled by the reference placements. Filling one of these cavities would therefore fill the pentagon.

An unrestricted tiling of the full 5063-tile triangle may cross the pentagon boundary. Completing or ruling out that larger triangle requires a further argument.

## Convex hull replay

The reference data contain all 5059 exact congruent tiles, plus triangulations of the two hexagonal holes. The Python verifier checks every metric, verifies pairwise disjoint interiors by exact separating axes, checks containment, and accounts for the full board area. The translation between the holes is (−11180,13545) in the displayed coordinates of denominator 43.

For a repair use the same convex polygon C and its translate C+T. Both polygons must be contained in the board, have disjoint interiors and meet no reference triangle across their perimeters. Place the reference triangles and a copy translated by −T in one frame. Starting at the convex hull of the first hole, repeatedly add any triangle which crosses the current hull and take convex hulls until stable. To enlarge the current polygon, search every triangle sharing a positive-length boundary interval with the outside, add it and repeat closure. Every permissible larger C contains at least one such next triangle, since its additional area touches the interior of the previous polygon across a nontrivial interval. Monotonicity of closure keeps every intermediate hull inside C. This justifies exhaustiveness for the stated pair-of-convex-patches class.

There are exactly 506 geometric candidates of area at most 300. Requiring integral sums of 13,35,43 for every side length, valid boundary-character sums and locally admissible corner angle coefficients leaves 128. Any boundary is formed by reference-triangle or board sides, so its directions occur within the finite supplied direction list. The final wide corner test allows both acute-angle coefficients through six, the total available at an interior vertex. The one-, two- and three-row pentagons contain 66, 102 and 128 of these candidates, respectively. The standalone checker verifies the area of the actual preserved complement in every successful containment.

## Independent search

The original position-independent checker, with the same four short-height intervals but no valuation or phase pruning, was also launched. Its four searches were still running when this replay was packaged. They are independent corroboration in progress. The four completed outcomes in the table use the two-prime phase bounds. A separate compilation of the phase search with a fourfold similar triangle gives a positive control, and the two-row 245-tile case also has a complete position-independent exclusion.

## Sources and hypotheses

- [Original exposed-corner enumerator, exhaustive branching and positive controls](https://github.com/DenisUkranian/erdos-634-tilings/blob/aff4ab39ec4365fd72f29aab9f7beb04adc817f4/research/2026-11-20/semiprimes/continuation/patches/decision/PENTAGON_SWEEP.md)
- [Height and congruence arguments for pentagons](https://github.com/DenisUkranian/erdos-634-tilings/blob/aff4ab39ec4365fd72f29aab9f7beb04adc817f4/research/2026-11-20/semiprimes/continuation/patches/decision/SMALL_HEIGHT_BUDGETS.md)
- [Nodewise cancellation, signed line constraints and phase-tree bounds](https://github.com/DenisUkranian/erdos-634-tilings/blob/8d5517243cfbddb62e5b646fa78c7544189dbfb4/research/2026-11-20/semiprimes/continuation/phase-height/PHASE_BRANCHES.md)
- [Published reference-packing inputs](https://github.com/DenisUkranian/erdos-634-tilings/blob/aff4ab39ec4365fd72f29aab9f7beb04adc817f4/research/2026-11-20/semiprimes/continuation/packing/inventory_certificate.json)
