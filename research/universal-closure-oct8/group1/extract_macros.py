#!/usr/bin/env python3
"""Exploratory exact same-orientation union boundaries from a fixed seed."""
from collections import defaultdict
from fractions import Fraction as F
from math import gcd
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def mul(p, q):
    return (p[0]*q[0]-2*p[1]*q[1], p[0]*q[1]+p[1]*q[0])


def primitive(p):
    x, y = p
    d = gcd(x, y)
    x, y = x//d, y//d
    return (-x, -y) if x < 0 or (x == 0 and y < 0) else (x, y)


def unit(h):
    z = (F(-1, 3), F(2 if h >= 0 else -2, 3))
    q = (F(1), F(0))
    for _ in range(abs(h)):
        q = mul(q, z)
    den = q[0].denominator*q[1].denominator
    return primitive((int(den*q[0]), int(den*q[1])))


def main():
    data = json.loads((HERE/'W224_m3_p1.certificate.json').read_text())
    den = data['denominator']
    heights = {unit(h): h for h in range(-3, 2)}
    groups = defaultdict(list)
    for t in data['triangles']:
        sig = []
        for a, b in zip(t, t[1:]+t[:1]):
            v = (b[0]-a[0], b[1]-a[1])
            length2 = (v[0]**2+2*v[1]**2)//den**2
            sig.append((length2, heights[primitive(v)]))
        groups[tuple(sorted(sig))].append(t)
    components = []
    for sig, triangles in groups.items():
        parent = list(range(len(triangles)))

        def root(i):
            while parent[i] != i:
                i = parent[i]
            return i

        edge_lists = []
        for t in triangles:
            ee = []
            for a, b in zip(t, t[1:]+t[:1]):
                d = primitive((b[0]-a[0], b[1]-a[1]))
                key = (*d, d[0]*a[1]-d[1]*a[0])
                aa = d[0]*a[0]+d[1]*a[1]
                bb = d[0]*b[0]+d[1]*b[1]
                ee.append((key, min(aa, bb), max(aa, bb)))
            edge_lists.append(ee)
        for i, ee in enumerate(edge_lists):
            for j in range(i):
                if any(k == l and max(a, c) < min(b, d)
                       for k, a, b in ee for l, c, d in edge_lists[j]):
                    parent[root(i)] = root(j)
        cc = defaultdict(list)
        for i, t in enumerate(triangles):
            cc[root(i)].append(t)
        components.extend((sig, ts) for ts in cc.values())
    report = []
    for sig, triangles in components:
        lines = defaultdict(lambda: defaultdict(int))
        endpoints = {}
        for t in triangles:
            for a, b in zip(t, t[1:]+t[:1]):
                a, b = tuple(a), tuple(b)
                d = primitive((b[0]-a[0], b[1]-a[1]))
                intercept = d[0]*a[1]-d[1]*a[0]
                key = (*d, intercept)
                aa = d[0]*a[0]+d[1]*a[1]
                bb = d[0]*b[0]+d[1]*b[1]
                sign = 1 if bb > aa else -1
                lines[key][min(aa, bb)] += sign
                lines[key][max(aa, bb)] -= sign
                endpoints[(key, aa)] = a
                endpoints[(key, bb)] = b
        outgoing = defaultdict(list)
        for key, events in lines.items():
            keys = sorted(events)
            flow = 0
            for aa, bb in zip(keys, keys[1:]):
                flow += events[aa]
                if flow:
                    assert abs(flow) == 1
                    a, b = endpoints[(key, aa)], endpoints[(key, bb)]
                    if flow < 0:
                        a, b = b, a
                    outgoing[a].append(b)
        assert all(len(v) == 1 for v in outgoing.values()), 'Point-touch junction needs explicit resolution.'
        polygons = []
        while outgoing:
            start = next(iter(outgoing))
            poly, a = [], start
            while True:
                poly.append(a)
                a = outgoing.pop(a)[0]
                if a == start:
                    break
            clean = []
            for i, b in enumerate(poly):
                a, c = poly[i-1], poly[(i+1) % len(poly)]
                if (b[0]-a[0])*(c[1]-b[1]) != (b[1]-a[1])*(c[0]-b[0]):
                    clean.append(b)
            polygons.append([[str(F(x, den)), str(F(y, den))] for x, y in clean])
        report.append({'edge_signature_squared_length_height': sig,
                       'tile_count': len(triangles), 'polygons': polygons})
    (HERE/'W224_macro_exploration.json').write_text(json.dumps(report, indent=2)+'\n')
    for group in report:
        print(json.dumps(group))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O.')
    main()
