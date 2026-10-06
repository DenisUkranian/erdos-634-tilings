# Erdős Problem 634 — congruent triangle tilings

**Denis Paliy** · Research with ChatGPT assistance · 3 October 2026

[Status](STATUS.md) · [Reproduce](REPRODUCIBILITY.md) · [Full-problem roadmap](docs/full-solution-roadmap.md) · [Citation](CITATION.cff)

Which positive integers N allow a triangle to be dissected into N congruent triangles? Reflections and arbitrary T-junctions are allowed.

**This repository contains partial research results, not a complete solution of Erdős problem 634.** The N=105 argument combines written geometric lemmas, published classification inputs, and separately replayed exact certificates. Universal arguments are not formally certified by running the code; the all-primes manuscript remains a candidate.

## Results and complete materials

| Result | Read and reproduce |
|---|---|
| Finite criteria for square-class tails and odd-prime-power rays (6 October) | [Theorems and full proof](docs/square-class-tails.md), [exact arithmetic tool and independent checks](research/square-class-tails/): decide whether every sufficiently large `d m²` is admissible, and whether any `d q^(2k)` is admissible for a fixed odd prime `q`. A negative ray test excludes all exponents; a positive test supplies a sufficient tail. Individual small multipliers remain separate. The proof also excludes every `22 q^(2k)` with odd prime `q`, while retaining the previously known positive composite-multiplier witness in square class 22. |
| Quantitative bound for **all** admissible counts (6 October) | [Complete deduction and dependencies](docs/quantitative-density.md): `S(X) ≪ X / ((log X)^δ (log log X)^(3/2))`, where `δ=0.086071…`. Integrates the [1 October long-seam and zero-density proof](docs/long-seams-density.md), freshly audited, and strengthens it using Ford's uniform divisor estimate. This is a bound on how many counts occur, not an exact membership criterion. |
| A nonexchangeable extreme pure island inside an equilateral triangle (6 October) | [Proof](docs/extreme-pure-island-in-triangle.md), [hierarchical exact certificate](research/extreme-pure-embedding/): the counterexample below persists as the unique maximal `+1` component while every exterior edge has level `-1` or `0`. Triangular boundary alone cannot justify opposite pure exchanges. Mixed or global replacements remain possible; the entire example has another low-level tiling. |
| Universal nonconvex pure-island exchange is false (6 October) | [Counterexample and proof](docs/nonconvex-chirality-counterexample.md), [all unit coordinates and exact checks](research/nonconvex-chirality/): a simple `(3,5,7)` pure island has 1862 tiles, while its boundary forces the impossible opposite population `(930,-30,962)`. This closes the proposed general pure-switch route negatively; it does not solve Erdős 634. |
| Nonconvex pure regions: phase decomposition and `2c²` count divisibility (6 October) | [Proof](docs/nonconvex-pure-island-reduction.md): group by short-lattice cosets to obtain whole long-edge boundaries, including holes. Every group and the whole region have tile count divisible by `2c²`; disks also admit straight whole-tile crosscuts. General nonconvex exchange is false, as shown in the counterexample above. The same note shows that the convex exchange move is absent throughout the remaining small equilateral interval. |
| Complete convex pure-island criterion and same-polygon chirality exchange (5 October) | [Proof](docs/convex-pure-island-classification.md), [exact checks](research/pure-convex-islands/): for every primitive integral 120° tile, a convex all-long-direction polygon is pure-tileable exactly when centrally symmetric with every side a multiple of `abc`. First-derivative invariants prove necessity; a universal stepped-surface construction proves sufficiency. Nonconvex and mixed-state islands remain outside this theorem. |
| General 120° trapezoids and balanced scalene branches | [Positive surgery](research/group2-trapezoids/PROOF.md) improves the sufficient equilateral tail to `m>=3 ceil(c/min(a,b))`. [Corner transfers](research/group2-trapezoids/BALANCED_F4.md) construct F4, F2 and F3 for every `m>=2` when `b<a` and `3c>=4a`; primitive scale one is not settled by this theorem. |
| W and beta constructions at every scale in `v+<u,v>` | [Six-block cap proof](research/w-beta-caps/PROOF.md), [exact certificates and separate checker](research/w-beta-caps/): for every primitive `0<u<v`, all scales `m>=uv-u+1` are realized. This improves the sufficient bound; it does not exclude scales outside the displayed semigroup. |
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

Use ordinary Python, without `-O`, `-OO`, or `PYTHONOPTIMIZE`. The coordinator checks integrity and local links, replays the legacy suite and all four N=105 certificates, expands the 116,640-tile construction, and runs the uniform-reduction, uniform-sectors, square-class-saturation, W/beta-cap, F4, trapezoid, attempted-width-bound and c-relation tests in temporary copies. Reports record the scope of each check. See [REPRODUCIBILITY.md](REPRODUCIBILITY.md).

## Remaining question and attribution

A finite exception interval for each fixed tile is not a finite exception list over infinitely many tiles. Neither the necessary arithmetic spectra nor the existing finite membership search supplies the requested structural classification of all N. The [3 October audit](docs/audits/research-2026-10-03.md) reconciles the later archive; the [continuation record](docs/audits/full-solution-attempt-2026-10-03.md) identifies the new constructions, failed general reductions and the still-missing implications. See the [roadmap](docs/full-solution-roadmap.md).

Denis Paliy directed the investigation; ChatGPT assisted with derivations, drafting and code. [Assistance disclosure](AI_USAGE_DISCLOSURE.md). No external referee acceptance, proof-assistant verification of the whole project, or priority is claimed. [Corrections](CONTRIBUTING.md) are welcome.

Software: [MIT](LICENSE). Original documentation and figures: [CC BY 4.0](LICENSE-DOCUMENTATION.md). Cited third-party work retains its own rights.
