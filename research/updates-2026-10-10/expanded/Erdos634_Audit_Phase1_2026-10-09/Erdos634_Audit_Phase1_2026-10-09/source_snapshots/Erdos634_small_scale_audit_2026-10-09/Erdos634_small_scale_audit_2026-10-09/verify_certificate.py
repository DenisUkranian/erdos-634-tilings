#!/usr/bin/env python3
"""Independent exact replay of a finite convex-corner refutation tree.
Standard library only. Imports neither the search nor the certificate generator.
Uses a global recomputation of residual boundary and direct side-length
construction of all six possible incident triangles. No direction cutoff.
"""
from fractions import Fraction as Q
from collections import Counter, defaultdict
from math import isqrt
from pathlib import Path
from time import monotonic
import json,sys

class Invalid(ValueError):pass
def need(c,s):
    if not c:raise Invalid(s)
def point(p):return tuple(Q(x) for x in p)
def minus(p,q):return (p[0]-q[0],p[1]-q[1])
def plus(p,q):return (p[0]+q[0],p[1]+q[1])
def times(k,p):return (k*p[0],k*p[1])
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def turn(p,q,r):return det(minus(q,p),minus(r,p))
def ee(t):return list(zip(t,t[1:]+t[:1]))
def norm(p,D):return p[0]*p[0]+D*p[1]*p[1]
def rt(x):
    need(x>=0,'negative radicand'); a,b=isqrt(x.numerator),isqrt(x.denominator)
    need(a*a==x.numerator and b*b==x.denominator,'nonrational required length')
    return Q(a,b)
def canonical(t):
    t=tuple(t);s=turn(*t);need(s!=0,'degenerate triangle')
    if s<0:t=(t[0],t[2],t[1])
    k=min(range(3),key=lambda j:t[j]);return t[k:]+t[:k]
def within(t,p):return all(turn(a,b,p)>=0 for a,b in ee(t))
def separate(a,b):
    for t,s in ((a,b),(b,a)):
        for p,q in ee(t):
            if max(turn(p,q,r) for r in s)<=0:return True
    return False

def residual(target,tiles):
    segments=ee(target)
    for t in tiles:segments.extend((b,a) for a,b in ee(t))
    vertices=set(p for e in segments for p in e); counts=Counter()
    for a,b in segments:
        pts=sorted(p for p in vertices if turn(a,b,p)==0 and min(a,b)<=p<=max(a,b))
        for p,q in zip(pts,pts[1:]):counts[(p,q)]+=1 if a<b else -1
    out=[]
    for (a,b),n in counts.items():
        need(abs(n)<=1,'boundary multiplicity exceeds one')
        if n:out.append((a,b) if n==1 else (b,a))
    return out

def check_sector(boundary,encoded):
    v,p,q=map(point,encoded);out,inc=minus(p,v),minus(q,v)
    need(det(out,inc)>0,'selected sector not strictly convex')
    rays=[]
    for a,b in boundary:
        if a==v:rays.append((minus(b,v),'out'))
        if b==v:rays.append((minus(a,v),'in'))
    def same(a,b):return det(a,b)==0 and a[0]*b[0]+a[1]*b[1]>0
    need(any(k=='out' and same(r,out) for r,k in rays),'missing outgoing boundary ray')
    need(any(k=='in' and same(r,inc) for r,k in rays),'missing incoming boundary ray')
    need(not any(det(out,r)>0 and det(r,inc)>0 for r,k in rays),'sector contains another boundary ray')
    return v,out,inc

def choices(target,placed,sector,sides,D):
    v,out,inc=sector;length=rt(norm(out,D));axis=times(1/length,out);perp=(-D*axis[1],axis[0])
    found=set()
    for i,s in enumerate(sides):
        for j,r in enumerate(sides):
            if i==j:continue
            third=sides[3-i-j]
            projection=Q(s*s+r*r-third*third,2*s)
            coefficient=rt((r*r-projection*projection)/D)
            other=plus(times(projection,axis),times(coefficient,perp))
            if det(other,inc)<0:continue
            tri=canonical((v,plus(v,times(s,axis)),plus(v,other)))
            need(sorted(norm(minus(a,b),D) for a,b in ee(tri))==sorted(k*k for k in sides),'metric construction')
            if not all(within(target,p) for p in tri):continue
            if not all(separate(tri,t) for t in placed):continue
            found.add(tri)
    return found

def verify(data):
    u,v,m,branch=(data['parameters'][k] for k in ('u','v','m','branch'))
    need(0<u<v and m>0 and branch in ('W','beta'),'parameters')
    sides=(u*v,v*v-u*u,v*v);D=data['D'];N=((2 if branch=='W' else 3)*v*v-u*u)*m*m
    need(D>0 and data['N']==N and list(sides)==data['tile'],'announced shape/count')
    target=canonical(tuple(map(point,data['target'])))
    expected=([m*v**3,m*u*(2*v*v-u*u),m*v*(v*v-u*u)] if branch=='W' else [m*v**3,m*v**3,m*u*(3*v*v-u*u)])
    need(sorted(norm(minus(a,b),D) for a,b in ee(target))==sorted(k*k for k in expected),'target metric')
    a,b,c=sides
    heron=(a+b+c)*(-a+b+c)*(a-b+c)*(a+b-c)
    need(4*D*turn(*target)**2==N*N*heron,'target area ratio')
    rows=data['nodes'];seen=set();stats=Counter()
    def walk(ix,placed):
        need(isinstance(ix,int) and 0<=ix<len(rows) and ix not in seen,'invalid or repeated tree node')
        seen.add(ix);need(len(placed)<N,'branch reaches full tile count')
        row=rows[ix]; B=residual(target,placed)
        s=check_sector(B,row['sector']); ps=choices(target,placed,s,sides,D)
        kids=row['children']; advertised=[canonical(tuple(map(point,x['triangle']))) for x in kids]
        need(len(set(advertised))==len(advertised),'duplicate branch')
        need(set(advertised)==ps,'branch list is not exhaustive')
        stats['nodes']+=1
        stats['max_depth']=max(stats['max_depth'],len(placed))
        if not kids:stats['contradiction_leaves']+=1
        for t,k in zip(advertised,kids):walk(k['node'],placed+[t])
    walk(0,[]);need(len(seen)==len(rows),'unreachable proof rows')
    return {'status':'PASS','N':N,'tile':list(sides),'target_sides':expected,'parameters':data['parameters'],**dict(stats),
            'scope':'specified tile and target only','uses_reverse_apex_or_packing':False,'direction_cutoff':None}

if __name__=='__main__':
    reports=[]
    for path in sys.argv[1:]:
        start=monotonic();r=verify(json.loads(Path(path).read_text()));r['file']=Path(path).name;r['replay_seconds']=round(monotonic()-start,4);reports.append(r);print(json.dumps(r),flush=True)
    if len(reports)>1:Path(__file__).with_name('replay_report.json').write_text(json.dumps(reports,indent=2)+'\n')
