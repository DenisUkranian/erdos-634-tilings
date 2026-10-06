# Effective finite bases on a fixed prime support

**Research directed by Denis Paliy, with ChatGPT assistance — 6 October 2026**

Let \(\mathcal S\) be the set of positive integers that count congruent nondegenerate triangles in a dissection of a nondegenerate triangle. Reflections and arbitrary T-junctions are allowed. Fix a positive squarefree integer \(d\) and a finite set \(H\) of primes, and write

\[
\mathcal M(H)=\left\{\prod_{p\in H}p^{e_p}:e_p\ge0\right\}.
\]

The empty product is 1. We call these multipliers \(H\)-smooth.

This note gives a uniform effective reduction over **all exponents on a fixed prime support**. Its arithmetic step uses a published effective unit-equation theorem. Its geometric inputs are the previously established necessary spectra and constructive tails. No unit-equation solver has been run here, no practical bound is claimed, and this does not solve the unrestricted classification in Erdős problem 634. External priority and referee acceptance have not been established.

## 1. The finite-basis theorem

**Theorem 1.1.** Given \(d,H\), one can compute a finite set \(B\subseteq\mathcal M(H)\) and positive integers \(T_s\), one for each \(s\in B\), with the following properties:

1. If \(m\in\mathcal M(H)\) and \(dm^2\in\mathcal S\), then some \(s\in B\) divides \(m\).
2. If \(s\in B\), \(s\mid m\), and \(m/s\ge T_s\), then \(dm^2\in\mathcal S\).

Consequently, for

\[
M=\max\bigl(\{1\}\cup\{sT_s:s\in B\}\bigr),
\]

every \(H\)-smooth \(m\ge M\) satisfies

\[
\boxed{dm^2\in\mathcal S\quad\Longleftrightarrow\quad
\text{some }s\in B\text{ divides }m.}
\tag{1.1}
\]

The elements of \(B\) are generators for an eventual divisibility criterion. They are **not necessarily realizable at multiplier one**: \(ds^2\) itself need not lie in \(\mathcal S\).

If \(B\) is empty, no multiplier on this support is admissible, at any size. If \(H\) is nonempty, existence of any admissible multiplier on this support is equivalent to \(B\ne\varnothing\): any fixed prime of \(H\) can enlarge a residual multiplier beyond \(T_s\). For empty \(H\), only the individual count \(d\) remains.

An additional use of the already known fixed-count decision procedure turns (1.1) into an exact finite divisibility basis, including all small multipliers; see Section 6. The effective bound is essential. Abstract existence of a finite divisibility basis already follows from grid refinement and Dickson's lemma.

## 2. Prior inputs and the nine residual rows

We use the inputs and finite cofinal test \(\mathsf T(d)\) of [square-class tails](square-class-tails.md). If that test passes, the previous constructions supply every sufficiently large \(dm^2\), with a computable sufficient threshold. Every odd \(d\) passes. If it fails, \(d\) is even, and the classical, W, and beta conditions \(C_0(d),C_W(d),C_B(d)\), together with the exact product-coefficient test \(\mathcal P(d)\), all fail.

The exhaustive classification and integral-scale reductions give \(N=Dt^2\), with a **positive integer** \(t\), in thirteen nonclassical primitive rows. They are recorded in [uniform sectors](../research/uniform-sectors/PROOF.md) and [uniform reduction](../research/uniform-reduction/PROOF.md), using the cited Beeson–Zhang classification and rationality inputs. Every fixed primitive witness used below has a computable every-integer multiplier tail. For all seven norm rows, this includes the previous Harries/Zhang positive transfers recalled in Appendix A of [square-class tails](square-class-tails.md).

Suppose \(\mathsf T(d)\) fails and \(m\) is odd. Squarefreeness of \(d\) implies that an integral square scale \(t\) divides \(m\), so

\[
D=d s^2,\qquad s=m/t\mid m.
\tag{2.1}
\]

The two primitive difference-of-squares rows are impossible: for coprime \(u,v\), the coefficient \(v^2-u^2\) is odd or divisible by 8, whereas \(v_2(dm^2)=1\).

The classical rows would force \(C_0(d)\). A W coefficient \(Q=2v^2-u^2\) cannot contain an odd prime inert for 2 in a primitive representation, so it would force \(C_W(d)\). Similarly a beta coefficient \(P=3v^2-u^2\) cannot contain a prime \(p>3\) inert for 3. Moreover \(v_3(P)\in\{0,1\}\); if \(3\nmid P\), then \(P\equiv2\pmod3\), and if \(3\mid P\), then \(P/3\equiv1\pmod3\). Equation (2.1) therefore forces exactly the sign conditions in \(C_B(d)\), even when \(3\mid m\). All three conditions fail.

