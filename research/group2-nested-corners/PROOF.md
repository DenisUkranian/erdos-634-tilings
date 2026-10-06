# Nested corner removal: a three-generator sufficient criterion

This extends the positive reflected-corner construction in
[BALANCED_F4.md](../group2-trapezoids/BALANCED_F4.md). Its extra freedom is
to tile a larger rectangle and remove a smaller triangular grid corner.
It is a sufficient construction theorem, not a classification of all F3
tilings or a complete solution of Erdős 634.

## 1. Construction theorem

Let positive integers `a>b` satisfy `c²=a²+ab+b²`, and let `m` be a
positive integer. If there is a positive integer `k` such that

```
kc >= m(a-b),
r0 = mbc-a²k belongs to <a,b,c>,
```

then all the targets below can be tiled by congruent `(a,b,c)` tiles:

| Family | Target side lengths | Tile count |
|---|---|---:|
| Reversed F4 | `m(ac,b(2a+b),c(a+b))` | `(2a+b)(a+b)m²` |
| F2 | `m(a(a+2b),b(2a+b),c²)` | `(a+2b)(2a+b)m²` |
| F3 | `m(c²,c(a+2b),3b(a+b))` | `3(a+b)(a+2b)m²` |
| F3, exchanged short-side labels | `m(c²,c(2a+b),3a(a+b))` | `3(a+b)(2a+b)m²` |

Here `<a,b,c>` means nonnegative integral combinations of the three
numbers. Primitivity is unnecessary for this sufficient theorem.

Write `r0=Aa+Bb+sc` with `A,B,s` nonnegative integers, and set

```
n=m(a-b),    q=n+s,    r=r0-sc=Aa+Bb.
```

Thus `q>=n`, `kc>=n`, and

```
r=mac-a²k-cq >=0.
```

The last inequality, together with `q>0`, gives `mc>ak`.

## 2. Exact positive partition

Work in complex coordinates `x+y*rho`, where `rho=exp(i*pi/3)`, and put
`z=(a+b*rho)/c`. The large triangle with vertices

```
F=0,    A0=mc²,    B0=mac*z
```

is an `mc`-fold tile. Introduce

```
E=akc,    C=qc*z,    D=E+C,
U=C+a²k*z,    V=E+a(mc-ak)*z.
```

The following identities locate all the pieces:

```
V=A0+((mc-ak)/(mc))(B0-A0),
B0-U=r*z,    V-D=r*z,
D-U=ak(c-a*z),    |c-a*z|=b.
```

Hence `E` lies on `FA0`, `C,U` lie on `FB0`, `V` lies on `A0B0`, and
`D` lies on `EV`. The large triangle is partitioned, with disjoint
interiors, into the parallelogram `FEDC`, the triangles `CDU` and
`EA0V`, and the parallelogram `UDVB`. Degenerate `UDVB` is omitted if
`r=0`. This is the same positive partition as in the existing corner
construction, with its formerly tied rectangle height now independent.

The low parallelogram has edge vectors `kc*u` and `q*v`, where

```
u=a,    v=a+b*rho.
```

Each elementary `u,v` cell splits along its length-`b` diagonal into
two original tiles. It has a `kc`-by-`q` grid. Because `kc>=n` and
`q>=n`, the triangular corner with vertices `0,n*u,n*v` is exactly
an `n`-fold triangular subgrid. Delete its `n²` tiles. Notice that the
deleted corner need not reach the top edge of the rectangle.

The two high triangles are ordinary grids with respective integer
scales `ak` and `mc-ak`. The last parallelogram has side lengths `abk`
and `r`, with angles 60 and 120 degrees. The identity

```
Re(conjugate(z)*(c-a*z))=b/2
```

checks that angle. Since `r=Aa+Bb`, its width splits into `A` strips
of width `a` and `B` strips of width `b`; its other side `abk` is
divisible by both short sides. Every strip is a rectangular array of
two-tile parallelograms. This gives `2kr` original tiles there.

The resulting tiled region is precisely the canonical reflected-corner
quadrilateral

```
Q = [na, mc², mac*z, nc*z].
```

Its count is

```
(2kcq-n²) + (ak)² + (mc-ak)² + 2k(mac-a²k-cq)
    = m²c²-n²
    = 3abm².
```

The established reversed-F4 attachment, F2 reflection bridge, and F3
attachment in the cited proof depend only on this Q, not on its internal
grid. They therefore give the asserted targets and counts.

