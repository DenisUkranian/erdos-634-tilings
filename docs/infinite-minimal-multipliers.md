# Infinitely many minimal admissible multipliers in square class 38

6 October 2026. Written proof with separate internal arithmetic and geometric-input audits. This is a structural limitation of fixed seed lists, not a complete solution of Erdős problem 634 or a claim of external priority.

## 1. Statement and scope

Let S denote the admissible tile counts in Erdős problem 634, with the repository's definition. Put

\[
\mathcal M_{38}=\{m\in\mathbb Z_{>0}:38m^2\in S\}.
\]

**Theorem.** For every finite set H of primes, there is an odd multiplier m in \(\mathcal M_{38}\), realized by an F3 tiling, such that

\[
v_3(m)=1,\qquad v_p(m)=0\quad(p\in H\setminus\{3\}).
\tag{1}
\]

Consequently \(\mathcal M_{38}\) contains an infinite sequence of odd multipliers with pairwise gcd exactly 3. It has infinitely many odd divisibility-minimal elements. No finite fixed list of admissible seeds can generate every admissible multiplier in this square class by grid refinement.

The corresponding assertion holds for positive primitive F3 coefficient multipliers. This result does not preclude an input-dependent finite criterion, finitely many parameterized families, or a full solution of the tiling problem. It is compatible with the [finite-basis theorem](fixed-prime-support.md) for each *fixed finite prime support*: the present construction escapes every prescribed finite support.

The geometric inputs are the [necessary coefficient spectra and every-integer fixed-tile F3 tail](square-class-tails.md), with their stated published classification dependencies. The new reasoning below concerns an explicit elliptic orbit, simultaneous neighborhoods along that orbit, and divisibility.

## 2. Explicit orbit and persistence of the square lift

Set k=114=3·38 and use

\[
E:Y^2=X^3+k^3,\qquad F:y^2=x^3+6kx^2-3k^2x.
\]

The point \(Q=(-110,388)\) lies on E since \(388^2=(-110)^3+114^3=150544\), and is nontorsion. By Lutz–Nagell, a nonzero torsion ordinate on this integral short Weierstrass model has square dividing its discriminant. But \(97\mid388\), whereas \(\Delta_E=-432\cdot114^6\) has support only \(\{2,3,19\}\). Alternatively Q reduces to order 3 at the good prime 5, and order 6 at the good prime 7; prime-to-residue-characteristic torsion injectivity makes these incompatible for a rational torsion point.

The translated equation with \(t=X+k\) is \(Y^2=t^3-3kt^2+3k^2t\). A degree-two isogeny and its dual, with a compatible choice of ordinate signs, are

\[
\phi(X,Y)=\left(\frac{Y^2}{(X+k)^2},\frac{Y[3k^2-(X+k)^2]}{(X+k)^2}\right),
\]

\[
\widehat\phi(x,y)=\left(\frac{y^2}{4x^2}-k,\frac{y(-3k^2-x^2)}{8x^2}\right).
\tag{2}
\]

Both formulas can be verified by substitution. The point \(G=(54,216)\in F(\mathbb Q)\) satisfies \(\widehat\phi(G)=-Q\). Thus every nonzero multiple \(nQ=\widehat\phi(-nG)\) satisfies

\[
X(nQ)+k\text{ is a nonzero rational square.}
\tag{3}
\]

No exceptional kernel point occurs, since nQ has infinite order. The integral image \(\phi(Q)=(9409,945071)\) is a useful arithmetic check but is not needed for the proof. No denominator sequence or primitive-divisor theorem is used.

## 3. Exact primitive coefficient normalization

Write any orbit point as

\[
X=A/C^2,\quad Y=B/C^3,\quad A,B\in\mathbb Z,\ C>0,\quad
\gcd(A,C)=\gcd(B,C)=1.
\]

Equation (3) gives a positive integer W with

\[
A+kC^2=W^2,\qquad \gcd(W,C)=1.
\tag{4}
\]

Factoring the cubic gives

\[
B^2=W^2(A^2-kAC^2+k^2C^4).
\]

Therefore \(V=B/W\) is an integer and \(V^2=A^2-kAC^2+k^2C^4\). Suppose that \(0<X<k\). Set

\[
g=\gcd(kC^2-A,A)=\gcd(k,A),\quad
 a=(kC^2-A)/g,\quad b=A/g,\quad c=|V|/g.
\]

Here g divides V, since g² divides V². Hence a,b,c are positive integers with \(\gcd(a,b)=1\) and \(c^2=a^2+ab+b^2\). Their F3 coefficient is

\[
3(a+2b)(a+b)=\frac{3kC^2(A+kC^2)}{g^2}
=38\left(\frac{3WC}{g}\right)^2.
\tag{5}
\]

Thus its multiplier is exactly

