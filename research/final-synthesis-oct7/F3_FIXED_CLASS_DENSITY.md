# Fixed-square-class F3 density and a sparse geometric remainder

7 October 2026. Research with ChatGPT assistance. This note combines the
existing F3 elliptic map and constructive tails with Mordell–Weil height
counting. It classifies an asymptotic quantity and bounds the remaining
geometric uncertainty. It does not decide every multiplier or claim a
complete solution of Erdős problem 634.

## 1. Sets and theorem

Fix a positive squarefree integer d. Define the set of **odd primitive
coefficient multipliers**

\[
\mathcal B_d=\{s\ge1:s\text{ odd},\quad
3(a+b)(a+2b)=ds^2\text{ for some positive integers }a,b,c,
\ \gcd(a,b)=1,\ c^2=a^2+ab+b^2\}.
\]

Let A_d be the arithmetic divisibility envelope and F_d the actual odd
F3 multipliers:

\[
\mathcal A_d=\{m\ge1:m\text{ odd and some }s\in\mathcal B_d\text{ divides }m\},
\]

\[
\mathcal F_d=\{m\ge1:m\text{ odd and }dm^2
\text{ is realized in the classified F3 branch}\}.
\]

For each primitive witness (a,b,c), the previous Harries–Zhang transfers
and equilateral constructions give the every-integer sufficient threshold

\[
T(a,b)=\left\lceil\frac32
\left(\left\lfloor\frac{\max(a,b)}{\min(a,b)}\right\rfloor+2\right)\right\rceil.
\tag{1}
\]

For s in B_d, minimize (1) over its finite list of primitive witnesses,
and call the minimum tau_d(s). This is a finite divisor-and-square
calculation. Put

\[
\mathcal C_d=\{m\ge1:m\text{ odd},\quad
s\mid m\text{ and }m/s\ge\tau_d(s)
\text{ for some }s\in\mathcal B_d\}.
\]

Thus C_d uses only existing explicit sufficient constructions. Necessary
integer scales and those constructions give

\[
\mathcal C_d\subseteq\mathcal F_d\subseteq\mathcal A_d.
\tag{2}
\]

Let

\[
E_d:\ Y^2=X^3+(3d)^3,\qquad r_d=\operatorname{rank}E_d(\mathbb Q).
\]

**Theorem.** For each fixed d the following hold:

1. The coefficient list is sparse:
   \[
   \#\{s\in\mathcal B_d:s\le X\}
   =O_d((1+\log X)^{r_d/2}).
   \tag{3}
   \]
   The same bound holds when primitive ordered triples are counted.
2. Its reciprocal sum converges, with
   \[
   \sum_{\substack{s\in\mathcal B_d\\s>K}}\frac1s
   =O_d\left(\frac{(1+\log K)^{r_d/2}}K\right).
   \tag{4}
   \]
3. The necessary and constructive tests in (2) disagree on at most
   \[
   \boxed{\#((\mathcal A_d\setminus\mathcal C_d)\cap[1,X])
   =O_d\bigl(X^{1/3}(1+\log X)^{r_d/2}\bigr).}
   \tag{5}
   \]
4. All three sets in (2) have the same natural density **relative to odd
   positive integers**. Write that density delta_d. If B_d(K) consists
   of its elements at most K, then
   \[
   \delta_d(K)=
   \sum_{\varnothing\ne J\subseteq\mathcal B_d(K)}
   \frac{(-1)^{|J|+1}}{\operatorname{lcm}(J)}
   \tag{6}
   \]
   is an exact finite arithmetic quantity, and
   \[
   0\le\delta_d-\delta_d(K)
   \le\sum_{\substack{s\in\mathcal B_d\\s>K}}\frac1s
   =O_d\left(\frac{(1+\log K)^{r_d/2}}K\right).
   \tag{7}
   \]
   The density is positive exactly when B_d is nonempty.

Relative density here means the limit of the count through X divided by
ceil(X/2), not division by X. Empty coefficient sets have density zero.
The rank and implied constants are fixed-class quantities; there is no
uniform assertion as d varies. Positive rank alone must not be confused
with existence of an **odd** coefficient multiplier.

