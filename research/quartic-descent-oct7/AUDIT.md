# Independent audit of the odd-product F3 obstruction

7 October 2026. Independent internal audit; no external referee acceptance.

**Verdict: PASS.** The proposed statement follows from the existing exhaustive
F3-isolation theorem and the elementary argument below. The infinitude claim
is also valid, using Chebotarev. This does not classify small even multipliers
or solve all of Erdős 634.

## Statement audited

Let R be a squarefree product of an odd number of distinct primes p satisfying

    p = 13 (mod 24),       3^((p-1)/4) = 1 (mod p).

Then no positive odd integer m has 6 R m² as a triangle-tiling count.

The singleton cases p=13,109,181 exclude all odd multipliers in square
classes 78,654,1086 respectively. The three-prime product
R=13·109·181=256477 excludes the odd multipliers in square class
1538862. By contrast p=37 does **not** satisfy the power test:
3^9=-1 modulo 37. The result does not cover all primes 13 modulo 24.

## 1. Reduction and rational map

Each p is 5 modulo 8, so R is 5 modulo 8. Thus 6Rm² is 14 modulo 16
for odd m. Its valuation at 3 is odd. The existing F3-isolation theorem
therefore leaves F3 as the only possible branch.

Write its primitive coefficient as

    3(a+b)(a+2b) r² = 6 R m²,
    c² = a²+ab+b²,       gcd(a,b)=1.

Since 6R is squarefree, r divides m. Put s=m/r, S=a+b, T=a+2b.
Then s is odd and

    ST = 2R s²,         c² = T²-3ST+3S².

Exactly one of S,T is even, with valuation one. If S were even, reducing
the norm modulo 4 would give c²=3 modulo 4. Thus S is odd and T has
valuation one. In particular a is even and b,c are odd.

Define

    x = 2R(2c+2T-3S)/S,
    y = 4R s x/S.

Then x>0, v₂(x)=1, and

    y² = x³+12R x²-12R² x.                         (1)

For an independent verification, put S0=S/s, T0=T/s, C0=c/s.
Then S0 T0=2R, C0²=T0²-6R+3S0², and

    x=T0(2T0-3S0+2C0),      y=2T0 x.

Substitution gives x²+(12R-4T0²)x-12R²=0, proving (1).
Positivity follows from 2c-a+b>0; c>a. Its parity follows because S
and 2c-a+b are odd. No elliptic-curve rank or basis is needed.

## 2. Exhaustive positive squareclasses

At a prime not dividing 12R², an odd valuation of x is impossible in
(1): the cubic term is uniquely minimal for negative valuations, and
the linear term is uniquely minimal for positive valuations. Hence

    x=e(u/v)²,    e=2·3^j·A,    j in {0,1},    A divides R,

with coprime positive integers u,v. Positivity of x excludes negative
squareclasses; this restriction is essential and justified by the map.
The valuation at 2 ensures that e is even. Substitution gives

    W²=e u⁴+12R u²v²-(12R²/e)v⁴,       W an integer.       (2)

Indeed W=yv³/(eu) is rational with integral square, so it is integral.
Let B=R/A.

## 3. Local requirement at a prime dividing B

Let p divide B, so p does not divide e. If (e/p)=-1, (2) modulo p
forces p to divide u,W. Dividing by p² then gives

    (W/p)² = -(12/e)(R/p)² v⁴ (mod p).

Here (-12/p)=1 because p=13 modulo 24. Thus the coefficient is again
a quadratic nonresidue, forcing p to divide v, a contradiction.
Therefore (e/p)=1. Since (2/p)=-1 and (3/p)=1, this says

    (A/p) = -1       for every p dividing B.              (3)

## 4. Local requirement at a prime dividing A

Let p divide A and write e=pδ, 2R=pκ. Equation (2) has a factor p
on its right, so p divides W. Dividing by p and reducing modulo p gives

    δu⁴+6κu²v²-(3κ²/δ)v⁴=0.

Neither u nor v vanishes modulo p, since either vanishing would force
both to vanish. Therefore q=δu²/(κv²) is nonzero and satisfies

    q²+6q-3=0,       (q/p)=(δκ/p)=(B/p).                 (4)

For r²=3 modulo p the roots are -3±2r. They have equal quadratic
character because their product is -3, a square modulo p. The identity

    -3+2r = r(r-1)²/2

shows their character is -(r/p). But

    (r/p)=r^((p-1)/2)=3^((p-1)/4)=1.

Thus both roots in (4) are nonsquares, and

    (B/p) = -1       for every p dividing A.              (5)

## 5. Quadratic reciprocity contradiction

Multiplying (3) and (5) gives

    product_{p|B}(A/p) · product_{q|A}(B/q) = (-1)^ω(R)=-1.

Every prime divisor of R is 1 modulo 4. Expanding both products into
symbols between a prime dividing A and a prime dividing B, quadratic
reciprocity makes each pair multiply to 1. The left side is therefore
1, contradiction. This includes A=1 and B=1 via empty products.

All supported positive squareclasses have been excluded, proving the
theorem. Neither coprimality between m and R nor a bound on m is used.

## 6. Infinitely many qualifying primes

Let α be the positive fourth root of 3 and F=Q(i,√2,√3).
Then F/Q is an abelian extension of degree eight. The field Q(α) is
not normal (it is real and misses iα), so it cannot be a subfield of F.
Since α²=√3, the Galois extension L=F(α) has degree sixteen.

Put K=Q(i,α). It is the splitting field of X⁴-3 and has degree eight:
X⁴-3 is Eisenstein at 3, and Q(α) is real. Thus L=K(√2), and
√2 is not in K (otherwise L would have degree eight). The automorphism
σ fixing K and negating √2 is central: K and Q(√2) are Galois with
trivial intersection, and their Galois groups form a direct product.

For an unramified prime p, Frobenius equal to σ means that X⁴-3 splits
over F_p, p=1 modulo 4, and (2/p)=-1. This is equivalent to

    p=13 (mod 24),       3^((p-1)/4)=1 (mod p).

For the reverse direction, p=13 modulo 24 contains the fourth roots of
unity, and the displayed power test says that 3 is a fourth power.
Thus X⁴-3 splits and Frobenius is the identity on K; the condition on
2 determines its remaining action.

Chebotarev applied to the singleton conjugacy class {σ} proves that
these primes have Dirichlet density 1/16 among rational primes, and in
particular are infinite. The natural density is the same if desired.
This density refers to the prime set, not to the excluded tiling counts.

Source for the invoked general theorem: Andrew V. Sutherland, MIT
18.785, Lecture 28 (Fall 2021), Theorem 28.9 and Remark 28.12:
https://math.mit.edu/classes/18.785/2021fa/LectureNotes28.pdf

## Scope of the audit

The symbolic and congruence argument above is universal. The accompanying
checker verifies its algebra and bounded residue/product instances only;
those finite checks are not substituted for the proof. The necessary
angular classification and integral square scales remain prior inputs.
No complete positive criterion for even m is asserted here.
