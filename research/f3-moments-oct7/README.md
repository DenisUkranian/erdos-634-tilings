# A position-moment obstruction barrier at 4830

7 October 2026. Research directed by Denis Paliy, with ChatGPT assistance.

**This is not a tiling and does not decide whether 4830 is admissible.**
It is an exact counterexample to a proposed obstruction method: first
position moments, individual containment and the known orientation-level
congruences do not suffice to exclude the outstanding F3 candidate.

For the primitive tile `(24,11,31)`, there is a multiset of exactly 4830
congruent triangles such that:

1. Every triangle is contained in the correct F3 target.
2. The complete directed-edge length signature matches the target.
3. For each direction separately, both coordinate first moments of the
   signed edge-length measure match the target.
4. The total tile area and its first area moment (hence its centroid)
   match the target.
5. The short-height populations are `n_1=93` and `n_2=4737`, satisfying
   `31 | n_1` and `n_2=4830 (mod 31)`.

There are only nine distinct placements. One placement is repeated 2385
times. Those triangles have identical interiors and overlap completely;
therefore the displayed multiset is explicitly not a tiling.

## Exact definitions

Use Eisenstein coordinates: `(x,y)` denotes `x+y*rho`, where
`rho=exp(i*pi/3)` and `rho^2=rho-1`. Set

    z=(24+11*rho)/31,
    R=conv(0,24,24+11*rho).

The target is counterclockwise with vertices

    (0,0), (961,0), (173926/961,1275120/961).

These are `0,c^2,c(a+2b)z^3`. The third side identity is

    c(a+2b)z^3-c^2 = 3b(a+b)rho z^2.

For each tuple `(h,j,e)` in the certificate, take a translate of
`z^h rho^j R` when `e=0`, or of `z^h rho^j conjugate(R)` when `e=1`.
The reflected triangle is traversed counterclockwise when its edge
moments are computed. Its translation and positive integer multiplicity
are specified in `exact-4830.json`.

The orientation inventory is:

| Short height | Rotation j | Reflected | Multiplicity |
| --- | --- | --- | --- |
| 1 | 0 | no | 38 |
| 1 | 0 | yes | 31 |
| 1 | 2 | no | 4 |
| 1 | 4 | no | 20 |
| 2 | 0 | no | 2385 |
| 2 | 1 | yes | 2 |
| 2 | 3 | no | 2339 |
| 2 | 3 | yes | 4 |
| 2 | 5 | yes | 7 |

For an oriented segment `e` of Euclidean length `l`, choose the canonical
unit vector for its unoriented direction, and let `s=+1` or `-1` according
to its orientation. If its midpoint is `(x_e,y_e)`, its three entries are

    (s*l, s*l*x_e, s*l*y_e).

These are its signed length and the two integrals of the coordinate
functions against signed arclength. Each entry is additive when an edge
is split. Hence every actual tiling, including one with T-junctions, must
have precisely the target values after its internal segments cancel.

This condition retains actual positions: translating a tile by `(u,v)`
adds its signed edge length times `u,v` to each direction's moments.
It is stronger than a translation-invariant orientation inventory.
Nevertheless, the certificate passes it exactly and overlaps.

All unit tile areas are equal. The area-centroid condition is therefore
simply that the sum of their centroids, with multiplicity, is 4830 times
the target centroid. This is separately checked; it does not follow from
matching first edge moments alone.

## Independent exact verification

Run from the repository root:

```bash
python research/f3-moments-oct7/independent_check.py
python research/f3-moments-oct7/exact_witness.py research/f3-moments-oct7/exact-4830.json
```

Both checks use rational arithmetic. The independent geometric checker
reconstructs the nine triangles, classifies their physical edge vectors,
and checks congruence, containment, all directed edge moments, total area,
and area centroid without importing the linear-programming model. It
checks all 81 vertex/target-halfplane inequalities for the nine positive
placements. Its report is `independent-check.json`.

The model-based check contains 39 scalar equalities and 216 containment
inequalities. The latter include zero-multiplicity orientation types;
there are only 81 actual positive-placement containment inequalities.
Neither checker searches for a tiling, and neither uses a numerical
solver to accept the certificate.

`moment_lp.py` records the exploratory linear/integer relaxation used to
find the witness. NumPy/SciPy are imported only when its solver is called;
ordinary exact verification is standard-library only. The solver allows
coincident placements, as is explicit in the mathematical formulation.

## Scope of the barrier

The result rules out an impossibility proof for 4830 using only the five
listed conditions. It does not rule out second or higher directional
moments, nonoverlap inequalities, adjacency, ordered seam conditions,
or a position-sensitive argument using stronger geometric information.
It supplies neither a new admissible count nor a negative decision.

A symbolic nine-type orientation inventory can also be written for norm
parameters, but the chosen four active containment constraints for this
certificate do not remain feasible throughout `a>2b`. Thus no universal
contained first-moment witness is asserted from this example.
