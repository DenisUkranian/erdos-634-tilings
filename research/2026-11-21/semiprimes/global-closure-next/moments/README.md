# Optional numerical height-moment diagnostics

These exploratory runs are not premises of the global theorem or exact
certificates of target feasibility. They retain the tile height, orientation,
hand, signed populations, and linear/quadratic endpoint moments. The anchor
domain is the containment triangle for each orientation. The resulting
columns are affine in the anchor, so its three vertices suffice for this
particular continuous fractional projection.

[height_moment_probe.py](height_moment_probe.py) uses NumPy and SciPy.
[NUMERICAL_DIAGNOSTICS.json](NUMERICAL_DIAGNOSTICS.json) records three runs:
3431 at odd mass 111 and heights 0--2; 5063 at odd mass 215 and heights
0--2; and 5063 at odd mass 215 over its full known height envelope.
The solver returned numerical feasibility in each projection. No result
was converted to an exact rational certificate. In particular small
floating-point negative masses and residuals must not be presented as
an integer or exact positive tiling.

For example, from this directory:

```sh
python3 height_moment_probe.py 35 13 43 --lo 0 --hi 2 --odd 215
```

This projection omits exact phase membership, individual contact lines,
integral multiplicity, and nonoverlap. The separate
[3431 first-transverse-moment theorem](../geometry3431/FIRST_MOMENT_LIMIT.md)
is an exact result about a different, stronger specified periodic model.
It does not depend on these numerical runs.
