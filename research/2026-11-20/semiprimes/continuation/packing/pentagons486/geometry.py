"""Verify an exact shell on the 3431 board and optionally lift an arbitrary region tiling."""
from argparse import ArgumentParser
from collections import Counter,defaultdict
from math import gcd,isqrt,lcm
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
EXPECTED={'hex538':(538,6,1),'region337':(337,9,3),'oct538':(538,8,2)}


def det(p,q):
    return p[0]*q[1]-p[1]*q[0]


def diff(p,q):
    return (p[0]-q[0],p[1]-q[1])


def norm(p):
    return p[0]**2+p[0]*p[1]+p[1]**2


def edges(vertices):
    return zip(vertices,vertices[1:]+vertices[:1])


def doubled_area(poly):
    return sum(det(p,q) for p,q in edges(poly))


def ccw(poly):
    return poly if doubled_area(poly)>0 else poly[::-1]


def integer_vertices(data):
    assert all(len(p)==2 and all(type(x) is int for x in p) for p in data)
    return tuple(map(tuple,data))


def intersect(a,b,c,d):
    if any(max(min(a[i],b[i]),min(c[i],d[i]))>min(max(a[i],b[i]),max(c[i],d[i])) for i in (0,1)):
        return False
    ab,cd=diff(b,a),diff(d,c)
    return (det(ab,diff(c,a))*det(ab,diff(d,a))<=0 and
            det(cd,diff(a,c))*det(cd,diff(b,c))<=0)


def simple(poly):
    n=len(poly)
    assert n>=3 and len(set(poly))==n and doubled_area(poly)>0
    lines=list(edges(poly))
    for i,(a,b) in enumerate(lines):
        assert det(diff(b,a),diff(poly[(i+2)%n],b))!=0
        for j in range(i+1,n):
            if j==i+1 or (i==0 and j==n-1):
                continue
            assert not intersect(a,b,*lines[j])


def translated(poly,shift):
    return tuple((x+shift[0],y+shift[1]) for x,y in poly)


def scaled(poly,factor):
    return tuple((factor*x,factor*y) for x,y in poly)


def check_tiles(tiles,den,count):
    assert len(tiles)==len({tuple(sorted(t)) for t in tiles})==count
    sizes=[(den*k)**2 for k in (7,33,37)]
    for t in tiles:
        assert len(t)==3 and sorted(norm(diff(q,p)) for p,q in edges(t))==sizes


def boundary_identity(positive,target):
    """Compare oriented interval jumps separately on each individual supporting line."""
    lines=defaultdict(Counter)
    for sign,poly in [(1,p) for p in positive]+[(-1,target)]:
        assert doubled_area(poly)>0
        for p,q in edges(poly):
            dx,dy=diff(q,p)
            g=gcd(dx,dy)
            dx,dy=dx//g,dy//g
            if (dx,dy)<(0,0):
                dx,dy=-dx,-dy
            jumps=lines[dx,dy,dx*p[1]-dy*p[0]]
            jumps[p]+=sign
            jumps[q]-=sign
    assert all(not any(jumps.values()) for jumps in lines.values())


