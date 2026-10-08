# Direct LRAT: the independently checked SAT certificate gate

The geometric reduction and the CNF encoding are separate obligations.
The former is audited in [E135_REDUCTION_AUDIT.md](E135_REDUCTION_AUDIT.md),
with the physical pool-to-endpoint-model link checked by
[check_unit_metric_model.py](../e135/check_unit_metric_model.py).
The latter has a separate [SAT encoding audit](../overlap-literature/SAT_AUDIT.md).
This note concerns checking the resulting CNF contradiction.

## Fixed upstream sources

- CaDiCaL: <https://github.com/arminbiere/cadical>, tag `rel-3.0.0`,
  commit `7b99c07f0bcab5824a5a3ce62c7066554017f641`.
- Independent checker: `lrat-check.c` from
  <https://github.com/marijnheule/drat-trim>, commit
  `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.

The solver was built by `./configure && make -j4`, with its default
`g++ -Wall -Wextra -O3 -DNDEBUG` flags. The separate checker was built by
`gcc -O3 lrat-check.c -o lrat-check`. Neither upstream source was modified.

## Input clause identifiers

The native CaDiCaL DIMACS parser is essential here. Its `src/parse.cpp`
reserves the declared number of original clause identifiers before adding
the clauses. It also checks that the input contains that many clauses.
The independent checker numbers the original clauses consecutively from
one. Thus simplification of a unit, duplicate, or tautological input clause
does not shift the meaning of later LRAT hints.

An initial experiment through the PySAT incremental input interface did
not preserve this correspondence on one control formula. That route was
discarded; the certificate route uses the native CLI parser.

## Acceptance condition

The reproduction driver is [reproduce_direct_lrat.py](reproduce_direct_lrat.py).
It accepts only the conjunction of:

1. Solver exit status 20 (UNSAT).
2. Exit status zero from the separately compiled checker.
3. The checker's exact line `c VERIFIED`.

The checker sets its `found_empty_clause` flag only after `checkClause`
has successfully checked that clause. Its success condition is
`found_empty_clause && !found_error`. A timeout, a prefix that does not
derive the empty clause, or incorrect hints therefore does not pass.

[direct_lrat_controls.json](direct_lrat_controls.json) records four
verified UNSAT controls, including input simplification, together with
three deliberately invalid or incomplete proofs that are all rejected.
It records the complete small input formulas and proof text, source hash,
and binary hashes. A [separate source review](../e135/LRAT_GATE_REVIEW.md)
checks the driver, the native parser's ID reservation, and the checker's
empty-clause gate.

For the large run, the unchanged checker also accepts the proof on standard
input. Feeding it exactly the growing proof file allows proof checking to
overlap the solver run. The stream is closed only after the solver exits;
the byte count must equal the completed proof's size. The final reports
and hashes, rather than a running solver's status, record the outcome.

## Reproduction

After generating the independently audited endpoint CNF, run:

```sh
python3 reproduce_direct_lrat.py /path/e135-k7.cnf /path/e135-direct \
  --cadical /path/cadical/build/cadical \
  --checker /path/lrat-check --seconds 2400
```

The command writes a complete native ASCII LRAT file, solver and checker
logs, and a report binding the checked contradiction to the input CNF and
proof by SHA-256. A certificate checker does not trust the SAT search or
its UNSAT announcement.
