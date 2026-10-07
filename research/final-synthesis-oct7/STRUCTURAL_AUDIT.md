# Structural audit and nonperiodicity inside square class 38

7 October 2026. Research with ChatGPT assistance. This note combines existing
project theorems with a new finite arithmetic deduction. It does not establish
external priority or a complete solution of Erdős problem 634.

## 1. Audit of the remaining global implication

The [thirteen-row ledger](../../docs/global-gap-2026-10-07.md) retains the
published angular-classification and rationality hypotheses, the similar,
right and rational-angle exceptions, both short-side orders, integer residual
scales, reflections, and T-junctions. For a specified count N, the two proved
implications are still

    known construction => actual tiling => necessary arithmetic candidate.

There is no proved reverse implication from necessary coefficients. In
particular:

- QP is completely constructive and may be removed from the unknown list.
- F3 is completely constructive for the ordered sector 0<a<2b; exchanging
  a and b changes its target and coefficient.
- F4 is constructive for a<b; its reversed order remains separate.
- The F1 and 60-degree equilateral coefficient sets agree, but this is not
  a same-count equivalence between arbitrary tilings in those two shapes.
- Every fixed norm tile has an effective constructive tail. The union of
  the norm-family representations below these tails is O(sqrt X) through X,
  but is still infinite as the primitive tile varies.
- Positive elliptic rank concerns existence somewhere in a square class.
  It does not prescribe a divisor of a given multiplier or fill a small
  geometric target.
- Complete incidence disks can be checked exactly. Their existence is the
  remaining geometric question; decidability for one N does not supply
  a structural classification of all N.

The [unique F3 coefficient for 4830](../strategy-oct7/plan-b.md) blocks any
universal attempt to replace a primitive candidate by another tile already
in a constructive cone. W-only and F3-only infinite families block deleting
one of those branches globally. No missing converse was found in the
existing repository results. Both 154 and 4830 remain unresolved here.

The next sections strengthen one known structural limitation: even within
one fixed square class, no finite list of congruence classes, with finitely
many exceptions, can determine admissibility.

## 2. An entire family of negative rays in class 38

Write

    M_38 = {m >= 1 : 38m^2 is an admissible count}.

**Theorem 1.** For every odd prime q and every integer k>=0,

\[
\boxed{3q^k\notin\mathcal M_{38}.}
\]

**Proof.** The complete odd-sector branch isolation in
[the class-38 theorem, Section 6](../../docs/infinite-minimal-multipliers.md)
shows that any odd admissible multiplier must arise from a primitive
positive F3 triple. Thus there would be positive integers a,b,c and s with

\[
\gcd(a,b)=1,\quad c^2=a^2+ab+b^2,\quad
3(a+b)(a+2b)=38s^2,\quad s\mid 3q^k.
\]

The factor 3 forces 3|s. If q!=3 this gives s=3q^r with 0<=r<=k; if q=3,
write s=3q^r with 0<=r<=k in exactly the same way. Set

\[
A=a+b,\qquad B=a+2b.
\]

Then

\[
AB=114q^{2r},\qquad \gcd(A,B)=1,\qquad A<B<2A.
\tag{1}
\]

When r>=1 all powers of q in the product occur in one factor; the other
factor divides 114 and is at most 114. The ratio in (1) therefore implies

\[
AB<2\cdot114^2,\qquad q^{2r}<228.
\]

For r=0 the latter inequality is automatic. The possible odd prime powers
z=q^r are consequently just

\[
z\in\{1,3,5,7,9,11,13\}.
\]

The following table lists **all** divisor pairs AB=114z^2 satisfying
A<B<2A. Recover a=2A-B and b=B-A, and test the norm.

| z | A | B | a | b | gcd(a,b) | a^2+ab+b^2 |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | none | | | | | |
| 3 | 27 | 38 | 16 | 11 | 1 | 553 |
| 5 | 38 | 75 | 1 | 37 | 1 | 1407 |
| 5 | 50 | 57 | 43 | 7 | 1 | 2199 |
| 7 | 57 | 98 | 16 | 41 | 1 | 2593 |
| 9 | 81 | 114 | 48 | 33 | 3 | 4977 |
| 11 | 114 | 121 | 107 | 7 | 1 | 12247 |
| 13 | 114 | 169 | 59 | 55 | 1 | 9751 |

Every last-column entry lies strictly between consecutive integer squares.
No primitive norm triple survives. This excludes the last possible branch
and proves the theorem. No geometric nonexistence search is used. QED.

In count form the theorem excludes every

\[
342q^{2k}\qquad(q\text{ an odd prime},\ k\ge0).
\]

This is stronger than testing one prime-power ray with squarefree kernel
38, because the multiplier has the additional prescribed factor 3.
It makes no statement about q=2 or unrestricted products of distinct primes.

## 3. No eventual congruence classification in this one square class

**Theorem 2.** For every positive integer M there is a residue r modulo M
containing infinitely many odd members of M_38 and infinitely many odd
nonmembers. In particular M_38, and its restriction to odd multipliers,
are not eventually periodic.

**Proof.** Apply the existing
[prime-avoidance theorem](../../docs/infinite-minimal-multipliers.md) with H
containing every prime divisor of 2M. It supplies an actual odd admissible
multiplier m_0 such that

\[
v_3(m_0)=1,\qquad
v_p(m_0)=0\quad(p\mid 2M,\ p\ne3).
\]

Consequently h=m_0/3 is an integer coprime to 2M. Dirichlet's theorem
therefore supplies infinitely many odd primes

\[
q\equiv h\pmod{2M}.
\]

For each of them the odd multiplier 3q is congruent to m_0 modulo M,
but is inadmissible by Theorem 1. This produces infinitely many negative
multipliers in that residue class.

On the positive side, subdividing every tile of the actual m_0 tiling
into (1+2Mj)^2 congruent triangles gives the actual admissible multipliers

\[
m_0(1+2Mj),\qquad j\ge0.
\]

All are odd and congruent to m_0 modulo M. They form an infinite positive
sequence. Thus the same residue class contains both answers arbitrarily
far out, proving the assertion. QED.

The analytic input is only the standard theorem that every reduced
arithmetic progression contains infinitely many primes. A primary course
source with statement and proof is K. S. Kedlaya, *Primes in arithmetic
progressions*, MIT 18.785 (spring 2007), Theorem 1, p. 1:
<https://kskedlaya.org/18.785/dirichlet.pdf> (inspected 7 October 2026).

## 4. Scope and reproducibility

Theorem 2 is not implied solely by infinitely many divisibility-minimal
members: the upward-closed, eventually constant set {2,3,4,...} already
has every prime as a divisibility-minimal member. The additional negative
rays and prime-avoidance property are essential to the proof here.

This excludes a fixed finite congruence classification with finite
exceptions even after fixing the kernel 38. It does not exclude finite
parameterized descriptions, divisor tests, elliptic descriptions,
algorithms using input-dependent moduli, or a full classification by a
stronger geometric theorem.

The complete finite arithmetic step can be replayed by

```sh
python research/final-synthesis-oct7/check_class38_nonperiodic.py
```

The checker constructs the finite table both by inverse factorization and
by independent forward (a,b) enumeration, verifies the nonsquares, and
checks the possible prime-power list. It does not pretend to computationally
prove the infinite prime-avoidance theorem, Dirichlet's theorem, or the
published angular classification. Those are explicit mathematical inputs.
No decision of 154 or 4830 and no full Erdős-634 solution follows.
