#!/usr/bin/env python3
"""Exact finite dynamic program for the 154 Laurent inventory obstruction.

This uses integers only. See INVENTORY_SUPPORT.md for completeness of the
W parametrization, the bound |W_h| <= 13, and the population cost.
No geometric sufficiency is claimed for any surviving formal inventory.
"""
import json
from pathlib import Path

N=154
BOUND=13

def uv(h,p,w,q):
    return (-8 if h==0 else 0)+w-13*q, (-7 if h==0 else -13 if h==1 else 0)-w+13*p

def cost(h,p,w,q):
    u,v=uv(h,p,w,q);s=abs(u)+abs(v)
    if h==0:
        n=11+13*max(0,(s-11+12)//13)
    else:
        n=13*max(1,(s+12)//13)
    if (n-u-v)%2:n+=13
    return n

def solve(L,U):
    states={(0,0):(0,[])}
    # States after h hold (W_h,W_{h+1}), cost through h and W_{L+1..h+1}.
    for h in range(L,U+1):
        following={}
        for (p,w),(old,path) in states.items():
            if h==U and w!=(1 if U==0 else 0):continue
            values=[0] if h==U else range(-BOUND,BOUND+1)
            for q in values:
                new=old+cost(h,p,w,q)
                if new>N:continue
                key=(w,q)
                if key not in following or new<following[key][0]:
                    following[key]=(new,path+[q])
        states=following
    if not states:return {'support':[L,U],'status':'EXCLUDED_BY_EXACT_INVENTORY_DP'}
    best=min(states.values());total,path=best
    W={L-1:0,L:0};W.update({L+1+i:q for i,q in enumerate(path)})
    records=[]
    for h in range(L,U+1):
        u,v=uv(h,W[h-1],W[h],W[h+1]);n=cost(h,W[h-1],W[h],W[h+1])
        records.append({'h':h,'U':u,'V':v,'n':n})
    assert (N-total)%26==0
    records[-L]['n']+=N-total
    assert sum(r['n'] for r in records)==N
    d={r['h']:r for r in records}
    for h in range(L-1,U+2):
        u=d.get(h,{}).get('U',0);v=d.get(h,{}).get('V',0)
        left=d.get(h-1,{}).get('U',0);right=d.get(h+1,{}).get('V',0)
        assert u+v-13*left-13*right==(154 if h==0 else 91 if abs(h)==1 else 0)
    for r in records:
        assert r['n']>=abs(r['U'])+abs(r['V']) and (r['n']-r['U']-r['V'])%2==0
        assert r['n']>0 and r['n']%13==(11 if r['h']==0 else 0)
    return {'support':[L,U],'status':'EXACT_FORMAL_WITNESS','minimum_under_154':total,'witness':records}

def main():
    rows=[solve(L,L+K-1) for K in range(3,13) for L in range(1-K,1)]
    excluded=[r['support'] for r in rows if r['status'].startswith('EXCLUDED')]
    result={'status':'PASS','scope':'Exact signed inventory only; no geometric sufficiency','full_Erdos634_solved':False,'case154_solved':False,'supports':len(rows),'excluded_supports':excluded,'surviving_supports':len(rows)-len(excluded),'records':rows}
    out=Path(__file__).with_name('inventory_exact.json');out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'}))

if __name__=='__main__':main()
