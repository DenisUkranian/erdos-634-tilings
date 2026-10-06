# Alpha with an odd square multiplier: a joint descent criterion

**Research directed by Denis Paliy, with ChatGPT assistance — 6 October 2026**

The [alpha congruent-number criterion](alpha-congruent-numbers.md) characterizes existence somewhere in a square class. Requiring the square multiplier to be odd imposes an additional condition. In the sector considered here, that condition is exactly a joint real-sign and 2-adic character of the rational Mordell–Weil group. Both coordinates are necessary.

The criterion below is finite when certified rational generators are supplied. It does not decide a prescribed small geometric scale, provide a general rank algorithm, or solve all of Erdős problem 634. No certified strict enlargement of the previous B1 obstruction is claimed.

## 1. Statement

Let \(d>0\) be squarefree, with \(d\equiv6\pmod{16}\), and put

\[
A_d:\quad Y^2=X^3+6dX^2+d^2X.
\tag{1.1}
\]

Write \(O\) for its origin at infinity and \(T=(0,0)\). For \(P\ne O,T\), define

\[
\begin{aligned}
\sigma(P)&=\begin{cases}0,&X(P)>0,\\1,&X(P)<0,\end{cases}\\
\nu(P)&=v_2(X(P))\pmod2,\\
h(P)&=(\sigma(P),\nu(P))\in\mathbb F_2^2.
\end{aligned}
\tag{1.2}
\]

Set \(h(O)=h(T)=(0,0)\). Section 2 proves that \(h\) is a group homomorphism.

**Theorem 1.1.** The following are equivalent:

1. There are coprime integers \(0<u<v\) and an odd positive integer \(s\) such that
   \[
   (v^2-u^2)(2v^2-u^2)=ds^2.
   \tag{1.3}
   \]
2. An actual tiling in the Group-1 alpha-isosceles branch has count \(dm^2\) for some odd positive integer \(m\).
3. \((0,1)\in h(A_d(\mathbb Q))\).

No separate positive-rank hypothesis is required. A point with the specified character directly gives a positive primitive coefficient.

**Finite generator criterion.** Suppose \(G_1,\ldots,G_r\), including torsion generators, generate \(A_d(\mathbb Q)\). Condition 3 holds exactly when either:

- some \(h(G_i)=(0,1)\); or
- two generators have images \((1,0)\) and \((1,1)\).

Thus a positive character certificate requires at most two generator images and at most one addition to produce a point with image \((0,1)\). This is a statement about the two-dimensional image, not a bound on the Mordell–Weil rank.

For a negative conclusion, complete certified generators suffice. More generally, a certified subgroup of odd index suffices, because \(h\) kills twice the group. An arbitrary finite-index collection of independent points is insufficient: an omitted coset of even index may contain the required image. No complete bases are computed in this note.

## 2. The joint character is a homomorphism

The usual 2-isogeny descent map for (1.1) is

\[
\delta:A_d(\mathbb Q)\longrightarrow
\mathbb Q^*/\mathbb Q^{*2},\qquad
\delta(P)=[X(P)]\quad(P\ne O,T),
\]

with \(\delta(O)=[1]\) and \(\delta(T)=[d^2]=[1]\).

For this model, its homomorphism property can be checked directly. Intersect a line \(Y=\lambda X+\mu\) with the cubic. Its three intersection abscissas, counted with multiplicity, have product \(\mu^2\). The third intersection is the negative of the sum of the first two in the elliptic group law, and negation preserves the abscissa. The product relation therefore proves multiplicativity modulo squares whenever the three abscissas are nonzero. If the line passes through \(T\), the other two abscissas have product \(d^2\), giving the same conclusion with the stated value of \(\delta(T)\). Tangencies are covered by repeated roots, while vertical lines give \(P+(-P)=O\).

Both the real sign and the parity of \(v_2\) are well-defined homomorphisms on \(\mathbb Q^*/\mathbb Q^{*2}\). Their product is precisely \(h\). In particular,

\[
h(P+Q)=h(P)+h(Q),\qquad h(2P)=0.
\tag{2.1}
\]

The finite generator criterion is now the elementary span test in \(\mathbb F_2^2\): without a listed \((0,1)\), that vector belongs to the span exactly when both \((1,0)\) and \((1,1)\) occur.

## 3. Rational maps and the real condition

Set \(b=v^2-u^2\) and \(Q=2v^2-u^2\). The substitution \(z=u/v\), \(w=s/v^2\) turns (1.3) into

