# Finite arithmetic criteria for square-class tails and prime-power rays

**Research directed by Denis Paliy, with ChatGPT assistance — 6 October 2026**

Let \(\mathcal S\) consist of the positive integers \(N\) for which some nondegenerate triangle can be dissected into \(N\) congruent nondegenerate triangles. Reflections and arbitrary T-junctions are allowed.

This note gives a finite arithmetic criterion for whether a square class \(dm^2\), with \(d\) squarefree, contains **every sufficiently large odd multiplier**. It also gives a finite criterion for whether a fixed odd-prime-power ray \(dq^{2k}\) contains any admissible count. A positive ray test implies a tail of admissible exponents; it does not assert that a particular small exponent is admissible.

The new deduction uses prime-power multipliers to turn an unbounded search over tile shapes into finite divisor tests. The necessary spectra, fixed-tile eventual constructions, and W/beta square-class saturation are prior inputs. The positive norm-family transfers are credited to Harries and Zhang. No proposed all-primes classification, withdrawn scale divisibility, density estimate, or local orientation-switching hypothesis is used. External priority and referee acceptance have not been established.

This is a classification of two asymptotic properties and of existence somewhere on a fixed prime-power ray. It is **not** a classification of membership in \(\mathcal S\) for each individual integer.

## 1. The finite tests

For a positive squarefree integer \(d\), define the following conditions.

**Classical condition \(C_0(d)\):** either \(d\in\{1,2,3,6\}\), or every odd prime divisor of \(d\) is \(1\pmod4\).

**W condition \(C_W(d)\):** every odd prime divisor of \(d\) is \(1\) or \(7\pmod8\).

**Beta condition \(C_B(d)\):** every prime \(p\mid d\), \(p>3\), is \(1\) or \(11\pmod{12}\), and

\[
\begin{cases}
d\equiv2\pmod3,&3\nmid d,\\
d/3\equiv1\pmod3,&3\mid d.
\end{cases}
\tag{1.1}
\]

For an arbitrary positive integer \(D\), let \(\mathcal P(D)\) mean that \(D\) occurs as an **exact coefficient**, without an additional square factor, in at least one of the following nine necessary spectra.

In the first two rows take coprime \(0<u<v\) and put

\[
b=v^2-u^2,\qquad Q=2v^2-u^2,\qquad P=3v^2-u^2.
\]

In each norm row take positive integers \(a,b,c\) with \(\gcd(a,b)=1\) and the indicated norm equation. Both orders of \(a,b\) are included.

| Family | Exact coefficient \(D\) | Tile condition |
|---|---:|---|
| Group-1 alpha-isosceles | \(bQ\) | \(0<u<v,\ \gcd(u,v)=1\) |
| Group-1 other scalene | \(QP\) | Same |
| 60-degree equilateral | \(ab\) | \(c^2=a^2-ab+b^2\) |
| 120-degree equilateral | \(ab\) | \(c^2=a^2+ab+b^2\) |
| 120-degree F1 | \(b(a+b)\) | Plus norm |
| 120-degree isosceles | \(b(a+2b)\) | Plus norm |
| 120-degree F2 | \((a+2b)(2a+b)\) | Plus norm |
| 120-degree F3 | \(3(a+2b)(a+b)\) | Plus norm |
| 120-degree F4 | \((2a+b)(a+b)\) | Plus norm |

These are necessary coefficient forms, not assertions that multiplier one is geometrically realizable. Section 4 gives finite divisor tests for \(\mathcal P(D)\).

Define the **tail test**

\[
\mathsf T(d):\quad
d\text{ is odd},\quad\text{or}\quad
C_0(d)\lor C_W(d)\lor C_B(d)\lor\mathcal P(d).
\tag{1.2}
\]

For an odd prime \(q\), define the **prime-power ray test**

