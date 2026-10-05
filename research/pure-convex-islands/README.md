# Exact checks for the convex pure-island theorem

The complete proof is in
[convex-pure-island-classification.md](../../docs/convex-pure-island-classification.md).
It proves a necessary and sufficient condition for convex pure all-long-edge
islands of primitive integral 120-degree triangles, and their opposite-state
retiling on the same polygon. It does not solve all of Erdős 634.

All scripts use Python's standard library. From the repository root:

Use ordinary Python without `-O`, `-OO`, or `PYTHONOPTIMIZE`, since the
checkers use assertions. The repository's `scripts/verify_all.py` also
runs these three checks in a disposable copy.

```bash
python research/pure-convex-islands/verify_laurent_jets.py
python research/pure-convex-islands/verify_hex_jets.py
python research/pure-convex-islands/verify_stepped_seed.py
```

The first two scripts enumerate actual lattice cells independently of the
displayed boundary formulas, and use exact integer cyclotomic remainders.
They check both derivatives as well as values. Their JSON reports are saved
next to the scripts. The third constructs the facets directly from the height
formula and checks integer grid compatibility, containment, separating-axis
nonoverlap and exact area. It prints its report.

The selected cases exercise odd and even parameters, both jet families,
all four hexagon phase branches, a known positive boundary, and an asymmetric
norm triple. The universal statements follow from the written proof, not
from a finite search or an optimization solver's status.

The main text includes the complete geometric reduction, so these checks
do not depend on unpublished notebooks or the older search engines.
