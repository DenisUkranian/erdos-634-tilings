#!/usr/bin/env python3
"""Exact signed-integer image probe for the two additive phase marginals.

No positivity or physical placement conclusion follows from image membership.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import importlib.util
import json
from math import gcd
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p/'research').is_dir())
spec = importlib.util.spec_from_file_location('additive', ROOT/'research/2026-11-21/semiprimes/global-invariant/additive_gate_model.py')
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)


def system(a,b,c,up,down,positive,negative):
    A, shapes = old.make(a,b,c)
    A=A.tocoo()
    rows=[defaultdict(int) for _ in range(A.shape[0]+2)]
    rhs=[0]*len(rows)
    rhs[6*c]=up; rhs[7*c]=down
    rhs[-2:]=[positive,negative]
    for i,j,v in zip(A.row,A.col,A.data):
        rows[int(i)][int(j)]+=int(v)
    for o,(j,s) in enumerate(shapes):
        sign=s*(-1 if j%2 else 1)
        for t in range(c):
            rows[-2 if sign>0 else -1][o*c+t]=1
    return [{j:v for j,v in row.items() if v} for row in rows],rhs,A.shape[1]


def eliminate(rows,rhs,ncols,include_pivots=False,small_witness=False):
    rows=[dict(row) for row in rows];rhs=list(rhs)
    column=defaultdict(set)
    for i,row in enumerate(rows):
        for j in row:column[j].add(i)
    active=set(range(len(rows)));saved=[];divisions=[];pivot_indices=[]
    started=time.monotonic()
    while active:
        chosen=None;cost=None
        for i in active:
            row=rows[i]
            for j,v in row.items():
                if abs(v)==1:
                    score=(len(row)-1)*(len(column[j])-1)
                    if cost is None or score<cost:
                        chosen=(i,j);cost=score
                    if cost==0:break
            if cost==0:break
        if chosen is None:
            divided=False
            for i in active:
                row=rows[i]
                if not row:
                    if rhs[i]:return {'inconsistent':True,'row':i,'rhs':rhs[i]}
                    continue
                g=0
                for v in row.values():g=gcd(g,v)
                if g>1:
                    if rhs[i]%g:return {'inconsistent':True,'row':i,'gcd':g,'rhs':rhs[i]}
                    rows[i]={j:v//g for j,v in row.items()};rhs[i]//=g
                    divisions.append([i,g]);divided=True
            if divided:continue
            break
        i,j=chosen;row=rows[i];pivot=row[j]
        pivot_indices.append([i,j,pivot])
        saved.append((j,{k:v//pivot for k,v in row.items() if k!=j},rhs[i]//pivot))
        active.remove(i)
        for other in list(column[j]):
            if other==i:continue
            target=rows[other];mult=target[j]//pivot
            for k,v in row.items():
                new=target.get(k,0)-mult*v
                if new:
                    target[k]=new;column[k].add(other)
                elif k in target:
                    del target[k];column[k].discard(other)
            rhs[other]-=mult*rhs[i]
        for k in row:column[k].discard(i)
    rem=[i for i in sorted(active) if rows[i]]
    out={'inconsistent':False,'pivots':len(saved),'divisions':divisions,
         'remaining_rows':len(rem),'remaining_columns':len(set(k for i in rem for k in rows[i])),
         'remaining_nonzeros':sum(len(rows[i]) for i in rem),'seconds':time.monotonic()-started}
    if include_pivots:
        out['pivot_indices']=pivot_indices
        out['remaining']=[{'row':i,'coefficients':sorted(rows[i].items()),'rhs':rhs[i]} for i in rem]
    for i in active:
        if not rows[i] and rhs[i]:return {'inconsistent':True,'row':i,'rhs':rhs[i]}
    x=[0]*ncols
    if rem:
        base=rows[rem[0]];br=rhs[rem[0]]
        if all(rows[i]==base and rhs[i]==br for i in rem):
            # A primitive one-row system always has an integral solution.
            # Accumulate an explicit Bezout combination, preferring small
            # coefficients to avoid unnecessarily large witness entries.
            def egcd(a,b):
                old_r,r=a,b;old_s,s=1,0;old_t,t=0,1
                while r:
                    q=old_r//r
                    old_r,r=r,old_r-q*r
                    old_s,s=s,old_s-q*s
                    old_t,t=t,old_t-q*t
                if old_r<0:return -old_r,-old_s,-old_t
                return old_r,old_s,old_t
            coeff={};g=0
            for j,v in sorted(base.items(),key=lambda pair:abs(pair[1])):
                ng,s,t=egcd(g,v)
                coeff={k:s*w for k,w in coeff.items() if s*w}
                if t:coeff[j]=t
                g=ng
                if g==1:break
            if br%g:return {'inconsistent':True,'remaining_gcd':g,'rhs':br}
            for j,v in coeff.items():x[j]=v*(br//g)
            out['residual_primitive_equations']=1
        else:
            columns=sorted(set(k for i in rem for k in rows[i]))
            patterns={}
            for k in columns:
                pattern=tuple(rows[i].get(k,0) for i in rem)
                patterns.setdefault(pattern,k)
            if len(patterns)>250:
                out['remaining']=[{'row':i,'coefficients':sorted(rows[i].items()),'rhs':rhs[i]} for i in rem]
                return out
            from sympy import ZZ
            from sympy.polys.matrices import DomainMatrix
            from sympy.polys.matrices.normalforms import smith_normal_decomp
            vectors=list(patterns);nr=len(rem);nc=len(vectors)
            A=DomainMatrix([[ZZ(vectors[j][i]) for j in range(nc)] for i in range(nr)],(nr,nc),ZZ)
            D,S,T=smith_normal_decomp(A)
            assert D==S*A*T
            target=S*DomainMatrix([[ZZ(rhs[i])] for i in rem],(nr,1),ZZ)
            dl=D.to_list();bb=target.to_list();z=[ZZ(0)]*nc
            invariants=[]
            for i in range(nr):
                di=dl[i][i] if i<nc else 0
                if not di:
                    if bb[i][0]:return {'inconsistent':True,'smith_zero_row_rhs':int(bb[i][0])}
                else:
                    invariants.append(int(di))
                    if bb[i][0]%di:return {'inconsistent':True,'smith_diagonal':int(di),'smith_rhs':int(bb[i][0])}
                    z[i]=bb[i][0]//di
            free=(T*DomainMatrix([[v] for v in z],(nc,1),ZZ)).to_list()
            if small_witness:
                # Optional discovery-only optimization. The resulting integer
                # vector is checked exactly before it replaces the Smith one.
                import numpy as np
                from scipy.optimize import Bounds,LinearConstraint,milp
                mat=np.array(vectors,dtype=float).T
                doubled=np.c_[mat,-mat]
                rhs_array=np.array([rhs[i] for i in rem],dtype=float)
                answer=milp(np.ones(2*nc),integrality=np.ones(2*nc),
                    bounds=Bounds(0,np.inf),constraints=LinearConstraint(doubled,rhs_array,rhs_array),
                    options={'time_limit':10})
                if answer.x is not None:
                    candidate=[int(round(answer.x[j]))-int(round(answer.x[nc+j])) for j in range(nc)]
                    if all(sum(vectors[j][i]*candidate[j] for j in range(nc))==rhs[r] for i,r in enumerate(rem)):
                        free=[[v] for v in candidate]
                        out['residual_small_integer_witness_verified']=True
            for pattern,entry in zip(vectors,free):x[patterns[pattern]]=int(entry[0])
            out['residual_smith_invariants']=invariants
            out['distinct_residual_columns']=nc
    for j,row,b in reversed(saved):x[j]=b-sum(v*x[k] for k,v in row.items())
    out['signed_integer_witness']=[[j,v] for j,v in enumerate(x) if v]
    out['maximum_absolute_multiplicity']=max(map(abs,x))
    out['negative_variables']=sum(v<0 for v in x)
    return out


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target',type=int,choices=(3431,5063),required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    a,b,c=(33,7,37) if args.target==3431 else (35,13,43)
    positive,negative=(74,37) if c==37 else (129,86)
    up,down=2*c-2*(a-b),-c+2*(a-b)
    rows,rhs,ncols=system(a,b,c,up,down,positive,negative)
    out=eliminate(rows,rhs,ncols)
    out.update(tile=[a,b,c],profile=[up,down],positive=positive,negative=negative,
        scope='Signed integer additive marginal image only; positivity, full periodic two-coordinate currents, nonoverlap and tiling are not asserted.')
    if 'signed_integer_witness' in out:
        x=dict(out['signed_integer_witness'])
        assert all(sum(v*x.get(j,0) for j,v in row.items())==r for row,r in zip(rows,rhs))
        out['exact_rows_verified']=len(rows)
    args.out.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('signed_integer_witness','remaining')},indent=2))

if __name__=='__main__':main()
