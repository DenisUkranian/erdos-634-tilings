# Independent review of the direct LRAT acceptance gate

The position-model agent reviewed `global/reproduce_direct_lrat.py`,
`global/direct_lrat_controls.json`, the native CaDiCaL `src/parse.cpp`, and
the separate official drat-trim `lrat-check.c` used by the global auditor.
No acceptance-gate issue was found.

The wrapper accepts only the conjunction of solver exit code 20, checker
exit code 0, and the exact checker line `c VERIFIED`. A solver status alone,
a time limit, or an incomplete proof cannot trigger the accepted status.

CaDiCaL's complete native DIMACS parser reserves all input clause IDs from
the header before adding any clauses (`reserve_ids(clauses)`), and checks
for too many or missing input clauses. This preserves the clause numbering
needed by the independent checker, including input clauses simplified by
the solver. The checker loads the original CNF in its original clause order.

In `lrat-check.c`, `found_empty_clause` is set only after the clause has
passed `checkClause`. Final acceptance requires this flag and absence of
any detected checking error. Merely reaching end of file does not suffice.
The saved controls include valid derivations with input simplification and
negative controls for an empty proof, a wrong hint, and a missing final empty
clause. These checks supplement the source review.

This review concerns the proof interface and final gate. It does not itself
assert that the large E135 run has finished or that its final empty clause
has been checked. The exact binding of the CNF to the geometrical Boolean
model is a separate required encoding audit.
