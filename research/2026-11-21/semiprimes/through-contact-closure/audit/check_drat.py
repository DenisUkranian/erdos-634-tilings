#!/usr/bin/env python3
"""Small exact checker for Z3 ASCII DRAT with explicit initial i-records.

Every input clause is checked against the expected CNF using one bijective
variable renaming. Every addition is RUP or RAT, and an empty clause is
required. Deletions are conservatively ignored: every addition is checked
against all previously accepted clauses. This may reject a valid deletion-
sensitive RAT trace, but every accepted addition sequence is itself a valid
refutation. The simple implementation targets small/medium root cases.
"""
import argparse
import hashlib
import json
from pathlib import Path

if not __debug__:
    raise SystemExit('Run without -O: exact verification assertions are required.')


class ProofError(ValueError):
    pass


def read_dimacs(path):
    variables = count = None
    clauses = []
    pending = []
    for line in Path(path).read_text().splitlines():
        if not line.strip() or line.startswith('c'):
            continue
        if line.startswith('p '):
            _, kind, variables, count = line.split()
            if kind != 'cnf':
                raise ProofError('Expected CNF')
            variables, count = int(variables), int(count)
            continue
        for token in line.split():
            value = int(token)
            if value:
                pending.append(value)
            else:
                clauses.append(tuple(pending))
                pending = []
    if pending or variables is None or count != len(clauses):
        raise ProofError('Malformed DIMACS')
    if any(abs(x) > variables for c in clauses for x in c):
        raise ProofError('Literal outside declared variable range')
    return variables, clauses


def rup(database, candidate):
    assignment = {}

    def assign(literal):
        variable, value = abs(literal), literal > 0
        if variable in assignment:
            return assignment[variable] == value
        assignment[variable] = value
        return True

    for literal in candidate:
        if not assign(-literal):
            return True
    changed = True
    while changed:
        changed = False
        for clause in database:
            satisfied = False
            unassigned = []
            for literal in clause:
                value = assignment.get(abs(literal))
                if value is None:
                    unassigned.append(literal)
                elif value == (literal > 0):
                    satisfied = True
                    break
            if satisfied:
                continue
            if not unassigned:
                return True
            if len(unassigned) == 1:
                literal = unassigned[0]
                if not assign(literal):
                    return True
                changed = True
    return False


def propagate_inputs(clauses):
    """Exact satisfiability-preserving unit reduction, with no solver calls."""
    assignment = {}
    remaining = list(map(tuple, clauses))
    while True:
        units = []
        reduced = []
        seen = set()
        for clause in remaining:
            if any(abs(x) in assignment and assignment[abs(x)] == (x > 0) for x in clause):
                continue
            free = tuple(x for x in clause if abs(x) not in assignment)
            if not free:
                return [()], assignment
            if len(free) == 1:
                units.append(free[0])
            if frozenset(free) not in seen:
                seen.add(frozenset(free))
                reduced.append(free)
        if not units:
            return reduced, assignment
        for literal in units:
            variable, value = abs(literal), literal > 0
            if variable in assignment and assignment[variable] != value:
                return [()], assignment
            assignment[variable] = value
        remaining = reduced


