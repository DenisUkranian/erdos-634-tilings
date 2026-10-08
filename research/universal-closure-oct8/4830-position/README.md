# A positive 480-tile corner certificate, completing the 4830 construction

The convex quadrilateral, in Eisenstein coordinates with
`rho = exp(i*pi/3)`,

```
Q = [(22,0), (528,0), (-242,242), (-48,48)]
```

has a tiling by **480 congruent triangles with sides (24,11,31)**.
The explicit rational-coordinate certificate is `q480_tiling.json`.
Its common coordinate denominator divides 31. The norm of `(x,y)` is
`x*x+x*y+y*y`.

This is the 22-fold ordinary tile triangle minus a reflected 2-fold
corner triangle. The companion construction in `../f3-general/` embeds
Q into an F3 target and supplies the other 4350 tiles. Consequently
the positive certificate here completes a 4830-tile construction.
Excluding a particular Q construction would not have excluded 4830;
the result is positive and does not need such a converse.

## Direct verification

Run, using only Python's standard library:

```
python check_q480.py
```

This checks all 480 triangles for exact side lengths, positive area,
containment, equality of oriented boundary currents, and all **114960**
unordered pairs for disjoint interiors using rational arithmetic. The
area sum equals the quadrilateral area. This check does not invoke the
enumerator, compression code, or a solver. The PASS report from the
initial check is `q480_verified.json`.

## Discovery and reproducibility

The two short-edge heights are -1 and 0 for
`z=(24+11*rho)/31`. Put `eta=5+rho`, so `z=eta/conj(eta)`.
Multiplication by `rho*eta` gives integral working coordinates.

The complete two-height lattice enumeration had **35300834** contained
placements. Endpoint-current zero-support propagation reduced this to
648 placements. Ordinary zero/one row bounds forced 334 of these;
the other 314 joined into five equality components with sizes
84,62,22,84,62. The resulting exact five-variable system has three
Boolean solutions. The certificate uses `(0,1,0,1,0)`.

The survivor list is `q480_band_survivors.txt`. The compressed model,
placement mapping, and report are `q480_residual.pbtxt`,
`q480_residual.mapping.bin`, and `q480_residual.json`. The binary mapping
has native little-endian int32 records `(group,orientation,x,y)`, where
group -1 denotes a forced placement. `decode_q480.py` exhausts the 32
Boolean assignments, decodes a solution, and repeats the geometric
checks. These small files preserve the discovery independently of
large search traces.

To recreate the complete enumeration and reductions in a temporary
directory (requires a C++17 compiler):

```
g++ -std=c++17 -O3 bitmap_q480.cpp -o /tmp/q480-bitmap
g++ -std=c++17 -O3 packed_q480.cpp -o /tmp/q480-packed
g++ -std=c++17 -O3 compress_q480.cpp -o /tmp/q480-compress
/tmp/q480-bitmap -1 0 /tmp/q480-band 60 0
/tmp/q480-packed -1 0 /tmp/q480-rows 60 0 0 /tmp/q480-band.remaining.txt
/tmp/q480-compress -1 0 /tmp/q480-compressed 60 0 0 /tmp/q480-rows.survivors.bin
```

The positive geometric certificate is sufficient even without trusting
the completeness of these search reductions. Further checks of the
completed 4830 target are documented in the companion construction
folder.

## A simple visible subregion

The 124 tiles of height -1 form one parallelogram, with vertices

```
[(-242,242), (-180,180), (205,59), (143,121)].
```

For `u=(35-11*rho)/31`, let `v1=11*u` and `v2=24*rho^2*u`.
Its sides are `2*(v1-v2)` and `31*v1`. Thus it has the elementary
2-by-31 grid construction with two tiles in every parallelogram cell.
The other 356 tiles all have short height zero.

## Earlier search branches

Files with `q792` refer to the larger sufficient corner Q792 attempted
before Q480 was identified. They produced no construction and no
global negative result. The positive Q480 certificate supersedes those
searches for the purpose of constructing 4830. Reports for rejected
one-height Q480 and the other adjacent two-height band are retained
as search records; no negative theorem relies on those reports here.
