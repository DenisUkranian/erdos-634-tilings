#!/usr/bin/env python3
"""Solver-free mixed corner whenever b²-a(a-2b)-qc lies in <a,b>."""
from fractions import Fraction as F
from pathlib import Path
from math import gcd
import argparse,json
from reduce_corner import add,sub,scale,grid,enc,orient

def semigroup(r,a,b):
    if r<0:return None
    g=gcd(a,b)
    if r%g:return None
    aa,bb,rr=a//g,b//g,r//g
    A=0 if bb==1 else (rr*pow(aa,-1,bb))%bb
    return (A,(r-A*a)//b)if A*a<=r else None

def witness(a,b,c,q=None):
    if not(type(a)is int and type(b)is int and type(c)is int and c*c==a*a+a*b+b*b and a>2*b>0):raise ValueError('require integer norm triple with a>2b')
    k=a-2*b;D=b*b-a*k
    for n in ([q]if q is not None else range(1,D//c+1)):
        if type(n)is not int or n<=0:continue
        r=D-n*c;w=semigroup(r,a,b)
        if w is not None:return n,r,*w
    raise ValueError('new mixed-corner criterion fails')

def construct(a,b,c,q=None):
    q,r,Aa,Bb=witness(a,b,c,q);k=a-2*b
    C=(F(-2*b*b),F(2*b*b));D=(F(-a*k),F(a*k));A=(F(b*k),F(0));B=(F(2*a*b),F(0));G=(F(a*b),F(0));H=add(D,G)
    e=(F(1),F(-1));F0=(F(a*b-b*b),F(b*b));C1=add(C,scale(q*c,e));F1=add(F0,scale(q*c,e));V=sub(D,scale(r,e))
    regions=[];triangles=[];parts=[]
    def append(name,poly,ts):
        ts=[orient(t)for t in ts];parts.append({'name':name,'polygon':enc(orient(poly)),'count':len(ts),'first_triangle':len(triangles)});regions.extend([name]*len(ts));triangles.extend(ts)
    # q by c cells with side lengths c and b; their remaining diagonal is a.
    u=scale(c,e);v=(F(b*(a+b),c),F(-b*b,c));ts=[]
    for i in range(q):
        for j in range(c):
            o=add(C,add(scale(i,u),scale(j,v)));x=add(o,u);y=add(o,v);ts.extend(([o,x,y],[x,add(x,v),y]))
    append('rotated_parallelogram',[C,C1,F1,F0],ts)
    append('outer_b_grid',[F0,G,B],grid(F0,G,B,b))
    append('inner_b_grid',[C1,V,F1],grid(C1,V,F1,b))
    # ab by r 60-degree parallelogram. Split r=Aa*a+Bb*b into strips.
    ts=[];offset=0
    for width,step,num in ((a,b,Aa),(b,a,Bb)):
        for _ in range(num):
            for j in range(a*b//step):
                o=add(V,add((F(j*step),F(0)),scale(offset,e)));u=(F(step),F(0));v=scale(width,e);x=add(o,u);y=add(o,v);z=add(x,v);ts.extend(([o,x,z],[o,z,y]))
            offset+=width
    if offset!=r:raise RuntimeError('strip width')
    if r:append('semigroup_strip',[V,D,H,F1],ts)
    elif ts:raise RuntimeError('zero strip')
    # a by k reflected grid rectangle minus its k-fold triangular corner.
    u=(F(b),F(0));v=(F(-a),F(a));ts=[]
    for i in range(a):
        for j in range(k):
            o=add(scale(i,u),scale(j,v));x=add(o,u);y=add(o,v)
            if i+j>=k:ts.append([o,x,y])
            if i+j>=k-1:ts.append([x,add(x,v),y])
    append('reflected_grid_corner',[D,A,G,H],ts)
    N=a*(4*b-a)
    if len(triangles)!=N:raise RuntimeError('count')
    return {'format':'ERDOS634_RATIONAL_EISENSTEIN_TILING_V1','tile':[a,b,c],'count':N,'target':enc(orient([A,B,C,D])),'triangles':[enc(t)for t in triangles],'construction':'solver-free mixed gamma corner','parameters':{'k':k,'q':q,'r':r,'semigroup_A':Aa,'semigroup_B':Bb},'parts':parts}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--a',type=int,default=24);ap.add_argument('--b',type=int,default=11);ap.add_argument('--c',type=int,default=31);ap.add_argument('--q',type=int);ap.add_argument('--output',type=Path,default=Path(__file__).with_name('q480_macro.json'));ar=ap.parse_args();d=construct(ar.a,ar.b,ar.c,ar.q);ar.output.write_text(json.dumps(d,separators=(',',':'))+'\n');print(json.dumps({k:d[k]for k in ('tile','count','parameters','parts')}))
if __name__=='__main__':main()