## 2. Height of the coefficient point

For a primitive coefficient witness put U=a+2b and V=a+b. The existing
[elliptic map](../../docs/elliptic-square-classes.md), Section 1, is

\[
X=\frac{3d\,b}{a+b},\qquad
Y=\frac{9d\,(a+2b)c}{s(a+b)}.
\tag{8}
\]

Direct substitution, using 3UV=ds^2, gives Y^2=X^3+(3d)^3. Also
0<X<3d. These facts have already been proved in the cited note.

The map is injective on primitive positive ordered triples: X/(3d)
is the reduced rational number b/(a+b), so it uniquely determines the
coprime pair (a,b), and c is its positive norm square root. The multiplier
s is then uniquely determined as well. We use the positive sign of Y.

Since V<U and UV=ds^2/3,

\[
a+b<s\sqrt{d/3}.
\]

The multiplicative rational height H(X), defined as the larger absolute
value of reduced numerator and denominator, consequently satisfies

\[
H(X)\le3d(a+b)<\sqrt3\,d^{3/2}s.
\tag{9}
\]

Choose the normalization of the canonical height satisfying

\[
\widehat h(P)=\log H(X(P))+O_d(1).
\]

A conventional normalization smaller by a factor two gives the same
counting estimate. The Mordell–Weil theorem identifies the free part of
E_d(Q) with a rank-r_d lattice on which the canonical height is a positive
definite quadratic form. Hence its number of points of canonical height
at most H is O_d((1+H)^{r_d/2}), including the finite torsion translates.
Equation (9) and injectivity prove (3). This is an upper bound, so no real
or 2-adic distribution theorem for the counted points is required.

The external inputs are stated and proved in J. S. Milne, *Elliptic
Curves*, second edition, Chapter IV: the finite basis theorem at the
chapter opening (printed p. 105), the canonical-height comparison and
quadraticity in Section 4, Theorem 4.7 and Proposition 4.9 (pp. 125–126),
and positive definiteness in Section 6, Theorem 6.1 (p. 133):
<https://www.jmilne.org/math/Books/EC2.pdf> (inspected 7 October 2026).
The lattice-point bound itself follows by enclosing the positive-definite
ellipsoid in a Euclidean box.

Partial summation of (3) gives

\[
\sum_{s>K}\frac1s
\le\int_K^\infty\frac{\#\{s\in\mathcal B_d:s\le t\}}{t^2}\,dt
=O_d\left(\frac{(1+\log K)^{r_d/2}}K\right),
\]

proving (4).

## 3. A square-root bound for the known geometric threshold

Let A=max(a,b) and B=min(a,b). The norm identity gives

\[
(2c-2A-B)(2c+2A+B)=3B^2.
\]

The first factor is a positive integer, because
c^2-(A+B/2)^2=3B^2/4>0. The second is strictly larger than 4A.
Consequently

\[
A<\frac{3B^2}{4},\qquad
\frac AB<\sqrt{\frac{3A}{4}}
<\frac{(3d)^{1/4}}2\sqrt s.
\tag{10}
\]

Here the last step uses A<a+b<s sqrt(d/3), valid in either ordered
orientation. The existing threshold (1) therefore satisfies

\[
T(a,b)\le\frac32\frac AB+4
\le\left(4+\frac34(3d)^{1/4}\right)\sqrt s
=:\kappa_d\sqrt s.
\tag{11}
\]

In particular tau_d(s)<=kappa_d sqrt(s). This is a sufficient bound; it
is not a necessary minimum scale.

Every m in A_d minus C_d has at least one divisor s in B_d, and for every
such divisor its residual scale obeys m/s<tau_d(s). Count possible
representations (s,t) rather than distinct m. For any 1<=L<=X the count
is at most

\[
\sum_{\substack{s\in\mathcal B_d\\s\le L}}\kappa_d\sqrt s
+X\sum_{\substack{s\in\mathcal B_d\\s>L}}\frac1s
=O_d\left(
\sqrt L(1+\log L)^{r_d/2}
+\frac XL(1+\log L)^{r_d/2}\right).
\]

Taking L=X^(2/3) proves (5). Oddness only decreases these representation
counts. In terms of tile counts dm^2<=Z, the corresponding fixed-class
exception bound is

\[
O_d\bigl(Z^{1/6}(1+\log Z)^{r_d/2}\bigr).
\tag{12}
\]

These are supersets of geometric uncertainty, not sets of proven negative
counts. Counts outside A_d are negative for the F3 branch, and counts
inside C_d have known genuine F3 constructions.

## 4. Density and finite approximations

The finite union of odd multiples of s in B_d(K) is periodic. For odd s,
its odd-relative density is 1/s; finite inclusion–exclusion therefore
gives (6). Any member of A_d outside this finite union is divisible by
some s>K. The union bound gives, uniformly in X,

\[
\#\{m\le X:m\in\mathcal A_d\setminus
\bigcup_{s\in\mathcal B_d(K)}s\mathbb Z\}
\le X\sum_{s>K}1/s.
\]

