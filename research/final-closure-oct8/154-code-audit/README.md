# Independent source and arithmetic audit of the five-height bitmap refutations

8 October 2026. This is an internal independent review of the finite-band
positioned-boundary computation. It is not external mathematical refereeing
or proof-assistant formalization. The large certificate traces are checked
separately by `../154-audit/replay_bitmap.cpp`; this audit does not replace
that replay or the global height/population reductions.

## Result

The entire `bitmap_zero_rotated.cpp` producer and the separately written
`replay_bitmap.cpp` verifier were read. No gap or unsound elimination was
found in the lattice coordinates, orientation completeness, containment,
endpoint-current signs, zero-support propagation, bitmap shifts, or
terminal contradiction test.

The independent program `check_bitmap_arithmetic.py` additionally:

* extracts the **actual read/erase C++ lambdas** from the producer, and
  compares them with direct per-bit operations in 442,476 cases compiled
  with undefined-behavior sanitization;
* independently counts every valid placement by eroding the three target
  halfplanes by the three template vertices, instead of intersecting
  precomputed shifted scanline intervals;
* checks all template side norms, oriented areas, and lattice scale factors.

Every check passes. The report `arithmetic_audit.json` records the exact
source SHA256 hashes and the count for each of the sixty orientations.

| Height band | Basis rotation | Independently counted placements |
|---|---:|---:|
| `[0,4]` | 1 | 4,759,540,301 |
| `[-1,3]` | 1 | 4,770,414,013 |
| `[-2,2]` | 0 | 4,773,371,018 |

These match the production runs. The centered run used the unrotated
producer. The rotated version may choose a different bounding rectangle
for that band; rotating the entire integer Eisenstein lattice preserves
all placement counts.

## Why the geometric enumeration is complete

Set `eta=3+rho`, `bar(eta)=4-rho`, so

```
eta*bar(eta)=13, eta²=8+7rho, z=eta/bar(eta).
```

The previously proved integer-atom/extreme-edge lemma places every vertex
of a tiling supported on `[L,U]` in

```
Lambda = sum_(h=L)^U z^h Z[rho].
```

For `g=eta^L/bar(eta)^U`, multiplication by `1/g` sends every generator
`z^h` to the integer Eisenstein vector

```
eta^(h-L) bar(eta)^(U-h).
```

Thus the program's integer grid contains **every possible vertex**. This
inclusion alone is sufficient for a negative result. In fact equality
holds by the Bezout identity recorded in the separate lattice proof.
No assumption about an initially chosen placement mesh is involved.

Multiplication by an additional `rho^r` is an invertible integer lattice
map and a rotation, so the bounding-box optimization preserves candidates.
For width four every transformed unit direction has norm squared
`13^4=28561`, as does the multiplier applied to the target.

Each tile has a unique 120-degree vertex. Its two adjacent sides have
lengths 8 and 7, in either order, with directions differing by 120 degrees.
The six rotations and two orders therefore enumerate all twelve possible
orientations at each allowed height, including reflections. All translates
whose three vertices lie in the target are retained. Convexity makes that
vertex test exactly equivalent to containment of the entire triangle.

The scanline bounds use the counterclockwise target inequality

```
dx*(y-ay)-dy*(x-ax) >= 0.
```

Positive dy yields an upper floor bound for x; negative dy yields the
corresponding lower ceiling bound. Both denominators passed to the integer
floor/ceiling helpers are positive. Zero dy is handled as a constant
inequality. The independent audit counts the equivalent eroded target
without using these shifted scanlines: for anchor p and template vertices v,
all inequalities reduce to

```
cross(e,p) >= max_v cross(e,a-v)
```

for each target edge a->a+e.

## Endpoint equations and soundness of elimination

For each exact point p and unoriented supporting direction d, a row records
+1 at the starting endpoint and -1 at the ending endpoint of every
counterclockwise oriented tile edge on that line. Reversing an edge swaps
its endpoint signs. The row is precisely the derivative of its signed
one-dimensional edge current; **no additional direction-dependent sign or
edge-length multiplier is needed**.

Equal endpoint data on every supporting line implies equal edge currents:
their difference has zero derivative, is constant on that line, and is zero
outside its bounded support. Conversely equal currents have equal endpoint
data. This accommodates T-junctions because subdivision introduces one
positive and one negative endpoint contribution at the same point.
Consequently every actual tiling satisfies the finite linear equations

```
B x = boundary(target), x >= 0.
```

For a zero right-hand-side row, if no still-available variable has a
negative coefficient, every variable with a positive coefficient must be
zero. The same assertion holds after exchanging signs. The bitmap program
applies only these valid zero-support deductions. Its proof does not need
an integrality assumption, binary upper bounds, or a separate nonoverlap
condition.

At each of the six nonzero target endpoint rows, the producer deliberately
disables ordinary zero-row deletion. If the sign required by the target
has no surviving variable, the equation is impossible even when all
opposite-sign variables remain available. This is the terminal contradiction.
Distinct sides of the nondegenerate target have distinct directions, so no
row receives two conflicting target-corner contributions.

All deletions within a word are justified from its support before the
word update. Therefore applying the resulting masks successively to the
incident orientations cannot invalidate their logical justification.

## Bitmap indexing audit

For endpoint offset p, a row at integer coordinate q reads the candidate
anchored at q-p. Write the x-offset as `64s+k`, `0<=k<64`. The producer's
read operation is

```
(word[w+s] >> k) | (word[w+s+1] << (64-k)),
```

with the second term omitted when k=0. Its erase operation distributes a
row mask by the inverse shifts. Out-of-range words and rows read as zero;
padding bits start at zero and are never introduced by deletion. Every
shift amount is between 0 and63; the potentially undefined shift by64 is
explicitly avoided. The per-bit harness tests negative x-offsets, every
residue modulo64, word crossings, masks at the edges, and out-of-range
rows. The tested x-offset range `[-2048,2048]` contains every endpoint
x-offset used by the five-height templates.

The production counts exceed 2^32, but total placements, total removals,
bitmap addresses and counters use 64-bit unsigned integers. The small
coordinates and template products fit signed 32-bit integers for the
accepted bands; determinant products are explicitly promoted to 64-bit.
The program rejects unsupported band widths and oversized index ranges.
Timeouts are separately marked incomplete and cannot trigger a conflict
claim. The independent verifier rechecks the geometric terminal row and
the justified deletion masks rather than trusting the producer's status.

## Reproduction and limits

From the repository root:

```
python3 research/final-closure-oct8/154-code-audit/check_bitmap_arithmetic.py
```

The test builds its small C++ kernel harness in a temporary directory.
It needs Python3 and a C++17 compiler with undefined-behavior sanitizer
support. No multi-gigabyte trace is needed for this arithmetic audit.

To conclude the unrestricted 154 case, separately retain the complete
candidate reduction, the global height-support bound, and all three large
trace replays. This review confirms the correctness of the finite-band
model and its bit operations; it does not substitute those other inputs.
