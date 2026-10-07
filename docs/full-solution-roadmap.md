# What would constitute a complete solution of Erdős problem 634?

**Assessment of this repository, updated 7 October 2026 — not a claim that every remaining subproblem is new or open in the literature.**

## The actual quantifiers

Let

$$\mathcal S=\{N\in\mathbb Z_{>0}:\text{some triangle has a dissection into }N\text{ congruent triangles}\}.$$

The task is a necessary-and-sufficient characterization of membership in **S for every N**. Positive membership needs just one valid tile and target. Negative membership must exclude **every** permitted tile/target family. Solving N=105, solving all primes, or solving one fixed tile does not answer that all-integer question.

A complete fixed-tile spectrum for every shape would be one sufficient route. It is **not logically necessary** to resolve every fixed-tile question separately: an alternative global characterization could exploit overlap, because a count already constructed by another tile is globally admissible. The roadmap below is an organized route, not an artificially stronger definition of the problem.

## What is already available here

| Block | Available result | What it does not decide |
|---|---|---|
| Elliptic square-class correspondences | [F3 iff positive rank and a class-number exact sector](elliptic-square-classes.md); [finite odd-F3 test on a certified full basis](f3-odd-multipliers.md); [alpha iff congruent-number rank is positive](alpha-congruent-numbers.md). | Branch existence somewhere is different from realization at a prescribed small residual multiplier. Full bases have not been computed generally. |
| Entire square class 22 | [Exact criterion](square-class-22.md) for every `22 m²`: even multipliers are positive; odd multipliers have a finite necessary-and-sufficient QP allocation test. F3 is removed by an elliptic rank-zero obstruction. | This complete class result does not classify other kernels. |
| Entire square class 78 | [Complete criterion](../research/best-move-oct7/new-arithmetic/CLASS78.md): `78m²` is admissible exactly when m is even. A new 312-tiling supplies sufficiency; an elementary modulo-13 descent excludes every odd multiplier. | No rank computation is needed, but the argument is specific to this class and does not classify all kernels. |
| Any fixed finite prime support | [Effective finite-basis theorem](fixed-prime-support.md) bounds primitive product coefficients over all support exponents, supplies an eventual divisor test, and reduces an exact basis to finitely many bounded geometric decisions. | Bounds are theoretical and depend on the support; the general unit-equation enumeration and geometric campaign have not been executed. No universal finite obstruction catalog follows. |
| Square-class tails and prime-power rays | [Finite arithmetic criteria](square-class-tails.md) decide whether all sufficiently large `d m²` occur, and whether any `d q^(2k)` occurs for fixed odd prime `q`. In the latter question only product coefficients with `q^r<2d` need checking. | A positive ray test leaves its small exponents undecided. Failure of cofinal saturation does not exclude arbitrary composite multipliers. |
| Size of the global set of counts | [Quantitative density bound](quantitative-density.md): `S(X) ≪ X / ((log X)^δ (log log X)^(3/2))`, with `δ=0.086071…`; strengthens the integrated [1 October qualitative proof](long-seams-density.md). | A counting bound does not characterize membership of the remaining sparse set, and does not supply an effective exclusion percentage at a specified finite X. |
| Classical/similar tilings | Published classifications and explicit constructions; among familiar admissible families are k², 2k², 3k², 6k² and sums of two squares. Exact source hypotheses remain necessary. | Not a proof that these are all global counts; 322 is an explicit nonclassical construction. |
| Prime counts | [Candidate deduction](prime-case-dependencies.md) from the two scale-one geometric candidates and cited classifications. | Not externally accepted or formally checked here; in any event it concerns primes, not arbitrary composites. |
| Group 1: 3alpha+2beta=pi | [All-five-shape eventual construction](universal-rational-scales.md), explicit bounds/seeds; a complete other-scalene family and a complete [fixed (2,3,4) spectrum](first-tile-classification.md). | The small admissible scales for general primitive (u,v), including the relevant W, beta, theta and alpha targets, are not classified by the eventual theorem. |
| General W and beta cap | [Explicit collars](../research/w-beta-caps/PROOF.md) construct every scale in v+<u,v>, hence every m>=uv-u+1. | This is a sufficient set, not a proved exact spectrum; for example it leaves scale 4 of tile (6,5,9) undecided. |
| General 120-degree surgery | [Smaller trapezoids](../research/group2-trapezoids/PROOF.md) and [balanced F4/F2/F3 transfers](../research/group2-trapezoids/BALANCED_F4.md), including all m>=2 when b<a and 3c>=4a. | The exact trapezoid spectrum, the primitive scale-one cases and the complementary parameter range are not settled by these sufficient results. |
| Oriented 120-degree F4, a<b | [Four-region construction](../research/group2-f4/PROOF.md) supplies every positive integer multiplier. | Reversing a and b changes the target and does not preserve this construction; the a>b branch remains unresolved in general. |
| Oriented 120-degree F3, 0<a<2b | [New a<b construction](../research/best-move-oct7/hexagon/F3_SMALL_A.md), combined with the earlier ordered gamma theorem, supplies every positive integer multiplier throughout this sector. | The remaining a>2b domain has partial constructions and tails, but no complete scale criterion. In particular 4830 remains unresolved. |
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
Thus the individual-membership problem includes square classes
with infinitely many positive and negative odd multipliers. The new
criterion correctly distinguishes these from classes with a cofinal
positive tail; it does not decide their arbitrary composite multipliers.

