# Erdős Problem 634 — congruent triangle tilings

**Denis Paliy** · Research with ChatGPT assistance

[Status](STATUS.md) · [Reproduce](REPRODUCIBILITY.md) · [Open questions](docs/open-frontier.md) · [Citation](CITATION.cff)

Erdős problem 634 asks which positive integers N allow some triangle to be dissected into N congruent triangles. Reflections and T-junctions are permitted.

**This repository does not claim a complete solution of Problem 634.** Written proofs, candidate arguments and finite computational certificates have different verification scopes; see the [claim ledger](STATUS.md).

## Research currently published here

| Result | Material and scope |
|---|---|
| Prime-count classification candidate | [Manuscript](paper/prime-case-candidate.pdf) and [dependencies](docs/prime-case-dependencies.md). The universal geometric arguments require independent review. |
| Exact constructions, including 322 tiles | [Two-piece construction](docs/two-piece-construction.md), [PDF](paper/two-piece-construction.pdf), and [coordinate certificate](data/tiling-322.json). |
| All five rational target shapes at sufficiently large scales | [Two-annulus construction](docs/universal-rational-scales.md) and [explicit seeds](docs/explicit-theta-seeds.md). Small scales are not classified in general. |
| Complete fixed-tile analysis for (2,3,4) | [All target shapes for this tile](docs/first-tile-classification.md). This is not a classification over every possible tile. |
| Global exclusion of 21 | [Reduction](docs/n21-global-reduction.md) and separately replayed finite certificate. Prior work is credited. |
| Historical N=105 investigation | [Partial results](docs/n105-partial-results.md). These committed files are partial; the later complete N=105 package prepared separately has not yet been incorporated into this branch. |

## Verification

Python 3.10 or newer; the finite checks use the standard library:

```bash
python3 scripts/reproduce.py
```

Do not use `-O`, `-OO`, or `PYTHONOPTIMIZE`. A successful replay checks the supplied finite evidence, not every universal theorem or the full problem. Read [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for the exact boundary.

## Authorship and reuse

Denis Paliy directed the investigation. ChatGPT assisted with proof exploration, drafting, programming and checks; see [AI_USAGE_DISCLOSURE.md](AI_USAGE_DISCLOSURE.md). No external referee acceptance, proof-assistant verification of the whole project, or research priority is claimed.

Original software: [MIT](LICENSE). Original documentation and figures: [CC BY 4.0](LICENSE-DOCUMENTATION.md). Third-party work retains its own rights. [Corrections and independent review](CONTRIBUTING.md) are welcome.