Thus every remaining actual odd-multiplier count comes from one of these nine product rows. In Group 1 use coprime \(0<u<v\), with \(b=v^2-u^2\), \(Q=2v^2-u^2\), \(P=3v^2-u^2\). In each norm row use positive integers \(a,b,c\), with \(\gcd(a,b)=1\).

| Row | Primitive coefficient \(D\) | Tile condition |
|---|---:|---|
| Group-1 alpha-isosceles | \(bQ\) | As above |
| Group-1 other scalene | \(QP\) | As above |
| 60-degree equilateral | \(ab\) | \(c^2=a^2-ab+b^2\) |
| 120-degree equilateral | \(ab\) | \(c^2=a^2+ab+b^2\) |
| 120-degree F1 | \(b(a+b)\) | Plus norm |
| 120-degree isosceles | \(b(a+2b)\) | Plus norm |
| 120-degree F2 | \((a+2b)(2a+b)\) | Plus norm |
| 120-degree F3 | \(3(a+2b)(a+b)\) | Plus norm |
| 120-degree F4 | \((2a+b)(a+b)\) | Plus norm |

## 3. Quartic parametrizations

The two Group-1 coefficients are the binary quartics

\[
(v^2-u^2)(2v^2-u^2),\qquad
(2v^2-u^2)(3v^2-u^2).
\]

In \(z=u/v\), their projective roots are respectively \(\{\pm1,\pm\sqrt2\}\) and \(\{\pm\sqrt2,\pm\sqrt3\}\).

For either primitive norm triple

\[
c^2=a^2+\sigma ab+b^2,\qquad \sigma\in\{1,-1\},
\]

write \(h/k=(c-a)/b\) in lowest terms, with \(k>0\). Then

\[
\begin{aligned}
A&=k^2-h^2,& B_\sigma&=k(2h-\sigma k),\\
C_\sigma&=h^2-\sigma hk+k^2,&
(a,b,c)&=(A,B_\sigma,C_\sigma)/g,
\end{aligned}
\tag{3.1}
\]

where \(g\in\{1,3\}\). The parameter ranges are \(1/2<h/k<1\) for the plus norm and \(-1/2<h/k<1\) for the minus norm.

To prove completeness, substitute \(c=a+(h/k)b\) into the norm equation; this gives \(a/b=A/B_\sigma\). Since \(\gcd(h,k)=1\), any common divisor of \(A,B_\sigma\) is coprime to \(hk\) and divides \(2h-\sigma k\). Reduction modulo that divisor gives \(3h^2=0\), so it divides 3. When the common divisor is 3 it also divides \(C_\sigma\). Primitivity now gives (3.1). Both orders of \(a,b\) are covered, including the minus-norm triple \((1,1,1)\), which corresponds to \((h,k)=(0,1)\).

For plus norm put

\[
\begin{aligned}
B&=k(2h-k),& W&=A+B=h(2k-h),\\
U&=A+2B=-h^2+4hk-k^2,&
V&=2A+B=-2h^2+2hk+k^2.
\end{aligned}
\]

The seven norm rows become the following quartics. The roots are in \(z=h/k\); infinity denotes a factor \(k\).

| Row | \(g^2D\) | Four distinct projective roots |
|---|---|---|
| 60-degree equilateral | \(AB_{-1}\) | \(-1,1,-1/2,\infty\) |
| 120-degree equilateral | \(AB\) | \(-1,1,1/2,\infty\) |
| F1 | \(BW\) | \(1/2,\infty,0,2\) |
| Isosceles | \(BU\) | \(1/2,\infty,2-\sqrt3,2+\sqrt3\) |
| F2 | \(UV\) | \(2\pm\sqrt3,(1\pm\sqrt3)/2\) |
| F3 | \(3UW\) | \(2-\sqrt3,2+\sqrt3,0,2\) |
| F4 | \(VW\) | \((1-\sqrt3)/2,(1+\sqrt3)/2,0,2\) |

All nine quartics have four distinct roots and split over the fixed field \(\mathbb Q(\sqrt2,\sqrt3)\). Reducibility is harmless in the argument below; an irreducible Thue–Mahler theorem alone would not justify this application. The algebraic identities and quartic nondegeneracy have supplementary exact checks in [the composite-support package](../research/composite-support/). Its finite coefficient checks are not a completed unit-equation computation.

## 4. Effective finiteness of primitive witnesses

**Lemma 4.1.** For fixed positive \(d\) and fixed finite odd prime set \(H_o\), the complete list of primitive witnesses in the nine product rows satisfying

\[
D=d s^2,\qquad s\in\mathcal M(H_o),
\tag{4.1}
\]

is finite and can be determined effectively.

**Proof.** Set

