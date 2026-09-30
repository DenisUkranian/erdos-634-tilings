# Erdős 634 — general parity and construction note

30 September 2026. General proofs plus a reproducible fixed-tile construction.

**Not a complete solution of Erdős 634. No external review or priority claim.**

Read the [attribution addendum](ATTRIBUTION.md) and `PROOF.md`. The typeset version is
`paper.pdf`, with editable source `paper.tex`.

The equilateral arithmetic proof uses two signed-direction characters and
parity. The related isosceles/F1 necessary spectra are credited to Vico Bonfioli;
the underlying trapezoid construction is credited to Yan X Zhang. This note
also gives an exact residue refinement of the sufficient multiplier threshold.

The certificate `construction_116640.json` partitions an equilateral triangle
of side 12960 into 36 macroregions. Each has an explicit standard subdivision
into copies of the primitive tile (45,32,67), for 116640 tiles in total.
`tiles_116640.jsonl.gz` contains their expanded exact coordinates. Coordinates
(x,y) represent (x+y/2,sqrt(3)*y/2).

## Reproduce

Use Python 3.10 or newer and the standard library, from this directory:

```sh
python verify_certificate.py construction_116640.json --expand
python check_general_formulas.py
```

Regenerate the hierarchical certificate separately:

```sh
python build_certificate.py --output regenerated.json
python verify_certificate.py regenerated.json --expand
```

The checker does not import the generator. Macroregion disjointness is checked
by exact rational clipping. Every expanded small triangle is checked for
congruence, oriented area and containment. Small-triangle disjointness uses the
explicit standard grid/strip partitions, rather than an O(N^2) pair test.
The verifier performs explicit checks, not optimization-sensitive assertions.

`construction_expanded_check.json` records the retained expanded replay.
`general_checks.json` records supplementary formula and mutation tests.
The written proofs, not extrapolation from finite tests, establish the
all-parameter results. Small-scale realizability and the other angular
families remain outside these results.

All supplied code is original to this continuation. Referenced authors' source
files are not redistributed in this package. No fonts are included.
