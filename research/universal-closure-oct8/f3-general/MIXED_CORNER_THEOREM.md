# A mixed-direction corner theorem: 4830 and a larger primitive F3 sector

## The constructive theorem

Let positive integers `a,b,c` satisfy `c²=a²+ab+b²` and `a>2b`. Put

```
D=b²+2ab−a².
```

If there are nonnegative integers `A,B` and a positive integer `q` such
that

```
D = q c + A a + B b,                                    (1)
```

then the ordered F3 triangle with sides

```
c², c(a+2b), 3b(a+b)
```

has a tiling by `3(a+b)(a+2b)` congruent `(a,b,c)` triangles. Subdivision
supplies every positive integer multiplier. Primitivity is not needed
for this sufficient geometric theorem.

For `(a,b,c)=(24,11,31)`, equation (1) reads

```
73 = 2·31 + 11.
```

Thus **4830 is realizable**, with tile `(24,11,31)` and target sides
`(961,1155,1426)`. Every `4830m²`, including `m=1`, is consequently
realizable. This result closes this count and square class; it does not
claim the full Erdős 634 classification.

The [independent arithmetic argument](../global/F3_UNIFORM_CONE.md)
proves (1) for every primitive norm triple in `2<a/b<2725/1139`. Combined
with the existing constructions for `0<a/b<2`, this gives every
multiplier of ordered F3 throughout `0<a/b<2725/1139` (approximately
2.3924495). For a nonprimitive triple `g(a0,b0,c0)`, multiply each
coefficient in a primitive witness (1) by g; this gives (1) directly
for the nonprimitive triple. (The equality `a=2b`
cannot hold in an integer norm triple.) See that arithmetic note for
its explicit finite verification and exact semigroup input; the
geometric proof below only assumes (1).

## Coordinates and the five positive regions

Use physical unit axes meeting at 120 degrees. A point `(x,y)` in this
section corresponds to Eisenstein coordinates `(x−y,y)`; its squared
Euclidean length is `x²−xy+y²`.

Put

```
k=a−2b,   r=D−qc=Aa+Bb.
```

Since `r>=0` and `q>=1`, one has `D>0`, hence
`2b<a<(1+sqrt(2))b`. In particular the positive gamma partition and
the [corner transport identity](CORNER_REDUCTION.md) apply. They reduce
the F3 construction to the quadrilateral

```
Q=[(bk,0),(2ab,0),(0,2b²),(0,ak)],
```

namely a `2b`-fold ordinary triangle with a reflected `k`-fold corner
removed. Its unit-tile area is `4b²−k²=a(4b−a)`.

Set

```
G=(ab,0),       H=(ab,ak),
F=(ab,b²),     E=(ab,b²−qc)=(ab,ak+r),
C=(0,2b²),     C1=(0,2b²−qc),
V=(0,b²−qc)=(0,ak+r),
J=(0,ak),      A0=(bk,0),     B0=(2ab,0).
```

Partition Q into these five regions:

| Region | Vertices in 120-degree axes | Unit count |
| --- | --- | ---: |
| Rotated parallelogram | C,C1,E,F | `2qc` |
| Right triangle | F,G,B0 | `b²` |
| Upper triangle | C1,V,E | `b²` |
| Middle strip | V,J,H,E | `2r` |
| Cut rectangle | J,A0,G,H | `2ak−k²` |

If `r=0`, omit the zero-area strip. Positivity and coverage are directly
visible from the cuts `x=ab` and `y=ak`, and from `b²−qc=ak+r>=ak`.
For `0<=x<=ab`, the outer sloping boundary is
`y=2b²−(b/a)x`; the rotated parallelogram is precisely the strip of
vertical thickness `qc` below that boundary. Its lower edge joins C1
to E, above `y=ak`. The upper triangle and middle strip fill everything
between this edge and `y=ak`. The cut rectangle fills the lower part
outside the removed corner. The right triangle fills `ab<=x<=2ab`.
Thus no signed pieces or unproved disjointness assertions are used.

The two displayed triangles are ordinary `b`-fold grids. For the middle
strip, split its height `r=Aa+Bb` into A strips of height a and B strips
of height b. Its width ab is divisible by both a and b. Each strip is
an array of two-tile parallelograms and the total is `2r`.

The cut rectangle is the `[0,ab]×[0,ak]` rectangle in the reflected grid
with horizontal step b and vertical step a. It contains `2ak` unit
triangles. Delete its `k`-fold corner at the origin; `k<a` ensures this
corner is contained. It removes exactly `k²` whole tiles.

## The rotated parallelogram

Only this piece uses another short-edge direction class. Return to
Eisenstein coordinates, put `rho=exp(i*pi/3)`, and let

```
z=(a+b*rho)/c.
```

The parallelogram has adjacent vectors

```
q c rho^(-1),     b c conjugate(z).
```

Subdivide them into q steps `u=c rho^(-1)` and c steps
`v=b conjugate(z)`. Then

```
|u|=c,   |v|=b,
u−v = a conjugate(z) rho^(-1),   |u−v|=a.
```

Every small cell therefore splits along the u−v diagonal into two
original tiles. There are `qc` cells, giving `2qc` tiles. Their short
edges have level −1 relative to the surrounding grids. This explicit
construction is the entire mixed-direction input; it requires no
position search or normal-form assumption.

The five counts sum to

```
2qc+2b²+2r+2ak−k²
 =2qc+2b²+2(b²−ak−qc)+2ak−k²
 =4b²−k².
```

This tiles Q. The corner transport and three c-fold triangles complete
the asserted F3 tiling.

## The short proof of 4830

For `(24,11,31)`, use `k=2`, `q=2`, `r=11`. The five residual counts are

```
124 + 121 + 121 + 22 + 92 = 480.
```

The pre-existing positive reduction contributes

```
3·31² + (24²+2·24·11) + 3·11²
 = 2883 + 1104 + 363 = 4350.
```

Adding the five explicit grids gives 4830, with no solver required to
reproduce the construction.

The positional search first located the useful 480-tile arrangement.
`construct_mixed_corner.py` now generates the five regions and their
unit triangles directly from `(a,b,c,q)`. Its `(24,11,31)` output has
exactly the same 480-triangle coordinate set as the search certificate;
this equality was checked using rational arithmetic. The full 4830
certificate passed a separate exact spatial geometry verifier, covering
all 11,662,035 pairs through a complete rational filter and 21,373
separating-axis checks. A third implementation independently checked
its full oriented boundary and every tile metric.

These are independent internal implementations, not external peer
review. The arithmetic condition (1) is sufficient, not necessary for
arbitrary F3 tilings. In particular, failure of (1) does not imply that
the target cannot be tiled. It fails for the primitive triple
`(2725,1139,3439)`, so the entire interval `2<a/b<1+sqrt(2)` is not
claimed by this criterion.

## Reproduction

From the repository root, the complete 4830 construction can be rebuilt
without reading any search output:

```bash
python research/universal-closure-oct8/f3-general/construct_f3_mixed.py
python research/group2-mixed-gamma/verify_spatial.py research/universal-closure-oct8/f3-general/f3_4830_macro.json
```

The independent general geometric audit is
[`GENERAL_CORNER_AUDIT.md`](../4830-position/GENERAL_CORNER_AUDIT.md).
Exact macro diagrams are available as
[`q480_five_regions.svg`](q480_five_regions.svg) and
[`f3_4830_macro.svg`](f3_4830_macro.svg).
