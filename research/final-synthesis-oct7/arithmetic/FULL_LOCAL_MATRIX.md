# The full local matrix at 2, 3 and the prime factors of R

7 October 2026. Research directed by Denis Paliy, with ChatGPT assistance.

This strengthens the [selected-prime matrix](MATRIX_OBSTRUCTION.md).
It gives an exact linear criterion for local solubility of the relevant
quartic covers at every prime dividing 6R, with the required valuation at 2.
It remains a necessary test for tiling, not a global existence theorem.

## Theorem

Let R be odd, squarefree, coprime to 3, and congruent to 5 modulo 8.
Write its distinct prime factors as p_1,...,p_n. Use binary variables
a_1,...,a_n,f, with

\[
A=\prod_i p_i^{a_i},\qquad B=R/A,\qquad
\varepsilon=3^f,\qquad e=2\varepsilon A.
\]

For i≠j let λ_ij be the bit of the Legendre symbol (p_j/p_i), meaning
the symbol is (−1)^λ_ij. Let h_i be the bit of (2/p_i). For p_i=1
modulo 12 only, let c_i be the bit of 3^((p_i−1)/4), interpreted as ±1.

Form the following system over F_2:

| Prime condition | Required equation(s) |
| --- | --- |
| p_i=1 mod12 | Σ_{j≠i}λ_ij a_j + (c_i+Σ_{j≠i}λ_ij)a_i = h_i |
| p_i=5 mod12 | a_i=0 |
| p_i=7 mod12 | a_i=0 and Σ_{j≠i}λ_ij a_j + f = h_i |
| p_i=11 mod12 | No equation |
| The prime 2 | f + Σ_{p_j=3 mod4} a_j = 1 |

For each assignment of the variables, this system holds **if and only if**
the cover

\[
W^2= e u^4+12R u^2v^2-\frac{12R^2}{e}v^4
\tag{1}
\]

has a nontrivial local point at each prime dividing 6R, with u,v both
2-adic units at the prime 2. The local points at different primes need not
be the same point or come from a rational point.

Consequently, if the system is inconsistent, no count 6Rm² with m odd
is realizable. A Gaussian-elimination certificate consists of a set of
rows whose sum has zero coefficients and right-hand side one.

The tiling implication uses exactly the F3 reduction and rational map in
[§2 of the preceding note](MATRIX_OBSTRUCTION.md). No new geometric or
rank assumption enters this theorem.

## Proof at odd primes dividing R

For a p-adic point, scale the homogeneous coordinates so u,v are integral
and at least one is a unit.

**Case p|B.** The right side of (1) has coefficients of valuations 0,1,2.
If u is a unit, its residue is e u⁴, requiring (e/p)=1. If p divides u,
then v is a unit and division by p² requires (−12/e /p)=1. Conversely,
either character condition gives a local point: use (u,v)=(1,p) in the
first case or (p,1) in the second. After removing the even valuation, a
unit with square residue is a p-adic square. Thus the exact condition is

\[
(e/p)=1\quad\hbox{or}\quad\left(\frac{-12/e}{p}\right)=1.
\tag{2}
\]

If (−3/p)=−1, the two characters are opposite and there is no restriction.
If (−3/p)=1, condition (2) reduces to (e/p)=1.

**Case p|A.** Both u,v must be units; otherwise the right side of (1)
has valuation one. Write e=pδ and 2R=pκ. Since p|W, divide (1) by p
and reduce modulo p. The necessary equation is

\[
q^2+6q-3=0,\qquad q=\frac{\delta u^2}{\kappa v^2}.
\tag{3}
\]

Its discriminant is 48. If (3/p)=−1, there is no root, so a_i=0 is
forced. If (3/p)=1, its roots are −3±2√3, both nonzero.

When p=11 modulo 12, (−3/p)=−1, so these roots have opposite characters.
One therefore has the prescribed character (δ/κ /p), whatever A,B,ε are.
There is no restriction in this case.

When p=1 modulo 12, (ε/p)=1 and both roots have the same character
(2/p)χ_p, where χ_p=3^((p−1)/4). The identity
−3+2r=r(r−1)²/2 for r²=3 proves this assertion. Their required character
is (B/p), giving precisely the first row type in the table, together
with case p|B. This is the previous matrix derivation.

All admissible roots in (3) lift: take v=1 and W=0, and choose u_0
with δu_0²/κ=q modulo p. The derivative of the divided quartic at u_0
is 4κu_0(q+3), nonzero modulo p. Hensel's lemma applies.

