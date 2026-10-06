# Extreme pure island in a triangular target

Exact certificates for the [proof](../../docs/extreme-pure-island-in-triangle.md).
A previously proved nonexchangeable pure island is embedded as the unique
highest short-level component of an equilateral tiling. The collar and
three corners use only the two lower edge levels.

This refutes the proposed **component-local opposite-pure replacement**
even for a triangular target. It does not refute mixed replacements or
global orientation normalization: this same target has another tiling
using only the two lower levels. The tile count is construction bookkeeping,
not a newly resolved case of Erdős 634.

## Files

| File | Purpose |
|---|---|
| `collar.json` | 1902 macrolozenges between the bad polygon and a regular hexagon |
| `verify_collar.py` | Exact cell enumeration, perfect matching and two boundary checks; optional deterministic regeneration |
| `collar_verified.json` | Recorded integer verification and certificate hash |
| `corner_base.json` | Established $(5,3,7)$ equilateral construction at multiplier 63 |
| `corner_base_verified.json` | Existing independent macrogeometry verifier's report |
| `verify_embedding.py` | Independent collar boundary-chain check, corner assembly, all block directions, modified strip grids and total counts |
| `embedding_verified.json` | Recorded independent embedding report |

## Reproduce from the repository root

```bash
python research/extreme-pure-embedding/verify_collar.py
python research/general-spectra/verify_certificate.py research/extreme-pure-embedding/corner_base.json
python research/extreme-pure-embedding/verify_embedding.py
```

Use ordinary Python without `-O`: the two new checkers explicitly reject
optimization because their verification gates use assertions. They require
only the Python standard library. The general-spectra macrogeometry checker
uses explicit runtime checks.

The matching can optionally be regenerated with:

```bash
python research/extreme-pure-embedding/verify_collar.py --regenerate
```

This rewrites `collar.json`; ordinary verification is read-only. The base
corner certificate can be regenerated with the existing program:

```bash
python research/general-spectra/build_certificate.py --tile 5 3 7 --angle 120 --m 63 --output research/extreme-pure-embedding/corner_base.json
```

## What is checked and what is proved geometrically

`verify_collar.py` and `verify_embedding.py` independently check the same
collar. The latter does not import the former's winding or matching code:
it reconstructs distinct grid cells, verifies adjacency and containment,
and cancels their boundary chain to the outer hexagon plus the clockwise
hole. This establishes actual coverage, not just the area sum.

The existing general-spectra checker certifies the base corner's 252
convex macroregions and 31626 pairs. Uniform scaling by three preserves
that partition. The embedding checker verifies all 189 triangle-block
directions and all 63 modified strips. Each strip is filled exclusively
by cells with local vectors `(3,0)` and `(-5,5)`; using the unmodified
mixed-width strip filling would introduce the unwanted highest level.

Each collar lozenge is filled by the previously proved 1470-tile
opposite-pure seed. The island is the previous 1862-tile counterexample
scaled by 15 and subdivided into unit triangles. The whole construction
contains 4822335 tiles; these were not expanded or subjected to an
all-pairs test. Disjointness follows from the exact macro partition and
explicit standard grids. The obstruction is the island's negative
opposite inventory, not a numerical search failure.

The mathematical proof and certificates received separate internal
checks; no external referee approval or formal proof-assistant
verification is claimed.
