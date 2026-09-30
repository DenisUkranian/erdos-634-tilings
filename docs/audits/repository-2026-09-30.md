# Publication audit — 30 September 2026

**Repository:** DenisUkranian/erdos-634-tilings. **Publication version:** 0.2.0.

## Coverage and provenance

The audit began from main commit `f1a5f7a861e06f00731ad5d2b6ab6bf0b2dbad84`. A preparatory branch added a file-inventory workflow at `af03bbd8e489d9e81e7299b940eea3e350e6b0da`. Its [GitHub Actions run](https://github.com/DenisUkranian/erdos-634-tilings/actions/runs/36699854537) successfully inspected all 121 tracked files, parsed all JSON, compiled Python sources, and reran the existing finite suite.

The original final N105 and general-spectra packages were read in full. The N105 four-certificate suite was replayed afresh locally, with complete root counts 120,15,1788,120. The general-spectra checker expanded all 116640 tiles and matched the recorded uncompressed-coordinate hash; the formula/mutation tests passed. The c-relations arithmetic is also included in the full coordinator.

The exact input archive names, lengths and SHA-256 digests are recorded in [import-provenance.json](../../verification/import-provenance.json). Published certificates are plain JSON. A lossless staging encoding may be used during transport; reconstruction must match the frozen original bytes before publication. The mathematical checker does not rely on the transport codec.

## What was corrected

| Finding | Publication correction |
|---|---|
| GitHub's About description named the unrelated circle problem 506 | Confirmed in the GitHub repository metadata. The intended description is in [.github/ABOUT.txt](../../.github/ABOUT.txt). File edits do not change the administrative Description field. The available connector has metadata read but no administration-write action; this item requires a repository-owner About edit and must not be marked fixed merely because README changed. |
| Current pages still described N105 as unresolved | README in both languages, STATUS, the open frontier and reproduction instructions now point to the complete four-instance global proof. Earlier limited notes have explicit historical banners. |
| An additional general-spectra package was not published | Added proof, editable source, construction certificate, checker, expanded coordinates and attribution. |
| The N105 classical-case paragraph omitted twice-a-square counts | Added this even rational-angle family to both Markdown and the PDF source. It cannot affect the odd count 105. Certificate bytes and decisions are unchanged. |
| Historical baseline still reported a partial fourth N105 target | Added a banner distinguishing the baseline lemmas from the current complete proof. No incomplete branch is repackaged as an exclusion. |
| Reports from different partial stages could be mistaken for current coverage | The full coordinator validates the four final certificates and their complete root coverage; old partial counts are explicitly historical. |
| Old short-chain arithmetic regression relied on assertions | Added an explicit refusal of optimized Python. The complete coordinator also refuses -O/-OO/PYTHONOPTIMIZE. |
| Documentation lacked a single all-suite entry point | Added scripts/verify_all.py, isolated mutable replays, integrity/link/syntax/scope checks, and expanded CI evidence. |

## What “checked” means here

Every tracked file is inventoried. Python and JSON syntax are checked. Relative Markdown link targets are checked; rendered heading anchors that cannot be reproduced safely are reported separately. SHA-256 manifests bind the actual source, data and publication files. Every bundled finite verification suite is run, including prior constructions and collar regressions, not only the latest result.

The separate N105 verifier rebuilds initial configurations and fan branches and uses a different geometric intersection implementation from the search. The general-spectra construction checks macroregion disjointness and standard internal subdivisions, plus every expanded tile's shape/containment; it does not run an unperformed O(N²) pair test over 116640 tiles.

This does **not** mean every universal mathematical proof has been formalized, every external paper re-proved, or the literature searched exhaustively for priority. The published-input reduction, boundary lemmas, annular constructions, and prime-case candidate retain their stated human-review boundaries. Successful finite CI must not be described as a solution of the all-integer problem.

## Source and metadata checks

The live Beeson–Zhang rationality paper, Table 1 and Theorems 1.1–1.2, and Zhang's version-4 construction/cutoff context were consulted for the [roadmap](../full-solution-roadmap.md). Some source URLs can reject automated access or have stale search snippets; HTTP errors and cached status labels are not a proof that a theorem is absent or established. External-link checks are diagnostic and distinguish definite not-found responses from blocked/rate-limited/network results.

The existing review issue contains only project-authored requests/updates at the time of this audit. No external referee acceptance is inferred from that issue or from private communications. No private email body is published.

## Remaining mathematics

The single global count 105 is excluded by the project proof. The prime classification remains a candidate. Necessary spectra and sufficient large-scale bounds do not classify small scales uniformly over infinitely many primitive tiles. The [full-solution roadmap](../full-solution-roadmap.md) identifies these missing implications without treating external review as a substitute for them.
