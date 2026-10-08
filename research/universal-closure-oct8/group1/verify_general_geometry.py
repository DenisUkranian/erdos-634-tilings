#!/usr/bin/env python3
"""Independent integer verification of arbitrary diagonal-metric certificates."""
from pathlib import Path
import argparse
import json


def determinant(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])


def edges(p):
    return zip(p, p[1:]+p[:1])


def area2(p):
    return sum(a[0]*b[1]-a[1]*b[0] for a, b in edges(p))


def separate(p, q):
    return any(all(determinant(a, b, c) <= 0 for c in q) for a, b in edges(p))


def check(path):
    data = json.loads(path.read_text())
    D, den = data['metric_y_coefficient'], data['denominator']
    assert isinstance(D, int) and D > 0 and isinstance(den, int) and den > 0
    tiles, goal = data['triangles'], data['target']
    assert all(isinstance(x, int) for t in tiles+[goal] for p in t for x in p)
    expected = sorted(x*x*den*den for x in data['tile'])
    assert area2(goal) > 0
    for t in tiles:
        assert len(t) == 3 and area2(t) > 0
        assert sorted((a[0]-b[0])**2+D*(a[1]-b[1])**2 for a, b in edges(t)) == expected
        assert all(determinant(a, b, p) >= 0 for a, b in edges(goal) for p in t)
    assert sum(area2(t) for t in tiles) == area2(goal)
    for i, t in enumerate(tiles):
        for q in tiles[:i]:
            assert separate(t, q) or separate(q, t)
    return {'status': 'PASS', 'tile_count': len(tiles),
            'exact_pair_checks': len(tiles)*(len(tiles)-1)//2,
            'metric_y_coefficient': D, 'integer_coordinates': True,
            'congruence': True, 'containment': True, 'area_equality': True,
            'pairwise_disjoint_interiors': True}


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O.')
    ap = argparse.ArgumentParser()
    ap.add_argument('certificate', type=Path)
    args = ap.parse_args()
    report = check(args.certificate)
    args.certificate.with_suffix('.verified.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report))
