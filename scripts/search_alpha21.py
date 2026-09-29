#!/usr/bin/env python3
"""Exact convex-frontier tiling search, without an a priori coordinate grid.

Coordinates (x,y) denote (x,y*sqrt(15)). All arithmetic is rational. A convex
uncovered corner forces a tile vertex there and a tile edge on its boundary
ray. The six angle/side choices enumerate every such tile. The search has an
explicit node cap; only exhaustive completion is reported as UNSAT.
"""
from fractions import Fraction as F
from collections import Counter, defaultdict
from functools import cmp_to_key
from math import isqrt
from pathlib import Path
import argparse, json, time, hashlib, sys

if not __debug__:
    raise SystemExit('Assertions required; do not run with -O.')

P=lambda x,y:(F(x),F(y))
add=lambda a,b:(a[0]+b[0],a[1]+b[1])
sub=lambda a,b:(a[0]-b[0],a[1]-b[1])
mul=lambda a,t:(a[0]*t,a[1]*t)
det=lambda a,b:a[0]*b[1]-a[1]*b[0]
dot=lambda a,b:a[0]*b[0]+15*a[1]*b[1]
cross=lambda a,b,c:det(sub(b,a),sub(c,a))
def length(a):
    z=dot(a,a); n,d=isqrt(z.numerator),isqrt(z.denominator)
    assert n*n==z.numerator and d*d==z.denominator,z
    return F(n,d)
