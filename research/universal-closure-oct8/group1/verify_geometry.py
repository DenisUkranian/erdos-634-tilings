#!/usr/bin/env python3
"""Independent integer geometric checker; no imports from search or solvers."""
from pathlib import Path
import argparse
import json


def sub(a, b):
    return (a[0]-b[0], a[1]-b[1])


def det(a, b):
    return a[0]*b[1]-a[1]*b[0]


def edges(p):
    return list(zip(p, p[1:]+p[:1]))


def area2(p):
    return sum(det(a, b) for a, b in edges(p))


def norm(p):
    return p[0]*p[0]+2*p[1]*p[1]


def separated(p, q):
    return any(all(det(sub(b, a), sub(c, a)) <= 0 for c in q)
               for a, b in edges(p))


def check(path):
    d = json.loads(path.read_text())
    assert d['metric'] == 'x^2+2y^2'
    den = d['denominator']
    assert isinstance(den, int) and den > 0
    target, tiles = d['target'], d['triangles']
    assert area2(target) > 0
    wanted = sorted(a*a*den*den for a in d['tile'])
    area = 0
    for t in tiles:
        assert area2(t) > 0
        assert sorted(norm(sub(b, a)) for a, b in edges(t)) == wanted
        assert all(det(sub(b, a), sub(c, a)) >= 0 for a, b in edges(target) for c in t)
        area += area2(t)
    assert area == area2(target)
    pairs = 0
    for i, t in enumerate(tiles):
        for u in tiles[:i]:
            assert separated(t, u) or separated(u, t)
            pairs += 1
    return {'status': 'PASS', 'tile_count': len(tiles), 'exact_pair_checks': pairs,
            'metric': d['metric'], 'positive_areas': True,
            'correct_sides': True, 'contained': True,
            'area_equality': True, 'pairwise_disjoint_interiors': True}


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O so assertions execute.')
    ap = argparse.ArgumentParser()
    ap.add_argument('path', type=Path)
    args = ap.parse_args()
    report = check(args.path)
    args.path.with_suffix('.verified.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report))