\[
L=6d\prod_{p\in H_o}p,\qquad
R=\mathbb Z[\sqrt2,\sqrt3,1/L].
\]

This is an explicitly presented finitely generated characteristic-zero domain:

\[
R\cong\mathbb Z[X,Y,Z]/(X^2-2,Y^2-3,LZ-1).
\tag{4.2}
\]

The degree-four extension \(\mathbb Q(\sqrt2,\sqrt3)\) and localization at \(L\) verify that the displayed quotient is a domain.

Each quartic in Section 3 splits as

\[
F(x,y)=c\prod_{i=1}^4 L_i(x,y),
\]

with pairwise nonproportional linear forms over \(R\) and \(c\in R^*\). Root factors \(x-r_i y\), and \(y\) at infinity, need only \(\sqrt2,\sqrt3,1/2\); their scalar factors involve only 2 and 3. Under (4.1), the value \(F(x,y)\), equal to \(D\) or \(g^2D\), is a unit of \(R\). Every linear factor value is therefore a nonzero unit as well.

Choose three of these forms. Their coefficient vectors have a relation

\[
\lambda_1 L_1+\lambda_2 L_2+\lambda_3 L_3=0,
\]

where the \(\lambda_i\in R\) can be taken as signed two-by-two determinants. Pairwise nonproportionality makes all three coefficients nonzero. Division by \(L_3\) gives

\[
\lambda_1\varepsilon+\lambda_2\eta=-\lambda_3,
\qquad \varepsilon=L_1/L_3,\quad\eta=L_2/L_3\in R^*.
\tag{4.3}
\]

Evertse–Győry, Theorem 1.1 and Corollary 1.2 [EG], determine the finite solution set of this unit equation effectively from (4.2) and its nonzero coefficients. Those coefficients need not be units, so no additional localization at the determinants is needed.

Each \(\varepsilon\) determines at most one projective point \((x:y)\), since \(L_1/L_3\) is an invertible projective linear fractional map. Recover it by exact arithmetic, discard nonrational points, and choose its coprime integer representative with the required signs. Recover the tile, check positivity, primitivity and the norm equation, and retain it exactly when \(D/d\) is an integer square whose root is supported in \(H_o\). These finite tests give precisely the required list. ∎

Effectiveness here is a proved bound before enumeration, not a search stopped after a long interval without a new solution. Theorem 1.1 of [EG] bounds representatives of the units and their inverses in the explicit ring presentation. Alternatively, the number-field unit-equation height estimate of Győry–Yu [GY, Theorem 1] gives a computable height cutoff, which the inverse fractional linear map converts to a primitive-parameter cutoff. Neither route is claimed to be computationally practical for this application.

## 5. Constructing the eventual basis

If \(\mathsf T(d)\) passes, set \(B=\{1\}\), with \(T_1\) a sufficient global threshold supplied by the existing construction. Theorem 1.1 follows immediately in this case.

Otherwise \(d\) is even. Put \(H_o=H\setminus\{2\}\). Use Lemma 4.1 to compute the primitive witnesses with \(D=ds^2\), \(s\in\mathcal M(H_o)\). Each witness has a known every-integer row threshold. Include its \(s\) in \(B\), taking the least of these thresholds when several witnesses have the same \(s\).

If \(2\in H\), also include \(s=2\). Indeed

\[
u=d-1,\quad v=d+1,\quad \gcd(u,v)=1,\quad v^2-u^2=4d.
\]

The old theta construction supplies \((4d)t^2=d(2t)^2\) at every sufficiently large integer \(t\). Assign its computable residual threshold to \(T_2\).

Every actual odd multiplier has a witness on the complete list by Section 2, and its \(s\) divides \(m\). Every even multiplier is divisible by the included seed 2. This proves necessity in Theorem 1.1. Each seed's assigned constructive tail proves sufficiency. Finally \(m\ge M\) and \(s\mid m\) imply \(m/s\ge T_s\), giving (1.1).

This separation of the prime 2 is essential. Difference-of-squares forms have only two linear factors and can have infinitely many primitive coefficients on a fixed even support. Lemma 4.1 is not applied to them; one old theta construction already covers their required even-multiplier tail.

## 6. An exact finite basis, with a finite geometric remainder

Assume \(H\ne\varnothing\) and put \(p_{\max}=\max H\). Every admissible \(H\)-smooth multiplier has an admissible \(H\)-smooth divisor \(n\) satisfying

\[
n<p_{\max}M.
\tag{6.1}
\]

For \(m<M\), take \(n=m\). Otherwise choose \(s\mid m\) from Theorem 1.1 and put \(r=m/s\ge T_s\). Repeatedly divide \(r\) by a prime factor while retaining \(r\ge T_s\). At termination, either \(r=1<p_{\max}T_s\), or \(r/p<T_s\) for each prime \(p\mid r\), again giving \(r<p_{\max}T_s\). Thus \(n=sr<p_{\max}sT_s\le p_{\max}M\), and \(dn^2\) is constructive.