\[
\mathsf R(d,q):\quad
d\text{ is odd},\quad\text{or}\quad
C_0(d)\lor C_W(d)\lor C_B(d)
\lor
\bigvee_{\substack{r\ge0\\q^r<2d}}\mathcal P(dq^{2r}).
\tag{1.3}
\]

The disjunction is finite. All coefficients tested in it are strictly less than \(4d^3\).

## 2. Statements

**Theorem 2.1 — cofinal square-class criterion.** For every positive squarefree \(d\), the following are equivalent:

1. \(\mathsf T(d)\) holds.
2. \(dm^2\in\mathcal S\) for every sufficiently large odd integer \(m\).
3. \(dm^2\in\mathcal S\) for every sufficiently large integer \(m\).

A positive test supplies a fixed tile and target shape and a computable sufficient threshold for the multiplier. If the test fails, then

\[
\boxed{dq^{2k}\notin\mathcal S
\quad\text{for every prime }q>2d\text{ and every }k\ge0.}
\tag{2.1}
\]

**Theorem 2.2 — fixed prime-power ray criterion.** For every positive squarefree \(d\) and every odd prime \(q\), including \(q=3\) and \(q\mid d\), the following are equivalent:

1. \(\mathsf R(d,q)\) holds.
2. \(dq^{2k}\in\mathcal S\) for at least one integer \(k\ge0\).
3. \(dq^{2k}\in\mathcal S\) for every sufficiently large integer \(k\).

Thus a negative ray test excludes **every** exponent on that ray. A positive test gives a computable sufficient exponent threshold. It does not decide each smaller exponent.

## 3. Precise prior inputs

The exhaustive angular classification and rationality normalization are those recorded in Beeson–Zhang, Table 1 and Theorem 1.2 [BZ], with the classical exceptions separated. The [uniform-sectors proof](../research/uniform-sectors/PROOF.md), Section 2, and [uniform-reduction proof](../research/uniform-reduction/PROOF.md) give the necessary integral-scale spectra.

After the classical counts

\[
r^2,\quad r^2+s^2,\quad2r^2,\quad3r^2,\quad6r^2
\tag{3.1}
\]

are separated, the thirteen nonclassical rows are the nine product rows in Section 1, W with coefficient \(Q\), beta-isosceles with coefficient \(P\), and two difference-of-squares rows with coefficient \(v^2-u^2\). Every actual count in a row has the form \(N=Dt^2\) with a **positive integer** \(t\). This integrality, proved by exterior lengths and signed-direction characters, is essential below and survives T-junctions.

The constructive inputs are:

- [Universal rational scales](universal-rational-scales.md) and [explicit theta seeds](explicit-theta-seeds.md): each primitive Group-1 row has an effective every-integer multiplier tail; the QP row is constructive at every positive multiplier.
- [Square-class saturation](../research/square-class-saturation/PROOF.md), Sections 5–6: conditions \(C_W\) and \(C_B\) supply primitive representatives \(Q=d\) and \(P=d\), respectively, outside their classical exceptional kernels, and construct every multiplier \(m\ge2d\). These are prior norm and tail results.
- [General spectra](../research/general-spectra/PROOF.md): every primitive 60-degree or 120-degree norm tile has an explicit every-integer equilateral multiplier tail. Appendix A recalls the positive transfers that give every-integer tails for all five other 120-degree rows.

For odd \(d\ge3\), the old theta construction already gives all sufficiently large \(dm^2\): choose \(u=(d-1)/2\), \(v=(d+1)/2\), so \(v^2-u^2=d\). Kernel \(1\) is classical. This is why both tests accept all odd kernels immediately.

These inputs, rather than any quantitative density theorem, are the dependencies of the present criteria.

## 4. Finite inverse formulas

Each condition \(C_0,C_W,C_B\) requires only integer factorization and congruences. To test \(\mathcal P(D)\), enumerate the indicated divisor pairs and apply these formulas.

