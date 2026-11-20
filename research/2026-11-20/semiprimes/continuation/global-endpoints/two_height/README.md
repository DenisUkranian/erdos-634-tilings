# Full two-height catalogue: an inconclusive experiment

These sources enumerate every placement in the two-height lattice and apply
necessary corner-fan and straight-line bank filters. They do not solve exact
cover. A nonempty fixed point is OPEN.

The mathematical and integer-width review is in
[the independent audit](../AUDIT_TWO_HEIGHT.md). The normalization covers all
real translations for a genuine tiling with at most two short heights. The
`check_native.cpp` option imposes additional residue classes and has narrower
scope.

| Run | Initial placements | Final result |
|---|---:|---|
| 143 full catalogue | See regenerated control | OPEN with 371 placements; all 143 known tiles retained |
| 3431 full catalogue | 311,334,312 | OPEN with 128,146,772 placements |
| 3431 selected native phases | Restricted subcatalogue | OPEN with 1,951,119 placements |
| 5063 full catalogue | See partial log | Interrupted; no final result |

The 3431 full run completed 50 sweeps, numbered 0 through 49. Its nonempty
fixed point is not evidence of a positive tiling. The last line of the partial
5063 log is not a fixed-point certificate.

Generate the inputs and replay the known positive control:

```sh
python make.py
python control143.py
c++ -O3 -std=c++20 check.cpp -o check
./check board143.known < board143.in
```

The full target commands use `board3431.in` and `board5063.in`. They are large
computations and are deliberately excluded from the short package replay.
Recorded logs accompany the source; they are computational history, not
tiling or nonexistence certificates. The control's macro certificate is
copied from the existing project staircase package with its original data.
