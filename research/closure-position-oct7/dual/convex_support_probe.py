#!/usr/bin/env python3
"""Exploratory floating convex support propagation; NOT a proof checker.

Keeps all orientations in a requested integer height interval. Domains are
convex relaxations of anchor positions. This can test whether a cheap global
position-sensitive relaxation is promising before a huge lattice expansion.
"""
import argparse, json, math, time
import numpy as np
from scipy.spatial import ConvexHull, QhullError

def hull(points):
    P=np.asarray(points,dtype=float)
    if len(P)<3:return np.empty((0,2))
    try:return P[ConvexHull(P).vertices]
    except QhullError:return np.empty((0,2))

def clip(poly,n,c):
    if len(poly)==0:return poly
    out=[]
    for p,q in zip(poly,np.roll(poly,-1,axis=0)):
        vp=float(n@p-c);vq=float(n@q-c)
        ip=vp<=1e-9;iq=vq<=1e-9
        if ip:out.append(p)
        if ip!=iq:out.append(p+(q-p)*(vp/(vp-vq)))
    return np.asarray(out).reshape((-1,2))

def area(poly):
    if len(poly)<3:return 0.
    return abs(np.cross(poly,np.roll(poly,-1,axis=0)).sum())/2

def run(L,U,steps,seconds):
    start=time.time();z=complex(8+3.5,7*math.sqrt(3)/2)/13
    def d(h,j):
        q=z**h*complex(math.cos(j*math.pi/3),math.sin(j*math.pi/3))
        return np.array([q.real,q.imag])
    P=np.array([[0.,0.],[154.,0.],[77.,28*math.sqrt(3)]])
    cons=[]
    for p,q in zip(P,np.roll(P,-1,axis=0)):
        e=q-p;n=np.array([e[1],-e[0]]);cons.append((n,float(n@p)))
    variants=[];domains=[]
    for h in range(L,U+1):
      for x,y in [(8,7),(7,8)]:
       for j in range(6):
        V=np.array([[0.,0.],x*d(h,j),y*d(h,j+2)])
        edges=[(h,j,x),(h-1,(j+3)%6,13),(h,(j+5)%6,y)] if x==8 else [(h,j,x),(h+1,(j+2)%6,13),(h,(j+5)%6,y)]
        atoms=[]
        for v,(eh,ej,le) in zip(V,edges):
            for k in range(le):atoms.append((eh,ej%6,v+k*d(eh,ej)))
        domain=P.copy()
        for n,c in cons:domain=clip(domain,n,c-max(V@n))
        variants.append(atoms);domains.append(domain)
    boundary={}
    for p,(h,j,le) in zip(P,[(0,0,154),(1,2,91),(-1,4,91)]):
        boundary[(h,j)]=[p,p+(le-1)*d(h,j)]
    history=[]
    for it in range(steps):
        sets={}
        for atoms,D in zip(variants,domains):
            if len(D)<3:continue
            for h,j,off in atoms:sets.setdefault((h,j),[]).extend(D+off)
        support={}
        # A tile edge has a neighbouring edge with reverse orientation,
        # whose starting point is one unit further along this tile edge.
        for key,points in sets.items():
            h,j=key;forward=(h,(j+3)%6)
            target=list(points)
            # Express all supports as the starting point of forward atom.
            target=np.asarray(target)+d(h,j)
            if forward in boundary:target=np.concatenate([target,boundary[forward]])
            support[forward]=hull(target)
        for key,points in boundary.items():
            if key not in support:support[key]=hull(points)
        equations={}
        for key,S in support.items():
            eq=[]
            for p,q in zip(S,np.roll(S,-1,axis=0)):
                e=q-p;n=np.array([e[1],-e[0]]);eq.append((n,float(n@p)))
            equations[key]=eq
        new=[];change=0.
        for atoms,D in zip(variants,domains):
            old=area(D)
            for h,j,off in atoms:
                if (h,j) not in equations or not equations[h,j]:D=np.empty((0,2));break
                for n,c in equations[h,j]:D=clip(D,n,c-float(n@off))
                if len(D)<3:break
            new.append(D);change=max(change,old-area(D))
        domains=new
        row={'iteration':it+1,'live_variants':sum(len(D)>=3 for D in domains),'sum_domain_area':sum(area(D) for D in domains),'max_area_loss':change,'seconds':time.time()-start}
        history.append(row);print(json.dumps(row),flush=True)
        if row['live_variants']==0 or change<1e-8 or time.time()-start>seconds:break
    return {'scope':'EXPLORATORY_FLOATING_CONVEX_RELAXATION','band':[L,U],'history':history,'not_a_tiling_or_nonexistence_certificate':True}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--lo',type=int,default=-22);p.add_argument('--hi',type=int,default=22);p.add_argument('--iterations',type=int,default=20);p.add_argument('--seconds',type=float,default=90);p.add_argument('--output');a=p.parse_args()
    result=run(a.lo,a.hi,a.iterations,a.seconds)
    if a.output:open(a.output,'w').write(json.dumps(result,indent=2)+'\n')