| Row | Factorization | Recovered parameters |
|---|---|---|
| Group-1 alpha | \(D=bQ\) | \(v^2=Q-b,\ u^2=Q-2b\) |
| Group-1 QP | \(D=QP\) | \(v^2=P-Q,\ u^2=2P-3Q\) |
| Either equilateral | \(D=ab\) | Test \(a^2\pm ab+b^2\) for a square |
| F1 or isosceles | \(b\mid D\) | \(a=D/b-jb\), with \(j=1\) or \(2\) |
| F2 | \(D=AB\) | \(a=(2B-A)/3,\ b=(2A-B)/3\) |
| F3 | \(D/3=AB\), if \(3\mid D\) | \(a=2A-B,\ b=B-A\) |
| F4 | \(D=AB\) | \(a=B-A,\ b=2A-B\) |

For Group 1 retain positive integer square roots with \(0<u<v\) and \(\gcd(u,v)=1\). For norm rows retain positive integral \(a,b\), \(\gcd(a,b)=1\), and an integral positive \(c\) satisfying the required norm. F2 uses \(A=a+2b,B=2a+b\); F3 uses \(A=a+b,B=a+2b\); F4 uses \(A=a+b,B=2a+b\). Both factor orders are tested where appropriate.

No unbounded search over rational points is hidden in these procedures. A witness to \(\mathcal P(D)\) is a witness to a necessary coefficient and an eventual construction, not automatically to a \(D\)-tiling.

## 5. The prime-power coefficient bound

**Lemma 5.1.** Let \(d\ge2\) be even and squarefree, \(q\) an odd prime, and \(r\ge0\). If a product coefficient from the nine rows equals

\[
D=dq^{2r},
\]

then \(q^r<2d\).

**Proof.** The assertion is immediate for \(r=0\). Suppose \(r\ge1\).

The factors \(b,Q\) and \(Q,P\) are coprime. In the norm rows, \(a,b\), \(b,a+b\), \(b,a+2b\), \(a+b,2a+b\), and \(a+b,a+2b\) are coprime. The gcd of \(a+2b,2a+b\) divides 3 and is also 1: otherwise \(a\equiv b\not\equiv0\pmod3\), and writing \(b=a+3z\) gives

\[
c^2=3a^2+9az+9z^2\equiv3\pmod9,
\]

which is impossible. Thus the prime \(q\), including \(q=3\), cannot split between the two product factors.

For every row except F3, one factor is therefore free of \(q\) and divides \(d\), so is at most \(d\). This remains true when \(q\mid d\): its entire exponent \(2r+1\) then belongs to the other factor. We bound each product using this small factor.

**Group-1 alpha.** If \(Q\le d\), then \(b<Q\) and \(D<d^2\). If \(b\le d\), use

\[
b=(v-u)(v+u)\ge v+u>v
\]

to obtain \(Q<2v^2<2d^2\), hence \(D<2d^3\).

**Group-1 QP.** Since \(Q<P<2Q\), a factor at most \(d\) forces \(D<2d^2\).

**A norm side bound.** If \(B\) is one of \(a,b\) and \(A\) the other, then

\[
\begin{aligned}
(2c-2A-B)(2c+2A+B)&=3B^2&&\text{for the plus norm},\\
(2c-2A+B)(2c+2A-B)&=3B^2&&\text{for the minus norm}.
\end{aligned}
\tag{5.1}
\]

Both factors in the applicable identity are positive integers: this follows from \(c^2-(A\pm B/2)^2=3B^2/4>0\). The first factor is at least 1. Comparing the second factor with \(4A+2B\), or \(4A-2B\), gives the adequate bounds

\[
A<\frac{3B^2}{4}\quad\text{in the plus case},
\qquad
A<\frac{3B^2+2B}{4}\quad\text{in the minus case}.
\tag{5.2}
\]

**The two equilateral rows.** One side \(B\le d\). Therefore