\[
s=3WC/g\in\mathbb Z_{>0}.
\tag{6}
\]

Integrality follows also directly from (5): a rational square times squarefree 38 can be integral only if the rational number has denominator one. Outside the real interval the same expression can be used for local valuation calculations, without claiming positive tile sides.

## 4. Prescribing avoidance of any finite prime set along this orbit

Let \(J=H\cup\{2,3,19\}\). At Q the reduced data are \(A=-110,C=1,W=2,g=2\), so the expression (6) equals 3.

For each prime in J choose the following open neighborhood of Q:

| Prime | Required condition on X | Consequence for (6) |
|---|---|---|
| 2 | \(X\in\mathbb Z_2,\ X\equiv-110\pmod8\) | \(v_2(C)=0,v_2(W)=1,v_2(g)=1\), so \(v_2(s)=0\) |
| 3 | \(X\in\mathbb Z_3,\ X\equiv-110\pmod3\) | C,W,g are units, so \(v_3(s)=1\) |
| 19 | \(X\in\mathbb Z_{19},\ X\equiv-110\pmod{19}\) | C,W,g are units, so \(v_{19}(s)=0\) |
| \(p\in J\setminus\{2,3,19\}\) | \(X\in\mathbb Z_p,\ X+k\in\mathbb Z_p^\times\) | C,W,g are units, so \(v_p(s)=0\) |

These neighborhoods all contain Q: \(X(Q)+k=4\). Integrality of X gives \(p\nmid C\). At 2, X has valuation one and X+k has valuation two. At the other primes, (4) and \(g\mid k\) give the indicated assertions. In particular the conditions apply even at 5 and 11, where X(Q) itself is not a unit.

Each group \(E(\mathbb Q_p)\) is compact and has arbitrarily small open subgroups at O, supplied by its formal group. Choose an open subgroup \(U_p\) so that \(Q+U_p\) is contained in the chosen neighborhood. The quotient \(E(\mathbb Q_p)/U_p\) is finite. Let L be a common multiple of the orders of Q in these finitely many quotients. Then every integer \(n\equiv1\pmod L\) has

\[
nQ\in Q+U_p\quad(p\in J).
\tag{7}
\]

For the standard local subgroup and compactness facts, see J. S. Milne,
*Elliptic Curves*, second edition, Chapter II, §4, Theorem 4.1 and its proof,
printed pp. 62–64: <https://jmilne.org/math/Books/EC2.pdf>.
Its filtration consists of open subgroups shrinking to O, and each has
finite index. This applies at the bad primes as well. No reduction at a
singular point is being treated as a homomorphism.

The real curve E(R) is a connected compact circle: the cubic \(X^3+k^3\) has only one real root. Since Q has infinite order, so does LQ, and its nonnegative multiples are dense in that circle. Therefore the arithmetic progression \((1+Lr)Q\), \(r\ge0\), meets the nonempty open interval \(0<X<k\). Choose such a point. Section 3 produces a positive primitive F3 witness whose multiplier s satisfies

\[
v_3(s)=1,\qquad v_p(s)=0\quad(p\in J\setminus\{3\}).
\tag{8}
\]

This uses finitely many neighborhoods of the *same rational point Q*, maintained by a congruence on one cyclic orbit, and real density of that progression. It makes no assertion of approximation to arbitrary unrelated local points and needs no rank or generator computation.

## 5. From the coefficient to an actual admissible count

The repository's prior F3 tail guarantees a tiling with count

\[
3(a+2b)(a+b)t^2=38(st)^2
\]

for every integer \(t\ge T(a,b)\). A safe bound is

\[
T(a,b)=\left\lceil\frac32\left(\left\lfloor\frac{\max(a,b)}{\min(a,b)}\right\rfloor+2\right)\right\rceil.
\tag{9}
\]

Choose such a t additionally satisfying

\[
t\equiv1\pmod{\prod_{p\in J}p}.
\tag{10}
\]

There are arbitrarily large positive integers in this progression. Then m=st is odd, is an actual admissible multiplier, and satisfies (1), proving the prime-avoidance claim.

The geometric source used here is [square-class tails, Appendix A](square-class-tails.md): the every-integer equilateral construction and the positive F2-to-F3 transfer. It explicitly attributes the prior constructions to Harries/Zhang and earlier repository proofs. In particular this step does not infer tiling at t=1 merely from a coefficient witness.

## 6. Excluding the two possible common-divisor seeds, 1 and 3

We check the stronger statement that **every odd admissible multiplier in class 38 must come from F3**. If \(38m^2=Dt^2\) is a necessary primitive spectrum, integrality and squarefreeness give \(D=38s^2\), \(s\mid m\). For odd m, both s and t are odd and \(D\equiv6\pmod{16}\).

