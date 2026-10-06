# Exact membership in square class 22

**Research directed by Denis Paliy, with ChatGPT assistance — 6 October 2026**

Let \(\mathcal S\) be the set of positive integers \(N\) for which some nondegenerate triangle can be dissected into \(N\) congruent nondegenerate triangles. Reflections and arbitrary T-junctions are allowed.

This note gives an exact finite arithmetic test for **every** integer in the square class \(22m^2\). The new step removes the remaining 120-degree F3 branch by mapping any proposed coefficient to a rational point on an elliptic curve of rank zero. The exhaustive necessary spectra and the positive QP and 88-tile constructions are prior inputs, explicitly credited below. This is a complete result for one square class, not a solution of all of Erdős problem 634. External priority and referee acceptance have not been established.

## 1. Exact criterion

For an odd positive integer \(m\), let \(\mathsf Q_{22}(m)\) mean that there exist positive odd integers \(x,y\) such that

\[
xy\mid m,\qquad \gcd(x,y)=1,\qquad 11\nmid x,
\tag{1.1}
\]

\[
3x^2<11y^2<4x^2,
\tag{1.2}
\]

and both

\[
11y^2-2x^2,\qquad 22y^2-6x^2
\tag{1.3}
\]

are integer squares.

**Theorem 1.1.** For every positive integer \(m\),

\[
\boxed{22m^2\in\mathcal S
\quad\Longleftrightarrow\quad
m\text{ is even},\quad\text{or}\quad
\bigl(m\text{ is odd and }\mathsf Q_{22}(m)\bigr).}
\tag{1.4}
\]

In particular, every admissible odd multiplier has a tiling in the QP branch, regardless of which tile or target originally established membership. There is no exceptional unresolved range of small scales in this theorem.

The test is finite. For odd \(m\), enumerate \(x\mid m\) and \(y\mid m/x\), retain the coprime pairs with \(11\nmid x\), and apply the inequalities and integer-square tests. The implementation is [classify22.py](../research/composite-support/classify22.py). It uses exact arithmetic; factoring a large input can still be expensive.

A positive odd witness constructs a tiling explicitly. Set

\[
u=\sqrt{22y^2-6x^2},\quad
v=\sqrt{11y^2-2x^2},\quad
t=\frac m{xy},
\tag{1.5}
\]

and put \(b=v^2-u^2\), \(Q=2v^2-u^2\), \(P=3v^2-u^2\). The tile has sides

\[
(uv,b,v^2),
\]

and the target has sides

\[
t\bigl(v^4,v^2Q,bP\bigr).
\tag{1.6}
\]

The existing QP dissection supplies exactly \(QPt^2=22m^2\) congruent tiles.

## 2. Prior classification and construction inputs

