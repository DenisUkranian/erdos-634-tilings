# Erdős 634: positioned-current obstruction for a restricted 154 candidate

**Full problem status: unresolved. N=154 and N=4830 are not decided.**

Read `PROOF.md` first. The proved result is that a tiling of the
`(91,91,154)` triangle by `(8,7,13)` tiles would require at least **three**
short-edge direction classes modulo 60 degrees. The computed part excludes
all 873,496 contained placements in the complete adjacent-height lattice.
The arithmetic result is exact infeasibility even for nonnegative real
weights in that dictionary; it is not an inference from a stopped search.

## Requirements

Python 3, NumPy, SciPy, and GNU g++ supporting C++17. The binary interchange
is little-endian (checked by the replay wrapper). No network access,
commercial optimizer, or external repository checkout is required.
Generated matrix and binary working files use a few hundred MB of disk.
Peak memory can be substantially larger during sparse-matrix construction.
Do not use Python `-O`: these scripts reject optimization because their
exact checks include assertions.

## One-command independent replay

From an extracted copy of this directory:

```sh
python reproduce.py
```

This regenerates the complete dictionary and matrix, runs independent
geometry and matrix audits, exports integer CSR data, decompresses the
retained proof, compiles the independent C++ verifier, replays it, and runs
the positive construction control. It writes fresh JSON reports and a
`REPLAY_RESULT.json`. All outputs stay in this extracted working directory.

Expected key results:

- Gamma anchors: 56,183; orientation variants: 24.
- Contained placements: 873,496.
- Matrix: 550,333 rows, 19,222,288 signed entries.
- Retained proof: 678,493 forced assignments.
- Contradiction: row 70104, residual 1 outside [-1,0].
- Positive control: known 88-tiling, 3,828 exact pair checks.

`twolevel154_steps.txt.gz` is the proof object. It records only integer
triples `(variable, forced_0_or_1, row)`. `verify_twolevel.cpp` recomputes all
row bounds from scratch for each step. It does not run an optimizer and
does not import the producer algorithm.

## Optional rediscovery

After the matrix and binary data have been generated:

```sh
g++ -O2 -std=c++17 propagate.cpp -o propagate
./propagate
python prune_certificate.py
./verify_twolevel
```

The producer generates 869,546 assignments. Pruning removes premises which
are unnecessary for the selected contradiction, leaving the retained proof.
The final replay, not the producer exit status, is the certificate check.
To repeat pruning from a fresh full transcript, remove any previous
`twolevel154_steps_full.txt` first; the script otherwise uses that saved
original full transcript.

## Files

- `PROOF.md`: lemmas, computer-assisted theorem, dependencies and limitations.
- `twolevel154_build.py`: exact complete placement dictionary.
- `independent_geometry_check.py`: independent Cartesian integer enumeration.
- `twolevel154_matrix.py`: positioned signed-boundary matrix.
- `audit_matrix.py`: separate lattice-coordinate reconstruction of every entry.
- `export_sparse.py`: integer sparse arrays for C++ replay.
- `verify_twolevel.cpp`: independent exact proof replay.
- `propagate.cpp`, `prune_certificate.py`: proof discovery/compression.
- `positive_controls.py`: known positive 88-tiling and malformed controls.
- `reproduce.py`: reproducible verification pipeline.
- JSON reports and `SHA256SUMS.txt`: frozen observations/integrity records.

No precomputed matrix, native executable, or third-party font/library is
redistributed. The matrix is regenerated from the small exact description.
The numerical geometry is specific to 154; it is not a universal height
bound. No GitHub repository or other external resource is modified by
these programs.
