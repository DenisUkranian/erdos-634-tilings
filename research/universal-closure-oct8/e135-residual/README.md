# Residual135 Boolean encoding

The completed result is the [global135 proof](../global/GLOBAL_135_PROOF.md).
Its final negative certificate is **native LRAT**, verified separately in
full. The optional binary-DRAT route in this folder was an earlier attempt;
its unfinished proof-checking runs are not premises of the theorem.

`sat_certificate.py encode` translates the exact signed endpoint rows into
CNF. The retained formula has 5,925,966 variables and 12,154,716 clauses.
No explicit135-count constraint is added in this run: impossibility of the
weaker boundary system is sufficient. The [separate encoder audit](../overlap-literature/SAT_AUDIT.md)
gives the mathematical sign conversion, auxiliary-variable separation,
inspection of the actual row structure and independent finite replay.

The run used `python-sat==1.9.dev15`. In a Python environment with that
version installed, use:

```sh
python research/universal-closure-oct8/e135-residual/sat_certificate.py encode /path/e135-k7-center.model.txt /path/e135-k7.cnf
python research/universal-closure-oct8/global/reproduce_direct_lrat.py /path/e135-k7.cnf /path/e135-direct --cadical /path/cadical/build/cadical --checker /path/lrat-check --seconds 2400
```

The [source audit](../global/DIRECT_LRAT_SOURCE_AUDIT.md) pins the two C/C++
program versions and records the acceptance gate. The [final report](../global/direct_lrat_certificate.json)
binds the model, CNF, full proof and checking logs by SHA-256. The
[geometric reproduction](../global/E135_REDUCTION_AUDIT.md) constructs and
independently checks the complete position reduction feeding this model.

Use ordinary Python with assertions enabled. A timeout, UNKNOWN or an
unfinished certificate is never interpreted as a nonexistence result.
