#!/usr/bin/env python3
"""Replay independent certificate gates and exact gamma arithmetic.

The general geometric theorem is proved in PROOF.md. The finite coordinate
certificate and symbolic count identity do not by themselves prove it.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent


def run(script, *args):
    result = subprocess.run([sys.executable, str(script), *map(str, args)],
                            check=True, capture_output=True, text=True)
    report = json.loads(result.stdout)
    if report.get('status') != 'PASS':
        raise RuntimeError(f'{script.name} did not report PASS')
    return report


def gamma_arithmetic():
    # Homogeneous quadratic coefficients are ordered a^2, a*b, b^2.
    def square(x, y):
        return (x*x, 2*x*y, y*y)

    plus_norm = (1, 1, 1)
    outer = square(1, 2)
    hole = square(1, -1)
    count = tuple(3*n+o-d for n, o, d in zip(plus_norm, outer, hole))
    expected = (3, 9, 6)  # 3(a+b)(a+2b)
    if count != expected:
        raise RuntimeError('Formal gamma count identity failed')

    a, b, c, m = 5, 3, 7, 1
    h, delta = a+2*b, a-b
    if not (c*c == a*a+a*b+b*b and b < a <= 2*b
            and h >= a+b and 0 < delta <= b):
        raise RuntimeError('Retained example violates the construction domain')
    ordinary_rectangle_tiles = 2*(m*b)*(m*a)
    swapped_rectangle_tiles = 2*(m*a)*(m*b)
    if ordinary_rectangle_tiles != swapped_rectangle_tiles:
        raise RuntimeError('The two common-rectangle grids have different areas')
    result = 3*(m*c)**2+(m*h)**2-(m*delta)**2
    if result != 264:
        raise RuntimeError('Retained gamma count is not 264')
    return {
        'status': 'PASS',
        'formal_count_identity': '3c^2+h^2-delta^2=3(a+b)(a+2b)',
        'substitution': 'c^2=a^2+ab+b^2, h=a+2b, delta=a-b',
        'quadratic_coefficients_a2_ab_b2': list(count),
        'example_outer_scale': h,
        'example_removed_scale': delta,
        'example_three_large_triangle_tiles': 3*c*c,
        'example_gamma_remainder_tiles': h*h-delta*delta,
        'example_common_rectangle_tiles_before_deletion': ordinary_rectangle_tiles,
        'N': result,
        'general_geometry_basis': 'PROOF.md; a mathematical positive-partition proof',
        'finite_checks_claim_general_geometric_completeness': False,
    }


def main():
    if not __debug__:
        raise SystemExit('Run without -O')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    geometry = run(HERE.parent/'group2-nested-corners/verify.py',
                   HERE/'f3-264.json')
    disk = run(HERE.parent/'disk-certificates/verify_disk.py',
               HERE/'disk-264.json')
    if geometry.get('N') != 264 or disk.get('N') != 264:
        raise RuntimeError('Unexpected retained certificate tile count')
    obstruction = run(HERE/'check_two_axis_obstruction.py')
    if obstruction.get('arbitrary_F3_tiling_excluded') is not False:
        raise RuntimeError('Obstruction checker claims an unsupported exclusion')
    report = {
        'status': 'PASS',
        'ordered_positive_theorem_scope': {
            'tile_relation': 'c^2=a^2+ab+b^2',
            'parameter_range': 'b<a<=2b; positive integers',
            'primitivity_required': False,
            'multipliers': 'Every positive integer m',
            'target_sides': ['m*c^2', 'm*c*(a+2b)', '3*m*b*(a+b)'],
            'tile_count': '3*(a+b)*(a+2b)*m^2',
            'exchanged_label_F3_target_automatically_included': False,
        },
        'gamma_arithmetic': gamma_arithmetic(),
        'geometry': geometry,
        'coordinate_free_disk': disk,
        'primitive_multiplier_one_gamma_obstruction': obstruction,
        'full_Erdos634_solved': False,
        'external_peer_review': False,
    }
    output = json.dumps(report, indent=2)+'\n'
    if args.report:
        args.report.write_text(output)
    print(output, end='')


if __name__ == '__main__':
    main()
