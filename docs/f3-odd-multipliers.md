# F3 with an odd square multiplier: a finite Mordell–Weil test

**Research directed by Denis Paliy, with ChatGPT assistance — 6 October 2026**

The [F3 elliptic-rank theorem](elliptic-square-classes.md) decides whether a square class occurs anywhere in the F3 coefficient spectrum. This note distinguishes the narrower question in which the square multiplier must be odd. Positive rank supplies the real interval needed for positive tile sides. A separate, finite specialization test decides the required parity.

The result concerns the classified 120-degree F3 branch. It neither decides arbitrary individual tile counts nor solves all of Erdős problem 634. The necessary spectra and the fixed-tile eventual constructions are prior geometric inputs. External priority and referee acceptance have not been established.

## 1. Statement and inputs

Let \(d>0\) be squarefree and put

\[
k=\operatorname{sf}(3d),\qquad
\epsilon=v_2(k)=v_2(d)\in\{0,1\},
\]

where \(\operatorname{sf}\) denotes the squarefree kernel. Consider the 2-isogenous curves

\[
E_k:\ Y^2=X^3+k^3,
\qquad
E'_k:\ y^2=x^3+6kx^2-3k^2x.
\tag{1.1}
\]

They have the same rational rank. Also, 3d/k is either 1 or 9, so E_k is rationally isomorphic to E_{3d} by the corresponding square/cube coordinate scaling. Write

