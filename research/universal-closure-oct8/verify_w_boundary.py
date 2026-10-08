#!/usr/bin/env python3
"""Independent exact positioned-boundary check of the W certificates.

Coordinates represent (x,y*sqrt(2))/denominator.  Every tile is positively
oriented. Cancellation of its signed atomic boundary against the target
forces multiplicity one almost everywhere, and hence is a tiling proof.
"""
import argparse
from collections import defaultdict
import hashlib
import json
from math import gcd
from pathlib import Path


def verify(path):
    data = json.loads(path.read_text())
    assert data['metric'] == 'x^2+2y^2'
    den = data['denominator']
    assert isinstance(den, int) and den > 0
    events = defaultdict(lambda: defaultdict(int))
    target = data['target']
    tiles = data['triangles']
    wanted = sorted(den*den*s*s for s in data['tile'])
    def add(poly, weight, tile=False):
        assert len(poly) == 3 and all(len(p)==2 and all(isinstance(v,int) for v in p) for p in poly)
        twice_area = 0
        lengths = []
        for a,b in zip(poly, poly[1:]+poly[:1]):
            dx,dy = b[0]-a[0],b[1]-a[1]
            twice_area += a[0]*b[1]-a[1]*b[0]
            lengths.append(dx*dx+2*dy*dy)
            g = gcd(dx,dy)
            assert g > 0
            u,v = dx//g,dy//g
            if (u,v) < (0,0): u,v = -u,-v
            key = (u,v,u*a[1]-v*a[0])
            s,t = u*a[0]+v*a[1],u*b[0]+v*b[1]
            lo,hi = min(s,t),max(s,t)
            sign = weight*(1 if s<t else -1)
            events[key][lo] += sign
            events[key][hi] -= sign
        assert twice_area > 0
        if tile: assert sorted(lengths) == wanted
        return sorted(lengths)
    target_lengths = add(target,-1)
    for tri in tiles: add(tri,1,True)
    assert all(value == 0 for line in events.values() for value in line.values())
    return dict(status='PASS', tile_count=len(tiles), line_count=len(events),
                event_locations=sum(map(len,events.values())),
                target_squared_sides_scaled=target_lengths,
                denominator=den, tile=data['tile'],
                certificate_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                method='Exact signed boundary cancellation, distinct from pairwise intersection checker')


if __name__=='__main__':
    if not __debug__: raise RuntimeError('Assertions must be enabled')
    p=argparse.ArgumentParser();p.add_argument('certificate',type=Path);p.add_argument('report',type=Path);a=p.parse_args()
    result=verify(a.certificate);a.report.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
