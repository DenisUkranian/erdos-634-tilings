# Elliptic rank and exact odd-multiplier sectors

**Research directed by Denis Paliy, with ChatGPT assistance — 6 October 2026**

Let \(\mathcal S\) denote the triangle-tiling counts used throughout this repository. For positive squarefree \(d\), define

\[
E_{3d}:\quad Y^2=X^3+(3d)^3.
\]

This note proves that the 120-degree F3 family has a coefficient in square class \(d\) exactly when \(E_{3d}\) has positive rational rank. It then combines the rank-zero obstruction with the existing angular classification and QP construction to give exact membership tests for all odd multipliers in a uniform sector. A class-number condition supplies a finite arithmetic certificate for part of that sector.

Elliptic curves have previously been used to characterize square-class existence in triangle tilings. In particular, Laczkovich's work, published online in 2019 [L], treats equilateral targets using different curves. The present note makes no claim to originate that approach or to establish external priority. The necessary spectra, QP construction, F3 constructive tails and oriented F4 construction are prior inputs. These results do not classify every count in Erdős problem 634.

## 1. F3 existence is equivalent to positive rank

A primitive F3 coefficient is

\[
D=3(a+2b)(a+b),\qquad
c^2=a^2+ab+b^2,
\tag{1.1}
\]

where \(a,b,c\) are positive integers and \(\gcd(a,b)=1\).

**Theorem 1.1.** For every positive squarefree \(d\), the following are equivalent:

1. \(\operatorname{rank}E_{3d}(\mathbb Q)>0\).
2. Some primitive F3 coefficient equals \(ds^2\) for a positive integer \(s\).
3. Some count \(dm^2\) is realizable in the F3 family.

The last equivalence uses the prior integral-scale necessary spectrum and every-integer F3 constructive tail, recorded in [square-class tails, Appendix A](square-class-tails.md). It does not assert existence at any prescribed multiplier \(m\).

### Rational torsion

For any positive integer \(K\), write \(E_K:Y^2=X^3+K^3\). Its rational torsion has no point with \(0<X<K\).

Here is a proof that does not require curve-specific tables. At a prime \(p\nmid6K\) with \(p\equiv2\pmod3\), cubing is a bijection on \(\mathbb F_p\), so

\[
\#E_K(\mathbb F_p)=p+1.
\]

Good reduction injects prime-to-\(p\) rational torsion into this finite group. For any prime \(\ell>3\), the Chinese remainder theorem and Dirichlet's theorem supply good primes with \(p\equiv2\pmod3\), \(p\equiv1\pmod\ell\); they exclude \(\ell\)-torsion. Good primes \(p\equiv5\pmod{12}\) exclude 4-torsion, and good primes \(p\equiv2\pmod9\) exclude 9-torsion. Thus every rational torsion point has order dividing 6.

The only nontrivial rational 2-torsion point is \((-K,0)\). The 3-division polynomial is

\[
3X(X^3+4K^3).
\]

Its only possible rational root is \(X=0\), since \(\sqrt[3]4\notin\mathbb Q\). This gives rational 3-torsion exactly when \(K\) is a square. The torsion group is therefore \(\mathbb Z/2\mathbb Z\) for nonsquare \(K\). For square \(K\), its six points are

\[
O,\quad(-K,0),\quad(0,\pm K\sqrt K),\quad(2K,\pm3K\sqrt K).
\tag{1.2}
\]

Neither case has torsion in \(0<X<K\). The good-reduction and division-polynomial inputs are standard; [S] records both. In our application \(K=3d\) is a square only for \(d=3\).

### From an F3 coefficient to a non-torsion point

Suppose (1.1) equals \(ds^2\). Put

\[
A=a+2b,\quad B=a+b,\quad K=3d,\quad h=s/3.
\]

Then

\[
AB=Kh^2,\qquad c^2=A^2-3AB+3B^2,\qquad B<A<2B.
\]

The rational point

\[
X=\frac{K(A-B)}B,\qquad Y=\frac{KAc}{hB}
\tag{1.3}
\]

satisfies \(Y^2=X^3+K^3\) and \(0<X<K\). It is non-torsion by (1.2), proving positive rank. This direction requires neither primitivity nor a parity restriction on \(s\).

### From positive rank to a primitive coefficient

Let \(P\in E_K(\mathbb Q)\) be non-torsion. The real group \(E_K(\mathbb R)\) is connected because the defining cubic has exactly one real root. As a compact connected one-dimensional Lie group, it is a circle. Therefore the even multiples \(2nP\) are dense, and one lies in the nonempty open arc

\[
0<X<K,\qquad Y>0.
\]

Every double has an additional square property. If \(Q=(u,v)\), the duplication formula gives

\[
X(2Q)+K=
\left(\frac{u^2+2Ku-2K^2}{2v}\right)^2.
\tag{1.4}
\]

