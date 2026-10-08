# A geometric counterexample to a proposed extreme-level lower bound

8 October 2026. Denis Paliy, research with ChatGPT assistance.

**Theorem.** An equilateral triangle of side 180 has a tiling by 2,160
congruent `(3,5,7)` triangles with short-edge height populations

```
(n_0,n_1,n_2) = (774,1372,14).
```

Thus a universal claim that every occupied extreme nonzero height
contains at least `c min(a,b)` tiles is **false even for actual equilateral
triangle tilings**: here `14 < 7*3=21`. It also refutes the stronger
candidate thresholds `bc=35` and `c(3c-2a-2b)=35` for this ordered tile.
The example does not settle the proposed 154 or 135 tilings.

## A small positive local trade

Use `rho=exp(i*pi/3)` and `z=(a+b rho)/c`, with
`c²=a²+ab+b²`. The parallelogram

```
P = [0, c, c+ac z, ac z]
```

has a tiling by `2c` triangles at short-edge height one: split its
second side into c vectors `az`, then split each of the c parallelogram
cells into the triangles `0,c,az` and their half-turns. The identity

```
c-az = b z rho^(-1)
```

shows that their side lengths are c,a,b.

In Eisenstein coordinates `ac z=(a²,ab)`. Attach the two ordinary
`a`-fold grid triangles

```
[(0,0),(a²,ab),(0,ab)],
[(c,0),(c+a²,0),(c+a²,ab)].
```

They each contain `a²` tiles at short-edge height zero. The resulting
union is exactly the parallelogram

```
[(0,0),(c+a²,0),(c+a²,ab),(0,ab)].                 (1)
```

This is a positive partition, with `2c+2a²` tiles. If
`c+a²` belongs to `<a,b>`, the same parallelogram has an all-height-zero
short-grid tiling: split its width into a- and b-width strips; its leg
ab is divisible by both short lengths. This is a genuine boundary-
preserving local exchange, not an inference from equal area alone.

For `(a,b,c)=(3,5,7)`, (1) has width 16 and leg 15, and contains
`14+18=32` tiles. Append a width-14 strip, where `14=5+3+3+3`.
The resulting width-30, leg-15 parallelogram has 60 tiles, of which
14 have height one and 46 have height zero.

The same width-30, leg-15 parallelogram also has an ordinary grid with
horizontal width-5 cells and leg-3 cells: it is a 6-by-5 cell rectangle.
All 60 triangles then have short-edge height zero and c-edge height
minus one. This second chirality is useful for embedding the exchange
at the highest occupied height of an existing tiling.

## Embedding in the new equilateral construction

Start with the independently verified 240-tile equilateral construction
and enlarge it by a factor of three, subdividing each enlarged tile into
nine original tiles. This gives an equilateral triangle of side 180,
with 2,160 tiles and populations `(774,1386)` at heights zero and one.

Its macroregion 11 in
[`MACRO_240_PROOF.md`](../equilateral240/MACRO_240_PROOF.md), previously
an ordinary 5-fold triangle, becomes an ordinary 15-fold triangle.
Its gamma vertex is

```
G=(225/7,900/7),
```

and its other vertices are `(0,525/7)` and `(0,1260/7)`. It is the
image under `w -> G+z w` of

```
[(0,0),(-75,0),(0,45)].
```

In this reference 15-fold grid, the parallelogram

```
[(-30,0),(0,0),(0,15),(-30,15)]
```

is exactly a 6-by-5 array of whole grid cells. It lies inside the
triangle because the two grid coordinates satisfy `0<=i<=6`,
`0<=j<=5`, and hence `i+j<=11<=15`.

Replace this array by the translated 60-tile trade above, and then apply
`w -> G+z w`. The removed triangles all have global short height one.
The replacement has 46 at global height one and 14 at global height
two. The boundary of the replaced region is unchanged. Thus the final
populations are exactly

```
774, 1386-60+46=1372, 14.
```

No tile outside the replaced parallelogram moves, and no third direction
class is assumed away.

## Exact certificate and independent geometric verification

`extreme_population_counterexample.py` reconstructs the full tiling
from the existing 240 seed and elementary grids. It outputs
`equilateral_2160_extreme14.json`, with integer numerators and denominator
49, plus the smaller replacement certificate `local_trade_60.json`.

The independent geometric checker from the preceding equilateral audit
verified all 6,480 side lengths, containment of every triangle, exact
area equality, and all **2,331,720 pairs**. Its report is
`equilateral_2160_extreme14_verified.json`. It imports none of the
construction routines. These are exact internal checks, not external
peer review.

## The corresponding obstruction to the proposed (8,7,13) bound

For `(a,b,c)=(8,7,13)`, the same trade has width `c+a²=77`, leg 56,
and `26+128=154` tiles. Its all-height-zero tiling uses `77=11*7`.
Append a width-35 strip to obtain width 112 and leg 56. The enlarged
parallelogram has 224 tiles: 26 at height one, and 198 at height zero.
Its alternate pure grid is a 16-by-7 array of width-7, leg-8 cells and
fits in an ordinary down-chirality triangle of any integer scale at
least 23.

The classical two-height equilateral construction for `(8,7,13)`
contains ordinary c-fold triangles of height one and c-edge height
zero. Subdivision by two makes these scale-26 triangles. Inserting the
trade in one such triangle therefore produces an actual larger
equilateral tiling whose unique top height has only 26 tiles. This is
a symbolic embedding argument; the full unit expansion supplied in this
folder is the `(3,5,7)` example above.

Consequently a general threshold `n_extreme>=91` cannot be used to
exclude 154. A bound specialized to the small 154 target would need a
separate global geometric argument.

## What this says about the diameter proposal

A c-fold original triangle has a side of length c², so it cannot fit
inside an equilateral triangle of side 45 when c=7. That eliminates
constructions which require such a block *inside* the target. It does
not prove that every possible tiling contains a c-fold block or a
straight c²-long chain.

The local trade above explains why an extreme-level count cannot supply
that missing extraction step by itself. General mixed-height cut chains
contain whole c-steps in two adjacent direction classes and generate a
lattice of index c, not c². The candidate statement that **every
nonsimilar triangular tiling** has diameter at least c² remains unproved
here; no counterexample to that particular triangular statement is
asserted. For arbitrary convex polygons it is plainly false, already
for a two-tile parallelogram of diameter c.
