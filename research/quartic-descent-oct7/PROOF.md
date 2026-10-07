# An infinite product extension of the square-class 78 obstruction

7 October 2026. Research directed by Denis Paliy, with ChatGPT assistance.

This note extends the elementary negative half of the complete square-class
78 theorem. It is not a complete classification of every square class below:
their small even multipliers remain outside the conclusion.

## Theorem

Let R be a product of an odd number of distinct primes p such that

\[
p\equiv13\pmod {24},\qquad 3^{(p-1)/4}\equiv1\pmod p.
\tag{1}
\]

Then, for every odd positive integer m, no triangle can be tiled by
6R m² congruent triangles, allowing reflections and arbitrary T-junctions.

There are infinitely many primes satisfying (1), and no bound is imposed
on the number of prime factors of R. The first qualifying primes are
13, 109, 181, 229, 277, 421, 541, 709, 733, 757. Thus examples include
the square classes 78, 654, 1086, 1374, 1662, and 1538862, the last
being 6·13·109·181.

The input about tilings is the existing necessary spectra and
[F3 isolation theorem](../../docs/f3-global-overlap.md). The descent proof itself is
elementary and uses no elliptic-curve rank or basis calculation.

## 1. Reduction to F3 and an explicit rational point

Each prime in (1) is 5 modulo 8. Because their number is odd,

\[
R\equiv5\pmod8,\qquad 6R m^2\equiv14\pmod {16}.
\]

Also v₃(6R m²) is odd. The existing residue-sector reduction leaves only
W and F3, and the W coefficient Q=2v²−u² has even valuation at 3 for
primitive coprime u,v: it cannot be divisible by 3 at all. Thus W is
excluded, leaving F3.

Its necessary count equation would be

\[
3(a+b)(a+2b)t^2=6R m^2,\quad
c^2=a^2+ab+b^2,\quad \gcd(a,b)=1.
\]

Since 6R is squarefree, comparison of prime valuations gives t|m.
Put s=m/t, S=a+b, T=a+2b. Then s is odd and

\[
ST=2R s^2,\qquad c^2=T^2-3ST+3S^2.
\tag{2}
\]

Exactly one of S,T has 2-adic valuation one. If S were even, (2)
would give c²=3 modulo 4. Consequently S is odd and v₂(T)=1;
a is even, b and c odd.

Define

\[
x=\frac{2R(2c+2T-3S)}{S},\qquad y=\frac{4Rs x}{S}.
\tag{3}
\]

The numerator factor 2c+2T−3S is odd, and is positive because it
equals 2c−a+b with c>a. Hence x>0 and v₂(x)=1. Direct substitution
using (2) gives

\[
y^2=x^3+12R x^2-12R^2x.
\tag{4}
\]

For clarity, write S₀=S/s, T₀=T/s, C₀=c/s. Then
S₀T₀=2R, C₀²=T₀²−6R+3S₀²,
x=T₀(2T₀−3S₀+2C₀), y=2T₀x, and
x²+(12R−4T₀²)x−12R²=0, which proves (4).

## 2. Every possible square class gives a partition R=AB

Any positive rational x satisfying (4), with odd v₂(x), can be written

\[
x=e(u/v)^2,\qquad e=2\varepsilon A,\qquad
\varepsilon\in\{1,3\},\quad A\mid R,
\tag{5}
\]

where u,v are positive coprime integers. Indeed, at any prime not
dividing 12R² an odd valuation of x makes either x³ or −12R²x the
unique least-valuation term in (4), contradicting the even valuation
of y². Thus the squarefree class of x is supported on 2,3 and R;
positivity excludes negative classes and odd v₂(x) forces the factor 2.

Substitution in (4) gives

\[
W^2=e u^4+12R u^2v^2-\frac{12R^2}{e}v^4,
\qquad W\in\mathbb Z.
\tag{6}
\]

Here W=yv³/(eu) is rational with integral square, hence an integer.
Set B=R/A, so A and B are coprime squarefree integers.

## 3. A prime in B requires (A/p)=−1

Let p|B. In particular p does not divide e. If p does not divide u,
reduction of (6) modulo p requires (e/p)=1. If p divides u, it divides
W; division by p² followed by reduction modulo p instead requires
(−12/e / p)=1. These are the same requirement because (−3/p)=1.

For every prime in (1), (2/p)=−1 and (3/p)=1. Therefore either case
forces

\[
\left(\frac A p\right)=-1\qquad(p\mid B).
\tag{7}
\]

The notation is the Legendre symbol. The case B=1 simply contributes
an empty product later.

## 4. A prime in A requires (B/p)=−1

Let p|A, write e=pδ and 2R=pκ. If exactly one of u,v is a p-adic
unit, the right side of (6) has valuation one, impossible. Thus both
are units. Since p|W, dividing (6) by p and reducing modulo p gives

\[
\delta u^4+6\kappa u^2v^2-3\kappa^2v^4/\delta=0.
\]

Equivalently, q=δu²/(κv²) must solve

\[
q^2+6q-3=0\pmod p,
\qquad
\left(\frac q p\right)
=\left(\frac{\delta\kappa}p\right)
=\left(\frac Bp\right).
\tag{8}
\]

The last equality follows from δκ=4ε(A/p)²B and (ε/p)=1.

Choose r with r²=3 modulo p. The roots of (8) are −3±2r, both
nonzero, and their product −3 is a square, so they have the same
quadratic character. Moreover

