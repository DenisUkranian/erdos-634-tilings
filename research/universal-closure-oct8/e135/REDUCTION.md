# The complete nine-level E135 problem reduces to 246,600 placements

The target is the equilateral triangle with Eisenstein-coordinate vertices
`(0,0), (45,0), (0,45)`. The tile has sides `(3,5,7)`, so an actual tiling would
contain exactly 135 tiles.

This note proves the finite placement reduction, conditional only on the
separately audited structural statement that every potential tiling has its
short-edge heights in an interval of at most nine consecutive integers
containing zero. It does not substitute a solver status for an exact negative
certificate on the final residual model.

## Complete geometric domains

Let `rho=exp(i*pi/3)`, `R=Z[rho]`, `eta=2+rho`, and `bar(eta)=3-rho`.
Then `eta*bar(eta)=7` and

```
z=(3+5*rho)/7=eta/bar(eta).
```

For heights `[L,U]`, the seam lattice lemma gives

```
Lambda = sum_(h=L)^U z^h R = g R,
g = eta^L / bar(eta)^U.
```

The equality holds because `eta` and `bar(eta)` are coprime: a common divisor
would have norm dividing both 7 and the norm 3 of `eta-bar(eta)`. After
extracting `g`, the generating ideal contains the coprime endpoint powers.

Multiplication by `rho^r/g` takes all possible vertices into `Z[rho]`. Here
`r` is an optional coordinate rotation chosen only to reduce storage. In this
frame the short-edge unit at height `h` is

```
u_h = rho^r * eta^(h-L) * bar(eta)^(U-h).
```

The twelve tile orientations at that height are the six rotations of
`{0,3*u_h,5*rho^2*u_h}` and `{0,5*u_h,3*rho^2*u_h}`. Every integer placement of
these triangles whose three vertices belong to the target is included. Since
the target is convex, checking its three vertex inequalities is sufficient.

For a fixed orientation and fixed integer y-coordinate of the 120-degree
vertex, the possible x-coordinates initially form one interval. This follows
by intersecting three translated copies of the target's exact half-planes.
The program stores finite unions of integer intervals throughout the
calculation; it does not materialize the hundreds of billions of individual
positions.

## Exact eliminations with arbitrary T-junctions

Give the target and every candidate tile counterclockwise boundary orientation.
On a line with fixed unoriented direction, the derivative of a directed edge
from `p` to `q` has endpoint coefficients `+1` at `p` and `-1` at `q`.
A row is specified by the direction and the exact endpoint. Any tiling therefore
satisfies

```
B*x=b,   x>=0.
```

All right-hand sides vanish except the target's six endpoint-direction
incidences. In a zero row with no surviving negative term, every positive term
must be zero; conversely with signs exchanged. This rule remains valid if a
row has no terms at all.

At each direction and horizontal line, the program forms the unions `P` and
`N` of endpoint positions supported by positive and negative candidate terms.
The differences `P\N` and `N\P`, excluding the finitely many nonzero boundary
rows, specify exactly such valid eliminations. Union, difference and translation
are performed on sorted integer intervals. T-junctions require no special
assumption: a long edge has no derivative at an intermediate point, while the
two adjoining short edges cancel their endpoint contributions there.

The generator emits an independently replayable trace. A record consists of
five little-endian signed32 integers:

```
(direction_id, y_index, x_left, x_right, sign)
```

It asserts that, for each integer x in the inclusive interval, the zero row
has no remaining term of the opposite sign. Every matching-sign candidate
incident there may consequently be deleted. A replayer must check absence of
the opposite sign and absence of a nonzero boundary right-hand side throughout
the interval. It need not require the claimed sign to remain nonempty: earlier
records from the same batch may already have deleted some of these candidates,
and a vacuous deletion is valid.

## All nine-level cases

Reflection of the equilateral target sends height `h` to `-h`. The following
five bands therefore cover every interval of width at most eight containing
zero, including smaller intervals with unoccupied end levels.

| Band | All contained placements | Final surviving placements |
|---|---:|---:|
| `[-4,4]` | 420,445,247,592 | 246,600 |
| `[-3,5]` | 420,583,549,524 | 246,600 |
| `[-2,6]` | 420,309,426,351 | 246,558 |
| `[-1,7]` | 420,224,867,466 | 186,798 |
| `[0,8]` | 420,441,801,582 | 83,163 |

All five calculations reached a fixed point. None ended at a resource limit.
Their traces only eliminate forced-zero variables; these fixed points by
themselves are not assertions of satisfiability or unsatisfiability.

`normalize_pools.py` converts every surviving triangle into original physical
Eisenstein coordinates with common denominator `7^8=5764801`, sorts its three
vertices, and performs literal set containment checks. Every band residual,
and its reflection `(x,y)->(y,x)`, is contained in the **same 246,600-placement
pool** obtained independently from the old complete `[-3,3]` bitmap model.
The first two residuals are equal to that reference pool. Its normalized
SHA-256 is

