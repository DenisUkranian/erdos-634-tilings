# F3 vertex-defect inventory

The proof is [Necessary vertex defects](../../docs/f3-vertex-defects.md).
Every F3 tiling by an integer-sided 120-degree tile must have a triple-γ
interior vertex and a mixed T-junction, with the exact inequalities stated
there. For consecutive shorter tile sides it must also have a unit seam
atom. These are necessary conditions only. The subsequent
[nested-corner construction](../group2-nested-corners/PROOF.md) resolves
990 positively; 4830 remains unresolved.

Run from the repository root:

```sh
python research/f3-vertex-defects/check_inventory.py
```

Or run `python check_inventory.py` from this directory. Both commands are
read-only and print deterministic JSON. An optional `--report PATH` saves
the report; `verified_inventory.json` freezes the checked fixtures.

The checker obtains F2 tilings from the existing
`../group2-trapezoids/construct_free_k.py` constructor and its `grid`,
`cmul`, and `smul` helpers. It attaches the standard F3 triangle using the
explicit formula in `../group2-trapezoids/BALANCED_F4.md`. It then uses
integer-scaled coordinates to compute all vertex corner inventories and
flat incidences, the forced mismatch endpoints, and atomic seam lengths.
It checks the charge identity, injectivity of mismatched radial contacts,
the mixed-T lower bound, and the predicted unit atom when `|a-b|=1`.

The two examples are `(5,3,7)` at scale 2, with 1,056 tiles, and
`(8,7,13)` at scale 2, with 3,960 tiles. Both have exactly one triple-γ
vertex, so the universal lower bound is sharp. The second has 20 unit
atoms, counted as 40 tile-side incidences in the report.

The replay does not independently check all tile-pair intersections; it
uses the prior positive construction as its geometric input. It provides
a reproducible implementation check of the vertex accounting, not the
basis for extrapolating the theorem or a nonexistence certificate.
