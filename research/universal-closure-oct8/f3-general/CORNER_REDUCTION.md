# A smaller convex corner sufficient for primitive F3

**Scope of this note: a proved conditional reduction. The required
480-tile filling has since been constructed in
[MIXED_CORNER_THEOREM.md](MIXED_CORNER_THEOREM.md), completing 4830.
This reduction alone is not a classification of the remaining F3 sector.**

Let positive integers `a,b,c` satisfy `c²=a²+ab+b²` and

```
2b < a < (1+sqrt(3))b.
```

It suffices to tile one explicit convex quadrilateral, of only

```
a(4b−a)
```

unit tiles, in order to tile the ordered F3 target of sides
`(c²,c(a+2b),3b(a+b))`. For `(24,11,31)` this sufficient residual has
**480 tiles**, compared with the earlier reflected-beta quadrilateral
of 792 tiles. An impossibility result for this residual would exclude
only this construction.

## The general corner transport identity

Use physical coordinates along two unit axes meeting at 120 degrees.
Let `C(L,t)` be the ordinary `L`-fold `(a,b,c)` triangle

```
[0,(La,0),(0,Lb)]
```

with the reflected `t`-fold corner

```
[0,(tb,0),(0,ta)]
```

removed. Suppose

```
b<t<a,   L>=a+b,
```

and the removed triangle is strictly contained at the shared corner.
The ordinary tile grid has axis steps `a,b`. The first common cell
`[0,ab]×[0,ab]` is wholly contained because `L>=a+b`; it also has the
reflected grid with steps `b,a`.

The part of the reflected hole above this cell is, after translation
by `(0,ab)`, exactly a reflected `(t−b)`-fold triangle. The ordinary
outer triangle above the same horizontal line is an ordinary
`(L−a)`-fold triangle. Thus this upper residual is `C(L−a,t−b)`.

Everything else tiles explicitly. Outside the common cell and the
upper ordinary triangle, retain the original grid. Switch the common
cell to the reflected grid and delete the part of the reflected hole
lying in it. All cuts follow the relevant unit grids. Consequently,
a tiling of `C(L−a,t−b)` supplies a tiling of `C(L,t)`.

This statement is sufficient, not an equivalence for arbitrary tilings:
a tiling of the larger corner need not respect the prescribed cuts.

## F3 specialization

The established positive gamma partition gives three ordinary
`c`-fold grids and the corner

```
C(a+2b,a−b).
```

Its positivity is precisely `2ab+2b²−a²>0` in the present range. Apply
the transport identity with `L=a+2b`, `t=a−b`. The unresolved region
becomes

```
C(2b,a−2b).
```

It is convex: it is the intersection of the outer triangle with the
half-plane outside the corner cut. Its area, in unit-tile units, is

```
(2b)²−(a−2b)² = a(4b−a).
```

In Eisenstein coordinates of squared norm `x²+xy+y²`, with the physical
120-degree axes `1` and `rho²=rho−1`, its CCW vertices are

```
(b(a−2b),0), (2ab,0), (−2b²,2b²), (−a(a−2b),a(a−2b)).
```

The explicitly tiled portion has three counts:

```
3c²,
(a+2b)²−2ab−4b² = a²+2ab,
2ab−(a−b)²+(a−2b)² = 3b².
```

Together with the residual these sum to
`3(a+b)(a+2b)`. Thus the switched-cell portion always has exactly
`3b²` tiles, independently of `a`.

## The exact 4830 reduction

For `(a,b,c)=(24,11,31)`, the residual vertices are

```
(22,0), (528,0), (−242,242), (−48,48).
```

Its sides are `506,682,194,62`, its tile count is `480`, and its
remaining positive pieces contain

```
2883 + 1104 + 363 = 4350
```

tiles. `reduce_corner.py` deterministically writes all 4350 exact unit
triangles, the remaining quadrilateral, and the isometry embedding that
quadrilateral into the F3 target. It imports only the elementary grid
and coordinate functions from the earlier staircase constructor.

`check_reduction.py` imports no constructor. It checks every unit side
length, positive orientation, containment, the convex residual, both
area counts, and exact cancellation of all oriented boundaries. With
positive triangle and quadrilateral coefficients, zero boundary implies
multiplicity one in the target and zero outside, so this also proves
that the 4350 tiles and the remaining quadrilateral have disjoint
interiors and cover the target. No assumption of an overlap-free input
is made.

Reproduce from the repository root:

```bash
python research/universal-closure-oct8/f3-general/reduce_corner.py
python research/universal-closure-oct8/f3-general/check_reduction.py
```

The resulting `f3_4830_corner480_reduction.json` is deliberately labelled
`CONDITIONAL_REDUCTION_NOT_A_TILING`. Its checked SHA256 is
`f6ec1da5aeab9d3d52a4c17637d800d414520a6befb449ced8acaffbf3c78085`.

## Exact limit of the new two-c-layer trade

The local trade from the preceding turn generalizes as follows. For
any integer `q>=1`, the 60-degree parallelogram with side lengths

```
ab, a²+qc
```

can be tiled by `2(a²+qc)` original tiles. Take the parallelogram with
adjacent vectors `qc` and `ac*z`, where `z=(a+b*rho)/c`. Since
`c−az=bz*rho^(-1)`, a `q`-by-`c` array gives `2qc` tiles. Attach the two
ordinary `a`-fold triangles on its left and right. The union is exactly
`[0,a²+qc]×[0,ab]` in the 60-degree coordinate basis. Exchanging a,b
also yields side lengths `ab,b²+qc`. Nonnegative a/b-width strips may
be appended.

This positive statement does **not** make every `<a,b,c>`-width
parallelogram tileable: it carries the overhead `a²` or `b²`. Moreover,
for a primitive ordered `a>b` triple, the old scale-one free-corner
width is `r=bc−a²`, and

```
r < b(a+b)−a² = b²+a(b−a) < b².
```

Every new block has width at least `b²+c`. Therefore these blocks cannot
fill that old positive width; when `a>2b`, the old width is negative
already. All their widths also belong to the numerical semigroup
`<a,b,c>` already allowed by the nested-corner construction. They do
not enlarge that construction's parameter criterion. A universal F3
proof needs a different geometric arrangement, not substitution of this
trade into the existing free-corner remainder.

The corner transport above changes the arrangement and gives a smaller
concrete target. Its filling is now supplied by the companion
[MIXED_CORNER_THEOREM.md](MIXED_CORNER_THEOREM.md); that separate positive
construction is the step which completes 4830.
