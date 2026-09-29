"""Independent exact checks for the W/beta bridge and Bonfioli seeds.

No upstream code is imported or executed. The two optional source files are
read as coordinate data only. Obtain them from Vico Bonfioli's repository:
ElVec1o/erdos_634_proof, snapshot 2f9af59.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import combinations
from math import gcd
import argparse
import ast
import hashlib
import json
import re

if not __debug__:
    raise SystemExit("Verification requires assertions: do not run Python with -O or PYTHONOPTIMIZE.")


def cross(o, a, b):
    return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])


def plus(a, b):
    return (a[0]+b[0], a[1]+b[1])


def mult(a, k):
    return (a[0]*k, a[1]*k)


def ccw(t):
    return t if cross(*t) > 0 else (t[0], t[2], t[1])


def separated(a, b):
    return any(all(cross(t[i], t[(i+1)%3], p) <= 0 for p in s)
               for t, s in ((a,b),(b,a)) for i in range(3))


def verify(tiles, target, metric, sides):
    tiles = [ccw(t) for t in tiles]
    def d2(p, q):
        x,y=p[0]-q[0],p[1]-q[1]
        A,B,C=metric
        return A*x*x+2*B*x*y+C*y*y
    for t in tiles:
        assert cross(*t)>0
        assert sorted(d2(p,q) for p,q in combinations(t,2)) == sorted(s*s for s in sides)
        assert all(cross(target[i],target[(i+1)%len(target)],p)>=0
                   for i in range(len(target)) for p in t)
    twice_area=sum(cross(target[0],target[i],target[i+1])
                   for i in range(1,len(target)-1))
    assert sum(cross(*t) for t in tiles)==twice_area
    tested=0
    for a,b in combinations(tiles,2):
        assert separated(a,b)
        tested+=1
    return {"status":"PASS", "tile_count":len(tiles), "pairs":tested,
            "twice_area_in_coordinate_basis":str(twice_area)}


def bridge(u,v,p,q,kind):
    """kind=1 for W; kind=2 for beta. Use stacked elementary bridges."""
    assert gcd(u,v)==1 and 0<u<v and kind in (1,2)
    assert q%u==0 and kind*p>=u
    a,b,c=u*v,v*v-u*u,v*v
    n0=(kind+1)*c-u*u
    h,j=u*v,kind*p*v
    s=p*u*b
    one=[]
    def cell(i,k,offset,lower,upper):
        o=(F(offset+i*a),F(k*c))
        x,y=plus(o,(a,0)),plus(o,(0,c))
        z=plus(x,(0,c))
        if lower: one.append((o,x,y))
        if upper: one.append((x,z,y))
    for i in range(h):
        for k in range(h): cell(i,k,0,i+k<=h-1,i+k<=h-2)
    for i in range(j):
        for k in range(h): cell(i,k,s,i+k>=h,i+k>=h-1)
    U=(F(b),F(0))
    V=(F(-a*a,b),F(a*c,b))
    origin=(F(h*a),F(0))
    for i in range(p*u):
        for k in range(b):
            o=plus(origin,plus(mult(U,i),mult(V,k)))
            x,y=plus(o,U),plus(o,V)
            z=plus(x,V)
            one.extend(((o,x,z),(o,z,y)))
    tiles=[tuple(plus(x,(0,k*u*v**3)) for x in t)
           for k in range(q//u) for t in one]
    width,height=p*u*n0,q*v**3
    co=F(a*a+c*c-b*b,2*a*c)
    target=((0,0),(width,0),(width,height),(0,height))
    result=verify(tiles,target,(F(1),co,F(1)),(a,b,c))
    assert result['tile_count']==2*p*q*n0
    result.update(u=u,v=v,p=p,q=q,family='W' if kind==1 else 'beta')
    return result


def read_w63(path):
    text=path.read_text()
    raw=re.search(r'def tiles : List Tri := (\[.*?\])\s*def wit',text,re.S).group(1)
    data=ast.literal_eval(raw)
    assert all(z[1]==z[2]==0 for t in data for z in t)
    tiles=[tuple((F(z[0],8),F(z[3],8)) for z in t) for t in data]
    target=((F(0),F(0)),(F(21),F(0)),(F(9,2),F(9,2)))
    result=verify(tiles,target,(F(1),F(0),F(15)),(2,3,4))
    assert len(tiles)==63
    result.update(source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                  attribution='Vico Bonfioli, CevianTiling63.lean',
                  tile_sides=[2,3,4],target_sides=[18,21,24],scale=3)
    return result


def read_beta99(path):
    lines=path.read_text().splitlines()
    assert lines[0]=='FILE:i_99:9.txt 99 15'
    tiles=[]
    for line in lines[1:]:
        z=list(map(int,line.split()))
        assert len(z)==18
        assert all(z[i+1]==z[i+3]==0 for i in (0,6,12))
        tiles.append(tuple((F(z[i],z[i+2]),F(z[i+4],z[i+5])) for i in (0,6,12)))
    target=((F(0),F(0)),(F(33),F(0)),(F(33,2),F(9,2)))
    result=verify(tiles,target,(F(1),F(0),F(15)),(2,3,4))
    assert len(tiles)==99
    result.update(source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                  attribution='Vico Bonfioli, tiling_99_isobeta_24_24_33.txt',
                  tile_sides=[2,3,4],target_sides=[24,24,33],scale=3)
    return result


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--bonfioli-root',type=Path)
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    cases=[(1,2,1,1,1),(1,3,1,1,1),(2,3,2,2,1),(3,4,3,3,1),
           (2,3,1,2,2),(1,2,1,1,2),(1,2,1,2,1)]
    out={'bridges':[],'external_seeds':[],'arithmetic':'fractions.Fraction; all tile pairs tested'}
    for case in cases:
        r=bridge(*case);out['bridges'].append(r);print(json.dumps(r),flush=True)
    if args.bonfioli_root:
        r=args.bonfioli_root
        out['external_seeds']=[read_w63(r/'lean/Erdos634/CevianTiling63.lean'),
                              read_beta99(r/'code/engine/tilings/tiling_99_isobeta_24_24_33.txt')]
        for item in out['external_seeds']: print(json.dumps(item),flush=True)
    if args.output:
        args.output.write_text(json.dumps(out,indent=2)+'\n')
