# Alpha-isosceles square classes and congruent numbers

**Research directed by Denis Paliy, with ChatGPT assistance — 6 October 2026**

The Group-1 alpha-isosceles family has a primitive coefficient in square class \(d\) exactly when the classical congruent-number curve has positive rational rank. The proof below includes an explicit passage from a non-torsion point to the required positive parameter range. Together with the previous fixed-shape constructive tails, this characterizes existence of an alpha tiling somewhere in that square class.

The related F3 rank criterion and its applications to restricted multiplier sectors are in [elliptic square classes](elliptic-square-classes.md). Elliptic methods and the congruent-number rank criterion are established mathematics; no external priority claim is made here. Neither criterion by itself decides a prescribed small tiling multiplier.

## 1. Statement and geometric inputs

For coprime integers \(0<u<v\), put

\[
b=v^2-u^2,\qquad Q=2v^2-u^2.
\]

The associated primitive tile is

\[
(a,b,c)=(uv,v^2-u^2,v^2).
\]

Its alpha-isosceles target has sides \((bcK,bcK,bQK)\) and necessary count \(bQK^2\), with a positive integer \(K\). The earlier [necessary spectrum and gluing transfer](audits/eventual-rational-families.md), Sections 6–7, and [universal rational scales](universal-rational-scales.md) give the two geometric inputs used here:

1. Every tiling in this normalized alpha family has count \(bQK^2\) for an integer \(K>0\).
2. For each fixed primitive pair \((u,v)\), every sufficiently large integer \(K\) is realizable.

The second statement follows from a theta tiling at scale \(vK\) by attaching a standard \(bK\)-fold tile. These prior constructions allow T-junctions. They do not assert that an arbitrary alpha tiling contains a removable block.

**Theorem 1.1.** For every positive squarefree integer \(d\), the following are equivalent:

1. There are coprime integers \(0<u<v\) and an integer \(s>0\) such that
   \[
   (v^2-u^2)(2v^2-u^2)=ds^2.
   \tag{1.1}
   \]
2. The quartic
   \[
   C_d:\quad dw^2=(1-z^2)(2-z^2)
   \tag{1.2}
   \]
   has a rational point with \(0<z<1\).
3. The congruent-number curve
   \[
   E_d:\quad y^2=x^3-d^2x
   \tag{1.3}
   \]
   has positive rank over \(\mathbb Q\).
4. Some count \(dm^2\), with a positive integer \(m\), is realized by an alpha-isosceles tiling.

Thus the squarefree kernels occurring in this branch are exactly the congruent numbers. Statement 4 is an existence assertion somewhere in the square class, not at a prescribed \(m\).

## 2. Primitive normalization and necessity

Equation (1.1) gives a point of (1.2) by

\[
z=u/v,\qquad w=s/v^2.
\]

Conversely, write a point with \(0<z<1\) as \(z=u/v\) in lowest terms, with \(0<u<v\). Then

\[
(v^2-u^2)(2v^2-u^2)=d(v^2w)^2.
\]

If \(v^2w=p/q\) in lowest terms, integrality of the left side implies \(q^2\mid d\). Squarefreeness gives \(q=1\), so \(s=|v^2w|\) is a positive integer. The resulting tile is primitive and nondegenerate: \(\gcd(v,v^2-u^2)=1\), and \(uv+v^2-u^2>v^2\). This proves the equivalence of statements 1 and 2.

From a point of (1.2), define

\[
x=d(z^2-1),\qquad y=d^2zw.
\tag{2.1}
\]

Substitution proves \(y^2=x^3-d^2x\). In the required parameter range,

\[
-d<x<0,\qquad y\ne0.
\]

The rational torsion of \(E_d\) is exactly

\[
\{O,(-d,0),(0,0),(d,0)\}.
\tag{2.2}
\]

Consequently (2.1) is non-torsion, proving statement 3. This uses the torsion of \(E_d\), not an assertion that every nonzero-\(Y\) point on an isogenous curve is non-torsion.

