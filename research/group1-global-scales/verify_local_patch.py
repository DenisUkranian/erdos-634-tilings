#!/usr/bin/env python3
"""Independent exact verification of an eleven-tile partial W56 patch."""
from fractions import Fraction as F
from itertools import combinations
import json
from math import isqrt
from pathlib import Path

ROOT=Path(__file__).resolve().parent
def p(x,y):return F(x),F(y)
def sub(a,b):return a[0]-b[0],a[1]-b[1]
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def det(a,b,c):return cross(sub(b,a),sub(c,a))
def norm(v):return v[0]*v[0]+2*v[1]*v[1]
def edges(t):return list(zip(t,t[1:]+t[:1]))
def ccw(t):return t if det(*t)>0 else [t[0],t[2],t[1]]
def inside(t,z):return all(det(a,b,z)>=0 for a,b in edges(t))
def overlap(t,u):
    return not any(all(det(a,b,z)<=0 for z in w)
                   for v,w in [(t,u),(u,t)] for a,b in edges(v))
def on(a,b,z):
    return det(a,b,z)==0 and min(a[0],b[0])<=z[0]<=max(a[0],b[0]) and min(a[1],b[1])<=z[1]<=max(a[1],b[1])
def enc(t):return [[str(x),str(y)] for x,y in t]

def run():
    L=lambda i:p(F(23*i,3),F(10*i,3))
    plus6=lambda z:p(z[0]+6,z[1])
    target=[p(0,0),p(56,0),p(46,20)]
    tiles=[[L(i),plus6(L(i)),L(i+1)] for i in range(6)]
    tiles.append([L(1),p(6,0),plus6(L(1))])
    V=L(2);A=p(F(41,3),F(10,3));P=p(F(55,3),F(2,3))
    tiles += [[V,A,P],[V,P,p(20,4)],
              [V,p(F(173,9),F(40,9)),p(F(73,3),F(20,3))]]
    tiles.append([p(F(64,3),F(20,3)),p(29,10),p(23,10)])
    tiles=[ccw(t) for t in tiles]
    if not all(sorted(norm(sub(a,b)) for a,b in edges(t))==[25,36,81] for t in tiles):
        raise AssertionError('Tile metric failure')
    if not all(inside(target,z) for t in tiles for z in t):
        raise AssertionError('Containment failure')
    pairs=list(combinations(tiles,2))
    if any(overlap(t,u) for t,u in pairs):
        raise AssertionError('Interior overlap')
    vertices=set(z for t in tiles for z in t)
    atom_lengths=set()
    for t in tiles:
        for a,b in edges(t):
            points=sorted(z for z in vertices if on(a,b,z))
            for z,w in zip(points,points[1:]):
                squared=norm(sub(z,w));root=isqrt(squared.numerator)
                if squared.denominator!=1 or root*root!=squared.numerator:
                    raise AssertionError('Nonintegral known seam atom')
                atom_lengths.add(root)
    report={'status':'PASS','metric':'dx^2 + 2 dy^2','tile_sides':[6,5,9],
            'target_sides':[56,54,30],'target_tile_count':56,
            'placed_tile_count':len(tiles),'pairwise_checks':len(pairs),
            'known_seam_atom_lengths':sorted(atom_lengths),
            'remaining_area_in_tile_units':56-len(tiles),
            'fan_at_L2':'alpha + beta + alpha; no gamma tile at L2',
            'partial_patch_only':True,'extendibility':'UNKNOWN',
            'full_Erdos634_solved':False}
    certificate={'target':enc(target),'tiles':[enc(t) for t in tiles],**report}
    (ROOT/'W56-local-escape-patch.json').write_text(json.dumps(certificate,indent=2)+'\n')
    (ROOT/'local-patch-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

if __name__=='__main__':print(json.dumps(run(),indent=2))
