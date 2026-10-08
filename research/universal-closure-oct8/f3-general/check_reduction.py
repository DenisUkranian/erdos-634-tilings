#!/usr/bin/env python3
"""Independent exact current/length checker. Does not import constructor."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
from math import gcd,lcm
import argparse,hashlib,json

def cross(p,q):return p[0]*q[1]-p[1]*q[0]
def sub(p,q):return p[0]-q[0],p[1]-q[1]
def norm(p):return p[0]*p[0]+p[0]*p[1]+p[1]*p[1]
def parse(poly):return [tuple(map(F,p))for p in poly]
def area(poly):return sum(cross(poly[i],poly[(i+1)%len(poly)])for i in range(len(poly)))
def inside(p,poly):return all(cross(sub(poly[(i+1)%len(poly)],q),sub(p,q))>=0 for i,q in enumerate(poly))
def require(ok,msg):
    if not ok:raise ValueError(msg)

def verify(path):
    raw=path.read_bytes();d=json.loads(raw);a,b,c=d['tile'];P=parse(d['target']);Q=parse(d['omitted_polygon']);T=[parse(t)for t in d['partial_triangles']]
    require(c*c==a*a+a*b+b*b,'norm triple');require(area(P)>0 and area(Q)>0,'positive orientations')
    require(all(cross(sub(Q[(i+1)%4],Q[i]),sub(Q[(i+2)%4],Q[(i+1)%4]))>0 for i in range(4)),'strictly convex omitted quad')
    require(all(inside(p,P)for p in Q),'omitted containment')
    currents=defaultdict(lambda:defaultdict(int))
    def boundary(poly,weight):
        for i,p in enumerate(poly):
            q=poly[(i+1)%len(poly)];dx,dy=sub(q,p);require(dx!=0 or dy!=0,'zero edge');den=lcm(dx.denominator,dy.denominator);vx,vy=int(dx*den),int(dy*den);gg=gcd(abs(vx),abs(vy));vx//=gg;vy//=gg
            if vx<0 or(vx==0 and vy<0):vx=-vx;vy=-vy
            v=(vx,vy);key=(vx,vy,cross(v,p));tp=vx*p[0]+vy*p[1];tq=vx*q[0]+vy*q[1];sign=1 if tq>tp else -1;lo,hi=sorted((tp,tq));currents[key][lo]+=weight*sign;currents[key][hi]-=weight*sign
    for i,t in enumerate(T):
        require(area(t)>0,f'orientation{i}');require(sorted(norm(sub(t[(j+1)%3],t[j]))for j in range(3))==sorted((a*a,b*b,c*c)),f'length{i}');require(all(inside(p,P)for p in t),f'containment{i}');boundary(t,1)
    boundary(Q,1);boundary(P,-1)
    nonzero=[]
    for line,events in currents.items():
        value=0;xs=sorted(events)
        for j,x in enumerate(xs):
            value+=events[x]
            if j+1<len(xs)and value!=0:nonzero.append((str(line),str(x),str(xs[j+1]),value))
        require(value==0,'unbalanced infinite segment')
    require(not nonzero,f'nonzero exact boundary intervals:{nonzero[:3]}')
    require(len(T)==d['partial_count']==d['count']-d['omitted_count'],'count');require(area(Q)==a*b*d['omitted_count'],'omitted area');require(area(P)==a*b*d['count'],'target area')
    # Positive currents determine multiplicity exactly: outside P it is zero,
    # and zero boundary makes it constant in every component of the edge
    # arrangement. Thus T plus the one convex Q form a partition of P.
    return {'status':'PASS_CONDITIONAL_REDUCTION','sha256':hashlib.sha256(raw).hexdigest(),'tiles':len(T),'omitted_tiles':d['omitted_count'],'supporting_lines':len(currents),'nonzero_boundary_intervals':0,'positive_current_partition':True,'claims_omitted_quad_is_tilable':False}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('path',nargs='?',type=Path,default=Path(__file__).with_name('f3_4830_corner480_reduction.json'));ar=ap.parse_args();r=verify(ar.path);ar.path.with_suffix('.verified.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
if __name__=='__main__':main()
