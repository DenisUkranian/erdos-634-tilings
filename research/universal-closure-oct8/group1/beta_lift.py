#!/usr/bin/env python3
"""Attach the ordinary tile grid to a W_(2,3) coordinate certificate."""
from pathlib import Path
import argparse
import json


def lift(source, target, scale):
    data = json.loads(source.read_text())
    den = data['denominator']
    assert data['metric'] == 'x^2+2y^2'
    assert data['tile'] == [6, 5, 9]
    assert data['target'] == [[0, 0], [28*scale*den, 0],
                              [23*scale*den, 10*scale*den]]
    assert den % 3 == 0
    assert len(data['triangles']) == 14*scale*scale
    n = 3*scale
    anchor = (28*scale*den, 0)
    e = (6*den, 0)
    f = (-5*den//3, 10*den//3)

    def point(i, j):
        return [anchor[0]+i*e[0]+j*f[0], anchor[1]+i*e[1]+j*f[1]]

    extra = []
    for i in range(n):
        for j in range(n-i):
            extra.append([point(i, j), point(i+1, j), point(i, j+1)])
            if i+j < n-1:
                extra.append([point(i+1, j), point(i+1, j+1), point(i, j+1)])
    assert len(extra) == n*n
    data['triangles'].extend(extra)
    data['target'] = [[0, 0], [46*scale*den, 0], [23*scale*den, 10*scale*den]]
    assert len(data['triangles']) == 23*scale*scale
    data['scope'] = (f'Beta scale{scale} seed obtained from W scale{scale} '
                     f'by an ordinary{3*scale}-fold quadratic corner.')
    target.write_text(json.dumps(data, indent=2)+'\n')


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O.')
    ap = argparse.ArgumentParser()
    ap.add_argument('source', type=Path)
    ap.add_argument('target', type=Path)
    ap.add_argument('--scale', type=int, required=True)
    args = ap.parse_args()
    lift(args.source, args.target, args.scale)
