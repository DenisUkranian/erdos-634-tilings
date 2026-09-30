#!/usr/bin/env python3
"""Bounded complete convex-corner search over Q(sqrt(D)).

No boundary-collar theorem, packing lemma, assumed grid, or primality lemma.
A node/time limit returns INCOMPLETE, never an exclusion. This is a research
implementation, not a proof-assistant formalization. See PROOF.md.
"""
from __future__ import annotations
from fractions import Fraction as F
from functools import cmp_to_key
from collections import defaultdict, Counter
from dataclasses import asdict
from math import isqrt
import argparse, json, time
from pathlib import Path
from candidates import Instance, heron16, enumerate_candidates, classical

Point=tuple[F,F]
Tri=tuple[Point,Point,Point]

def add(a,b): return (a[0]+b[0],a[1]+b[1])
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def scale(a,t): return (a[0]*t,a[1]*t)
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def orient(a,b,c): return cross(sub(b,a),sub(c,a))
def edges(t): return tuple(zip(t,t[1:]+t[:1]))
def conj(a): return (a[0],-a[1])
def cmul(a,b,D): return (a[0]*b[0]-D*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def dot(a,b,D): return a[0]*b[0]+D*a[1]*b[1]

def rational_sqrt(x):
    p,q=isqrt(x.numerator),isqrt(x.denominator)
    if p*p!=x.numerator or q*q!=x.denominator:
        raise ArithmeticError('Unexpected irrational edge length; no rejection is inferred')
    return F(p,q)

def triangle(t):
    if orient(*t)==0: raise ValueError('Degenerate triangle')
    if orient(*t)<0: t=(t[0],t[2],t[1])
    k=min(range(3),key=lambda i:t[i])
    return t[k:]+t[:k]

def inside(T,p): return all(orient(a,b,p)>=0 for a,b in edges(T))

def overlap(T,U):
    """Strict interior overlap by an exact separating-axis test."""
    for V,W in ((T,U),(U,T)):
        for a,b in edges(V):
            if all(orient(a,b,p)<=0 for p in W):
                return False
    return True

def on_segment(a,b,p):
    return orient(a,b,p)==0 and min(a[0],b[0])<=p[0]<=max(a[0],b[0]) and min(a[1],b[1])<=p[1]<=max(a[1],b[1])

def atomic_boundary(T,placed,check=None):
    """Actual residual boundary, oriented with unfilled region to its left."""
    all_edges=list(edges(T))
    for p in placed:
        all_edges += [(b,a) for a,b in edges(p)]
    vertices=set(p for a,b in all_edges for p in (a,b))
    net=Counter()
    for a,b in all_edges:
        if check is not None:check()
        pts=sorted((p for p in vertices if on_segment(a,b,p)),reverse=a>b)
        for x,y in zip(pts,pts[1:]):
            if x==y: continue
            if x<y: net[(x,y)]+=1
            else: net[(y,x)]-=1
    result=[]
    for (a,b),n in net.items():
        if abs(n)>1:
            raise ArithmeticError('Invalid boundary multiplicity; not a tiling rejection')
        if n==1: result.append((a,b))
        elif n==-1: result.append((b,a))
    return result

def polar_cmp(x,y):
    a,b=x[0],y[0]
    def half(p): return 0 if p[1]>0 or (p[1]==0 and p[0]>=0) else 1
    h,k=half(a),half(b)
    if h!=k:return -1 if h<k else 1
    c=cross(a,b)
    return -1 if c>0 else 1 if c<0 else 0

def convex_sectors(B,D):
    incident=defaultdict(list)
    for a,b in B:
        incident[a].append((sub(b,a),'out'))
        incident[b].append((sub(a,b),'in'))
    result=[]
    for v,rays in incident.items():
        rays.sort(key=cmp_to_key(polar_cmp))
        for i,(out,kind) in enumerate(rays):
            if kind!='out':continue
            inc,next_kind=rays[(i+1)%len(rays)]
            if next_kind!='in':
                raise ArithmeticError('Nonalternating residual rays; no exclusion inferred')
            if cross(out,inc)>0:
                cosine=dot(out,inc,D)/(rational_sqrt(dot(out,out,D))*rational_sqrt(dot(inc,inc,D)))
                result.append((cosine,v,out,inc))
    return sorted(result,reverse=True)

def placements(template,sector,T,placed,D,check=None):
    _,v,out,inc=sector
    length=rational_sqrt(dot(out,out,D))
    found=set()
    for i in range(3):
        for j in range(3):
            if i==j:continue
            k=3-i-j
            ref=sub(template[j],template[i]); other=sub(template[k],template[i])
            side=rational_sqrt(dot(ref,ref,D))
            for flip in (False,True):
                if check is not None:check()
                t=conj(ref) if flip else ref
                z=conj(other) if flip else other
                rot=scale(cmul(out,conj(t),D),1/(length*side))
                w=add(v,scale(out,side/length)); q=add(v,cmul(rot,z,D))
                if cross(out,sub(q,v))<=0:continue
                if cross(sub(w,v),inc)<0 or cross(sub(q,v),inc)<0:continue
                cand=triangle((v,w,q))
                if not all(inside(T,p) for p in cand):continue
                if any(overlap(cand,p) for p in placed):continue
                found.add(cand)
    if len(found)>6:raise ArithmeticError('More than six candidate placements')
    return sorted(found)

def encode_tri(t): return [[str(x),str(y)] for x,y in t]

class BudgetExceeded(Exception):
    """Resource stop, never a contradiction."""

class Search:
    def __init__(self,instance:Instance,max_nodes:int|None=None,seconds:float|None=None):
        instance.validate()
        self.I=instance;self.D=heron16(instance.tile)
        a,b,c=map(F,instance.tile)
        self.template=triangle(((F(0),F(0)),(c,F(0)),((b*b+c*c-a*a)/(2*c),1/(2*c))))
        A,B,C=map(F,sorted(instance.target))
        self.target=triangle(((F(0),F(0)),(C,F(0)),((B*B+C*C-A*A)/(2*C),F(instance.n)/(2*C))))
        self.nodes=0;self.max_nodes=max_nodes;self.dead=set();self.start=time.monotonic();self.seconds=seconds
        self.deepest=0;self.found=None

    def check_deadline(self):
        if self.seconds is not None and time.monotonic()-self.start>=self.seconds:
            raise BudgetExceeded("Time limit")

    def dfs(self,placed:tuple[Tri,...]):
        if self.max_nodes is not None and self.nodes>=self.max_nodes:return None
        if self.seconds is not None and time.monotonic()-self.start>=self.seconds:return None
        self.nodes+=1;self.deepest=max(self.deepest,len(placed))
        if len(placed)==self.I.n:
            self.found=placed;return True
        key=tuple(sorted(placed))
        if key in self.dead:return False
        B=atomic_boundary(self.target,placed,self.check_deadline)
        sectors=convex_sectors(B,self.D)
        if not sectors:raise ArithmeticError('Positive residual area without a convex sector')
        # Any sector is complete. Minimum fan size is only a deterministic order choice.
        best=None
        for sector in sectors:
            ps=placements(self.template,sector,self.target,placed,self.D,self.check_deadline)
            if best is None or len(ps)<len(best):best=ps
            if len(ps)<=1:break
        if best is None:raise ArithmeticError('No selected corner')
        complete=True
        for t in best:
            r=self.dfs(placed+(t,))
            if r is True:return True
            if r is None:complete=False;break
        if complete:
            self.dead.add(key);return False
        return None

    def run(self):
        resource_stop=None
        try:
            r=self.dfs(())
        except (BudgetExceeded, RecursionError) as exc:
            r=None;resource_stop=type(exc).__name__
        return {'instance':asdict(self.I),'status':('TILING_FOUND' if r is True else 'EXHAUSTED' if r is False else 'INCOMPLETE'),
                'nodes':self.nodes,'maximum_placed':self.deepest,'seconds':round(time.monotonic()-self.start,6),
                'field_D':self.D,'target_coordinates':encode_tri(self.target),
                'tile_coordinates':[encode_tri(t) for t in self.found] if self.found is not None else None,
                'resource_stop':resource_stop,'exact_arithmetic':True,'uses_collar_lemma':False,'uses_prime_candidate':False}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('n',type=int);ap.add_argument('--max-nodes',type=int,default=100000)
    ap.add_argument('--seconds',type=float,default=30);ap.add_argument('--branch')
    ap.add_argument('--output')
    args=ap.parse_args()
    instances=enumerate_candidates(args.n)
    if args.branch:instances=[r for r in instances if r.branch==args.branch]
    reports=[Search(r,args.max_nodes,args.seconds).run() for r in instances]
    result={'n':args.n,'classical_witness':classical(args.n),'runs':reports,
            'scope':'Selected finite instances, not a full solution of Erdos 634'}
    text=json.dumps(result,indent=2)+'\n'
    if args.output:Path(args.output).write_text(text)
    print(text,end='')
if __name__=='__main__':main()
