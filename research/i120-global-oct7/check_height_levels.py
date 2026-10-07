#!/usr/bin/env python3
"""Exact regression checks for the written I120 cut-lattice theorem."""
from collections import Counter
from fractions import Fraction as F
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations
from math import gcd, isqrt
from pathlib import Path
import json
import gzip
import argparse

ROOT = Path(__file__).resolve().parents[2]


def load(name, path):
    spec = spec_from_file_location(name, ROOT / path)
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def mul(p, q):
    x, y = p
    u, v = q
    return x*u-y*v, x*v+y*u+y*v


def conj(p):
    return p[0]+p[1], -p[1]


def power(p, h):
    if h < 0:
        p = conj(p)
    out = (F(1), F(0))
    for _ in range(abs(h)):
        out = mul(out, p)
    return out


def sub(p, q):
    return p[0]-q[0], p[1]-q[1]


def norm(p):
    return p[0]**2+p[0]*p[1]+p[1]**2


def height_counts(triangles, a, b, c, exceptional=0):
    z = (F(a, c), F(b, c))
    directions = {}
    # This bound is only a lookup for these constructed fixtures.
    # An unrecognized direction fails the replay; it is never discarded.
    for h in range(-4, 5):
        u = power(z, h)
        for _ in range(6):
            if u in directions:
                assert directions[u] == h
            directions[u] = h
            u = mul(u, (F(0), F(1)))
    counts = Counter()
    for tri in triangles:
        edges = [sub(tri[(i+1) % 3], tri[i]) for i in range(3)]
        assert sorted(map(norm, edges)) == sorted([a*a, b*b, c*c])
        hs = []
        for length in [a, b]:
            e = next(e for e in edges if norm(e) == length*length)
            hs.append(directions[(e[0]/length, e[1]/length)])
        assert hs[0] == hs[1]
        counts[hs[0]] += 1
    assert all(n % c == 0 for h, n in counts.items() if h != exceptional)
    assert counts[exceptional] % c == len(triangles) % c
    return {str(h): n for h, n in sorted(counts.items())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path,
                        help='Optional output report; default run writes no files.')
    args = parser.parse_args()
    checked = 0
    for a in range(2, 501):
        for b in range(2, a):
            if gcd(a, b) != 1:
                continue
            c = isqrt(a*a+a*b+b*b)
            if c*c != a*a+a*b+b*b:
                continue
            vectors = [(c, 0), (0, c), (a, b), (-b, a+b)]
            minors = [abs(p[0]*q[1]-p[1]*q[0])
                      for p, q in combinations(vectors, 2)]
            assert gcd(*minors) == c
            assert gcd(a*b, c) == 1
            checked += 1

    builder = load('i120_fixture_builder', 'research/general-spectra/build_certificate.py')
    verifier = load('i120_fixture_verifier', 'research/general-spectra/verify_certificate.py')
    a, b, c, m = 5, 3, 7, 9
    cert = builder.construct(a, b, c, 120, m)
    verification = verifier.verify(cert, expand=True)
    equi = []
    for region in cert['regions']:
        poly = verifier.points(region['vertices'])
        if region['kind'] == 'similar_triangle':
            equi.extend(verifier.triangle_grid(poly, region['scale']))
        else:
            equi.extend(verifier.strip_grid(poly, region['counts'], a, b, 120))
    equi_counts = height_counts(equi, a, b, c)

    # Standard positive I120 partition: one equilateral core and two
    # bm-fold copies of the original tile. Coordinates use 1,rho.
    e = (F(b*b*m), F(0))
    g = (F(b*(a+b)*m), F(0))
    k = (F(b*b*m), F(a*b*m))
    o = (F(0), F(0))
    big_b = (F(b*(a+2*b)*m), F(0))
    target = [o, big_b, k]
    macros = [[e, g, k], [o, e, k], [g, big_b, k]]
    assert all(verifier.inside(p, target) for poly in macros for p in poly)
    assert sum(verifier.area2(poly) for poly in macros) == verifier.area2(target)
    for p, q in combinations(macros, 2):
        inter = verifier.clip(p, q)
        assert len(inter) < 3 or verifier.area2(inter) == 0
    i120 = [[(p[0]+e[0], p[1]) for p in tri] for tri in equi]
    i120.extend(verifier.triangle_grid(macros[1], b*m))
    i120.extend(verifier.triangle_grid(macros[2], b*m))
    assert len(i120) == b*(a+2*b)*m*m
    i120_counts = height_counts(i120, a, b, c)

    # A positive region with a closed whole-c-step boundary need not
    # have a c-squared-divisible tile count.
    unit = (F(a*a,c), F(a*b,c))
    small = []
    for j in range(c):
        p = (j*unit[0],j*unit[1])
        q = (p[0]+c,p[1])
        r = (q[0]+unit[0],q[1]+unit[1])
        s = (p[0]+unit[0],p[1]+unit[1])
        small.extend([[p,q,s],[q,r,s]])
    small_outer = [(F(0),F(0)),(F(c),F(0)),
                   (F(c+a*a),F(a*b)),(F(a*a),F(a*b))]
    assert all(verifier.inside(p,small_outer) for tri in small for p in tri)
    assert sum(verifier.area2(t) for t in small) == verifier.area2(small_outer)
    small_pairs = 0
    for p,q in combinations(small,2):
        inter = verifier.clip(p,q)
        assert len(inter) < 3 or verifier.area2(inter) == 0
        small_pairs += 1
    small_counts = height_counts(small,a,b,c)
    assert small_counts == {'1':2*c,'0':0} or small_counts == {'1':2*c}
    assert len(small) % (c*c) != 0

    f23_checks = []
    for rel in ['research/group2-nested-corners/f2-506.json',
                'research/group2-nested-corners/f3-990.json',
                'research/group2-mixed-gamma/f3-19320.json.gz']:
        path = ROOT / rel
        raw = gzip.open(path,'rt').read() if path.suffix == '.gz' else path.read_text()
        data = json.loads(raw)
        aa,bb,cc = data['tile']
        mm = data['multiplier']
        zz = (F(aa,cc),F(bb,cc))
        is_f2 = '/f2-' in rel
        factor = mm*(aa if is_f2 else cc)*(aa+2*bb)
        direction = power(zz,2 if is_f2 else 3)
        expected_target = [(F(0),F(0)),(F(mm*cc*cc),F(0)),
                           tuple(factor*x for x in direction)]
        assert [tuple(map(F,p)) for p in data['target']] == expected_target
        triangles = [[tuple(map(F,p)) for p in tri] for tri in data['triangles']]
        counts = height_counts(triangles,aa,bb,cc,exceptional=2)
        f23_checks.append({'certificate':rel,'count':len(triangles),
                          'height_counts':counts,'exceptional_height':2,
                          'canonical_target_normalization_checked':True})

    report = {
        'status': 'PASS',
        'full_Erdos634_solved': False,
        'primitive_norm_triples_checked': checked,
        'parameter_range': '2 <= b < a <= 500; c is the positive square root',
        'equilateral': {'tile': [a,b,c], 'm': m, 'count': len(equi),
                        'height_counts': equi_counts,
                        'macro_validation': verification['result']},
        'I120': {'tile': [a,b,c], 'm': m, 'count': len(i120),
                 'height_counts': i120_counts,
                 'positive_three_macro_partition_checked': True},
        'c_squared_cut_argument_counterexample': {
            'target': 'parallelogram, not I120', 'tile': [a,b,c],
            'count': len(small), 'height_counts': small_counts,
            'all_pairs_checked': small_pairs,
            'tile_count_mod_c_squared': len(small) % (c*c)},
        'case_154': {'n0_residue_mod13': 154 % 13,
                     'max_occupied_heights': 154 // 13 + 1,
                     'passing_unplaced_counts': {'0': 141, '1': 13},
                     'status': 'UNRESOLVED'},
        'F2_F3_existing_certificate_checks': f23_checks,
        'scope': 'Finite algebra and construction regression checks; the universal theorem is the written whole-edge-chain proof.'
    }
    if args.report is not None:
        args.report.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
