# A reflected 120-degree corner: primitive F3 for b<a<=2b

## The positive theorem

Let positive integers `a,b,c` satisfy

```
b<a<=2b,    c²=a²+ab+b².
```

For every positive integer `m`, the F3 triangle with sides

```
m(c², c(a+2b), 3b(a+b))
```

can be tiled by `3(a+b)(a+2b)m²` congruent `(a,b,c)` triangles.
Primitivity is unnecessary. This is an ordered F3 statement: it does
not automatically give the different F3 target obtained by interchanging
the labels a,b. Nor does it supply an F2 tiling by itself.

It suffices to prove multiplier one; quadratic subdivision gives every
positive integer multiplier. The generator also implements the grids
directly at each multiplier.

## 1. A general reflected-gamma-corner lemma

Let R have sides a,b meeting at angle 120 degrees. Let L,t be positive
integers. An L-fold R triangle admits removal of a reflected t-fold R
triangle from its 120-degree corner whenever

```
L>=a+b,    t<=min(a,b).
```

The remaining polygon has a positive tiling by `L²-t²` original tiles.

To see this, let u,v be the unit-grid edge vectors of lengths a,b with
angle 120 degrees. The large triangle is `[0,Lu,Lv]`. Inside its ordinary
quadratic grid, take the parallelogram

```
P={s*u+r*v: 0<=s<=b, 0<=r<=a}.
```

It lies inside the large triangle since `a+b<=L`. Both its physical side
lengths are ab. Its b-by-a array of two-tile cells can therefore be
replaced by the a-by-b array with edge steps

```
u'=(b/a)u,    v'=(a/b)v.
```

These are lengths b,a at the same 120-degree angle, so their two cell
halves are congruent copies of R. The reflected triangular corner
`[0,t*u',t*v']` is exactly a triangular portion of this second grid,
because t fits both array dimensions. Delete its `t²` tiles. Every other
unit triangle remains intact. This proves the lemma.

There is a useful larger-rectangle version. Positive integers p,q work
whenever

```
bp+aq<=L,    t<=min(ap,bq).
```

Use the common parallelogram with standard-grid dimensions bp by aq,
or swapped-grid dimensions ap by bq. Thus one such common rectangle
works if and only if

```
L >= b*ceil(t/a)+a*ceil(t/b).
```

This characterizes that rectangle-interchange recipe, not arbitrary
reflected-corner tilings.

## 2. A different positive F3 partition

Use `rho=exp(i*pi/3)` and write

```
S=c²,    h=a+2b,    ell=2a+b,    delta=a-b,    Z=a+b*rho.
```

The canonical F3 vertices and auxiliary points are

```
X=0,    Y=S,    I=aZ,    J=Z²,
T=(ah/S)Z²,    K=(h/S)Z³,
J'=a(1+rho)Z.
```

The target is triangle XYK. As in the established
[F2/F3 bridge](../group2-trapezoids/BALANCED_F4.md), T lies on YK,
triangle XTK is an h-fold tile, and J lies on XT. The new point J'
also lies on YK. Direct multiplication in `rho²=rho-1` gives

```
YJ'=S,    YT=b*ell,    YK=3b(a+b),
IJ=bc,    IJ'=ac,
JT=b*delta,    TJ'=a*delta,    JJ'=c*delta.
```

Here each unbolded segment notation denotes its positive length. The
points I,J,J' are collinear in that order. Moreover

```
YJ'-YT = S-b*ell = a*delta >0,
YK-YJ' = 3b(a+b)-S = 2b²+2ab-a² >0.
```

The final inequality follows from `a<=2b`; it is at least `2b²` when
`a=2b`, and the quadratic expression is no smaller on b<a<=2b.
Thus the order on the target side is Y,T,J',K.

The three triangles

```
XYI,    YIJ',    XIJ
```

are all c-fold copies of the original tile. Their interiors are disjoint.
One way to see the whole partition without signed areas is to start from
the established positive partition of XYT into XYI, XIJ, and the
quadrilateral YIJT. The larger triangle YIJ' is exactly YIJT together
with triangle TJJ': J lies on IJ' and T lies on YJ', so this is an ordinary
triangle with its corner cut off.

The triangle TJJ' lies inside the attached h-fold triangle TXK: J lies
on TX, J' lies on TK, and both distances from T are smaller than the
corresponding full side lengths. It is a reflected delta-fold tile at
the 120-degree corner T. Consequently the target XYK is the disjoint
union of those three c-fold triangles and

```
triangle TXK minus triangle TJJ'.
```

This positive partition differs from the earlier beta-corner transfer.
It does not assume that the earlier quadrilateral Q can be tiled.

## 3. Fill the reflected 120-degree corner

Apply the lemma with `L=h=a+2b` and `t=delta=a-b`. Its hypotheses follow
from

```
h>a+b,    0<delta<=b<a.
```

The remainder of TXK therefore has `h²-delta²` tiles. Including the three
c-fold grids, the target has

```
3c²+h²-delta²
  =3(a²+ab+b²)+(a+2b)²-(a-b)²
  =3(a+b)(a+2b)
```

tiles. This proves the theorem.