The later [class-22 theorem](square-class-22.md) now closes every individual
multiplier in that particular class, by excluding the last F3 branch through
an elliptic rank-zero obstruction. The [fixed-support theorem](fixed-prime-support.md)
also supplies an effective stopping bound for composite multipliers on each
chosen prime support. Neither result bounds the unrestricted collection of
prime supports or removes the other classes' geometric small-scale questions.

## 6 October: local descent and a limit of global replacement

The [local descent theorem](local-descent-obstructions.md) excludes all odd
multipliers for uniform families with unbounded kernel prime support. It
continues to apply at positive elliptic rank, so zero rank is not the only
way to remove F3 from an entire odd sector. Its finite local cover sieve is
only a necessary-condition test: surviving covers do not certify rational
points, and rational coefficient witnesses alone do not settle small scales.

The [global-overlap theorem](f3-global-overlap.md) closes a proposed escape
route negatively. There are infinitely many actual tiling counts for which
every classified realization must be F3. Consequently a solution cannot
simply discard F3 on the ground that other branches always cover its counts.
This does not prove that a particular small F3 coefficient is unrealizable.
The remaining general tasks include the surviving arithmetic classes and
the exact geometric behavior below the established constructive tails.

## 6 October: unrestricted support needs infinitely many fixed witnesses

The [class-38 theorem](infinite-minimal-multipliers.md) gives actual odd
admissible multipliers with pairwise gcd 3, although neither multiplier
1 nor 3 is admissible in that class. Consequently the class has infinitely
many minimal admissible multipliers under divisibility. Even finitely many
fixed primitive tiles, with all their residual scales allowed, cannot cover
its odd sector. This refutes a fixed finite witness list across all prime
supports. It does not refute the [fixed-support theorem](fixed-prime-support.md),
an input-dependent finite coefficient test, or a finite parameterized or
recursive construction rule.

The [seam certificate theorem](exact-seam-certificates.md) makes the remaining
geometry discrete. A true integer-sided tiling in a convex triangle has
integer atomic seams; each original-side contact component is a tree.
Leaf elimination determines all atom lengths. A compatible oriented disk
with the exact angle sums and triangular boundary is sufficient, by flat
development and degree one. The number of disk incidences is at most 4N-1,
but is unbounded as N varies. Local tree balances do not by themselves
ensure that the three sides of every tile fit into one global disk.

There is also a concrete limit to increasing the residual multiplier by
changing the tile. For N=990 and N=4830, the [F3 isolation test](f3-global-overlap.md)
applies: both counts are 14 modulo 16 and have an odd valuation at 5.
For 4830, squarefreeness forces residual scale one. Writing
U=a+2b, V=a+b gives UV=1610 and V<U<2V; the sole factor pair is (46,35),
so the sole tile is (24,11,31). For 990, the possible residual scales are
1 and 3; scale 3 would require the coefficient 110, impossible for F3.
At scale one, UV=330 has the sole admissible factor pair (22,15), giving
(8,7,13). These facts do **not** exclude either count; they show that
coefficient replacement cannot remove their primitive geometric question.

