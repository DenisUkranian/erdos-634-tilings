# A linear local obstruction and a flexible extension of square class 78

7 October 2026. Research directed by Denis Paliy, with ChatGPT assistance.

This extends the [earlier product obstruction](../../quartic-descent-oct7/PROOF.md).
It gives a computable sufficient condition excluding **every odd multiplier**
in a square class. Passing the test is not a rational-point or tiling
existence theorem. No complete classification of Erdős 634 follows.

## 1. General matrix theorem

Let R be odd and squarefree, with 3 not dividing R and R = 5 modulo 8.
List all its prime factors as p_1,...,p_n. Let I be the indices for which
p_i = 1 modulo 12. All arithmetic defining the following matrix is over F_2.
For i in I and j different from i, set

\[
(-1)^{\lambda_{ij}}=\left(\frac{p_j}{p_i}\right),\qquad
(-1)^{h_i}=\left(\frac2{p_i}\right),\qquad
(-1)^{c_i}\equiv 3^{(p_i-1)/4}\pmod {p_i}.
\]

The last residue is ±1 because (3/p_i)=1. Define the |I|-by-n matrix M by

\[
M_{ij}=\lambda_{ij}\quad(j\ne i),\qquad
M_{ii}=c_i+\sum_{j\ne i}\lambda_{ij}.
\tag{1}
\]

**Theorem.** If any count 6Rm² with m odd is realizable, the linear system

\[
Ma=h
\tag{2}
\]

has a solution a in F_2^n. Consequently, inconsistency of (2) excludes
every odd multiplier in this square class. Equivalently, it is enough to
supply a vector z in F_2^{|I|} satisfying

\[
z^TM=0,\qquad z^Th=1.
\tag{3}
\]

Once R is factored, the obstruction is evaluated by modular exponentiation
and Gaussian elimination. This avoids enumerating all 2^n descent covers.

If every p_i is 1 modulo 12, quadratic reciprocity makes M symmetric. In
that case (3) becomes Mz=0 and z·h=1. If all p_i are 13 modulo 24, then
h is the all-ones vector, so any odd-weight kernel vector suffices.

## 2. Reduction from tilings to the same quartic covers

The [existing F3 isolation](../../../docs/f3-global-overlap.md) applies
because 6Rm² = 14 modulo 16 and its 3-adic valuation is odd. The W branch
cannot occur: for primitive coprime u,v, 3 never divides 2v²−u².
Thus a tiling would give

\[
3(a+b)(a+2b)t^2=6Rm^2,\qquad c^2=a^2+ab+b^2.
\]

Here the geometric side variables a,b,c are unrelated to the binary
vector a in (2). Since 6R is squarefree, t divides m. Put
s=m/t, S=a+b, T=a+2b. Then

\[
ST=2Rs^2,\qquad c^2=T^2-3ST+3S^2.
\]

As s is odd, S is odd and v_2(T)=1: otherwise reduction modulo 4 would
give c²=3. The rational map

\[
x=\frac{2R(2c+2T-3S)}S,\qquad y=\frac{4Rsx}S
\]

therefore gives x>0, v_2(x)=1 and

\[
y^2=x^3+12Rx^2-12R^2x.
\tag{4}
\]

The elementary valuation argument from the earlier proof shows that the
squarefree part of x is supported on 2,3 and R. Thus

\[
x=e(u/v)^2,\qquad e=2\varepsilon A,\quad
\varepsilon\in\{1,3\},\quad A\mid R,\quad B=R/A,
\]

with positive coprime integers u,v. Equation (4) implies

\[
W^2=e u^4+12R u^2v^2-\frac{12R^2}{e}v^4,
\qquad W\in\mathbb Z.
\tag{5}
\]

No congruence condition on the other prime divisors of R was used in this
reduction. This observation permits the rectangular matrix in §1.

## 3. Exact character conditions at the selected primes

Fix p=p_i with i in I, so p is 1 modulo 12. In particular
(−1/p)=(3/p)=1. Write η_p=(2/p) and
χ_p=3^{(p−1)/4}, interpreted as the sign ±1.

If p divides B, reducing (5) modulo p when u is a unit, or dividing by p²
first when p divides u, gives the same necessary requirement (e/p)=1.
Because (ε/p)=1, this is exactly

\[
\left(\frac A p\right)=\eta_p\qquad(p\mid B).
\tag{6}
\]

If p divides A, write e=pδ and 2R=pκ. Exactly one of u,v being a unit
would give valuation one on the right of (5), impossible for a square.
Thus both are units. Dividing (5) by p and reducing modulo p gives

\[
q^2+6q-3=0,\qquad
q=\frac{\delta u^2}{\kappa v^2},\qquad
\left(\frac q p\right)=\left(\frac Bp\right).
\]

For r²=3 modulo p, its two roots −3±2r have the same character, because
their product is −3. The identity

\[
-3+2r=\frac{r(r-1)^2}{2}
\]

shows that their common character is η_p χ_p. Here r is nonzero and
r−1 is nonzero, since p>3. Consequently

\[
\left(\frac Bp\right)=\eta_p\chi_p\qquad(p\mid A).
\tag{7}
\]

