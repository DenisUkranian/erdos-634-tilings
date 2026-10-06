# A quantitative upper bound for congruent triangle tile counts

**Erdős problem 634 — research directed by Denis Paliy, with ChatGPT assistance**  
**6 October 2026**

Let \(\mathcal S\) be the set of positive integers \(N\) for which some nondegenerate triangle admits a dissection into \(N\) congruent nondegenerate triangles. Reflections and arbitrary T-junctions are permitted. Write

\[
S(X)=\#\bigl(\mathcal S\cap[1,X]\bigr).
\]

This note combines the necessary geometric scale bounds proved in [Long one-type seams and the density question](long-seams-density.md) with Kevin Ford's established estimate for integers possessing a divisor in a short multiplicative interval. It gives a quantitative strengthening of the project's **1 October 2026** zero-density argument. The earlier qualitative conclusion \(S(X)=o(X)\) and its fixed-scale/tail proof are prior project work, not new findings of this note.

The exhaustive triangle classification and rationality theorem, the necessary count spectra, the long-seam inequalities, and Ford's theorem are explicit inputs. The quantitative summation combining them is given below. No external priority, referee acceptance, or formal verification is claimed. This does **not** classify membership in \(\mathcal S\), and does not solve Erdős problem 634 in full.

## 1. Statement and dependencies

All logarithms are natural. Put

\[
\delta=1-\frac{1+\log\log 2}{\log 2}
=0.086071\ldots .
\]

**Theorem.** Under the exhaustive classification, necessary spectra, and geometric scale bounds specified below,

\[
\boxed{
S(X)\ll
\frac{X}{(\log X)^\delta(\log\log X)^{3/2}}
\qquad (X\longrightarrow\infty).
}
\tag{1.1}
\]

The implied constant does not depend on \(X\). In particular, admissible counts have natural density zero. No matching lower bound or optimality assertion for \(S(X)\) follows from this argument. Ford's sharp estimate for general divisor sets does not establish sharpness for triangle tilings.

The geometric classification is Laczkovich's classification as recorded in Beeson–Zhang, Table 1; Beeson–Zhang's Theorem 1.2 supplies the rationality input after the classical exceptions are separated [BZ]. The necessary integral-scale spectra and their signed-direction derivations are recorded in [the uniform-sectors proof](../research/uniform-sectors/PROOF.md), Section 2, with the underlying calculations in [the uniform-reduction proof](../research/uniform-reduction/PROOF.md). Their use here includes arbitrary T-junctions: internal edge contributions cancel after subdivision, without assuming that partial interior edges have integral lengths.

The only extra geometric restrictions required for the two remaining isosceles rows are

\[
\begin{array}{ll}
\text{Group-1 theta:}&t(v^2-u^2)\ge uv,\\[2mm]
\text{double angle:}&t(v^2-u^2)\ge u^2.
\end{array}
\tag{1.2}
\]

Their complete source-to-relation and boundary arguments are in [the long-seam proof](long-seams-density.md). The arithmetic proof below needs only their common consequence

\[
u^2\le t(v^2-u^2).
\tag{1.3}
\]

No proposed scale-one exclusion for W or beta-isosceles targets, proposed all-primes classification, withdrawn packing lemma, or unproved construction-specific divisibility is used.

## 2. Exhaustive necessary count families

The classical cases contribute only counts in

\[
\{r^2,\ r^2+s^2,\ 2r^2,\ 3r^2,\ 6r^2:r,s\ge1\}.
\tag{2.1}
\]

For Group 1 put

\[
(a,b,c)=(uv,v^2-u^2,v^2),\qquad
Q=2v^2-u^2,\qquad P=3v^2-u^2,
\]

where \(0<u<v\) and \(\gcd(u,v)=1\). For the double-angle row the primitive tile is \((u^2,v^2-u^2,uv)\), with \(0<u<v<2u\) and \(\gcd(u,v)=1\). Every row below has the form \(N=dt^2\), with **integer** \(t\ge1\).

| Target family | Necessary coefficient \(d\) | Estimate used |
|---|---:|---|
| Group-1 W | \(Q\) | Quadratic-character envelope |
| Group-1 beta-isosceles | \(P\) | Quadratic-character envelope |
| Group-1 theta-isosceles | \(b\) | \(tb\ge uv\), then Section 3 |
| Group-1 alpha-isosceles | \(bQ\) | Sparse parameter count |
| Group-1 other scalene | \(QP\) | Sparse parameter count |
| Double-angle isosceles | \(v^2-u^2\) | \(t(v^2-u^2)\ge u^2\), then Section 3 |