Finally, classify the inert primes (3/p)=−1. These are p=5 or7 modulo
12, and they have already forced a_i=0. At p=5 modulo12, (−3/p)=−1,
so (2) is automatic. At p=7 modulo12, (−3/p)=1 and (3/p)=−1, so
(e/p)=1 becomes Σ_{j≠i}λ_ij a_j+f=h_i. This proves all odd-prime rows
and their local sufficiency.

## Exact condition at 2

The required v_2(x)=1, with x=e(u/v)², means u and v can both be taken
to be odd. Since R=1 modulo4, reduction of (1) modulo16 gives

\[
W^2\equiv
\begin{cases}
4(3R-A)&\varepsilon=1,\\
4(A+3R)&\varepsilon=3.
\end{cases}
\pmod {16}.
\]

Each expression is either 0 or8 modulo16; only 0 is a square. Thus

\[
\varepsilon A\equiv3\pmod4,
\tag{4}
\]

which is exactly the last row of the table.

This necessary condition is sufficient. Set v=1 and let

\[
F(u)=2A\left(\varepsilon u^4+6Bu^2-
\frac3\varepsilon B^2\right).
\]

Under AB=5 modulo8 and (4), the four possibilities for
(ε,A mod8,B mod8) are
(1,3,7), (1,7,3), (3,1,5), (3,5,1).
In each case

\[
F(1)/16\equiv1\pmod4,\qquad
\frac{F(3)-F(1)}{16}=2A(5\varepsilon+3B)\equiv4\pmod8.
\tag{5}
\]

The first quotient is integral. To check its residue without assuming
more than A,B modulo8, use
F(1)/16=A(1+6B−3B²)/8 for ε=1 and
F(1)/16=A(3+6B−B²)/8 for ε=3. Replacing B by B+8 preserves the quotient
modulo4 in the corresponding cases. Hence one of u=1 or3 makes F(u)/16
congruent to1 modulo8. Every such 2-adic unit is a square, so F(u) has
a 2-adic square root, proving sufficiency with u,v odd.

## The prime 3 adds no new equation

When ε=1, a primitive local point of (1) requires A=2 modulo3. Indeed,
if u is divisible by3, the right side has valuation one, impossible;
otherwise reduction modulo3 gives W²=2A u⁴. Conversely, if A=2 modulo3,
take (u,v)=(1,3); the right side is a square unit modulo3 and hence in Q_3.

When ε=3, the same argument with v in place of u gives the exact
condition A=1 modulo3. Sufficiency follows from (u,v)=(3,1).
Together these conditions are

\[
f+\sum_{p_j=2\bmod3}a_j=1.
\tag{6}
\]

The odd-prime rows have already forced a_j=0 for primes 5 and7 modulo12.
The remaining possible factors of A are 1 or11 modulo12. For these,
the properties p=2 modulo3 and p=3 modulo4 coincide. Thus (6) is
identical to the last row in the table. This proves the stated equivalence
at every prime dividing 6R.

## Consequences and limits

The single-13 corollary in the preceding note remains valid. For example
13·17 has all other factors quadratic residues modulo13 and is5 modulo8,
so **1326m² is impossible for every odd m**. The same argument excludes
all odd multipliers in kernels 8814=78·113, 18174=78·233 and 20046=78·257.
An elementary infinite subfamily is 78q with q prime and q=1 modulo104;
arbitrary squarefree products of these q also work as cofactors of13.

The added rows can exclude cases missed by the selected-prime matrix.
For R=7·19, both factors are inert, so a_7=a_19=0. The rows at7 and19
respectively require f=0 and f=1. Hence every odd multiplier in square
class 798 is excluded. This example illustrates the additional rows;
no claim of priority for the individual count or class is made.

Consistency supplies local points on a cover. It does not supply a
rational point, an integral norm triple at a prescribed multiplier, or a
geometric tiling. Even these three subsequent requirements are distinct.
In particular, this theorem does not resolve 154, 4830, or Erdős634.

`check_full_matrix.py` compares the linear system with direct local
quartic calculations, verifies explicit dual certificates, and checks
the 2-adic construction for all odd A,B modulo128 with AB=5 modulo8.
The accompanying JSON records the exact counts and examples. These
checks support the universal proof above, not replace it. The prior
geometric classification and rationality inputs remain explicit dependencies.

The method belongs to the established theory of local descent and Selmer
groups. Related literature includes [Liu–Yang–Feng (2020)](https://arxiv.org/abs/2010.09238)
and [Wei–Guo (2022)](https://arxiv.org/abs/2210.01678) on π/3- and
2π/3-congruent numbers and associated elliptic curves. Their terminology
"tiling numbers" and their curve families must not be identified with all
prescribed counts in Erdős634 without an explicit reduction. No novelty of
the general matrix or descent method is claimed here.
