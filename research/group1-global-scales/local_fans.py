#!/usr/bin/env python3
"""Investigate complete fans at a prescribed W56 boundary-strip junction.

This only tests the specified partial patches; it is not a W56 exclusion.
"""
from fractions import Fraction as F
import json
from pathlib import Path
from pruned_search import E,Instance,PrunedSearch

def point(x,y): return F(x),F(y)/40
def L(i): return point(F(23*i,3),F(10*i,3))
def encode(t): return [[str(x),str(40*y)] for x,y in t]

def setup():
    s=PrunedSearch(Instance('G1-W',(6,5,9),(54,56,30),56,(2,3),2),
                   seconds=60,use_angles=True)
    strip=[E.triangle((L(i),E.add(L(i),point(6,0)),L(i+1))) for i in range(6)]
    return s,strip

def fans(s,placed,vertex,out,inc,partial=()):
    if E.cross(out,inc)==0 and E.dot(out,inc,s.D)>0:
        yield partial
        return
    if E.cross(out,inc)<=0:
        raise ArithmeticError('Fan recursion left a convex sector')
    for t in E.placements(s.template,(None,vertex,out,inc),s.target,
                          placed+partial,s.D):
        other=[E.sub(q,vertex) for q in t if q!=vertex]
        radial=[r for r in other if E.cross(out,r)!=0]
        if len(radial)!=1: raise ArithmeticError('Ambiguous next fan ray')
        yield from fans(s,placed,vertex,radial[0],inc,partial+(t,))

def force(s,placed):
    forced=[]
    for _ in range(57):
        boundary=E.atomic_boundary(s.target,placed)
        if not s.residual_valid(boundary):
            return 'FILTER_REJECTED',forced,None
        sectors=E.convex_sectors(boundary,s.D)
        choices=[(len(ps),sec,ps) for sec in sectors
                 for ps in [E.placements(s.template,sec,s.target,placed,s.D)]]
        size,sector,best=min(choices,key=lambda r:r[0])
        if size==0:return 'NO_TILE_AT_CONVEX_VERTEX',forced,sector[1]
        if size>1:return 'UNRESOLVED',forced,None
        forced.append(best[0]);placed=placed+(best[0],)
    raise ArithmeticError('Too many forced triangles')

def run(junction=2):
    s,strip=setup()
    for i in range(1,junction):
        strip.append(E.triangle((L(i),E.add(L(i-1),point(6,0)),
                                  E.add(L(i),point(6,0)))))
    initial=tuple(strip)
    vertex=L(junction)
    out=E.sub(E.add(L(junction-1),point(6,0)),vertex)
    inc=point(6,0)
    reports=[]
    for patch in fans(s,initial,vertex,out,inc):
        status,forced,dead_vertex=force(s,initial+patch)
        reports.append({'fan':[encode(t) for t in patch],
                        'status':status,'forced':[encode(t) for t in forced],
                        'dead_vertex':encode([dead_vertex])[0] if dead_vertex else None})
    return {'junction':junction,'fans':reports,
            'scope':'Only this fixed six-c-edge boundary strip and its specified preceding mates',
            'full_Erdos634_solved':False}

if __name__=='__main__':
    report=run()
    Path(__file__).with_name('W56-junction2-fans.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'fans':len(report['fans']),
          'statuses':[r['status'] for r in report['fans']]},indent=2))
