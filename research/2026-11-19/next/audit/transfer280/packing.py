"""Build and independently verify the 277-unit partial placement in the 280 target."""
from fractions import Fraction as F
from math import gcd,lcm
from collections import defaultdict
from pathlib import Path
import argparse
import json
from itertools import combinations

HERE=Path(__file__).resolve().parent
def sub(a,b):return a[0]-b[0],a[1]-b[1]
def add(a,b):return a[0]+b[0],a[1]+b[1]
def mul(a,b):return a[0]*b[0]-2*a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def orient(a,b,c):return det(sub(b,a),sub(c,a))
def norm(v):return v[0]*v[0]+2*v[1]*v[1]
def edges(t):return zip(t,t[1:]+t[:1])

def triangulate():
    def v(a,b):return 50-5*a+2*b,4*b
    for i in range(10):
        for j in range(10-i):
            yield (v(i,j),v(i+1,j),v(i,j+1))
            if i+j<9:yield (v(i+1,j+1),v(i+1,j),v(i,j+1))

def build(src,path):
    lines=src.read_text().splitlines();d=F(1,int(lines[0]))
    tris=list(triangulate())
    for l in lines[1:]:
        w=list(map(int,l.split()));pts=[]
        for x,y in zip(w[::2],w[1::2]):
            pts.append(add((50,0),mul((d*x,-d*y),(F(1,3),F(2,3)))))
        tris.append(tuple(pts))
    assert len(tris)==277
    den=lcm(*(F(c).denominator for t in tris for pt in t for c in pt))
    data=dict(axial_metric=[1,2],denominator=den,grid_tiles=100,theta_tiles=177,
              target_scaled=[[0,0],[140*den,0],[70*den,40*den]],
              tiles_scaled=[[[int(x*den),int(y*den)] for x,y in t] for t in tris])
    path.write_text(json.dumps(data,separators=(',',':'))+'\n')

def verify(path):
    b=json.loads(path.read_text());d=b['denominator'];outer=b['target_scaled'];ts=b['tiles_scaled']
    assert outer==[[0,0],[140*d,0],[70*d,40*d]] and len(ts)==277
    def ccw(s):
        u=list(map(tuple,s))
        if orient(*u)<0:u.reverse()
        return u
    ts=list(map(ccw,ts));out=ccw(outer)
    for t in ts:
        assert sorted(norm(sub(v,w)) for v,w in edges(t))==[25*d*d,36*d*d,81*d*d]
        assert orient(*t)==20*d*d
        assert all(orient(x,y,p)>=0 for x,y in edges(out) for p in t)
    for a,b in combinations(ts,2):
        assert any(all(orient(x,y,v)<=0 for v in t) for f,t in [(a,b),(b,a)] for x,y in edges(f))
    assert orient(*out)==280*20*d*d
    leftover=orient(*out)-sum(orient(*t) for t in ts)
    events=defaultdict(lambda:defaultdict(int))
    for polygon,sg in [(out,1)]+[(t,-1) for t in ts]:
        for a,b in edges(polygon):
            u,v=sub(b,a);g=gcd(u,v);u//=g;v//=g
            if (u,v)<(0,0):u,v=-u,-v
            ev=events[u,v,u*a[1]-v*a[0]];ev[a]+=sg;ev[b]-=sg
    boundary=set()
    for ev in events.values():
        sign=0;prev=None
        for pt,delta in sorted(ev.items()):
            if not delta:continue
            if sign:boundary.add((prev,pt) if sign==1 else (pt,prev))
            sign+=delta;prev=pt
            assert abs(sign)<=1
        assert sign==0
    hole=[(630,180),(720,180),(690,240),(648,216),(645,210),(699,210)]
    assert d==9 and boundary==set(edges(hole))
    assert norm(sub(hole[4],hole[3]))==d*d and orient(*hole[2:5])>0 and orient(*hole[3:6])>0
    print(f"verified 277 tiles, {len(ts)*(len(ts)-1)//2} disjoint pairs, area deficit {leftover//(20*d*d)}, coordinate denominator {d}")
    print("uncovered hexagon verified; its length-1 edge has two convex ends")

if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path);args=ap.parse_args()
    path=HERE/'packing277.json'
    if args.source:build(args.source,path)
    verify(path)
