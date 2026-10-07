#!/usr/bin/env python3
"""Positive F3 grids using a reflected 120-degree corner interchange.

Domain a>b>0, a<=2b, c²=a²+ab+b²; all positive integer multipliers.
Coordinates x+y*rho with rho=exp(i*pi/3).
"""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path


def add(p,q):return(p[0]+q[0],p[1]+q[1])
def sub(p,q):return(p[0]-q[0],p[1]-q[1])
def scale(k,p):return(k*p[0],k*p[1])
def mul(p,q):return(p[0]*q[0]-p[1]*q[1],p[0]*q[1]+p[1]*q[0]+p[1]*q[1])
def encode(poly):return[[str(x),str(y)]for x,y in poly]


def grid(p,q,r,n):
    u,v=scale(F(1,n),sub(q,p)),scale(F(1,n),sub(r,p))
    for i in range(n):
        for j in range(n-i):
            o=add(p,add(scale(i,u),scale(j,v)));x=add(o,u);y=add(o,v)
            yield[o,x,y]
            if i+j<n-1:yield[x,add(x,v),y]


def gamma_remainder(T,X,K,a,b,m):
    h=m*(a+2*b);n=m*(a-b)
    u,v=scale(F(1,h),sub(X,T)),scale(F(1,h),sub(K,T))
    # Delete the common ab-by-ab rectangle from the ordinary h-grid.
    for i in range(h):
        for j in range(h-i):
            if i<m*b and j<m*a:continue
            o=add(T,add(scale(i,u),scale(j,v)));x=add(o,u);y=add(o,v)
            yield[o,x,y]
            if i+j<h-1:yield[x,add(x,v),y]
    # Transpose its a-by-b unit parallelogram grid and omit the n-corner.
    u2,v2=scale(F(b,a),u),scale(F(a,b),v)
    for i in range(m*a):
        for j in range(m*b):
            o=add(T,add(scale(i,u2),scale(j,v2)));x=add(o,u2);y=add(o,v2)
            if i+j>=n:yield[o,x,y]
            if i+j>=n-1:yield[x,add(x,v2),y]


def construct(a,b,c,m=1):
    if any(type(t)is not int for t in(a,b,c,m)):
        raise ValueError('integer parameters required')
    if not(a>b>0 and a<=2*b and c*c==a*a+a*b+b*b and m>0):
        raise ValueError('require b<a<=2b, plus norm, and m>0')
    S=c*c;h=a+2*b;delta=a-b
    Z=(F(a),F(b));Z2=mul(Z,Z)
    X=(F(0),F(0));Y=(F(m*S),F(0));I=scale(m*a,Z);J=scale(m,Z2)
    T=scale(F(m*a*h,S),Z2);K=scale(F(m*h,S),mul(Z2,Z))
    J2=scale(m*a,mul((F(1),F(1)),Z))
    triangles=[]
    for p,q,r in((X,Y,I),(Y,I,J2),(X,I,J)):
        triangles.extend(grid(p,q,r,m*c))
    remainder=list(gamma_remainder(T,X,K,a,b,m))
    if len(remainder)!=m*m*(h*h-delta*delta):
        raise RuntimeError('gamma-corner count mismatch')
    triangles.extend(remainder)
    expected=3*(a+b)*h*m*m
    if len(triangles)!=expected:raise RuntimeError('F3 count mismatch')
    return{'format':'ERDOS634_F3_UNIT_TRIANGLES_V1',
           'coordinate_metric':'x^2+x*y+y^2','tile':[a,b,c],
           'multiplier':m,'count':expected,'target':encode([X,Y,K]),
           'triangles':[encode(t)for t in triangles],
           'construction':'three cR grids and reflected gamma-corner rectangle interchange',
           'macro_vertices':{name:encode([p])[0]for name,p in
                             [('X',X),('Y',Y),('I',I),('J',J),('J2',J2),('T',T),('K',K)]},
           'gamma_corner':{'outer_scale':m*h,'removed_scale':m*delta,
                           'standard_rectangle_columns':m*b,
                           'standard_rectangle_rows':m*a,
                           'swapped_rectangle_columns':m*a,
                           'swapped_rectangle_rows':m*b,
                           'count':len(remainder)}}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for key in('a','b','c'):parser.add_argument(key,type=int)
    parser.add_argument('--multiplier',type=int,default=1)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    result=construct(args.a,args.b,args.c,args.multiplier)
    args.output.write_text(json.dumps(result,separators=(',',':'))+'\n')
    print(json.dumps({'count':result['count'],'gamma_corner':result['gamma_corner']}))


if __name__=='__main__':main()
