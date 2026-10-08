#!/usr/bin/env python3
"""Exact conditional reduction of primitive F3 to a smaller convex corner."""
from fractions import Fraction as F
from pathlib import Path
import argparse, importlib.util, json

ROOT=Path(__file__).resolve().parents[3]
spec=importlib.util.spec_from_file_location('stair',ROOT/'research/group2-mixed-gamma/construct_staircase.py')
s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
add,sub,scale,mul,grid=s.add,s.sub,s.scale,s.mul,s.grid

def enc(poly):return [[str(x),str(y)]for x,y in poly]
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def orient(poly):return list(poly)if sum(cross(poly[i],poly[(i+1)%len(poly)])for i in range(len(poly)))>0 else list(reversed(poly))

def reduction(a,b,c):
    if not all(type(x)is int for x in (a,b,c)) or not(0<2*b<a and a*a+a*b+b*b==c*c and 2*a*b+2*b*b>a*a):
        raise ValueError('Require integer norm triple and 2b<a<(1+sqrt(3))b')
    S,h,t=c*c,a+2*b,a-b
    Z=(F(a),F(b));Z2=mul(Z,Z)
    X=(F(0),F(0));Y=(F(S),F(0));I=scale(a,Z);J=Z2
    T=scale(F(a*h,S),Z2);K=scale(F(h,S),mul(Z2,Z));J2=scale(a,mul((F(1),F(1)),Z))
    tiles=[]
    for p,q,r in ((X,Y,I),(Y,I,J2),(X,I,J)):
        tiles.extend(grid(p,q,r,c))
    macro_count=len(tiles)
    u=scale(F(1,h),sub(X,T));v=scale(F(1,h),sub(K,T))
    # Retain the original h-grid outside first common cell and top 2b-grid.
    ordinary=[]
    for i in range(h):
        for j in range(h-i):
            if j>=a or (i<b and j<a):continue
            o=add(T,add(scale(i,u),scale(j,v)));xx=add(o,u);yy=add(o,v)
            ordinary.append([o,xx,yy])
            if i+j<h-1:ordinary.append([xx,add(xx,v),yy])
    tiles.extend(ordinary)
    # Switch only the first common cell, deleting its reflected-hole portion.
    uu=scale(F(b,a),u);vv=scale(F(a,b),v);switched=[]
    for p in range(a):
        for q in range(b):
            o=add(T,add(scale(p,uu),scale(q,vv)));xx=add(o,uu);yy=add(o,vv)
            if p+q>=t:switched.append([o,xx,yy])
            if p+q>=t-1:switched.append([xx,add(xx,vv),yy])
    tiles.extend(switched)
    k=a-2*b
    canonical=[(F(b*k),F(0)),(F(2*a*b),F(0)),(F(-2*b*b),F(2*b*b)),(F(-a*k),F(a*k))]
    origin=add(T,scale(a,v))
    def embed(p):
        x,y=p
        return add(origin,add(scale((x+y)/a,u),scale(y/b,v)))
    omitted=orient([embed(p)for p in canonical]);N=3*(a+b)*h;R=a*(4*b-a)
    if len(tiles)!=N-R or R!=4*b*b-k*k:raise RuntimeError('count')
    return {'format':'ERDOS634_F3_CONDITIONAL_CORNER_REDUCTION_V1','tile':[a,b,c],'count':N,'partial_count':len(tiles),'omitted_count':R,'target':enc(orient([X,Y,K])),'omitted_polygon':enc(omitted),'canonical_corner':enc(canonical),'embedding':{'origin':enc([origin])[0],'u':enc([u])[0],'v':enc([v])[0],'formula':'origin + ((x+y)/a)*u + (y/b)*v'},'partial_triangles':[enc(orient(tri))for tri in tiles],'counts':{'three_c_grids':macro_count,'ordinary_complement':len(ordinary),'switched_first_cell':len(switched)},'status':'CONDITIONAL_REDUCTION_NOT_A_TILING'}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--a',type=int,default=24);ap.add_argument('--b',type=int,default=11);ap.add_argument('--c',type=int,default=31);ap.add_argument('--output',type=Path,default=Path(__file__).with_name('f3_4830_corner480_reduction.json'));ar=ap.parse_args()
    data=reduction(ar.a,ar.b,ar.c);ar.output.write_text(json.dumps(data,separators=(',',':'))+'\n');print(json.dumps({k:data[k]for k in ('tile','count','partial_count','omitted_count','counts','status')}))
if __name__=='__main__':main()
