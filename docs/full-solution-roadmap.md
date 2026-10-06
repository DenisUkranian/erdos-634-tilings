# What would constitute a complete solution of Erdős problem 634?

**Assessment of this repository, updated 3 October 2026 — not a claim that every remaining subproblem is new or open in the literature.**

## The actual quantifiers

Let

$$\mathcal S=\{N\in\mathbb Z_{>0}:\text{some triangle has a dissection into }N\text{ congruent triangles}\}.$$

The task is a necessary-and-sufficient characterization of membership in **S for every N**. Positive membership needs just one valid tile and target. Negative membership must exclude **every** permitted tile/target family. Solving N=105, solving all primes, or solving one fixed tile does not answer that all-integer question.

A complete fixed-tile spectrum for every shape would be one sufficient route. It is **not logically necessary** to resolve every fixed-tile question separately: an alternative global characterization could exploit overlap, because a count already constructed by another tile is globally admissible. The roadmap below is an organized route, not an artificially stronger definition of the problem.

## What is already available here

| Block | Available result | What it does not decide |
|---|---|---|
| Square-class tails and prime-power rays | [Finite arithmetic criteria](square-class-tails.md) decide whether all sufficiently large `d m²` occur, and whether any `d q^(2k)` occurs for fixed odd prime `q`. In the latter question only product coefficients with `q^r<2d` need checking. | A positive ray test leaves its small exponents undecided. Failure of cofinal saturation does not exclude arbitrary composite multipliers. |
| Size of the global set of counts | [Quantitative density bound](quantitative-density.md): `S(X) ≪ X / ((log X)^δ (log log X)^(3/2))`, with `δ=0.086071…`; strengthens the integrated [1 October qualitative proof](long-seams-density.md). | A counting bound does not characterize membership of the remaining sparse set, and does not supply an effective exclusion percentage at a specified finite X. |
| Classical/similar tilings | Published classifications and explicit constructions; among familiar admissible families are k², 2k², 3k², 6k² and sums of two squares. Exact source hypotheses remain necessary. | Not a proof that these are all global counts; 322 is an explicit nonclassical construction. |
| Prime counts | [Candidate deduction](prime-case-dependencies.md) from the two scale-one geometric candidates and cited classifications. | Not externally accepted or formally checked here; in any event it concerns primes, not arbitrary composites. |
| Group 1: 3alpha+2beta=pi | [All-five-shape eventual construction](universal-rational-scales.md), explicit bounds/seeds; a complete other-scalene family and a complete [fixed (2,3,4) spectrum](first-tile-classification.md). | The small admissible scales for general primitive (u,v), including the relevant W, beta, theta and alpha targets, are not classified by the eventual theorem. |
| General W and beta cap | [Explicit collars](../research/w-beta-caps/PROOF.md) construct every scale in v+<u,v>, hence every m>=uv-u+1. | This is a sufficient set, not a proved exact spectrum; for example it leaves scale 4 of tile (6,5,9) undecided. |
| General 120-degree surgery | [Smaller trapezoids](../research/group2-trapezoids/PROOF.md) and [balanced F4/F2/F3 transfers](../research/group2-trapezoids/BALANCED_F4.md), including all m>=2 when b<a and 3c>=4a. | The exact trapezoid spectrum, the primitive scale-one cases and the complementary parameter range are not settled by these sufficient results. |
| Oriented 120-degree F4, a<b | [Four-region construction](../research/group2-f4/PROOF.md) supplies every positive integer multiplier. | Reversing a and b changes the target and does not preserve this construction; the a>b branch remains unresolved in general. |
| 60°/120° equilateral | [Necessary N=abm² and sufficient large-m bounds](../research/general-spectra/PROOF.md). | The exact realizable set below the sufficient threshold for each primitive tile. Passing parity/area tests is not a tiling. |
| 120° F1 and isosceles | Necessary spectra b(a+b)m² and b(a+2b)m², with large-m constructions by transfer. The spectra are credited to Bonfioli. | Small m; a sufficient cutoff is not a necessary cutoff. The 116640-tile example demonstrates why that distinction matters. |
| Other classified irrational-angle shapes | Published shape/rationality inputs and explicit branch-specific necessary equations, audited in the [105 reduction](../research/n105/PROOF_N105.md). | A contradiction for squarefree 105 cannot be generalized to all composites. The gamma=2alpha and other 120° scalene families must retain their full hypotheses in a global argument. |
| Single negative counts | Complete project arguments for [21](n21-global-reduction.md) and [105](n105-global.md), with published-input dependencies and exact certificates. | No inference that every other unconstructed number is impossible. |

## The concrete mathematical work still needed

**1. Finish the global classification ledger.** Use an exhaustive published angular classification, and make the normalization, side rationality, integer scales, and overlaps explicit for every branch. Sources with withdrawn claims may only be used for independently valid, specifically identified statements. Table 1 and Theorems 1.1–1.2 of Beeson–Zhang [BZ] are the rationality/classification entry point, not a count-existence theorem.

**2. Close necessity versus sufficiency.** For a fixed primitive 60°/120° tile set A=max(a,b), B=min(a,b). The earlier equilateral bounds are 3(floor(A/B)+1) for 60° and 3(floor(A/B)+2) for 120°; the new 120° trapezoids sharpen the latter to 3 ceil(c/B), with further parameter-specific improvements. The finite interval below a sufficient threshold still needs either constructions or obstructions. Group-1 annuli similarly give eventual spectra, not exact minimum scales. Arithmetic admissibility alone cannot fill the gap; the N=105 instances themselves pass substantial arithmetic tests but are geometrically impossible.

