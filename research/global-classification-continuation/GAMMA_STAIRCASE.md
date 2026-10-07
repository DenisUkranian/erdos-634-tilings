# A common staircase fills every positive gamma corner at large scales

7 October 2026. This gives a new sufficient F3 construction. Its exact
scale predicate describes the stated construction, not arbitrary tilings.

## 1. Replace a common staircase, not its bounding rectangle

Let positive integers a>b and c satisfy `c²=a²+ab+b²`. Use affine
coordinates on two physical unit axes meeting at 120 degrees. Consider

    outer triangle: (0,0), (La,0), (0,Lb),
    reflected hole: (0,0), (tb,0), (0,ta),             (1)

where L,t are positive integers. On these axes define the closed cells

    C(i,j)=[ab*i,ab*(i+1)] × [ab*j,ab*(j+1)]

for nonnegative integers i,j. Each cell admits both the ordinary a-by-b
unit grid and the reflected b-by-a unit grid. Its sides are grid lines
in both grids; in either grid each little parallelogram is split into
two congruent `(a,b,c)` triangles.

Let P be the union of cells with

    ai+bj<t.                                        (2)

These are exactly the common cells whose interiors intersect the
reflected hole. The hole is contained in their closed union: for a point
in its interior, take i=floor(x/(ab)), j=floor(y/(ab)); then
`ai+bj<=x/b+y/a<t`. The boundary follows by closure.

A common cell lies in the outer triangle exactly when its far corner
does, namely

    b(i+1)+a(j+1)<=L.                               (3)

The maximum of the left side over (2) is exactly

    b+a*ceil(t/b).                                  (4)

Indeed (2) and a>b imply `i+j<=ceil(t/b)-1`, whence

    b(i+1)+a(j+1)
      =a+b+a(i+j)+(b-a)i <= b+a*ceil(t/b).

Equality is attained at `i=0, j=ceil(t/b)-1`.

It follows that P lies in the outer triangle if and only if

    b+a*ceil(t/b)<=L.                               (5)

When (5) holds, start with the ordinary quadratic tiling of the outer
triangle. Replace its grid on P by the reflected grid, and delete all
unit triangles in the reflected hole. Nothing is cut through a tile:
each common-cell side lies on both grids, and the t-scaled hole itself
is a union of exactly t² triangles in the reflected grid. This proves
a tiling of the remainder with L²-t² tiles. T-junctions along the
staircase are allowed.

This argument is independent of a primitive normalization. It is a
positive region replacement, with no signed pieces or overlaps.

## 2. Apply the staircase to the F3 macro partition

Put

    h=a+2b,  delta=a-b,  E=bh-a*delta=2ab+2b²-a².

At positive multiplier m the F3 target has sides

    m(c²,c(a+2b),3b(a+b))

and count `3(a+b)(a+2b)m²`. The
[gamma-corner macro partition](../group2-gamma-corners/PROOF.md),
Section 2, consists of three mc-scaled tile triangles and the
remainder (1) with `L=mh`, `t=m*delta`. Its order condition is E>0:
the reflected corner then has both intercepts strictly inside the
outer triangle, and the auxiliary point J' lies between T and K.
All the cited coordinate identities remain valid with a>2b when E>0.

Therefore the exact sufficient staircase test is

    S(m):=b+a*ceil(m*delta/b)-mh <= 0.                (6)

Feasibility itself implies E>0: from (6) and `ceil(x)>=x`,
`mE>=b²>0`. Thus no separate unproved geometry hypothesis is needed.
The resulting number of unit tiles is

    3(mc)²+(mh)²-(m*delta)²
      =3(a+b)(a+2b)m².                              (7)

## 3. Exact model spectrum and an every-integer tail

For positive integers m,n,

    S(m+n)<=S(m)+S(n)-b,                            (8)
    S(m+b)=S(m)-E.                                  (9)

The successful positive scales, together with 0 by convention, form
an additive submonoid. Notice that (6) at m=0 is not being applied;
the empty scale is merely the additive identity.

