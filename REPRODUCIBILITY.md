# Reproducibility and verification boundary

**v0.3.0 — 3 October 2026**

## Entire published suite

Python 3.11 or later; verification uses the standard library. Do not use `-O`, `-OO`, or `PYTHONOPTIMIZE`: some preserved legacy checks rely on assertions, and the coordinator explicitly rejects optimized execution.

```bash
python scripts/verify_all.py --jobs 2
```

The coordinator checks the file manifest, syntax, local links and scope flags, then runs every finite suite in disposable copies. Original certificates and frozen reports are not overwritten. A fresh report is written to `audit-output/full-replay.json`, which is ignored by Git. Runtime depends on hardware; the exact rational N105 checks can take several minutes. A process timeout is a failure to finish, never a mathematical exclusion.

## Suites and their scope

| Command, from repository root unless noted | What is checked |
|---|---|
| `python research/infinite-minimal/verify_orbit.py` | Exact finite orbit, two curve group laws, dual square lift, primitive coefficient normalization, local valuations and the small class-38 exclusions. Infinitely many actual minimal multipliers follow from the written local-group, real-density and prior constructive-tail proof, not from this finite sample. |
| `python research/seam-certificates/verify_seams.py` | Original-side contact trees and exact integer atom reconstruction in the retained 322-tiling. This checks the certificate method on one example; it does not enumerate all disks or settle an unresolved count. |
| `python research/local-descent/run_checks.py` | All signed even descent covers for each certificate; both projective charts in modular obstructions; true odd-F3 and even/positive-rank controls; family input and scope restrictions. The universal prime-family deductions require the written proof. Surviving local covers are never a positive global decision. |
| `python research/elliptic-sectors/run_checks.py` and `python research/elliptic-sectors/check_alpha_maps.py` | Complete reduced-form comparisons, exact elliptic maps, primitive F3 round trips, QP allocation versus forward enumeration, alpha candidates including factors of 3, scope controls, and universal alpha rational-function identities. No general rank algorithm or Mordell–Weil basis computation. |
| `python research/composite-support/run_checks.py` | Nine quartic identities/discriminants; allocation versus independent forward coefficient enumeration through 5000; scoped general-tool statuses; exact class-22 interfaces; rank-zero central-value certificate; fresh replay of the old 88-tile certificate. It does not execute a general S-unit solver. |
| `cd research/group2-trapezoids && python check_family.py` | 420 primitive ordered seed triples, 64 balanced corner instances, exact macro certificates, two fully expanded small seeds and five corruption rejections. |
| `cd research/group2-trapezoids && python check_balanced_f4.py` | Complete 1380- and 3105-tile F4 examples; all unit pairs, a nonprimitive normalization case and four corrupted certificates. |
| `cd research/group2-trapezoids && python check_free_k.py` | Free-parameter corner construction, arithmetic criterion and full unit examples outside the original scaled-shave domain. The criterion concerns this construction only. |
| `cd research/group2-trapezoids && python check_target_bridges.py` | F2/F3 target transfers for 70 primitive triples at two scales; scale-one tests verify only the macro partition, not tileability. |
| `cd research/group2-trapezoids && python verify_f2.py certificates/f2_balanced_8_7_13_m2.json` | Exact congruence, containment, coverage and all 2,047,276 pairs of the 2024-tile F2 example. |
| `cd research/attempt-obstructions && python check_corner_chord.py` | Five congruent corner tiles, disjointness, exact complement, chord avoidance and a certified square-root inequality. This is a partial configuration refuting a proposed scalar bound, not a full tiling. |
| `cd research/w-beta-caps && python run_checks.py --output fresh.json` | 48 exact symbolic identities; 45 caps, 90 collars, 112 full targets; 34,959 macro pairs; 300 expanded unit triangles and 10,908 unit pairs; arithmetic scale checks and rejected corruptions. The universal construction and its quantifiers are proved in the accompanying text. |
| `cd research/group2-f4 && python run_checks.py --output fresh.json` | 80 primitive macro instances; complete 88-, 352- and 546-tile certificates with all-pairs exact geometry; six corrupted/out-of-scope cases rejected. The general construction requires the symbolic proof. |
| `python scripts/check_repository.py` | Every included file, SHA-256 manifest, Python/JSON syntax, local link targets, scope sentinels and expanded coordinate-stream hash. |
| `python scripts/reproduce.py` | Preserved 77/322/897 and theta constructions; all old N105 collar/fan regressions; scale bridges, annuli/seeds, N21 reduction and certificate, and verifier rejection tests. This legacy runner alone is not the complete current suite. |
| `cd research/n105 && python verify_all.py --jobs 2` | Four complete fixed-instance certificates, arithmetic reduction, capped-chain and mutation regressions. The global theorem also needs the manuscript's published and geometric inputs. |
| `cd research/general-spectra && python verify_certificate.py construction_116640.json --expand` | 36 macroregions, 630 macroregion intersections and the shape/containment of all 116640 expanded triangles. Internal disjointness uses explicit standard subdivisions. |
| `cd research/general-spectra && python check_general_formulas.py` | Supplementary parameter/scale checks, 52 macro-constructions and seven rejected mutations; not an extrapolated universal proof. |
| `cd research/uniform-sectors && python run_checks.py --output fresh.json` | Modular restrictions, independent arithmetic enumeration, 554 macrocertificates, complete 2006-tile pair checks and rejected corruptions. The infinite theorem also requires the written proof and its stated classification inputs. |
| `cd research/square-class-saturation && python run_checks.py --output fresh.json` | Norm/cone criteria, exact strip cutoffs, constructive plans and 193 full macrocertificates, including corrupt-certificate rejection. No general small-scale sufficiency is inferred. |
| `cd research/c-relations && python check_relations.py --max-v 40` | Exhaustive finite integer-chain regression against the written parameterization; not the geometric prime induction. |

