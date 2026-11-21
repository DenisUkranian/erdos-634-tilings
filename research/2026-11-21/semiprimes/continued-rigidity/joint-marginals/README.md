# Exploratory joint integer marginal models

21 November 2026. **Neither target is excluded.**

`probe_joint_marginal_integer.py` keeps both one-coordinate endpoint
projections of each orientation, equates their orientation totals, and
imposes exact positive/negative cell populations. Integer cell gate
currents are summed before the complete-node charge congruences are
imposed. The optional `--integer-marginals` flag also requires each
orientation/residue marginal count to be integral.

Every physical tiling induces these marginals. Conversely, feasible
marginals need not reconstruct a full two-coordinate endpoint kernel,
actual supporting lines, or disjoint triangles. A numerical solve is
therefore exploratory. An integral returned point is checked against
the complete integer matrix and bounds before being recorded; no such
point was obtained in these target runs.

Both free-charge two-cell native roles at 5063 reached 45-second limits
without a feasible incumbent. The native one-cell integer-marginal
profile reached a 60-second limit. These statuses are retained in the
three JSON files in this folder. The neighboring `integer3431` folder
records fixed/free 3431 runs and a first-moment congruence augmentation;
their integer runs were also inconclusive.

The continuous two-cell endpoint feasibility question is separately
settled positively for the displayed profiles by
[exact rational certificates](../cells5063/TWO_CELL_RATIONAL_LIMIT.md).
Those certificates are stronger mathematical information than these
numerical timeouts, but they do not settle integer marginal feasibility.

This optional script needs NumPy/SciPy and is not part of the exact
replay or any target impossibility proof.
