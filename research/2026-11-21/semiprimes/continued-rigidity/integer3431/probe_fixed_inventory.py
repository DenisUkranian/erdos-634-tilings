#!/usr/bin/env python3
"""Exact small kernel discovery with a specified orientation inventory."""
import argparse,json,time
from collections import Counter,defaultdict
from pathlib import Path
from small_balanced_kernel import columns
from functools import lru_cache
columns=lru_cache(maxsize=4)(columns)

def run(a,b,c,inventory):
    labels,cols,inc=columns(a,b,c);orientation=[p[2:] for p in labels]
    start_orientation=min(inventory,key=lambda v:inventory[v]);first=labels.index((0,0,*start_orientation))
    remaining=dict(inventory);remaining[start_orientation]-=1
    states=0;seen=set();answer=None
    def dfs(selected,R,left):
        nonlocal states,answer
        if answer is not None:return
        key=tuple(sorted(selected))
        if key in seen:return
        seen.add(key);states+=1
        rem=sum(left.values())
        if not R:
            if rem==0:answer=key
            return
        if rem==0 or sum(abs(v) for v in R.values())>4*rem:return
        candidates=[]
        for r,v in R.items():
            opts=[k for k in inc[(r,-1 if v>0 else 1)] if left.get(orientation[k],0)>0]
            if not opts:return
            if not candidates or len(opts)<len(candidates):candidates=opts
        for k in candidates:
            S=dict(R)
            for r,v in cols[k].items():
                S[r]=S.get(r,0)+v
                if not S[r]:del S[r]
            ori=orientation[k];left[ori]-=1;dfs(selected+(k,),S,left);left[ori]+=1
    t=time.monotonic();dfs((first,),cols[first],remaining)
    return {'tile':[a,b,c],'inventory':[[*o,n] for o,n in inventory.items()],'states':states,'seconds':time.monotonic()-t,'found':answer is not None,'support':None if answer is None else [labels[k] for k in answer],'scope':'Exact periodic integer kernel discovery in one specified inventory; no nonoverlap or tiling assertion.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);args=p.parse_args()
    d=run(35,13,43,{(3,-1):1,(1,1):1,(2,1):6,(2,-1):6});args.out.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d,indent=2))
