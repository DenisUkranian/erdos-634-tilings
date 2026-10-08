#!/usr/bin/env python3
'''Complete direction-inventory support projection for a five-height band.
All states retain population used. No minimum-cost dominance or chosen witness
is substituted for enumeration of feasible terminal paths. Exact integer DP.
The local capacity screens are necessary, not sufficient for planar tilings.
'''
from pathlib import Path
import sys,json,argparse,time
from collections import defaultdict
from functools import lru_cache
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'research/closure-position-oct8/layers'))
import filtered_dp as old
from probe import actuals,violates
from probe_central_24 import classify

def run(L,U,seconds):
    if U-L!=4 or not L<=0<=U:raise ValueError('K5 band containing0 required')
    start=time.monotonic();history=[];calls=0
    def checktime():
        if time.monotonic()-start>seconds:raise TimeoutError
    base=lambda h:24 if h==0 else 26
    # At one nonzero level, the maximum remaining allocation is52.
    lim=154-sum(base(h) for h in range(L,U+1))+26
    groups=defaultdict(list)
    for x in range(-lim,lim+1):
      for y in range(-lim+abs(x),lim-abs(x)+1):
       rem=lim-abs(x)-abs(y)
       for z in range(-rem,rem+1):
        B=(x,y,z);S=old.s1(B);groups[tuple(v%13 for v in S)].append((B,old.norm(B),S))
    zero=(0,0,0);A=tuple(-v//13 for v in old.target(L-1));initial=(A,zero,0)
    states={initial};transitions=[]
    for h in range(L,U+1):
      new=set();edges=[];F=old.target(h);suffix=sum(base(k) for k in range(h+1,U+1))
      for A,Bprev,used in states:
        left=old.s0(A);required=tuple((f-v)%13 for f,v in zip(F,left));available=154-used-suffix-old.norm(A)
        if available<0:continue
        for B,bnorm,right in groups.get(required,[]):
          if bnorm>available:continue
          size=old.norm(A)+bnorm
          n=11+13*max(0,(size-11+12)//13) if h==0 else 13*max(1,(size+12)//13)
          n=max(n,base(h))
          if (n-size)%2:n+=13
          if used+n+suffix>154:continue
          if h==U and old.scale(13,old.r2(B))!=old.target(U+1):continue
          q=old.sub(old.add(left,right),F)
          if not all(v%13==0 for v in q):raise AssertionError('integrality')
          Anext=old.add(tuple(v//13 for v in q),old.r2(Bprev))
          if h==U and Anext!=zero:continue
          if h<U and old.norm(Anext)>154-used-n-(suffix-base(h+1)):continue
          while used+n+suffix<=154:
            calls+=1
            if old.local_feasible(h,A,B,n):
              dest=(Anext,B,used+n);new.add(dest);edges.append(((A,Bprev,used),dest,(A,B,n)))
            n+=26
            checktime()
      states=new;transitions.append(edges)
      history.append(dict(height=h,states=len(states),transitions=len(edges),seconds=time.monotonic()-start))
      print(json.dumps(history[-1]),flush=True)
      if not states:return dict(status='EXACT_UNSAT_NECESSARY_MODEL',band=[L,U],history=history,seconds=time.monotonic()-start)
    terminal={s for s in states if s[2]==154}
    live=terminal;local=[set() for _ in transitions]
    for k in range(len(transitions)-1,-1,-1):
      previous=set()
      for src,dst,rec in transitions[k]:
        if dst in live:previous.add(src);local[k].add(rec)
      live=previous
    if initial not in live:return dict(status='EXACT_UNSAT_NECESSARY_MODEL',band=[L,U],history=history,seconds=time.monotonic()-start)
    # Retain population correlations, not only coordinatewise minima/maxima.
    profiles={initial:{()}}
    for edges in transitions:
      nextprofiles=defaultdict(set)
      for src,dst,rec in edges:
        for profile in profiles.get(src,()):nextprofiles[dst].add(profile+(rec[2],))
      profiles=nextprofiles
    population_profiles=sorted(set().union(*(profiles[t] for t in terminal)))
    support=[]
    for k,records in enumerate(local):
      h=L+k;mask=0;witnesses={};checked=0;feasible=0;populations=sorted({r[2] for r in records})
      print(json.dumps(dict(projecting_height=h,local_records=len(records),populations=populations)),flush=True)
      for A,B,n in sorted(records):
        for inv in actuals(A,B,n):
          checked+=1
          if (classify(inv) if h==0 else not violates(inv,h)):
            feasible+=1
            for i,num in enumerate(inv):
              if num and i not in witnesses:witnesses[i]=dict(A=A,B=B,n=n,unsigned=inv)
              if num:mask|=1<<i
          if mask==4095:break
          if checked%100==0:checktime()
        if mask==4095:break
      support.append(dict(h=h,local_signed_records=len(records),populations=populations,support_mask=mask,can_be_positive=[i for i in range(12) if mask>>i&1],universally_zero=[i for i in range(12) if not(mask>>i&1)],witnesses=witnesses,local_inventories_checked=checked,local_inventories_feasible=feasible,enumeration_stopped_after_full_support=(mask==4095)))
    return dict(status='EXACT_SUPPORT_PROJECTION',band=[L,U],history=history,terminal_states=len(terminal),population_profiles=population_profiles,support=support,calls=calls,seconds=time.monotonic()-start,meaning='Support over the necessary direction and affine-line model. A positive support witness is not a geometric tiling.',N154_solved=False)

def main():
 p=argparse.ArgumentParser();p.add_argument('--lo',type=int,required=True);p.add_argument('--hi',type=int,required=True);p.add_argument('--seconds',type=int,default=240);p.add_argument('--output',required=True);args=p.parse_args()
 try:r=run(args.lo,args.hi,args.seconds)
 except TimeoutError:r=dict(status='INCOMPLETE_TIMEOUT',band=[args.lo,args.hi],N154_solved=False)
 Path(args.output).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in ('support','history')}))
if __name__=='__main__':main()
