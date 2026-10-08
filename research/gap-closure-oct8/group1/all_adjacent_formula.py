#!/usr/bin/env python3
"""Solver-free two-parameter W seeds: v=u+1, m=v+t, 2<=t<=u-1."""
from fractions import Fraction as F
from math import lcm
from pathlib import Path
import argparse
import json


def det(a,b):return a[0]*b[1]-a[1]*b[0]
def area2(p):return sum(det(a,b) for a,b in zip(p,p[1:]+p[:1]))
def ccw(p):return list(p) if area2(p)>0 else list(reversed(p))


def tri_grid(vertices,n,inner=0):
    origin,left,right=vertices
    e=tuple(F(left[k]-origin[k],n) for k in range(2))
    f=tuple(F(right[k]-origin[k],n) for k in range(2))
    def p(i,j):return tuple(origin[k]+i*e[k]+j*f[k] for k in range(2))
    out=[]
    for i in range(n):
        for j in range(n-i):
            if i+j>=inner:out.append(ccw([p(i,j),p(i+1,j),p(i,j+1)]))
            if inner-1<=i+j<n-1:out.append(ccw([p(i+1,j),p(i+1,j+1),p(i,j+1)]))
    assert len(out)==n*n-inner*inner
    return out


def rectangle(x0,y0,x1,y1,w,h):
    assert x1>=x0 and y1>=y0 and (x1-x0)%w==0 and (y1-y0)%h==0
    out=[]
    for x in range(x0,x1,w):
        for y in range(y0,y1,h):
            out.extend([[(x,y),(x+w,y),(x,y+h)],[(x+w,y),(x+w,y+h),(x,y+h)]])
    return out


def mixed_rectangle(x,y,u,Acols,Bcols):
    v=u+1
    assert Acols>=0 and Bcols>=0
    out=rectangle(x,y,x+Acols*u,y+u*v,u,v)
    x+=Acols*u
    out.extend(rectangle(x,y,x+Bcols*v,y+u*v,v,u))
    return out


def rising_cell(x,y,u,k):
    # Bottom interval [x,x+W], top shifted left by v^2; height uv.
    v=u+1;b=2*u+1;W=b*(u+k)
    out=tri_grid([(x,y),(x,y+u*v),(x-v*v,y+u*v)],v)
    out.extend(mixed_rectangle(x,y,u,k-1,u+k-1))
    out.extend(tri_grid([(x+W-v*v,y),(x+W,y),(x+W-v*v,y+u*v)],v))
    assert len(out)==2*W
    return out


def falling_cell(x,y,u,k,inner=0):
    # Top interval [x,x+W], bottom shifted right by v^2; height uv.
    v=u+1;b=2*u+1;W=b*(u+k)
    out=tri_grid([(x,y),(x+v*v,y),(x+v*v,y-u*v)],v,inner)
    out.extend(mixed_rectangle(x+v*v,y-u*v,u,k-1,u+k-1))
    out.extend(tri_grid([(x+W,y),(x+W,y-u*v),(x+W+v*v,y-u*v)],v))
    assert len(out)==2*W-inner*inner
    return out


