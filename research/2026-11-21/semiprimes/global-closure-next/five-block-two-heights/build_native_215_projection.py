#!/usr/bin/env python3
"""Discover a compact exact-checkable certificate for one native215 profile.

Floating arithmetic constructs the candidate only. The independent exact
replay must pass before its strictly positive rational conclusion is used.
"""
from pathlib import Path
import gzip
import importlib.util
import json
import math

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'research').is_dir() and (p / 'scripts').is_dir())


def main():
    module_path = ROOT / 'research/2026-11-21/semiprimes/global-invariant/verify_3431_rational_projection.py'
    spec = importlib.util.spec_from_file_location('established_exact_fourier_blocks', module_path)
    exact = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(exact)
    a, b, c = 35, 13, 43
    Q, R, D = 10**12, 10**6, 10**12
    roots = [(round(Q*math.cos(2*math.pi*r/c)), round(Q*math.sin(2*math.pi*r/c))) for r in range(c)]
    blocks = []
    for kx in range(c):
        for ky in range(c):
            raw = exact.block(a, b, c, kx, ky, roots, Q)
            matrix = np.asarray([[complex(re, im)/Q for re, im in row] for row in raw])
            inverse = np.linalg.inv(matrix@matrix.conj().T)
            numerators = [[[round(float(z.real)*R), round(float(z.imag)*R)] for z in row] for row in inverse]
            blocks.append({'frequency': [kx, ky], 'inverse_numerators': numerators})
    old = json.loads(gzip.decompress((HERE / 'N5063_NATIVE_215_PROFILE_IPM.json.gz').read_bytes()))
    assert old['tile'] == [a, b, c] and old['status'] == 0 and old['population'] < 215
    uniform = (215-old['population'])/(12*c*c)
    base = round(uniform*D)
    increments = []
    for x, y, j, hand, gate, value in old['support']:
        increment = round((value+uniform)*D)-base
        if increment:
            increments.append([x, y, j, hand, increment])
    certificate = {
        'tile': [a, b, c], 'point_denominator': D,
        'uniform_point_numerator': base, 'point_increments': increments,
        'root_denominator': Q, 'root_numerators': roots,
        'inverse_denominator': R, 'fourier_blocks': blocks,
        'target_population': 215, 'native_gate_currents': [42, 1],
        'positive_gate_capacity': 94,
        'scope': 'One strictly positive rational full periodic profile for a native215 class, with sign masses129/86. The point is x0+M^dagger(b-Mx0). No integer tile multiplicities or physical tiling are asserted.'}
    encoded = (json.dumps(certificate, sort_keys=True, separators=(',', ':'))+'\n').encode()
    compressed = gzip.compress(encoded, compresslevel=9, mtime=0)
    destination = HERE / 'N5063_NATIVE_215_RATIONAL_CERTIFICATE.json.gz'
    destination.write_bytes(compressed)
    print(json.dumps({'certificate': destination.name, 'fourier_blocks': len(blocks),
                      'nonuniform_point_increments': len(increments),
                      'raw_bytes': len(encoded), 'compressed_bytes': len(compressed)}, indent=2))


if __name__ == '__main__':
    main()