Apply the previous fixed-count decision procedure to the finitely many \(dn^2\) with \(n\in\mathcal M(H)\), \(n<p_{\max}M\). Retain their positive multipliers that are minimal under divisibility, obtaining \(E\). Then, for **every** \(H\)-smooth multiplier,

\[
\boxed{dm^2\in\mathcal S\quad\Longleftrightarrow\quad
\text{some }e\in E\text{ divides }m.}
\tag{6.2}
\]

Necessity follows from (6.1) and finite descent among admissible divisors. Sufficiency follows by refining each tile into \((m/e)^2\) congruent pieces. If \(B\) is empty, take \(E\) empty without any geometry calls. For empty \(H\), decide only \(d\), obtaining \(E=\varnothing\) or \(\{1\}\).

Fixed-count decidability is a prior input, discussed in [uniform reduction](../research/uniform-reduction/PROOF.md) and the Beeson work cited there. This section does not claim a new decision procedure for fixed \(N\). The new arithmetic cutoff restricts all geometric uncertainty on a fixed support to a computably bounded finite set. The support and its bound still vary; there is no finite global exception list.

## 7. An elementary constraint on prime allocation

The previous prime-ray coefficient bound has a useful extension. Suppose \(d\ge2\), a primitive coefficient in one of the nine product rows is \(D=ds^2\), and

\[
s=q^r n,\qquad r\ge1,\quad q\text{ odd prime},\quad\gcd(q,n)=1.
\]

Then

\[
\boxed{q^r<2dn^2.}
\tag{7.1}
\]

Put \(A_0=dn^2\). Product-factor coprimality from Lemma 5.1 of [square-class tails](square-class-tails.md) puts the entire \(q\)-power in one factor. The other factor divides \(A_0\), so is at most \(A_0\). For F3, remove the prefactor 3 first; the same bound holds, including \(q=3\) and \(q\mid d\). The size estimates of that lemma use only the size of this small factor, not its squarefreeness. With \(A_0\) in place of \(d\), they give \(D<4A_0^3\). Since \(D=A_0q^{2r}\), (7.1) follows.

This constrains the **primitive coefficient**, not automatically the full multiplier. A large prime-power block of \(m\) can enter the geometric scale. If \(m=q^e h\), \(\gcd(q,h)=1\), the exponent left in any primitive coefficient instead satisfies \(q^r<2dh^2\) whenever \(r>0\), independently of \(e\). These inequalities alone do not bound all exponents simultaneously. The unit-equation argument supplies that step on fixed support.

For comparison, a smaller cofinal-support result needs no unit-equation algorithm: for nonempty finite odd \(H\), all sufficiently large \(H\)-smooth multipliers are admissible exactly when every existing prime-ray test \(\mathsf R(d,q)\), \(q\in H\), passes. Necessity follows along each ray. For sufficiency choose an actually admissible \(dq^{2e_q}\) on each positive ray, with \(e_q\ge1\). Refinement covers every multiplier divisible by some \(q^{e_q}\); the others are at most \(\prod_{q\in H}q^{e_q-1}\). If 2 belongs to the support, its ray already has the old theta tail. This cofinal test does not settle mixed-support existence when the prime-power rays fail.

## 8. Sources and verification scope

- **[EG]** J.-H. Evertse and K. Győry, *Effective results for unit equations over finitely generated domains*, [arXiv:1107.5756](https://arxiv.org/pdf/1107.5756), Theorem 1.1 and Corollary 1.2, pages 3–4. The required external result is effective determination of solutions to \(a\varepsilon+b\eta=c\) in units of an explicitly presented finitely generated characteristic-zero domain.
- **[GY]** K. Győry and K. Yu, *Bounds for the solutions of S-unit equations and decomposable form equations*, Acta Arithmetica 123.1 (2006), 9–41, Theorem 1, DOI [10.4064/aa123-1-2](https://doi.org/10.4064/aa123-1-2); [publisher PDF](https://www.impan.pl/shop/en/publication/transaction/download/product/83173). This is an alternative effective number-field bound.
- The necessary tiling classification, integer scales, fixed-tile tails, Harries/Zhang transfers, and cofinal square-class tests are the prior inputs linked above. Supplementary exact checks in [research/composite-support](../research/composite-support/) verify algebraic identities and finite coefficient calculations. They do not implement the effective unit-equation enumeration or the complete geometric decision procedure required to compute \(E\).

The result controls an unbounded set of composite multipliers by a finite effective support-dependent object. It leaves the unrestricted problem, and all uncomputed finite bases, open.