\[
dw^2=(1-z^2)(2-z^2),\qquad 0<z<1.
\tag{3.1}
\]

The birational maps to (1.1), derived and checked in the [alpha rank note](alpha-congruent-numbers.md), are

\[
X=d\frac{1+z}{1-z},\qquad
Y=\frac{2d^2w}{(1-z)^2},
\tag{3.2}
\]

and

\[
z=\frac{X-d}{X+d},\qquad
w=\frac{2Y}{(X+d)^2}.
\tag{3.3}
\]

The positive parameter interval corresponds to \(X>d\). More generally, \(X>0\) gives \(|z|<1\). Translation by \(T\) sends

\[
(X,Y)\longmapsto
\left(\frac{d^2}{X},-\frac{d^2Y}{X^2}\right),
\tag{3.4}
\]

and hence replaces \(z\) by \(-z\). It preserves \(h\). Thus a point with \(X>0\) may be moved to \(X>d\) by at most one such translation, provided \(X\ne d\).

The exceptional equality cannot occur here: \(X=d\) would require \(Y^2=8d^3\), so \(2d\) would be a rational square. For positive even squarefree \(d\), this is possible only at \(d=2\), outside the stated sector. Similarly, \(X=-d\) would require \(d\) to be a square. The only rational point with \(Y=0\) is \(T\), since the other roots of the cubic are \(d(-3\pm2\sqrt2)\).

The sign condition is essential. Points with \(X<0\) correspond to the other real component of (3.1), where \(|z|>\sqrt2\); they cannot yield positive parameters \(0<u<v\).

## 4. Exact 2-adic condition

For primitive \(u,v\), the coefficient \(bQ\) has 2-adic valuation one exactly when \(u\) is even and \(v\) is odd. Indeed, when both are odd, \(8\mid b\) and \(Q\) is odd; when \(u\) is odd and \(v\) is even, both factors are odd. Since \(v_2(d)=1\), an odd \(s\) in (1.3) is therefore equivalent to

\[
z=u/v\in2\mathbb Z_2.
\tag{4.1}
\]

Write \(X=dt\). Then \(z=(t-1)/(t+1)\) belongs to \(2\mathbb Z_2\) exactly when \(t\) is a 2-adic unit congruent to 1 modulo 4. On the elliptic curve,

\[
Y^2=d^3t(t^2+6t+1).
\tag{4.2}
\]

If \(v_2(X)=1\), then \(t\) is a unit. When \(t\equiv1\pmod4\), the last factor in (4.2) is 8 modulo 16 and has valuation three. When \(t\equiv3\pmod4\), it has valuation two; the right side then has valuation five and cannot be a square. Consequently, for rational points where (3.3) is defined,

\[
z\in2\mathbb Z_2
\quad\Longleftrightarrow\quad v_2(X)=1.
\tag{4.3}
\]

All other finite abscissa valuations are even. For \(n=v_2(X)<1\), the cubic term in (1.1) uniquely has smallest valuation \(3n\), forcing \(n\) even. For \(n>1\), the linear term uniquely has smallest valuation \(2+n\), again forcing \(n\) even. Thus

\[
v_2(X)=1\quad\Longleftrightarrow\quad\nu(P)=1.
\tag{4.4}
\]

## 5. Proof of Theorem 1.1 and geometric scope

A primitive coefficient satisfying (1.3) maps to a point with \(X>d\) and \(\nu=1\). Hence its character is \((0,1)\).

Conversely, let \(h(P)=(0,1)\). By (3.4), translate by \(T\) if necessary to obtain \(X>d\). Equations (3.3), (4.3) and (4.4) give a rational \(z\) in \((0,1)\cap2\mathbb Z_2\). Write it in lowest terms as \(u/v\), with \(0<u<v\); then \(u\) is even and \(v\) is odd. The quartic equation gives

\[
bQ=d(wv^2)^2.
\]

The rational number \(s=|w|v^2\) is integral: if its reduced denominator is \(q\), then \(q^2\mid d\), so squarefreeness forces \(q=1\). Its 2-adic valuation is zero by the parity calculation. This proves the equivalence of statements 1 and 3 without a density argument or an unbounded point search.

For the geometric equivalence, the prior [necessary alpha spectrum](../research/uniform-reduction/PROOF.md) is

\[
N=bQK^2,\qquad K\in\mathbb Z_{>0}.
\]