**3. Eliminate the infinite-parameter gap.** There are infinitely many primitive tiles. “Only finitely many exceptions for each fixed tile” is not a finite global list. A successful structural route could supply a uniform theorem or an exhaustive family of constructions and obstructions. The integrated uniform-reduction note now supplies an explicit finite candidate list and a complete abstract per-N search, subject to the cited classification inputs. The general fixed-N decidability principle already appears in earlier literature and is not claimed as a new solution. This does not prove a finite global exception list, nor does it turn any resource-limited INCOMPLETE run into an answer.

**4. Prove both directions of one final statement.** State a set or criterion C and prove N∈C implies a construction, and N∉C implies impossibility across the exhaustive branches. Do not require a fixed-tile solution when a different tile already supplies the required positive witness; do not omit any tile on the negative side. Include N=1,2,3, the rational-angle exceptions, orientation symmetries and T-junctions.

**5. Validate the universal steps, not only finite certificates.** The prime candidate still needs scrutiny of the forced patch and strictly decreasing column dependencies. The c-relation audit proves the sharp arithmetic thresholds but not those geometric inductions. For nonexistence certificates, root generation, fan completeness, supported-boundary marks and convex-capped chain hypotheses must stay explicit. External review or formalization would strengthen confidence; neither can substitute for a missing mathematical implication.

## Why more case counts alone will not finish it

The convex-capped chain lemma and exact fan checker are reusable tools. An isolated excluded N, even with a small certificate, does not supply a rule for all N. Progress toward the full problem should target the gap between necessary spectra and actual realizability, rather than describe a rising number of checked configurations as a percentage of the infinite classification.

The short-term review targets are therefore precise: the universal scale-one candidates, the parameter-dependent small-m spectra, the remaining branch conditions, and an all-N mechanism connecting them. This repository's **full_Erdos634_solved remains false**.

The [finite-scheme investigation](finite-schemes-attack.md) distinguishes
the already-refuted absolute grid-block bound from explicit recipes with
unbounded repetitions. A uniform orientation bound is necessary for the
subclass of recipes whose orientation counts are uniformly bounded; it
does not follow from an arbitrary finite recursive description. The
[capacity extension](grid-capacity-and-orientations.md) supplies tileable
pairs with unbounded convex grid-block complexity and at most 18 rigid
orientations. Neither the universal orientation bound nor completeness
of the broader finite catalog is established.

## Sources and source limitations

[BZ] M. Beeson and Y. X Zhang, *Rationality of certain triangle tilings*, [arXiv:2604.01314v1](https://arxiv.org/html/2604.01314v1), Table 1 and Theorems 1.1–1.2.

[Z] Y. X Zhang, *Tiling Triangles with 2pi/3 Angles*, [arXiv:2512.22696v4](https://arxiv.org/pdf/2512.22696v4). The construction theorems and separately labelled conjectural completeness/cutoff statements must not be conflated.

The [project source ledger](sources-and-provenance.md), [prime dependency ledger](prime-case-dependencies.md), and [N105 proof references](../research/n105/PROOF_N105.md#references-only-the-specified-inputs-are-used) identify the exact versions used. Source retrieval is not an adjudication of the entire literature or priority. The [problem statement](https://www.erdosproblems.com/634) concerns all integers; a cached website label is not evidence that this repository solves it.

## Integrated continuation: uniform reduction (30 September 2026)

The [uniform-reduction note](uniform-reduction.md) and its complete source, test data, and separately checked positive witnesses are included in this publication. Its results are necessary spectra, two squarefree congruence obstructions, a finite candidate overlist, and formal boundary-signature witnesses. They are not a complete all-integer classification. The N=154 search is recorded as INCOMPLETE. The root verification coordinator now also replays all supplementary tests of this module in a disposable copy. Historical reports are retained with their original preparation scope.

## 6 October: the universal pure-switch route is closed negatively

The [nonconvex counterexample](nonconvex-chirality-counterexample.md) is a
simple all-long-edge disk tiled by 1862 pure `(3,5,7)` triangles, with no
opposite-state pure tiling. The boundary forces the impossible population
`(930,-30,962)`. It already has one lattice phase and whole long contacts,
so the [phase reduction](nonconvex-pure-island-reduction.md) cannot remove
this obstruction. General pure-island exchange is therefore false and
should no longer be pursued as a missing universal lemma.

The [triangular embedding](extreme-pure-island-in-triangle.md) also defeats
the proposed restriction to extreme components actually occurring in a
triangular target. The bad island can be the unique maximal `+1` component
of an equilateral tiling whose exterior edges have only levels `-1,0`.
Neither a single opposite pure switch nor a finite sequence of those
switches confined to this island can remove all of its `+1` tiles.

A surviving normalization route must allow a different class of changes,
such as mixed states or modifications outside the island.
The same whole triangle has a separate low-level tiling, so global
normalization is not contradicted. No completeness theorem for those
broader moves is established. The independent Group-1 and all-count
membership gaps also remain.

## 6 October: exact decisions about infinite square-class families

The [square-class criterion](square-class-tails.md) closes a different
unbounded quantifier: whether every sufficiently large multiplier in a
given square class is admissible. This now has a finite divisor-and-square
test. The same argument decides whether an odd-prime-power ray contains
any admissible count at all; a positive witness supplies an effective
tail of exponents through existing constructions.

The proof also identifies a concrete limit of trying to settle each
square class by one universal cutoff. In class 22, all odd-prime-power
multipliers are impossible, while the previously constructed composite
multiplier and its odd multiples yield infinitely many actual tilings.
Thus the remaining individual-membership problem includes square classes
with infinitely many positive and negative odd multipliers. The new
criterion correctly distinguishes these from classes with a cofinal
positive tail; it does not decide their arbitrary composite multipliers.
