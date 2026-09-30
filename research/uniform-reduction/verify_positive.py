#!/usr/bin/env python3
"""Independent exact replay of positive triangular dissection certificates.

Does not import exact_search or its separating-axis predicates. Sutherland-
Hodgman polygon clipping is used for all pairwise interior intersections.
"""
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path

def cross(a,b,p):
    return (b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0])
def area2(p):
    return sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(p,p[1:]+p[:1]))
def lengths(p,D):
    return sorted((a[0]-b[0])**2+D*(a[1]-b[1])**2 for a,b in zip(p,p[1:]+p[:1]))
def clip(subject,boundary):
    out=list(subject)
    for a,b in zip(boundary,boundary[1:]+boundary[:1]):
        inp=out;out=[]
        for p,q in zip(inp,inp[1:]+inp[:1]):
            fp,fq=cross(a,b,p),cross(a,b,q)
            if fp>=0:out.append(p)
            if fp*fq<0:
                t=fp/(fp-fq)
                out.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])))
        if not out:break
    return out

def check(report):
    if report['status']!='TILING_FOUND':raise ValueError('Not a positive certificate')
    I=report['instance'];N=I['n'];D=report['field_D']
    def polygon(x):return tuple(tuple(F(z) for z in p) for p in x)
    outer=polygon(report['target_coordinates'])
    tiles=[polygon(t) for t in report['tile_coordinates']]
    if len(tiles)!=N:raise ValueError('Wrong tile count')
    if len(outer)!=3 or area2(outer)<=0:raise ValueError('Invalid target')
    if lengths(outer,D)!=sorted(s*s for s in I['target']):raise ValueError('Wrong target sides')
    total=0
    for t in tiles:
        if len(t)!=3 or area2(t)<=0:raise ValueError('Degenerate/reversed tile')
        if lengths(t,D)!=sorted(s*s for s in I['tile']):raise ValueError('Not congruent')
        if any(cross(a,b,p)<0 for a,b in zip(outer,outer[1:]+outer[:1]) for p in t):raise ValueError('Tile outside')
        total+=area2(t)
    if total!=area2(outer):raise ValueError('Wrong covered area')
    pairs=0
    for x,y in combinations(tiles,2):
        if area2(clip(x,y))>0:raise ValueError('Overlapping interiors')
        pairs+=1
    vertices=set(p for t in tiles for p in t)
    ts=set()
    for t in tiles:
        for a,b in zip(t,t[1:]+t[:1]):
            for p in vertices:
                if p not in (a,b) and cross(a,b,p)==0 and min(a[0],b[0])<=p[0]<=max(a[0],b[0]) and min(a[1],b[1])<=p[1]<=max(a[1],b[1]):ts.add(p)
    return {'status':'ACCEPT_POSITIVE','n':N,'pairs':pairs,'t_junction_vertices':len(ts),'search_imported':False}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('file',type=Path)
    args=p.parse_args();obj=json.loads(args.file.read_text())
    rows=obj if isinstance(obj,list) else [obj]
    print(json.dumps([check(x) for x in rows if x['status']=='TILING_FOUND'],indent=2))
