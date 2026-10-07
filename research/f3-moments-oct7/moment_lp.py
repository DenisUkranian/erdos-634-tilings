#!/usr/bin/env python3
"""Research only: finite direction, fractional-placement first-moment relaxation."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json


def add(u,v): return (u[0]+v[0],u[1]+v[1])
def sub(u,v): return (u[0]-v[0],u[1]-v[1])
def scale(t,u): return (t*u[0],t*u[1])
def mul(u,v): return (u[0]*v[0]-u[1]*v[1],u[0]*v[1]+u[1]*v[0]+u[1]*v[1])
def conj(u):return (u[0]+u[1],-u[1])
def pw(u,n):
    if n<0:return pw(conj(u),-n)
    out=(F(1),F(0))
    for _ in range(n):out=mul(out,u)
    return out

def cross(u,v):return u[0]*v[1]-u[1]*v[0]
def direction(h,j):return (h,j%3),1 if j%6<3 else -1

def build(a,b,c,low,high):
    z=(F(a,c),F(b,c));rho=(F(0),F(1));U=a+2*b;N=3*(a+b)*U
    target=[(F(0),F(0)),(F(c*c),F(0)),scale(c*U,pw(z,3))]
    types=[]
    for h,j,ch in product(range(low,high+1),range(6),range(2)):
        rot=mul(pw(z,h),pw(rho,j))
        ref=[(F(0),F(0)),(F(a),F(0)),(F(a),F(b))] if ch==0 else [(F(0),F(0)),(F(a+b),F(-b)),(F(a),F(0))]
        vertices=[mul(rot,p) for p in ref]
        edges=[(h,j,a),(h,j+1,b),(h+1,j+3,c)] if ch==0 else [(h-1,j,c),(h,j+2,b),(h,j+3,a)]
        types.append({'height':h,'rotation':j,'chirality':ch,'vertices':vertices,'edges':edges})
    directions=sorted({direction(h,j)[0] for t in types for h,j,_ in t['edges']}|{(0,0),(2,1),(3,0)})
    nr=len(types)*3
    eq=[];rhs=[];labels=[]
    boundary={d:[F(0),F(0),F(0)] for d in directions}
    for edge,(h,j,l) in enumerate([(0,0,c*c),(2,1,3*b*(a+b)),(3,3,c*U)]):
        key,s=direction(h,j);mid=scale(F(1,2),add(target[edge],target[(edge+1)%3]))
        boundary[key]=[s*l,s*l*mid[0],s*l*mid[1]]
    for d in directions:
        rows=[[F(0)]*nr for _ in range(3)]
        for t_idx,t in enumerate(types):
            for e,(h,j,l) in enumerate(t['edges']):
                key,s=direction(h,j)
                if key!=d:continue
                mid=scale(F(1,2),add(t['vertices'][e],t['vertices'][(e+1)%3]))
                rows[0][3*t_idx]+=s*l
                for k in range(2):
                    rows[k+1][3*t_idx]+=s*l*mid[k]
                    rows[k+1][3*t_idx+k+1]+=s*l
        for k in range(3):eq.append(rows[k]);rhs.append(F(boundary[d][k]));labels.append((d,k))
    eq.append([F(i%3==0) for i in range(nr)]);rhs.append(F(N));labels.append(('count',))
    for k in range(2):
        row=[F(0)]*nr
        for i,t in enumerate(types):
            row[3*i]=sum(p[k] for p in t['vertices'])/3
            row[3*i+k+1]=F(1)
        eq.append(row);rhs.append(N*sum(p[k] for p in target)/3);labels.append(('area_centroid',k))
    ub=[];ubr=[]
    for i,t in enumerate(types):
        for p,q in zip(target,target[1:]+target[:1]):
            d=sub(q,p)
            for v in t['vertices']:
                row=[F(0)]*nr;row[3*i]=-cross(d,sub(v,p));row[3*i+1]=d[1];row[3*i+2]=-d[0]
                ub.append(row);ubr.append(F(0))
    return types,target,N,eq,rhs,ub,ubr,labels

def solve(a,b,c,low=1,high=2,integral=False):
    import numpy as np
    from scipy.optimize import linprog
    types,target,N,eq,rhs,ub,ubr,labels=build(a,b,c,low,high)
    Ae=np.array(eq,dtype=float);Be=np.array(rhs,dtype=float);Au=np.array(ub,dtype=float);Bu=np.array(ubr,dtype=float)
    se=np.maximum(1,np.max(abs(Ae),axis=1));su=np.maximum(1,np.max(abs(Au),axis=1))
    objective=np.zeros(len(types)*3)
    for i,t in enumerate(types):objective[3*i]=1e-3*(t['rotation']+6*t['chirality'])+abs(t['height']-2)
    bounds=[(0,None) if i%3==0 else (None,None) for i in range(len(objective))]
    if integral:
        from scipy.optimize import milp,Bounds,LinearConstraint
        ilp=milp(objective,integrality=np.array([int(i%3==0) for i in range(len(objective))]),bounds=Bounds([0 if i%3==0 else -np.inf for i in range(len(objective))],np.inf),constraints=[LinearConstraint(Ae/se[:,None],Be/se,Be/se),LinearConstraint(Au/su[:,None],-np.inf,Bu/su)],options={'time_limit':60})
        res=ilp
    else:res=linprog(objective,A_ub=Au/su[:,None],b_ub=Bu/su,A_eq=Ae/se[:,None],b_eq=Be/se,bounds=bounds,method='highs')
    print(res.message,flush=True)
    if res.x is None:return None
    for i,t in enumerate(types):
        if res.x[3*i]>1e-7:print((t['height'],t['rotation'],t['chirality']),res.x[3*i:3*i+3].tolist(),flush=True)
    result={'parameters':[a,b,c,low,high],'status':res.message,'x':res.x.tolist(),'integral':integral}
    return result

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--a',type=int,default=24);p.add_argument('--b',type=int,default=11);p.add_argument('--c',type=int,default=31);p.add_argument('--low',type=int,default=1);p.add_argument('--high',type=int,default=2);p.add_argument('--integral',action='store_true');p.add_argument('--out')
    v=p.parse_args();result=solve(v.a,v.b,v.c,v.low,v.high,v.integral)
    if v.out and result:Path(v.out).write_text(json.dumps(result,indent=2)+'\n')
