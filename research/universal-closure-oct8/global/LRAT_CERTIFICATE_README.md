# Reproducing the completed 135 certificate

The full theorem and all mathematical dependencies are in
[GLOBAL_135_PROOF.md](GLOBAL_135_PROOF.md). The result is **135 impossible**
and **15m² realizable if and only if m >= 4**. It does not classify all N.

## Check the supplied propositional certificate

The separate archive contains the complete compressed LRAT proof and CNF,
the endpoint model, its coordinate dictionary and metadata, the unchanged
upstream `lrat-check.c`, logs and SHA-256 manifests. Its compressed proof
is about 361 MiB. No SAT solver is needed to check an existing certificate.
In the extracted directory, with a C compiler and zstd installed:

```sh
sha256sum -c SHA256SUMS
zstd -d e135-k7.cnf.zst
zstd -d e135-k7-direct.lrat.zst
gcc -O3 lrat-check.c -o lrat-check
./lrat-check e135-k7.cnf e135-k7-direct.lrat
```

Accept only exit status zero together with `c VERIFIED`. The checker must
derive the empty clause, not merely read a valid proof prefix.
The uncompressed SHA-256 values are:

```text
CNF:  5eba9cd04914c8cc9ee9e7ca6299ee8a90f766b6cbf11c9e17c09c2a2e13c54d
LRAT: 78953bc1c44275f878eb2428454a3476042de1ae4b247dd5a8f77e2ee27a704a
```

The CNF has 5,925,966 variables and 12,154,716 clauses. The LRAT contains
1,944,819,324 bytes. The original file was checked once as a complete
stream and again directly from the finished file. The second run took
37.97 seconds wall time and a peak of 498,048 KiB resident memory in this
environment. About 3 GiB of free disk space is sufficient for the supplied
compressed files plus the uncompressed CNF and proof; allow 4 GiB for margin.

## Check geometry, the exported equations, and the encoding

From the repository root, set `CERT` to the extracted archive's absolute
directory and decompress its model and geometry:

```sh
zstd -d "$CERT/e135-k7-center.model.txt.zst"
zstd -d "$CERT/e135-k7-center.geometry.txt.zst"
zstd -d "$CERT/e135-k7-center.remaining.txt.zst"
python3 research/universal-closure-oct8/e135/check_unit_metric_model.py \
  "$CERT/e135-k7-center.geometry.txt" "$CERT/e135-k7-center.model.txt" \
  "$CERT/geometry-model-checked.json" --reference-prefix "$CERT/e135-k7-center"
```

This independently checks the exact tile metrics, target containment,
uniqueness, physical pool hash, and every positioned endpoint equation.
The written and finite implementation checks of the encoding are in
[the SAT audit](../overlap-literature/SAT_AUDIT.md). Install its documented
`python-sat==1.9.dev15` dependency, then regenerate the CNF:

```sh
python3 research/universal-closure-oct8/overlap-literature/check_sat_encoder.py
python3 research/universal-closure-oct8/e135-residual/sat_certificate.py encode \
  "$CERT/e135-k7-center.model.txt" "$CERT/e135-regenerated.cnf"
sha256sum "$CERT/e135-regenerated.cnf"
```

The regenerated CNF must have the exact hash displayed above. Set
`ERDOS_PYSAT_PATH` for a nonstandard python-sat installation when running
the small encoder audit. The encoder itself uses the active Python import
path normally.

## Regenerate the exhaustive geometric reductions

The proof needs the complete nine-height bands, not only the smaller
reference pool. The historical seven-height metadata in the archive
identifies that reference dictionary; its old `equilateral_135_decided:false`
field is not the status of the completed nine-height proof.

Set `WORK` to an absolute working directory. The following generates and
independently replays all five complete bands, removing each large raw
range trace after its successful replay:

```sh
python3 research/universal-closure-oct8/global/reproduce_e135_reduction.py "$WORK"
python3 research/universal-closure-oct8/e135/normalize_pools.py \
  --reference "$CERT/e135-k7-center" --output "$WORK/normalized.json" \
  "$WORK/e135-rle-k9-center" "$WORK/e135-rle-k9-offset1" \
  "$WORK/e135-rle-k9-offset2" "$WORK/e135-rle-k9-offset3" "$WORK/e135-rle-k9-edge"
python3 research/universal-closure-oct8/global/check_e135_pool_embedding.py \
  --manifest "$WORK/normalized.json" --output "$WORK/embedding-checked.json"
```

The five dictionaries contain 2,102,004,892,515 placements before reduction.
All 250,744,655 range cuts must pass independent replay. The normalization
then checks that every survivor and reflection belongs to the same physical
246,600-triangle pool. The raw traces total about 5 GB if `--keep-traces`
is requested. They are reproducible outputs, not extra files required to
check the supplied LRAT. The global no-gap and height-bound arguments remain
mathematical premises, with their own separately checked small cell bounds.

## Regenerate a new proof

Fixed upstream source revisions and build commands are recorded in
[DIRECT_LRAT_SOURCE_AUDIT.md](DIRECT_LRAT_SOURCE_AUDIT.md). With native
CaDiCaL 3.0.0 and the independent checker built:

```sh
python3 research/universal-closure-oct8/global/reproduce_direct_lrat.py \
  "$CERT/e135-k7.cnf" "$WORK/e135-new" \
  --cadical /absolute/path/to/cadical --checker /absolute/path/to/lrat-check \
  --seconds 2400
```

The observed native solver run took 998 seconds wall time, 995.79 seconds
CPU time, and at most 4,341.67 MB resident memory. Allow 8 GiB RAM for
comfortable regeneration. Times are observations on this environment,
not universal runtime guarantees. A timeout leaves the outcome unverified.
The extra Boolean DSU presolve, RoundingSAT attempt and earlier DRAT proof
are not needed for this completed certificate route.