Both F3 orientations follow. The F2 target is unchanged up to reflection
when `a,b` are interchanged. More explicitly, let `S=c²`, `h=a+2b`,
`ell=2a+b`, `Z=a+b*rho`, and `W=b+a*rho`. Its canonical third vertex is
`T=ma*h*Z²/S`. The reflection `w -> mS-conjugate(w)` exchanges the first
two vertices and sends T to `mb*ell*W²/S`, the swapped canonical F2
target. Apply the old F3 attachment there with scale `m*ell`, rather
than `m*h`. Its count is `h*ell*m²+ell²*m²=3(a+b)ell*m²`.

Equivalently, one can remove a larger reflected `q`-fold corner first,
when that larger corner fits the rectangle, and then fill back its
quadratic-grid annulus down to the desired `n`-fold corner. The direct
rectangle argument above is more general: it only needs `kc>=n`, not
`kc>=q`.

The `c` term in the semigroup condition is absorbed by the increased
rectangle height. It is **not** being filled as a width-`c` short-grid
strip, and no such strip tiling is assumed.

## 3. Primitive multiplier one and a uniform balanced family

At `m=1`, the stated construction criterion is equivalent to

```
bc-a² belongs to <a,b,c>.
```

Indeed `k=1` automatically satisfies `c>=a-b`. No `k>=2` can have
`bc-a²k>=0`, since `b<a` and `c<2a`. This equivalence concerns this
particular construction family only; failure does not exclude a tiling.

In particular, **if `a>b` and `c<=2b`, multiplier one works in all three
families, and hence every positive integer multiplier works.** Put

```
d=a+b-c>0.
```

Then

```
bc-a² = b*d + c*(2b-c),
```

with nonnegative coefficients. Equivalently, choose `k=1`, remove the
`n=a-b` corner, and take rectangle height `q=d>=n`. The sufficient
ratio range is

```
1 < a/b <= (sqrt(13)-1)/2.
```

The three-generator criterion is strictly wider than this clean ratio
range. For the primitive tile `(88,65,133)`, one has `133>2*65` but

```
bc-a²=901=5*88+3*65+2*133.
```

Thus `n=23`, `q=25`, `k=1`, and the actual short-strip width is
`635=5*88+3*65`. This supplies the same three multiplier-one targets.

A broader uniform result is proved in the
[ternary semigroup companion](../f3-descent-attempt/TERNARY_SEMIGROUP_TAIL.md): **every primitive
plus-norm tile with `1<a/b<=7/5` satisfies `bc-a² in <a,b,c>`.** Hence all
targets listed in Section 1, including both F3 orientations, have tilings
at multiplier one and at every positive integer multiplier. The general
residue-lattice estimate proves this for `b>=4900`; the complete
[240 retained integer witnesses](balanced-7-5-small-witnesses.json) cover
`b<4900`. The [read-only replay](check_balanced_7_5_small.py) independently
enumerates both reduced parameters and all eligible side pairs and checks
that their sets agree exactly. This proves the entire ratio interval,
without a remaining size qualification.

## 4. The tile (8,7,13)

For this tile,

```
n=1,    d=q=2,    k=1,
bc-a²=27=2*7+13,    r=14=2*7.
```

The low rectangle contributes `2*13*2-1=51` tiles, the high triangular
grids contribute `8²=64` and `5²=25`, and the high parallelogram contributes
`2*14=28`. Their sum is `168`.

The existing bridges therefore yield

| Family | Target sides | Count |
|---|---|---:|
| Reversed F4 | `(104,161,195)` | 345 |
| F2 | `(176,161,169)` | 506 |
| F3 | `(169,286,315)` | 990 |

This bypasses the unresolved 54-tile parallelogram from the earlier
fixed-height attempt. No claim about that parallelogram's own tileability
follows.

The generator `construct.py` emits every unit triangle in exact rational
Eisenstein coordinates. `f3-990.json` contains the 990-unit construction.
An independently implemented rational separating-axis checker verified
congruence, containment, all 489,555 pairs for interior disjointness, and
the exact area sum. A separately exported coordinate-free disk certificate
also passes the abstract-disk checker, including integer seam reconstruction,
exact development and the triangular boundary condition. It has 583 vertices,
1,572 atomic edges and 100 interior T-junctions. The two reports are
`f3-990-geometric-report.json` and `f3-990-disk-report.json`.

These are internal independent checks, not external peer review. They do
not replace the general positive partition argument above.
