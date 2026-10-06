#!/usr/bin/env python3
"""Run the independent retained-certificate checks without the constructor."""
import argparse
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent


def run(script, *args):
    completed = subprocess.run([sys.executable, str(script), *map(str, args)],
                               check=True, capture_output=True, text=True)
    result = json.loads(completed.stdout)
    if result.get('status') != 'PASS':
        raise RuntimeError(f'{script.name} did not return PASS')
    return result


def main():
    if not __debug__:
        raise SystemExit('Run without -O')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    geometry = []
    for name, count in (('f4-345.json', 345), ('f2-506.json', 506),
                        ('f3-990.json', 990)):
        result = run(HERE/'verify.py', HERE/name)
        if result.get('N') != count:
            raise RuntimeError(f'Unexpected tile count for {name}')
        geometry.append({'certificate': name, 'N': count, 'status': 'PASS',
                         'pairs_checked': result['pairs_checked'],
                         'sha256': result['certificate_sha256']})
    disk = run(HERE.parent/'disk-certificates/verify_disk.py', HERE/'disk-990.json')
    if disk.get('N') != 990:
        raise RuntimeError('Unexpected disk tile count')
    negative = run(HERE/'test_verifier.py')
    report = {'status': 'PASS', 'geometry': geometry,
              'coordinate_free_disk': {'certificate': 'disk-990.json', 'N': 990,
                                       'status': 'PASS',
                                       'sha256': disk['certificate_sha256']},
              'duplicate_tile_negative_test': negative['negative_rejection'],
              'full_Erdos634_solved': False, 'external_peer_review': False}
    output = json.dumps(report, indent=2)+'\n'
    if args.report:
        args.report.write_text(output)
    print(output, end='')


if __name__ == '__main__':
    main()
