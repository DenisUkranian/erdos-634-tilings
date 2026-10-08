#!/usr/bin/env python3
"""Check the full 4830 witness independently by exact positioned boundaries.

Does not import constructors, reducers, tiling verifiers, or solvers.
After normalizing each triangle's vertex order, positive oriented congruent
triangles and equality of currents force
multiplicity one throughout the target, hence no overlaps and no holes.
"""
from collections import defaultdict
import hashlib
import json
from math import gcd
from pathlib import Path
import argparse


def check(path):
    j=json.loads(path.read_text())
    assert j['format']=='ERDOS634_INTEGER_EISENSTEIN_TILING_V1'
    d=j['denominator'];assert isinstance(d,int) and d>0
    assert j['tile']==[24,11,31] and j['count']==4830 and len(j['triangles'])==4830
    target=j['target'];triangles=j['triangles']
    events=defaultdict(lambda:defaultdict(int))
    def polygon(poly,weight,wanted):
        assert len(poly)==3 and all(len(p)==2 and all(type(x) is int for x in p) for p in poly)
        orientation=sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(poly,poly[1:]+poly[:1]))
        assert orientation!=0
        if orientation<0:poly=list(reversed(poly))
        side_squares=[];area=0
        for a,b in zip(poly,poly[1:]+poly[:1]):
            dx=b[0]-a[0];dy=b[1]-a[1]
            side_squares.append(dx*dx+dx*dy+dy*dy)
            area+=a[0]*b[1]-a[1]*b[0]
            g=gcd(dx,dy);assert g>0
            u,v=dx//g,dy//g
            if (u,v)<(0,0):u,v=-u,-v
            line=(u,v,u*a[1]-v*a[0])
            s=u*a[0]+v*a[1];t=u*b[0]+v*b[1]
            sign=weight*(1 if s<t else -1)
            events[line][min(s,t)]+=sign
            events[line][max(s,t)]-=sign
        assert area>0 and sorted(side_squares)==sorted(x*x*d*d for x in wanted)
        return area
    outer=polygon(target,-1,[961,1155,1426])
    total=0
    for triangle in triangles:
        total+=polygon(triangle,1,[24,11,31])
        for a,b in zip(target,target[1:]+target[:1]):
            for c in triangle:
                assert (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])>=0
    assert total==outer
    assert all(value==0 for line in events.values() for value in line.values())
    return dict(status='PASS',count=4830,tile=[24,11,31],target_sides=[961,1155,1426],
                denominator=d,positive_orientations=True,correct_metric=True,
                all_vertices_contained=True,exact_area_equality=True,
                exact_boundary_cancellation=True,line_count=len(events),
                event_positions=sum(map(len,events.values())),
                certificate_sha256=hashlib.sha256(path.read_bytes()).hexdigest())


if __name__=='__main__':
    if not __debug__:raise RuntimeError('Run with assertions enabled')
    p=argparse.ArgumentParser();p.add_argument('certificate',type=Path);p.add_argument('report',type=Path);a=p.parse_args()
    r=check(a.certificate);a.report.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
