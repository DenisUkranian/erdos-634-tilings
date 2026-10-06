# A counterexample to universal pure chirality exchange

The [complete proof](../../docs/nonconvex-chirality-counterexample.md)
constructs a simple nonconvex all-long-edge disk with a pure unit tiling,
but proves that its opposite pure tiling is impossible. It is an auxiliary
counterexample, not a solution of Erdős problem 634.

For tile `(3,5,7)`, six ordinary triangular grids of scales
`25,15,9,25,15,9` give 1862 tiles. Their orientation-pair populations
are `(162,1250,450)`. The boundary forces any opposite pure tiling
to have populations `(930,-30,962)`.

Run ordinary Python, without `-O`, `-OO`, or `PYTHONOPTIMIZE`:

```bash
python verify_witness.py
python check_boundary.py
```

- `verify_witness.py` generates the construction and checks every unit
  triangle against the six allowed rotations. It checks containment,
  all 1,732,591 unit pairs for interior overlap, the six macrotriangles,
  exact total area, atomized edge cancellation, long-edge boundary,
  and the negative opposite inventory. It rewrites the two JSON files
  beside the script deterministically.
- `witness_3_5_7.json` contains every unit triangle, its macrotriangle,
  and its rotation index in short Eisenstein coordinates.
- `verified.json` records the result and finite checking scope.
- `check_boundary.py` does not import the grid generator. It reconstructs
  the boundary transformation by exact matrix inversion of the long lifts,
  then independently computes both boundary vector areas by cross products.
- `counterexample.svg` is an explanatory Euclidean drawing of the six
  macrotriangles. Its rendering is not used by either exact check.

The project coordinator replays both programs in its disposable copy.
The infinite family and the topological lift argument are written proofs,
not conclusions inferred from finite numerical testing. Internal audits
are not external refereeing or proof-assistant verification.