If E<=0, the lower bound `S(m)>=b-mE/b` makes every scale fail.
If E>0, `ceil(x)<x+1` already gives

    S(m)<a+b-mE/b.

Since m*delta is integral, the sharper bound
`b*ceil(m*delta/b)<=m*delta+b-1` gives

    b*S(m)<=b(a+b)-a-mE.

Hence every integer

    m>=ceil((b(a+b)-a)/E)                           (10)

is successful. Thus a staircase succeeds at some positive scale
if and only if the gamma macro partition is geometrically positive,
equivalently `1<a/b<1+sqrt(3)`.

For an exact finite description write `m=s+kb`, `1<=s<=b`, k>=0.
By (9), when E>0, condition (6) is equivalent to

    k>=max(0,ceil(S(s)/E)).                         (11)

This is an exact residue description of this construction. It is
stronger than the earlier common-rectangle recipe, whose unnecessary
bounding corner sometimes leaves the outer triangle.

## 4. A uniform half-integer aspect domain

**For every integer norm tile with `b<a<=5b/2`, the ordered F3 target
has a tiling at every integer multiplier m>=2.**

The earlier construction covers every m>=1 when a<=2b. Suppose
`2b<a<=5b/2`. At m=2, `ceil(2*delta/b)=3`, so

    S(2)=b+3a-2(a+2b)=a-3b<0.

At m=3, `ceil(3*delta/b)<=5`, so

    S(3)<=b+5a-3(a+2b)=2a-5b<=0.

Every integer at least 2 is a nonnegative combination of 2 and 3,
so (8) proves the assertion.

Throughout `2b<a<=5b/2` the exact nonnegative spectrum of this
staircase is `<2,3>={0,2,3,4,...}`, since

    S(1)=b+2a-(a+2b)=a-b>0.

The endpoint 5/2 is also sharp for this recipe's m=2: if a/b>5/2,
then `ceil(2*delta/b)>=4` and
`S(2)>=b+4a-2(a+2b)=2a-3b>0`.

These construction-specific failures do not prove nonexistence
of a different filling or a different tiling of the F3 target.

## 5. The entire class 4830 except its primitive member

For `(a,b,c)=(24,11,31)`, one has

    h=46, delta=13, E=194,
    ceil((b(a+b)-a)/E)=ceil(361/194)=2.

Consequently

    4830*m² is an actual tiling count for every m>=2. (12)

At m=2, the staircase consists of just four common cells:

    (0,0), (0,1), (0,2), (1,0).

The maximum corner cost is `b+3a=83<=L=92`. After swapping their
grids, remove the reflected corner of scale t=26. The gamma
remainder has `92²-26²=7788` tiles; the three ordinary triangles
have `3*62²=11532`, for total **19320**.

At m=1, `S(1)=13>0`, so this staircase fails. The original boundary
obstruction also forbids every single-short-direction-class filler
of that primitive gamma remainder. Neither statement excludes a
general tiling with count4830.

The exhaustive candidate enumerator from
`../uniform-reduction/candidates.py` leaves exactly one candidate
for each of 4830 and 19320: the same `(24,11,31)` tile in F3, at
scale1 or2, respectively. Thus (12) leaves **only the single integer
4830 unresolved in this whole square class**, rather than two
integers after the rectangle improvement or five after the older
tail bound6. It supplies no answer to the other isolated candidate154.

## 6. Verification boundary

The arithmetic checker in this directory verifies formulas (6)–(11),
the uniform ratio domain, and the finite candidate lists. The positive
proof is the grid replacement above; it is not inferred from finite
samples. A [separate constructor and independent exact verifier](../group2-mixed-gamma/README.md)
now retain all 19320 unit triangles in a compressed certificate. They
check congruence, containment, total area and every possible overlap by
a complete rational spatial filter and separating-axis tests. No all-N
classification or necessity of this macro partition is claimed.
