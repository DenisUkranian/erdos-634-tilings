#!/usr/bin/env python3
"""Diagnostic integer-charge model on two endpoint marginals.

A numerical solver status is not an exported exact infeasibility proof.
"""
from additive_gate_model import make,U
import numpy as np
from scipy.sparse import coo_matrix,hstack,vstack
from scipy.optimize import milp,Bounds,LinearConstraint
from pathlib import Path
import argparse,time,json,math

def run(a,b,c,seconds,cutfile=None,cutlimit=None):
    old,shapes=make(a,b,c);nt=old.shape[1];gb=6*c;d=a-b
    remote=[i for i in range(2*c) if i not in [0,c]];nr=len(remote)
    n=nt+2*c+2*nr;pbase=nt+2*c;mbase=pbase+nr
    M=hstack([old,coo_matrix((old.shape[0],n-nt))]).tolil();rhs=np.zeros(old.shape[0]);rhs[gb]=2*c;rhs[gb+c]=-c
    for g in range(2*c):M[gb+g,nt+g]=-d
    M=M.tocsc();lo=np.zeros(n);hi=np.full(n,np.inf);integ=np.zeros(n);integ[nt:]=1
    cap=51 if c==43 else 44
    for i,(j,s) in enumerate(shapes):
        eps=s*(-1)**j
        hi[i*c:(i+1)*c]=2*c if eps>0 else c
        hi[(12+i)*c:(13+i)*c]=2*c if eps>0 else c
    for g in remote:lo[nt+g]=-1;hi[nt+g]=cap//d
    for g,offset in [(0,2*c),(c,-c)]:lo[nt+g]=math.ceil((-c-offset)/d);hi[nt+g]=math.floor((cap-offset)/d)
    hi[pbase:mbase]=2*c//d;hi[mbase:]=c//d
    ii=[];jj=[];vv=[];lower=[];upper=[]
    def add(entries,l,u):
        r=len(lower)
        for col,val in entries:
            if val:ii.append(r);jj.append(col);vv.append(val)
        lower.append(l);upper.append(u)
    for i,g in enumerate(remote):add([(nt+g,1),(pbase+i,-1),(mbase+i,1)],0,0)
    add([(pbase+i,1) for i in range(nr)],0,2*c//d);add([(mbase+i,1) for i in range(nr)],0,c//d)
    for eps in [1,-1]:
        entries=[]
        for k,(j,s) in enumerate(shapes):
            if s*(-1)**j==eps:entries.extend((k*c+r,1) for r in range(c))
        count=2*c if eps>0 else c;add(entries,count,count)
    # Each positive physical tile contributes to exactly one of these bins.
    bins=[[] for _ in range(2*c)]
    for kind,(lx,ly) in enumerate([(-b,a),(a,-b)]):
        for k,(j,s) in enumerate(shapes):
            if s*(-1)**j<0 or (s>0)!=(kind==0):continue
            du=-a*(lx*U[j][0]+ly*U[j][1])
            for r in range(c):bins[kind*c+(r+du)%c].append(((kind*12+k)*c+r,1))
    for entries in bins:add(entries,0,cap)
    E=coo_matrix((vv,(ii,jj)),shape=(len(lower),n)).tocsc();M=vstack([M,E]).tocsc()
    obj=np.zeros(n);obj[pbase:]=1
    lows=np.r_[rhs,lower];highs=np.r_[rhs,upper];cut_count=0
    if cutfile is not None:
        raw=list(map(int,Path(cutfile).read_text().split()));cc,dd,_,_,_,count,_=raw[:7];assert (cc,dd)==(c,d)
        cut_count=count if cutlimit is None else min(count,cutlimit);cuts=[];at=7
        for _ in range(count):
            D=raw[at];at+=1;wu=raw[at:at+c];at+=c;wd=raw[at:at+c];at+=c
            cuts.append((D,wu,wd))
        oldn=n;n+=2*cut_count;M=hstack([M,coo_matrix((M.shape[0],2*cut_count))]).tocsc()
        lo=np.r_[lo,np.full(2*cut_count,-np.inf)];hi=np.r_[hi,np.full(2*cut_count,np.inf)]
        integ=np.r_[integ,np.zeros(2*cut_count)];obj=np.r_[obj,np.zeros(2*cut_count)]
        ii=[];jj=[];vv=[];lower=[];upper=[]
        for k,(D,wu,wd) in enumerate(cuts[:cut_count]):
            for kind,w in enumerate([wu,wd]):
                offset=2*c if kind==0 else -c
                for shift in range(c):
                    entries=[(oldn+2*k+kind,1)]
                    entries.extend((nt+kind*c+r,-d*w[(r+shift)%c]/D) for r in range(c))
                    add(entries,offset*w[shift]/D,np.inf)
            add([(oldn+2*k,1),(oldn+2*k+1,1)],-np.inf,3*c)
        E=coo_matrix((vv,(ii,jj)),shape=(len(lower),n)).tocsc();M=vstack([M,E]).tocsc()
        lows=np.r_[lows,lower];highs=np.r_[highs,upper]
    start=time.monotonic();res=milp(obj,integrality=integ,bounds=Bounds(lo,hi),constraints=LinearConstraint(M,lows,highs),options={'time_limit':seconds,'mip_rel_gap':0.0})
    out={'tile':[a,b,c],'odd_population':3*c,'status':int(res.status),'message':res.message,'seconds':time.monotonic()-start,
         'rows':M.shape[0],'columns':n,'translation_saturated_cuts':cut_count,'scope':'Necessary additive continuous-marginal/integer-gate relaxation. Feasibility is not a physical tiling; numerical infeasibility requires independent exact proof.'}
    for key in ['mip_node_count','mip_gap','mip_dual_bound','fun']:
        value=getattr(res,key,None)
        if value is not None:out[key]=float(value)
    if res.x is not None:
        x=res.x
        out['up_gate_charges']=np.rint(x[nt:nt+c]).astype(int).tolist();out['down_gate_charges']=np.rint(x[nt+c:nt+2*c]).astype(int).tolist()
        out['marginal_support']=[[k//c,k%c,float(v)] for k,v in enumerate(x[:nt]) if v>1e-8]
        val=M@x;out['max_constraint_violation']=float(max(0,np.max(lows-val),np.max(val-highs)))
        out['max_integrality_error']=float(np.max(abs(x[integ>0]-np.rint(x[integ>0]))))
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('a',type=int);p.add_argument('b',type=int);p.add_argument('c',type=int);p.add_argument('--seconds',type=float,default=60);p.add_argument('--out',type=Path,required=True);p.add_argument('--cuts',type=Path);p.add_argument('--cut-limit',type=int);ar=p.parse_args()
    out=run(ar.a,ar.b,ar.c,ar.seconds,ar.cuts,ar.cut_limit);ar.out.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='marginal_support'},indent=2))