\[
D=AB<\frac{d(3d^2+2d)}4\le d^3
\qquad(d\ge2).
\]

**F1 and isosceles.** Write \(D=b(a+jb)\), \(j=1,2\). If \(a+jb\le d\), then \(D\le d^2\). Otherwise \(b\le d\), and the plus side bound gives

\[
a+jb<\frac34d^2+2d\le\frac74d^2,
\]

so \(D<2d^3\).

**F2 and F4.** A positive linear factor at most \(d\) bounds both \(a,b<d\). The other factor is less than \(3d\), giving \(D<3d^2<2d^3\) for \(d\ge2\).

**F3.** Put \(A=a+b\), \(B=a+2b\), so \(A<B<2A\) and \(D=3AB\). If \(q\ne3\), necessarily \(3\mid d\), and a \(q\)-free factor of \(AB\) divides \(d/3\). If \(q=3\), removing the initial factor 3 leaves a power of 3 times a divisor of \(d\); coprimality again makes one factor at most \(d\). In either case a factor is at most \(d\), and \(A<B<2A\) gives

\[
D<6d^2\le3d^3<4d^3.
\]

All nine rows satisfy \(D<4d^3\). Since \(D=dq^{2r}\), it follows that \(q^r<2d\). ∎

## 6. Exhausting all thirteen rows

Fix even squarefree \(d\), an odd prime \(q\), and an integer \(k\ge0\), and suppose \(dq^{2k}\in\mathcal S\).

Any integer square scale \(t\) in a necessary spectrum divides \(q^k\): every prime other than \(q\) occurs in \(dq^{2k}\) to exponent at most 1, while the exponent of \(q\) is \(2k\) or \(2k+1\). Thus

\[
t=q^j,\quad0\le j\le k,
\qquad D=dq^{2(k-j)}.
\tag{6.1}
\]

The two primitive difference-of-squares rows are impossible. Indeed, \(v^2-u^2\) is odd or divisible by 8 for coprime \(u,v\), whereas \(v_2(dq^{2k})=1\) and \(t\) is odd.

The classical rows force \(C_0(d)\). In the sum-of-two-squares case each odd prime congruent to 3 modulo 4 has even valuation, while every prime dividing the squarefree kernel \(d\) has odd valuation. The other classical square multiples allow only kernels \(1,2,3,6\).

A W tiling forces \(C_W(d)\). If an odd prime inert for 2 divided \(Q=2v^2-u^2\), it would divide both \(u,v\), contradicting primitivity. Every prime of \(d\) divides this coefficient to odd exponent.

A beta-isosceles tiling similarly forces all primes \(p\mid d\), \(p>3\), to split for 3. Its primitive coefficient \(P=3v^2-u^2\) has 3-adic valuation either 0 or 1. If \(3\nmid P\), then \(P\equiv2\pmod3\); if \(3\mid P\), write \(u=3z\), obtaining \(P/3=v^2-3z^2\equiv1\pmod3\). In (6.1), when \(q\ne3\) its even power is 1 modulo 3; when \(q=3\), a positive residual exponent \(k-j\) is impossible because it would give \(v_3(P)\ge2\). The precise sign conditions (1.1) follow in all cases. Thus \(C_B(d)\) holds.

Every remaining tiling belongs to one of the nine product rows. Lemma 5.1 forces its coefficient to be one of the finite values tested in (1.3). We have proved

\[
dq^{2k}\in\mathcal S\quad\Longrightarrow\quad\mathsf R(d,q).
\tag{6.2}
\]

This argument uses all thirteen nonclassical rows and all classical exceptions. In particular, neither \(q=3\) nor \(q\mid d\) is omitted.

## 7. Completion of both criteria

If \(\mathsf R(d,q)\) holds because \(d\) is odd or because of a classical, W, or beta condition, the prior constructions in Section 3 give \(dm^2\) for all sufficiently large \(m\), hence \(dq^{2k}\) for all sufficiently large \(k\).

