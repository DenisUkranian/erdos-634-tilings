# What is settled here, and what remains

**29 September 2026 · research snapshot v0.1.0**

Erdős problem 634 asks which positive integers occur as the number of congruent triangular pieces in a triangle. It quantifies over both the tile and the target. A result for one fixed tile and one target shape is therefore a different statement from a global exclusion or existence claim for a number.

## Prime counts

The principal deliverable is the [candidate proof for all primes](../paper/prime-case-candidate.pdf): exactly 2, 3 and the primes congruent to 1 modulo 4. The [dependency ledger](prime-case-dependencies.md) records the outside classification inputs. The scale-one W and beta-isosceles arguments are universal geometric arguments requiring external scrutiny; replaying finite coordinates does not certify them.

## A complete rational construction family

For a fixed primitive tile

$$
(a,b,c)=(uv,v^2-u^2,v^2),\qquad 0<u<v,\quad\gcd(u,v)=1,
$$

the target shape with angles $(2\alpha,\alpha,2\beta)$ has exactly the counts

$$
N=k^2(2v^2-u^2)(3v^2-u^2),\qquad k\ge1.
$$

The [two-piece proof](two-piece-construction.md) supplies both necessity and sufficiency. The 322 certificate is an explicit finite instance, independently replayed within the project. This result does not depend on the prime-case obstructions.

## W and beta-isosceles scales

The [scale-spectrum theorem](scale-spectra.md) shows that, for each fixed primitive tile, each of these two nonempty scale sets eventually consists exactly of the multiples of a divisor $d\mid v$. It also provides an explicit sufficient threshold from any additional verified seed.

The theorem does **not** determine the general value of $d$, the least scale in each attainable residue class, or a uniform bound on all exceptional scales. A search finding more constructions does not by itself certify that no later construction lowers the gcd.

For the first tile $(2,3,4)$, the complete W and beta spectra, respectively $7t^2$ and $11t^2$ for $t\ge2$, are already present in Vico Bonfioli's work. They are credited inputs, not claimed discoveries here. In particular, $v\mid t$ is not a necessary condition.

## The theta-isosceles branch

Write $b=qh^2$ with $q$ squarefree. The [theta note](theta-branch.md) gives the necessary form $N=qt^2$ and the stronger necessary bound

$$
qh(t-h)\ge2v.
$$

For tile $(2,3,4)$, the target has equal sides $6t$, base $3t$, and count $3t^2$. Scales 1, 2 and 3 are excluded. Every scale $t\ge4$, except possibly $t=5$, is constructed using the 48-, 108-, 147- and 243-tile seeds and geometric addition. Thus the only remaining case **for this tile and shape** is $(30,30,15)$ tiled by 75 copies of $(2,3,4)$.

The numbers 75, 147 and 243 are already globally admissible, being three times squares. The unresolved 75 instance is not a global open count. The odd-scale 147 and 243 constructions supply explicit counterexamples to the divisibility assertion in Lemma 55 of Beeson, arXiv:1206.2229v4; see the note and independent coordinate checks for the precise hypotheses.

For that remaining fixed 75 instance, the two-c-edge lemma reduces the base of length 15 to precisely two edge-count possibilities: $(A,B,C)=(2,1,2)$ or $(0,1,3)$ for lengths $(2,3,4)$. These are necessary boundary data, not a completed search or a sufficiency criterion.

There is also an explicit eventual construction of $N=bT^2$ in the range $b(a^2+b^2)-a^2c>0$. When $b$ is squarefree this covers every sufficiently large arithmetically possible scale. For general $b$, it only covers the stated subsequence. The complementary parameter range and finite exceptions are not classified here.

## The remaining N=105 investigation

The [arithmetic and additive-invariant reduction](n105-partial-results.md) and the [positional frontier](n105-positional-frontier.md) do not establish either a 105-tiling or its impossibility.

The two surviving irrational-angle 60-degree equilateral candidates, with tiles $(5,21,19)$ and $(7,15,13)$, each admit an exactly verified complete boundary collar. Their unfilled interiors have areas equal to 60 and 48 tiles respectively. These are partial placements, not full tilings. Their existence rules out a contradiction derived solely from that first boundary collar.

For the 120-degree scalene candidate with tile $(8,7,13)$ and target $(105,56,91)$, a particular macro-decomposition leaves an equilateral 56-tile remainder after a 49-tile corner block. The corner block has not been proved compulsory in every tiling. Therefore this decomposition is not an exclusion proof.

The established invariant barrier concerns **additive direction-length invariants**. It must not be extended to all noncommutative tiling-group invariants on the strength of finite quotient experiments.

## What a full solution would still require

The preceding results leave general composite counts across several shape families unresolved. A full solution needs necessity and sufficiency covering every classified family, including their scales and exceptions, together with sound dependence on the source classification. No finite batch of successful constructions, no isolated failed search, and no unforced geometric cut supplies that missing argument.

All new universal arguments in this snapshot are inspectable mathematical proofs or candidates with internal review. No external acceptance, formal verification of the full argument, or priority ruling is claimed.