\[
U_k=\{P\in E'_k(\mathbb Q_2):v_2(x(P))=\epsilon\}.
\tag{1.2}
\]

Neither infinity nor \((0,0)\) belongs to \(U_k\).

**Theorem 1.1.** The following are equivalent:

1. A primitive positive plus-norm triple satisfies
   \[
   c^2=a^2+ab+b^2,\qquad
   3(a+2b)(a+b)=d s^2
   \]
   for an odd positive integer \(s\).
2. An actual tiling in the F3 branch has count \(d m^2\) for some odd positive integer \(m\).
3. \(\operatorname{rank}E'_k(\mathbb Q)>0\), and \(E'_k(\mathbb Q)\cap U_k\ne\varnothing\).

If \(k\not\equiv1,2\pmod8\), all three conditions fail already over \(\mathbb Q_2\). Equivalently, an odd multiplier requires \(d\equiv3\pmod8\) for odd \(d\), and \(d\equiv6\pmod8\) for even \(d\).

**Finite specialization test.** Suppose a **complete, certified set of Mordell–Weil generators** of \(E'_k(\mathbb Q)\) is available, including generators of the rational torsion subgroup. For \(k\equiv1\) or \(2\pmod8\), condition 3 is equivalent to positive rank together with the existence of a listed generator \(P\) such that

\[
v_2(x(P))=\epsilon.
\tag{1.3}
\]

A finite-index collection of independent points is not sufficient for a negative conclusion: the missing coset could be supplied by an omitted generator. One rational point satisfying (1.3), together with any rational nontorsion point, is sufficient for a positive conclusion. This note does not compute complete bases for all \(k\), nor assert an unconditional general algorithm for computing them.

**Corollary 1.2.** If \(d\ne3\), a rational point satisfying (1.3) is automatically nontorsion. In that case the positive-rank hypothesis can be omitted: an odd-multiplier F3 witness exists if and only if \(E'_k(\mathbb Q)\) meets \(U_k\). Given a complete generating set, this is equivalent to at least one generator satisfying (1.3). Thus one such rational point is a complete positive arithmetic certificate.

Indeed, \(d\ne3\) means that the squarefree integer \(k\ne1\). The rational torsion of \(E_k\) is then exactly \(C_2\), as proved in the elliptic-rank note. The degree-two isogeny injects odd-order torsion of \(E'_k\) into \(E_k\), so none exists. Its only rational point of order two is \((0,0)\), and a rational half of this point would require \(x^2=-3k^2\), which is impossible. Hence \(E'_k(\mathbb Q)_{\mathrm{tors}}=\{O,(0,0)\}\), both outside \(U_k\). The general theorem retains the rank hypothesis so that the exceptional kernel \(d=3\) requires no separate convention.

The geometric dependencies are the F3 necessary count \(3(a+2b)(a+b)t^2\) with integral \(t\), recorded in the [uniform-reduction proof](../research/uniform-reduction/PROOF.md), and the effective every-integer fixed-tile F3 tail recalled in the [square-class tail note](square-class-tails.md), Appendix A. The latter credits the prior Harries–Zhang positive transfers. Once a coefficient with odd \(s\) is found, choosing any sufficiently large odd \(t\) gives an actual odd multiplier \(m=st\). A prescribed small scale is not asserted realizable.

## 2. One quartic describes all factor allocations

Put

\[
A=a+2b,\qquad B=a+b.
\]

Then

\[
\gcd(A,B)=1,\quad B<A<2B,\quad
c^2=A^2-3AB+3B^2.
\tag{2.1}
\]

The equation \(3AB=ds^2\) says that \(AB\), and hence \(A/B\), has square class \(k\). Thus there are rational numbers \(z,w\) with

\[
T=\frac AB=kz^2,\qquad w=\frac cB,
\]

on the quartic

\[
C_k:\quad w^2=k^2z^4-3kz^2+3.
\tag{2.2}
\]

Its positive tile cone is exactly \(1<T<2\). Its leading coefficient is a square, so its two points at infinity are rational. A birational model is \(E'_k\), with maps

\[
z=\frac{y}{2kx},\qquad
w=\frac{x^2+3k^2}{4kx},\qquad
T=\frac{x^2+6kx-3k^2}{4kx},
\tag{2.3}
\]

and, in the other direction,

\[
x=k(2w+2T-3),\qquad y=2kxz.
\tag{2.4}
\]

The displayed finite formulas exclude \(x=0\); the exceptional points extend in the smooth projective models. They do not lie in the positive cone used here. All identities follow by direct substitution.

Conversely, take a rational point with \(1<T<2\). Reduce \(T=A/B\) to positive coprime integers. Then

\[
a=2B-A,\qquad b=A-B,\qquad c=|w|B
\tag{2.5}
\]

are positive integers with \(\gcd(a,b)=1\). Indeed, \(c\) is rational and its square is the integer \(A^2-3AB+3B^2\), so it is an integer. The absolute value is necessary on the negative real component of \(E'_k\), where the formula for \(w\) is negative. Since \(d\) is squarefree, the rational square \(3AB/d\) has an integer square root \(s\).

## 3. Oddness is a precise 2-adic condition

For primitive plus-norm triples, reduction modulo 8 gives the following alternatives:

| Parity of \((a,b)\) | Forced divisibility | Valuation of \(D=3(a+2b)(a+b)\) |
|---|---|---|
| Both odd | \(8\mid a+b\) | \(v_2(D)\ge3\) |
| \(a\) odd, \(b\) even | \(8\mid b\) | \(v_2(D)=0\) |
| \(a\) even, \(b\) odd | \(8\mid a\) | \(v_2(D)=1\) |

Thus \(s\) is odd exactly when \(a,b\) have opposite parity. These two cases respectively give \(D\equiv3\) and \(6\pmod8\).

In the quartic coordinates, the exact condition is

\[
s\text{ odd}\quad\Longleftrightarrow\quad v_2(z)=0.
\tag{3.1}
\]

To see this, use \(v_2(A/B)=\epsilon+2v_2(z)\). For \(\epsilon=0\), the odd-multiplier branch has \(A,B\) both odd. For \(\epsilon=1\), it has \(v_2(A)=1\) and \(B\) odd. The alternative \(A\) odd, \(v_2(B)=1\) is ruled out by the first row of the table. Conversely, these valuations recover the opposite-parity cases.

On \(E'_k\), (3.1) becomes exactly \(P\in U_k\). If \(z\) is a 2-adic unit, (2.2) makes \(w\) a unit, and (2.4) gives \(v_2(x)=\epsilon\). Conversely, write \(x=kt\) with \(t\) a 2-adic unit. The cubic equation gives

\[
y^2=k^3t(t^2+6t-3).
\]

For \(t\equiv1\pmod4\), the last factor has valuation 2; for \(t\equiv3\pmod4\), it has valuation 3. When \(\epsilon=0\), only the first case can be a square, and \(v_2(y)=1\). When \(\epsilon=1\), only the second can be a square, and \(v_2(y)=3\). In either case (2.3) makes \(z\) a unit.

Finally,

\[
U_k\ne\varnothing\text{ over }\mathbb Q_2
\quad\Longleftrightarrow\quad k\equiv1\text{ or }2\pmod8.
\tag{3.2}
\]

Necessity follows from (2.2) with \(z\) a unit. For sufficiency choose \(z=1\): the right side \(k^2-3k+3\) is then \(1\pmod8\), hence has a 2-adic square root. Formula (2.4) produces a point in \(U_k\).

## 4. From a rational local seed to a positive tile

Assume \(\operatorname{rank}E'_k(\mathbb Q)>0\), and choose a rational point \(P\in U_k\) and a rational nontorsion point \(R\).

The set \(U_k\) is both open and closed in the compact 2-adic group \(E'_k(\mathbb Q_2)\). Some open finite-index subgroup \(H\) therefore preserves it under translation: cover the compact set by finitely many cosets of sufficiently small open subgroups, then take a common subgroup. Choose an integer \(L>0\) such that \(LR\in H\) and \(LR\) belongs to the identity component of \(E'_k(\mathbb R)\). Every point

\[
P+nLR,\qquad n\ge0,
\tag{4.1}
\]

remains in \(U_k\). Since \(LR\) is nontorsion, its multiples are dense in the real elliptic circle, so (4.1) is dense in the real component containing \(P\).

Both real components have an open arc in the required positive cone. Put \(t=x/k\). On the identity component, the interval \(1<t<3\) is available; on the other component, the interval \(-3<t<-1\) is available. On each interval,

\[
1<T=\frac{t^2+6t-3}{4t}<2.
\]

Consequently some point in (4.1) gives a positive primitive triple through (2.5), and its multiplier is odd by Section 3. This uses density on one real circle while keeping a fixed 2-adic coset. It is not an assumption of weak approximation for rational points on an elliptic curve.

Conversely, a positive F3 coefficient gives a rational point in \(U_k\). It also forces positive rank by the F3 elliptic-rank theorem: the corresponding point on \(E_k\) lies in \(0<X<k\), where none of its rational torsion points lie. Together with the prior eventual geometric construction, this proves Theorem 1.1.

## 5. Why checking a complete generating set is enough

### Even \(k\)

For even \(k\), any finite nonzero \(x\)-valuation other than 1 is even. In fact, for \(n=v_2(x)<1\), the cubic term has the unique least valuation \(3n\); for \(n>1\), the linear term has the unique least valuation \(2+n\). Since the sum is \(y^2\), either valuation is even. Thus

\[
U_k=\{P:\ v_2(x(P))\equiv1\pmod2\}.
\tag{5.1}
\]

The valuation parity is the homomorphism

\[
\delta_2:E'_k(\mathbb Q_2)\longrightarrow\mathbb Z/2,
\qquad \delta_2(P)=v_2(x(P))\pmod2,
\tag{5.2}
\]

with \(\delta_2(O)=0\) and \(\delta_2((0,0))=v_2(-3k^2)=0\). This is the valuation of the usual 2-isogeny descent map. Its homomorphism property can also be checked directly: a line through three intersection points on \(y^2=x(x^2+6kx-3k^2)\) makes the product of their \(x\)-coordinates a square. Addition by \((0,0)\) sends \(x\) to \(-3k^2/x\), which gives the same parity rule in the exceptional case.

Therefore a rational point in \(U_k\) exists exactly when at least one generator has nonzero \(\delta_2\). A sum of generators with zero image cannot supply it.

### Odd \(k\)

Only \(k\equiv1\pmod8\) needs consideration. The displayed integral model has

\[
\Delta=2^8\,3^3k^6,
\]

so it is minimal at 2: a nonminimal integral equation would have discriminant valuation at least 12. Modulo 2 the curve is

\[
y^2=x^3+x,
\]

with unique singular point \((1,0)\). Exactly the points with \(v_2(x)=0\) reduce to this singular point. Points with positive \(x\)-valuation reduce to the nonsingular point \((0,0)\); points with negative \(x\)-valuation reduce to infinity, also nonsingular. Hence

\[
E'_k(\mathbb Q_2)\setminus U_k=E'_{k,0}(\mathbb Q_2),
\tag{5.3}
\]

the finite-index subgroup of nonsingular reduction. The standard subgroup property is the local reduction theory for a minimal Weierstrass equation; see Silverman, *The Arithmetic of Elliptic Curves*, Chapter VII, Section 2, or Milne, [*Elliptic Curves*, second edition](https://jmilne.org/math/Books/EC2.pdf), Chapter II, Section 4.

Thus a rational point in \(U_k\) exists exactly when a complete set of Mordell–Weil generators, including torsion generators, contains a point outside this subgroup. This proves the finite specialization test in both parity cases.

## 6. Scope of the remaining arithmetic

Positive rank and (3.2) do not, by the arguments here alone, imply the existence of a rational point in \(U_k\). The precise additional obligation is a nontrivial specialization of the global Mordell–Weil group, as tested in Section 5. No counterexample to a possible stronger rank-plus-residue theorem is asserted here.

The rational points at infinity on the quartic do not remove this obligation. In a sufficiently small 2-adic neighborhood of either infinity, \(z\) has negative valuation. Primitive normalization then gives \(A\) odd and \(B\) divisible by 8, which is the wrong parity branch. Real density alone cannot change a progression that has been confined to that local neighborhood.

The test is therefore finite **given certified complete generators**. A positive certificate needs much less: one rational local seed and one rational nontorsion point; for \(d\ne3\), the seed itself supplies the nontorsion point. The exact maps in [elliptic.py](../research/elliptic-sectors/elliptic.py) support the underlying F3 correspondence; no general Mordell–Weil computation or implementation of this specialization test is claimed by that package.
