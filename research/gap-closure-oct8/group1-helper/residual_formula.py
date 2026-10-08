#!/usr/bin/env python3
"""Explicit adjacent W remainder, 2<=t<=u-1, using horizontal grids."""
from fractions import Fraction as F
import argparse
import json
from pathlib import Path


def ccw(p):
    area=sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(p,p[1:]+p[:1]))
    return p if area>0 else list(reversed(p))


def triangle(p,n,cut=0):
    origin,left,right=p
    e=tuple(F(left[k]-origin[k],n)for k in range(2))
    f=tuple(F(right[k]-origin[k],n)for k in range(2))
    def at(i,j):return tuple(origin[k]+i*e[k]+j*f[k]for k in range(2))
    out=[]
    for i in range(n):
        for j in range(n-i):
            if i+j>=cut:out.append(ccw([at(i,j),at(i+1,j),at(i,j+1)]))
            if cut-1<=i+j<n-1:out.append(ccw([at(i+1,j),at(i+1,j+1),at(i,j+1)]))
    assert len(out)==n*n-cut*cut
    return out


def rectangle(x0,y0,x1,y1,w,h):
    assert x1>=x0 and y1>=y0 and (x1-x0)%w==0 and (y1-y0)%h==0
    out=[]
    for x in range(x0,x1,w):
        for y in range(y0,y1,h):
            out.extend([[(x,y),(x+w,y),(x,y+h)],[(x+w,y),(x+w,y+h),(x,y+h)]])
    return out


def columns(x,y,p,q,u,v):
    assert p>=0 and q>=0
    out=rectangle(x,y,x+p*u,y+u*v,u,v)
    out.extend(rectangle(x+p*u,y,x+p*u+q*v,y+u*v,v,u))
    return out


def cell(x,y,W,p,q,u,v,cut=0):
    assert W-v*v==p*u+q*v
    # The left origin must be its upper-left apex so that cut removes
    # the small similar corner, rather than its right-angle corner.
    out=triangle([(x-v*v,y+u*v),(x,y),(x,y+u*v)],v,cut)
    out.extend(columns(x,y,p,q,u,v))
    out.extend(triangle([(x+W-v*v,y),(x+W,y),(x+W-v*v,y+u*v)],v))
    return out


def generate(u,t):
    assert u>=3 and 2<=t<=u-1
    v=u+1;b=2*u+1;m=v+t
    out=[]
    for j in range(t):
        x,y=-v*v*j,u*v*j;q=u*b-u*u*j
        out.extend(triangle([(x,y),(x-v*v,y+u*v),(x,y+u*v)],v))
        out.extend(triangle([(q-u*u,y),(q,y),(q-u*u,y+u*v)],u))
        out.extend(columns(x,y,j,u+j,u,v))
    for j in range(t,v):out.extend(cell(-v*v*j,u*v*j,b*(u+t),t-1,u+t-1,u,v))
    upper=triangle([(-u*m,0),(-u*m,v*m),(0,0)],m)
    upper.extend(rectangle(-u*m,-u*v,0,0,u,v))
    upper.extend(triangle([(0,-u*v),(v*v,-u*v),(0,0)],v))
    for j in range(1,t):
        upper.extend(cell((j+1)*v*v-b*m,-(j+1)*u*v,b*m,t,u+t,u,v,cut=t if j==1 else 0))
    V=(-u*u*m,u*v*m)
    out.extend([[(x+V[0],y+V[1])for x,y in tri]for tri in upper])
    assert len(out)==b*(2*u*v+4*v*t+t*t)
    assert all(z.denominator==1 if isinstance(z,F)else True for tri in out for p in tri for z in p)
    out=[[[int(x),int(y)]for x,y in tri]for tri in out]
    boundary=[(0,0),(-u*v*m,u*u*m),(-u*v*m,v*v*m),V,
              (-u*u*m+t*v*v,u*v*v),(-u*u*v+b*(t-1),u*v*v),
              (u*b-u*u*t,u*v*t),(u*b,0)]
    return dict(u=u,t=t,v=v,triangles=out,target=ccw(boundary),
                construction='Explicit horizontal strip and annulus formula')


if __name__=='__main__':
    if not __debug__:raise RuntimeError('Run without -O.')
    p=argparse.ArgumentParser();p.add_argument('--u',type=int,required=True);p.add_argument('--t',type=int,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    data=generate(a.u,a.t);a.output.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'u':a.u,'t':a.t,'tiles':len(data['triangles']),'output':str(a.output)}))
