# Erdős Problem 634 — congruent triangle tilings

**Denis Paliy** · Research with ChatGPT assistance · 3 October 2026

[Status](STATUS.md) · [Reproduce](REPRODUCIBILITY.md) · [Full-problem roadmap](docs/full-solution-roadmap.md) · [Citation](CITATION.cff)

Which positive integers N allow a triangle to be dissected into N congruent triangles? Reflections and arbitrary T-junctions are allowed.

**This repository contains partial research results, not a complete solution of Erdős problem 634.** The N=105 argument combines written geometric lemmas, published classification inputs, and separately replayed exact certificates. Universal arguments are not formally certified by running the code; the all-primes manuscript remains a candidate.

## Results and complete materials

| Result | Read and reproduce |
|---|---|
| Every multiplier in the oriented 120° F4 branch with a<b | [Four-region proof](research/group2-f4/PROOF.md), [unit generator and independent checker](research/group2-f4/): `(2a+b)(a+b)m²` is constructed for every positive m when `c²=a²+ab+b²` and `a<b`. The reversed orientation remains unresolved in general. |
| Exact criterion on an infinite arithmetic domain | [Uniform sectors proof](research/uniform-sectors/PROOF.md): for N≡6 (mod16), 3∤N, and no p≡7 (mod8) with odd exponent, admissibility is exactly the constructive QP form. [Code and certificates](research/uniform-sectors/). |
| Constructive tails in compatible square classes | [Square-class saturation proof](research/square-class-saturation/PROOF.md), [generator and separate verifier](research/square-class-saturation/): a fixed W/beta tile realizes every sufficiently large multiplier, with an explicit bound below 2d. Small multipliers remain unclassified in general. |
| Global exclusion of N=105 | [Written proof](research/n105/PROOF_N105.md), [PDF](research/n105/PROOF_N105.pdf), [four certificates and checking programs](research/n105/), [report](research/n105/VERIFIED_RESULTS.json). Covers both equilateral and both scalene candidates. |
| General scale restrictions and constructive bounds | [Proof](research/general-spectra/PROOF.md), [PDF](research/general-spectra/paper.pdf), [code and data](research/general-spectra/). Small multipliers remain unclassified in general. |
| Exact construction with 116,640 tiles | Tile (45,32,67), equilateral side 12,960: [macrocertificate](research/general-spectra/construction_116640.json), [all coordinates](research/general-spectra/tiles_116640.jsonl.gz), [checker](research/general-spectra/verify_certificate.py). |
| Squarefree obstructions and finite candidate reduction | [Proof](research/uniform-reduction/PROOF.md), [PDF](research/uniform-reduction/paper.pdf), [full supplementary package](research/uniform-reduction/). Includes the double-angle scale restriction and limits of linear boundary signatures. N=154 remains incomplete. |
| All-prime classification candidate | [Manuscript](paper/prime-case-candidate.pdf), [dependencies](docs/prime-case-dependencies.md), [c-relation audit](research/c-relations/audit.md). Universal geometric forcing still requires scrutiny. |
| Construction with 322 tiles and an infinite family | [Two-piece construction](docs/two-piece-construction.md), [PDF](paper/two-piece-construction.pdf), [certificate](data/tiling-322.json). |
| All five rational shapes at sufficiently large scales | [Two-annulus theorem](docs/universal-rational-scales.md) and [explicit seeds](docs/explicit-theta-seeds.md). Bounds depend on the fixed tile. |
| Complete fixed-tile analysis for (2,3,4) | [Classification](docs/first-tile-classification.md), including the [75-tile construction](docs/theta-75-construction.md). Prior results are credited. |
| Global exclusion of 21 | [Reduction](docs/n21-global-reduction.md) and [391-state certificate argument](docs/alpha-21-obstruction.md). Independently reproduces previously reported work. |

The N=105 root coverage is 120/120 for each scalene target, 15/15 for tile (5,19,21), and 1,788/1,788 for tile (7,13,15). Historical partial collars remain as regression fixtures, not as substitutes for these complete finite proofs.

The equilateral divisibility conclusion, the 120-degree cutoff refinement, and the (45,32,67), m=9 example are prior results in Harries's August 2026 manuscript, rederived and independently implemented here. Read the [attribution addendum](research/general-spectra/ATTRIBUTION.md) and [literature audit](docs/literature-audit-2026-09-30.md).

## Verification

Python 3.11 or newer; the finite tests use the standard library:

```bash
python scripts/verify_all.py --jobs 2
```

Use ordinary Python, without `-O`, `-OO`, or `PYTHONOPTIMIZE`. The coordinator checks integrity and local links, replays the legacy suite and all four N=105 certificates, expands the 116,640-tile construction, and runs the uniform-reduction, uniform-sectors, square-class-saturation, F4 and c-relation tests in temporary copies. Reports record the scope of each check. See [REPRODUCIBILITY.md](REPRODUCIBILITY.md).

## Remaining question and attribution

A finite exception interval for each fixed tile is not a finite exception list over infinitely many tiles. Neither the necessary arithmetic spectra nor the existing finite membership search supplies the requested structural classification of all N. The [3 October audit](docs/audits/research-2026-10-03.md) reconciles the later archive, records the fresh replays and distinguishes unresolved global strategies from the prime-case candidate. See the [roadmap](docs/full-solution-roadmap.md).

Denis Paliy directed the investigation; ChatGPT assisted with derivations, drafting and code. [Assistance disclosure](AI_USAGE_DISCLOSURE.md). No external referee acceptance, proof-assistant verification of the whole project, or priority is claimed. [Corrections](CONTRIBUTING.md) are welcome.

Software: [MIT](LICENSE). Original documentation and figures: [CC BY 4.0](LICENSE-DOCUMENTATION.md). Cited third-party work retains its own rights.