For primitive norm triples \(c^2=a^2\pm ab+b^2\), with \(a,b>0\) and \(\gcd(a,b)=1\), the remaining necessary rows are:

| Target family | Norm sign | Necessary coefficient \(d\) |
|---|:---:|---:|
| 60-degree equilateral | \(-\) | \(ab\) |
| 120-degree equilateral | \(+\) | \(ab\) |
| 120-degree F1 | \(+\) | \(b(a+b)\) |
| 120-degree isosceles | \(+\) | \(b(a+2b)\) |
| 120-degree F2 | \(+\) | \((a+2b)(2a+b)\) |
| 120-degree F3 | \(+\) | \(3(a+2b)(a+b)\) |
| 120-degree F4 | \(+\) | \((2a+b)(a+b)\) |

Both orders of \(a,b\) are included. These are thirteen necessary nonclassical spectra, not thirteen new existence assertions. Together they divide into two isosceles rows treated in Section 3, two quadratic-character rows, and nine sparse rows. Allowing \(t=1\) in the isosceles rows only enlarges the set being bounded; their separate scale-one exclusions are unnecessary here.

## 3. A uniform bound for the two isosceles rows

We first prove an arithmetic statement that overcovers both rows. Let \(\mathcal R\) be the set of integers having a representation

\[
N=t^2(v^2-u^2),\qquad
t\ge1,\quad 0<u<v,\quad
u^2\le t(v^2-u^2),
\tag{3.1}
\]

with all three parameters integral. Neither coprimality nor the double-angle restriction \(v<2u\) is imposed.

**Lemma 3.1.** With \(A(X)=(\log X)^\delta(\log\log X)^{3/2}\),

\[
\#\bigl(\mathcal R\cap[1,X]\bigr)\ll X/A(X).
\tag{3.2}
\]

**Analytic input.** Let \(H(x,y,2y)\) count the positive integers at most \(x\) possessing a divisor in \((y,2y]\). Ford proves [F, equation (1.1)]

\[
H(x,y,2y)\ll
\frac{x}{(\log y)^\delta(\log\log y)^{3/2}}
\qquad(3\le y\le\sqrt x),
\tag{3.3}
\]

uniformly with an absolute implied constant. We use only this upper bound. Uniformity is essential because both the scale and the divisor intervals vary with \(X\).

**Proof of Lemma 3.1.** Write \(b=v^2-u^2\). First remove all representations with \(t>X^{1/8}\). Even without (3.1), their counts lie in a set of size at most

\[
\sum_{t>X^{1/8}}\left\lfloor\frac{X}{t^2}\right\rfloor
\ll X^{7/8}.
\tag{3.4}
\]

Among the remaining scales \(t\le X^{1/8}\), coefficients \(b<X^{1/2}\) contribute at most \(X^{5/8}\) pairs \((t,b)\), hence at most that many distinct counts.

Fix a remaining \(t\), and partition \(X^{1/2}\le b\le X/t^2\) into dyadic shells \(B<b\le2B\), with \(B\ge X^{1/2}/2\). Empty shells are ignored. Their endpoints can be covered by including them in an adjacent shell. Factor

\[
b=(v-u)(v+u)=rs,\qquad r<s.
\]

By (3.1), \(v^2\le(t+1)b\), so

\[
s\le2\sqrt{(t+1)b},\qquad
\frac{\sqrt B}{2\sqrt{t+1}}\le r<\sqrt{2B}.
\tag{3.5}
\]

Put \(Z=\sqrt{2B}\) and \(\ell=\sqrt B/(2\sqrt{t+1})\). Cover \([\ell,Z]\) by the intervals

\[
\left(\frac Z{2^{j+1}},\frac Z{2^j}\right],
\qquad 0\le j\le J,
\tag{3.6}
\]

where \(J\) is the first index for which \(Z/2^{J+1}<\ell\). There are \(O(1+\log(t+1))\) intervals. Each lower endpoint \(y\) satisfies

\[
\ell/2\le y\le Z/2\le\sqrt{2B}.
\]

Since \(B\ge X^{1/2}/2\) and \(t+1\le2X^{1/8}\), these endpoints also satisfy \(y\ge X^{3/16}/8\). Thus, for large \(X\), all hypotheses of (3.3) hold with \(x=2B\), and the denominator there is comparable to \(A(X)\), uniformly in \(t,B,j\).

Every admissible coefficient \(b\) in this shell possesses its divisor \(r\) in at least one interval (3.6). The shell therefore contains at most

\[
\ll\frac{(1+\log(t+1))B}{A(X)}
\]