def check_records(expected, lines):
    inputs = 0
    mapping, inverse = {}, {}
    database = set()
    additions = deletions = rup_steps = rat_steps = 0
    derived_empty = False
    started = False
    for lineno, raw in enumerate(lines, 1):
        words = raw.split()
        if not words or words[0] == 'c':
            continue
        kind = words.pop(0) if words[0] in ('i', 'd') else 'a'
        try:
            numbers = list(map(int, words))
        except ValueError as exc:
            raise ProofError(f'Invalid record at line {lineno}') from exc
        if not numbers or numbers[-1] != 0 or any(x == 0 for x in numbers[:-1]):
            raise ProofError(f'Expected one zero terminator at line {lineno}')
        clause = tuple(numbers[:-1])
        if len(set(clause)) != len(clause):
            raise ProofError(f'Duplicate literals at line {lineno}')
        key = frozenset(clause)
        if kind == 'i':
            if started or inputs >= len(expected):
                raise ProofError('Unexpected extra or late input clause')
            source = expected[inputs]
            if len(source) != len(clause):
                raise ProofError('Input clause length mismatch')
            known = {mapping[abs(x)] if x > 0 else -mapping[abs(x)]
                     for x in source if abs(x) in mapping}
            if not known <= key:
                raise ProofError('Mapped input literals disagree')
            fresh_old = [x for x in source if abs(x) not in mapping]
            fresh_new = sorted(key - known, key=abs)
            if len(fresh_old) != len(fresh_new):
                raise ProofError('Input variable introduction mismatch')
            # Propose newly introduced SAT identifiers in allocation order.
            # Every complete clause and the global bijection are then checked;
            # the proposal is not itself a trusted fact about Z3.
            for old, new in zip(fresh_old, fresh_new):
                signed_image = new if old > 0 else -new
                old_var, new_var = abs(old), abs(new)
                if new_var in inverse and inverse[new_var] != old_var:
                    raise ProofError('Noninjective input variable mapping')
                mapping[old_var] = signed_image
                inverse[new_var] = old_var
            image = frozenset(mapping[abs(x)] if x > 0 else -mapping[abs(x)] for x in source)
            if image != key:
                raise ProofError('Input clause mismatch')
            database.add(key)
            inputs += 1
            continue
        if inputs != len(expected):
            raise ProofError('The complete expected input prefix is missing')
        started = True
        if kind == 'd':
            # Checking the addition-only trace avoids depending on the native
            # solver's retention of root-level propagated units after deletion.
            # RAT checks below include every retained opposing-pivot clause.
            deletions += 1
            continue
        additions += 1
        if rup(database, clause):
            rup_steps += 1
        elif clause:
            pivot = clause[0]
            for other in tuple(database):
                if -pivot not in other:
                    continue
                resolvent = (key - {pivot}) | (other - {-pivot})
                if any(-x in resolvent for x in resolvent):
                    continue
                if not rup(database, resolvent):
                    raise ProofError(f'Failed RAT resolvent at line {lineno}')
            rat_steps += 1
        else:
            raise ProofError(f'Empty clause is not RUP at line {lineno}')
        database.add(key)
        if not clause:
            derived_empty = True
    if inputs != len(expected):
        raise ProofError('Incomplete input clause prefix')
    if not derived_empty:
        raise ProofError('No verified derived empty clause')
    return dict(status='VERIFIED_UNSAT', input_clauses=inputs, mapped_variables=len(mapping),
                additions=additions, ignored_deletions=deletions, rup_steps=rup_steps, rat_steps=rat_steps)


def check_files(cnf, proof):
    _, clauses = read_dimacs(cnf)
    with Path(proof).open() as stream:
        result = check_records(clauses, stream)
    result.update(cnf_sha256=hashlib.sha256(Path(cnf).read_bytes()).hexdigest(),
                  proof_sha256=hashlib.sha256(Path(proof).read_bytes()).hexdigest())
    return result


def check_with_propagation(original_cnf, reduced_cnf, proof):
    variables, original = read_dimacs(original_cnf)
    reduced_variables, supplied = read_dimacs(reduced_cnf)
    expected, assignment = propagate_inputs(original)
    if variables != reduced_variables or expected != supplied:
        raise ProofError('Incorrect exact unit reduction')
    result = check_files(reduced_cnf, proof)
    result.update(original_cnf_sha256=hashlib.sha256(Path(original_cnf).read_bytes()).hexdigest(),
                  propagated_variables=len(assignment), reduced_clauses=len(supplied))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('cnf', type=Path)
    parser.add_argument('proof', type=Path)
    args = parser.parse_args()
    print(json.dumps(check_files(args.cnf, args.proof), sort_keys=True))


if __name__ == '__main__':
    main()
