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

## Optional rebuild of publication outputs

The two new PDFs have editable sources. PDF rebuilding additionally needs Pandoc, XeLaTeX, pdfLaTeX, standard TeX packages and DejaVu fonts. No font files are distributed. From repository root:

```bash
python scripts/build_publication_outputs.py
```

This rebuilds the N105 and spectra PDFs and regenerates the expanded coordinate gzip. For coordinates alone use `--coordinates-only`; for the PDFs alone use `--pdfs-only`. Changes in typesetting tool versions or PDF metadata can change PDF hashes; treat a rebuilt artifact as a new publication snapshot, inspect it, then intentionally update the manifests. Do not expect a byte-identical PDF across TeX distributions.

## Mathematical boundary

Exact arithmetic eliminates numerical rounding in the implemented finite predicates. A separate geometric implementation reduces shared-code risk. Neither establishes external refereeing or formalizes the human lemmas and published classification theorems. In particular, finite CI does not prove the candidate all-primes induction, the all-parameter construction arguments, or a complete classification of all positive N.

The [claim ledger](STATUS.md), [N105 dependency note](docs/n105-global.md), [general spectra attribution](docs/general-spectra.md), and [full-solution roadmap](docs/full-solution-roadmap.md) keep those boundaries explicit.

## Integrated continuation: uniform reduction (30 September 2026)

The [uniform-reduction note](docs/uniform-reduction.md) and its complete source, test data, and separately checked positive witnesses are included in this publication. Its results are necessary spectra, two squarefree congruence obstructions, a finite candidate overlist, and formal boundary-signature witnesses. They are not a complete all-integer classification. The N=154 search is recorded as INCOMPLETE. The root verification coordinator now also replays all supplementary tests of this module in a disposable copy. Historical reports are retained with their original preparation scope.

## Integrated October modules

The original October package sources and their internal manifests are preserved byte-for-byte. ZIP digests are in [october-imports.json](verification/october-imports.json). The outer repository manifest additionally covers their integration. Fresh coordinator reports are separate from the historical `verification.json` records. The source packages’ statements that they did not push GitHub describe their original preparation, not the present integration.
