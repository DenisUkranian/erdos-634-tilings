# Terminal-phase obstruction checkpoint

20 November 2026. This branch investigates a universal impossibility
proof for the 3431 and 5063 F2 targets. It supplies local results and
an exact barrier example. **Neither target is decided.**

## Results

* [Terminal Euclidean translates](TERMINAL_TRANSLATES.md): every
  occupied translate in a terminal exterior-free phase node has
  population divisible by `c`, at least `2c`, with its two sign counts
  separately divisible by `c`. Thus a terminal node of population
  less than `4c` lies in a single Euclidean translate. The proof
  cancels only outward long edges of paired tiles, retaining their
  short-edge currents.
* [Charged terminal polygon](CHARGED_TERMINAL_PATCH.md): an explicit
  positively tiled polygon has a terminal exterior-free node with
  population `c^2` and character `-c`. A rigid motion puts the entire
  polygon inside the F2 target. The resulting F2 placement is a
  partial packing; a completion may add same-node tiles or descendants.
  The example therefore refutes a general polygonal terminal-zero-
  character theorem, not an F2-specific theorem using the complete
  complement.
* [Whole-c domain](WHOLE_C_DOMAIN.md): a domain with connected tile
  adjacency and whole-`c` boundary cannot contain exactly `c` tiles,
  even with mixed heights. For boundaries represented by outside
  long sides, the final step requires the per-line single-block
  theorem; the shortcut `dD=0` requires inside long sides.

The translate note also proves that a charged region cannot be
replaced using only heights of the opposite parity, and that even a
balanced half-turn pair has no positive local replacement entirely
below its short height. These observations prevent an unsupported
branch-removal argument.

## Integer torus diagnostic

For a terminal node of population `3c`, the translate lemma permits
normalizing all vertices into `R`. Reduce them modulo `cR`. Selected
short-edge endpoint currents vanish separately on each of the three
axes, because complementary whole `c` edges have identical residue
endpoints. The outward-hand tiles occur in half-turn pairs; the
inward hand is left as individual columns.

`terminal_torus.py` imposes these exact integer endpoint equations,
population `3c`, and signed population `G=c`. Translation and
120-degree rotation place one positive inward tile at the origin.
All column multiplicities are nonnegative integers. The projection
contains no geometric containment, nonoverlap, or full-tiling
completion constraints. It also identifies different physical
supporting lines with the same residues.

| Tile | Rows | Columns | Run limit | Observed result |
|---|---:|---:|---:|---|
| `(5,3,7)` | 149 | 441 | 20 s | Exact integer witness: population 21, character 7 |
| `(33,7,37)` | 4109 | 12321 | 20 s | Time limit, no integer witness and no infeasibility result |
| `(35,13,43)` | 5549 | 16641 | 20 s | Time limit, no integer witness and no infeasibility result |

The control witness is checked with integer arithmetic in
`verify_terminal_torus_witness.py`; SciPy is unnecessary for replay.
It is a residue-pattern witness, not a tiling or a counterexample to
a geometric lower bound. The two target diagnostics are explicitly
inconclusive. No further search is hidden behind those outcomes.

The separate same-sign possibility `G=3c` was not excluded by this
diagnostic. The existing terminal `2c` balance proof does not extend
automatically to `3c`: inward tiles may have both signs, and the
outward pairs retain their short-edge currents.

## Replay

```sh
python3 verify_charged_patch.py
python3 verify_terminal_torus_witness.py
```

The first verifies `charged_patch_certificate.json`, whose native
coordinates describe one `c`-grid triangle and its parent teeth.
It checks only the asserted partial packing inside F2.
The second replays the exact control pattern and reports the two
saved timeouts without rerunning optimization.

## Remaining global step

No proof that a charged terminal F2 node must have at least `c^2`
tiles has been obtained. No exclusion of a charged terminal node
with `3c` tiles has been obtained. Even a valid zero-character
theorem for all exterior-free terminal nodes would leave the
distinguished height-one node, whose subtree contains the outer
height-two edge node; it can carry `G_odd=-c`.

A universal impossibility proof still needs an argument using the
complete complement, or a proved positive replacement that removes
branches and leaves a class already known impossible. None of the
finite integer diagnostics supplies that missing step.