distinct admissible coefficients. The sum of its dyadic shell sizes \(B\) is \(O(X/t^2)\). Consequently the contribution at this scale is

\[
\ll\frac{(1+\log(t+1))X}{t^2A(X)}.
\]

Finally,

\[
\sum_{t\ge1}\frac{1+\log(t+1)}{t^2}<\infty.
\]

Summing over the retained scales gives \(O(X/A(X))\). The previously discarded contributions \(O(X^{7/8}+X^{5/8})\) are smaller, proving (3.2). Repeated representations only enlarge these upper bounds. No uncontrolled exchange of an infinite sum and a fixed-scale limit occurs. ∎

This divisor-interval argument retains the full factor \((\log\log X)^{3/2}\) in the denominator. Applying only the square multiplication-table bound separately at each growing scale would lose a logarithmic factor in the subsequent summation.

## 4. The quadratic-character envelopes

For \(\chi\) one of the real primitive quadratic characters of discriminant \(-4,8,12\), define

\[
\mathcal E_\chi=
\{n\ge1:v_p(n)\text{ is even whenever }\chi(p)=-1\}.
\]

**Lemma 4.1.** For each of these three fixed characters,

\[
\#\bigl(\mathcal E_\chi\cap[1,X]\bigr)
\ll X/\sqrt{\log X}.
\tag{4.1}
\]

**Proof.** Let \(f\) be the multiplicative indicator of \(\mathcal E_\chi\), and let \(F(s)=\sum_{n\ge1}f(n)n^{-s}\) for real \(s>1\). Checking the Euler factors gives

\[
F(s)=\zeta(s)^{1/2}L(s,\chi)^{1/2}
\prod_{\chi(p)=-1}(1-p^{-2s})^{-1/2}
\prod_{\chi(p)=0}(1-p^{-s})^{-1/2}.
\tag{4.2}
\]

The first extra product is uniformly bounded as \(s\downarrow1\), since \(\sum_p p^{-2}\) converges; the ramified-prime product is finite and bounded. The periodic mean-zero character has bounded partial sums, so summation by parts shows that \(L(s,\chi)\) is bounded for real \(s\) near 1. The positive square roots in (4.2) are supplied by the Euler products for \(s>1\). Together with \(\zeta(s)\ll(s-1)^{-1}\), this gives

\[
F(1+1/\log X)\ll\sqrt{\log X}.
\]

Since \(n^{1/\log X}\le e\) for \(n\le X\),

\[
\sum_{n\le X}\frac{f(n)}n
\le eF(1+1/\log X)
\ll\sqrt{\log X}.
\tag{4.3}
\]

