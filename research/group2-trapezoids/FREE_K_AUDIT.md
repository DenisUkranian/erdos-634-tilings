# Independent audit of the free-k reflected-corner construction

3 October 2026. The symbolic construction and its positive grid recipes
pass this audit. This is a sufficient construction theorem, not a
necessary tiling criterion or a scale-one nonexistence proof.

The checked geometric statement is as follows. Let positive integers
`a>b` satisfy `c²=a²+ab+b²`, put `t=a−b`, and take positive integers
m,k. If

```
kc >= mt,
r = mbc−a²k belongs to <a,b>,
```

then the quadrilateral formed by deleting the reflected `mt`-fold
beta-corner triangle from the `mc`-fold tile is positively tiled by
`3abm²` unit tiles. The extra condition `mc>=ak` sometimes displayed
with the construction is redundant and is actually strict: `r>=0`
implies `a²k<=mbc<mac`, hence `ak<mc`.

## Partition and order

In the 60-degree oblique coordinates put `z=(a/c,b/c)` and

```
F=0, O=(mat,0), A=(mc²,0), B=mac z, C=mtc z,
E=(akc,0), D=E+C,
U=C+a²k z, V=E+a(mc−ak)z.
```

The target is the convex quadrilateral `OABC`. It is the outer triangle
`FAB` with `FOC` removed. These triangles have scales `mc` and `mt`,
and the adjacent a,c sides are swapped at their shared beta corner.

The relevant ordered incidences follow from the hypotheses:

- `O<=E<A` along the horizontal base because `kc>=mt` and `ak<mc`.
- `U` lies on `CB`, with `B−U=r z`.
- `V` lies strictly on `AB`, since
  `V=A+((mc−ak)/(mc))(B−A)` and the fraction is strictly between zero and one.
- `D` lies on `EV`, with `V−D=r z`.

Consequently the four regions `OEDC`, `CDU`, `EAV`, and `UBVD` have
disjoint interiors and cover `OABC`. The first or last can degenerate
as described below; that does not create a gap.

The middle triangles have scales `ak` and `mc−ak`. The final region is
a parallelogram with side vectors `r z` and `ak(c−az)`, of respective
lengths `r` and `abk`. Its angle is 60 degrees because

```
|c−az|=b,
Re(conj(z)(c−az))=b/2.
```

## Positive subdivisions and count

The low parallelogram `FEDC` uses the unit vectors
`u=(a,0)` and `v=(a,b)`. Their lengths are a,c and `|v−u|=b`, so
each u,v cell contains two original tiles. The full grid has `kc`
columns and `mt` rows. Its removed corner triangle has vertices
`0,mt u,mt v` and consists of exactly `(mt)²` whole unit triangles.
The inequality `kc>=mt` is precisely what makes that subtraction fit.

For the high parallelogram, write `r=Xa+Yb`. Its other side `abk`
is divisible by both a and b, so the usual short-edge strip tiling is
positive and contains `2kr` tiles.

The four counts are

```
2kcm t−m²t², (ak)², (mc−ak)², 2kr.
```

Their sum is

```
m²(c²−t²)=3abm².
```

No extra triangles, signed pieces, or enlarged target are introduced.

## Both degeneracies are valid

If `kc=mt`, then `O=E`. The low retained region becomes the other
half of a square array in the u,v basis, hence a triangle with
`(mt)²` unit tiles. Merge the repeated polygon vertex; do not reject
this valid case merely because a quadrilateral became a triangle.

If `r=0`, then `U=B` and `V=D`. The high parallelogram has no area
and no tiles and must simply be omitted. The other three regions
still give the stated coverage. The inequality `ak<mc` remains
strict, so the second high triangle does not disappear.

The exact audit fixtures include:

| Tile | m | k | r | `kc−mt` | Total tiles | Degeneracy |
|---|---:|---:|---:|---:|---:|---|
| (5,3,7) | 2 | 1 | 17 | 3 | 180 | none |
| (5,3,7) | 3 | 2 | 13 | 8 | 405 | none |
| (5,3,7) | 7 | 2 | 97 | 0 | 2205 | low region is triangular |
| (5,3,7) | 25 | 21 | 0 | 97 | 28125 | high parallelogram omitted |

## Uniform consequence for every m at least two

If `3c>=4a`, the construction works for every `m>=2`.

First, this norm inequality implies `a<2b`. If `a>=2b`, then
`9c²−16a²=−7a²+9ab+9b²` is at most its value at `a=2b`, namely
`−b²<0`, a contradiction.

The two valid parameter pairs are `(m,k)=(2,1)` and `(3,2)`:

```
r_(2,1)=(2b−a)a+2(c−a)b,
r_(3,2)=(4b−2a)a+(3c−4a)b.
```

All coefficients are nonnegative. For the fit inequalities,
`c>2(a−b)` follows from `c>a` and `a<2b`; likewise
`2c>3(a−b)` follows from `c>a` and `a<3b`.
Both seed remainders and both fit slacks are therefore strictly
positive.

Every `m>=2` is `2u+3v` for nonnegative u,v. Set `k=u+2v`.
Both `kc−mt` and r are then the corresponding nonnegative linear
combinations of their seed values; r remains in `<a,b>`.
An explicit choice is `k=ceil(m/2)`, using v=0 for even m and v=1
for odd m. This constructs a single quadrilateral at the desired
scale; it does not assume that smaller quadrilaterals can be glued.

The ratio range is

```
1 < a/b <= (9+sqrt(333))/14, approximately 1.9463.
```

The inequality is never equality for positive integer norm triples,
but its weak formulation causes no problem.

## Scale one remains a separate problem

Assume here that gcd(a,b)=1. At m=1, `ak<mc` and `c<2a` force k=1. Write `a=qb+s`, where
`q>=1` and `0<s<b` by coprimality. In a putative representation
`bc−a²=Xa+Yb`, the smallest nonnegative coefficient of a is
`X=(q+1)b−a`; it gives `Y=c−(q+1)a<0`. Larger congruent values of
X decrease Y further. Thus no primitive scale-one certificate exists
within this free-k construction. This calculation does not exclude
other tilings of the quadrilateral or of the attached triangle.

## Exact verification scope

`audit_free_k.py` independently implements the displayed coordinates;
it does not import the norm-completion constructor. It uses the
original rational polygon primitives from the package. It checks:

- congruence of both triangle blocks, the low and high unit-cell shapes,
  and the nonnegative grid recipes;
- the outer/removed triangle partition;
- convex containment, every pair of nondegenerate macroregions, and
  exact equality of the covered area;
- the uniform choice `k=ceil(m/2)` at m=2,3,4,5,7 for 184 distinct
  primitive triples in the inspected parameter range;
- the four explicit fixtures, including both degeneracies.

All 920 uniform instances and all four fixtures passed. The files
`certificates/free_k_macro_fixtures.json` and `free_k_audit_results.json` freeze
these results. This audit does not expand the unit tiles; separate
expanded certificates belong to the constructive companion campaign.
