#!/usr/bin/env python3
"""Exact first-return periodic kernel search, with multiplicities allowed.

The search stops when its residual first becomes zero. An exact-size exclusion
of all kernels needs the separate component-size induction in
SMALL_BALANCED_CELLS.md; this program alone does not enumerate decomposable
kernels at arbitrary sizes (for example two independent six-tile wheels).
"""
from collections import Counter,defaultdict
import argparse,json,time
from pathlib import Path
U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))

def columns(a,b,c):
    labels=[];cols=[];inc=defaultdict(list)
    def row(j,p):return (j%3,p[0]%c,p[1]%c)
    for x in range(c):
        for y in range(c):
            q=x,y
            for j in range(6):
                for s in (-1,1):
                    u=x-a*U[j][0],y-a*U[j][1]
                    w=x+b*U[(j+s)%6][0],y+b*U[(j+s)%6][1]
                    C=Counter()
                    for axis,p,v in ((j,q,s),(j,u,-s),(j+s,w,s),(j+s,q,-s)):C[row(axis,p)]+=v
                    C={r:v for r,v in C.items() if v}
                    k=len(labels);labels.append((x,y,j,s));cols.append(C)
                    for r,v in C.items():inc[(r,v)].append(k)
    return labels,cols,inc

def search(a,b,c,total):
    labels,cols,inc=columns(a,b,c);first=labels.index((0,0,0,1));states=0;seen=set();solutions=[]
    def visit(selected,residual,charge):
        nonlocal states
        key=tuple(sorted(selected))
        if key in seen:return
        seen.add(key);states+=1
        left=total-len(selected)
        if abs(charge)>left or (left-charge)%2:return
        if not residual:
            if left==0 and charge==0:solutions.append(key)
            return
        if left==0 or sum(abs(v) for v in residual.values())>4*left:return
        # Every completion must supply an opposite contribution at this row.
        r,v=max(residual.items(),key=lambda rv:(abs(rv[1]),rv[0]))
        needed=-1 if v>0 else 1
        for k in inc[(r,needed)]:
            C=dict(residual)
            for p,d in cols[k].items():
                C[p]=C.get(p,0)+d
                if not C[p]:del C[p]
            j,s=labels[k][2:];eps=s*(-1 if j%2 else 1)
            visit(selected+(k,),C,charge+eps)
    t=time.monotonic();visit((first,),cols[first],1)
    return {'tile':[a,b,c],'total':total,'normalized_first_tile':[0,0,0,1],'visited_states':states,'solutions':[[labels[k] for k in I] for I in solutions],'seconds':time.monotonic()-t,'scope':'Exact first-return all-residue positive integer endpoint kernels of the stated size and charge zero, modulo a symmetry sending one tile to (0,0,0,+1). Multiplicities allowed. Stops at closed proper prefixes; a full-population exclusion requires the separately stated component-size induction. No gate constraints.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('a',type=int);p.add_argument('b',type=int);p.add_argument('c',type=int);p.add_argument('--total',type=int,required=True);p.add_argument('--out',type=Path,required=True);args=p.parse_args();r=search(args.a,args.b,args.c,args.total);args.out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v if k!='solutions' else len(v) for k,v in r.items()},indent=2))
