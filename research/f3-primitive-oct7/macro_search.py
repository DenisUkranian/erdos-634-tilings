#!/usr/bin/env python3
"""Exploratory exact corner search with integer-scaled triangle macrotiles.

A success is a positive certificate to expand into ordinary square grids.
Exhaustion means only failure within the stated macro-count/scale restrictions.
This program is not used for a nonexistence claim about unit tilings.
"""
from fractions import Fraction as F
from pathlib import Path
from functools import lru_cache
from math import isqrt
import argparse, json, sys, time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'uniform-reduction'))
import exact_search as E

class Search:
    def __init__(self,a,b,c,m=1,max_macros=8,min_scale=1,seconds=60):
        self.a,self.b,self.c,self.m=a,b,c,m
        self.n=3*(a+b)*(a+2*b)*m*m
        Z=(F(a)+F(b,2),F(b,2))
        K=E.scale(E.cmul(E.cmul(Z,Z,3),Z,3),F(m*(a+2*b),c*c))
        self.target=E.triangle(((F(0),F(0)),(F(m*c*c),F(0)),K))
        self.unit=E.triangle(((F(0),F(0)),(F(a),F(0)),Z))
        self.templates={k:tuple(E.scale(v,k) for v in self.unit) for k in range(min_scale,isqrt(self.n)+1)}
        self.max_macros=max_macros; self.min_scale=min_scale; self.seconds=seconds
        self.nodes=0; self.deepest=0; self.dead=set(); self.start=time.monotonic();self.found=None
    def check(self):
        if time.monotonic()-self.start>=self.seconds:raise E.BudgetExceeded()
    @lru_cache(None)
    def sums(self,n,slots,kmax):
        if n==0:return True
        if slots==0 or n<self.min_scale**2 or n>slots*kmax*kmax:return False
        return any(self.sums(n-k*k,slots-1,k) for k in range(min(kmax,isqrt(n)),self.min_scale-1,-1))
    def dfs(self,placed,scales):
        self.check();self.nodes+=1;self.deepest=max(self.deepest,len(placed))
        n=self.n-sum(k*k for k in scales); slots=self.max_macros-len(placed)
        if n==0:self.found=(placed,scales);return True
        if not self.sums(n,slots,isqrt(n)):return False
        key=tuple(sorted(placed))
        if key in self.dead:return False
        B=E.atomic_boundary(self.target,placed,self.check)
        sectors=E.convex_sectors(B,3)
        ks=[k for k in range(isqrt(n),self.min_scale-1,-1) if self.sums(n-k*k,slots-1,isqrt(n-k*k))]
        best=None
        # Acute corners are geometrically the most useful and cheap to examine.
        for sector in sectors[:min(4,len(sectors))]:
            ps=[]
            for k in ks:
                ps.extend((k,t) for t in E.placements(self.templates[k],sector,self.target,placed,3,self.check))
            if best is None or len(ps)<len(best):best=ps
            if not best:break
        for k,t in best:
            if self.dfs(placed+(t,),scales+(k,)):return True
        self.dead.add(key);return False
    def run(self):
        try:r=self.dfs((),())
        except (E.BudgetExceeded,RecursionError):r=None
        return {'tile':[self.a,self.b,self.c],'multiplier':self.m,'count':self.n,
            'max_macros':self.max_macros,'min_scale':self.min_scale,
            'status':('FOUND' if r else 'RESTRICTED_EXHAUSTED' if r is False else 'INCOMPLETE'),
            'nodes':self.nodes,'deepest':self.deepest,'seconds':round(time.monotonic()-self.start,3),
            'coordinate_field':'(x,y) denotes x+y*sqrt(3)*i',
            'target':E.encode_tri(self.target),
            'macros':None if self.found is None else [{'scale':k,'vertices':E.encode_tri(t)} for t,k in zip(*self.found)]}

def main():
    p=argparse.ArgumentParser();p.add_argument('--a',type=int,default=24);p.add_argument('--b',type=int,default=11);p.add_argument('--c',type=int,default=31)
    p.add_argument('--m',type=int,default=1);p.add_argument('--max-macros',type=int,default=8);p.add_argument('--min-scale',type=int,default=4)
    p.add_argument('--seconds',type=float,default=60);p.add_argument('--output')
    a=p.parse_args();r=Search(a.a,a.b,a.c,a.m,a.max_macros,a.min_scale,a.seconds).run()
    s=json.dumps(r,indent=2)+'\n'
    if a.output:Path(a.output).write_text(s)
    print(s)
if __name__=='__main__':main()
