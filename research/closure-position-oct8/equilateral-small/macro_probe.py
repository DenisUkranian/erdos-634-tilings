#!/usr/bin/env python3
"""Positive-only convex macrotile search for Zhang's (3,5,7) targets.

A restricted exhaustion is never a unit-tiling nonexistence result.
Coordinates (x,y) mean x+i*sqrt(3)*y; all predicates are rational.
"""
from fractions import Fraction as F
from pathlib import Path
from functools import lru_cache
from math import isqrt
import argparse,json,sys,time
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'uniform-reduction'))
import exact_search as E

def P(u,v):return (F(u)+F(v)/2,F(v)/2)
def canon(poly):
    p=tuple(poly)
    if sum(E.cross(a,b) for a,b in E.edges(p))<0:p=p[::-1]
    k=min(range(len(p)),key=lambda k:p[k]);return p[k:]+p[:k]
def trap(x,L):return canon(map(lambda p:P(*p),[(0,0),(x+L,0),(x,L),(0,L)]))
@lru_cache(None)
def triangulate(poly):
    """Exact ear clipping, used also for the nonconvex 35-tile seed island."""
    if len(poly)==3:return (poly,)
    for i in range(len(poly)):
        a,b,c=poly[i-1],poly[i],poly[(i+1)%len(poly)]
        if E.orient(a,b,c)<=0:continue
        tri=canon((a,b,c))
        if any(E.inside(tri,p) for j,p in enumerate(poly) if j not in ((i-1)%len(poly),i,(i+1)%len(poly))):continue
        return (tri,)+triangulate(canon(poly[:i]+poly[i+1:]))
    raise ArithmeticError('Could not triangulate a purported simple polygon')
def overlap(a,b):
    if len(a)<=4 and len(b)<=4:return E.overlap(a,b)
    return any(E.overlap(t,u) for t in triangulate(a) for u in triangulate(b))
def placements(poly,sector,target,placed,check):
    _,v,out,inc=sector; length=E.rational_sqrt(E.dot(out,out,3));found=set()
    for i in range(len(poly)):
        for j in ((i+1)%len(poly),(i-1)%len(poly)):
            ref=E.sub(poly[j],poly[i]);side=E.rational_sqrt(E.dot(ref,ref,3))
            for flip in (False,True):
                check();r=E.conj(ref) if flip else ref
                rot=E.scale(E.cmul(out,E.conj(r),3),1/(length*side))
                q=[]
                for p in poly:
                    d=E.sub(p,poly[i]);d=E.conj(d) if flip else d
                    q.append(E.add(v,E.cmul(rot,d,3)))
                if any(E.cross(out,E.sub(p,v))<0 or E.cross(E.sub(p,v),inc)<0 for p in q):continue
                q=canon(q)
                if not all(E.inside(target,p) for p in q):continue
                if any(overlap(q,p) for p in placed):continue
                found.add(q)
    return sorted(found)

