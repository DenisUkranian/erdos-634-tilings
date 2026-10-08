#!/usr/bin/env python3
"""Regenerate and independently replay the complete three-height exclusions."""
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
PRODUCER = HERE.parent / '154-cpsat/full_three_level.cpp'
VERIFIER = HERE / 'replay_three_level.cpp'
EXPECTED = [(0, 17013246, 17012488), (1, 16972710, 16972231)]

def run(argv):
    subprocess.run([str(x) for x in argv], check=True)


def main():
    results = []
    with tempfile.TemporaryDirectory(prefix='erdos634-three-heights-') as temporary:
        tmp = Path(temporary)
        producer, verifier = tmp/'produce', tmp/'replay'
        run(['g++', '-std=c++17', '-O2', PRODUCER, '-o', producer])
        run(['g++', '-std=c++17', '-O2', VERIFIER, '-o', verifier])
        for center, count, steps in EXPECTED:
            prefix = tmp/f'band-{center}'
            run([producer, '120', prefix, str(center)])
            outcome = json.loads(prefix.with_suffix('.json').read_text())
            if not outcome['conflict'] or outcome['incomplete']:
                raise RuntimeError('Producer did not finish with a contradiction')
            trace = Path(str(prefix)+'.assignments.bin')
            report = tmp/f'replayed-{center}.json'
            run([verifier, str(center), trace, report])
            result = json.loads(report.read_text())
            if (result['status'], result['placements'], result['assignments_checked'],
                result['lower'], result['upper'], result['rhs']) != ('PASS',count,steps,-1,-1,0):
                raise RuntimeError('Independent result differs from frozen scope')
            result['trace_sha256'] = hashlib.sha256(trace.read_bytes()).hexdigest()
            results.append(result)
    print(json.dumps({'status':'PASS','three_height_bands_refuted':True,
                      'full_154_decided':False,'results':results}, indent=2))

if __name__ == '__main__':
    main()
