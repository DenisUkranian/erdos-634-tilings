#!/usr/bin/env python3
"""Exact positive and deliberately invalid controls for the proof path."""
import argparse
from itertools import product
import json
from pathlib import Path

from proof_cnf import encode_assertions, parse, write_dimacs
from check_drat import ProofError, check_records, check_files, check_with_propagation, read_dimacs, rup

HERE = Path(__file__).resolve().parent


def evaluate(node, assignment):
    if isinstance(node, str):
        return node == 'true' if node in ('true', 'false') else assignment[node]
    operator, *args = node
    values = [evaluate(x, assignment) for x in args]
    if isinstance(operator, tuple):
        actual = sum(int(w)*v for w,v in zip(operator[3:],values)) if operator[1] == 'pble' else sum(values)
        return actual <= int(operator[2]) if operator[1] in ('at-most','pble') else actual == int(operator[2])
    if operator == 'not':
        return not values[0]
    if operator == 'and':
        return all(values)
    if operator == 'or':
        return any(values)
    if operator == '=>':
        return not values[0] or values[1]
    if operator == '=':
        return values[0] == values[1]
    raise ValueError(operator)


def satisfies_by_propagation(clauses, assignment):
    # All input variables fixed: the independently checked gate definitions
    # must determine every auxiliary variable, or reveal a contradiction.
    state = dict(assignment)
    while True:
        changed = False
        for clause in clauses:
            if any(abs(x) in state and state[abs(x)] == (x > 0) for x in clause):
                continue
            free = [x for x in clause if abs(x) not in state]
            if not free:
                return False
            if len(free) == 1:
                state[abs(free[0])] = free[0] > 0
                changed = True
        if not changed:
            assert all(any(abs(x) in state and state[abs(x)] == (x > 0) for x in c) for c in clauses)
            return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replay-only',action='store_true',
                        help='Check frozen CNF/DRAT controls with Python stdlib only; no solver, no file writes.')
    args = parser.parse_args()
    expressions = ['true', 'false', '(not x)', '(=> x y)', '(= x y)',
                   '(and x (or y (not z)))', '(or x (not x))',
                   '(and (= aux (or x y)) (=> aux z))']
    for literals in (['x'], ['x', 'y', 'z'], ['x', '(not x)', 'true', 'false'],
                     ['x', 'x', '(not y)', 'z', 'true', 'false'],
                     ['true', 'false', 'false', 'false']):
        for bound in range(-1, len(literals) + 2):
            body = ' '.join(literals)
            expressions.append(f'((_ at-most {bound}) {body})')
            expressions.append(f'((_ pbeq {bound}' + ' 1' * len(literals) + f') {body})')
    for literals,weights in ((['x','y','z'],[1,2,3]),
                             (['x','(not x)','true','false'],[2,3,4,1]),
                             (['x','x','(not y)'],[1,4,2])):
        for bound in range(-1,sum(weights)+2):
            expressions.append(f'((_ pble {bound} '+ ' '.join(map(str,weights))+') '+ ' '.join(literals)+')')
    formula_count = len(expressions)
    truth_checks = 0
    for expression in expressions:
        encoded = encode_assertions([expression])
        names = sorted(encoded['symbols'])
        for values in product((False, True), repeat=len(names)):
            logical = dict(zip(names, values))
            inputs = {encoded['symbols'][name]: value for name, value in logical.items()}
            assert satisfies_by_propagation(encoded['clauses'], inputs) == evaluate(parse(expression), logical), expression
            truth_checks += 1

    examples = {
        'boolean_square': ['(or x y)', '(or (not x) y)', '(or x (not y))', '(or (not x) (not y))'],
        'cardinality_conflict': ['((_ pbeq 2 1 1 1) x y z)', '((_ at-most 1) x y z)'],
        'owned_fan_conflict': ['root', '(=> root (or owner0 owner1))',
                               '(=> owner0 (and left right))', '(=> owner1 (and left right))',
                               '((_ at-most 1) left right)'],
        'three_pigeons_two_holes': [
            '(or a b)', '(or c d)', '(or e f)',
            '((_ at-most 1) a c e)', '((_ at-most 1) b d f)'],
        'weighted_population_conflict': [
            '(or x y)', '((_ pble 3 4 4) x y)'],
    }
    reports = []
    for name, expressions in examples.items():
        encoded = encode_assertions(expressions)
        cnf, proof = HERE / f'control_{name}.cnf', HERE / f'control_{name}.drat'
        if args.replay_only:
            variables,clauses = read_dimacs(cnf)
            assert variables == encoded['variables']
            assert clauses == list(map(tuple,encoded['clauses'])), 'Frozen CNF differs from independent re-encoding'
            reduced = Path(str(proof)+'.propagated.cnf')
            report = check_with_propagation(cnf,reduced,proof) if reduced.exists() else check_files(cnf,proof)
            report['producer'] = 'Frozen proof replay; no solver used'
        else:
            from run_cnf_proof import solve_cnf
            write_dimacs(encoded, cnf)
            report = solve_cnf(cnf, proof, 10000)
        assert report['status'] == 'VERIFIED_UNSAT'
        report.update(control=name, variables=encoded['variables'], clauses=len(encoded['clauses']))
        reports.append(report)

    # Independent RAT case: start with a satisfiable nonunit clause, add a
    # vacuously RAT fresh-variable clause; it must pass as a prefix but never
    # be mistaken for an UNSAT proof.
    expected = [(1, 2), (-1, 2), (1, -2), (-1, -2)]
    prefix = ['i ' + ' '.join(map(str, c)) + ' 0' for c in expected]
    valid = prefix + ['3 0', '2 0', '0']
    rat_report = check_records(expected, valid)
    assert rat_report['rat_steps'] >= 1
    bad = {
        'missing_empty_clause': prefix + ['2 0'],
        'unjustified_empty_clause': prefix + ['0'],
        'changed_input_clause': prefix[:-1] + ['i -1 2 0', '2 0', '0'],
        'missing_input_clause': prefix[:-1] + ['2 0', '0'],
        'late_input_clause': prefix + ['2 0', 'i 3 0', '0'],
        'invented_rat_contradiction': ['i 1 2 0', '3 0', '0'],
    }
    rejected = []
    for name, lines in bad.items():
        try:
            check_records([(1, 2)] if name == 'invented_rat_contradiction' else expected, lines)
        except ProofError:
            rejected.append(name)
        else:
            raise AssertionError('Accepted invalid proof: ' + name)
    result = dict(status='PASS', exhaustive_truth_assignments=truth_checks,
                  formulas=formula_count, proof_controls=reports,
                  mode='stdlib-frozen-replay' if args.replay_only else 'native-generation-and-independent-replay',
                  explicit_rat_control=rat_report, rejected_invalid_controls=rejected,
                  scope='Restricted Boolean/PB encoding and independent finite refutation checks; no target exclusion.')
    if not args.replay_only:
        (HERE / 'PROOF_PIPELINE_REPLAY.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
