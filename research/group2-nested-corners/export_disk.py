#!/usr/bin/env python3
"""Export rational Eisenstein-coordinate triangles to a coordinate-free disk.

The independent disk verifier receives only lengths and incidence lists.
"""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
from math import isqrt, lcm
from pathlib import Path


def cross(p, q, r):
    return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])


def ccw(t):
    points = [tuple(Fraction(x) for x in p) for p in t]
    if len(points) != 3 or cross(*points) == 0:
        raise ValueError('Expected a nondegenerate triangle')
    return points if cross(*points) > 0 else [points[0], points[2], points[1]]


def export(data):
    if data.get('coordinate_metric') != 'x^2+x*y+y^2':
        raise ValueError('Unsupported coordinate metric')
    tiles = [ccw(t) for t in data['triangles']]
    target = ccw(data['target'])
    rational_vertices = sorted({p for t in tiles for p in t})
    scale = lcm(*(x.denominator for p in rational_vertices+target for x in p))
    # Integer affine coordinates make all side-incidence decisions exact and
    # keep the exporter independent of any construction grid.
    def integer_point(p):
        return tuple(int(x*scale) for x in p)
    tiles = [[integer_point(p) for p in t] for t in tiles]
    target = [integer_point(p) for p in target]
    vertices = sorted({p for t in tiles for p in t})
    ids = {p: i for i, p in enumerate(vertices)}
    if not set(target) <= set(vertices):
        raise ValueError('A target corner is not a tile vertex')

    def length(p, q):
        x, y = p[0]-q[0], p[1]-q[1]
        square = x*x+x*y+y*y
        root = isqrt(square)
        if root <= 0 or root*root != square or root % scale:
            raise ValueError('A whole side or atomic segment has nonintegral length')
        return root//scale

    def subdivide(p, q):
        interior = [r for r in vertices if cross(p, q, r) == 0
                    and min(p[0], q[0]) <= r[0] <= max(p[0], q[0])
                    and min(p[1], q[1]) <= r[1] <= max(p[1], q[1])]
        interior.sort(key=lambda r: ((r[0]-p[0])*(q[0]-p[0])
                                     +(r[1]-p[1])*(q[1]-p[1])))
        if interior[0] != p or interior[-1] != q:
            raise ValueError('A side endpoint disappeared')
        if sum(length(r, s) for r, s in zip(interior, interior[1:])) != length(p, q):
            raise ValueError('Incorrect side subdivision')
        return [ids[r] for r in interior]

    faces = []
    for tile in tiles:
        edges = list(zip(tile, tile[1:]+tile[:1]))
        lengths = [length(p, q) for p, q in edges]
        if sorted(lengths) != sorted(data['tile']):
            raise ValueError('Noncongruent source triangle')
        faces.append({'side_lengths': lengths,
                      'side_vertices': [subdivide(p, q) for p, q in edges]})
    return {'schema': 'integer-triangle-disk-v1', 'tile_sides': data['tile'],
            'faces': faces, 'target_corners': [ids[p] for p in target],
            'target_side_lengths': [length(p, q)
                                   for p, q in zip(target, target[1:]+target[:1])]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    source = args.source.read_bytes()
    result = export(json.loads(source))
    raw = (json.dumps(result, separators=(',', ':'))+'\n').encode()
    args.output.write_bytes(raw)
    flats = Counter(v for f in result['faces'] for s in f['side_vertices'] for v in s[1:-1])
    report = {'status': 'EXPORTED', 'N': len(result['faces']),
              'genuine_T_junction_vertices': len(flats),
              'source_sha256': hashlib.sha256(source).hexdigest(),
              'export_sha256': hashlib.sha256(raw).hexdigest(),
              'coordinates_in_export': False, 'atomic_lengths_in_export': False,
              'full_Erdos634_solved': False}
    output = json.dumps(report, indent=2)+'\n'
    if args.report:
        args.report.write_text(output)
    print(output, end='')


if __name__ == '__main__':
    main()