The new [nested-corner theorem](../research/group2-nested-corners/PROOF.md)
now resolves **990 positively**. Its target `(169,286,315)` has 990
congruent `(8,7,13)` tiles, checked independently by pairwise rational
geometry and by the incidence-only disk verifier. Therefore the
[entire odd sector of square class 110](square-class-110-odd.md) is now
classified: `110m²` is admissible if and only if `3|m` for odd m.
The prior 54-tile auxiliary parallelogram remains an unresolved separate
construction route; it is no longer needed for 990.

The positive theorem covers reversed F4, F2 and both F3 orientations
whenever `kc>=m(a-b)` and `mbc-a²k in <a,b,c>`. A
[uniform conductor bound and complete finite audit](../research/f3-descent-attempt/TERNARY_SEMIGROUP_TAIL.md)
give **every multiplier for every primitive tile with `1<a/b<=7/5`**.
This removes a full range of primitive geometric cases, not only 990.

The [squarefree F3 front](../research/arithmetic-continuation/SQUAREFREE_F3_FRONT.md)
contains infinitely many necessary coefficient candidates of residual
scale one, beginning with **4830, still unresolved**. Neither the positive
cone nor the large-scale arithmetic theorems decides this front.

The full problem is still unsolved here. The attempted pure-island size
bound, the diagnostic corner-quadrilateral search, and local transport
lemmas produced no general construction or impossibility theorem for this
residual geometry; they are not used as negative tiling certificates.

## 6 October: a smaller remainder and sectors with unrestricted prime support

The [global fixed-split-part theorem](../research/arithmetic-continuation/GLOBAL_FIXED_SPLIT_PART.md)
now covers all branches for even squarefree d and odd m, after fixing
the full part H of m supported at primes p>3 outside `5,19 mod24`.
Both difference-of-squares rows and three norm rows are excluded by
2-adic valuation. All eight surviving nonclassical rows have bounded
primitive parameters depending only on `dH²`; classical counts are
handled separately. The finite coefficient list and prior constructive
tails give a computable cutoff C(d,H), above which global membership is
exactly a finite divisibility test. This permits unrestricted prime
support in the complement `{3} union {p=5,19 mod24}`.

The theorem does not determine every member of the finite small remainder,
cover even multipliers, or give a common finite list as H grows. These
qualifications are essential to its compatibility with the class-38
infinite antichain and the remaining geometric cases.

The [norm-family counting argument](../research/arithmetic-continuation/NORM_GEOMETRIC_REMAINDER.md)
shows that all representations below the seven established constructive
tails number only `O(sqrt X)` up to X. This narrows the size of a set
containing the unresolved norm-family cases, but leaves infinitely many
cases and does not classify Group 1.

The [F3 split-part theorem](../research/arithmetic-continuation/F3_SPLIT_PART_REDUCTION.md)
handles another unbounded parameter. For `N=dm²`, fix the full part `h`
of `m` on primes `1,11,13,23 mod24`. The possible primitive F3 tiles then
belong to an explicit finite list independent of the number of remaining
prime factors. Beyond `m>=8dh³` (or `6dh³` for `d>=2`), an exact finite
divisibility test is sufficient as well as necessary. The theorem gives
a global answer only when other branches are independently excluded.
It excludes every odd class-38 multiplier with `h=1`, but has no uniform
finite cutoff when `h` itself grows without bound.

The [same factor argument](../research/arithmetic-continuation/OTHER_SPLIT_BRANCHES.md)
also covers I120, F2 and F4, with common sufficient cutoff `15dh³`, or
`12dh³` for `d>=2`. This extension does not classify the other norm rows
or Group 1.

The [Group-1 two-long-edge theorem](../research/group1-continuation/PROOF.md)
also supplies a universal boundary obstruction for both side orders.
It excludes W scale one when `u=1` or `u=v−1`, but does not resolve the
remaining small scales or the all-branch membership problem. The exact disk verifier closes verification
of a supplied complete gluing; it does not supply a structural description
of which complete gluings exist. Full Erdős 634 remains unresolved here.

The [54-tile core attempt](../research/f3-core-attempt/README.md) records
a concrete sufficient route to 990: filling one 60-degree parallelogram
with sides 56 and 27 by `(8,7,13)` tiles completes the established
corner transfers. No such filling or exhaustive obstruction has been
obtained. Its bounded searches are explicitly INCOMPLETE, and even an
obstruction to that core would not exclude every possible 990-tiling.

## 7 October: the exact next implication and a larger primitive domain

