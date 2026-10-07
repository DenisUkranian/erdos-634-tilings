# Infinitely many positive gamma remainders have no filling

**Research directed by Denis Paliy, with ChatGPT assistance — 7 October 2026.**

This is a nonexistence theorem for the reflected-gamma-corner remainder,
allowing arbitrary tile directions, reflections and T-junctions. It does
**not** exclude the full F3 target, which could have a different partition.
The proof uses the classical theorem of Siegel on integral points. No
effective cutoff for the infinite sequence below is claimed.

## The geometric boundary test

Let `a>b>0` be a primitive integer norm triple,

    c²=a²+ab+b²,  h=a+2b,  delta=a-b.

In unit axes meeting at 120 degrees the gamma remainder is the convex
quadrilateral obtained from

    [(0,0),(ha,0),(0,hb)]

by removing the reflected corner

    [(0,0),(delta*b,0),(0,delta*a)].

It is geometrically positive precisely when

    E=hb-delta*a=2ab+2b²-a²>0.

One of its exterior sides has length E. In any tiling of a convex
polygon, each tile side lying on a supporting boundary line is a whole
side: it cannot extend past the boundary segment while the tile remains
contained. The exterior side is therefore a concatenation of whole sides.
Consequently a necessary condition, without any restriction on directions,
is

    E in <a,b,c> = {Aa+Bb+Cc : A,B,C are nonnegative integers}.       (1)

For `(a,b,c)=(35,13,43)`, the remainder is positive but E=23. This is
not in `<35,13,43>`: only 13 could occur, and it does not divide 23.
Thus this remainder has no filling by the tile, even with multiple
short-direction classes. The corresponding full F3 count 8784 is not
excluded: `8784=72²+60²` is a classical positive count.

## An infinite sequence of failures of (1)

Put

    r = 1 + (3/2)sqrt(2) + sqrt(3) + (1/2)sqrt(6).

Thus `6<r<7` and `r≈6.0781160225`. Take the infinitely many reduced
continued-fraction convergents `m/n<r`, omitting finitely many initial
ones so that `6<m/n<r`. They satisfy

    0 < r-m/n < 1/n².                                             (2)

Define

    a0=m²-n²,  b0=2mn+n²,  c0=m²+mn+n²,
    g=gcd(a0,b0,c0),  (a,b,c)=(a0,b0,c0)/g.

The norm identity is immediate. Also `g` is 1 or 3. Indeed
`gcd(a0,n)=1`, so g divides `2m+n`; reducing a0 modulo g shows that g
divides `3m²`, and `gcd(m,g)=1`. In particular the resulting triple is
primitive. The ratios a/b tend to `1+sqrt(3)` from below, so the gamma
remainder is positive and eventually a>2b.

For the unnormalized boundary expression one has

    E0=2a0*b0+2b0²-a0²
      =F(m,n)
      =-m⁴+4m³n+12m²n²+4mn³-n⁴,
    E=E0/g².                                                     (3)

Let `f(x)=F(x,1)`. Its root r is simple; f is positive immediately to
the left of r. On `6<=x<=7` its derivative has absolute value at most
612. Equations (2)--(3) give

    0<E0<612n²,   b0>13n²,
    0<E/b<612/(13g)<48.                                          (4)

If (1) holds, since b is the smallest side, it follows that

    A+B+C <48.                                                  (5)

Multiplying (1) by g² therefore puts (m,n) on one of finitely many
fixed affine curves

    F(m,n) = g[A(m²-n²)+B(2mn+n²)+C(m²+mn+n²)],                  (6)

where `g in {1,3}` and `A,B,C>=0`, `A+B+C<=47`.

Every curve (6) has only finitely many integer points. Here are the
details needed to apply the integral-point theorem safely. The leading
homogeneous form F is irreducible over Q and has four distinct complex
linear factors. To see irreducibility, r has degree four: its displayed
expression in the basis `1,sqrt(2),sqrt(3),sqrt(6)` is fixed by none of
the three nonidentity automorphisms of the biquadratic field. Moreover

    r+1/r=2+3sqrt(2),
    r⁴-4r³-12r²-4r+1=0.

This degree-four polynomial is therefore the minimal polynomial, and its
roots are distinct in characteristic zero. Hence F is irreducible over
Q. A factorization over Q of the affine polynomial in (6) would factor
its leading homogeneous part, so the affine polynomial too is
irreducible over Q.

If this polynomial is absolutely irreducible, its projective closure
meets the line at infinity at the four distinct roots of F. These
points are nonsingular: the gradient of the simple leading binary form
is nonzero there. They remain four distinct missing points on the
normalization. Siegel's theorem consequently makes its integral points
finite, irrespective of its genus.