To obtain the sharp odd-relative bound in (7), first truncate the tail
at a finite J. Its upper relative density is at most sum_{K<s<=J}1/s.
The remainder has upper relative density at most 2 sum_{s>J}1/s by the
uniform displayed bound. Let J tend to infinity and use (4). Thus the
upper relative density of the whole tail is at most sum_{s>K}1/s.
Letting K tend to infinity proves existence of the density of A_d and
(7). Equation (5) then gives exactly the same density for F_d and C_d.

If B_d contains s, all sufficiently large odd multiples of s lie in
C_d; their relative density is 1/s>0. If B_d is empty, all three sets
are empty. This proves the last assertion.

## 5. Global consequence in square class 38

The [class-38 all-branch isolation](../../docs/infinite-minimal-multipliers.md),
Section 6, proves that **every** actual odd multiplier in this square
class must be F3. Therefore

\[
\{m\text{ odd}:38m^2\in\mathcal S\}=\mathcal F_{38}.
\]

The theorem now concerns global tilings, not just a branch. The set of
odd admissible multipliers in class 38 has a positive natural relative
density delta_38, given by (6)–(7); positivity follows from the existing
actual class-38 constructions. Every coefficient multiplier is divisible
by 3, so 0<delta_38<=1/3.

The unresolved distinction between arithmetic candidates and these
explicit genuine constructions occupies at most

\[
O\bigl(X^{1/3}(1+\log X)^{r_{38}/2}\bigr)
\]

multipliers through X. Simultaneously, the
[nonperiodicity theorem](STRUCTURAL_AUDIT.md) shows that no fixed modulus
can decide the odd sector up to finitely many exceptions. Positive density,
a sparse arithmetic list of primitive coefficients, infinitely many
minimal multipliers, and nonperiodicity are compatible.

No decimal value of delta_38 or certified full Mordell–Weil basis is
computed here. Finite coefficient lists are effective by inverse divisor
formulas, but a numerical certified error bar from (7) additionally needs
explicit certified height/lattice bounds. This note does not assert those
bounds have been computed, nor does it assume a finite-index point list
is a complete basis.

The geometric input (1) is the existing
[square-class tail note, Appendix A](../../docs/square-class-tails.md),
including its attribution of the Harries–Zhang transfers. No candidate
W/beta scale-one proof is used. The cases 154 and 4830 and the unrestricted
all-N classification remain unresolved here.

## 6. Finite regression checks

```sh
python research/final-synthesis-oct7/check_f3_height_density.py
```

The independent integer/Fraction script checks all 174 primitive ordered
plus-norm triples with a,b<=500: the elliptic map, recovery of the primitive
pair, the rational-height bound, the norm factorization, and the sufficient
scale inequalities. It also compares finite inclusion–exclusion with exact
period enumeration on four sample odd divisor lists. These finite checks
are not the proof of Mordell–Weil height counting or of an infinite density.
