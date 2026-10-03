# W and beta caps

This package proves and checks an exact six-block collar for every coprime
`0<u<v`, giving W/beta realizability at every scale in `v+<u,v>` and hence
every integer `m>=uv-u+1`. Read `PROOF.md` for the universal argument and
its limits. No necessity is claimed outside that semigroup.

Everything runs with standard-library Python; no external packages are
required.

```sh
python run_checks.py
python run_checks.py --output fresh-replay.json
python generate.py 2 3 5 --output examples/W_u2_v3_m5.json
python verify.py examples/W_u2_v3_m5.json
python generate.py 1 2 3 --output examples/W_u1_v2_m3.json
python verify.py examples/W_u1_v2_m3.json --expand
python generate.py 2 3 --kind cap
python generate.py 2 3 1 --kind shell --family beta
python check_symbolic.py
```

The generator returns rational-coordinate triangular/parallelogram grid
certificates. The independent checker verifies the complete target by exact
metric and polygon arithmetic. `--expand` additionally checks every unit
tile and every pair; use it only for small examples. `verification.json`
records the exact regression scope and deliberate corruptions rejected.
The optional `--output` writes a fresh report at the requested path while
preserving the package's saved examples, default report, and manifest.

The main threshold replaces the older `S0+(u-1)(v-1)` sufficient W/beta
threshold with `v+(u-1)(v-1)`. For `(u,v)=(2,3)` it supplies scales
`3,5,6,7,...`; it does not decide scale `4`. The tile count is `Qm²` for
W and `Pm²` for beta, where `Q=2v²-u²` and `P=3v²-u²`.

The triquadratic seed is credited to Beeson, as in the existing saturation
package. The cap and its proof are project-internal research; research
priority and external acceptance are not asserted. Erdős 634 remains open
within this package's stated scope.
