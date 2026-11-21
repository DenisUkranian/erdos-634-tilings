#!/usr/bin/env python3
"""Orientation-moment filtering and exact fixed-inventory kernel discovery."""
import argparse,json,time
from collections import defaultdict
from pathlib import Path
from probe_fixed_inventory import run

ORIENTATIONS=tuple((j,s) for j in range(6) for s in (-1,1))
POS=tuple((j,s) for j,s in ORIENTATIONS if s*(-1 if j%2 else 1)==1)
NEG=tuple(((j+3)%6,s) for j,s in POS)

def comps(n,m=6):
    if m==1:
        yield (n,);return
    for x in range(n+1):
        for tail in comps(n-x,m-1):yield (x,)+tail

def inventories(a,b,c,total):
    k=total//2
    bysig=defaultdict(list)
    def signature(v):
        d=[0,0,0]
        for n,(j,s) in zip(v,POS):d[j%3]+=a*n;d[(j+s)%3]-=b*n
        return tuple(x%c for x in d)
    for v in comps(k):bysig[signature(v)].append(v)
    seen=set();out=[];raw=0
    for group in bysig.values():
        for p in group:
            for n in group:
                raw+=1
                D={o:v for o,v in zip(POS,p)};D.update({o:v for o,v in zip(NEG,n)})
                orbit=[]
                for flip in (False,True):
                    for rot in range(6):
                        E={(((-j if flip else j)+rot)%6,-s if flip else s):v for (j,s),v in D.items()}
                        orbit.append(tuple(E[o] for o in ORIENTATIONS))
                canon=min(orbit)
                if canon not in seen:
                    seen.add(canon);out.append({o:v for o,v in zip(ORIENTATIONS,canon) if v})
    return raw,out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('a',type=int);p.add_argument('b',type=int);p.add_argument('c',type=int);p.add_argument('--total',type=int,required=True);p.add_argument('--out',type=Path,required=True);args=p.parse_args()
    t=time.monotonic();raw,inv=inventories(args.a,args.b,args.c,args.total);print(json.dumps({'raw_inventories':raw,'orbits':len(inv)}),flush=True)
    out={'tile':[args.a,args.b,args.c],'total':args.total,'raw_inventories':raw,'orbits':len(inv),'checked':[],'scope':'Moment-compatible orientation inventories modulo dihedral symmetry. Fixed-inventory search may stop on a closed proper component; completeness for an excluded nonmultiple-of-six size depends on the separately established absence of smaller nonmultiple-of-six balanced kernels.'}
    for i,D in enumerate(inv):
        r=run(args.a,args.b,args.c,D);out['checked'].append(r)
        if i%10==0 or r['found']:print(json.dumps({'index':i,'states':r['states'],'found':r['found'],'elapsed':time.monotonic()-t}),flush=True)
        args.out.write_text(json.dumps(out,indent=2)+'\n')
        if r['found']:break
    out['completed']=len(out['checked'])==len(inv);out['seconds']=time.monotonic()-t;args.out.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='checked'}),flush=True)
