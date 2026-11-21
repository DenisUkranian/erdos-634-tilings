#!/usr/bin/env python3
"""Exact rational correction certificate for the native215 periodic model.

Standard library only. Reuses the previously audited, parameterized exact
Fourier inverse bound; reconstructs every integer endpoint and gate column.
This proves fractional projection feasibility, never a physical tiling.
"""
from pathlib import Path
import gzip
import hashlib
import importlib.util
import json

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'research').is_dir() and (p / 'scripts').is_dir())
U = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))
FOURIER_SOURCE = ROOT / 'research/2026-11-21/semiprimes/global-invariant/verify_3431_rational_projection.py'


def inverse_bound(certificate):
    """Public entry point for subsequent exact lifting certificates."""
    spec = importlib.util.spec_from_file_location('established_exact_fourier_bound', FOURIER_SOURCE)
    exact = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(exact)
    return exact.inverse_bound(certificate)


def point_checks(certificate, K):
    a, b, c = certificate['tile']
    D = certificate['point_denominator']
    base = certificate['uniform_point_numerator']
    assert isinstance(D, int) and D > 0 and isinstance(base, int)
    values = [base]*(12*c*c)

    def column(x, y, j, hand):
        return ((x*c+y)*6+j)*2+(hand == 1)

    seen = set()
    for x, y, j, hand, increment in certificate['point_increments']:
        assert all(isinstance(v, int) for v in (x, y, j, hand, increment))
        assert 0 <= x < c and 0 <= y < c and 0 <= j < 6 and hand in (-1, 1)
        index = column(x, y, j, hand)
        assert index not in seen
        seen.add(index)
        values[index] += increment
    minimum = min(values)
    assert minimum > 0
    gate_base = 3*c*c
    population_row = gate_base+2*c
    currents = [0]*(population_row+1)
    positive_bins = [0]*(2*c)

    def row(axis, x, y):
        return (axis % 3)*c*c+(x % c)*c+y % c

    for x in range(c):
        for y in range(c):
            for j in range(6):
                for hand in (-1, 1):
                    value = values[column(x, y, j, hand)]
                    epsilon = hand*(-1 if j % 2 else 1)
                    ux, uy = x-a*U[j][0], y-a*U[j][1]
                    wx, wy = x+b*U[(j+hand) % 6][0], y+b*U[(j+hand) % 6][1]
                    for axis, px, py, sign in ((j, x, y, hand), (j, ux, uy, -hand),
                                               (j+hand, wx, wy, hand), (j+hand, x, y, -hand)):
                        currents[row(axis, px, py)] += sign*value
                    gate = (a*uy-b*ux) % c if hand == 1 else c+(a*ux-b*uy) % c
                    currents[gate_base+gate] += epsilon*value
                    currents[population_row] += value
                    if epsilon > 0:
                        positive_bins[gate] += value
    target = [0]*len(currents)
    target[gate_base] = 42*D
    target[gate_base+c] = D
    target[-1] = 215*D
    residual = [wanted-actual for wanted, actual in zip(target, currents)]
    squared = sum(value*value for value in residual)
    assert K*squared < minimum*minimum
    capacity = certificate['positive_gate_capacity']
    assert capacity == (8*129+35*86)//43 == 94
    slack = min(capacity*D-value for value in positive_bins)
    assert slack > 0 and (3*c)**2*K*squared < slack*slack
    assert 42+1 == 43 and (215+43)//2 == 129 and (215-43)//2 == 86
    assert 42 == 2*c+(a-b)*(-2) and 1 == -c+(a-b)*2
    negative_capacity = (8*86+35*129)//43
    assert negative_capacity == 121 and 86 < negative_capacity
    return {
        'variables': len(values), 'equations': len(currents),
        'point_denominator': D,
        'minimum_approximate_numerator': minimum,
        'residual_squared_numerator': squared,
        'norm_bound_K': K,
        'positivity_inequality': [K*squared, minimum*minimum],
        'positive_gate_capacity': capacity,
        'negative_gate_capacity': negative_capacity,
        'negative_gate_population_bound_from_total_sign_mass': 86,
        'minimum_gate_slack_numerator': slack,
        'gate_capacity_inequality': [(3*c)**2*K*squared, slack*slack],
        'exact_corrected_population': 215,
        'exact_corrected_positive_population': 129,
        'exact_corrected_negative_population': 86,
        'exact_gate_currents': {'native_up': 42, 'native_down': 1, 'all_remote': 0},
        'exact_node_charge_units': {'native_up': -2, 'native_down': 2, 'all_remote': 0}}


def main():
    path = HERE / 'N5063_NATIVE_215_RATIONAL_CERTIFICATE.json.gz'
    compressed = path.read_bytes()
    raw = gzip.decompress(compressed)
    assert compressed[4:8] == b'\0\0\0\0', 'Require deterministic gzip timestamp.'
    certificate = json.loads(raw)
    assert certificate['tile'] == [35, 13, 43]
    assert certificate['target_population'] == 215
    assert certificate['native_gate_currents'] == [42, 1]
    K, histogram = inverse_bound(certificate)
    point = point_checks(certificate, K)
    report = {
        'status': 'PASS', 'tile': [35, 13, 43],
        'certificate_sha256': hashlib.sha256(compressed).hexdigest(),
        'uncompressed_certificate_sha256': hashlib.sha256(raw).hexdigest(),
        'exact_fourier_dependency_sha256': hashlib.sha256(FOURIER_SOURCE.read_bytes()).hexdigest(),
        'root_enclosures_checked': 43, 'fourier_blocks_checked': 1849,
        'block_row_counts': histogram, 'point': point,
        'full_5063_excluded': False, 'physical_tiling_constructed': False,
        'integer_tile_multiplicities_asserted': False,
        'scope': 'A strictly positive rational feasible point exists in the full native215 periodic endpoint model, with integer gate charges and both sign-specific gate capacities. This proves a limit of this fractional relaxation only.'}
    (HERE / 'N5063_NATIVE_215_RATIONAL_REPLAY.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    main()
