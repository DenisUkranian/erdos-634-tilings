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

The [new eventual-construction theorem](eventual-rational-families.md) now determines $d=1$ whenever $\Delta=b(a^2+b^2)-a^2c>0$. Outside that parameter range, the general value of $d$ is still undetermined. The least admissible scales and finite exceptions are not classified in general. A search finding more constructions does not by itself certify that no later construction lowers the gcd.

For the first tile $(2,3,4)$, the complete W and beta spectra, respectively $7t^2$ and $11t^2$ for $t\ge2$, are already present in Vico Bonfioli's work. They are credited inputs, not claimed discoveries here. In particular, $v\mid t$ is not a necessary condition.

## The theta-isosceles branch

For every primitive rational tile in the $3\alpha+2\beta=\pi$ family, the [theta note](theta-branch.md) now gives the stronger necessary form

$$
N=bT^2,\qquad T\in\mathbb Z_{>0},
$$

using two direction characters and parity. This applies even when $b$ is not squarefree. The independent boundary bound becomes

$$
b(T-1)\ge2v.
$$

For tile $(2,3,4)$, the target has equal sides $6t$, base $3t$, and count $3t^2$. Scales 1, 2 and 3 are excluded. The 75-tile construction fills the last missing scale $t=5$; the supplied seeds and geometric addition realize every $t\ge4$. The exact spectrum **for this tile and shape** is therefore $N=3t^2$ for every integer $t\ge4$.

The numbers 75, 147 and 243 were already globally admissible, being three times squares. The new 75 certificate specifically tiles $(30,30,15)$ with 75 copies of $(2,3,4)$; it is a result about the prescribed tile and target. It also gives a smaller counterexample to the integrality/divisibility assertion in Lemma 55 of Beeson, arXiv:1206.2229v4: $\mu=15/2$, $M=5$. See the note and the independent coordinate checks for the precise hypotheses.

There is also an explicit eventual construction of $N=bT^2$ in the range $b(a^2+b^2)-a^2c>0$. Together with the stronger necessary form, this covers every sufficiently large arithmetically possible scale throughout that range, including nonsquarefree $b$. The complementary parameter range and finite exceptions are not classified here.

## Eventual classification for all five rational shapes when $\Delta>0$

Let $Q=b+c$, $P=b+2c$ and set

$$
\Delta=b(a^2+b^2)-a^2c,\qquad F=(a-1)(b-1),\qquad
B=\left\lceil\frac{(a^2c+F)(a^2+b^2)}{u\Delta}\right\rceil.
$$

For $\Delta>0$, the [construction and transfer theorem](eventual-rational-families.md) supplies:

| Target shape | Necessary count form | Guaranteed construction |
|---|---|---|
| $W=(2\alpha,\beta,\alpha+\beta)$ | $N=QT^2$ | Every integer $T\ge B$ |
| $\beta$-isosceles | $N=PT^2$ | Every integer $T\ge B$ |
| $\theta$-isosceles | $N=bT^2$ | Every integer $T\ge B$ |
| $\alpha$-isosceles | $N=bQK^2$ | Every integer $K\ge\lceil B/v\rceil$ |
| Other scalene $(2\alpha,\alpha,2\beta)$ | $N=QPK^2$ | Every integer $K\ge1$ |

The sharper necessary count forms in the theta and alpha rows follow from two direction characters and parity for **every** primitive tile; only the displayed eventual existence bounds require $\Delta>0$. The other-scalene construction works for every primitive parameter pair without that restriction.

Thus this parameter range has only finitely many potentially unresolved scales per fixed tile, with an explicit bound. This is not a uniform finite list for all tiles, and it leaves the complementary range $\Delta<0$ and small exceptions unresolved in general. The proof transfers actual theta tilings to the other shapes; no unproved assumption that every hypothetical tiling has that decomposition is used.

## The remaining N=105 investigation

The [arithmetic and additive-invariant reduction](n105-partial-results.md) and the [positional frontier](n105-positional-frontier.md) do not establish either a 105-tiling or its impossibility.

The two surviving irrational-angle 60-degree equilateral candidates, with tiles $(5,21,19)$ and $(7,15,13)$, each admit an exactly checked partial placement covering the outer boundary. Their unfilled interiors have areas equal to 60 and 48 tiles respectively. These are partial placements, not full tilings. Boundary coverage and the finite geometric checks do not establish extendability, and they do not rule out further obstructions involving the inner frontier of a collar.

The [four-placement inner-corner argument](n105-fixed-collar-obstructions.md)
now proves that neither of these two particular collars extends: all four
possible first tiles at one convex inner corner overlap already placed tiles.
Both complete one-node refutations have separate exact replays. This rejects
two fixed configurations, not either tile globally and not the count 105.

For the 120-degree scalene candidate with tile $(8,7,13)$ and target $(105,56,91)$, a particular macro-decomposition leaves an equilateral 56-tile remainder after a 49-tile corner block. The corner block has not been proved compulsory in every tiling. Therefore this decomposition is not an exclusion proof.

The established invariant barrier concerns **additive direction-length invariants**. It must not be extended to all noncommutative tiling-group invariants on the strength of finite quotient experiments.

## What a full solution would still require

The preceding results leave general composite counts across several shape families unresolved. A full solution needs necessity and sufficiency covering every classified family, including their scales and exceptions, together with sound dependence on the source classification. No finite batch of successful constructions, no isolated failed search, and no unforced geometric cut supplies that missing argument.

All new universal arguments in this snapshot are inspectable mathematical proofs or candidates with internal review. No external acceptance, formal verification of the full argument, or priority ruling is claimed.