class Search:
    def __init__(self,x,L,slots,seconds,parallelograms,min_macro_area=0,include_pentagon=True):
        self.target=trap(x,L);self.n=(2*x+L)*L//15
        assert (2*x+L)*L%15==0
        self.slots=slots;self.seconds=seconds;self.start=time.monotonic();self.nodes=0;self.deepest=0;self.dead=set();self.found=None
        self.templates=[]
        unit=(P(0,0),P(3,0),P(3,5))
        for k in range(1,isqrt(self.n)+1):self.templates.append((k*k,{'kind':'grid','scale':k},canon(E.scale(p,k) for p in unit)))
        for leg in range(15,L+1,15):
            for base in range(29,x+L+1):
                cost=(2*base+leg)*leg//15
                if cost<=self.n and (base in (29,31,32) or base>=34):self.templates.append((cost,{'kind':'ideal_trapezoid','short_base':base,'leg':leg},trap(base,leg)))
        self.templates.append((88,{'kind':'F4_88'},canon((P(0,0),P(56,0),P(F(275,7),F(165,7))))))
        # Union of CDQ, EAR, QBRD in group2-trapezoids/PROOF.md.
        if include_pentagon:self.templates.append((35,{'kind':'pentagon35'},canon(map(lambda p:P(*p),[(5,3),(40,3),(35,0),(49,0),(25,15)]))))
        if parallelograms:
            # Each basis consists of two sides meeting at a tile vertex.
            for U,V in ((P(3,0),P(3,5)),(P(-3,0),P(0,5)),(P(-3,-5),P(0,-5))):
                # Only use a pair if its difference or sum completes the tile.
                lengths=sorted(E.dot(w,w,3) for w in (U,V,E.sub(V,U)))
                if lengths != [F(9),F(25),F(49)]:continue
                for m in range(1,16):
                    for n in range(1,16):
                        cost=2*m*n
                        if cost>self.n:continue
                        u=E.scale(U,m);v=E.scale(V,n)
                        poly=canon(((F(0),F(0)),u,E.add(u,v),v))
                        self.templates.append((cost,{'kind':'parallelogram','u':list(map(str,U)),'v':list(map(str,V)),'m':m,'n':n},poly))
        self.min_macro_area=min_macro_area;self.include_pentagon=include_pentagon;self.parallelograms=parallelograms
        self.templates=[t for t in self.templates if t[0]>=min_macro_area]
        self.templates.sort(key=lambda t:-t[0]);self.costs=tuple(sorted(set(t[0] for t in self.templates),reverse=True))
    def check(self):
        if time.monotonic()-self.start>self.seconds:raise E.BudgetExceeded()
    @lru_cache(None)
    def possible(self,n,slots):
        if n==0:return True
        if slots==0 or n<0:return False
        return any(c<=n and self.possible(n-c,slots-1) for c in self.costs)
    def dfs(self,placed=(),kinds=(),used=0):
        self.check();self.nodes+=1;self.deepest=max(self.deepest,len(placed))
        n=self.n-used;slots=self.slots-len(placed)
        if n==0:self.found=(placed,kinds);return True
        if not self.possible(n,slots):return False
        key=tuple(sorted(placed))
        if key in self.dead:return False
        B=E.atomic_boundary(self.target,placed,self.check);sectors=E.convex_sectors(B,3)
        options=[t for t in self.templates if t[0]<=n and self.possible(n-t[0],slots-1)]
        best=None
        for sec in sectors[:3]:
            ps=[]
            for c,k,p in options:
                ps.extend((c,k,q) for q in placements(p,sec,self.target,placed,self.check))
            if best is None or len(ps)<len(best):best=ps
            if not best:break
        for c,k,q in best or ():
            if self.dfs(placed+(q,),kinds+(k,),used+c):return True
        self.dead.add(key);return False
    def run(self):
        try:r=self.dfs()
        except (E.BudgetExceeded,RecursionError):r=None
        return {'status':'FOUND' if r else 'RESTRICTED_EXHAUSTED' if r is False else 'INCOMPLETE','nodes':self.nodes,'deepest':self.deepest,'seconds':time.monotonic()-self.start,'count':self.n,'max_macros':self.slots,'templates':len(self.templates),'min_macro_area':self.min_macro_area,'include_pentagon35':self.include_pentagon,'include_parallelograms':self.parallelograms,'scope':'Positive construction probe only; no unrestricted negative conclusion','coordinate_field':'x+i*sqrt(3)*y','target':E.encode_tri(self.target),'macros':None if self.found is None else [{'type':k,'vertices':E.encode_tri(p)} for p,k in zip(*self.found)]}
def main():
    p=argparse.ArgumentParser();p.add_argument('--short-base',type=int,default=30);p.add_argument('--leg',type=int,default=45);p.add_argument('--max-macros',type=int,default=6);p.add_argument('--seconds',type=float,default=60);p.add_argument('--parallelograms',action='store_true');p.add_argument('--min-macro-area',type=int,default=0);p.add_argument('--exclude-pentagon',action='store_true');p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    s=Search(a.short_base,a.leg,a.max_macros,a.seconds,a.parallelograms,a.min_macro_area,not a.exclude_pentagon);r=s.run();a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
if __name__=='__main__':main()