At multiplier m, replace all coordinates by their m-fold multiples.
The three triangular grids have scale mc. The common parallelogram in
the mh-fold triangle has standard-grid dimensions mb by ma and swapped
dimensions ma by mb; the removed corner has scale m delta. All counts
are multiplied by m².

## 4. Exact example and verification

For `(a,b,c)=(5,3,7)`, one has `h=11`, `delta=2`. The three c-fold
triangles have 147 tiles in total. The gamma-corner remainder has
`11²-2²=117`. Thus the target with sides

```
(49,77,72)
```

has **264** tiles at multiplier one.

The full certificate `f3-264.json` was checked independently in exact
rational coordinates for tile congruence, target containment, all 34,716
tile pairs, and exact total area. The exported coordinate-free
`disk-264.json` also passes the disk verifier. These are internal
independent checks, not external peer review.

This example has `bc=21<a²=25`. It therefore also proves that the
nonnegative-width condition from the beta-corner rectangle construction
is not necessary for F3 tileability.

## 5. Exact boundary of the single-short-direction-class construction

The exchanged-label F3 target is not claimed by the positive theorem.
For the ordered target, the range `a>2b` has a precise obstruction to
this gamma construction using just one class of short-edge directions.
This restriction allows all six rotations by multiples of 60 degrees,
both reflections, arbitrary translates, and T-junctions. It is stronger
than merely allowing the two orientations in the displayed rectangle
interchange.

Here the negative assertion is for a **primitive triple at multiplier
one**. The positive assertion above still needs neither restriction.
The following argument does not exclude a tiling with multiple classes
of short-edge directions, or a different F3 macro partition.

Use affine coordinates along the two physical axes at the gamma corner,
with one affine unit having physical length one. The large triangle and
the reflected corner have vertices

```
outer: (0,0), (ha,0), (0,hb),
hole:  (0,0), (delta*b,0), (0,delta*a).
```

The hole is contained precisely when `delta*a<=hb`, since its other
axis intercept always fits. In the integer parameter range equality is
impossible; the condition is `a/b<1+sqrt(3)`. If it fails, the displayed
macro partition itself is not positive. Suppose therefore that the
hole is contained. Its complement Q is a convex quadrilateral. Its
axis side on the y-axis has length

```
E=hb-delta*a=2ab+2b²-a².                              (5.1)
```

First consider any filling whose short edges belong to the three axes
obtained from these axes by rotations through multiples of 60 degrees.
No c-edge is parallel to any of those short axes. The boundary side of
length E must therefore be a concatenation of whole tile sides of
length a or b. Whole sides, not merely their atomic seam subdivisions,
are involved: a tile side on a convex polygon's supporting boundary
line cannot extend beyond that boundary segment. Consequently

```
E in <a,b> = {Aa+Bb: A,B are nonnegative integers}.   (5.2)
```

Primitivity gives `gcd(a,b)=1`. Also b>1: when b=1 and a>1,
`a²<a²+a+1<(a+1)²` precludes integral c. Write

```
a=q*b+r,    0<r<b.
```

If `E=Aa+Bb`, reduction modulo b gives `A=-a (mod b)`, so the least
possible nonnegative A is b-r. But

```
E-a(b-r)=b[(1-q)a+2b].                               (5.3)
```

For a>2b one has q>=2, and the right side is strictly negative. Thus
E is smaller than even the least possible a-contribution to (5.2), a
contradiction. This rules out every such filling, without any assumption
on the internal seams or their pairing.

In fact the conclusion excludes **any one common short-direction
class**, even a class initially rotated away from the target axes.
To make this precise put `theta=arg(a+b*rho)` and consider directions
modulo pi/3. The two short sides of a tile are in one class phi; its
long side is in class `phi+theta` or `phi-theta`, according to chirality.
The number theta/pi is irrational: if it were rational,
`2*cos(theta)=(2a+b)/c` would be both a rational algebraic integer and
strictly between 1 and 2. In particular the classes n*theta are distinct.

The four sides of Q use all three classes `0,theta,-theta`. If all
tiles had short class phi, the axis side forces
`phi in {0,theta,-theta}`. The choice phi=theta cannot supply the
boundary class -theta, and phi=-theta cannot supply theta. Hence
phi=0, reducing to the preceding boundary argument.

Conversely, the positive construction uses exactly this single short
class whenever b<a<2b. The equality a=2b cannot occur for an integer
triple, since it would give c²=7b². We have therefore proved an exact
restricted classification: for primitive triples with b<a, the
geometrically defined gamma remainder at multiplier one has a tiling
with a single short-direction class **if and only if a<2b**.

For `(24,11,31)`, h=46 and delta=13, the hole is contained, but

```
E=46*11-13*24=194.
```

Any representation `194=24A+11B` would require `A=9 (mod 11)`, while
`9*24=216>194`. Thus no single-class filler exists. If any arbitrary
filler of this gamma remainder exists, at least one whole c-edge must
lie on this boundary side, and additional short-direction classes are
necessary. The boundary length alone permits this:
`194=2*31+12*11`. That equality is only a necessary boundary inventory,
not a geometric construction.

The independently retained `4830-two-axis-report.json` replays the exact
boundary arithmetic. This does not exclude the full F3 count 4830, a
gamma filling with more direction classes, or a different positive
macro partition.