Otherwise a finite witness supplies a primitive row with coefficient \(D=dq^{2r}\). Let \(T\) be a computable sufficient integer multiplier threshold for that fixed tile and target. Every \(k\ge r\) satisfying \(q^{k-r}\ge T\) is then constructible, since

\[
(dq^{2r})(q^{k-r})^2=dq^{2k}.
\]

This proves the positive direction of Theorem 2.2. Together with (6.2), it proves the full equivalence and the assertion that a negative test excludes every exponent. One may take the sufficient exponent threshold

\[
K=r+\min\{h\ge0:q^h\ge T\},
\]

using integer powers rather than floating-point logarithms.

If \(\mathsf T(d)\) holds, its witness similarly constructs every sufficiently large ordinary multiplier. For a witness to \(\mathcal P(d)\), simply use the fixed-row threshold with coefficient exactly \(d\). Thus Theorem 2.1(1) implies (3), which implies (2).

Conversely, suppose all sufficiently large odd multipliers are admissible. If \(d\) is odd, the test already holds. Otherwise choose a prime \(q>2d\) larger than the assumed multiplier threshold. By (6.2), \(\mathsf R(d,q)\) holds; but \(q^r<2d\) permits only \(r=0\). Therefore \(\mathsf R(d,q)\) reduces exactly to \(\mathsf T(d)\). This proves necessity and finishes Theorem 2.1. The same observation yields (2.1) when the tail test fails.

For a nonsaturated even kernel, only the finitely many odd primes \(q<2d\) can support any prime-power multiplier at all. Their ray tests involve coefficients bounded uniformly by \(4d^3\).

## 8. Square class 22 and the limitation of elliptic witnesses

For this kernel the exclusion has a short direct proof, so it need not depend on the finite ray-test computation:

\[
\boxed{22q^{2k}\notin\mathcal S
\quad\text{for every odd prime }q\text{ and every }k\ge0.}
\tag{8.1}
\]

**Proof.** Suppose there is a tiling. Every necessary coefficient has the form \(D=22q^{2r}\) for some \(r\ge0\), so \(D\equiv6\pmod8\). The classical square classes and beta sign condition exclude those branches: kernel 22 is neither a classical exceptional kernel nor a sum-of-two-squares kernel, and \(22\equiv1\pmod3\). W is excluded by the prime 11, which is inert for 2. The two difference-of-squares rows are excluded by their 2-adic valuation.

In a primitive norm triple, an even side is divisible by 8; when both sides are odd, the plus norm gives \(a+b\equiv0\pmod8\), while the minus norm gives \(ab\equiv1\pmod8\). Substitution into the seven norm coefficients shows that only F3 can have residue 6 modulo 8. The only remaining branches are therefore Group-1 alpha, Group-1 QP, and F3.

In the two Group-1 rows the residue 6 forces \(Q\) to be even. Its other factor, \(b\) or \(P\), is coprime to \(Q\); moreover \(11\nmid Q\), since \(2\) is a quadratic nonresidue modulo 11. If \(q\nmid Q\), including the case \(q=11\), this forces \(Q=2\), impossible for \(0<u<v\). Otherwise \(Q=2q^{2r}\) and the complementary factor is 11. In alpha, \(b=11\) forces \((u,v)=(5,6)\), giving the odd value \(Q=47\). In QP, \(P=11\) forces \((u,v)=(1,2)\), giving the odd value \(Q=7\). Both contradict evenness of \(Q\).

For F3, divisibility by 3 forces \(q=3\) and \(r\ge1\). Put \(A=a+2b\), \(B=a+b\). The primitive norm congruence used in Lemma 5.1 gives \(3\nmid A\), so

\[
3AB=22\cdot3^{2r}\quad\Longrightarrow\quad A\mid22.
\]