For \(Q=nP\), the denominator is nonzero. Write \(X+K=w^2\) with rational \(w>0\), and define rational positive sides

\[
a=K-X,\qquad b=X,\qquad c=Y/w.
\]

They satisfy

\[
a^2+ab+b^2=K^2-KX+X^2
=\frac{X^3+K^3}{X+K}=c^2,
\]

and

\[
3(a+2b)(a+b)=3K(K+X)=d(3w)^2.
\tag{1.5}
\]

Clear denominators and normalize \(a,b\) to coprime positive integers. The corresponding rational \(c\) has an integer square and is therefore an integer. The normalized coefficient \(D_0\) remains \(d\) times a rational square. If that square root is a reduced fraction \(r/s\), integrality of \(D_0\) implies \(s^2\mid d\). Squarefreeness gives \(s=1\). We have obtained exactly the primitive coefficient required in Theorem 1.1. ∎

This proves a rank equivalence, not a general terminating rank algorithm. Given a non-torsion point, successive even multiples eventually produce a coefficient witness. Failure of a bounded point search proves nothing about rank zero.

## 2. A related Mordell twist and a class-number certificate

The curve \(E_K\) is 3-isogenous over \(\mathbb Q\) to

\[
y^2=x^3-27K^3.
\]

Away from \(X=0\), an explicit isogeny is

\[
(X,Y)\longmapsto
\left(\frac{X^3+4K^3}{X^2},
\frac{Y(X^3-8K^3)}{X^3}\right).
\]

For \(K=3d\), scaling these coordinates by 9 and 27 gives

\[
F_d:\quad y^2=x^3-d^3.
\]

Hence

\[
\operatorname{rank}E_{3d}(\mathbb Q)
=\operatorname{rank}F_d(\mathbb Q).
\tag{2.1}
\]

**Proposition 2.1.** If \(d\) is positive, even, squarefree and \(d\equiv1\pmod3\), then

\[
\operatorname{rank}E_{3d}(\mathbb Q)
\le2\dim_{\mathbb F_3}
\operatorname{Cl}(\mathbb Q(\sqrt{-d}))[3].
\tag{2.2}
\]

In particular, \(3\nmid h(-4d)\) proves rank zero and excludes the entire F3 square class. Here \(h(-4d)\) is the imaginary quadratic class number, not the number of points on an elliptic curve.

**Proof.** Apply Stoll's formula as stated in Chang [C, Theorem 1.1] to \(y^2=x^3-A\), with \(A=d^3>0\), over \(L=\mathbb Q(\zeta_3)\). It requires \(-A\equiv2\pmod3\) and local nonsquareness of \(-A\) at every bad finite place away from the place over 3. Here \(-A\equiv8\pmod9\). Bad rational primes away from 3 divide \(2d\), and hence divide \(d\), since \(d\) is even. The extension \(L/\mathbb Q\) is unramified at each of them, so the corresponding valuation of \(-d^3\) is 3, which is odd. The local nonsquareness condition follows.

The stated Selmer formula bounds the rational rank by twice the 3-rank of \(\operatorname{Cl}(\mathbb Q(\sqrt{-d^3}))\), giving (2.2) through (2.1). Since \(d\) is even and squarefree, the discriminant of \(\mathbb Q(\sqrt{-d})\) is \(-4d\). ∎

The criterion \(3\nmid h(-4d)\) is sufficient; its failure is not evidence of positive rank. It is a finite computable condition. For example, enumerate primitive reduced positive binary quadratic forms of discriminant \(-4d\):

\[
b^2-4ac=-4d,\quad |b|\le a\le c,
\quad 1\le a\le\sqrt{4d/3},
\]

