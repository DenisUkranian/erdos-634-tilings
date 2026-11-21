#!/usr/bin/env python3
"""Finite-window balanced terminal-cell search with one accessible parent class.

Any positive output is checked geometrically. Failure in this catalogue is
not a lower bound for unrestricted placements.
"""
from collections import Counter,defaultdict
from fractions import Fraction as F
from pathlib import Path
import argparse,importlib.util,json,time

import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import coo_array

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4]
spec=importlib.util.spec_from_file_location('terminal_bank',ROOT/'research/2026-11-21/semiprimes/integer-closure/long-banks/long_bank_completion.py')
bank=importlib.util.module_from_spec(spec);spec.loader.exec_module(bank)
U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))


def mul(p,q):return p[0]*q[0]-p[1]*q[1],p[0]*q[1]+p[1]*q[0]+p[1]*q[1]


def run(radius,seconds,cap,outpath):
    a,b,c=5,3,7;z=(F(a,c),F(b,c));polys=[];labels=[];cols=[];eps=[];events=defaultdict(set)
    for x in range(-radius,radius+1):
        for y in range(-radius,radius+1):
            for j in range(6):
                for s in (-1,1):
                    poly=bank.ccw(((x,y),(x-a*U[j][0],y-a*U[j][1]),(x+b*U[(j+s)%6][0],y+b*U[(j+s)%6][1])))
                    col=Counter()
                    for p,q in zip(poly,poly[1:]+poly[:1]):
                        if bank.norm(bank.sub(q,p))==c*c:continue
                        line,direction,origin,t=bank.line_data(p,q,c)
                        for v,sign in ((p,1),(q,-1)):
                            col[line,v]+=sign
                            if (a*v[0]-b*v[1])%c==0:
                                coordinate=0 if direction[0] else 1
                                t=v[coordinate]/direction[coordinate]
                                residue=t-t.numerator//t.denominator
                                events[line,direction,origin,residue].add(t)
                    labels.append((x,y,j,s));polys.append(poly);cols.append(col);eps.append(s*(-1)**j)
    n_inner=len(labels);lookup={t:i for i,t in enumerate(labels)};pair_rows=[];banned=[]
    for i,(x,y,j,s) in enumerate(labels):
        ux=x-a*U[j][0];uy=y-a*U[j][1]
        if s==-1 and (a*ux-b*uy)%c==0:continue
        mate=(x-a*U[j][0]+b*U[(j+s)%6][0],y-a*U[j][1]+b*U[(j+s)%6][1],(j+3)%6,s)
        if mate not in lookup:banned.append(i)
        elif i<lookup[mate]:pair_rows.append({i:1,lookup[mate]:-1})
    for (line,direction,origin,residue),values in sorted(events.items()):
        t=min(values);upper=max(values)
        while t+1<=upper:
            p=bank.add(origin,bank.scale(t,direction));q=bank.add(p,direction)
            for sign in (-1,1):
                for poly in bank.triangle_choices(dict(p=p,q=q,coefficient=sign),a,b,c):
                    if not all(all(v.denominator==1 for v in mul(point,z)) for point in poly):continue
                    polys.append(poly);cols.append(Counter({(line,p):sign,(line,q):-sign}));eps.append(0)
            t+=1
    n=len(polys);rowids={key:i for i,key in enumerate(sorted(set().union(*(col.keys() for col in cols))))}
    rr=[];cc=[];vv=[]
    for j,col in enumerate(cols):
        for key,value in col.items():rr.append(rowids[key]);cc.append(j);vv.append(value)
        rr.append(len(rowids)+(0 if j<n_inner else 2));cc.append(j);vv.append(1)
        if eps[j]:rr.append(len(rowids)+1);cc.append(j);vv.append(eps[j])
    for k,row in enumerate(pair_rows):
        for j,v in row.items():rr.append(len(rowids)+3+k);cc.append(j);vv.append(v)
    rows=len(rowids)+3+len(pair_rows)
    A=coo_array((np.asarray(vv,dtype=float),(np.asarray(rr,dtype=np.int32),np.asarray(cc,dtype=np.int32))),shape=(rows,n)).tocsc()
    lo=np.zeros(rows);hi=lo.copy();lo[len(rowids)]=hi[len(rowids)]=14;hi[len(rowids)+2]=cap
    lb=np.zeros(n);ub=np.ones(n);ub[banned]=0
    objective=np.zeros(n);objective[n_inner:]=1
    conflicts=set();trace=[];start=time.monotonic();witness=None
    while time.monotonic()-start<seconds:
        constraints=[LinearConstraint(A,lo,hi)]
        if conflicts:
            rr=[];cc=[]
            for i,(u,v) in enumerate(sorted(conflicts)):rr.extend((i,i));cc.extend((u,v))
            C=coo_array((np.ones(len(rr)),(np.asarray(rr,dtype=np.int32),np.asarray(cc,dtype=np.int32))),shape=(len(conflicts),n)).tocsc()
            constraints.append(LinearConstraint(C,0,1))
        result=milp(objective,integrality=np.ones(n),bounds=Bounds(lb,ub),constraints=constraints,options={'time_limit':min(10,max(1,seconds-(time.monotonic()-start))),'mip_rel_gap':0})
        item=dict(status=int(result.status),message=str(result.message),objective=result.fun,seconds=time.monotonic()-start,conflicts=len(conflicts));trace.append(item);print(item,flush=True)
        if result.x is None:break
        xx=np.rint(result.x).astype(int);ids=np.flatnonzero(xx).tolist()
        assert np.max(np.abs(A@xx-np.minimum(np.maximum(A@xx,lo),hi)))==0
        collision={(j,i) for k,i in enumerate(ids) for j in ids[:k] if bank.overlaps(polys[i],polys[j])}
        if collision:conflicts.update(collision);continue
        branch=[i for i in ids if i<n_inner];parents=[i for i in ids if i>=n_inner]
        assert len(branch)==14 and sum(eps[i] for i in branch)==0 and len(parents)<=cap
        witness=dict(branch_labels=[labels[i] for i in branch],parent_polygons=[polys[i] for i in parents])
        break
    output=dict(scope=__doc__,radius=radius,inner_columns=n_inner,total_columns=n,rows=rows,bank_cap=cap,trace=trace,witness=witness)
    outpath.write_text(json.dumps(output,indent=2,default=str)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k!='trace'},default=str),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--radius',type=int,default=8);p.add_argument('--seconds',type=int,default=55);p.add_argument('--cap',type=int,default=4);p.add_argument('--out',type=Path,required=True);q=p.parse_args();run(q.radius,q.seconds,q.cap,q.out)
