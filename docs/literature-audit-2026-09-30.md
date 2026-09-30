# Literature and scope audit — 30 September 2026

This is a targeted comparison, not a claim of having independently re-proved every cited paper.

## Sources and consequences

- **Beeson–Zhang**, *Rationality of certain triangle tilings*, arXiv:2604.01314v1: the rationality theorem and angular classification table license integer normalization and the listed nonsimilar branches under their hypotheses. They do not decide all allowable multipliers.
- **Beeson**, *Tilings of an Isosceles Triangle*, arXiv:1206.1974v7: right-tile restrictions, double-angle necessary conditions, and the existing finite-search perspective. Decidability for each input N is not being presented as a new structural classification.
- **Zhang**, *Tiling Triangles with 2pi/3 Angles*, arXiv:2512.22696v4: trapezoid constructions and transfers supply sufficient large-scale existence. A sufficient cutoff must not be silently treated as necessary.
- **Harries**, *New constructions, obstructions, and multiplier structure for Erdős Problem 634*, v0.5, 28 August 2026: inspected source `progress634/progress634.tex`, blob `85536aabe013ad393e33985cbfcadbae50722f08`, including the introduction/import ledger, Laurent argument, trapezoid refinement, and multiplier-addition/generator-window results. It already proves the equilateral divisibility ab|S, including the 60-degree extension, and contains R=ceil(a/b)+ceil(b/a), the tail m>=3R, and the same (32,45,67), m=9, N=116640 example. These are explicitly credited in [our addendum](../research/general-spectra/ATTRIBUTION.md). The manuscript also distinguishes certified refutations, one-implementation exhaustion, and conditional forcing. Its fixed-ray finite generator windows do not bound the union over infinitely many tiles.
- **Bonfioli**, `ElVec1o/erdos_634_proof`: the current detailed open-case discussion leaves the attachment of the base-beta forcing scheme to arbitrary tilings unresolved. Broad historical summary claims in the README must not override that explicit dependency. Our prime manuscript remains a candidate, not certified by the other modules.

Relevant primary sources: [Beeson–Zhang](https://arxiv.org/abs/2604.01314v1), [Beeson isosceles](https://arxiv.org/abs/1206.1974v7), [Zhang](https://arxiv.org/abs/2512.22696v4), [Harries source](https://github.com/jphme/math-problems/blob/main/progress634/progress634.tex), [Bonfioli status](https://github.com/ElVec1o/erdos_634_proof).

## Consequence for this repository

The complete N=105 package, necessary spectra, eventual constructions, and squarefree congruence obstructions remain separate claims with their own proof boundaries. This audit supplies **no new full solution**. The N=154 instance (8,7,13) on (91,91,154) remains INCOMPLETE in the included search record.

To finish the structural problem one still needs an exhaustive answer for the surviving small multipliers over all primitive tiles, or a different argument classifying the union of realizable count sets without solving every fixed-tile problem. No finite global exception list has been established here. More length-linear translation-invariant boundary weights alone cannot close the scale-one W/beta instances: the included uniform-reduction note gives formal correct-count boundary witnesses, not geometric tilings.

Historical source hashes refer to the original recovered entries before editorial attribution updates. They are not the current integrity manifest. The current file inventory is `verification/manifest.json` and is checked without rebuilding it during verification.
