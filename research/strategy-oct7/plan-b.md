# Plan B: count-preserving parameter descent

7 October 2026. This is an arithmetic audit of a possible route to the
full classification, not a classification or a new tiling construction.

## 1. The exact same-count problem

For the ordered primitive F3 coefficient put

    s=a+b, t=a+2b, n=N/3.

At residual scale one the exact conditions are

    st=n, s<t<2s, gcd(s,t)=1,
    c²=t²−3st+3s².                                      (1)

The inverse is a=2s−t, b=t−s. Thus every same-count primitive F3
replacement, including either order of the short sides, occurs in this
divisor list. In particular the often tempting expression
`s²−st+t²` is not the correct norm in these variables.

Equivalently set

    X=3s²−n, Y=3s²c.

Then

    Y²=X³+n³.                                           (2)

Indeed the two sides are both `9s⁴c²`, after substituting (1).
The conditions that `s²=(X+n)/3` be an integer square, that `s|n`,
and that (1) hold remain essential. Rational points on (2), or elliptic
rank alone, therefore do not supply same-count primitive replacements.
No new theorem on all integral points of (2) is claimed.

The existing ordered gamma construction covers `b<a<=2b`. In these
variables its ratio condition is

    4/3 <= t/s < 3/2,
    2n/3 < s² <= 3n/4.                                 (3)

Testing for a replacement in that cone is a stricter divisor test; it
is not automatically true for a primitive F3 coefficient.

## 2. A complete same-count obstruction at 4830

**Proposition.** Every classified realization of N=4830, if one exists,
uses the F3 row at residual scale one with the ordered primitive tile
`(a,b,c)=(24,11,31)`.

The prior F3-only arithmetic theorem applies: `4830=14 mod16` and 5
has odd valuation and is inert for 2. Also

    4830=2*3*5*7*23

is squarefree. The integral necessary spectrum consequently forces
residual scale one, even if the primitive tile is changed.

For the same-count list (1), `n=1610=2*5*7*23` and

    sqrt(805)<s<sqrt(1610), hence 29<=s<=40.

The divisors of 1610 are

    1,2,5,7,10,14,23,35,46,70,115,161,230,322,805,1610.

Exactly one lies in that interval: s=35. It forces t=46 and then
`a=24,b=11,c=31`. This list includes all ordered positive possibilities;
swapping a and b is not a missing candidate. Since 24>2*11, the tile
is outside the existing ordered primitive gamma cone.

This excludes an unconditional procedure that sends **every arithmetic
F3 candidate** to another tile in that positive cone while preserving N.
It does not decide 4830 and does not refute a hypothetical theorem that
**every realizable** F3 count has a positive-cone replacement. Such a
theorem would need new geometry and would imply nonexistence at 4830.

For the infinite squarefree front

    a=h²−1, b=2h+1, c=h²+h+1, h=5 mod24,

the known squarefreeness result again forces residual scale one. Formula
(1) gives an exact way to examine alternate tiles, but no uniqueness
theorem for every member of this infinite family has been established.
The absence of collisions in bounded parameter experiments is not such
a theorem and is not used above.

## 3. F2 really embeds arithmetically in beta

For a primitive plus-norm tile let

    u=|a−b|, v=c.

Then

    (a+2b)(2a+b)=3c²−(a−b)²=3v²−u².                   (4)

Here `0<u<v` and `gcd(u,v)=1`, so these are legitimate primitive
Group-1 beta parameters. To check primitivity, a prime dividing
`a−b` and c also divides 3b²; coprimality of a,b leaves only 3.
But a primitive plus-norm triple has `3∤c`: otherwise its norm
modulo 3 forces a=b modulo 3, and the norm is 3 modulo 9 unless
both a and b are divisible by 3. Hence no prime divides the gcd.
Also a=b is impossible for a positive rational c, and
`c²−(a−b)²=3ab>0`.

Consequently every beta construction at residual scale m for the new
tile `(uv,v²−u²,v²)` is a count-preserving solution of the global
existence problem for that F2 count. This is a valid one-way transfer
of **known positive constructions**, not a dissection of the original
F2 target and not an equivalence of fixed-tile realizability.

The standard beta seed at scale v gives m=c here. This does not improve
the existing F2 tail. Indeed every primitive plus-norm triple has
`B=min(a,b)>=3`, `A=max(a,b)>=5` (check B=1,2 by consecutive squares,
and A<5 directly). Its existing sufficient threshold is

    ceil(3*(floor(A/B)+2)/2)
       <= ceil(A/2+3) <= A+1 <= c.

Thus (4) becomes useful for the remaining small scales only if new
beta constructions at those scales are first proved. The identity
does not independently close the F2 gap.

## 4. Assessment of this route

The exact divisor reduction is useful for certifying that an individual
candidate has no alternative primitive F3 tile. It cannot by itself
replace the missing geometric theorem: 4830 already has only its
original hard tile. The F2/beta identity is a genuine overlap, but
currently transfers the small-scale difficulty to another unresolved
branch. For a two- or three-turn attempt at the full problem, parameter
descent should therefore be a supporting audit rather than the primary
breakthrough strategy.

The checker `check_plan_b.py` verifies the complete 4830 divisor list,
the exact transformations, the gamma-cone translation, and the F2
identity/primitivity/threshold bound on primitive parameter samples.
The universal algebra and the scope limits are proved above, rather
than inferred from the finite check.
