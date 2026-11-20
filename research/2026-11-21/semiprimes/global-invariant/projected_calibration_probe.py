#!/usr/bin/env python3
"""Diagnostic LP on product-tree square coefficients supported on the board filling."""
from product_tree_probe import fill, stats, mul
from collections import defaultdict
from functools import lru_cache
import numpy as np
from scipy.sparse import coo_matrix
from scipy.optimize import linprog
import argparse,time,json

def gm(g,h,m):
 for i,e in h:g=mul(g,i,e,m)
 return g

def inv(g,m):return tuple((i,(-e)%m) for i,e in g[::-1])

def run(a,b,c):
 start=time.time();A=b*(2*a+b);B=a*(a+2*b)
 bd=fill([(A,0,0),(c*c,2,1),(B,0,4)],a,b,c)
 rows={k:i for i,k in enumerate(bd)};stars={(ea[0],eb[0]) for ea,eb in bd}
 cols={};witnesses=[]; attempts=0
 for h in range(6):
  for j in range(6):
   for s in [-1,1]:
    seg=[(a,h,j),(b,h,j+1),(c,h+1,j+3)] if s>0 else [(b,h,j+2),(a,h,j+3),(c,h-1,j)]
    f=fill(seg,a,b,c);tile_stars={(ea[0],eb[0]) for ea,eb in f}
    ea_set={ea for ea,eb in f};eb_set={eb for ea,eb in f}
    for sa,sb in tile_stars:
     for ta,tb in stars:
      if sa[1]!=ta[1] or sb[1]!=tb[1]:continue
      assert ta[0]==tb[0]==()
      iga=inv(sa[0],a);igb=inv(sb[0],b)
      ea_maps=[];eb_maps=[]
      for r in range(a):
       gA=gm(mul((),ta[1],r,a),iga,a);ma={}
       for ea in ea_set:
        pref,idx=ea[0];gpre=gm(gA,pref,a);star=(gpre[:-1] if gpre and gpre[-1][0]==idx else gpre,idx)
        ma[ea]=(star,gm(gA,ea[1],a))
       ea_maps.append((gA,ma))
      for t in range(b):
       gB=gm(mul((),tb[1],t,b),igb,b);mb={}
       for eb in eb_set:
        pref,idx=eb[0];gpre=gm(gB,pref,b);star=(gpre[:-1] if gpre and gpre[-1][0]==idx else gpre,idx)
        mb[eb]=(star,gm(gB,eb[1],b))
       eb_maps.append((gB,mb))
      for gA,ma in ea_maps:
       for gB,mb in eb_maps:
        attempts+=1;col={}
        for (ea,eb),v in f.items():
         key=(ma[ea],mb[eb]);k=rows.get(key)
         if k is not None:col[k]=col.get(k,0)+v
        sig=tuple(sorted((k,v) for k,v in col.items() if v))
        if sig and sig not in cols:
         cols[sig]=len(cols);witnesses.append((h,j,s,gA,gB))
  print('height',h,'unique',len(cols),'seconds',time.time()-start,flush=True)
 ii=[];jj=[];vv=[]
 for col,k in cols.items():
  for row,val in col:ii.append(row);jj.append(k);vv.append(val)
 M=coo_matrix((vv,(ii,jj)),shape=(len(rows),len(cols))).tocsc()
 rhs=np.array(list(bd.values()),float)
 res=linprog(np.ones(len(cols)),A_eq=M,b_eq=rhs,bounds=(0,None),method='highs',options={'time_limit':40})
 print('solve',res.status,res.message,res.fun,'total seconds',time.time()-start,flush=True)
 out={'tile':[a,b,c],'scope':'Projection to finite board-filling square support only; all abstract positive tile translates included, no physical geometry. Float feasibility is diagnostic, not a tiling.','rows':len(rows),'columns':len(cols),'attempts':attempts,'status':int(res.status),'message':res.message,'objective':res.fun,'seconds':time.time()-start}
 if res.x is not None:out['support']=[{'placement':witnesses[i],'weight':float(v)} for i,v in enumerate(res.x) if v>1e-8];out['maximum_residual']=float(np.max(abs(M@res.x-rhs)))
 return out

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('a',type=int);p.add_argument('b',type=int);p.add_argument('c',type=int);p.add_argument('--out',required=True);args=p.parse_args()
 r=run(args.a,args.b,args.c);open(args.out,'w').write(json.dumps(r,indent=2)+'\n')