Define \(\Lambda_f\) by \(-F'(s)/F(s)=\sum_{n\ge1}\Lambda_f(n)n^{-s}\). Its only nonzero values occur on prime powers. If \(\chi(p)\ne-1\), then \(\Lambda_f(p^k)=\log p\) for every \(k\ge1\). If \(\chi(p)=-1\), then \(\Lambda_f(p^{2k})=2\log p\) and \(\Lambda_f(p^{2k-1})=0\). Hence

\[
0\le\Lambda_f(n)\le2\Lambda(n),
\]

where \(\Lambda\) is the von Mangoldt function. The elementary Chebyshev estimate \(\sum_{d\le Y}\Lambda(d)\ll Y\), the coefficient identity \(f(n)\log n=(f*\Lambda_f)(n)\), and (4.3) imply

\[
\begin{split}
\sum_{n\le X}f(n)\log n
&=\sum_{m\le X}f(m)\sum_{d\le X/m}\Lambda_f(d)\\
&\ll X\sum_{m\le X}\frac{f(m)}m
\ll X\sqrt{\log X}.
\end{split}
\]

Split the unweighted sum at \(\sqrt X\). Below that point use \(f\le1\); above it use \(\log n\ge\tfrac12\log X\). This yields

\[
\sum_{n\le X}f(n)
\le\sqrt X+\frac2{\log X}\sum_{n\le X}f(n)\log n
\ll X/\sqrt{\log X}.
\]

This proof uses no prime number theorem in arithmetic progressions and no separate multiplicative mean-value theorem. ∎

A sum of two squares lies in \(\mathcal E_{\chi_{-4}}\). Positive integers \(2x^2-y^2\) and \(3x^2-y^2\) lie in \(\mathcal E_{\chi_8}\) and \(\mathcal E_{\chi_{12}}\), respectively: if an inert prime divides the form, it divides both variables; repeatedly divide by its square. The W and beta-isosceles rows remain in these envelopes after arbitrary square scaling, by taking \((x,y)=(tv,tu)\). The classical single-square multiples in (2.1) contribute only \(O(\sqrt X)\).

## 5. The nine sparse rows

For completeness, the parameter bound used here is summarized from [the uniform-sectors proof](../research/uniform-sectors/PROOF.md), Lemmas 5.1–5.2.

Primitive positive solutions of \(c^2=a^2+ab+b^2\) with \(ab\le Y\) number \(O(\sqrt Y)\). Write the reduced rational slope \((c-a)/b=h/k\), with \(k/2<h<k\). The standard conic parameterization is

\[
a=\frac{k^2-h^2}{g},\qquad
b=\frac{k(2h-k)}g,\qquad
c=\frac{h^2-hk+k^2}g,
\qquad g\in\{1,3\}.
\]

Set \(d=k-h\), \(e=2h-k\). Both are positive, \(k=2d+e\), and

\[
ab\ge\frac{k^3\min(d,e)}{27}.
\]

For fixed \(k\), at most two pairs have a prescribed \(\min(d,e)\). Summation gives

\[
\sum_{k\ge1}O\!\left(\min\{k,Y/k^3\}\right)=O(\sqrt Y),
\]

by splitting at \(k=Y^{1/4}\). The minus-norm case reduces, after choosing \(a>b\), to the plus-norm pair \((a-b,b)\), whose product is at most \(ab\). The primitive exception \(a=b=1\) is classical. Each of the seven norm-row coefficients is at least \(ab\), so every such row has \(O(\sqrt Y)\) primitive parameter pairs with coefficient at most \(Y\).

For the other two sparse rows, put \(d=v-u\). The inequalities

\[
bQ\ge dv^3,\qquad QP>2v^4
\]

give the same \(O(\sqrt Y)\) bound: in the first case sum \(O(\min(v,Y/v^3))\) over \(v\); in the second sum at most \(v\) choices up to \(v<(Y/2)^{1/4}\). Dropping coprimality in these upper bounds is harmless.

Allowing all integer square scales therefore contributes at most

\[
\sum_{t\le\sqrt X}O\!\left(\sqrt{X/t^2}\right)
=O(\sqrt X\log(2X))
\tag{5.1}
\]

across these nine rows. This is an upper bound on all arithmetic candidates, whether or not their tilings exist.

## 6. Completion of the bound and its limits

The exhaustive list in Section 2 partitions the nonclassical possibilities into:

1. two isosceles rows contained in \(\mathcal R\), by the geometric inequalities (1.2);
2. two quadratic-character rows covered by Lemma 4.1;
3. nine sparse rows covered by (5.1).

The classical counts are also covered by Lemma 4.1 and \(O(\sqrt X)\). Consequently

\[
S(X)\ll
\frac{X}{A(X)}
+\frac{X}{\sqrt{\log X}}
+\sqrt X\log(2X).
\]

Since \(\delta<1/2\), the latter two terms are \(o(X/A(X))\). This proves (1.1).

The argument controls the size of an explicit necessary arithmetic envelope. It supplies neither an existence construction for every number inside that envelope nor an impossibility proof for every exceptional number. Its constants are not supplied as practical finite-range exclusion percentages. The problem of deciding every remaining tile count, including all small-scale geometric cases, remains separate.

## 7. Attribution and sources

- **[F]** Kevin Ford, *Integers with a divisor in \((y,2y]\)*, equation (1.1), author's revised exposition: [PDF](https://www.ford126.web.illinois.edu/wwwpapers/hxy2y.pdf). The uniform divisor-interval estimate and the constant \(\delta\) are Ford's results; the underlying qualitative multiplication-table theorem is due to Erdős.
- **[BZ]** Michael Beeson and Yan X Zhang, *Rationality of certain triangle tilings*, arXiv:2604.01314v1, Table 1 and Theorem 1.2: [article](https://arxiv.org/html/2604.01314v1). The angular classification is attributed there to Laczkovich; rationality is the additional input used here.
- **Prior project spectra.** [Uniform arithmetic sectors and asymptotic concentration](../research/uniform-sectors/PROOF.md), 1 October 2026, Sections 2 and 5, and its cited 30 September necessary-spectrum derivations. These precede the present quantitative estimate.
- **Prior project qualitative density argument and geometric input.** [Long one-type seams and the density question](long-seams-density.md). Its 1 October provenance and subsequent audit are recorded there. The qualitative zero-density conclusion is not relabeled as new work on 6 October.

This note does not assert first priority for the integrated tiling estimate. The complete source dependencies and the distinction between old qualitative work and the quantitative deduction are retained so that an external reader can check them separately.
