# Endpoint certificates for the equilateral target of side 231

The two independent forward replays pass. Each one certifies a contradiction for its stated range of short-edge orientations, with arbitrary tile translations. The separate reduction in `../INDEPENDENT_REDUCTION.md` gives the shape, the orientation ranges and the symmetry that handles the reflected side band. The two binary proofs require about 776 MB together. The exact source and SHA-256 checks below regenerate them locally.

## Inference verified

For each physical line, add the oriented interval chains of the counterclockwise edges of all tiles on that line. Their sum is the exterior side on the line or zero. Internal seams cancel after subdivision at each endpoint, including T-junctions. Taking interval endpoints, with start coefficient +1 and end coefficient −1 by convention, gives a separate signed equation at each point and line direction.

At a point and direction of zero exterior demand, if every whole contained tile placement that could contribute an end has already been ruled out, every placement that contributes a start is forbidden. Interchanging the two signs gives the other rule. At a target vertex with a required exterior sign, forbidding every placement of that sign is a contradiction. Over a fixed orientation range the candidate list at one endpoint is exhaustive even for arbitrary real translations: matching that vertex to the endpoint fixes the translation.

One packed record specifies up to 64 physical endpoint equations and sign choices. For each bit the forbidden placements are given explicitly by a finite parametric rule: for each oriented shape with a matching signed incidence, translate that vertex to the designated endpoint. The verifier checks all possible opposite signed placements for geometric containment and prior elimination. It derives candidate translations from shape vertices and computes containment by translating the target's three supporting half-planes inward. It has no access to the original trace, producer's state, timestamps, or any candidate counts. Bitmap words implement 64 exact Boolean decisions at once.

The separate producer first records a complete zero-support propagation trace. The backward extractor starts with all geometrically possible placements required by the target at the contradicted corner. It walks the trace backwards, retaining endpoint deductions required by the pending placements and registering every possible premise of each deduction. The resulting certificate stores its records in reverse chronological order. A retained row can forbid additional placements simultaneously. This is a dependency-selected proof and carries no minimality claim.

Each record is little-endian `<IIIQQ`, consisting of a direction index, a y scanline index, an x word index, a start mask and an end mask. Coordinates are axial. Indices of x and y are measured from the target's smallest respective coordinates. Bits correspond to increasing x. Direction and shape order are defined by the loops in the verifier. The exact integers are bounded by the geometry of these two finite instances. Use a little-endian Linux C++17 environment.

| Short-height range | Packed deductions | Individual endpoint deductions | Exact proof size in bytes | Required target incidence |
|---|---:|---:|---:|---|
| $[0,2]$ | 13,601,241 | 346,727,411 | 380,834,748 | $(-7623,9240)$, axis $(40,-7)$, end |
| $[-1,1]$ | 14,129,619 | 354,827,395 | 395,629,332 | $(0,8547)$, axis $(0,1)$, start |

## Reproduction

From this directory, run these commands sequentially in a fresh working directory. `make_trace.cpp` is the packed zero-support enumerator used for the recorded source traces. The 600-second limits on that *producer* are operational only. If a machine reaches its limit, increase it until the reported corner contradiction is found. The verifier has no proof-search timeout.

```sh
src="$PWD"
work=$(mktemp -d)
cd "$work"
c++ -O3 -std=c++17 "$src/make_trace.cpp" -o make_trace
c++ -O3 -std=c++17 "$src/extract.cpp" -o extract
c++ -O3 -std=c++17 "$src/verify.cpp" -o verify
./make_trace 0 2 side 600 1 0
./make_trace -1 1 center 600 1 0
./extract 0 2 side 2 9240 0
./extract -1 1 center 7 8547 0
sha256sum -c "$src/SHA256SUMS.txt"
./verify 0 2 side.backtrace.bin 2 40 -7 1
./verify -1 1 center.backtrace.bin 2 0 1 0
```

Negative control for either full proof exchanges the sign masks of its first chronological inference, preserving every other byte. Both mutated proofs were rejected at inference 1 because a matching opposite-sign placement remained available. The verifier returned status 1 for each mutation.

```sh
python3 "$src/mutate.py" side.backtrace.bin bad-side.bin
python3 "$src/mutate.py" center.backtrace.bin bad-center.bin
./verify 0 2 bad-side.bin 2 40 -7 1
./verify -1 1 bad-center.bin 2 0 1 0
```

The proof status is an internally replayed computational result with a separate certificate verifier. The checks do not establish priority, external peer review, or a Lean formalization.