The first command is read-only except an optional requested report. The individual historical programs may update local reports; use the coordinator to isolate such writes.

## Root coverage, not a timeout or a search count

The N105 checkers independently regenerate root geometry and compare identities, not only a supplied number. The final root totals are 120,15,1788,120 for tiles (7,8,13), (5,19,21), (7,13,15), (5,16,19), respectively. The fourth original certificate stores 22552 states. A checker can validly visit fewer stored nodes if its own sound necessary conditions reject earlier; complete root/fan coverage and checked terminal conditions are decisive. `INCOMPLETE` never means refuted.

The historical false rule that marked an interior tile merely touching the exterior with its obtuse vertex is not used. A marked external junction must be supported by a tile with a whole edge on that same external side. The positive T-junction regression checks that distinction and the endpoint conditions of the new chain rule.

## Frozen hashes and mutable output

`verification/manifest.json` binds source, data and published document bytes. `scripts/build_manifest.py` deliberately rebuilds this ledger for a new publication; it is **not** a mathematical test. Do not regenerate hashes merely to make a failed integrity check disappear. `verification/replay.json` is a legacy mutable output excluded from that manifest; the coordinator produces fresh reports under `audit-output/` instead.

Each imported research package retains a `SHA256SUMS.txt`. For this publication the package manifests are synchronized with the explicitly documented editorial changes. Original ZIP digests are in [import-provenance.json](verification/import-provenance.json). The expanded gzip coordinate file is bound both as a file and by its uncompressed stream digest, since gzip timestamps alone can change compressed bytes.

The 6 October seam-certificate continuation corrects one explanatory sentence
in `research/uniform-sectors/PROOF.md`: atomic seams of the full convex
integer-sided tiling are integral, although additive cancellation does not
require that fact. Its package hash is updated for this explicit correction;
the sector theorem and its algorithms are unchanged. The two new finite
audits above are included in the coordinator; their infinite mathematical
claims still depend on the separately stated written proofs.

## Abstract disk certificates (6 October 2026)

The [new checker](research/disk-certificates/) reconstructs the retained
322-face tiling from incidence alone and certifies nonoverlap using the
[written degree-one argument](docs/audits/disk-realization-2026-10-06.md).
Unlike the earlier seam replay, it requires no coordinate certificate as
an input or geometric validation dependency. Its independent exporter
provides provenance for the retained combinatorial example.

```sh
python research/disk-certificates/verify_disk.py research/disk-certificates/disk-322.json
python research/disk-certificates/test_disk.py
```

The latter is integrated in the full coordinator. Four positive and thirteen
adversarial inputs are retained, including nontrivial holonomy and a 4-pi
fan whose holonomy is trivial but whose boundary is invalid. This addition
does not claim a fresh replay of every older research suite, a new tiling
count, or a general classification.

The independent [F3 vertex-inventory replay](research/f3-vertex-defects/)
checks the new written defect identities on two prior constructions:

```sh
python research/f3-vertex-defects/check_inventory.py
```

Its geometric inputs are the previous free-parameter construction and the
F2-to-F3 attachment; it does not independently recheck every tile pair or
decide either scale-one candidate.

## Arithmetic continuation (6 October 2026)

```sh
python research/arithmetic-continuation/check_norm_remainder.py
python research/arithmetic-continuation/check_split_part.py
python research/arithmetic-continuation/check_other_split_branches.py
python research/arithmetic-continuation/check_global_split_part.py
python research/arithmetic-continuation/check_global_sector_cli.py
```

