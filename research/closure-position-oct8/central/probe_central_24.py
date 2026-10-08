#!/usr/bin/env python3
"""Exact necessary line-capacity screen, not a tiling search."""
import sys,json,time
from pathlib import Path
from collections import defaultdict,Counter
from functools import lru_cache
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'closure-position-oct7/oct8-structural'))
from check_no_thirteen_height import compositions,EDGES,signature
PLUS=[i for i in range(12) if (1 if i<6 else -1)*(-1)**(i%6)==1]
MINUS=[i for i in range(12) if i not in PLUS]

def small_atoms(n):
    atoms=[]
    for size in range(1,n+1):
      for v in compositions(size,4):
        if (8*(v[0]-v[1])+7*(v[2]-v[3]))%13:continue
        if not any(all(a<=x for a,x in zip(at,v)) for at in atoms): atoms.append(v)
    return tuple(atoms)
ATOMS=small_atoms(13)
@lru_cache(None)
def maxlines(v,wanted=0,cap=1000):
    if not any(v):return 0
    best=-1000
    for atom in ATOMS:
        if all(x>=a for x,a in zip(v,atom)) and 8*atom[0]+7*atom[2]<=cap and 8*atom[1]+7*atom[3]<=cap:
            rest=tuple(x-a for x,a in zip(v,atom))
            best=max(best,int(atom[wanted]>0)+maxlines(rest,wanted,cap))
    return best

def inventories(n):
    target=(11,0,0)
    for np in range(n+1):
        if (2*np-n-11)%13: continue
        bank=defaultdict(list)
        for counts in compositions(n-np,6):
            inv=[0]*12
            for i,x in zip(MINUS,counts): inv[i]=x
            bank[signature(inv)].append(inv)
        for counts in compositions(np,6):
            inv=[0]*12
            for i,x in zip(PLUS,counts):inv[i]=x
            sig=signature(inv);need=tuple((t-x)%13 for t,x in zip(target,sig))
            for b in bank.get(need,[]):yield tuple(a+c for a,c in zip(inv,b))

def classify(inv):
    totals=[[0]*4 for _ in range(3)]
    for n,edges in zip(inv,EDGES):
        for d,l in edges: totals[d][(0 if abs(l)==8 else 2)+(l<0)]+=n
    other=[[maxlines(tuple(v),t,56) for t in range(4)] for v in totals[1:]]
    if any(min(v)<0 for v in other):return []
    feasible=[]
    # Exterior edges all point in the positive base direction.
    for b8 in range(totals[0][0]+1):
      for b7 in range(totals[0][2]+1):
        length=8*b8+7*b7
        if length>154 or (154-length)%13:continue
        rest=(totals[0][0]-b8,totals[0][1],totals[0][2]-b7,totals[0][3])
        baseother=[maxlines(rest,t,154) for t in range(4)]
        if min(baseother)<0:continue
        lm=[[baseother[t]+int((t==0 and b8>0) or (t==2 and b7>0)) for t in range(4)]]+other
        # Positive 8-edge: A0 or B1. Positive 7-edge: B0 or A1.
        if b8>min(inv[0],lm[2][3])+min(inv[7],lm[1][2]):continue
        if b7>min(inv[6],lm[2][1])+min(inv[1],lm[1][0]):continue
        if any(n>lm[ed[0][0]][(0 if abs(ed[0][1])==8 else 2)+(ed[0][1]<0)]*lm[ed[1][0]][(0 if abs(ed[1][1])==8 else 2)+(ed[1][1]<0)] for n,ed in zip(inv,EDGES)):continue
        feasible.append((b8,b7,(154-length)//13,lm))
    return feasible

def run(n):
    start=time.time();allcount=0;survive=0;examples=[];sizes=Counter()
    for inv in inventories(n):
        allcount+=1
        ok=classify(inv)
        if ok:
            survive+=1
            plus=sum(inv[i] for i in PLUS);sizes[plus]+=1
            if len(examples)<12:examples.append({'inventory':inv,'possible_base8_base7_base13_lines':ok})
    return {'population':n,'all_modular_inventories':allcount,'survive_necessary_capacity_screen':survive,'by_plus_population':dict(sizes),'examples':examples,'seconds':time.time()-start,'status':'EXHAUSTIVE_NECESSARY_SCREEN','N154_solved':False}
if __name__=='__main__':print(json.dumps(run(int(sys.argv[1]) if len(sys.argv)>1 else 24),indent=2))