Since \(A\ge3\), only \(A=11,22\) are possible. For each, \(a=A-2b>0\) and

\[
c^2=A^2-3Ab+3b^2,
\qquad1\le b\le\lfloor(A-1)/2\rfloor.
\]

Checking these two explicitly bounded quadratic lists gives exactly:

| \(A\) | \(b\) | \(a\) | \(c\) | Exclusion |
|---:|---:|---:|---:|---|
| 11 | 3 | 5 | 7 | \(D=264\) has 2-adic valuation 3 |
| 22 | 6 | 10 | 14 | Nonprimitive triple |
| 22 | 7 | 8 | 13 | \(D=990=22\cdot3^2\cdot5\) has an extra factor 5 |

No F3 candidate remains, proving (8.1). ∎

As a separate regression, the finite coefficient tests are empty for all 17 values \(D=22s^2\) where \(s=1\) or \(s\) is an odd prime power less than 44. Inverse divisor enumeration and forward Group-1/conic enumeration agree. Their [reproducible checks](../research/square-class-tails/) corroborate the proof above; they are not a replacement for its complete branch argument.

This does not exclude the whole square class. The [previous QP construction](../research/uniform-sectors/PROOF.md) supplies an admissible count with

\[
m=248599631=7\cdot3089\cdot11497,
\qquad
22m^2=1359639083733395542.
\]

Its coprime factors are \(Q=2(7\cdot3089)^2\) and \(P=11\cdot11497^2\). Distinct prime factors of the multiplier are distributed between the two coefficient factors, so the prime-power argument does not apply.

More generally, a QP square-class witness satisfies

\[
(2v^2-u^2)(3v^2-u^2)=ds^2.
\]

With \(x=u/v\), \(y=s/v^2\), this becomes the genus-one equation

\[
(2-x^2)(3-x^2)=dy^2,\qquad0<x<1.
\]

It maps to \(E_d:Y^2=X(X-2d)(X-3d)\) by \(X=dx^2\), \(Y=d^2xy\). Conversely, a rational point on \(E_d\) in \(0<X<d\) recovers such a witness only when \(X/d\) is a rational square. That extra square condition must not be discarded.

A witness with coefficient \(ds^2\) constructs multiples \(m\) divisible by \(s\); it does not by itself fill all large odd multipliers. Theorems 2.1–2.2 show that elliptic point searches are unnecessary for the two finite decision problems settled here. They can still matter for individual composite multipliers outside these criteria.

## Appendix A. Every-integer tails for all norm rows

The following positive geometry is existing work, not a new construction claimed in this note. It is recalled to make clear that the sufficiency arguments require no hidden divisibility of the multiplier.

For a primitive plus-norm tile let \(\alpha+\beta=\pi/3\), with sides \(a,b,c\) opposite \(\alpha,\beta,2\pi/3\). Put

\[
A=\max(a,b),\quad B=\min(a,b),\quad
U=a+2b,\quad V=2a+b,\quad W=a+b.
\]

The repository's [general-spectra construction](../research/general-spectra/PROOF.md) tiles an equilateral triangle of side \(abm\) for **every integer**

\[
m\ge M=3(\lfloor A/B\rfloor+2).
\]

For the minus norm the corresponding safe threshold is \(M_{60}=3(\lfloor A/B\rfloor+1)\). The equilateral tile itself is classical.

Starting from the plus-norm equilateral core, attach one ordinary \(bm\)-scaled tile triangle along a full side. The 60-degree corner and the attached 120-degree corner straighten, producing F1 with sides \(m(ab,bc,bW)\) and count \(bWm^2\). A second \(bm\)-scaled tile triangle similarly gives the isosceles target \(m(bc,bc,bU)\), with count \(bUm^2\). Each attached piece lies across a complete boundary side, with disjoint interior.

