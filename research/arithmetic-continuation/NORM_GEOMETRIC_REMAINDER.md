# Only O(sqrt X) norm-family candidates remain below constructive tails

6 October 2026. This is a quantitative reduction, not a membership
classification or a new tiling construction. All constructive thresholds
are prior inputs from `docs/square-class-tails.md`, Appendix A. In
particular, the positive transfers there retain their Harries/Zhang
attribution.

## Statement

For each of the seven norm rows, use its primitive ordered integer tile
`(a,b,c)`, its necessary count `N=D t^2`, and the following established
every-integer sufficient threshold. Put `R=max(a,b)/min(a,b)`.

| Row | D | Sufficient threshold T |
| --- | --- | --- |
| 60-degree equilateral | ab, c²=a²−ab+b² | 3(floor(R)+1) |
| 120-degree equilateral | ab, c²=a²+ab+b² | 3(floor(R)+2) |
| F1 | b(a+b), plus norm | 3(floor(R)+2) |
| Isosceles | b(a+2b), plus norm | 3(floor(R)+2) |
| F2 | (a+2b)(2a+b), plus norm | ceil(3(floor(R)+2)/2) |
| F3 | 3(a+2b)(a+b), plus norm | ceil(3(floor(R)+2)/2) |
| F4 | (2a+b)(a+b), plus norm | 3(floor(R)+2) |

Exclude the classical equilateral tile `(1,1,1)` from the minus-norm row.
Let `U_norm(X)` count the distinct integers at most X which have any
necessary norm-row representation with `1 <= t < T`. Then

    U_norm(X) = O(sqrt X).

In fact, the number of representations `(row,a,b,c,t)` with these
properties is `O(sqrt X)`. Thus every norm-family candidate not already
proved admissible by these fixed-tile tails belongs to a set of this
size. The set being counted can contain admissible integers; being below
a sufficient threshold never proves nonexistence.

The former unconditional count of all seven norm-row arithmetic
candidates was `O(sqrt X log X)`. The improvement removes the logarithm
from the *geometrically undecided tail remainder*. It does not assert
an `O(sqrt X)` upper bound for all norm-family tiling counts.

## Plus-norm parameter bound

Every primitive positive ordered plus-norm triple has the unique reduced
rational parameter

    h/k=(c-a)/b,  gcd(h,k)=1,  k/2<h<k,
    a=(k²−h²)/g,
    b=k(2h−k)/g,
    c=(h²−hk+k²)/g,
    g in {1,3}.

This parametrization and the gcd assertion are proved in
`docs/fixed-prime-support.md`, Section 3. Put

    d=k−h,  e=2h−k,  delta=min(d,e).

Then `d,e>=1`, `k=2d+e`, and

    a=d(2k−d)/g,   b=ke/g.

Both numerators defining a and b are at most k². On the other hand,
both a and b are at least `k delta/g`. Consequently

    R <= k/delta.                                      (1)

Also `max(d,e)>=k/3`, `2k−d>=k`, and `g²<=9`, giving

    ab = k d e (2k−d)/g² >= k³ delta/27.               (2)

For each fixed k and delta there are at most two possible pairs (d,e):
either `d=delta`, or `e=delta` and `d=(k−delta)/2`. Discarding gcd,
integrality and sign restrictions in the estimates only enlarges the
candidate set.

Every plus-row coefficient D is at least ab, and every threshold in the
table is at most `3R+6 <= 9R`. Therefore a subthreshold representation
`D t²<=X` necessarily satisfies

    delta < 9k/t,  delta <= 27X/(t²k³).                (3)

For a fixed t, the number of primitive parameter pairs is thus at most

    2 sum_{k>=1} min(9k/t, 27X/(t²k³)).                (4)

## The minus norm

For a nonclassical primitive minus-norm triple, exchange a and b if
necessary to have a>b, and set

    A=a−b,  B=b.

Then `A,B>0`, `gcd(A,B)=1`, and

    c²=A²+AB+B²,  ab=B(A+B)>=AB.

If `R_+=max(A,B)/min(A,B)`, then

    a/b=1+A/B <= 1+R_+,
    T_60 <= 3(a/b)+3 <= 3R_++6 <= 9R_+.

The same plus-norm parameter argument applies with `(A,B)` in place
of `(a,b)`. Each ordered plus pair produces at most the two original
minus-side orders. Thus the minus row obeys (4) up to a fixed factor.
If a=b, primitivity gives a=b=c=1, the classical case already removed.

## Summation

For positive A,B with `K=(B/A)^(1/4)>=1`, splitting a sum at K gives

    sum_{k>=1} min(Ak,B/k³) = O(sqrt(AB)).              (5)

Indeed the part up to K is `O(AK²)`, and the tail is `O(B/K²)`.
In (4), `A=9/t`, `B=27X/t²`, so the bound is

    O(sqrt X / t^(3/2)).                              (6)

Every representation has `t<=sqrt X` because D is a positive integer.
For X>=1 and such t, `K=(3X/t)^(1/4)>=1`, as required in (5).
Finally

    sum_{t>=1} t^(−3/2) < infinity.

Summing (6), then taking the finite union of the seven rows and the
minus-norm side orders, proves the stated `O(sqrt X)` estimate.

The proof is elementary once the existing constructive tails are
accepted. No analytic prime-distribution estimate, elliptic-rank
algorithm, unproved construction threshold, or geometric exclusion at
multiplier one is used. Independent finite enumeration in `check_norm_remainder.py`
checks the parameter inequalities and supplies scale examples; the
asymptotic theorem follows from the written bounds, not the examples.
