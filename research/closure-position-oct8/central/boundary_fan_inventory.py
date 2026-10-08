#!/usr/bin/env python3
"""Exact necessary boundary-fan inventory search, with explicit resource limit."""
import time,json,sys
from functools import lru_cache
from collections import Counter
from pathlib import Path
import fan_probe as fp
import base_profiles as bp
class Timeout(Exception):pass

def run(witness,seconds=30):
    start=time.monotonic();states=0
    inv={w['h']:w['unsigned_A0_to_A5_B0_to_B5'] for w in witness}
    keys=tuple((h,i) for h in sorted(inv) for i in range(12));ix={q:k for k,q in enumerate(keys)}
    initial=tuple(inv[h][i] for h,i in keys)
    tiles=[ix.get((d[1],d[2]),-1) for d in bp.DATA]
    fans={}
    for a in range(6):
      for b in range(6):
        opts=set()
        for fan in fp.fans(a,b):
            counts=Counter(fan)
            if any(k not in ix for k in counts):continue
            x=tuple(sorted((ix[k],v) for k,v in counts.items()))
            if all(initial[k]>=v for k,v in x):opts.add(x)
        fans[a,b]=tuple(sorted(opts,key=lambda x:(sum(n for _,n in x),x)))
    @lru_cache(None)
    def dfs(pos,last2,last,left):
        nonlocal states
        states+=1
        if states%1024==0 and time.monotonic()-start>seconds:raise Timeout
        if pos==154:return ()
        for k,d in enumerate(bp.DATA):
            nx=pos+d[3];ind=tiles[k]
            if ind<0 or left[ind]==0 or nx>154 or not bp.OK[pos,k]:continue
            if pos==0 and k not in (3,5):continue
            if nx==154 and k not in (2,4):continue
            if last!=-1 and not bp.PAIR[last,k]:continue
            if last2!=-1 and not bp.TRIPLE[last2,last,k]:continue
            choices=((),) if last<0 else fans[last,k]
            for fan in choices:
                new=list(left);new[ind]-=1
                if any(new[i]<n for i,n in fan):continue
                for i,n in fan:new[i]-=n
                ans=dfs(nx,last,k,tuple(new))
                if ans is not None:return ((k,fan),)+ans
        return None
    try:
        ans=dfs(0,-1,-1,initial)
        status='EXACT_RELAXATION_FEASIBLE' if ans is not None else 'EXACT_INVENTORY_IMPOSSIBLE'
    except Timeout:ans=None;status='INCOMPLETE'
    return {'status':status,'states':states,'seconds':time.monotonic()-start,'witness_if_feasible':ans,'claim':'Necessary boundary edge and angle-fan inventory; not a full tiling decision.','N154_solved':False}
if __name__=='__main__':
    p=Path(sys.argv[1]);d=json.loads(p.read_text());print(json.dumps(run(d['witness'],float(sys.argv[2]) if len(sys.argv)>2 else 30),indent=2))