Here is a proof of (2.2). At a good prime \(p\equiv3\pmod4\), pairing \(x\) with \(-x\) cancels the quadratic-character sum for \(x^3-d^2x\), so \(\#E_d(\mathbb F_p)=p+1\). Good reduction injects prime-to-\(p\) rational torsion into this finite group. If an odd prime \(\ell\) divided the rational torsion order, the Chinese remainder theorem and Dirichlet's theorem would supply a good prime with \(p\equiv3\pmod4\), \(p\equiv1\pmod\ell\), and \(p\ne\ell\). Then \(\ell\nmid p+1\), a contradiction. A good prime \(p\equiv3\pmod8\) bounds the rational 2-primary torsion order by four. The four displayed points already have order dividing two, proving (2.2). This is the usual congruent-number torsion fact; [R] also records it.

## 3. A quartic model and two explicit isogenies

The quartic has the rational point \((z,w)=(1,0)\). Its smooth projective model is therefore an elliptic curve, with that point as origin. The birational map

\[
X=d\frac{1+z}{1-z},\qquad
Y=\frac{2d^2w}{(1-z)^2}
\tag{3.1}
\]

identifies it with

\[
E'_d:\quad Y^2=X^3+6dX^2+d^2X.
\tag{3.2}
\]

The inverse, away from \(X=-d\), is

\[
z=\frac{X-d}{X+d},\qquad
w=\frac{2Y}{(X+d)^2}.
\tag{3.3}
\]

In particular, the desired range \(0<z<1\) corresponds exactly to \(X>d\). The point \((-1,0)\) of the quartic maps to \(T=(0,0)\), a rational point of order two on \(E'_d\).

There is a 2-isogeny \(\phi:E_d\to E'_d\) given by

\[
X=\frac{x(x-d)}{x+d},\qquad
Y=y\left(1-\frac{2d^2}{(x+d)^2}\right).
\tag{3.4}
\]

Its kernel is \(\{O,(-d,0)\}\). It is the ordinary 2-isogeny formula after replacing \(x\) by \(x+d\) in \(E_d\). The dual isogeny \(\psi:E'_d\to E_d\) is

\[
x=\frac{(X+d)^2}{4X},\qquad
y=\frac{Y(X^2-d^2)}{8X^2}.
\tag{3.5}
\]

Indeed, the quotient of \(E'_d\) by \(T\) has equation

\[
V^2=U(U-4d)(U-8d).
\]

Putting \(x=U/4-d\), \(y=V/8\) gives (1.3). The formulas extend over their displayed poles to the smooth projective curves. They preserve origins and have degree two; in particular, they send non-torsion points to non-torsion points. As a check, the composition has the usual doubling coordinate

\[
x(2P)=\frac{(x^2+d^2)^2}{4x(x^2-d^2)}.
\]

## 4. Positive rank gives the required parameter range

Suppose \(E_d(\mathbb Q)\) has positive rank. Take a rational non-torsion point \(P\), and put \(Q=\phi(P)\). This is a rational non-torsion point on \(E'_d\).

For a finite non-torsion point \(Q=(X_0,Y_0)\), the duplication formula on (3.2) gives

\[
X(2Q)=\frac{(X_0^2-d^2)^2}{4Y_0^2}>0.
\tag{4.1}
\]

The denominator is nonzero. A zero numerator would give \(2Q=T\), contradicting non-torsion. Thus \(R=2Q=(X,Y)\) has \(X>0\).

If \(X>d\), apply (3.3) immediately. Equality \(X=d\) is impossible because (4.1) would give \(2R=T\). If \(0<X<d\), replace \(R\) by \(R+T\). The addition formula is

\[
X(R+T)=\frac{d^2}{X},\qquad
Y(R+T)=-\frac{d^2Y}{X^2},
\tag{4.2}
\]

so the new \(X\)-coordinate is greater than \(d\). Formula (3.3) now produces a rational point with \(0<z<1\). This proves statement 2 by a finite sequence of algebraic group operations. No density argument or conjecture about ranks is needed for this passage.

The torsion distinction matters. For example, \((2,8)\) on \(E'_2\) has order four and maps to \(z=0\), which is outside the required open interval. The proof does not mistake this boundary point for a coefficient witness: necessity uses (2.1) on \(E_d\), while sufficiency starts with a non-torsion point and preserves that property throughout.

Finally, if (1.1) holds, the prior fixed-shape constructive tail gives alpha tilings with counts

\[
bQK^2=d(sK)^2
\]

for every sufficiently large integer \(K\). Conversely, the necessary integer-scale spectrum of an alpha tiling in square class \(d\) makes its primitive coefficient equal to \(d\) times an integer square. This proves the equivalence with statement 4 and completes the theorem. ∎

## 5. Verification and limits

The standalone [map checker](../research/elliptic-sectors/check_alpha_maps.py) expands nine rational-function identities using exact polynomial arithmetic over fractions. It checks both isogenies, the quartic map and inverse, (2.1), the composition's doubling coordinate, and (4.1)–(4.2). The identities are weighted homogeneous, so normalizing \(d=1\) checks the universal identities after cancellation of their powers of \(d\); it is not an assertion that different quadratic twists are isomorphic over \(\mathbb Q\).

Run from the repository root:

```bash
python research/elliptic-sectors/check_alpha_maps.py
```

The checker is read-only unless an explicit `--report` path is supplied. It rejects Python optimization. Its coefficient checks supplement the mathematical argument; they do not verify the cited geometric tails or compute elliptic ranks.

For a small arithmetic illustration, \((12,36)\in E_6(\mathbb Q)\) maps under (3.4) to \((4,28)\), whose translate by \(T\) is \((9,-63)\). Formula (3.3) gives \(z=1/5\), \(w=-14/25\), hence

\[
(5^2-1^2)(2\cdot5^2-1^2)=24\cdot49=6\cdot14^2.
\]

This illustrates that \(s\) may be even. The theorem does not force \(s=1\), odd \(s\), any prescribed prime support of \(s\), or a specified small geometric scale. Positive rank alone is therefore not a criterion for the odd-multiplier sector. Nor does the theorem supply a general terminating rank algorithm or a complete classification for Erdős problem 634.

**Sources.** The geometric inputs and their original sources are recorded in [universal rational scales](universal-rational-scales.md) and the [eventual-family audit](audits/eventual-rational-families.md), Sections 6–7. **[R]** L. Rolen, *A Generalization of the Congruent Number Problem*, [author-hosted manuscript](https://www.mi.uni-koeln.de/~lrolen/congruent_numbers.pdf), printed p.2, records the congruent-number torsion and positive-rank criterion. The good-reduction torsion input also appears in A. Sutherland, MIT 18.783, Fall 2025, [Problem Set 3](https://math.mit.edu/classes/18.783/2025/ProblemSet3.pdf), Problem 2(d). The needed torsion specialization and all rational maps are derived above.
