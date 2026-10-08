#!/usr/bin/env python3
"""Encode exact signed endpoint rows as CNF; optionally produce binary DRAT.

Dependencies: python-sat. The CNF is an existential encoding: each signed
row is an exact-cardinality constraint on its signed Boolean literals.
No floating-point calculation enters the encoding.
"""
import argparse
import itertools
import json
from pathlib import Path
import shutil
import time

from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical300


def encode(source, output, count=None):
    start = time.monotonic()
    body = Path(str(output) + '.body')
    with open(source) as src, body.open('w') as dst:
        nv, nsel = map(int, next(src).split())
        for _ in range(nv + nsel):
            next(src)
        top = nv
        clauses = 0
        rows = 0
        def emit(clause):
            nonlocal clauses
            dst.write(' '.join(map(str, clause)) + ' 0\n')
            clauses += 1
        def cardinality(lits, k):
            nonlocal top
            n = len(lits)
            if not 0 <= k <= n:
                emit([])
            elif k == 0:
                for x in lits: emit([-x])
            elif k == n:
                for x in lits: emit([x])
            elif n <= 5:
                for c in itertools.combinations(lits, k + 1): emit([-x for x in c])
                for c in itertools.combinations(lits, n - k + 1): emit(c)
            else:
                enc = CardEnc.equals(lits=lits, bound=k, top_id=top,
                                     encoding=EncType.seqcounter)
                top = max(top, enc.nv)
                for c in enc.clauses: emit(c)
        for line in src:
            b, n, *lits = map(int, line.split())
            assert n == len(lits) and all(1 <= abs(x) <= nv for x in lits)
            cardinality(lits, b + sum(x < 0 for x in lits))
            rows += 1
        if count is not None:
            # A binary sorting network avoids a sequential counter of size
            # proportional to nv * count for this optional global condition.
            enc = CardEnc.equals(lits=list(range(1, nv + 1)), bound=count-nsel,
                                 top_id=top, encoding=EncType.cardnetwrk)
            top = max(top, enc.nv)
            for c in enc.clauses: emit(c)
    with open(output, 'wb') as dst, body.open('rb') as src:
        dst.write(f'p cnf {top} {clauses}\n'.encode())
        shutil.copyfileobj(src, dst)
    body.unlink()
    report = dict(source=str(source), variables=nv, selected=nsel, rows=rows,
                  cnf_variables=top, clauses=clauses, explicit_count=count,
                  encoding_seconds=time.monotonic()-start)
    Path(str(output)+'.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report), flush=True)


def solve(cnf, proof, conflicts):
    start = time.monotonic()
    with Cadical300(with_proof=True, use_timer=True) as solver:
        with open(cnf) as f:
            for line in f:
                if line[0] in 'pc': continue
                c = list(map(int, line.split()))
                assert c[-1] == 0
                solver.add_clause(c[:-1])
        print('loaded CNF', flush=True)
        solver.conf_budget(conflicts)
        result = solver.solve_limited()
        solver.prfile.flush()
        solver.prfile.seek(0)
        with open(proof, 'wb') as dst:
            shutil.copyfileobj(solver.prfile, dst)
        report = dict(status='UNSAT' if result is False else 'SAT' if result else 'UNKNOWN',
                      seconds=time.monotonic()-start, stats=solver.accum_stats(),
                      proof=str(proof), proof_bytes=Path(proof).stat().st_size,
                      independently_checked=False)
        if result is True:
            Path(str(proof)+'.model').write_text(' '.join(map(str, solver.get_model()))+'\n')
    Path(str(proof)+'.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest='command', required=True)
    e = sub.add_parser('encode'); e.add_argument('source'); e.add_argument('output'); e.add_argument('--count',type=int)
    s = sub.add_parser('solve'); s.add_argument('cnf'); s.add_argument('proof'); s.add_argument('--conflicts',type=int,default=100000)
    a = p.parse_args()
    if a.command == 'encode': encode(a.source,a.output,a.count)
    else: solve(a.cnf,a.proof,a.conflicts)
