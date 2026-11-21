#!/usr/bin/env python3
"""Produce native Z3 SAT DRAT for a CNF and independently check it.

Only a complete successful replay is a refutation. A solver timeout or a
proof whose input prefix this checker cannot align is explicitly inconclusive.
"""
import argparse
from ctypes import CDLL, c_char_p, c_void_p
import hashlib
import json
from pathlib import Path
import time

from check_drat import check_files, check_with_propagation, propagate_inputs, read_dimacs, rup


def solve_cnf(cnf_path, proof_path, timeout_ms=60000):
    variables, clauses = read_dimacs(cnf_path)
    # Independently propagate before involving the solver. This also handles
    # syntactically false inputs which the SAT tactic may simplify immediately.
    if rup(set(map(frozenset, clauses)), ()):
        with Path(proof_path).open('w') as out:
            for clause in clauses:
                out.write('i ' + ' '.join(map(str, clause)) + (' ' if clause else '') + '0\n')
            out.write('0\n')
        result = check_files(cnf_path, proof_path)
        result.update(producer='Exact initial unit propagation', solver_status='unsat')
        return result
    # Eliminate input units ourselves. Native SAT can substitute an asserted
    # variable by its internal true literal before emitting i-records. Sending
    # the exactly reduced nonunit CNF avoids trusting that preprocessing.
    reduced, fixed = propagate_inputs(clauses)
    reduced_path = Path(str(proof_path) + '.propagated.cnf')
    with reduced_path.open('w') as out:
        out.write(f'p cnf {variables} {len(reduced)}\n')
        for clause in reduced:
            out.write(' '.join(map(str, clause)) + (' ' if clause else '') + '0\n')
    clauses = reduced
    z = CDLL('libz3.so.4')
    z.Z3_mk_config.restype = c_void_p
    z.Z3_mk_context.argtypes = [c_void_p]
    z.Z3_mk_context.restype = c_void_p
    z.Z3_eval_smtlib2_string.argtypes = [c_void_p, c_char_p]
    z.Z3_eval_smtlib2_string.restype = c_char_p
    z.Z3_del_context.argtypes = [c_void_p]
    context = z.Z3_mk_context(z.Z3_mk_config())

    def call(source):
        return z.Z3_eval_smtlib2_string(context, source.encode()).decode().strip()

    start = time.monotonic()
    version = call('(get-info :version)')
    path = str(Path(proof_path).resolve())
    if '"' in path or '\\' in path:
        raise ValueError('Use a plain proof path')
    call(f'(set-option :timeout {timeout_ms})\n'
         f'(set-option :sat.drat.file "{path}")\n'
         '(set-option :sat.drat.binary false)\n'
         '(set-option :sat.cardinality.solver false)\n'
         '(set-option :sat.pb.solver circuit)')
    call('\n'.join(f'(declare-const b{i} Bool)' for i in range(1, variables + 1)))
    batch = []
    for clause in clauses:
        literals = [f'b{x}' if x > 0 else f'(not b{-x})' for x in clause]
        term = literals[0] if len(literals) == 1 else '(or ' + ' '.join(literals) + ')'
        batch.append('(assert ' + term + ')')
        if len(batch) >= 1000:
            call('\n'.join(batch))
            batch = []
    if batch:
        call('\n'.join(batch))
    status = call('(check-sat-using sat)')
    z.Z3_del_context(context)
    result = dict(solver_status=status, solver_version=version,
                  seconds=round(time.monotonic() - start, 6),
                  producer='Z3 native SAT ASCII DRAT',
                  cnf_sha256=hashlib.sha256(Path(cnf_path).read_bytes()).hexdigest())
    if status != 'unsat':
        result['status'] = 'NO_REFUTATION'
        return result
    result.update(check_with_propagation(cnf_path, reduced_path, proof_path))
    result['exactly_reduced_cnf'] = reduced_path.name
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('cnf', type=Path)
    parser.add_argument('proof', type=Path)
    parser.add_argument('--timeout-ms', type=int, default=60000)
    args = parser.parse_args()
    result = solve_cnf(args.cnf, args.proof, args.timeout_ms)
    print(json.dumps(result, sort_keys=True))
    if result['status'] != 'VERIFIED_UNSAT':
        raise SystemExit(2)


if __name__ == '__main__':
    main()
