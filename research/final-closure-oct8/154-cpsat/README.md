# Complete placement certificates for the 154 candidate

This directory began as a CP-SAT experiment. Its final negative certificates use
only exact nonnegative boundary-current elimination; they do not need CP-SAT,
linear programming software, floating-point geometry, or an assumed tiling
pattern.

The target is the triangle with Eisenstein-coordinate vertices
`(0,0), (154,0), (49,56)`, and the tile has sides `(8,7,13)`.

## What has been computed

All placements in each of the following **complete** height-band lattices were
enumerated implicitly, and their nonnegative endpoint-current systems were
contradicted:

| Short-edge heights | Complete candidate placements | Recorded elimination steps | Final surviving candidates |
|---|---:|---:|---:|
| `[-2,2]` | 4,773,371,018 | 28,902,031 bitmap records | 346 |
| `[-1,3]` | 4,770,414,013 | 29,851,242 bitmap records | 573 |
| `[0,4]` | 4,759,540,301 | 29,846,977 bitmap records | 610 |

In every case a boundary equation with right-hand side `+1` or `-1` has no
remaining term of the required sign. The surviving candidates therefore do not
form a solution. This is a contradiction, not a search timeout.

The three bands, together with reflection, include every height support of
width at most four that contains zero. End levels need not be occupied in the
placement model. Consequently the older three- and four-level exclusions are
controls and are not separate prerequisites for the five-level certificates.

**The independent replay and the prerequisites bounding the height support are
owned by the adjacent audit directories.** In particular, the numerical lower
bounds `n_0 >= 24` and `n_h >= 26` alone do not exclude six levels: the separate
exact directional argument is required. These files by themselves do not claim
a classification of all tile counts in Erdős 634.

## Exact lattice and enumeration

Write `rho = exp(i*pi/3)`, `R = Z[rho]`, `eta = 3+rho`, and
`bar(eta) = 4-rho`. Then

```
eta * bar(eta) = 13,
z = (8+7*rho)/13 = eta/bar(eta).
```

The prior seam lattice lemma puts every vertex of a tiling whose short heights
are in `[L,U]` into `sum_(h=L)^U z^h R`, after fixing a target vertex at zero.
Since `eta` and `bar(eta)` are coprime in the Eisenstein ring,

```
Lambda_[L,U] = g R,       g = eta^L / bar(eta)^U.
```

Indeed, after extracting `g`, the generating ideal contains the relatively
prime elements `eta^(U-L)` and `bar(eta)^(U-L)`. Coprimality follows because a
common divisor would divide both `eta` (norm 13) and `eta-bar(eta)` (norm 3).

The coordinate change `w -> rho^r*w/g`, where `r` is an optional integer rotation,
puts the target and all admissible vertices in `Z[rho]`. The unit vector of
height `h` becomes the exact integer vector

```
u_h = rho^r * eta^(h-L) * bar(eta)^(U-h).
```

For each lattice point used as the 120-degree vertex, the program tries

```
{0, 8*u_h, 7*rho^2*u_h},
{0, 7*u_h, 8*rho^2*u_h},
```

and all six rotations by `rho`. These are all twelve orientations of the tile
at height `h`, including both reflections. A candidate is included exactly when
its three vertices lie in the closed target. Convexity makes this containment
test sufficient. For a fixed orientation and integer y-coordinate, admissible
x-coordinates form one interval obtained from the target's exact half-planes;
this is why a complete multi-billion-placement enumeration fits in bitmaps.

The rotated generator chooses `r` solely to reduce the rectangular bitmap's
memory. In the supplied certificates it uses `r=1` for `[-1,3]` and `[0,4]`.
The central certificate uses `r=0`.

## The negative certificate rule

Give every tile and the target the counterclockwise orientation. On each
unoriented line direction, differentiate its scalar boundary current along the
line. An oriented edge from `p` to `q` contributes `+1` at `p` and `-1` at `q`.
A row is identified by its direction and its exact endpoint. Hence an actual
tiling necessarily satisfies

```
B x = b_target,       x >= 0.
```

No upper bound or integrality of `x` is used in these certificates. All rows have
right-hand side zero except the six endpoint-direction incidences of the target
boundary, whose right-hand sides are `+1` or `-1`.

In a zero row, if no negative coefficient remains, every remaining positive
variable must be zero. The analogous statement holds with signs exchanged.
The bitmap program applies exactly this rule to 64 endpoint positions at a
time. At the terminal boundary row, all variables of the required sign have
been eliminated. A right-hand side `+1` then faces a nonpositive left-hand side,
or a right-hand side `-1` faces a nonnegative left-hand side.

This argument is independent of how the eliminated rows were discovered or
scheduled. An independent replayer only needs to verify each supplied
elimination and the terminal row.

## Reproduce the three certificates

A C++17 compiler and a machine with roughly 3 GB of free memory for one case are
sufficient. Run the cases sequentially. The limits below permit resource
interruption; an interrupted result is explicitly `incomplete` and is not a
negative certificate.

From the repository root:

```sh
g++ -O3 -std=c++17 research/final-closure-oct8/154-cpsat/bitmap_zero.cpp -o /tmp/634-bitmap
g++ -O3 -std=c++17 research/final-closure-oct8/154-cpsat/bitmap_zero_rotated.cpp -o /tmp/634-bitmap-rotated
/tmp/634-bitmap -2 2 /tmp/634-bitmap-five-center 180 1 0
/tmp/634-bitmap-rotated -1 3 /tmp/634-bitmap-five-offset 180 1 0
/tmp/634-bitmap-rotated 0 4 /tmp/634-bitmap-five-extreme 180 1 0
```

Arguments after the band are output prefix, time limit in seconds, whether to
save the trace, and the positive-control scale (zero means the 154 target).
A slower machine can use a longer time limit; the trace is deterministic when
completed. The exact trace hashes are in `trace_manifest.json`.

A raw trace record contains five little-endian fields, without padding:
`direction:uint32, y:uint32, word:uint32, positive_mask:uint64,
negative_mask:uint64`, for a total of 28 bytes. The x-coordinates represented by
a word are `xmin + 64*word + bit`. Each mask requests elimination of the
corresponding sign on zero rows. The opposite sign must have empty support
before that elimination. Rows with nonzero boundary right-hand side are not
eliminated by this rule. The final row is identified in the accompanying JSON.

The supplied records were generated on a little-endian platform. Reproduction
on a big-endian system should explicitly serialize these fields little-endian.

## Positive and checkpoint controls

`positive_control_search.json` uses the same five-level lattice and rotated
bitmap implementation on a triangle twice the size of the tile. Exactly four
placements survive. `positive_control_remaining.txt` contains them, and
`check_positive_bitmap.py` independently checks exact side lengths,
containment, total area, all six pairwise non-overlap tests, and boundary
currents. Removing or duplicating a tile is rejected. To reproduce:

```sh
/tmp/634-bitmap-rotated -1 3 /tmp/634-bitmap-positive-four 30 1 2
python3 research/final-closure-oct8/154-cpsat/check_positive_bitmap.py /tmp/634-bitmap-positive-four
```

The earlier scalar checkpoint implementation was also interrupted after
nonzero progress and resumed; its complete forcing-row trace was byte-for-byte
identical to a fresh run. See `resume_verified.json`. The scalar code and
restricted-pool experiments are retained as development history; neither is
needed to reproduce the final bitmap certificates.
