# Propagation from the 180-tile trapezoid and 240-tile equilateral seeds

8 October 2026. Research directed by Denis Paliy, with ChatGPT assistance.
This note gives constructive consequences of the preceding exact seed. It
is not a converse or a classification of all triangle tilings.

Use Eisenstein coordinates `(u,v) = u+v exp(i pi/3)` and write

```
T(x,L) = conv((0,0),(x+L,0),(x,L),(0,L)).
```

At `x=0` repeated vertices are removed, so `T(0,L)` is an equilateral
triangle. The tile throughout this note has sides `(3,5,7)` and area
`15 sqrt(3)/4`.

## Inputs and attribution

The new exact certificate tiles `T(30,30)` with 180 unit tiles and the
cyclic three-trapezoid assembly tiles `T(0,90)` with 540 unit tiles;
see [the construction and its independent audits](../../closure-position-oct8/equilateral-small/CONSTRUCTIONS.md).

The earlier symbolic shaving theorem gives the one-leg trapezoids

```
T(x,15),  x in {29,31,32} union {all integers >=34}.
```

These particular positive one-leg bases were already recorded by
Harries. Their formula proof is in
[the earlier trapezoid note](../../group2-trapezoids/PROOF.md).
A further exact certificate now tiles `T(0,60)` with 240 unit tiles; see
[`E60_0-1_certificate.json`](../equilateral-search/cpsat_count/E60_0-1_certificate.json)
and the separate [independent geometric audit](E60_independent_geometry.json).
All 28,680 unit-tile pairs passed exact interior-disjointness checks.

The short-grid strip operation and cyclic assembly are established
Zhang/Harries constructions. The new seed is the additional input here.

## Theorem

For every nonnegative integer x and positive integer n, the following are
sufficient conditions for a tiling of `T(x,15n)` by the original unit tile:

1. `n>=2` and `x>=29`;
2. `n>=4` and `x` belongs to `<3,5>`.

Here

```
<3,5> = {0,3,5,6} union {all integers >=8}.
```

In either case the number of unit tiles is exactly

```
n(2x+15n).
```

These conditions do not assert nonexistence outside their union. For
example the preceding one-leg family remains available at `n=1`.

## Two positive gluing operations

**Horizontal extension.** Suppose `T(x,L)` is tiled and `15` divides L.
If `d=3p+5q` with nonnegative integers p,q, then `T(x+d,L)` is tiled.
The complement of `T(x,L)` in the larger trapezoid is the parallelogram

```
(x+L,0), (x+d+L,0), (x+d,L), (x,L).
```

Its side vectors are `(d,0)` and `(-L,L)`. Split it into p strips of
width 3 and q strips of width 5. A width-3 strip is partitioned into
length-5 cells along `(-1,1)`; a width-5 strip is partitioned into
length-3 cells. Each cell splits across its long diagonal into two
`(3,5,7)` triangles. The divisibility by 15 makes every number of cells
an integer. There is no subtraction of a previously tiled region: the
explicit added parallelogram is filled by positive grids.

**Vertical stacking.** A translated `T(x,L)` above a `T(x+L,H)` gives
`T(x,L+H)`. Precisely, translate the first by `(0,H)` and leave the
second in its canonical position. Their common edge is the segment
from `(0,H)` to `(x+L,H)`. Their interiors are disjoint and the union
has the four stated outer vertices. This holds for arbitrary
nonnegative x and positive L,H.

## Proof of condition 1

For n=2, stack two known one-leg trapezoids whenever
`x in {29,31,32} union [34,infinity)`: their short bases are x and x+15,
and the latter is always at least 44. The missing base x=30 is exactly
the new seed; extending that seed by a width-3 strip gives x=33. Hence
all integer bases x>=29 work at n=2.

For n>2, put the resulting `T(x,30)` on top of
`T(x+30,15(n-2))`. The latter is a stack of one-leg trapezoids with
short bases `x+30, x+45, ..., x+15(n-1)`, all at least 59. Thus every
band has an old positive one-leg construction. Vertical stacking proves
the first assertion.

## Proof of condition 2

The new equilateral example is `T(0,60)`. For any `x in <3,5>`, its
horizontal extension gives `T(x,60)`. This proves n=4, including x=0.

For n>4 stack this trapezoid on top of
`T(x+60,15(n-4))`. All one-leg bases in the bottom stack are at least
60, so the old one-leg theorem fills it. The second assertion follows.

In particular, x=0 proves the full positive equilateral family
`N=15n^2` for every n>=4. Explicitly, the 240-tile side-60 triangle
translated by `(0,15)`, together with the old 135-tile `T(60,15)`,
forms a side-75 equilateral triangle with 375 tiles. Repetition adds
one known trapezoid band at each step. No search for 375 is needed.

The semigroup description follows from the initial elements 0,3,5,6
and the consecutive elements 8,9,10, since adding 3 preserves membership.
The integers 1,2,4,7 have no representation as `3p+5q`.

Finally, twice the coordinate determinant area of `T(x,L)` is
`L(2x+L)`, whereas that of the unit tile is 15. Substituting L=15n
gives the stated tile count. All constructions above are positive
partitions, so this area count is only bookkeeping, not a sufficiency
argument by itself. QED.

## Transfers to two further triangular shapes

Applying the standard equilateral-to-F1 and equilateral-to-I120
attachments to the previously established equilateral family gives,
for every integer m>=4, all four fixed-tile targets below:

| Shape and ordered short sides | Target side lengths | Unit count |
|---|---|---|
| F1, a=3,b=5 | m(15,35,40) | 40m^2 |
| F1, a=5,b=3 | m(15,21,24) | 24m^2 |
| I120, a=3,b=5 | m(35,35,65) | 65m^2 |
| I120, a=5,b=3 | m(21,21,33) | 33m^2 |

One ordinary bm-fold triangle is attached to the equilateral triangle
for F1; a second is attached for I120. These add b^2 m^2 tiles each.
The angle identity 60+120=180 straightens the boundary. The operation,
including its explicit target formula, is proved in
[the existing general-spectra note](../../general-spectra/PROOF.md),
in its final transfer paragraph. This is a direct consequence,
not a claim of a new attachment method or a sharp threshold.

## Remaining global obstruction

The seed supplies actual positive fillings in a new parameter region.
It does not imply that an arbitrary triangular tiling has a cyclic
three-trapezoid decomposition. Likewise it does not give a tile-preserving
transformation from arbitrary primitive sides to `(3,5,7)`. In
particular the uniquely ordered scale-one F3 candidate `(24,11,31)` for
4830 is untouched by these fixed-tile operations. No universal
small-scale geometric converse is established in this note.
