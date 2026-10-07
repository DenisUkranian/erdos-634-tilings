# Exact single-class gamma filling at multiplier two

7 October 2026. Independent mathematical audit of the new staircase
construction and a matching restricted obstruction. This does not
classify unrestricted F3 tilings or all counts in problem 634.

Let `a>b>0`, `c²=a²+ab+b²`, and put

```
h=a+2b,   delta=a-b,   E=2ab+2b²-a².
```

The gamma remainder at multiplier m is the outer triangle with intercepts
`mha,mhb` on axes at angle 120 degrees, minus the reflected corner
triangle with intercepts `m delta b,m delta a`. It is a genuine convex
quadrilateral precisely when `E>0`, equivalently `a/b<1+sqrt(3)`.

A single short-direction class means that all short edges are parallel
to one common set of three axes separated by 60 degrees. It allows all
six rotations in that class, either chirality, and arbitrary T-junctions.

**Theorem.** For a primitive integral norm triple with `a>b` and `E>0`,
the gamma remainder at multiplier two has a single-short-class tiling
if and only if

```
a < 5b/2.                                             (1)
```

The constructive implication needs no primitivity. Primitivity is used
only for the converse. Equality in (1) is impossible for an integral
norm triple.

## Positive implication and independent geometric check

For `a<2b`, the earlier
[gamma theorem](../group2-gamma-corners/PROOF.md) gives even multiplier
one. Consider `2b<a<=5b/2` and multiplier two. Put `t=2(a-b)` and
`L=2(a+2b)`.

Use physical affine coordinates along the gamma axes. A common cell is

```
[iab,(i+1)ab] × [jab,(j+1)ab],       i,j>=0.
```

It is a `b`-by-`a` array of standard two-tile cells and an `a`-by-`b`
array of reflected two-tile cells. Its interior intersects the reflected
hole `x/b+y/a<t` exactly when `ai+bj<t`. In this ratio interval the
intersecting cells have precisely the four indices

```
(0,0), (0,1), (0,2), (1,0).
```

Every one lies in the outer standard triangle: its farthest vertex has
standard coordinate sum `b(i+1)+a(j+1)`, whose maximum is `b+3a`.
The inequality `b+3a<=L` follows from `a<=3b`.

Replace the original grids in these four common cells by their reflected
grids, then delete the reflected triangular hole. Cell boundaries are
grid lines in **both** global grids. The hole boundary follows reflected
grid lines and the prescribed unit-triangle diagonals, so its deletion
removes whole unit triangles, including in cells which meet only part
of the hole. The remaining unit triangles partition the remainder with
no overlaps. All short edges belong to the original axis class.

This is the multiplier-two instance of the staircase construction in
[the constructive continuation](../global-classification-continuation/GAMMA_STAIRCASE.md).
The above argument independently checks the delicate partial-cell issue.

## Necessary boundary inventory

The four genuine sides of the gamma remainder use direction classes
`0,theta,-theta` modulo `pi/3`, where `theta=arg(a+b rho)` and
`rho=exp(i*pi/3)`. The number `theta/pi` is irrational: otherwise the
rational number `2cos(theta)=(2a+b)/c`, strictly between 1 and 2, would
be an integer algebraic integer. Thus the classes `n theta` are distinct.

If a filling uses one short-direction class phi, its long edges have
class `phi+theta` or `phi-theta`. The three boundary classes force
`phi=0`: phi equal to either theta or minus theta cannot supply the
opposite class. This is the same argument used in the earlier
[single-class obstruction](../group2-gamma-corners/PROOF.md).

In particular no c-edge is parallel to a short axis. The axis side of
length `2E` is a union of whole a- and b-edges. Whole edges are essential
here: because the quadrilateral is convex, a tile side on a supporting
boundary line cannot extend beyond that genuine boundary side. Hence

```
2E = Aa+Bb,            A,B>=0 integers.                 (2)
```

Suppose now `a>5b/2`. The containment bound gives `a<3b`, so write

```
a=2b+r,             b/2<r<b.
```

Primitivity of the norm triple gives `gcd(a,b)=1`. Reducing (2) modulo b
and canceling a gives

```
A = -2a = -2r (mod b).
```

Since `b<2r<2b`, the least nonnegative possibility is `A=2b-2r>0`.
But direct expansion gives

```
2E-a(2b-2r) = 2b(2b-a) < 0.
```

Even this smallest possible a-contribution is longer than the entire
boundary side. This contradicts (2), proving necessity.

Finally, equality `a=5b/2` gives `a=5k,b=2k` and `c²=39k²`, impossible
for a positive integer c. The other endpoint `a=2b` similarly gives
`c²=7b²` and does not occur. This completes the theorem.

## Precise scope

For primitive triples with `2b<a<5b/2`, multiplier one has no single-class
gamma filling by the earlier obstruction, while multiplier two now does.
Thus the least multiplier for this **restricted gamma remainder** is
exactly two. This does not prove any lower bound for unrestricted F3
tilings: another short-direction class or another macro partition may
change the answer. In particular primitive 4830 remains undecided.
