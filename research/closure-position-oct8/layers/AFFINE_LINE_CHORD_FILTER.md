# Exact supporting-line capacity inside the 154 target

8 October 2026. A necessary geometric filter, not a tiling certificate or an exclusion of 154.

The earlier population-13 proof retains the affine line supporting each short edge. This note adds the exact maximum chord of the target and permits all twelve orientations, with arbitrary signs. It rejects the five previously stored five-height formal inventories, but the full signed-direction recurrence supplies different inventories passing the stronger filter. Thus the five-height case remains open.

## The positioned geometric inequality

Use Eisenstein coordinates with `rho=exp(i*pi/3)`. The target has vertices

```
O=(0,0), P=(154,0), Q=(49,56).
```

For a nonzero short-edge height `h`, and a unit direction `d=rho^j z^h`, write `d=(x,y)` in Eisenstein coordinates. Its maximum parallel chord in the target has length

```
M(h,j) = 8624 / (max(0,-154y,56x-49y) - min(0,-154y,56x-49y)).
```

Indeed the three arguments of the maximum are the determinant projections of the vertices perpendicular to `d`. The physical width is their range times `sqrt(3)/2`. The area is `8624 sqrt(3)/4`. Parallel sections of a triangle have a piecewise-linear length profile, reaching their maximum on the line through the middle projected vertex. Consequently area is half the product of width and maximal chord. The displayed expression follows; `d` has unit norm. Every quantity in the displayed expression is rational, and the implementation uses exact fractions.

On a single affine line in this direction, count its height-h short edges as

```
v=(v_8+,v_8-,v_7+,v_7-).
```

The orientations are those of counterclockwise tile boundaries. A necessary condition is

```
8(v_8+ - v_8-) + 7(v_7+ - v_7-) = 0 (mod 13).
```

Every other edge on the same line is a whole length-13 edge; an exterior target side, if present at height `h=1` or `h=-1`, also has length divisible by 13. This whole-line identity allows partial contacts and T-junctions.

Edges with the same sign have disjoint relative interiors. Otherwise their tiles lie on the same side of an overlapping edge interval, and sufficiently small interior neighborhoods overlap. Hence

```
8v_8+ + 7v_7+ <= floor(M(h,j)),
8v_8- + 7v_7- <= floor(M(h,j)).
```

These bounds use the actual target. They do not assert that every line with these capacities occurs in a tiling.

## A finite upper bound on the number of lines

Every nonempty zero-sum multiset in the residues `(8,-8,7,-7)` modulo 13 splits into minimal nonempty zero-sum multisets. Each minimal multiset has size at most 13: among the consecutive prefix sums of a sequence of 14 elements in the cyclic group of order 13, a repeated residue supplies a proper zero-sum subsequence. The exact enumeration in `probe.py` gives 20 minimal multisets.

Fix total counts `v` across one whole direction family, an edge kind `t`, and the chord cap. The recurrence `max_lines(v,t,cap)` splits `v` into these minimal multisets, retaining only those whose positive and negative bank lengths satisfy the cap, and maximizes the number of pieces containing kind `t`.

This is an **upper bound** on the number of actual affine lines carrying kind `t`. Decomposing each actual line into minimal pieces preserves its counts and never decreases the number of pieces containing that kind. Each piece individually satisfies the actual line's bank-length bounds. The recurrence may treat pieces from the same physical line as separate lines, which only enlarges its upper bound.

For an orientation occurring `n` times, its two short edges have different direction families and specified signed kinds. If the two line-count bounds are `L` and `K`, necessarily `n<=LK`: its gamma vertices lie at intersections of those two line families. An excess forces two equally oriented tiles to have the same gamma vertex and therefore coincide. This is the implemented contradiction.

## Exhaustive arithmetic and surviving controls

`probe.py` expands every unsigned orientation inventory compatible with each signed layer of the five earlier formal controls in `closure-position-oct7/oct8-structural/all_height_direction_probe.json`. Every old control has at least one layer whose entire set of unsigned expansions is rejected; the full record is `probe_report.json`.

`filtered_dp.py` adds this necessary filter to the complete three-direction recurrence. For each signed layer it enumerates cancelling antipodal pairs to obtain every unsigned inventory of a proposed population. If all such inventories fail, it tries the next admissible population, 26 larger; it does not silently retain the old minimum. The central height uses the separate base-aware filter in `../central/probe_central_24.py` and its proved floor 24. Other occupied heights have floor 26.

The reports `filtered_*.json` retain formal survivors. These are controls for the filter, **not placed triangles**. Nothing here proves that their separate line partitions can coexist, nor that their orientations can be positioned without overlap. The new test still loses the incidence between three line families and between different height levels.

To reproduce one full recurrence:

```sh
python research/closure-position-oct8/layers/filtered_dp.py --lo 0 --hi 4 --seconds 180 --output /tmp/filtered_0_4.json
```

A time or state cutoff returns `INCOMPLETE`. No cutoff is interpreted as impossibility. The mathematical purpose of this finite computation is to test whether these proved local geometric inequalities close the direction-support argument; the surviving controls answer that question negatively.

The chord formula, same-sign bank disjointness, and safe direction of the minimal-multiset upper bound were independently read and checked by the central-height workstream in this research session. This is internal verification, not external review.
