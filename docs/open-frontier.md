# What is settled here, and what remains

**30 September 2026 · research snapshot v0.2.0**

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

## All five rational shapes at sufficiently large scales

The [universal annular theorem](universal-rational-scales.md) removes the earlier restriction on the sign of $\Delta=b(a^2+b^2)-a^2c$. For every primitive tile, each of the five rational target shapes admits **every sufficiently large arithmetically admissible scale**.

The mechanism is geometric: two explicitly dissected annuli increase a theta scale by $u$ and by $v$. Since $\gcd(u,v)=1$, these increments fill all sufficiently large scales from one seed. Seed existence for theta follows from Beeson v4, Corollary 5; the transfers to the other shapes use actual constructed pieces.

Set $Q=b+c$, $P=b+2c$, $F_0=(b-1)(c-1)$ and

$$
H_u=\left\lceil\frac{a^2+b^2+F_0}{ub}\right\rceil,\qquad
H_v=\left\lceil\frac{a^2+F_0}{bv}\right\rceil.
$$

Let

$$
C_{W,\beta}=v\left\lceil\frac{H_u}{v}\right\rceil+(u-1)(v-1).
$$

For any actual theta seed scale $s$, set

$$
C_\theta=s\left\lceil\frac{\max(H_u,H_v)}s\right\rceil+(u-1)(v-1).
$$

| Target shape | Necessary count form | Guaranteed construction |
|---|---|---|
| W | $QT^2$ | Every integer $T\ge C_{W,\beta}$ |
| Beta-isosceles | $PT^2$ | Every integer $T\ge C_{W,\beta}$ |
| Theta-isosceles | $bT^2$ | Every integer $T\ge C_\theta$ |
| Alpha-isosceles | $bQK^2$ | Every integer $K\ge\lceil C_\theta/v\rceil$ |
| Other scalene | $QPK^2$ | Every integer $K\ge1$ |

The W/beta bound uses only parameters and Beeson's known scale-$v$ construction. The [explicit seed appendix](explicit-theta-seeds.md) supplies $s$ directly from the parameters for both signs of $\Delta$, so the theta/alpha bound is numerical as well. The necessary theta and alpha forms are valid for nonsquarefree $b$ as well.

Consequently the earlier eventual divisors for W and beta are both $d=1$ for every primitive tile. The unresolved part is the least scales and their finite exceptions **for each fixed tile**. Primitive parameters remain unbounded, so this is not a finite global list of exceptions and not a solution of the unrestricted count problem.

## Complete classification for the tile (2,3,4)

For this tile, all triangular targets are now classified. The exact count set is

$$
\{t^2:t\ge1\}\cup
\{7t^2,11t^2,21t^2:t\ge2\}\cup
\{3t^2:t\ge4\}\cup
\{77t^2:t\ge1\}.
$$

The [fixed-tile theorem](first-tile-classification.md) gives the corresponding targets and proof dependencies. The W/beta spectra are credited to Bonfioli. The 75-tile theta construction supplies the formerly missing scale 5. The separately checked alpha21 obstruction, together with the theta-to-alpha construction, gives exactly $21t^2$ for $t\ge2$.

The 75-tile example also contradicts the integrality assertion in Beeson v4, Lemma 55: $\mu=15/2$, $M=5$. That lemma is not used by the prime candidate or these constructions. The count 75 was already globally admissible; the result concerns the specified tile and target.

## Global exclusion of 21

The [exhaustive arithmetic and source-based reduction](n21-global-reduction.md) shows that any 21-tiling must use tile $(2,3,4)$ in target $(12,12,21)$. The [391-state certificate](alpha-21-obstruction.md), independently replayed as 437 expanded states, excludes that instance. This proves global nonexistence at 21 under the stated published classification inputs, without the prime-case geometric candidates.

Bonfioli and Harries had already reported the exclusion. This is an independent compact proof and replay, with no priority claim. It settles one count and completes the fixed-tile table, but does not settle all composite counts.

## N=105: now globally excluded in this project

The [global proof](n105-global.md) supplies an exhaustive reduction and four complete fixed-target certificates. It includes both F1 candidates, (8,7,13) and (16,5,19), and both 60-degree equilateral candidates. The separate all-primes candidate is not a premise. See the [PDF](../research/n105/PROOF_N105.pdf) and [recorded replay](../research/n105/VERIFIED_RESULTS.json).

The older collar notes are retained as historical, limited-scope regression evidence. Their declarations that N=105 was unresolved describe that earlier stage, not the current result.

## New 60-degree and 120-degree spectra

The [general note](../research/general-spectra/PROOF.md) proves necessary equilateral counts N=abm² and constructs every m above the explicit thresholds 3(floor(A/B)+1) and 3(floor(A/B)+2), respectively, where A=max(a,b), B=min(a,b). It rederives the known F1 and isosceles necessary spectra with attribution, and transfers the 120-degree construction to their large multipliers. Its (45,32,67) example at m=9 has 116640 tiles.

Small multipliers remain unresolved in general. Infinite primitive tile parameters prevent replacing the per-tile finite intervals by a finite global exception list. The [full-solution roadmap](full-solution-roadmap.md) records the exact remaining quantifiers and obligations.

## What a full solution would still require

The preceding results leave general composite counts across several shape families unresolved. A full solution needs necessity and sufficiency covering every classified family, including their scales and exceptions; the roadmap distinguishes necessary criteria from sufficient constructions, together with sound dependence on the source classification. No finite batch of successful constructions, no isolated failed search, and no unforced geometric cut supplies that missing argument.

All new universal arguments in this snapshot are inspectable mathematical proofs or candidates with internal review. No external acceptance, formal verification of the full argument, or priority ruling is claimed.

## Integrated continuation: uniform reduction (30 September 2026)

The [uniform-reduction note](uniform-reduction.md) and its complete source, test data, and separately checked positive witnesses are included in this publication. Its results are necessary spectra, two squarefree congruence obstructions, a finite candidate overlist, and formal boundary-signature witnesses. They are not a complete all-integer classification. The N=154 search is recorded as INCOMPLETE. The root verification coordinator now also replays all supplementary tests of this module in a disposable copy. Historical reports are retained with their original preparation scope.
