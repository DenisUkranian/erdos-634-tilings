# Literature and dependency audit, 7 October 2026

## Outcome and scope

This audit searched the two available web indexes, read current arXiv records and relevant full-text passages, and fetched the current source manuscripts of Harries and Bonfioli through the GitHub connector. It also inspected other public repositories returned by a GitHub search for `erdos 634`. No source inspected supplies a valid missing global small-scale theorem, a construction of 4830, or a complete decision of 154. This is a report of the search, not a proof that no such source exists.

Erdős 634 allows similar as well as nonsimilar tiles; congruence is among the small triangles. The additional hypotheses excluding reptilings occur in branch theorems and must not be transferred to the definition of the whole problem.

## Sources of record

| Source inspected | Version or exact identity | What can be used here |
| --- | --- | --- |
| [Harries, *New constructions, obstructions, and multiplier structure for Erdős Problem 634*](https://github.com/jphme/math-problems/blob/main/progress634/progress634.tex) | v0.5, 28 August 2026; current TeX blob `85536aabe013ad393e33985cbfcadbae50722f08`, unchanged from the previous audit | Laurent quotient, constructive transfers, multiplier addition and finite windows, subject to their stated hypotheses and evidence classes. |
| [Zhang, *Tiling Triangles with 2π/3 Angles*](https://arxiv.org/abs/2512.22696v4) | v4, arXiv revision 4 April 2026; [full PDF](https://arxiv.org/pdf/2512.22696) inspected | Explicit sufficient constructions and transfers. Conjectural sharpness is not a necessity theorem. |
| [Beeson–Zhang, *Rationality of certain triangle tilings*](https://arxiv.org/abs/2604.01314v1) | v1, 1 April 2026 | Integer normalization under the nonsimilar, nonright, incommensurable-angle hypotheses. |
| [Beeson–Laczkovich–Zhang, *Solution of Erdős Problem 633*](https://arxiv.org/html/2604.03609v3) | v3, 25 August 2026 | Classification of target shapes admitting some nonsquare tiling; this is a different quantifier from prescribing N. See the dependency caveat below. |
| [Beeson, *Triangle Tiling: The case 3α+2β=π*](https://arxiv.org/abs/1206.2229v4) | v4, 25 September 2026 | Corrected rationality, necessary equations, and sufficient constructions; expressly leaves W and base-β prime exclusions open. |
| [Beeson, *Tilings of an Isosceles Triangle*](https://arxiv.org/abs/1206.1974v7) | v7, 4 May 2026 | Relevant shape restrictions and necessary conditions; not an exact all-scale construction theorem. |
| [Bonfioli repository](https://github.com/ElVec1o/erdos_634_proof) | main `4bb61193bafa4471f7ba3a35324ae0f70bd2177c`; paper blob `b7a471881297a7cb0e44dc80ae3f65df60e8e076` | Necessary spectra and local results need their own proofs; the repository explicitly records the remaining geometric attachment hypothesis. |

## Three important traps in importing the literature

### 1. A current all-primes abstract does not repair a retracted dependency

[arXiv:2607.23453v1](https://arxiv.org/html/2607.23453v1), dated 26 July 2026, still displays the full prime classification. Its Theorem 3 and Table 1 use older Group-1 no-prime theorems. The later [1206.2229v4 record](https://arxiv.org/abs/1206.2229v4) explicitly retracts the required assertions for W and the isosceles base-β target, together with necessity of K dividing M². Consequently the July argument cannot be imported as an unconditional repair of these branches merely because its abstract remains online.

Separately, [arXiv:2607.19572v2](https://arxiv.org/abs/2607.19572v2), *No Prime Tiling of an Isosceles Triangle*, was withdrawn on 24 September 2026 because Lemma 9 was incorrect as stated. The withdrawal note mentions Bonfioli; that mention must not replace checking the exact scope and dependency chain of his current proof.

The same issue appears in an ancillary remark of the 633 paper. Immediately after Proposition 29, its v3 derives a claimed exact W multiplier spectrum from necessity of K dividing M². That particular minimal-scale argument predates the September correction and cannot be used here. This observation does **not** refute the main 633 shape classification: existence of some tiling and the square class can be justified without that exact minimum.

### 2. Formal verification can start after the unresolved geometric reduction

Bonfioli's current README contains an older full-prime headline, but its detailed “What is open” section expressly says the base-β exclusion is unproved. The remaining hypothesis asserts a geometric wall configuration in every hypothetical tiling. Local Lean theorems about a supplied wall do not prove that every tiling supplies it. The written paper also lists 154 among the small sporadic members not settled by its known conditions.

The additional repository [Robertboy18/erdos-634-lean](https://github.com/Robertboy18/erdos-634-lean) makes its boundary explicit in [TrustBoundary.lean](https://github.com/Robertboy18/erdos-634-lean/blob/main/Erdos634/TrustBoundary.lean), inspected blob `9100d99a8536983765531ea94cfb46167bb34fb6`. Its `prime_admissible_iff` takes `PublishedTilingResults` as a parameter. A field named `prime_exhaustive_reduction` removes all but commensurable and 120-degree branches; that field is assumed rather than proved there. Such a conditional theorem supplies no independent W/base-β exclusion.

[David Turturean's manuscript](https://github.com/davidturturean/erdos-634/blob/main/main.tex), inspected blob `6a831ecd13cbc83fedccddaeda8f9f82b718fa3a`, likewise removes the triquadratic branch using the old Beeson III Theorem 21. Its headline prime classification therefore does not bypass the corrected Group-1 gap.

### 3. Zhang's “105 and 120” are side lengths, not tile counts

In Section 3.1 of Zhang v4, X denotes an equilateral side length for tile (3,5,7), with N=X²/15. The two mentioned unresolved values are X=105 and X=120, corresponding to N=735 and N=960. A secondary search result incorrectly described them as tile counts 105 and 120. Our global N=105 exclusion must not be presented as settling Zhang's two stated instances.

Also, the symbol y in Zhang's trapezoid discussion is inconsistent between the initial definition and the constructions: the constructions use the leg length. Harries explicitly warns of this and restates the geometry. All transfers here use the geometric lengths, not an unexamined symbol substitution.

## What the constructive synthesis actually yields

Harries proves multiplier addition for a fixed triangle shape and a fixed tile when a suitable corner has integral side ratios. All six Group-2 target rows satisfy his corner hypotheses. Combining addition with an eventual construction yields a numerical semigroup and a finite generator window for **that ordered tile and target**. It does not turn the union over infinitely many tiles in one square class into a finite list of seeds.

For example, write U=a+2b and V=2a+b. Zhang's Proposition 11 attaches a tiled macrotriangle to the F2 target

\[
(aU,bV,c^2)
\]

and obtains ordered F3

\[
(c^2,cU,3b(a+b)).
\]

The arithmetic count identity is

\[
3(a+b)U-UV=U^2.
\]

For (a,b,c)=(24,11,31), this would construct 4830 from an F2 tiling with 2714 tiles plus a 46²-tile triangular grid. This is a valid reduction, but neither inspected source gives the required F2 tiling at multiplier one. Replacing the F3 problem with this F2 problem is not closure.

The new local project constructions go substantially below the older sufficient tails: ordered F3 is now constructed for 0<a<2b at scale one, and for b<a≤5b/2 at every scale m≥2. The inspected general literature does not fill the remaining scale-one case (24,11,31). This comparison is not an external priority or refereeing claim.

## Blind spots that remain after combining sources

| Proposed shortcut | Exact missing implication |
| --- | --- |
| Use the solution of 633 | Some nonsquare N for each admissible shape does not prescribe the desired N. |
| Use all necessary branch spectra | Arithmetic admissibility does not supply a disjoint placement. |
| Use Harries's generator window | It is finite after the tile is fixed; the family of relevant primitive tiles can remain infinite. |
| Use signed/Laurent invariants | Their exact ideal-membership consequences omit edge positions and global embedding. |
| Use local wall or seam proofs | A hypothetical arbitrary tiling must first be shown to contain their configuration. |
| Use a verified complete disk | Verification of a supplied disk does not prove existence of a disk for every candidate. |
| Use positive macro subtraction | A tiled large region and a tiled subregion do not imply their set-theoretic difference inherits a tiling. |

The focused literature search therefore strengthens the dependency map and prevents several false completions, but does not close all N. The remaining geometric work still needs a uniform existence/obstruction theorem for small scales, or a different characterization of the union of counts that bypasses those scales.

## Search limitations

The problem website's indexed text still lists 634 as open, but its crawl is older than several manuscripts. A direct current forum fetch returned HTTP 403, so the audit does not claim to have read every present forum comment. GitHub source retrieval and arXiv version records supplied the current primary evidence above. No messages, issues, or comments were sent to other authors.