The existing exhaustive row reduction in [elliptic square classes, §4](elliptic-square-classes.md), eliminates the classical branches (kernel 38 is not one of 1,2,3,6, and has the prime 19 congruent to 3 modulo 4), both difference-of-squares rows, W, beta, and all norm rows except F3. That reduction does not require a rank-zero assumption until the separate step excluding F3, which is not invoked here. The only other candidate rows are alpha and QP, and they are excluded directly:

- **Alpha.** With \(b=v^2-u^2\), \(Q_0=2v^2-u^2\), the residue \(bQ_0\equiv6\pmod{16}\) forces v odd and \(u\equiv2\pmod4\), hence \(Q_0/2\equiv7\pmod8\). Coprimality partitions the odd squarefree kernel 19, so \(Q_0=2A r^2\) with \(A\in\{1,19\}\) and r odd. This would require \(A\equiv7\pmod8\), but A is 1 or 3 modulo 8. Contradiction.
- **QP.** Its coprime forms are \(Q_0=2v^2-u^2\), \(P_0=3v^2-u^2\), with \(\gcd(u,v)=1\). The prime 19 must divide one factor of their product. But both \((2/19)\) and \((3/19)\) equal −1, so division by 19 in either form forces \(19\mid u,v\), a contradiction.

Thus an odd admissible m must have a positive primitive F3 coefficient multiplier s dividing m. Every such s is divisible by 3, since \(3\mid38s^2\). The value s=3 is impossible: it would give

\[
(a+2b)(a+b)=114.
\]

Writing \(U=a+2b\), \(V=a+b\), positivity requires \(V<U<2V\). The factor pairs \((U,V)=(114,1),(57,2),(38,3),(19,6)\) exhaust the possibilities and none meets that interval. Therefore neither s=1 nor s=3 is a positive F3 witness. It follows that neither m=1 nor m=3 is an actual admissible multiplier:

\[
38\notin S,\qquad342\notin S.
\tag{11}
\]

## 7. Infinite antichain of minimal admissible multipliers within class 38

Construct \(m_1,m_2,\ldots\) inductively. At each step let H contain every prime divisor of the previously chosen multipliers, and apply Sections 4–5. Each new multiplier has 3-adic valuation exactly one and avoids every other prime in every preceding multiplier. Thus

\[
\gcd(m_i,m_j)=3\qquad(i\ne j).
\tag{12}
\]

For each i choose a divisibility-minimal element \(r_i\) of the finite nonempty set

\[
\{r\in\mathcal M_{38}:r\mid m_i\}.
\]

Every r_i is divisibility-minimal in \(\mathcal M_{38}\): any proper admissible divisor would also divide m_i. Each r_i is odd, since it divides odd m_i; possible even admissible multipliers therefore cannot affect its minimality. If \(r_i=r_j\), this common value divides \(\gcd(m_i,m_j)=3\), contradicting (11). Hence infinitely many distinct minimal admissible multipliers within class 38 exist. No finite seed list can generate all of \(\mathcal M_{38}\) by divisibility.

The identical argument, applied to the coefficient multipliers s before choosing their tails, proves infinitely many minimal positive primitive F3 coefficient multipliers. It uses the same exclusions s=1,3.

## 8. Fixed tiles, scope and checks

This does not generalize to all positive-rank classes. For d=110 the primitive triple (8,7,13) gives coefficient \(990=110\cdot3^2\), and every F3 coefficient multiplier in that class is divisible by 3. One coefficient witness therefore divides every coefficient multiplier in that class. The absent small witnesses in class 38 are essential here.

There is a slightly stronger fixed-tile consequence. Suppose finitely many
primitive tile/branch witnesses covered every odd admissible multiplier in
class 38, allowing any residual scale for each witness. Every such branch
must be F3 by Section 6. Its fixed coefficient multiplier s would divide
every m it covers. Among the pairwise-gcd-3 sequence in Section 7, one fixed
s can divide at most one member: dividing two would force s to divide 3,
which Section 6 excludes. Thus no finite list of fixed primitive tiles can
cover this entire odd sector, even using all their possible residual scales.
This is stronger than failure of a finite grid-refinement seed list.

The [exact arithmetic checks](../research/infinite-minimal/) independently
replay both curve group laws, the dual lift and primitive normalization for
finitely many multiples. They also check the small factor exclusions and
the local valuation identities. The infinite conclusion uses the written
local-group, real-density, and constructive-tail proof; it is not inferred
from a finite orbit sample. No full Mordell–Weil basis, conjectural rank
algorithm, prime-distribution statement or weak-approximation principle is
an input.

The result does not imply that a finite parameterized description is
impossible, or that the input-dependent coefficient allocation suggested
for a specified N fails. What remains unresolved is the exact geometric
small-scale spectrum of the surviving branches.