def residual(u,t):
    assert 2<=t<=u-1
    v=u+1;b=2*u+1;m=v+t
    out=[]
    # Lower cap: t expanding horizontal bands.
    for j in range(t):
        xl=-v*v*j;xr=u*b-u*u*j;y=u*v*j
        out.extend(tri_grid([(xl,y),(xl,y+u*v),(xl-v*v,y+u*v)],v))
        out.extend(mixed_rectangle(xl,y,u,j,u+j))
        out.extend(tri_grid([(xr-u*u,y),(xr,y),(xr-u*u,y+u*v)],u))
    # Central strip: v-t equal-height parallel cells.
    for j in range(t,v):
        out.extend(rising_cell(-v*v*j,u*v*j,u,t))
    # Upper cap, relative to V=(-u^2m,uvm).
    cap=tri_grid([(-u*m,v*m),(-u*m,0),(0,0)],m)
    cap.extend(rectangle(-u*m,-u*v,0,0,u,v))
    cap.extend(tri_grid([(0,0),(0,-u*v),(v*v,-u*v)],v))
    cap.extend(falling_cell(v*v-b*m,-u*v,u,t+1,inner=t))
    for j in range(2,t):
        cap.extend(falling_cell(j*v*v-b*m,-j*u*v,u,t+1))
    assert len(cap)==2*b*m*t
    shift=(-u*u*m,u*v*m)
    out.extend([[(x+shift[0],y+shift[1]) for x,y in p] for p in cap])
    assert len(out)==b*(2*u*v+4*v*t+t*t)
    return out


def outer(u,t):
    v=u+1;b=2*u+1;m=v+t
    O=(F(u*m*v**3,b),F(-u*u*m*v*v,b));X=(F(0),F(0))
    A=(F(-u*v*m),F(u*u*m));C=(F(-u*v*m),F(v*v*m))
    V=(F(-u*u*m),F(u*v*m));U=(F(-u*u*m+t*v*v),F(u*v*v))
    R=(F(-u*u*v+b*(t-1)),F(u*v*v));S=(F(u*b-u*u*t),F(u*v*t));Q=(F(u*b),F(0))
    P=(Q[0]+F(u*t*v**3,b),Q[1]-F(u*u*t*v*v,b))
    R0=(S[0]+F(t*u*v*v,b),S[1]-F(t*u*u*v,b))
    T=(U[0]+F((u-t)*v**3,b),U[1]-F((u-t)*u*v*v,b))
    return [O,A,C],[([O,X,Q,P],u*m,u*t),([P,Q,S,R0],v*t,t),
                    ([R0,R,U,T],b-t,u-t),([T,V,C],m,0)]


def annulus(poly,n,s):
    if s==0:return tri_grid(poly,n)
    left,right,tr,tl=poly
    apex=tuple((n*tl[k]-s*left[k])/(n-s) for k in range(2))
    return tri_grid([apex,left,right],n,s)


def generate(u,t,path):
    target,macros=outer(u,t);v=u+1;m=v+t;b=2*u+1
    ts=residual(u,t)
    for poly,n,s in macros:ts.extend(annulus(poly,n,s))
    assert len(ts)==(2*v*v-u*u)*m*m
    E=(F(u*u-2*v*v,2*v*v),F(u,2*v*v));FF=(F(-u,2*v),F(1,2*v));O=target[0]
    def physical(p):
        x,y=p[0]-O[0],p[1]-O[1]
        return (v*(x*E[0]+y*FF[0]),v*(x*E[1]+y*FF[1]))
    ts=[ccw([physical(p) for p in tri]) for tri in ts]
    goal=ccw([physical(p) for p in target]);den=lcm(*(x.denominator for tri in ts+[goal] for p in tri for x in p))
    D=4*v*v-u*u
    data={'metric':f'x^2+{D}y^2','metric_y_coefficient':D,'denominator':den,
          'tile':[u*v,b,v*v],'u':u,'v':v,'t':t,'scale':m,
          'target':[[int(x*den),int(y*den)] for x,y in goal],
          'triangles':[[[int(x*den),int(y*den)] for x,y in tri] for tri in ts],
          'construction':'Uniform two-parameter horizontal-band formula, no solver'}
    path.write_text(json.dumps(data,indent=2)+'\n')
    return len(ts)


if __name__=='__main__':
    if not __debug__:raise RuntimeError('Run without -O.')
    ap=argparse.ArgumentParser();ap.add_argument('--u',type=int,required=True);ap.add_argument('--t',type=int,required=True)
    ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    print(json.dumps({'u':args.u,'t':args.t,'tiles':generate(args.u,args.t,args.output)}))
