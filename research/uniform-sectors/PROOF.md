# Uniform arithmetic sectors and asymptotic concentration for congruent triangle dissections

**Erdős problem 634 — research directed by Denis Paliy, with ChatGPT assistance**  
**1 October 2026**

## Status, scope, and what is not assumed

Let \(\mathcal S\) be the set of positive integers \(N\) for which some nondegenerate triangle can be dissected into \(N\) congruent nondegenerate triangles. Reflections and arbitrary T-junctions are permitted.

This note does **not** classify all of \(\mathcal S\). It gives an exact classification on an explicitly defined infinite arithmetic domain, uniform exclusions of square multiples, and a global asymptotic concentration theorem. The arguments are deductions from the exhaustive shape classification and the necessary scale spectra recorded in Section 2. Those dependencies are explicit. The proposed scale-one W and beta-isosceles exclusions, the proposed all-primes theorem, the withdrawn packing lemma, and any assertion that a construction-specific divisibility is necessary are **not** inputs.

The proofs below have been checked within this investigation, with exact computational regression. They have not been formally verified or externally refereed. No claim of first priority is made. The QP construction used for sufficiency is an **existing** project result dated 29 September, not a new construction theorem in this note. The elliptic-curve example and the new integration of the arithmetic restrictions are distinguished from that older construction.

The source repository examined was `DenisUkranian/erdos-634-tilings`, commit `50d7459bd1d3f41352630323f1c55a92e8d9b64e` (30 September 2026). The 30 September uniform-reduction note is the immediate scale-spectrum input.

## 1. Main statements

Write the squarefree decomposition of an integer with exactly one factor of 2 as

\[
N=2D m^2,\qquad D\text{ odd and squarefree},\quad m\text{ odd}.
\]

Here squarefree means that no prime square divides the integer. Let \((a/p)\) denote the Legendre symbol for an odd prime \(p\).

### Theorem A — a complete factor-and-square criterion on an infinite domain

Suppose

\[
N\equiv6\pmod{16},\qquad 3\nmid N,
\tag{A1}
\]

and **no prime \(p\equiv7\pmod8\) occurs to an odd exponent in \(N\)**. Then the following are equivalent:

1. \(N\in\mathcal S\).
2. There exist positive integers \(t,Q,P\) such that
   \[
   N=t^2QP,\quad\gcd(Q,P)=1,\quad 3Q<2P<4Q,
   \tag{A2}
   \]
   and both
   \[
   P-Q\quad\hbox{and}\quad 2P-3Q
   \tag{A3}
   \]
   are integer squares.
3. There are coprime integers \(0<u<v\) and an integer \(t\ge1\) such that
   \[
   N=(2v^2-u^2)(3v^2-u^2)t^2.
   \tag{A4}
   \]

A positive witness supplies the tile

\[
(a,b,c)=(uv,v^2-u^2,v^2)
\]

and a target with sides

\[
t\bigl(v^4,\ v^2(2v^2-u^2),\ (v^2-u^2)(3v^2-u^2)\bigr).
\]

The decision procedure in (A2)–(A3) is finite: enumerate the square divisors \(t^2\mid N\), and then the factor pairs of \(N/t^2\). It does not enumerate tilings and does not use a geometric existence oracle.

The condition on primes concerns **odd exponents**, not the complete absence of such primes. In particular, a factor \(7^2\) is allowed.

### Theorem B — an enlarged exact domain

For odd squarefree \(D\equiv3\pmod8\), \(3\nmid D\), form the following finite set of factorizations \(D=AB\):

\[
\begin{split}
&A\equiv7\pmod8,\qquad B\equiv5\pmod8;\\
& (2/p)=1,\quad(-B/p)=1\qquad &&\text{for every }p\mid A;\\
& (2A/p)=1 &&\text{for every }p\mid B.
\end{split}
\tag{B1}
\]

If this set is empty, then the three equivalent conditions of Theorem A hold for **every** \(N=2Dm^2\) with \(\gcd(m,6)=1\), even when \(D\) has prime divisors congruent to 7 modulo 8.

A surviving factorization in (B1) is only a necessary local test for an alpha-isosceles branch. It is **not** a construction and is not asserted sufficient.

### Theorem C — uniform infinite exclusions

Let \(D\) be odd and squarefree, with \(3\nmid D\), and let \(\gcd(m,6)=1\).

* If \(D\equiv7\pmod8\) and some prime \(p\mid D\) has \((2/p)=-1\), then
  \[
  2Dm^2\notin\mathcal S.
  \tag{C1}
  \]
* If \(D\equiv3\pmod8\), \(3\nmid D\), the set (B1) is empty, and some prime \(p\mid D\) has both \((2/p)=-1\) and \((3/p)=-1\), then
  \[
  2Dm^2\notin\mathcal S.
  \tag{C2}
  \]

