# Bounded LP attempt for the 135 endpoint model

8 October 2026. **INCOMPLETE: no feasibility or nonexistence conclusion.**

`probe.py` loaded the residual endpoint model with 246,600 Boolean variables
relaxed to the intervals `[0,1]`. It retained all247,770 signed equality rows
and added the explicit tile-count equation `sum(x)=135`. The resulting LP
has247,771 rows and1,726,200 nonzeros.

HiGHS1.15.1, one thread, dual simplex with presolve, reached its180-second
limit after19,584 iterations. It produced neither a feasible solution nor
an infeasibility certificate. The retained `simplex_report.json` explicitly
records that limitation. No rank, rounding, or apparent numerical
infeasibility is interpreted as an exact negative result.

If an infeasible future run supplies a dual ray, the script attempts common-
denominator integer rounding and tests the exact interval Farkas inequality

    y·b > sum_j max((B^T y)_j, 0).

Only a strict inequality replayed with checked, nonoverflowing integer
arithmetic is saved as an exact certificate. That branch was not reached in
this run. Such a certificate would apply to the input residual pool; its
geometric completeness and exact soundness of all earlier deletions require
the separate universal-model proof.

Reproduce after generating the source model:

    python3 research/universal-closure-oct8/e135-lp/probe.py /tmp/e135-k7-center.model.txt /tmp/e135-universal-lp --seconds 180

Dependencies are NumPy, SciPy and highspy. The optional
`ERDOS_CERT_SOLVERS_PATH` points to their isolated installation directory.