\[
-3+2r=\frac{r(r-1)^2}{2},\qquad
\left(\frac rp\right)
\equiv3^{(p-1)/4}\equiv1\pmod p.
\]

As (2/p)=−1, each root is a nonsquare. Equation (8) therefore forces

\[
\left(\frac Bp\right)=-1\qquad(p\mid A).
\tag{9}
\]

## 5. Quadratic reciprocity gives the contradiction

Let ω(A),ω(B) count the prime factors in A,B. Multiplying (7) and (9)
separately gives

\[
\prod_{p\mid B}\left(\frac Ap\right)=(-1)^{\omega(B)},
\qquad
\prod_{p\mid A}\left(\frac Bp\right)=(-1)^{\omega(A)}.
\]

Every prime dividing R is 1 modulo 4. Quadratic reciprocity makes
these two products equal, since each is the product of the pairwise
symbols across the partition A,B. But ω(A)+ω(B)=ω(R) is odd, so the
two displayed signs are opposite. This contradiction excludes every
cover (6), hence the rational point (3), and therefore every odd-multiplier
tiling count in the theorem.

## 6. Infinitely many qualifying primes

This section alone uses Chebotarev's theorem. Put

\[
F=\mathbb Q(i,\sqrt2,\sqrt3),\qquad
L=F(\alpha),\quad\alpha=\sqrt[4]3.
\]

The independent rational square classes −1,2,3 give [F:Q]=8. Since
F/Q is abelian, every subfield is normal over Q. The polynomial X⁴−3
is irreducible by Eisenstein at 3. The real quartic field Q(α)
is not normal, because it does not contain its nonreal conjugates;
thus α is not in F. Consequently [L:F]=2 and [L:Q]=16. The extension
L/Q is Galois, being the splitting field of (X⁴−3)(X²−2).

The automorphism of F fixing i and √3 and negating √2 has a lift σ
to L fixing α. It is central: any automorphism sends α to ζα with
ζ in {±1,±i}, while σ fixes both α and i, and restrictions commute
on the abelian field F. Thus {σ} is a singleton conjugacy class.

For an unramified prime p with Frobenius σ, the three quadratic
characters are (−1/p)=1, (2/p)=−1, (3/p)=1. These are precisely
p≡13 modulo 24. Its action on α also gives
3^((p−1)/4)=1 modulo p. Conversely, those conditions determine σ.
Chebotarev's theorem ([Milne, Theorem 8.31](https://www.jmilne.org/math/CourseNotes/ANTc.pdf))
therefore gives density 1/16 among rational primes, and
in particular infinitely many primes satisfying (1).

## 7. What is and is not classified

The theorem excludes every odd multiplier in infinitely many square
classes with unbounded prime support. For each fixed R, the existing
effective theta construction also supplies every sufficiently large
even multiplier: take d=6R, u=d−1, v=d+1, so v²−u²=4d. Its
computable theta threshold T(d) realizes d(2t)² for every t≥T(d).
The [explicit seed bounds](../../docs/explicit-theta-seeds.md) and
[every-integer rational-scale construction](../../docs/universal-rational-scales.md)
are the existing inputs, as in
[the earlier local-descent corollary](../../docs/local-descent-obstructions.md).
Thus an effective eventual parity classification follows.

For R=13 the new 312-tile F3 seed covers every even multiplier, giving
the already proved [complete class78 theorem](../../docs/square-class-78.md). No claim that every
small even multiplier works is made for other R, and no complete
solution of Erdős634 follows here. The residue check alone is not a
global rational-point criterion when it fails to exclude a cover.

The family differs from the prior local-descent families: their main
product family uses an even number of primes 7 modulo 24, and their
other family has squarefree kernel 30p. The current kernels are 6R
with an odd number of primes 13 modulo 24, none equal to 5.

## 8. Verification and attribution

The residue identities and product signs have a separate exact checker:
`python research/quartic-descent-oct7/check_odd_product.py` from the
repository root. It checks both root characters for all 53 primes
p≡13 mod24 below 3000, including primes outside the quartic condition;
it checks all 29,524 partitions of the 512 odd-cardinality subsets of
the first ten qualifying primes. These finite checks support the
universal proof above and do not replace it. The independent internal
[audit](AUDIT.md) also checks the local quartics directly.

The modular obstruction and reciprocity deduction are this continuation's
results. The angular classification, rationality and integral spectra,
the theta construction, and Chebotarev's theorem are prior inputs.
This work was developed with ChatGPT assistance; independent internal
checks are not external human review or proof-assistant verification.
No priority over the literature or complete solution of Erdős 634 is claimed.

## Dependencies and sources

- `docs/f3-global-overlap.md` supplies the exhaustive F3 isolation at
  residue 14 modulo 16 with a suitable odd-valuation nonresidue prime.
- `research/best-move-oct7/new-arithmetic/CLASS78.md` supplies the
  previous one-prime instance and the 312-tile positive seed.
- `docs/local-descent-obstructions.md`, Section 3, records the general
  necessary 2-isogeny cover and local rules, while Section 7 records
  the effective theta argument used for the even tail. The full
  necessary descent argument used here is reproduced above.
- J. S. Milne, *Algebraic Number Theory*,
  [author notes](https://www.jmilne.org/math/CourseNotes/ANTc.pdf),
  Theorem 8.31, supplies Chebotarev's density theorem for Section 6.

All comparisons with previous results mean the existing project ledger;
external priority and independent referee acceptance are not asserted.