The exhaustive angular classification and rationality normalization are recorded in Beeson–Zhang, *Rationality of certain triangle tilings*, [arXiv:2604.01314v1](https://arxiv.org/html/2604.01314v1), Table 1 and Theorem 1.2, with the classical and right-tile cases separated. The integral-scale spectra used here are proved in the [uniform-reduction note](../research/uniform-reduction/PROOF.md), Sections 3–4, and summarized in the [uniform-sectors proof](../research/uniform-sectors/PROOF.md), Section 2.

After the classical counts

\[
r^2,\quad r^2+s^2,\quad 2r^2,\quad 3r^2,\quad 6r^2
\tag{2.1}
\]

are separated, there are thirteen nonclassical necessary rows. For Group 1 take coprime integers \(0<u<v\) and define

\[
b=v^2-u^2,\qquad Q=2v^2-u^2,\qquad P=3v^2-u^2.
\tag{2.2}
\]

Its five coefficients are \(Q,P,b,bQ,QP\). The double-angle isosceles row has coefficient \(b\), with its additional angle restriction. The remaining seven coefficients are listed in Section 3. Every actual count in these rows has the form

\[
N=Dt^2,\qquad t\in\mathbb Z_{>0}.
\tag{2.3}
\]

The integrality of \(t\), including in the presence of T-junctions, is part of those prior necessary-spectrum proofs. No proposed scale-one W/beta exclusion, withdrawn stronger divisibility, or finite experimental cutoff is used here.

For sufficiency, the prior [complete QP construction](two-piece-construction.md) supplies every coefficient \(QP\) and every positive integer multiplier \(t\). Its five-block coordinate proof is also recalled in the uniform-sectors proof, Section 6. The even-multiplier input is Harries's existing 88-tiling, retained and generalized in the [oriented F4 construction](../research/group2-f4/PROOF.md). The 88 example is credited to Harries, not claimed as a new construction here.

## 3. Exhausting the branches for odd multipliers

Suppose \(m\) is odd and \(22m^2\in\mathcal S\). Then

\[
v_2(22m^2)=1,\qquad 22m^2\equiv6\pmod8.
\]

In any necessary spectrum (2.3), prime valuations give \(t\mid m\), since 22 is squarefree. Consequently

\[
D=22s^2,\qquad s=m/t\text{ odd},\qquad D\equiv6\pmod8.
\tag{3.1}
\]

The classical rows are impossible: the exponent of 11 is odd, excluding a sum of two squares, and the squarefree kernel 22 is none of \(1,2,3,6\).

The two difference-of-squares rows are impossible because the primitive difference \(v^2-u^2\) is odd when \(u,v\) have opposite parity and is divisible by 8 when both are odd. It cannot have 2-adic valuation one.

The W row is impossible because \(11\nmid Q\) for primitive \(u,v\). Indeed, if \(11\mid2v^2-u^2\), either \(11\mid u,v\), contradicting primitivity, or 2 is a quadratic residue modulo 11, which it is not.

The beta-isosceles row is impossible because the primitive coefficient \(P=3v^2-u^2\) has only the residues \(2,3,7\pmod8\).

For the norm rows take positive coprime \(a,b\) with \(c^2=a^2\pm ab+b^2\). If exactly one side is even, it is divisible by 8: an even side of valuation one makes the norm a nonsquare modulo 4, and valuation two makes it 5 modulo 8. If both sides are odd, the plus norm gives \(ab\equiv7\pmod8\) and \(a+b\equiv0\pmod8\); the minus norm gives \(ab\equiv1\pmod8\). Substitution yields the exhaustive table:

| Branch | Coefficient | Possible residues modulo 8 |
|---|---|---|
| 60-degree equilateral | \(ab\), minus norm | \(0,1\) |
| 120-degree equilateral | \(ab\), plus norm | \(0,7\) |
| F1 | \(b(a+b)\) | \(0,1\) |
| Isosceles | \(b(a+2b)\) | \(0,1,2\) |
| F2 | \((a+2b)(2a+b)\) | \(2,7\) |
| F3 | \(3(a+2b)(a+b)\) | \(0,3,6\) |
| F4 | \((2a+b)(a+b)\) | \(0,1,2\) |

Both orders of \(a,b\) are included. Thus only Group-1 alpha, Group-1 QP, and F3 remain.

### Eliminating alpha for the entire odd square class

In the alpha row,

\[
bQ=22s^2,\qquad \gcd(b,Q)=1.
\tag{3.2}
\]

The difference coefficient \(b\) must be odd, so \(Q\) is even, \(u\) is even, and \(v\) is odd. If \(4\mid u\), then \(bQ\equiv2\pmod8\), impossible. Hence \(u\equiv2\pmod4\) and

\[
b\equiv5\pmod8.
\tag{3.3}
\]

On the other hand \(11\nmid Q\). Coprimality in (3.2) therefore assigns the squarefree kernel 2 to \(Q\) and 11 to \(b\):

\[
Q=2x^2,\qquad b=11y^2
\]

for odd positive integers \(x,y\). This makes \(b\equiv3\pmod8\), contradicting (3.3). This exclusion does not assume \(3\nmid m\).

## 4. A rank-zero obstruction removes F3

The underlying obstruction applies to every positive squarefree kernel \(d\), not only to 22. If an F3 coefficient equals \(ds^2\), put \(A=a+2b\), \(B=a+b\), \(K=3d\), and \(h=s/3\in\mathbb Q_{>0}\). Then \(AB=Kh^2\), and

\[
X=\frac{K(A-B)}B,\qquad
Y=\frac{KAc}{hB}
\tag{4.0}
\]

give a rational point on \(Y^2=X^3+K^3\) with \(0<X<K\). Indeed, before the translation \(X=z-K\), the norm identity gives \(Y^2=z^3-3Kz^2+3K^2z\) for \(z=KA/B\). Consequently, absence of rational points in that interval rules out the entire F3 contribution to the square class \(d\). An arbitrary rational point does not automatically reconstruct a primitive tile at a prescribed scale. The later [rank equivalence](elliptic-square-classes.md) proves the converse for existence somewhere in the square class by selecting a suitable even multiple and verifying the extra square condition.

**Lemma 4.1.** No F3 coefficient belongs to the square class 22.

**Proof.** Suppose positive integers \(a,b,c,s\) satisfy

\[
c^2=a^2+ab+b^2,\qquad
3(a+2b)(a+b)=22s^2.
\tag{4.1}
\]

Put \(A=a+2b\), \(B=a+b\). Then

\[
c^2=A^2-3AB+3B^2,\qquad B<A<2B.
\]

Divisibility by 3 in (4.1) forces \(s=3h\) for a positive integer \(h\), and hence

\[
AB=66h^2.
\tag{4.2}
\]

Define rational numbers

\[
z=\frac{66A}{B},\qquad w=\frac{66Ac}{hB}.
\]

Using (4.2), direct substitution gives

\[
w^2=z^3-198z^2+13068z.
\]

Consequently \(X=z-66\), \(Y=w\) give a rational point on

\[
E:\quad Y^2=X^3+66^3=X^3+287496,
\tag{4.3}
\]

with \(0<X<66\) and \(Y>0\). But

\[
E(\mathbb Q)=\{O,(-66,0)\},
\tag{4.4}
\]

as justified below. This contradiction proves the lemma. Primitivity and parity were not needed: the obstruction excludes F3 for even as well as odd multipliers. ∎

### A finite algebraic proof of rank zero

The later [class-number criterion](elliptic-square-classes.md) gives another
proof of (4.4), independent of the analytic certificate below. The curve
is 3-isogenous over the rationals to \(y^2=x^3-22^3\). Since 22 is even,
squarefree and 1 modulo 3, the cited Stoll formula bounds its rank by twice
the 3-rank of the class group of \(\mathbb Q(\sqrt{-22})\).
The only primitive reduced positive forms of discriminant \(-88\) are
\((1,0,22)\) and \((2,0,11)\). Thus \(h(-88)=2\), proving rank zero;
the elementary torsion determination then gives (4.4).
[The exact class-number checker](../research/elliptic-sectors/sector.py)
enumerates these forms with a proved complete bound. The source theorem
is read in Chang's explicit restatement; the original Stoll paper was
not retrieved. The former analytic certificate is retained below.

### Exact arithmetic input for the elliptic curve

Curve (4.3) is Cremona **69696o3**, LMFDB **69696.ej4**. The [pinned Cremona table](https://github.com/JohnCremona/ecdata/blob/25cec5ecfec8b9f016eb1631ac633194c2bed39f/allcurves/allcurves.60000-69999#L63083), commit `25cec5ecfec8b9f016eb1631ac633194c2bed39f`, file `allcurves/allcurves.60000-69999`, line 63083, records

```text
69696 o 3 [0,0,0,0,287496] 0 2
```

The last two entries are rank zero and torsion order two. The [LMFDB curve page](https://www.lmfdb.org/EllipticCurve/Q/69696/ej/4) identifies the same equation and rational torsion generator \((-66,0)\). This is a rigorous rank-zero result, not an assumption of the full Birch–Swinnerton-Dyer conjecture.

For a reproducible check beyond quoting the rank field, [verify_rank22.py](../research/composite-support/verify_rank22.py) computes an exact rational-interval certificate for \(L(E,1)>0\); its retained output is [rank22.json](../research/composite-support/rank22.json). The cited local inputs are conductor \(69696=264^2\), global root number \(+1\), and additive reduction at \(2,3,11\). These local inputs are not recomputed by this checker.

For root number \(+1\), the standard central-value formula is

\[
L(E,1)=2\sum_{n\ge1}\frac{a_n}{n}
\exp\!\left(-\frac{2\pi n}{264}\right).
\tag{4.5}
\]

The formula is stated in the [SageMath elliptic-curve L-series documentation](https://doc.sagemath.org/html/en/reference/arithmetic_curves/sage/schemes/elliptic_curves/lseries_ell.html#sage.schemes.elliptic_curves.lseries_ell.Lseries_ell.at1), with reference to Cohen, Section 7.5.3. The checker implements the formula directly and does not require SageMath.

The program computes the coefficients through \(n=500\) from finite-field point counts and Euler-factor recurrences. It bounds the exponential using alternating rational series and directed integer rounding. The bound \(|a_n|\le\tau(n)\sqrt n\le2n\) makes the absolute omitted tail at most \(4q^{501}/(1-q)\), where \(q=e^{-\pi/132}\). The certified interval is contained in

\[
4.14119<L(E,1)<4.14345.
\tag{4.6}
\]

Thus modularity and the unconditional rank-zero theorem imply \(\operatorname{rank}E(\mathbb Q)=0\). The [LMFDB rigor documentation](https://www.lmfdb.org/knowledge/show/rcs.rigor.ec.q) explicitly records that analytic rank at most one equals Mordell–Weil rank. For this complex-multiplication curve, the rank-zero implication also follows from Coates–Wiles, *On the conjecture of Birch and Swinnerton-Dyer*, Inventiones Mathematicae 39 (1977), 223–251, [DOI:10.1007/BF01402975](https://doi.org/10.1007/BF01402975). No conjectural deduction from an analytic rank of two or higher is involved.

For torsion there is also an independent elementary check: the discriminant is \(-432(66^3)^2\), so 5 and 7 are primes of good reduction, and direct counting gives

\[
\#E(\mathbb F_5)=6,\qquad \#E(\mathbb F_7)=4.
\]

Prime-to-characteristic torsion injects under good reduction. The first count excludes 7-primary torsion, the second excludes 5-primary torsion, and the remaining torsion order divides \(\gcd(6,4)=2\). The rational point \((-66,0)\) has order two. This proves (4.4).

## 5. Recovering the exact QP criterion

For odd \(m\), Sections 3–4 leave only QP. Necessarily

\[
QP=22s^2,\qquad \gcd(Q,P)=1.
\tag{5.1}
\]

The gcd follows from \(P-Q=v^2\), \(Q=2v^2-u^2\), and \(\gcd(u,v)=1\). Here \(Q\) must be even: otherwise \(P\) is even and \(u,v\) are both odd, giving \(QP\equiv1\cdot2=2\pmod8\), contrary to (3.1). As before, \(11\nmid Q\). Thus the complete coprime square-kernel allocation is

\[
Q=2x^2,\qquad P=11y^2,\qquad xy=s,
\tag{5.2}
\]

where \(x,y\) are positive odd integers, \(\gcd(x,y)=1\), and \(11\nmid x\). Conversely those gcd conditions are exactly what makes the two factors in (5.2) coprime.

Solving the two linear equations in \(u^2,v^2\) gives

\[
v^2=P-Q=11y^2-2x^2,\qquad
u^2=2P-3Q=22y^2-6x^2.
\tag{5.3}
\]

The condition \(0<u<v\) is equivalent to (1.2). Any integer square roots in (5.3) are automatically coprime, since a common prime would divide both \(Q\) and \(P\). Finally \(xy=s=m/t\) is equivalent to \(xy\mid m\).

This proves necessity of \(\mathsf Q_{22}(m)\). Conversely a witness to that condition gives the primitive parameters and positive integer scale (1.5). The prior QP construction gives the target (1.6) and exactly

\[
QPt^2=(2x^2)(11y^2)\left(\frac m{xy}\right)^2=22m^2
\]

congruent tiles. This proves sufficiency for all odd multipliers, including those divisible by 3.

## 6. Even multipliers and examples

For \((a,b,c)=(3,5,7)\), the prior F4 construction gives target sides

\[
(ac,b(2a+b),c(a+b))=(21,55,56)
\]

and count \((2a+b)(a+b)=11\cdot8=88\). If \(m=2k\), subdividing each of the 88 tiles into \(k^2\) congruent similar triangles gives

\[
88k^2=22m^2.
\]

Thus every even multiplier is admissible. Together with Section 5, this proves Theorem 1.1.

The [F4 package](../research/group2-f4/README.md) gives exact construction and verification commands for the existing 88-tiling. Its concrete starting example is attributed to Harries, [progress634.tex](https://github.com/jphme/math-problems/blob/67838578b5bd26aa66034fa46da96141be75de0e/progress634/progress634.tex), v0.5, 28 August 2026. The general oriented F4 extension is separate prior project work.

The previously certified odd positive example remains

\[
m=248599631=7\cdot3089\cdot11497.
\]

Here \(x=7\cdot3089=21623\), \(y=11497\) give \(u=10132\), \(v=22779\), and \(t=1\). Thus \(22m^2=1359639083733395542\) is admissible by the old QP certificate. The [square-class tail note](square-class-tails.md), Section 8, proves that every odd prime-power multiplier is inadmissible. There is no contradiction: distinct primes of this composite multiplier occupy the two different coprime factors in (5.2).

The advance here is the removal of the previous restriction \(3\nmid m\) from exact odd-multiplier membership in square class 22, followed by integration with the old even-multiplier construction. The result settles this whole square class without settling the other square classes or the full Erdős problem.
