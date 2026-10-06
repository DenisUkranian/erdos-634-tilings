# Internal audit of the F3 split-part reduction

6 October 2026. Separate mathematical review within the same project;
not external refereeing, formal verification, or a priority claim.

**Conclusion.** The original even-kernel, odd-multiplier theorem is
sound. Its proof extends to every squarefree `d>=1` and positive `m`,
with

    h = product of the full p-parts of m for p>3 with (3/p)=1,
    d_+ = gcd(d,2) product_{p|d, p>3, (3/p)=1} p.

The sufficient bound is `m>=8dh³` uniformly, sharpened to `m>=6dh³`
when `d>=2`. Passing the arithmetic test below the applicable bound
still does not prove existence.

## Necessity and reconstruction

Squarefreeness of d gives `t|m` in `dm²=3UWt²`, hence `s=m/t` is an
integer. Every odd prime divisor of `U=a+2b` is greater than 3 and
splits for 3: the norm equation reduces to `c²=3b²` at such a prime,
and primitivity prevents a zero denominator. The prime 3 is excluded
by the norm equation modulo 9.

If U is even, then a is even, b is odd, `8|a`, and `v_2(U)=1` while
W is odd. Thus `v_2(3UW)=1`, forcing d even and s odd. This proves
`U|d_+h²` for arbitrary m. The factor 2 must **not** be dropped when
m is even: `(d,m,a,b,c,s,t)=(110,6,8,7,13,3,2)` has U=22 and h=1.
Also s need not be odd in the generalized coefficient list:
`(a,b,c)=(5,3,7)` has coefficient `264=66*2²`.

The inequalities `U/2<W<U` give positive `a=2W−U`, `b=U−W`.
Their gcd is `gcd(U,W)=1`, and the square test is exactly
`c²=a²+ab+b²`. Thus the arithmetic test reconstructs a primitive
tile and a positive integral residual scale, without adding geometry.

## Sufficient threshold

For `A=max(a,b)`, `B=min(a,b)`, the positive integer
`q=2c−2A−B` satisfies `3B²=q(4A+2B+q)>4A`. Therefore
`A/B<sqrt(3U)/2`. Combining this with
`s<sqrt(3/d)U` and `U<=dh²` bounds `sM/2` strictly by

    (9/4)dh³ + 3sqrt(3d)h²,
    M=3(floor(A/B)+2).

After division by dh³, this is below 6 for d>=2 and below 8 for
d=1. The earlier every-integer F3 construction applies at
`t>=ceil(M/2)`. Since t=m/s is integral, no rounding or parity gap
occurs. The construction remains a cited dependency of the theorem.

## Class 38 and verification

For d=38 and h=1, d_+=2 makes `U|2` incompatible with `U>=3`.
This excludes F3 for every such multiplier. The **global** consequence
for `38m²` retains m odd: the other branches are excluded by
`docs/infinite-minimal-multipliers.md`, Section 6. Its alpha exclusion
uses `Q/2=7 mod 8` and the kernel factors 1,19; its QP exclusion uses
`(2/19)=(3/19)=-1`. No rank-zero assumption or candidate all-primes
theorem is needed. Even multipliers are not globally excluded here.

The generalized script passes 10,370 comparisons with direct
coefficient enumeration for squarefree kernels through 200, multipliers
through 99 and split part at most 13. The two parity examples above
are explicit regression checks. The output is
`split-part-verification.json`; it records `full_Erdos634_solved=false`.
These checks support the formulas; the universal result rests on the
proof, not on the finite ranges.