The [new thirteen-row gap map](global-gap-2026-10-07.md) states exactly
which scale predicates remain. In particular W and F3 each contain
infinite families of positive counts realizable in no other branch.
A complete result therefore cannot simply discard either one.

The constructive attack produced the
[ordered F3 gamma-corner theorem](../research/group2-gamma-corners/PROOF.md):
all multipliers for `b<a<=2b`, including an independently certified
264-tiling by `(5,3,7)`. The matching boundary argument classifies all
fillings of that gamma remainder using a single short-direction class.
For primitive multiplier one, that restricted construction is possible
exactly when `a<2b`. Extending it requires new direction classes or a
changed macro partition; repeating the same rectangle move cannot suffice.

The [full-signature identity](../research/f3-descent-attempt/F3_FULL_SIGNATURE_BARRIER.md)
shows why all translation-invariant edge-length inventories still pass
F3 cases such as 4830. The [Group-1 audit](../research/group1-continuation/SCALE_DESCENT_AUDIT.md)
locates the realizable `uc=va` exchange that breaks scale-one purity at
larger scales. The [width theorem](audits/seam-automata-global-width-2026-10-07.md)
excludes bounded-treewidth normalization even over alternative tilings.
A position-sensitive construction or obstruction remains necessary.
No complete classification of all N is asserted.

### The next construction closes every nonprimitive member of class 4830

The [staircase extension](../research/global-classification-continuation/GAMMA_STAIRCASE.md)
constructs ordered F3 at every m>=2 when b<a<=5b/2. In particular all
`4830m²`, m>=2, are positive; the explicit 19320-tiling has a
[complete exact coordinate check](../research/group2-mixed-gamma/README.md).
Only 4830 remains in this square class. For every positive gamma remainder
the proof also supplies an exact staircase-scale predicate and an explicit
every-integer tail. This advances sufficiency without proving necessity
of the chosen macro partition. The [updated gap map](global-gap-2026-10-07.md)
retains the unsolved W/beta converse and unrestricted cases 154 and 4830.

## 7 October: a new F3 construction and complete classification of class 78

The [next positive F3 theorem](../research/best-move-oct7/hexagon/F3_SMALL_A.md)
constructs every count `3(a+b)(a+2b)m²` for a<b and every integer m>=1.
Its five-region partition uses a c-fold tile, two b-fold tiles, a
previously filled F4(a,b) triangle, and an ideal trapezoid. The latter
has shorter base `2ab+b²`, leg `ab`, and a positive semigroup extension
`a(3b-c)` from the existing deficit seed. The
[independent audit](../research/best-move-oct7/geometry/F3_A_LT_B_AUDIT.md)
checks the dissection, side lengths, count, and applicable F4 order.

Combined with the earlier gamma theorem, the current all-multiplier
F3 domain is **0<a<2b**. This includes the whole opposite order a<b,
whose unbounded b/a ratios were not supplied by changing the names of
the short sides in the earlier construction.

At `(a,b,c)=(3,5,7)` the new theorem gives a complete 312-tile
certificate. An [elementary local descent](../research/best-move-oct7/new-arithmetic/CLASS78.md)
then proves the full square-class statement

\[
\boxed{78m^2\in\mathcal S\quad\Longleftrightarrow\quad m\text{ is even}.}
\]

Odd multipliers are excluded across all necessary branches: the
existing residue theorem isolates F3, its coefficient forces a
rational point with odd 2-adic x-valuation on
`y²=x³+156x²-2028x`, and four explicit quartic square classes are
impossible modulo 13. Even multipliers follow from the 312 seed by
subdivision. The [separate audit](../research/best-move-oct7/geometry/CLASS78_AUDIT.md)
rederives the map and all local exclusions without a rank assumption.

The positive theorem also supplies **573390** using `(136,209,301)`.
The [count audit](../research/best-move-oct7/new-arithmetic/COUNT_573390.md)
isolates F3, proves uniqueness of that primitive ordered tile at scale
one, and checks that the earlier recorded project constructions did
not already decide this count. This is a new positive decision within
the audited project ledger, not an external priority claim.

The remaining goal is still a necessary-and-sufficient rule for every
N. **154 and 4830 are unresolved here**; the latter satisfies
24/11>2 and is outside the newly completed F3 sector. Its nonprimitive
square multiples were already positive. The unfinished Group-1 and
other norm-family predicates also remain, so the new complete class
and sector theorems do not constitute a solution of all Erdős 634.