def compose(a,b):
    return (a[0]*b[0]-15*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def rotate(a,r):
    return (r[0]*a[0]-15*r[1]*a[1],r[1]*a[0]+r[0]*a[1])
ANGLES=(('alpha',(F(7,8),F(1,8)),(3,4)),
        ('beta',(F(11,16),F(3,16)),(2,4)),
        ('gamma',(F(-1,4),F(1,4)),(2,3)))

# Every sum of tile angles strictly between zero and pi. Adding one tile
# angle to a sum <pi gives a sum <2pi, so a positive sine is exactly the test.
FANS={(F(1),F(0)):(0,0,0)}
todo=[(F(1),F(0))]
while todo:
    r=todo.pop()
    for i,(_,angle,_) in enumerate(ANGLES):
        q=compose(r,angle)
        if q[1]>0 and q not in FANS:
            inventory=list(FANS[r]);inventory[i]+=1
            FANS[q]=tuple(inventory);todo.append(q)

OUTER=(P(0,0),P(21,0),P(F(21,2),F(3,2)))
AREA2=F(3,2)
assert sum(det(a,b) for a,b in zip(OUTER,OUTER[1:]+OUTER[:1]))==21*AREA2

def edges(tr):
    return list(zip(tr,tr[1:]+tr[:1]))
def separate(a,b):
    return any(all(cross(p,q,z)<=0 for z in b) for p,q in edges(a))
def overlap(a,b):
    return not separate(a,b) and not separate(b,a)
def contains(tr):
    return all(cross(a,b,p)>=0 for a,b in edges(OUTER) for p in tr)
def on(p,a,b):
    return cross(a,b,p)==0 and dot(sub(p,a),sub(p,b))<=0

def canonical_boundary(segs):
    """Atomize, cancel opposite traces, then erase straight subdivision points."""
    vertices={p for e in segs for p in e}
    cnt=Counter()
    for a,b in segs:
        pts=[p for p in vertices if on(p,a,b)]
        pts.sort(key=lambda p:dot(sub(p,a),sub(b,a)))
        for x,y in zip(pts,pts[1:]):
            cnt[x,y]+=1
    boundary=set()
    for a,b in set(cnt):
        n=cnt[a,b]-cnt[b,a]
        assert n in (-1,0,1),(a,b,n)
        if n==1:
            boundary.add((a,b))
    changed=True
    while changed:
        changed=False
        incoming=defaultdict(list);outgoing=defaultdict(list)
        for a,b in boundary:
            incoming[b].append(a);outgoing[a].append(b)
        for p in sorted(set(incoming)&set(outgoing)):
            if len(incoming[p])==len(outgoing[p])==1:
                a,b=incoming[p][0],outgoing[p][0]
                if cross(a,p,b)==0 and dot(sub(p,a),sub(b,p))>0:
                    boundary.remove((a,p));boundary.remove((p,b));boundary.add((a,b))
                    changed=True;break
    return tuple(sorted(boundary))

def half(a):
    return 0 if a[1]>0 or (a[1]==0 and a[0]>=0) else 1
def anglecmp(a,b):
    x,y=a[0],b[0]
    if half(x)!=half(y):return -1 if half(x)<half(y) else 1
    z=det(x,y)
    if z:return -1 if z>0 else 1
    return 0

def convex_sectors(boundary):
    at=defaultdict(list)
    for a,b in boundary:
        at[a].append((sub(b,a),'out',b))
        at[b].append((sub(a,b),'in',a))
    for p in sorted(at):
        rays=sorted(at[p],key=cmp_to_key(anglecmp))
        for i,(d,kind,q) in enumerate(rays):
            r,next_kind,s=rays[(i+1)%len(rays)]
            if kind=='out' and next_kind=='in' and det(d,r)>0:
                den=length(d)*length(r)
                phi=(dot(d,r)/den,det(d,r)/den)
                yield p,d,r,phi

def possibilities(sector,placed):
    p,d,r,phi=sector
    if phi not in FANS:
        return []
    unit=mul(d,1/length(d));ans=[]
    for name,angle,(x,y) in ANGLES:
        remainder=compose(phi,(angle[0],-angle[1]))
        if remainder not in FANS:
            continue
        for a,b in ((x,y),(y,x)):
            tr=(p,add(p,mul(unit,a)),add(p,mul(rotate(unit,angle),b)))
            assert cross(*tr)==AREA2,(name,a,b,tr,cross(*tr))
            if contains(tr) and not any(overlap(tr,old) for old in placed):
                ans.append((name,a,b,tr))
    return ans

def enc(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,(tuple,list)):return [enc(z) for z in x]
    if isinstance(x,dict):return {k:enc(v) for k,v in x.items()}
    return x

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--max-nodes',type=int,default=200000)
    ap.add_argument('--seconds',type=int,default=300);ap.add_argument('--output',required=True,help='Write the complete proof record to this explicit path')
    args=ap.parse_args();start=time.monotonic();nodes=[];memo={};stats=Counter();solution=None
    class Budget(Exception):pass
    def visit(boundary,placed):
        nonlocal solution
        if boundary in memo:
            stats['memo_hits']+=1
            return memo[boundary]
        if len(nodes)>=args.max_nodes or time.monotonic()-start>args.seconds:raise Budget
        idx=len(nodes);memo[boundary]=idx;nodes.append(None);stats['depth_'+str(len(placed))]+=1
        if len(nodes)%1000==0:
            print(json.dumps({'nodes':len(nodes),'depth':len(placed),'seconds':round(time.monotonic()-start,2)}),flush=True)
        if len(placed)==21:
            assert not boundary,boundary
            solution=placed;nodes[idx]={'depth':21,'result':'SAT'};return idx
        choices=[]
        for sector in convex_sectors(boundary):
            opts=possibilities(sector,placed)
            choices.append((len(opts),sector,opts))
            if not opts:break
        assert choices,('No convex sector',boundary,len(placed))
        _,sector,opts=min(choices,key=lambda z:(z[0],z[1][0]))
        node={'depth':len(placed),'corner':sector,'children':[]}
        nodes[idx]=node
        for name,a,b,tr in opts:
            child_boundary=canonical_boundary(list(boundary)+[(q,p) for p,q in edges(tr)])
            child=visit(child_boundary,placed+[tr])
            node['children'].append({'angle':name,'first_side':a,'second_side':b,'triangle':tr,'node':child})
            if solution is not None:break
        node['result']='SAT' if solution is not None else 'UNSAT'
        return idx
    status='UNSAT'
    try:
        visit(canonical_boundary(edges(OUTER)),[])
        if solution is not None:status='SAT'
    except Budget:
        status='INCOMPLETE_BUDGET'
    result=enc({'status':status,'nodes':len(nodes),'stats':dict(stats),'fan_count':len(FANS),'solution':solution,'tree':nodes,'target':OUTER,'D':15,'tile_sides':[2,3,4]})
    data=json.dumps(result,separators=(',',':'))+'\n';Path(args.output).write_text(data)
    print(json.dumps({k:v for k,v in result.items() if k not in ('tree','solution')},indent=2))
    print('certificate_sha256',hashlib.sha256(data.encode()).hexdigest())

if __name__=='__main__':main()
