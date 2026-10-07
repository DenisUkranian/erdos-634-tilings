# Independent internal review of the fixed-class F3 density theorem

7 October 2026. Reviewed `F3_FIXED_CLASS_DENSITY.md` after its full proof
was written. The claims below pass this mathematical review, subject to
the stated prior necessary spectra and constructive-tail inputs. This
is project-internal review, not external refereeing or formal verification.

## 1. Elliptic map and injective height bound

Write V=a+b, U=a+2b=V+b. Then

    U c² = (V+b)(V²−Vb+b²) = V³+b³.

The displayed ordinate in the source equals

    Y=3d² s c/V²,

since 3UV=ds². Therefore

    Y²=27d³ U c²/V³=27d³(1+b³/V³)=X³+(3d)³.

All denominators are nonzero because a,b,s are positive. Primitivity
gives gcd(b,V)=1, so X/(3d)=b/V uniquely recovers the ordered primitive
pair (a,b). The positive c and s are then unique. Thus bounding rational
points bounds primitive ordered triples, and also the set of distinct s.
No bounded-fibre assertion is being substituted for the actual injection.

The rational-coordinate height is at most 3dV, and V<s sqrt(d/3).
Consequently log H(X)<=log s+O_d(1). Canonical-height comparison and
positive definiteness on the Mordell–Weil lattice give the stated
O_d((1+log X)^(r_d/2)) count. Torsion translates contribute a finite
factor only; rank zero creates no exception to the upper-bound argument.
The proof does not require computing a basis or knowing the rank
numerically. It also does not claim that positive rank forces an odd s.

I separately inspected the cited primary source, J. S. Milne,
*Elliptic Curves*, second edition, Chapter IV, Section 4, Theorem 4.7
and the height discussion, and Section 6, Theorem 6.1:
<https://www.jmilne.org/math/Books/EC2.pdf>.
It supplies the asserted height properties and positive-definite
quadratic form. The lattice counting estimate itself is elementary.

## 2. Reciprocal sum and geometric threshold

Partial summation gives

    sum_{s>K}1/s = integral_K^infinity B_d(t)/t² dt − B_d(K)/K,

with the usual endpoint convention. Dropping the nonpositive final term
proves the upper bound used in the source. The resulting logarithmic
power divided by K is correct for every fixed nonnegative r_d.

For A=max(a,b), B=min(a,b), the integer

    e=2c−2A−B

is positive, since c²−(A+B/2)²=3B²/4>0. Thus e>=1. From

    3B²=e(2c+2A+B)>4A

one gets A/B<sqrt(3A/4). Combining A<a+b<s sqrt(d/3) proves the
square-root-in-s aspect-ratio bound, with its stated constant. The
bound holds in both ordered orientations.

The prior input `docs/square-class-tails.md`, Appendix A, explicitly
constructs F3 at every integer residual multiplier at least

    ceil(3(floor(A/B)+2)/2).

There is no parity or hidden divisibility restriction. The ceiling is
bounded by 3A/(2B)+4, giving precisely the sufficient threshold used in
the density proof. Minimizing over the finite witnesses for a fixed s
cannot weaken that upper bound.

## 3. The quantitative geometric remainder

If m belongs to the arithmetic envelope but not to the sufficient
construction set, every coefficient divisor s|m satisfies
m/s<tau_d(s). Counting all such representations can only overcount
the exceptional multipliers. For s<=L there are at most
kappa_d sqrt(s) possible residual scales. For s>L the number is at
most X/s. The source therefore legitimately obtains

    O_d(sqrt(L)(1+log L)^(r_d/2)
        +(X/L)(1+log L)^(r_d/2)).

The choice L=X^(2/3) gives X^(1/3), not X^(2/3), as the exponent in
the multiplier variable. The conversion to counts dm²<=Z gives
Z^(1/6), with constants allowed to depend on d. These estimates bound
unresolved candidates from above; they do not classify each of them
or declare any member impossible.

## 4. Natural density, odd normalization, and the order of limits

For a finite set of odd coefficient multipliers, the density among odd
integers of the multiples of a given lcm is 1/lcm. Hence the finite
inclusion–exclusion formula is exact with no missing factor two.

The infinite tail cannot initially be assigned its sum of densities
without justification. The source handles this correctly: a uniform
counting bound first gives twice the reciprocal tail in odd-relative
upper density. Split at a second finite cutoff J, apply the sharp
finite union bound to K<s<=J, and then let J tend to infinity. The
remaining doubled tail tends to zero. This proves the sharp tail
bound and the existence of the envelope's natural density. The
geometric remainder is o(X), so the actual and sufficient sets have
the same density by squeezing.

If a coefficient witness exists, every sufficiently large odd multiple
of that s is genuinely constructed, giving positive relative density
at least 1/s. If no coefficient exists the necessary spectrum makes
all three sets empty. No unproved equidistribution of elliptic points
or interchange of an uncontrolled infinite union with a limit is used.

## 5. Global class-38 consequence and computational scope

The earlier all-branch isolation in
`docs/infinite-minimal-multipliers.md`, Section 6, makes the F3 odd
sector identical to the global odd admissible sector in class 38.
The existing actual construction supplies positivity; 3|s for every
coefficient supplies the stated upper bound 1/3. These implications
do not invoke the candidate W/beta prime proof.

The final scope statement is necessary and accurate: finite coefficient
lists and finite inclusion–exclusion are effective, but the theorem's
unnumerical O_d constant does not by itself provide a certified decimal
density or a stopping rule at a prescribed numerical accuracy. Explicit
certified height/lattice bounds would be needed for that additional
computational claim. No such computation is claimed.

**Review outcome:** the written density theorem and quantitative
geometric-remainder bound pass this independent internal review. They
are substantive asymptotic results, not the missing all-N classification.

The accompanying `check_f3_height_density.py` was separately rerun after
the written review. All 174 primitive ordered norm triples in its stated
box and all four finite odd-density period checks passed. The finite
replay is supplementary to the infinite argument reviewed above.
