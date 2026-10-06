# F3 membership when the multiplier has a large nonsplit part

6 October 2026. This is an exact arithmetic sector obtained from the
previous F3 construction tail. It does not decide all small scales or
solve Erdős problem 634. The positive geometry and the exhaustive branch
classification remain the previously cited inputs; no new F3 dissection
is asserted here.

## 1. The split part of the multiplier

Let d be a positive squarefree integer, and let m be a positive integer.
Define

    h = product_{p | m, p>3, (3/p)=1} p^{v_p(m)},
    d_+ = gcd(d,2) product_{p | d, p>3, (3/p)=1} p.

Here `(3/p)` is the Legendre symbol. Thus h contains exactly the prime
power factors of m at primes congruent to 1, 11, 13 or 23 modulo 24.
The complementary factor m/h can involve arbitrarily many primes,
with arbitrary exponents, from

    P_- = {2,3} union {p prime: p=5,7,17,19 mod 24}.

No fixed finite support is imposed.
The factor 2 is included in d_+ whenever d is even, regardless of the
parity of m. An even m can contain a coefficient multiplier s which is
odd and a residual geometric scale m/s which is even.

Use the following finite arithmetic test A(d,m): there exist positive
integers U,W,s satisfying

    U | d_+ h²,   U/2 < W < U,   gcd(U,W)=1,
    3UW = d s²,   s | m,
    U²−3UW+3W² is an integer square.                 (1)

There are finitely many possibilities: enumerate divisors U of d_+h²
and integers W in the displayed interval. Alternatively enumerate s|m
and recover `W=ds²/(3U)` when integral. The first enumeration depends
only on d and h, before the final s|m check.

## 2. Exact large-nonsplit-part theorem

**Theorem.** Every primitive F3 realization of `N=dm²` implies A(d,m).
Conversely, if

    m >= 8 d h³,                                    (2)

then A(d,m) implies an actual F3 realization of `dm²`.
For every d>=2, the sharper sufficient bound `m>=6dh³` holds.

In particular, in any sector for which the existing exhaustive
classification forces every realization to belong to F3,

    dm² is admissible iff A(d,m), whenever (2) holds. (3)

Below the applicable sufficient bound, failure of A(d,m) still excludes
F3, but passing it is only a necessary arithmetic condition. No geometric
sufficiency at a small residual multiplier is inferred. The previous
case of even d and odd m is contained in the sharper d>=2 statement.

### Necessity and the bounded coefficient factor

The existing integral-scale F3 spectrum is

    dm² = 3(a+2b)(a+b)t²,
    c²=a²+ab+b²,  gcd(a,b)=1,  a,b,c,t positive integers.

Squarefreeness of d forces t|m. Put s=m/t, U=a+2b, W=a+b.
Then `3UW=ds²`, `gcd(U,W)=1`, and `U/2<W<U`.

We have `3 not dividing U`: if `a=b mod 3`, primitivity gives
`a=b=1 or 2 mod 3`; writing `a=b+3z` makes
`a²+ab+b²=3b²+9bz+9z²=3 mod 9`, a contradiction.

If an odd prime p>3 divides U, reduction of the norm equation gives

    c²=3b² mod p.

Primitivity gives p not dividing b or c, so `(3/p)=1`. No odd prime in
P_- can divide U; the prime 2 is treated separately below.

At 2, if a is odd then U is odd. If a is even, b is odd, and a is
divisible by 8: c and b are odd, so
`c²−b²=a(a+b)` is divisible by 8, while a+b is odd. Consequently
`v_2(U)=1`, W is odd, and `v_2(3UW)=1`. The equality `3UW=ds²` then
forces d even and s odd. Therefore U has no factor 2 when d is odd,
and at most one factor 2 when d is even. This argument does not assume
that s and m have the same parity.

For each p>3 dividing U, coprimality of U,W allocates the full exponent
`v_p(d)+2v_p(s)` to U. Since s|m, this exponent is at most
`v_p(d_+)+2v_p(h)`. Together with the conclusions at 2 and 3, this proves

    U | d_+ h²,  in particular U <= d h².            (4)

The norm identity expressed in U,W is exactly the last line of (1).
This proves necessity. Conversely, any arithmetic witness (1) gives

    a=2W−U, b=U−W, c=sqrt(U²−3UW+3W²),

which is a positive primitive plus-norm tile with coefficient ds².

### Passing the constructive threshold

Put `A=max(a,b)`, `B=min(a,b)` and R=A/B. The positive integer

    q=2c−2A−B

satisfies

    3B²=q(4A+2B+q)>4A.

Positivity follows from `c²−(A+B/2)²=3B²/4>0`. Thus

    R < sqrt(3A)/2 < sqrt(3U)/2.                    (5)