For each fixed cover and either ε, (6) and (7) are also sufficient for
local solubility **at this prime p only**. For p|B, take u=1 and v=p;
the right side of (5) is a p-adic unit with square residue. For p|A,
choose a root q with the prescribed character and take v=1. There is a
nonzero u_0 modulo p with δu_0²/κ=q. In (5) divided by p, with W=0,
the derivative of the right side at u_0 is
4κu_0(q+3), which is nonzero modulo p. Hensel's lemma gives a p-adic
solution. No simultaneous global or all-prime sufficiency is asserted.

## 4. Linearization and the dual certificate

Let a_i=1 mean p_i|A and a_i=0 mean p_i|B. If a_i=0, (6) reads
Σ_{j≠i} λ_ij a_j = h_i. If a_i=1, (7) reads
Σ_{j≠i} λ_ij(1−a_j) = h_i+c_i. These two cases are precisely

\[
\sum_{j\ne i}\lambda_{ij}a_j+
\left(c_i+\sum_{j\ne i}\lambda_{ij}\right)a_i=h_i.
\]

This proves (2). The dual criterion (3) is ordinary linear algebra over
F_2. In the square symmetric case it is equivalently orthogonality of h
to every vector in ker M.

The earlier product theorem is recovered when every p_i is 13 modulo 24,
every c_i=0 and n is odd. Then M is a graph Laplacian, M1=0, and
1·h=n=1 in F_2. The new criterion also handles mixed quartic characters,
primes 1 modulo 24, and unselected prime factors outside 1 modulo 12.

## 5. A simple flexible single-prime obstruction

**Corollary.** Suppose R is odd and squarefree, 3 does not divide R,
R=5 modulo 8, 13 divides R, and every prime q dividing R/13 satisfies
(q/13)=1. Then 6Rm² is impossible for every odd positive m.

Indeed, the row indexed by 13 is zero: all its λ_ij vanish and
3³=1 modulo 13 gives c_i=0. But h_i=1 because (2/13)=−1. Thus that
single row of (2) would say 0=1. Equivalently, when 13|B condition (6)
fails; when 13|A condition (7) fails.

In particular, for every prime q=1 modulo 104,

\[
\boxed{78q\,m^2\text{ is impossible for every odd }m.}
\tag{8}
\]

Here q=1 modulo 8 ensures 13q=5 modulo 8, and q=1 modulo 13 gives
the required square symbol. Such a prime is neither 3 nor 13.
The first examples are q=313,521,937, yielding kernels
24414,40638,73086. Dirichlet's theorem gives infinitely many q in this
progression. More generally, any product Q of distinct primes 1 modulo
104 works in R=13Q, with no restriction on the number of those primes.

This family needs no quartic-residue hypothesis on the other primes.
For example q=521 is 5 modulo 12 and lies outside the selected-prime
matrix rows entirely. The obstruction still comes from the row at 13.

A mixed family using only primes 13 modulo 24 is

\[
R=13\cdot61\cdot q,\qquad q\equiv157\pmod {312}
\]

with q prime. The fixed prime 61 has χ_61=−1, whereas (61/13)=1,
and q=1 modulo 13. Hence all odd multiples 4758q m² are impossible.
The first q=157 gives the squarefree kernel 747006. This is an infinite
family outside the hypotheses of the earlier all-χ=+1 product theorem.

Dirichlet's theorem is a standard external input; see
[Kedlaya, Analytic Number Theory, Theorem 4.2](https://kskedlaya.org/ant/chap-primes-in-ap.html).
The congruence progressions have coprime initial term and modulus.

## 6. A matrix obstruction with no zero row

Take the ordered primes (13,37,61,109,181). All are 13 modulo 24, and
their quartic-character bits are (0,1,1,0,0). The matrix is

\[
M=\begin{pmatrix}
0&1&0&1&0\\
1&0&1&1&0\\
0&1&1&0&1\\
1&1&0&1&1\\
0&0&1&1&0
\end{pmatrix},\qquad h=(1,1,1,1,1)^T.
\]

The vector z=(0,1,1,1,0)^T satisfies Mz=0 and z·h=1. No row is zero,
so this is stronger than the single-prime corollary. It excludes every
odd multiplier in square class

\[
6\cdot13\cdot37\cdot61\cdot109\cdot181=3473211534.
\]

## 7. Scope, checking and attribution

The local matrix is an exact reformulation of solubility of the two
ε-covers at the selected primes p_i=1 modulo 12. It does not check 2,
3, unselected primes, or global rational solubility. A consistent system
can still correspond to no tiling. The theorem is a negative criterion,
not an if-and-only-if classification of counts.

The previous effective theta construction provides all sufficiently
large even multipliers in each excluded square class. Small even
multipliers remain outside this note, except previously settled classes.
The counts 154 and 4830 are not resolved by this argument.

`check_matrix.py` checks matrix/partition equivalence, Gaussian-elimination
and dual certificates, root characters, the examples, and residue-level
local conditions. Finite checks support the written general proof; they
do not replace it. The geometric spectra, rationality, theta construction,
Hensel's lemma and Dirichlet's theorem are external or earlier inputs.
This work was developed with ChatGPT assistance. No external human review,
formal verification or priority over the literature is claimed.