```
7a9182ff37328cc6e5b7c6fe822bbcf529687ecd12a0bc31927e6633d71f715a
```

This hash describes the explicit sorted physical-coordinate records, not a
claim of mathematical equivalence based on a hash alone. The verifier performs
all coordinate conversions and set comparisons before recording the hash.
See `all_k9_normalized.json` for the comparisons and counts by height.

Consequently, after the separate structural bound and independent RLE replays
are checked, **any E135 tiling must use candidates from this one finite pool**.
An independently checked exact UNSAT certificate for the pool's Boolean
endpoint-current system would then exclude the unrestricted E135 tiling.
An ordinary CP-SAT message `INFEASIBLE` alone is not used as that certificate.

## Checks and reproduction

The RLE program's complete five- and seven-level fixed-point files agree
byte-for-byte with the previous bitmap implementation, although the algorithms
schedule eliminations differently. A four-tile positive control also agrees
and passes separate exact geometric checks. The actual C++ interval operators
have been compared against literal integer sets on 10,000 randomized cases.
These checks supplement, rather than replace, the independent trace replay.

The separate `check_unit_metric_model.py` checker also reconstructs the final
seven-level reference pool in exact physical coordinates and compares it
literally with the geometry file used to export the Boolean model. It verifies
all 246,600 placements: congruence to `(3,5,7)`, orientation, area, containment,
and uniqueness. Using its own direction-plus-endpoint row keys, it then rebuilds
all 247,770 endpoint equations with 1,479,600 signed coefficients and compares
their literal multiset with the exported model. Every pool variable is present
once. The model verification is independent of the exporter and does not claim
UNSAT. Its report is `unit_metric_model_verified.json`.

The subsequent Boolean presolve and native OPB export have also been reviewed.
`check_weighted_opb.py` independently checks all 166,392 reduced equalities,
preserving repeated-literal coefficients. It reconstructs the additional
original-tile count from the full affine identification map. In this instance
9,804 original variables are fixed to zero, and the 197,124 free variables have
positive count weights from 1 to 14. The last equality is the weighted sum 135;
an unweighted count on the reduced variables would be incorrect. See
`weighted_opb_verified.json`. This verifies the encoding, not its satisfiability.

A separate single-thread HiGHS interior-point probe of the original model with
bounds `[0,1]` and count 135 stopped at its time limit. The configured limit was
120 seconds, but basis construction delayed termination to about 174 seconds.
It produced no negative certificate; `ipm_original_report.json` explicitly
records this unresolved outcome.

Compile and run sequentially from the repository root:

```sh
g++ -O3 -std=c++17 research/universal-closure-oct8/e135/rle_equilateral135.cpp -o /tmp/e135-rle
/tmp/e135-rle -4 4 /tmp/e135-rle-k9-center 180 1 0
/tmp/e135-rle -3 5 /tmp/e135-rle-k9-offset1 180 1 0
/tmp/e135-rle -2 6 /tmp/e135-rle-k9-offset2 180 1 0
/tmp/e135-rle -1 7 /tmp/e135-rle-k9-offset3 180 1 0
/tmp/e135-rle 0 8 /tmp/e135-rle-k9-edge 180 1 0
```

Arguments after the band are output prefix, time limit, trace flag, and positive
control scale. A slower machine can increase the time limit; an interrupted
run is explicitly marked `incomplete` and proves no complete reduction.

Use the old bitmap generator to reproduce the reference seven-level pool, or
use the byte-identical RLE seven-level pool:

```sh
/tmp/e135-rle -3 3 /tmp/e135-reference 180 1 0
python3 research/universal-closure-oct8/e135/normalize_pools.py /tmp/e135-rle-k9-center /tmp/e135-rle-k9-offset1 /tmp/e135-rle-k9-offset2 /tmp/e135-rle-k9-offset3 /tmp/e135-rle-k9-edge --reference /tmp/e135-reference --output /tmp/e135-normalized.json
python3 research/universal-closure-oct8/e135/check_interval_operations.py
```

Once the geometry and endpoint-model exports have been regenerated, verify
their exact binding to the audited reference pool with:

```sh
python3 research/universal-closure-oct8/e135/check_unit_metric_model.py /tmp/e135-k7-center.geometry.txt /tmp/e135-k7-center.model.txt /tmp/e135-unit-model-checked.json --reference-prefix /tmp/e135-reference
python3 research/universal-closure-oct8/e135/check_weighted_opb.py /tmp/e135-dsu /tmp/e135-dsu-count135.opb /tmp/e135-opb-checked.json
```

The raw RLE trace format is documented above. Raw trace digests are in
`trace_manifest.json`. The original C++ `state_MB` diagnostic inherited from the
bitmap prototype is a hypothetical dense two-bit estimate; no such array is
allocated by the RLE program.