Also W<U and `3UW=ds²` imply

    s < sqrt(3/d) U.                               (6)

The prior F3 construction in `docs/square-class-tails.md`, Appendix A,
works at every integer scale `t>=ceil(M/2)`, where

    M=3(floor(R)+2).

There is no ceiling loss if one compares m directly with sM/2: an
integer t=m/s satisfies t>=M/2 exactly when t>=ceil(M/2). Equations
(4)–(6) imply

    sM/2 <= s(3R/2+3)
           < 9 U^(3/2)/(4 sqrt d) + 3 sqrt(3/d) U
           <= (9/4)d h³ + 3 sqrt(3d) h²
           < K(d) d h³,                            (7)

where K(1)=8 and K(d)=6 for d>=2.

For the last strict inequality when d>=2, divide by dh³ and use h>=1
and `sqrt(3/2)<5/4`. For d=1 use
`9/4+3sqrt(3)<8`. Under (2), or the sharper bound for d>=2, the
residual integer scale m/s is therefore past the established F3
threshold. This proves sufficiency and the theorem.

## 3. A uniform finite reduction on infinitely many prime supports

Fix d and a positive odd h supported on the splitting primes for 3.
The first enumeration in (1) gives a fixed finite list of primitive
F3 coefficient witnesses, independent of the number or size of primes
in m/h. For all m with this fixed split part h, sufficiently large
membership in the F3 branch is the finite divisibility test `s|m` on
this list; the explicit uniform cutoff is K(d)dh³, and 8dh³ is a
single sufficient bound valid for every squarefree d>=1. Both odd and
even m are included.

There are only finitely many positive integers m below that cutoff,
so the entire sector reduces to the finite coefficient list plus
finitely many small geometric decisions. This is different from the
previous fixed-finite-prime-support theorem: arbitrarily many new
primes from P_- can occur here, and the proof uses only elementary
factor allocation. No unit-equation solver or elliptic rank input is
needed.

It does **not** follow that the exact realizable multipliers in this
sector have a finite divisibility-minimal basis. For example, if a
coefficient's smallest scale were not realizable, arbitrarily large
prime residual scales could themselves be divisibility-minimal. The
statement is a finite list with an ordinary size cutoff and a finite
small remainder, not an assertion of a finite grid-refinement basis.

## 4. An infinite-support exclusion in square class 38

**Corollary.** If m is odd and every prime factor of m belongs to P_-,
then

    38m² is not an admissible tiling count.           (8)

Indeed d=38 has d_+=2 because `(3/19)=-1`, and h=1. Necessity gives
U|2, but a,b>0 require U=a+2b>=3. Thus no F3 coefficient exists at any
residual scale. The existing class-38 branch isolation proved in
`docs/infinite-minimal-multipliers.md`, Section 6, excludes every other
branch for an odd multiplier; this proves the global exclusion.

This rules out arbitrary mixed products and powers of odd primes in
four residue classes, as well as powers of 3, without bounding their
support. The global statement retains the hypothesis that m is odd;
for even m the argument excludes only F3, not the other branches.
It is compatible with the already proved infinite antichain
of positive class-38 multipliers: each of those positive multipliers
must contain a prime splitting for 3.

For comparison, d=110 has d_+=22. The fixed h=1 arithmetic list consists
of `(a,b,c,s)=(8,7,13,3)`. The subsequently verified nested-corner
construction now realizes the primitive 990 count itself. Combining
this seed with the old F3-only isolation gives the complete criterion
`110m² is admissible iff 3|m` for every odd m, without restricting its
split part; see `docs/square-class-110-odd.md`. The class-110 result is
a new positive geometric input, not a consequence of the older tail
estimate alone. The general small-scale gap in other classes remains.

## 5. Dependencies and verification scope

The F3 necessary spectrum and integer residual scale are the prior
`research/uniform-reduction/PROOF.md` inputs. The every-integer positive
threshold is the old Harries/Zhang transfer recorded in
`docs/square-class-tails.md`, Appendix A. Known F3-only global sectors
include class 38 by its cited branch proof and the sector in
`docs/f3-global-overlap.md`, Theorem 1.1: d=14 mod 16 and an odd-valuation
prime inert for 2. The present theorem characterizes only the F3 branch
unless such an independent global isolation applies.

`check_split_part.py` independently compares the restricted-factor list
with direct coefficient enumeration for odd and even multipliers and
odd and even squarefree kernels, including d=1. It checks the explicit
d=38 and d=110 lists, the even-coefficient multiplier `(d,s)=(66,2)`,
and `(d,m)=(110,6)`, where the factor 2 in U remains necessary despite
m being even. Those bounded computations test the formulas; the
universal large-nonsplit-part statement is proved by (4)–(7).
