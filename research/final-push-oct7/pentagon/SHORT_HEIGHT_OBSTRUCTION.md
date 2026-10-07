# The fan remainder needs additional short heights

This note concerns the positive F3 fan and hexagon reduction in
[`../f3/FAN_HEXAGON.md`](../f3/FAN_HEXAGON.md). It neither excludes an F3
count nor constructs a tiling of the remainder.

Let `a>b>0`, `c²=a²+ab+b²`, and let all three sides be integers. Write
`rho=exp(i*pi/3)`, `Z=a+b*rho`, and `z=Z/c`. Coordinates below are in the
basis `(1,rho)`. A tile of **short height zero** is a rotation by a power
of `rho` of either the tile `(0,a,Z)` or its reflection. Half turns and
reflections are allowed.

The two orbits of long-edge directions `rho^j Z` and `rho^j conjugate(Z)`
are disjoint from one another and from the short-edge directions. Indeed,
`0<arg(Z)<pi/6`; the only possible equality between the two long orbits
would force `2 arg(Z)` to be a multiple of `pi/3`, which it is not.
Thus the long-edge signed currents determine the signed orientation
counts independently.

## Pentagon obstruction

After a rigid motion, the fan remainder is `bP`, where

```
P = [(a-b,-2a-b), (-b,-a), (0,0), (-a-b,a), (a-b,a+2b)].
```

Its counterclockwise boundary has the long-edge vectors

```
-2b Z,  -b rho² Z,  -b rho conjugate(Z),  -b rho² conjugate(Z)
```

and the single short-edge vector `3b(a+b) rho`.

Use three signed rotation counts, identifying rotations differing by a
half turn with opposite signs. For direct tiles let these be `d0,d1,d2`;
for reflected tiles let them be `r0,r1,r2`. A direct tile has boundary
`a, b rho, -Z`. A counterclockwise reflected tile has boundary
`conjugate(Z), -b rho^-1, -a`.

Long-edge cancellation forces

```
(d0,d1,d2) = (2b,0,b),
(r0,r1,r2) = (0,-b,-b).
```

The resulting short-edge current in directions `(1,rho,rho²)` is

```
(2ab, ab+3b², 2ab),
```

whereas the required current is `(0,3ab+3b²,0)`. The difference is
`2ab(1,-1,1)`, which is nonzero as a **direction-resolved current**.
Although `1-rho+rho²=0` as vectors, this identity does not cancel
segments having distinct directions. Therefore `bP` has no tiling using
only short-height-zero tiles.

## Hexagon obstruction

The four additional positive macrotiles described in the fan reduction
leave a rigid copy of

```
H = b * [(a-b,-2a), (-b,-a), (0,-a),
         (0,0), (-a,a), (a-b,a)].
```

It has `N_H=2b(3a-2b)` tile areas. All six sides have short height zero.
Its clockwise direction-resolved boundary current is

```
(2ab,-2ab,2ab).
```

If a tiling used only short height zero, its vanishing long-edge boundary
would force every direct and reflected signed rotation count to vanish.
Its short-edge current would consequently vanish as well, a
contradiction. In particular, a subdivision into arbitrary `a` by `b`
parallelograms along the three short directions cannot work: every such
parallelogram has zero direction-resolved current. Periodic Fourier
tests that omit this current cannot establish the proposed filling.

## A positive two-height inventory still passes

The preceding obstruction does not persist at the level of unplaced
two-height inventories. In the ring
`Z[T,T^-1,X,X^-1]/(T³+1)`, put

```
P0 = a + bT - cX,
Q0 = -a + bT² + cX^-1,
D  = -b - (a-b)T + aT²,
R  = cT - cT².
```

Direct expansion gives

```
P0 D + Q0 X R = -2ab(1-T+T²),
```

the counterclockwise short current of `H`. Negative orientation
coefficients become positive counts after half turns. This produces
`2(a+c)` unplaced tiles, using short heights zero and one, and a half-turn
pair can increase the count by two without changing any signed current.

Every integer norm triple with `a>b>0` has `b>=3`: `b=1,2` are excluded
by factoring `(2c-2a-b)(2c+2a+b)=3b²`. Also `c<a+b` and `a>=b+1`, so

```
b(3a-2b) - (2a+b)
 = a(3b-2) - b(2b+1)
 >= b²-2 > 0.
```

Consequently `N_H>2(a+c)` and the parity agrees. Padding with half-turn
pairs gives exactly `N_H` positive unplaced orientation counts. This is
not a placement or a tiling certificate: it records the precise
limitation of the short-height obstruction.

No conclusion here forbids a different F3 partition, a filling using
more heights, or an alternative tiling of the original triangle.
