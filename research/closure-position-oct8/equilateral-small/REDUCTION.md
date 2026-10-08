# A focused attack on Zhang's small equilateral question

**Historical route and unsuccessful macrosearch record, 8 October 2026.**
The subsequent exact CP-SAT search found `T(30,30)`. The completed
[construction proof](CONSTRUCTIONS.md) and full unit certificates now
give equilateral tilings with 540, 735, and 960 tiles. The earlier
macrosearch timeouts below retain their original incomplete status.

## The precise published question

Yan X. Zhang, *Tiling Triangles with 2pi/3 Angles*,
[arXiv:2512.22696v4](https://arxiv.org/abs/2512.22696v4),
[PDF, Section 3.1, page 6](https://arxiv.org/pdf/2512.22696),
conjectures nonexistence of equilateral triangles of **side lengths**
`X=105` and `X=120` tiled by the fixed triangle `(3,5,7)`.
These are tile counts `735` and `960`, since `N=X²/15`.
They are not the counts 105 and 120.

The same section supplies constructions for `X=15m`, `m>=9`.
The cited lower bound `X<105` in Zhang should not be silently strengthened:
the inspected text of Beeson, *Tiling an Equilateral Triangle*,
[1812.07014v3](https://arxiv.org/html/1812.07014v3), explicitly discusses
an exclusion of *counts* `N<105`. We have not established the complete
chain supporting every smaller side length in Zhang's summary. This
does not affect the precise positive counterexample target `X=120`.

## Reduce a 960-tile triangle to a 315-tile trapezoid

Use Eisenstein coordinates `(u,v)` representing
`u+v/2 + i sqrt(3)v/2`. Define the ideal trapezoid

```
T(x,L) = [(0,0),(x+L,0),(x,L),(0,L)].
```

Its parallel sides have lengths `x+L,x`, its two legs have length `L`,
and its angles are 60,60,120,120 degrees. Its area in tile units is
`L(2x+L)/15` for the `(3,5,7)` tile.

**Conditional construction.** If `T(30,45)` is tiled by `(3,5,7)`, then
the equilateral triangle of side 120 has a 960-tiling.

Indeed, put `R(u,v)=(-u-v,u)`, rotation by 120 degrees. The following
three polygons form an exact partition of the equilateral triangle
`[(0,0),(120,0),(0,120)]`:

1. `(45,0) + T(30,45)`;
2. `(0,90) + R² T(45,45)`;
3. `(75,45) + R T(45,30)`.

Their tile counts are respectively `315,405,240`, summing to 960.
The last two are already positively constructed: stack bands of leg 15
whose short bases are 45,60,75 (or just 45,60). The seed
`T(29,15)` and semigroup extension from
[`group2-trapezoids/PROOF.md`](../../group2-trapezoids/PROOF.md)
apply because `45-29=16=2*3+2*5`, and further increments of 15 are in
`<3,5>`. Harries's prior one-leg classification is credited in that note.

The same cyclic partition with parameters `(2,2,3)` gives side 105 from
`T(30,45)`, `T(45,30)`, and `T(30,30)`. Their counts are 315,240,180.

This is a sufficient reduction, subsequently completed positively.
A negative answer for `T(30,45)` would not have excluded a different
tiling of the equilateral triangle.

## Why the one-leg obstruction does not settle this

Harries's manuscript (v0.5, 28 August 2026) classifies the one-leg
`T(x,15)` family as `x in {29,31,32} or x>=34`; its negative half has
the stated computational evidence boundary. In particular `T(30,15)`
does not tile. A tiling of `T(30,45)` need not respect the three bands
of leg 15, so the one-leg obstruction does not imply its impossibility.

## Search scope

`macro_probe.py` searches exact placements of positively known blocks:
ordinary triangular grids, the preceding ideal trapezoids, the known
88-tile F4 triangle, optionally grid parallelograms, and a 35-tile
nonconvex pentagon from the smaller-trapezoid construction. It handles
the pentagon by exact ear clipping for overlap predicates.

The pentagon has vertices `(5,3),(40,3),(35,0),(49,0),(25,15)`.
It consists of three positively tiled regions in the cited construction,
with counts 25,4,6. It must not be passed to a convex separating-axis
test without subdivision.

No bound on the number of these macroregions in an arbitrary tiling is
proved. Thus even a complete search of this library would establish only
a failure of the specified construction recipes.

The completed bounded runs all stopped at their time limits without a
construction. Their status is **INCOMPLETE**:

| Target | Maximum blocks | Library | Seconds | States |
| --- | ---: | --- | ---: | ---: |
| T(30,45) | 6 | 97 templates, no pentagon | 90 | 3897 |
| T(30,45) | 6 | 728 templates, with pentagon and parallelograms | 180 | 1504 |
| T(30,45) | 5 | 655 templates, each at least 20 tiles | 100 | 227 |
| T(30,45) | 4 | 98 templates, with pentagon | 120 | 4138 |
| T(30,30) | 5 | 46 templates, with pentagon | 90 | 7470 |

For example, from this directory:

```
python check_cyclic_reduction.py
python macro_probe.py --seconds 180 --max-macros 6 --parallelograms --output rerun.json
```

The first command verifies only the conditional three-trapezoid partition.
The second repeats a positive search whose outcome may depend on the
allocated time. Neither command supplies the missing trapezoid tiling.