If \(N=dm^2\) with \(m\) odd, squarefreeness applied to \(bQ=d(m/K)^2\) shows that \(s=m/K\) is an integer, necessarily odd. Conversely, a coefficient \(bQ=ds^2\) with odd \(s\), together with the prior [every-integer alpha tail](universal-rational-scales.md), supplies actual tilings for every sufficiently large odd \(K\). Their multipliers \(m=sK\) are odd. This proves statement 2 and completes the theorem. ∎

The theorem detects whether this branch occurs at any odd multiplier. It does not determine which smaller geometric scales for the resulting fixed tile are realizable.

## 6. Why valuation parity alone fails

For \(d=6\), the curve \(A_6\) contains

\[
P=(-2,8),\qquad
2P=(4,28),\qquad
3P=\left(-\frac{242}{9},\frac{2024}{27}\right).
\]

The point \(P\) has image \((1,1)\). It is non-torsion: after the integral change \(x=X+12\) to a short integral Weierstrass equation, the nonintegral abscissa of \(3P\) contradicts the Nagell–Lutz condition for torsion. Its double gives \(|z|=1/5\), and hence the positive even-square coefficient

\[
24\cdot49=1176=6\cdot14^2.
\]

Nevertheless no primitive positive odd-square coefficient exists in square class 6. Coprimality leaves only

\[
(b,Q)=(3y^2,2x^2)\quad\text{or}\quad(y^2,6x^2),
\]

where \(x,y\) are odd. Then \(v^2=Q-b\) is respectively 7 or 5 modulo 8, both impossible. Thus positive rank and a rational point of odd abscissa valuation do not suffice: the sign and valuation conditions must occur simultaneously.

This example concerns absence in the alpha branch at odd multipliers. The kernel 6 is classical, so it is not a global exclusion of counts \(6m^2\). Nor is it a new exclusion beyond the previous local allocation test.

## 7. Relation to the B1 obstruction and the QP sector

Write \(d=2D\). A positive odd-square alpha coefficient has coprime factor allocations

\[
Q=2Ar^2,\qquad b=Bt^2,\qquad AB=D,
\]

with \(r,t\) odd. The prior B1 conditions, recorded in [elliptic square classes, Section 3](elliptic-square-classes.md), are

\[
\begin{aligned}
A&\equiv7\pmod8,& B&\equiv5\pmod8,\\
(2/p)&=(-B/p)=1&&\text{for every prime }p\mid A,\\
(2A/p)&=1&&\text{for every prime }p\mid B.
\end{aligned}
\tag{7.1}
\]

Their alpha-branch necessity also holds when \(3\mid D\). Under (3.2),

\[
X=d\frac{v+u}{v-u}=\frac{db}{(v-u)^2},\qquad
[X]=[Q]=[2A]\in\mathbb Q^*/\mathbb Q^{*2}.
\tag{7.2}
\]

Thus B1 checks local necessary conditions on candidate descent square classes. Theorem 1.1 asks whether a suitable class actually occurs in the rational Mordell–Weil image. Empty B1 implies absence of \((0,1)\), but nonempty B1 is not, on the present evidence, a proved sufficient rational-point condition. No certified example separating the two tests is supplied, so a strict extension over B1 is not asserted.

There is a useful conditional application to the entire odd-multiplier sector. For squarefree \(d>6\) with \(d\equiv6\pmod{16}\), the existing [thirteen-row reduction](elliptic-square-classes.md) leaves only alpha, QP and F3 at odd multipliers. If

- \((0,1)\notin h(A_d(\mathbb Q))\); and
- the [odd-F3 specialization criterion](f3-odd-multipliers.md) is negative,

then, for every odd \(m\), the count \(N=dm^2\) is realizable exactly when it has the prior QP witness

\[
\begin{gathered}
N=K^2QP,\qquad \gcd(Q,P)=1,\qquad 3Q<2P<4Q,\\
P-Q\text{ and }2P-3Q\text{ are integer squares}.
\end{gathered}
\tag{7.3}
\]

Here \(K,Q,P\) are positive integers. The inequalities and square conditions recover coprime \(0<u<v\); the established QP construction works at every positive integer scale. Thus (7.3) is a finite arithmetic test with no remaining geometric existence test in that sector.

The hypotheses must be certified. The finite image criteria do not themselves supply complete rational generators, and no unconditional general procedure for obtaining every required basis is claimed. The geometric classification, integer-scale spectra and QP construction remain the prior inputs in [uniform sectors](../research/uniform-sectors/PROOF.md); the alpha constructive tail is the prior result linked above. These restricted criteria leave the full Erdős problem open.