For F2, take a triangle \(ABC\) with angles \(2\beta,2\alpha,\pi/3\), sides \(AB=c^2m\), \(AC=aUm\), \(BC=bVm\), and incenter \(I\). The triangle \(AIB\) is a \(cm\)-scaled tile: its other sides are \(AI=acm\), \(BI=bcm\). Choose \(P\in AC\) with \(AP=a^2m\) and \(Q\in BC\) with \(BQ=b^2m\). Then \(AIP\) and \(BIQ\) are ordinary tile triangles of scales \(am,bm\), with \(PI=IQ=abm\). The points \(P,I,Q\) are collinear; \(PC=CQ=PQ=2abm\). Thus the remaining region \(PCQ\) is an equilateral core of side \(2abm\). This is a positive four-piece partition, since \(I\) is interior and \(P,Q\) lie strictly on their specified sides. The total is

\[
(c^2+a^2+b^2+4ab)m^2=UVm^2.
\]

It works for every integer \(m\ge\lceil M/2\rceil\), with no parity restriction on \(m\).

Attach a \(Um\)-scaled tile to F2 along its side \(aUm\), placing the 120-degree corner against the old 60-degree corner. The union is F3 with sides \(m(c^2,cU,3bW)\) and count

\[
(UV+U^2)m^2=3UWm^2.
\]

Finally, start with the swapped F1 target, with sides \(m(ab,ac,aW)\). Attach a \(Wm\)-scaled tile along its full side \(aWm\), again straightening a 60-degree corner with a 120-degree corner. This gives F4 with sides \(m(ac,bV,cW)\) and count

\[
(aW+W^2)m^2=VWm^2.
\]

All additional triangles have integer scales and hence ordinary quadratic grid tilings. A safe sufficient-threshold table is therefore:

| Norm row | Every integer multiplier at or above |
|---|---:|
| 60-degree equilateral | \(M_{60}\) |
| 120-degree equilateral, F1, isosceles, F4 | \(M\) |
| F2 and F3 | \(\lceil M/2\rceil\) |

The narrower reflected-corner construction in the recent trapezoid note is not an input to this all-ratio statement.

## Sources and attribution

- **[BZ]** Michael Beeson and Yan X Zhang, *Rationality of certain triangle tilings*, arXiv:2604.01314v1, Table 1 and Theorem 1.2: [article](https://arxiv.org/html/2604.01314v1). The angular classification is attributed there to Laczkovich.
- **Prior project necessary spectra:** [uniform reduction](../research/uniform-reduction/PROOF.md) and [uniform sectors](../research/uniform-sectors/PROOF.md). The new argument uses their integral-scale necessity, not a claim of small-scale sufficiency.
- **Prior project constructive tails:** [universal rational scales](universal-rational-scales.md), [explicit theta seeds](explicit-theta-seeds.md), [square-class saturation](../research/square-class-saturation/PROOF.md), and [general spectra](../research/general-spectra/PROOF.md), with their existing attributions.
- **Harries/Zhang positive transfers:** Jan Philipp Harries, *New constructions, obstructions, and multiplier structure for Erdős Problem 634*, v0.5, 28 August 2026, [pinned source](https://github.com/jphme/math-problems/blob/67838578b5bd26aa66034fa46da96141be75de0e/progress634/progress634.tex), Corollary “Finite generator windows” and appendix “Addition data and constructive transfers.” Source blob SHA-1: `85536aabe013ad393e33985cbfcadbae50722f08`. Its rows E, I, III, IV, V, II correspond here to equilateral, isosceles, F4, F1, F2, F3. Harries credits the relevant positive transfers to Zhang's arXiv:2512.22696v4 and supplies the F2 bisector partition. Only these positive constructions are used; that manuscript's obsolete Group-1 divisibility and prime-case claims are not inputs.

The criterion's new content is the finite coefficient bound and its consequences for cofinal square classes and fixed prime-power rays. Small-exponent membership and multipliers with several distinct prime factors remain separate questions.
