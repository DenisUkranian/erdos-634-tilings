#!/usr/bin/env python3
"""Independent truth-table audit of the exact signed-row CNF encoder."""
from contextlib import redirect_stdout
from importlib.util import spec_from_file_location, module_from_spec
from io import StringIO
from itertools import product
from pathlib import Path
from tempfile import TemporaryDirectory
import json, os, sys, time

sys.path.insert(0, os.environ.get('ERDOS_PYSAT_PATH', '/tmp/erdos634-cert-solvers'))
from pysat.solvers import Glucose3

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent/'e135-residual'/'sat_certificate.py'
spec = spec_from_file_location('audited_sat_encoder', SOURCE)
encoder = module_from_spec(spec)
spec.loader.exec_module(encoder)


def load_cnf(path):
    lines = path.read_text().splitlines()
    p, cnf, nv, nc = lines[0].split()
    assert (p, cnf) == ('p', 'cnf')
    clauses = [list(map(int, row.split()))[:-1] for row in lines[1:]]
    assert len(clauses) == int(nc)
    assert all(row.endswith(' 0') or row == ' 0' for row in lines[1:])
    assert all(1 <= abs(z) <= int(nv) for c in clauses for z in c)
    return int(nv), clauses


def main():
    start = time.monotonic()
    cases = assignments = 0
    with TemporaryDirectory(prefix='erdos634-sat-audit-') as folder:
        inp, out = Path(folder)/'input.txt', Path(folder)/'output.cnf'
        for n in range(10):
            signs_set = {tuple([1]*n), tuple([-1]*n),
                         tuple(1 if j%2 else -1 for j in range(n))}
            for signs in signs_set:
                for k in range(-1, n+2):
                    lits = [signs[j]*(j+1) for j in range(n)]
                    b = k-sum(s<0 for s in signs)
                    inp.write_text(f'{n} 0\n'+'0 0 0 0\n'*n+
                                   f'{b} {n} '+' '.join(map(str,lits))+'\n')
                    with redirect_stdout(StringIO()):
                        encoder.encode(inp, out)
                    nv, clauses = load_cnf(out)
                    assert nv >= n
                    with Glucose3(bootstrap_with=clauses) as solver:
                        for bits in product([0,1], repeat=n):
                            expected = sum(s*x for s,x in zip(signs,bits)) == b
                            assumptions = [(j+1)*(1 if bits[j] else -1) for j in range(n)]
                            assert solver.solve(assumptions=assumptions) == expected, (n,signs,k,bits)
                            assignments += 1
                    cases += 1
        # Multiple nontrivial counters use one growing auxiliary-ID namespace.
        # Exhaust all 2^12 assignments for two overlapping signed constraints.
        rows = [(1, [1,-2,3,-4,5,-6,7]), (-1, [-5,6,-7,8,-9,10,-11,12])]
        inp.write_text('12 0\n'+'0 0 0 0\n'*12+''.join(
            f'{b} {len(lits)} '+' '.join(map(str,lits))+'\n' for b,lits in rows))
        with redirect_stdout(StringIO()):
            encoder.encode(inp, out)
        nv, clauses = load_cnf(out)
        assert nv > 12
        with Glucose3(bootstrap_with=clauses) as solver:
            for bits in product([0,1], repeat=12):
                expected = all(sum((1 if z>0 else -1)*bits[abs(z)-1] for z in lits)==b for b,lits in rows)
                assumptions = [(j+1)*(1 if bits[j] else -1) for j in range(12)]
                assert solver.solve(assumptions=assumptions) == expected
                assignments += 1
        cases += 1
    result = dict(status='PASS', single_row_sizes='0..9', cases=cases,
                  assignments_checked=assignments, independent_solver='Glucose3',
                  seconds=time.monotonic()-start,
                  scope='Signed-row equivalence and auxiliary namespaces; not source-model completeness or DRAT replay')
    HERE.joinpath('sat_encoder_checked.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
