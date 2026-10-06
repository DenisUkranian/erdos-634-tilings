# Exact verification from an abstract disk

`verify_disk.py` accepts only ordered vertex incidences, whole integer tile
side lengths, and three marked target corners and side lengths. Coordinates
and atomic seam lengths are not accepted as input. It verifies a supplied
gluing; it does not search for gluings or decide a new tile count.

The [existing disk theorem](../../docs/exact-seam-certificates.md) provides
the mathematical certificate system. The [proof audit and direct-development
criterion](../../docs/audits/disk-realization-2026-10-06.md) justify this
implementation: a consistent orientation-preserving development of a disk,
with boundary traversing a positive triangle once, has degree one. All face
interiors are therefore disjoint and their union covers the target.

## Run

From the repository root, using Python 3.11 or newer and its standard library:

```sh
python research/disk-certificates/verify_disk.py research/disk-certificates/disk-322.json
python research/disk-certificates/test_disk.py
```

Both commands are read-only unless `--report PATH` is supplied. Verification
uses explicit error checks, including under `python -O`.

To reproduce the coordinate-free input from the older coordinate certificate:

```sh
python research/disk-certificates/export_322.py --output /tmp/disk-322.json
```

Only the exporter reads the older coordinates. The standalone verifier imports
neither the exporter nor construction code.

## Input and verification

The `integer-triangle-disk-v1` JSON object has exactly five keys:

- `schema`: the schema name above;
- `tile_sides`: the three positive integer side lengths;
- `faces`: each has `side_lengths`, a cyclic permutation or reversed ordering
  of the tile lengths, and `side_vertices`, three ordered chains of global
  nonnegative integer vertex IDs;
- `target_corners`: three distinct IDs in the positive boundary order;
- `target_side_lengths`: lengths joining successive target corners.

Each face chain includes both endpoints; successive chains have matching
endpoints. Interior atomic edges occur twice, with reversed directions.
All face-boundary vertices must be distinct, except the repeated final
endpoint closing the face. Every subdivision vertex must be a genuine
triangle corner somewhere, so arbitrary sliding subdivision marks are absent.

The verifier checks the full disk topology, including vertex links and one
boundary component, not just Euler characteristic. Original-side contact
components must be [caterpillars](../../docs/seam-caterpillars.md). Integer
leaf elimination determines every contact length and rejects zero or negative
lengths. Each face is developed with exact `Fraction` arithmetic in coordinates
`(x, y sqrt(H))`, where `H=16 area(tile)^2`. All shared vertex images must agree,
including around cycles. Every boundary chain must run straight and strictly
forward between its designated corners. No angle approximation is used.

## Retained checks and their limits

The [322-face certificate](disk-322.json) verifies the previously known target
with sides `(115,126,81)` using tile `(5,6,9)`. It includes 24 T-junctions,
195 vertices, and 516 atomic edges. The [verification report](verification.json)
records this new incidence-only replay; it is not a new tiling construction.

The [test report](test-report.json) retains four positive cases and thirteen
adversarial cases. In particular, a disk fan of angle `4 pi` has consistent
holonomy and correctly spaced marked corners, yet fails the complete boundary
test. Checking closure or a rotation product alone would miss that obstruction.
Other examples check topology, orientation, side balance, and T-junction data.

The tests check code on finite inputs; the degree argument is a written
mathematical theorem, not a proof-assistant verification. Rejecting one disk
does not rule out another disk for the same tile count. The general F3
small-scale problem and Erdős 634 remain unresolved.
