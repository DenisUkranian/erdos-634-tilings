# Independent audit of the signed-row SAT translation

8 October 2026. **PASS for the translation inspected.** This audit does not
certify the geometric pool's completeness or replay the SAT solver's DRAT
proof; those are separate obligations.

The inspected implementation is
`../e135-residual/sat_certificate.py`, with installed `python-sat 1.9.dev15`.
The endpoint export uses Boolean variables x_j and equations

    sum_(positive z) x_(z) - sum_(negative z) x_(-z) = b.

For a negative literal, its Boolean truth value is `1-x_(-z)`. Therefore
this equation is exactly the cardinality equation on the signed literals
with target `k=b+number_of_negative_literals`. The implementation uses this
value, with no sign reversal or missing constant.

For k outside `[0,n]`, an empty clause is correct. For k=0 and k=n, the unit
clauses are correct. For `n<=5`, forbidding every simultaneously true
`(k+1)`-subset supplies the upper bound, and requiring at least one true
literal in every `(n-k+1)`-subset supplies the lower bound. Their conjunction
is exactly equality, including repeated literal positions if ever present.

For larger rows, `CardEnc.equals(..., encoding=seqcounter)` introduces an
existential cardinality encoding. The global top identifier starts at the
number of original variables. Each call receives the current top and then
advances it to at least the returned `enc.nv`. The installed Python wrapper
was also inspected: its at-least and at-most subcalls use successive top
identifiers, and its returned nv is their maximum. Thus auxiliary variables
are disjoint from all original variables, all earlier counters, and the
other half of the same equality counter. No independence of the *original*
variables across rows is assumed.

The source exporter `final-closure-oct8/154-cpsat/endpoint_pool.cpp` subtracts
the contributions of forced assignments from each row's right side before
writing residual literals. The encoder correctly skips the following
`nv+nsel` placement-metadata records and reads the remaining signed rows.
The source rows are asserted to use only original IDs `1..nv`. An additional
independent scan of the actual model found 246,600 variables, 247,770 rows,
1,479,600 nonzeros, maximum row width24, and no repeated variable in any row.

For the current negative-proof route, omitting the optional tile-count row
is sound: every true tiling still satisfies all retained rows. A refutation
of this relaxation suffices. A satisfiable relaxation alone would not be
reported as a tiling.

## Independent finite replay

`check_sat_encoder.py` calls the inspected encoder and then uses **Glucose3**,
not the producing CaDiCaL solver, to test every assignment in the retained
small cases. It checks all row sizes 0 through 9, all bounds from -1 through
n+1, three sign patterns, DIMACS counts and identifier bounds, and a pair of
overlapping large rows whose independent auxiliary counters must coexist.

The replay checks **216 cases and 37,871 assignments** and returns PASS.
The universal claims about the sign shift, combinatorial clauses and namespace
separation are established by the written argument; the finite replay is an
additional implementation check, not an extrapolation proving arbitrary n.

    python3 research/universal-closure-oct8/overlap-literature/check_sat_encoder.py

The module location defaults to `/tmp/erdos634-cert-solvers` and can be set
through `ERDOS_PYSAT_PATH`. The retained report is `sat_encoder_checked.json`.