All five commands are read-only by default and accept `--report PATH` to write
a fresh report. Optimized Python execution is explicitly rejected. The
first compares the norm parametrization with an independent square search
and counts subthreshold representations. The other commands compare restricted
split-factor lists with direct coefficient enumeration, including all eight
surviving rows in the global odd-multiplier theorem. None checks new
tiling coordinates or turns an arithmetic candidate into a small-scale
existence decision. Their universal conclusions require the written proofs
and the previously established constructive tails. All five commands are
included in the full coordinator; this update does not assert a fresh run
of every older, unchanged suite.

The last command checks the scoped membership tool's conclusive YES/NO,
unresolved small-scale status and input rejection. To inspect N=990, run
`python research/arithmetic-continuation/classify_global_sector.py 110 3`:
it correctly reports UNRESOLVED_SMALL_SCALE. See the
[package instructions](research/arithmetic-continuation/) for the exact
domain and runtime limitations.

The [source continuation audit](docs/audits/source-continuation-2026-10-06.md)
also records the attribution correction for the F3 vertex-count argument.

## Optional rebuild of publication outputs

The two new PDFs have editable sources. PDF rebuilding additionally needs Pandoc, XeLaTeX, pdfLaTeX, standard TeX packages and DejaVu fonts. No font files are distributed. From repository root:

```bash
python scripts/build_publication_outputs.py
```

This rebuilds the N105 and spectra PDFs and regenerates the expanded coordinate gzip. For coordinates alone use `--coordinates-only`; for the PDFs alone use `--pdfs-only`. Changes in typesetting tool versions or PDF metadata can change PDF hashes; treat a rebuilt artifact as a new publication snapshot, inspect it, then intentionally update the manifests. Do not expect a byte-identical PDF across TeX distributions.

## Mathematical boundary

The [complete class-22 theorem](docs/square-class-22.md) uses established
elliptic-curve arithmetic as well as the tiling spectra. Its new central-value
checker uses exact intervals and a rigorous infinite-tail bound, but cites
the conductor, local reduction types and root number. Modularity and the
rank-zero theorem are mathematical inputs, not software-verified theorems.
The [fixed-support theorem](docs/fixed-prime-support.md) likewise invokes a
published effective unit-equation result. No general S-unit enumeration or
bounded geometric campaign to compute its exact bases is claimed.

The [square-class tail/ray tool](research/square-class-tails/) implements
the finite tests in [the written theorem](docs/square-class-tails.md).
Its test suite compares inverse divisor formulas with a separate forward
parameter enumeration and checks scope-sensitive outputs. The bounds
reducing infinitely many exponents to finite coefficients are proved in
the note; they are not inferred from the test range.

The [quantitative density theorem](docs/quantitative-density.md) is a
written universal argument, including its [long-seam geometric input](docs/long-seams-density.md).
No finite checker is presented as proof of its asymptotic conclusion.
The separate [extreme-island embedding package](research/extreme-pure-embedding/)
checks an exact hierarchical construction: its 4,822,335 unit tiles are
specified by standard subdivisions, not expanded or tested pairwise.
The package README gives the exact replay commands and the boundary of
the local-switch obstruction.

Exact arithmetic eliminates numerical rounding in the implemented finite predicates. A separate geometric implementation reduces shared-code risk. Neither establishes external refereeing or formalizes the human lemmas and published classification theorems. In particular, finite CI does not prove the candidate all-primes induction, the all-parameter construction arguments, or a complete classification of all positive N.

The [claim ledger](STATUS.md), [N105 dependency note](docs/n105-global.md), [general spectra attribution](docs/general-spectra.md), and [full-solution roadmap](docs/full-solution-roadmap.md) keep those boundaries explicit.

## Integrated continuation: uniform reduction (30 September 2026)

The [uniform-reduction note](docs/uniform-reduction.md) and its complete source, test data, and separately checked positive witnesses are included in this publication. Its results are necessary spectra, two squarefree congruence obstructions, a finite candidate overlist, and formal boundary-signature witnesses. They are not a complete all-integer classification. The N=154 search is recorded as INCOMPLETE. The root verification coordinator now also replays all supplementary tests of this module in a disposable copy. Historical reports are retained with their original preparation scope.

## Integrated October modules

The original October package sources and their internal manifests are preserved byte-for-byte. ZIP digests are in [october-imports.json](verification/october-imports.json). The outer repository manifest additionally covers their integration. Fresh coordinator reports are separate from the historical `verification.json` records. The source packages’ statements that they did not push GitHub describe their original preparation, not the present integration.