with \(b\ge0\) on the boundaries \(|b|=a\) or \(a=c\). Their number is the class number; see the [SageMath reduced-form documentation](https://doc.sagemath.org/html/en/reference/quadratic_forms/sage/quadratic_forms/binary_qf.html). For discriminant -88 the only forms are (1,0,22) and (2,0,11), giving a finite algebraic certificate for the prior class-22 result.

## 3. An alpha obstruction without a restriction at 3

For odd squarefree \(D\equiv3\pmod8\), let \(\mathcal A(D)\) be the finite set of factorizations \(D=AB\) satisfying

\[
\begin{aligned}
A&\equiv7\pmod8,& B&\equiv5\pmod8,\\
(2/p)&=1,\quad(-B/p)=1&&\text{for every prime }p\mid A,\\
(2A/p)&=1&&\text{for every prime }p\mid B.
\end{aligned}
\tag{3.1}
\]

These are the existing B1 conditions in [uniform sectors](../research/uniform-sectors/PROOF.md). Their alpha-branch necessity holds without assuming \(3\nmid D\) or excluding multipliers divisible by 3.

Indeed, suppose a primitive alpha coefficient \(bQ\), with

\[
b=v^2-u^2,\quad Q=2v^2-u^2,\quad
\gcd(u,v)=1,\quad0<u<v,
\]

belongs to \(2D\) times an odd square. Its residue is 6 modulo 16, forcing \(v\) odd and \(u\equiv2\pmod4\). Hence \(b\equiv5\pmod8\), \(Q/2\equiv7\pmod8\). Since \(\gcd(b,Q)=1\), their square classes partition \(D\):

\[
b=B s^2,\qquad Q=2A r^2,\qquad AB=D,
\]

with \(r,s\) odd. If \(p\mid A\), reduction modulo \(p\) gives \((2/p)=1\) and \(b=-v^2\), hence \((-B/p)=1\). If \(p\mid B\), then \(u^2=v^2\) and \(Q=v^2\), giving \((2A/p)=1\). Coprimality ensures all denominators and square factors used here are nonzero modulo \(p\).

This includes \(p=3\): since \((2/3)=-1\), that prime cannot belong to \(A\). Thus emptiness of \(\mathcal A(D)\) excludes alpha for every odd multiplier. A simple sufficient condition for emptiness is that \(D\) has no prime factor congruent to 7 modulo 8; all primes of a putative \(A\) would then be 1 modulo 8. This sufficient condition also permits \(3\mid D\).

## 4. Exact QP membership for every odd multiplier

**Theorem 4.1.** Let \(d\) be positive and squarefree, with

\[
d\equiv6\pmod{16},\qquad
\mathcal A(d/2)=\varnothing,\qquad
\operatorname{rank}E_{3d}(\mathbb Q)=0.
\tag{4.1}
\]

Then, for every odd positive integer \(m\), \(dm^2\in\mathcal S\) if and only if there are positive integers \(t,Q,P\) satisfying

\[
dm^2=t^2QP,\quad\gcd(Q,P)=1,\quad3Q<2P<4Q,
\tag{4.2}
\]

such that \(P-Q\) and \(2P-3Q\) are integer squares. No restriction at 3 is imposed on \(d\) or \(m\).

**Proof.** In any necessary spectrum, the integral scale \(t\) divides \(m\), so its primitive coefficient is \(ds^2\), with \(s\) odd, and is 6 modulo 16. The two difference-of-squares rows cannot have 2-adic valuation one. A primitive W coefficient \(2v^2-u^2\) cannot be 6 modulo 16; the beta coefficient \(3v^2-u^2\) cannot be 6 modulo 8.

For primitive norm triples, the remaining coefficient residues are:

| Norm row | Possible residues modulo 8 |
|---|---|
| 60-degree equilateral | \(0,1\) |
| 120-degree equilateral | \(0,7\) |
| F1 | \(0,1\) |
| 120-degree isosceles | \(0,1,2\) |
| F2 | \(2,7\) |
| F3 | \(0,3,6\) |
| F4 | \(0,1,2\) |

To check this table, if one norm side is even it is divisible by 8. If both are odd, the plus norm gives \(ab\equiv7\pmod8\), \(a+b\equiv0\pmod8\), while the minus norm gives \(ab\equiv1\pmod8\). Substitution into the seven coefficients gives the table. Its only survivor, F3, is excluded by Theorem 1.1.

The classical sum-of-two-squares and twice-square forms are impossible modulo 8. Among the other classical forms, only kernel \(d=6\) is in this sector. But \(E_{18}\) has the point \((9,81)\), which is non-torsion by Section 1, so \(d=6\) contradicts (4.1).

Only alpha and QP remain. Section 3 excludes alpha. The integral QP spectrum gives (4.2) and the two square conditions. Conversely set

\[
v=\sqrt{P-Q},\qquad u=\sqrt{2P-3Q}.
\]

The inequalities give \(0<u<v\), and coprimality of \(Q,P\) gives \(\gcd(u,v)=1\). The previous QP construction, valid at every positive integer multiplier, supplies exactly \(QPt^2=dm^2\) tiles. ∎

For a direct prime-allocation version, write \(D=d/2\), enumerate \(D=AB\), and choose odd positive \(x,y\) with \(xy\mid m\). Test

\[
\begin{gathered}
Q=2Ax^2,\qquad P=By^2,\qquad\gcd(2Ax^2,By^2)=1,\\
3Ax^2<By^2<4Ax^2,\\
By^2-2Ax^2\text{ and }2By^2-6Ax^2\text{ are squares}.
\end{gathered}
\tag{4.3}
\]

Then \(t=m/(xy)\). The optional residue filters are \(A\equiv1\pmod8\), \(B\equiv3\pmod8\). This is a finite arithmetic test, using the established geometric sufficiency of QP; no tiling search is required.

**Corollary 4.2 — removing powers of 3.** Under (4.1), write an odd multiplier as \(m=3^k h\), with \(3\nmid h\). Then

\[
dm^2\in\mathcal S\quad\Longleftrightarrow\quad dh^2\in\mathcal S.
\tag{4.4}
\]

In a primitive QP coefficient, \(3\nmid Q\) and \(v_3(P)\le1\). The former follows because 2 is not a square modulo 3. For the latter, \(3\mid P\) forces \(3\mid u\), \(3\nmid v\), and \(P/3=v^2-3(u/3)^2\equiv1\pmod3\). Thus \(QP=ds^2\), with squarefree \(d\), implies \(3\nmid s\). All powers of 3 in \(m\) belong to the geometric scale and can be removed while keeping a positive integer QP scale. The converse is grid refinement.

**Corollary 4.3 — a computable class-number sector.** If \(d\) is positive and squarefree and

\[
d\equiv22\pmod{48},\qquad
3\nmid h(-4d),\qquad\mathcal A(d/2)=\varnothing,
\tag{4.5}
\]

then Theorem 4.1 and Corollary 4.2 apply. All conditions in (4.5) are finite arithmetic tests. The congruence combines \(d\equiv6\pmod{16}\) and \(d\equiv1\pmod3\); Proposition 2.1 supplies rank zero. No unproved rank conjecture enters this corollary.

## 5. When the same criterion settles every multiplier

The rank and alpha hypotheses alone do not prove that every even multiplier is admissible. The old theta construction supplies only an eventual even-multiplier tail in general.

An additional finite sufficient condition closes the even sector. Suppose a positive integer norm triple \(a<b<c\) satisfies

\[
c^2=a^2+ab+b^2,\qquad(2a+b)(a+b)=4d.
\tag{5.1}
\]

The prior oriented F4 construction gives a \(4d\)-tiling, and refinement gives \(dm^2\) for every even \(m\). Consequently, under (4.1) or (4.5), together with (5.1), exact membership for **every** multiplier is:

\[
\boxed{dm^2\in\mathcal S
\quad\Longleftrightarrow\quad
m\text{ is even, or }m\text{ is odd and passes (4.2).}}
\tag{5.2}
\]

To test (5.1), enumerate \(UV=4d\), recover \(a=V-U\), \(b=2U-V\), retain \(0<a<b\), and test the norm square. The orientation \(a<b\) is required by the existing proof and is not omitted. The construction and its attribution are in [the F4 package](../research/group2-f4/PROOF.md). For \(d=22\), the old triple \((3,5,7)\) gives 88; [square class 22](square-class-22.md) supplies its complete specialization.

The exact additional condition for an **odd** F3 coefficient is proved in
[the odd-multiplier note](f3-odd-multipliers.md). It reduces to a finite
coordinate test when a certified full Mordell–Weil basis is available.
The related [alpha correspondence](alpha-congruent-numbers.md) identifies
Group-1 alpha square-class existence with positive rank of the classical
congruent-number curve. Neither correspondence decides every prescribed
small geometric multiplier.

## 6. Dependencies and limits

- **[L]** M. Laczkovich, *Rational Points of Some Elliptic Curves Related to the Tilings of the Equilateral Triangle*, published online 2019, Discrete & Computational Geometry 64 (2020), 985–994, [DOI:10.1007/s00454-019-00143-5](https://link.springer.com/article/10.1007/s00454-019-00143-5). This is prior work relating tiling square classes to rational points, for equilateral targets and different elliptic curves.
- **[C]** S. Chang, *Note on the rank of quadratic twists of Mordell equations*, [arXiv:math/0510001](https://arxiv.org/pdf/math/0510001), Theorem 1.1, page 3. It states the Stoll formula used in Proposition 2.1. The original reference is M. Stoll, *On the arithmetic of the curves \(y^2=x^\ell+A\) and their Jacobians*, J. reine angew. Math. 501 (1998), 171–189, Corollary 2.1.
- **[S]** A. Sutherland, MIT 18.783, Fall 2025, [Problem Set 3](https://math.mit.edu/classes/18.783/2025/ProblemSet3.pdf), Problem 2(d) and Problem 3: good-reduction torsion injectivity and division-polynomial formulas. Section 1 gives the required specialization explicitly.
- The complete necessary row reduction and QP construction are the previous [uniform-sectors results](../research/uniform-sectors/PROOF.md). The constructive F3 tail uses the previous Harries/Zhang transfers, with sources and geometry recalled in [square-class tails](square-class-tails.md). The even-seed construction is the prior oriented F4 result.

The rank theorem decides existence somewhere in the F3 square class, not a particular small F3 multiplier. The exact odd-multiplier theorem applies only under its stated alpha and rank hypotheses; the class-number test is one sufficient way to verify them. The all-multiplier extension additionally requires a proved even seed. No density estimate, universal rank algorithm, or complete solution of Erdős problem 634 is claimed.