If it is not absolutely irreducible, its distinct geometric components
are conjugate. A rational point belongs to every conjugate of any
component containing it; in particular it lies in the intersection of
two distinct components. Such an intersection is finite by Bezout.
Thus the rational, and hence integral, points are finite in this case
as well.

There are only finitely many curves (6). Consequently only finitely
many members of the infinite convergent sequence can satisfy (1).
All remaining members are **positive gamma remainders with no tiling**
by the corresponding primitive tile. They approach the geometric
positivity boundary `a/b=1+sqrt(3)`.

### Arbitrarily many initial multipliers are excluded

There is a stronger uniform conclusion. Fix any positive integer K.
For all sufficiently late members of this same convergent sequence,
none of the homothetic gamma remainders at multipliers `t=1,...,K`
can be filled by unit copies of its primitive tile.

Indeed its short exterior side would have length tE, so a filling
requires `tE=Aa+Bb+Cc`. Now (4) gives `A+B+C<48K`, and the analogue
of (6) is

    tF(m,n)=g[Aa0+Bb0+Cc0],   1<=t<=K.

This is still a finite list of curves. Multiplying the leading form by
the nonzero integer t does not change its irreducibility or its four
distinct roots at infinity. The preceding finiteness proof applies
verbatim. Therefore no fixed upper bound on the multiplier can make
this gamma construction work for every primitive tile in its positive
geometric range, even when arbitrary directions are admitted.

For illustration, exact finite checks give the following first
multiplier for which the necessary boundary semigroup condition holds:

| Primitive tile | E | First t with tE in `<a,b,c>` |
| --- | ---: | ---: |
| (35,13,43) | 23 | 3 |
| (2024,741,2479) | 1154 | 37 |
| (101084920,36999651,123803239) | 819563042 | 131 |

These are necessary boundary thresholds, not tiling existence claims
at the listed multipliers. The next eight checked convergents have
no admissible boundary multiplier at most 200.

### The gamma remainder is not a necessary route to an F3 tiling

This conclusion can be combined with the existing positive F3 tail,
without a conjecture about small scales. All sufficiently late triples
above have

    2<a/b<1+sqrt(3)<3.

The established [all-norm tail](../../docs/square-class-tails.md),
Appendix A, constructs their ordered F3 targets for every integer

    t >= ceil(3*(floor(a/b)+2)/2) = 6.

Fix any t>=6 and apply the preceding negative result with K=t. It
follows that infinitely many of these primitive tiles have **an actual
F3 tiling at multiplier t**, whereas their gamma remainder at the very
same multiplier has **no tiling by that tile in any directions**. Thus
requiring the gamma remainder to be fillable is not a necessary condition
for F3 tiling existence, even inside the positive geometric domain of
this macro partition. The construction remains a sufficient route only.

There is a concrete instance independent of Siegel's theorem. For
`(a,b,c)=(2024,741,2479)` the gamma remainder is positive and E=1154.
At t=6 its short exterior side has length 6924. If

    6924 = 2024A + 741B + 2479C,

then C can only be 0, 1 or 2. Reduction modulo 741 forces the least
nonnegative A in these three cases to be respectively 453, 283 or 113.
Each already gives `2024A > 6924-2479C`, so no representation exists.
On the other hand the positive F3 tail just cited gives the full target
at t=6, with `3(a+b)(a+2b)*6²=1046961720` tiles. This is an application
of the existing general construction, not an expanded billion-tile
coordinate certificate. It supplies an explicit counterexample to the
proposed necessity of the gamma macro partition.

The dependence on Siegel is an explicit classical input; it is not a
new proof of that theorem. Its relevant formulation is stated in the
primary research source P. Corvaja and U. Zannier, *On integral points on
surfaces*, Annals of Mathematics 160 (2004), 705--726:
<https://annals.math.princeton.edu/2004/160-2/p09>.

## Why this does not settle 4830

For `(24,11,31)`, E=194 does satisfy (1). There is even a concrete
one-side collar inside the smaller quadrilateral left after removing
the 31-fold triangle from the gamma remainder. In Eisenstein
coordinates `x+y*rho`, `rho=exp(i*pi/3)`, that quadrilateral is

    [(0,0),(194,0),(506,143),(242,528)].

Eight tiles cover its first side in the sequence

    31,31,31,31,24,24,11,11.

The third vertices for the first four tiles are

    ((121+961j)/31,264/31), j=0,1,2,3,

and those for the last four are respectively

    (113,11), (137,11), (148,24), (159,24).

They are exactly congruent, contained, and interior-disjoint. Each of the
seven intervening straight-boundary fans can be filled by one additional
tile; the resulting 15-tile patch is checked by `check_boundary.py`.
These tiles use additional short-direction classes. Their existence
demonstrates that the short-side boundary inventory is geometrically
realizable, not merely a formal length equation. The rest of the
quadrilateral remains unfilled; no 4830-tile certificate follows.