Both assertions retain the common hypothesis \(3\nmid Dm\).

A particularly simple consequence is

\[
\boxed{\quad 2p m^2\notin\mathcal S
\quad\text{for every prime }p\equiv19\pmod{24}
\text{ and every }m\text{ with }\gcd(m,6)=1.\quad}
\tag{C3}
\]

Thus \(38m^2,86m^2,134m^2,\ldots\) are excluded uniformly in the stated multipliers. This is not an extrapolation from finitely many checked values. The restriction on multiples of 3 is retained: another classified branch contributes counts divisible by 3.

### Theorem D — the global asymptotic concentration theorem

Let \(\mathcal T\subseteq\mathcal S\) consist of counts having a tiling in at least one of these two branches:

* the Group-1 theta-isosceles branch;
* the double-angle isosceles branch \(\gamma=2\alpha\).

Then

\[
\boxed{\#\bigl((\mathcal S\setminus\mathcal T)\cap[1,X]\bigr)=o(X).}
\tag{D1}
\]

Thus every possible positive-density contribution to the complete answer must come from those two isosceles branches. This does **not** say that they contain all tilings or all admissible counts.

In both branches an actual count has the form

\[
N=(v^2-u^2)t^2,\qquad\gcd(u,v)=1,\quad t\ge2.
\tag{D2}
\]

Consequently, if \(S(X)=\#(\mathcal S\cap[1,X])\),

\[
\boxed{\limsup_{X\to\infty}\frac{S(X)}X
\le \frac34-\frac9{2\pi^2}
=0.2940546736\ldots .}
\tag{D3}
\]

Equivalently, the lower natural density of impossible tile counts is at least

\[
\frac14+\frac9{2\pi^2}=0.7059453264\ldots .
\tag{D4}
\]

This is a density statement about integers, **not** a percentage of completion of the research problem. It asserts neither that the density of \(\mathcal S\) exists nor that the upper bound is sharp.

## 2. Exhaustive inputs and their exact role

The angular classification is Laczkovich's classification of triangle dissections [1–3], with the rational-angle exceptions and the right-tile cases separated. The 2026 Beeson–Zhang rationality theorem [2] permits primitive integer tile sides for the remaining nonsimilar, nonright, incommensurable-angle cases. Classical counts lie in

\[
\mathcal C=\{r^2,r^2+s^2,2r^2,3r^2,6r^2:r,s\ge1\}.
\tag{2.1}
\]

Twice a sum of two squares is itself a sum of two squares, so the right-tile formulation does not introduce another family here. Zero-square instances are covered by perfect squares.

For primitive Group 1 use

\[
a=uv,\ b=v^2-u^2,\ c=v^2,\quad Q=b+c,\quad P=b+2c,
\quad 0<u<v,\quad\gcd(u,v)=1.
\tag{2.2}
\]

Its five necessary count forms are:

| Target family | Necessary count | Scale restriction used |
|---|---|---|
| W | \(Qt^2\) | \(t\) a positive integer |
| beta-isosceles | \(Pt^2\) | \(t\) a positive integer |
| theta-isosceles | \(bt^2\) | \(t\ge2\) |
| alpha-isosceles | \(bQt^2\) | \(t\) a positive integer |
| other scalene | \(QPt^2\) | \(t\) a positive integer |

The last row is sufficient at every positive integer scale by the two-piece construction [6] recalled in Section 6. No analogous sufficiency is assumed for the other four rows.

For the double-angle isosceles branch, the primitive tile is

\[
(u^2,v^2-u^2,uv),\qquad 0<u<v<2u,\quad\gcd(u,v)=1,
\]

and the count is \((v^2-u^2)t^2\), with \(t\ge2\).

For primitive norm triples, write

\[
c^2=a^2\pm ab+b^2,\qquad\gcd(a,b)=1.
\tag{2.3}
\]

The minus sign occurs in the 60-degree equilateral branch; the plus sign occurs in the 120-degree branches. Both side orders are included. The seven necessary forms are:

| Branch | Coefficient \(d\) in \(N=dt^2\) |
|---|---|
| 60-degree equilateral | \(ab\) |
| 120-degree equilateral | \(ab\) |
| 120-degree F1 | \(b(a+b)\) |
| 120-degree isosceles | \(b(a+2b)\) |
| 120-degree F2 | \((a+2b)(2a+b)\) |
| 120-degree F3 | \(3(a+2b)(a+b)\) |
| 120-degree F4 | \((2a+b)(a+b)\) |

All scales are positive integers. These tables comprise thirteen nonclassical branches, not thirteen new theorems of this note.

### Why the integer scales survive T-junctions

An exterior side of a convex target is a chain of whole tile edges. With primitive integer tile sides, its length is an integer. Primitive integral target side proportions therefore give an integral similarity scale by Bézout.

Where exterior integrality and area alone are weaker, the two signed-direction characters provide integer values \(U,V\) satisfying \(U\equiv V\equiv N\pmod2\). Their half-sums and half-differences are integers. Interior edge contributions cancel after subdivision at all incident vertices; the lengths of those subsegments need not be integers.

For example, in the double-angle case the target has sides \(\lambda(u,u,v)\), area equation \(N=\lambda^2/b\), and character values

\[
U=-\lambda/(u+v),\qquad V=\lambda/(v-u).
\]

Their half-sum and half-difference give \(\lambda u/b,\lambda v/b\in\mathbb Z\). Thus \(b\mid\lambda\). The Group-1 theta calculation is the same with reversed signs. In the alpha-isosceles case the half-difference is \(\lambda uv/b\); \(\gcd(uv,b)=1\) again gives \(b\mid\lambda\).

In the plus norm case, the two nonzero reference character values are \(c+a-b,c+b-a\), with product \(3ab\). The equilateral half-sum is \(Sc/(ab)\); since \(\gcd(c,ab)=1\), \(ab\mid S\). In the minus case the corresponding half-sum is \(S(a+b)/(ab)\), with the same conclusion. The F1 and isosceles half-differences respectively give \(\lambda a/b\) and \(\lambda(a+b)/b\), forcing \(b\mid\lambda\). The other rows follow from primitive side proportions and the area equation.

These are the scale calculations in the 30 September uniform-reduction note [5]. They do not require a global geometric lattice or an edge-to-edge tiling.

### The scale-one exclusion used for the two difference-of-squares families

For the Group-1 theta target, its apex is a single alpha tile. Thus one equal side contains a b-edge. At scale one that side has length \(bv\); reduction modulo \(v\) makes its b-edge count a positive multiple of \(v\), forcing the entire side to be b-edges. Every b-edge contributes an obtuse gamma endpoint, no target corner contains gamma, and at most one gamma can occur at each straight boundary junction. There are fewer internal junctions than edges: a contradiction.

For the double-angle target, take the equal side incident to the alpha tile at its apex. It must contain a b-edge. Otherwise all boundary edges are a or c, each contributing a beta endpoint, while the two outer endpoint tiles have alpha there and every straight boundary junction contains exactly one beta. Again there are too few internal junctions. Modulo \(u\), the b-edge count is divisible by \(u\); at scale one the length \(bu\) forces a pure-b side. Its \(2\alpha\) endpoints cannot occur at the outer corners, and a straight junction contains at most one \(2\alpha\), giving the same contradiction. The angle inventories follow by equating the rational and irrational parts using \(\beta=\pi-3\alpha\).

These short boundary arguments are separate from the proposed scale-one W and beta arguments.

## 3. The modulo-16 collapse

### Lemma 3.1

Assume \(3\nmid N\) and \(N\equiv6\) or \(14\pmod{16}\). Then:

\[
\begin{array}{c|c}
N\pmod{16}&\text{only possible nonclassical branches}\\ \hline
14& W\\
6&\text{alpha-isosceles or other-scalene QP}.
\end{array}
\tag{3.1}
\]

**Proof.** Such an \(N\) has exactly one factor of 2, so every scale \(t\) in the thirteen count forms is odd. Multiplication by an odd square fixes an even residue having exactly one factor of 2 modulo 16: \(t^2\equiv1\) or 9, and \(8N\equiv0\pmod{16}\).

For coprime \(u,v\), at least one is odd. If both are odd, \(b=v^2-u^2\) is divisible by 8. Otherwise b is odd. Therefore neither difference-of-squares branch can produce an \(N\) with exactly one factor of 2.

Direct substitution of the squares \(0,1,4,9\pmod{16}\), with u and v not both even, gives the following intersections with \(\{6,14\}\):

| Coefficient | Possible intersection |
|---|---|
| \(Q\) | \(\{14\}\) |
| \(P\) | empty |
| \(bQ\) | \(\{6\}\) |
| \(QP\) | \(\{6\}\) |

For a primitive plus norm triple, if a and b are odd then \(ab\equiv7\pmod8\) and \(a+b\equiv0\pmod8\). If exactly one is even, that even side is divisible by 8. To see the latter, with the odd side and c odd, reduction modulo 8 gives \(a(a+b)\equiv0\pmod8\); if a is even then a+b is odd. For both odd, reduction modulo 8 gives ab congruent to 7; an odd integer is its own inverse modulo 8, so b is congruent to minus a and a+b is divisible by 8. For a minus norm triple, the same argument makes its even side divisible by 8, while the both-odd case has \(ab\equiv1\pmod8\).

Substitution in the seven coefficients shows that none has residue 6 modulo 8, except possibly F3. That branch is always divisible by 3 and has been excluded by hypothesis. A sum of two squares or twice a square also cannot be 6 modulo 8; the remaining classical forms are divisible by 3. This proves (3.1). ∎

For clarity, in the alpha-isosceles case surviving in (3.1), u is 2 modulo 4 and v is odd. Consequently

\[
b\equiv5\pmod8,\qquad Q/2\equiv7\pmod8.
\tag{3.2}
\]

In the QP case surviving there, u is divisible by 4 and v is odd; then

\[
Q/2\equiv1\pmod8,\qquad P\equiv3\pmod8.
\tag{3.3}
\]

## 4. Square-class descent and the proofs of Theorems A–C

### Lemma 4.1 — prime divisors of Q and P

For coprime \(u,v\), every odd prime dividing \(Q=2v^2-u^2\) satisfies \((2/p)=1\). Every odd prime \(p\ne3\) dividing \(P=3v^2-u^2\) satisfies \((3/p)=1\).

**Proof.** A prime dividing v cannot divide either Q or P, since it would also divide u. Reducing modulo a prime divisor of Q gives \((u/v)^2=2\). The proof for P is identical. ∎

Also \(\gcd(b,Q)=\gcd(Q,P)=1\), because subtracting the two factors reduces the gcd to a gcd with \(v^2\).

### Lemma 4.2 — alpha-isosceles partitions

Under (A1), if the alpha-isosceles branch occurs, then a factorization satisfying (B1) exists.

**Proof.** Because b and Q are coprime, their square classes partition the odd squarefree kernel D:

\[
b=B s^2,\qquad Q=2A r^2,\qquad AB=D.
\tag{4.1}
\]

Both r and s are odd. Equation (3.2) gives \(A\equiv7\pmod8\) and \(B\equiv5\pmod8\). A prime divisor of A divides Q, so Lemma 4.1 gives \((2/p)=1\). At such a prime, \(u^2=2v^2\), hence \(b=-v^2\); since \(b=B s^2\) and neither v nor s vanishes, \((-B/p)=1\).

At a prime dividing B, \(u^2=v^2\) and therefore \(Q=v^2\). Using \(Q=2A r^2\) and coprimality gives \((2A/p)=1\). These are precisely (B1). ∎

**Proof of Theorem B.** By Lemma 3.1 only alpha-isosceles and QP are possible. Lemma 4.2 excludes the former when (B1) is empty. The QP branch has exactly the count form (A4), with full sufficiency from Section 6. For (A2)–(A3), put \(v^2=P-Q\) and \(u^2=2P-3Q\). The inequalities imply \(0<u<v\), and any common prime divisor of u and v would divide Q and P, a contradiction. Conversely Q and P built from primitive u,v are coprime and satisfy those inequalities. Thus (A2), (A3), and (A4) are equivalent. ∎

**Proof of Theorem A.** Every prime divisor of A in a putative factorization (B1) has \((2/p)=1\), hence is 1 or 7 modulo 8. If D has no prime divisor 7 modulo 8, every such prime is 1 modulo 8. Their product A is then 1 modulo 8, contradicting \(A\equiv7\pmod8\). Thus (B1) is empty, and Theorem B applies. ∎

**Proof of Theorem C.** If \(D\equiv7\pmod8\), then \(N\equiv14\pmod{16}\), so only W remains. Every prime in D divides Q to an odd exponent, contradicting Lemma 4.1 as soon as one is inert for 2. This proves (C1).

For (C2), Theorem B leaves only QP. As Q and P are coprime, each prime in D must occur in one of them to an odd exponent. A prime inert for both 2 and 3 can occur in neither factor, by Lemma 4.1. This proves (C2).

For (C3), a prime \(p\equiv19\pmod{24}\) has p congruent to 3 modulo 8, so \((2/p)=-1\), and p congruent to 7 modulo 12, so \((3/p)=-1\). Its kernel has no prime 7 modulo 8. Apply Theorems A and C2. ∎

These proofs control **all primitive tile parameters at once**. They do not assert that an unconstructed arithmetic candidate is geometrically realizable.

## 5. Global asymptotic concentration: proof of Theorem D

The proof has three components: a sparse count for nine branches; density zero for the classical/W/beta norm restrictions; and the two residual isosceles branches.

### Lemma 5.1 — a universal primitive-triple bound

The number of ordered primitive positive solutions of

\[
c^2=a^2+ab+b^2,\qquad ab\le Y
\]

is \(O(\sqrt Y)\).

**Proof.** The rational slope \((c-a)/b\) lies strictly between 1/2 and 1. Write it in lowest terms as \(h/k\), so \(k/2<h<k\). Solving the conic gives

\[
a=\frac{k^2-h^2}{g},\quad b=\frac{k(2h-k)}g,\quad
c=\frac{h^2-hk+k^2}g,
\quad g\in\{1,3\}.
\tag{5.1}
\]

Here \(\gcd(h,k)=1\). The gcd of the first two numerators is odd, coprime to k, and divides 3, proving the asserted bound on g. If it is 3, the third numerator is divisible by 3 too. Thus (5.1) covers every ordered primitive triple; no unbounded scaling parameter was discarded.

Set \(\delta=k-h\), \(\epsilon=2h-k\). They are positive and \(k=2\delta+\epsilon\). Then

\[
ab=\frac{\delta\epsilon\,k(k+h)}{g^2}
\ge\frac{\delta\epsilon\,k^2}{9}
\ge\frac{k^3\min(\delta,\epsilon)}{27}.
\tag{5.2}
\]

The last inequality uses \(\max(\delta,\epsilon)\ge k/3\). For a fixed k, there are at most two pairs with a given value of \(\min(\delta,\epsilon)\). Therefore the number of parameters at k is at most

\[
2\min\{k,\,27Y/k^3\}.
\]

Sum up to \(k\le Y^{1/4}\), and above that split point:

\[
O\!\left(\sum_{k\le Y^{1/4}}k+
Y\sum_{k>Y^{1/4}}k^{-3}\right)=O(\sqrt Y).
\]

Overcounting nonprimitive parameters only makes this an upper bound, as needed. ∎

For the minus norm, interchange a and b so that a is larger. If a=b, primitivity gives the classical equilateral tile. Otherwise \((A,B)=(a-b,b)\) is a primitive plus norm pair and \(AB\le ab\). The same \(O(\sqrt Y)\) bound follows, with at most two side orders.

Every coefficient in the seven norm rows of Section 2 is at least ab. Thus each row has at most \(O(\sqrt Y)\) primitive parameter pairs with coefficient at most Y.

### Lemma 5.2 — the two other Group-1 sparse rows

There are \(O(\sqrt Y)\) primitive parameter pairs with \(bQ\le Y\), and \(O(\sqrt Y)\) with \(QP\le Y\).

**Proof.** Put \(d=v-u\). Then

\[
bQ\ge d v^3.
\]

At a fixed v there are at most \(\min(v,Y/v^3)\) choices. Splitting the sum at \(Y^{1/4}\) gives \(O(\sqrt Y)\). Also \(Q>v^2\) and \(P>2v^2\), so \(QP>2v^4\); summing at most v possible u up to \(v<(Y/2)^{1/4}\) gives the same bound. ∎

Allowing square scales in any of these nine rows yields at most

\[
\sum_{t\le\sqrt X}O(\sqrt{X/t^2})
=O(\sqrt X\log(2X))
\tag{5.3}
\]

counts up to X, even if every arithmetic candidate were realizable. Repeated representations do not cause a problem because this is an upper bound.

### Lemma 5.3 — the three quadratic-character envelopes have density zero

For each of the characters \(\chi_{-4},\chi_8,\chi_{12}\), the set

\[
\mathcal R_\chi=\{n\ge1:v_p(n)\text{ is even whenever }\chi(p)=-1\}
\tag{5.4}
\]

has natural density zero.

**Proof.** For a fixed prime p, the integers with even p-adic valuation have density

\[
(1-1/p)\sum_{j\ge0}p^{-2j}=p/(p+1).
\]

For a finite collection of primes these conditions have density equal to the product, by the Chinese remainder theorem and truncation of p-adic valuations. The upper density of \(\mathcal R_\chi\) is therefore at most the corresponding finite product \(\prod p/(p+1)\).

For completeness, \(\sum_{\chi(p)=-1}1/p\) diverges for each of these three characters. An elementary Euler-product argument suffices here. For real s>1,

\[
\log\zeta(s)-\log L(s,\chi)
=2\sum_{\chi(p)=-1}p^{-s}+O(1),
\tag{5.5}
\]

where the contribution of higher prime powers is uniformly bounded, and the finitely many ramified primes are harmless. The periodic, mean-zero character series has a finite limit at s=1. That limit is positive: group its terms respectively as

\[
\frac1{4j+1}-\frac1{4j+3},
\]
\[
\frac1{8j+1}-\frac1{8j+3}-\frac1{8j+5}+\frac1{8j+7},
\]
\[
\frac1{12j+1}-\frac1{12j+5}-\frac1{12j+7}+\frac1{12j+11}.
\]

Every group is positive, and these grouped series converge. Positivity in the last two cases follows by comparing equal-length reciprocal differences at an earlier and a later interval. Hence \(\log L(s,\chi)\) remains bounded as s decreases to 1, whereas \(\log\zeta(s)\) diverges. Equation (5.5) proves the divergence of the inert-prime reciprocal sum. The finite products of \(p/(p+1)\) consequently tend to zero, proving density zero. ∎

A sum of two squares belongs to \(\mathcal R_{\chi_{-4}}\). Any positive integer \(2x^2-y^2\) belongs to \(\mathcal R_{\chi_8}\), and any \(3x^2-y^2\) belongs to \(\mathcal R_{\chi_{12}}\). Indeed, if an inert prime divides such a form it divides both variables; divide by its square and repeat. Thus W counts and beta-isosceles counts, even after arbitrary square scales, lie in the latter two density-zero envelopes. The classical exceptional forms \(2r^2,3r^2,6r^2\) contribute only \(O(\sqrt X)\) counts.

**Proof of (D1).** The thirteen-row classification outside the classical set leaves two difference-of-squares isosceles rows, two quadratic-character rows W and beta, and the nine rows counted in (5.3). Every count in \(\mathcal S\setminus\mathcal T\) is therefore in a union of three density-zero envelopes and a set of size \(O(\sqrt X\log(2X))\). This is o(X). ∎

### Lemma 5.4 — the exact arithmetic envelope of the two remaining branches

The primitive positive difference coefficients are exactly

\[
\mathcal B=\{v^2-u^2:0<u<v,\ \gcd(u,v)=1\}
=\{b\ge3:b\text{ odd}\}\ \cup\ 8\mathbb Z_{>0}.
\tag{5.6}
\]

Indeed, opposite parities give an odd difference at least 3, while two odd parameters give a multiple of 8. Conversely, for an odd b≥3 take \(u=(b-1)/2,v=(b+1)/2\); for b=8k take \(u=2k-1,v=2k+1\). These pairs are coprime. This converse concerns a coefficient, not the existence of a tiling at a prescribed scale.

Put \(\mathcal E=\bigcup_{t\ge2}t^2\mathcal B\). The true set \(\mathcal T\) is contained in \(\mathcal E\), but equality is not asserted. Define the disjoint union

\[
\mathcal U=
\{\text{odd squarefree integers}\}
\ \cup\ \{n:n\equiv2\pmod4\}
\ \cup\ \{8q:q\text{ odd and squarefree}\}.
\tag{5.7}
\]

Then the complement of the arithmetic envelope is exactly

\[
\mathbb Z_{>0}\setminus\mathcal E
=\mathcal U\ \cup\ \{p^2:p\text{ an odd prime}\}\ \cup\ \{4,16\}.
\tag{5.8}
\]

To check this, write n=2^e q with q odd. When e=1, no square factor can remove the forbidden 2-adic valuation of the coefficient. When e=3 and q is squarefree, the only possible scales are 1 and 2; the first is forbidden by t≥2 and the second leaves a coefficient of 2-adic valuation 1. When e=0, an odd nonsquarefree number has a representation in \(\mathcal E\) unless it is exactly an odd prime square: remove a prime square and the remaining odd coefficient must be at least 3. For e=2 or e=4 and q>1, scales 2 or 4 respectively leave the allowed odd coefficient q; q=1 gives exactly 4 and 16. For e=3 and nonsquarefree q, an odd prime-square divisor of q supplies t≥3 and leaves a multiple of 8. Finally, every e≥5 permits t=2, leaving a multiple of 8. This exhausts the possibilities and proves (5.8).

**Proof of (D3)–(D4).** The three sets in (5.7) have respective natural densities

\[
\frac4{\pi^2},\qquad \frac14,\qquad \frac1{2\pi^2}.
\]

The first follows from

\[
\frac12\prod_{p>2}(1-p^{-2})=\frac4{\pi^2},
\]

and the third is one eighth of the first. The extra sets in (5.8) have density zero. Thus the arithmetic envelope has exact density

\[
\operatorname{dens}(\mathcal E)
=\frac34-\frac9{2\pi^2}.
\tag{5.9}
\]

Since \(\mathcal T\subseteq\mathcal E\) and \(\mathcal S\setminus\mathcal T\) has density zero by (D1), the upper density of \(\mathcal S\) is at most (5.9). Taking the complement gives (D4). Notice that \(\mathcal S\cap\mathcal U\) has density zero, not necessarily that it is empty. ∎

### A precise remaining density question

The proof does not show that \(\mathcal S\) itself has density zero. It isolates what would suffice: for each fixed integer t≥2, show that the realizable difference coefficients b in each of the two residual isosceles branches have density zero. The union over a fixed finite number of t would then have density zero, while the upper density of the tail t>K is at most \(\sum_{t>K}t^{-2}\), which tends to zero. This is a rigorous reduction of that **density question**, not a replacement for the full membership problem.

## 6. Constructive sufficiency: the existing five-block QP dissection

This section recalls the project's complete QP construction so that the positive direction is geometric, not just an area calculation.

Let \(a,b,c,Q,P\) be as in (2.2), and let a coordinate pair (x,y) represent the Euclidean point \((x,y\sqrt{4v^2-u^2})\). Put

\[
\begin{aligned}
O&=(0,0), & A&=(b^2,0),\\
C&=(-u^2b/2,ub/2), &D&=(-u^2b/2,-ub/2),\\
E&=(-u^2Q/2,-u^3/2),&B&=D+E,\\
H&=C+(Q/c)(C-A).
\end{aligned}
\tag{6.1}
\]

The target is ABH. Its five macroregions are OAC, OAD, OCE, BCH, and the parallelogram ODBE. The four triangles are similar copies of the tile at integral scales b,b,a,Q. In the parallelogram, the step vectors D/b and E/u² have lengths a,c and difference length b. A b by u² grid, split along that difference diagonal, consists of \(2bu^2\) congruent tiles.

The identities

\[
E=(u^2/b)(D-A),\qquad D=(b/c)(E-C)
\]

place D between A and B and E between C and B. The first three triangles and the parallelogram partition ABC. Their angles about O sum to \(3\gamma+\beta=2\pi\). Furthermore A,C,H are collinear with C between A and H, and BCH lies on the other side of BC from A. Thus the final union is the triangle ABH, not a nonconvex polygon or an overlap.

Its side lengths are \(c^2,cQ,bP\), and its count is

\[
2b^2+a^2+Q^2+2bu^2=cQ+Q^2=QP.
\tag{6.2}
\]

Scaling the target by an integer t and refining all blocks gives QPt² congruent tiles. This is the construction in `docs/two-piece-construction.md` of the pinned source commit.

### An ordinary-sized positive example

Take \(u=4,v=5\). Then

\[
(a,b,c)=(20,9,25),\quad Q=34,\quad P=59,
\]

and

\[
N=2006,\qquad\text{target sides }(625,850,531).
\]

This lies in Theorem A's exact domain. The four triangle blocks contribute \(81,81,400,1156\) tiles, and the parallelogram contributes 288, totaling 2006. In this run every one of the 2006 tiles and all 2,011,015 unordered pairs were checked with exact integer arithmetic after clearing denominators. The checker found no positive-area overlap.

### A large witness in square class 22

Take

\[
u=10132,\qquad v=22779.
\]

Then

\[
\begin{aligned}
a&=230796828,& b&=416225417,&c&=518882841,\\
Q&=935108258=2\cdot21623^2,\\
P&=1453991099=11\cdot11497^2.
\end{aligned}
\]

Hence

\[
\boxed{QP=22\cdot248599631^2
=1359639083733395542\in\mathcal S.}
\tag{6.3}
\]

The multiplier is coprime to 6. This shows why one must not infer that the entire square class 22 is impossible from its small negative instances. No minimality claim is made for this witness.

The positive certificate is compressed into four triangular grids and one parallelogram grid. Exact checks verify all macroregion sides, containment, ten macroregion pair intersections, the integer grids, and area coverage. **The approximately \(1.36\times10^{18}\) individual tiles were not enumerated.** The grid formulas are the finite constructive description.

### How the large witness was obtained

The equation \((2v^2-u^2)(3v^2-u^2)=n w^2\) maps to

\[
E_n:\quad y^2=x(x-2n)(x-3n),\qquad
x=n u^2/v^2,\quad y=n^2uw/v^3.
\tag{6.4}
\]

For n=22, the rational point \((352/9,1936/27)\) comes from u=4,v=3,w=1. It is **not** a valid triangular parameter pair because u>v. Exact tripling on the elliptic curve gives a point with \(x/22=(10132/22779)^2\); recovering u,v gives (6.3), now with 0<u<v. The code checks the elliptic equation and the recovered integers exactly. This is a witness-generation method, not a rank computation, completeness theorem for elliptic points, or nonexistence test.

## 7. Reproducibility and checks

All delivered checkers use only the Python standard library. Python 3.10 or later is sufficient.

```bash
python run_checks.py --output verification.json
python arithmetic_sectors.py 22 38 950 2006 17542 154
python verify_macro.py construction_22_large.json
python check_expanded.py construction_2006.json
python elliptic_witness.py
```

The saved run records:

| Check | Actual finite scope |
|---|---|
| Trial factorization against an independently generated smallest-prime-factor sieve | integers 1 through 20,000 |
| Modulo-16 branch collapse | complete residue tables, including odd-square multipliers |
| Factor-and-square criterion against direct QP parameter enumeration | 2,571 tested N values through 30,000 |
| Local partition/character regression | 3,043 primitive pairs with v≤100 |
| Infinite forbidden-family regression | 187 instances; the universal claim is proved above |
| Conic parameterization comparison | all primitive positive plus-norm triples with a,b≤150 |
| Difference-coefficient and exact-envelope identities | coefficient b≤1,000; arithmetic envelope n≤100,000 |
| Macrogeometry | 554 certificates for 277 primitive pairs, scales 1 and 2; 5,540 macro pairs |
| Invalid certificate mutations | 12 rejected |
| Expanded 2006 construction | 2,006 tiles and 2,011,015 unordered pairs |
| Large square-class-22 witness | one complete compressed-grid certificate |

The 30,000 scan of the residues 6 and 14 modulo 16, excluding multiples of 3, returned 1,504 `NO`, 3 `YES`, and 993 `NOT_COVERED`. These are finite test statistics, not an asymptotic estimate or a claim that previously known numbers are new discoveries.

`NOT_COVERED` deliberately does not mean `NO`. For example, 154 is outside this module's exact arithmetic domain. The already studied N=105 is also outside this module; this does not contradict or supersede its separate project certificate.

The factorization routine uses exact trial division. It terminates, but is not optimized for very large prime inputs. The large example above has a small-prime factorization and is inexpensive. No bounded search or timeout is reinterpreted as a proof of impossibility.

## 8. What this changes, and what it does not

The exact-domain theorem is an instance of the missing type of global integration: eliminate every alternative tile family by a uniform arithmetic argument, then use a family for which necessity and construction already match. It avoids solving every fixed-tile spectrum unnecessarily.

The density theorem supplies a different global integration. The infinite tile parameters in nine branches are controlled by a proved count, rather than a cutoff experiment. Three quadratic-character envelopes have density zero. Only two isosceles branches can affect the answer on a positive-density set of integers.

Neither result decides every composite count, validates the proposed all-primes proof, or closes the full Erdős problem. In particular, scale-one W and beta geometry, small realizable scales in the residual isosceles families, and other exact-membership questions remain separate obligations. The previous fixed-tile eventual constructions are retained as inputs and complementary results, not relabeled as a uniform full classification.

## 9. Sources and attribution

1. M. Laczkovich, *Tilings of triangles*, Discrete Mathematics 140 (1995), 79–94, Theorems 4.1, 5.1, 5.3. DOI: 10.1016/0012-365X(93)E0176-5. Exhaustive shape classification, as restated in the sources below.
2. M. Beeson and Y. X. Zhang, *Rationality of certain triangle tilings*, arXiv:2604.01314v1, Table 1 and Theorems 1.1–1.2. Read via https://arxiv.org/html/2604.01314v1 . This is the rationality input; an older flawed rationality proof is not used.
3. M. Beeson, *Tilings of an Isosceles Triangle*, arXiv:1206.1974v7, especially Theorems 2.1, 3.1, 7.8, 7.10, and 11.7. Read via https://arxiv.org/html/1206.1974v7 . The erroneous omission of N=2 from Corollary 7.9 is not used.
4. M. Beeson, *Triangle Tiling: The case 3α+2β=π*, arXiv:1206.2229v4, revised 25 September 2026. Read via https://arxiv.org/html/1206.2229v4 . Only the valid classification/normalization and construction inputs are used, not a retracted global prime conclusion or unproved necessary scale divisibility.
5. D. Paliy, project research with ChatGPT assistance, *Square-class obstructions and a uniform finite reduction for triangle tilings*, 30 September 2026, Library copy `Erdos634_uniform_reduction_proof_2026-09-30.md`. Immediate source of the complete necessary scale tables, two-character derivations, and difference-family scale-one exclusions.
6. D. Paliy, project research with ChatGPT assistance, *A complete construction for the other scalene Group 1 branch*, 29 September 2026, `docs/two-piece-construction.md` in the pinned repository. The QP construction and motif are prior project results; this note applies them.
7. The repository's 30 September literature audit and general-spectra attribution addendum credit Harries for the equilateral divisibility and 120-degree cutoff refinement previously reproduced in this project. Those are not claimed as new results here.

Repository: https://github.com/DenisUkranian/erdos-634-tilings/tree/50d7459bd1d3f41352630323f1c55a92e8d9b64e . This note and its checkers were prepared separately; no remote commit or external acceptance is asserted by their creation.
