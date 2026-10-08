#!/usr/bin/env python3
"""Exact signed direction DP for E45 tiled by 135 (3,5,7) triangles.
The population lower bounds are explicit assumptions linked in README.
"""
from collections import defaultdict
import json,time,argparse
from pathlib import Path
from line_filter import feasible,actuals,violates,central_violates

def r2(v):return(-v[1],-v[2],v[0])
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(k,a):return tuple(k*x for x in a)
def norm(v):return sum(map(abs,v))
def s0(v):return sub(mul(3,v),mul(5,r2(v)))
def s1(v):return sub(mul(5,v),mul(3,r2(v)))
def target(h):return (45,-45,45) if h==0 else (0,0,0)

def run(support,seconds=120):
 L,U=min(support),max(support);support=set(support)
 base=lambda h:9 if h==0 else 14 if h in support else 0
 start=time.monotonic();budget=135-sum(base(h) for h in support)
 lim=max((base(h)+budget for h in support),default=0);groups=defaultdict(list)
 for x in range(-lim,lim+1):
  for y in range(-lim+abs(x),lim-abs(x)+1):
   rem=lim-abs(x)-abs(y)
   for z in range(-rem,rem+1):
    B=(x,y,z);S=s1(B);groups[tuple(v%7 for v in S)].append((B,norm(B),S))
 zero=(0,0,0);states={(zero,zero):(0,[])};hist=[]
 for h in range(L,U+1):
  new={};F=target(h);suffix=sum(base(k) for k in range(h+1,U+1));occupied=h in support
  for (A,Bprev),(used,path) in states.items():
   left=s0(A);required=tuple((f-v)%7 for f,v in zip(F,left));avail=135-used-suffix-norm(A)
   if avail<0 or (not occupied and norm(A)>0):continue
   for B,bnorm,right in groups.get(required,[]) if occupied else [(zero,0,zero)]:
    if bnorm>avail:continue
    size=norm(A)+bnorm
    if occupied:
     n=2+7*max(0,(size-2+6)//7) if h==0 else 7*max(1,(size+6)//7)
     n=max(n,base(h))
     if(n-size)%2:n+=7
    else:n=0
    if used+n+suffix>135:continue
    if h==U and B!=zero:continue
    q=sub(add(left,right),F)
    if any(v%7 for v in q):continue
    Anext=add(tuple(v//7 for v in q),r2(Bprev))
    if h==U and Anext!=zero:continue
    if h<U and norm(Anext)>135-used-n-(suffix-base(h+1)):continue
    while used+n+suffix<=135 and not feasible(h,A,B,n):n+=14
    if used+n+suffix>135:continue
    key=(Anext,B);total=used+n
    if key not in new or total<new[key][0]:new[key]=(total,path+[{'h':h,'A':A,'B':B,'n':n}])
   if time.monotonic()-start>seconds:return {'status':'INCOMPLETE','support':sorted(support),'history':hist,'height':h,'seconds':time.monotonic()-start}
  states=new;hist.append({'h':h,'states':len(states),'seconds':time.monotonic()-start})
  print(json.dumps({'support':sorted(support),'progress':hist[-1]}),flush=True)
  if not states:return{'status':'EXACT_FORMAL_UNSAT','support':sorted(support),'history':hist,'seconds':time.monotonic()-start,'N':135,'filters':'unsigned affine-line chord caps; central boundary-line inventories'}
 total,path=min(states.values());padding=135-total
 # Adding antipodal pairs preserves all signed currents and adds14 perheight.
 assert padding%14==0,(total,path)
 path[-L]['n']+=padding
 for w in path:
  for inv in actuals(w['A'],w['B'],w['n']):
   if not (central_violates(inv) if w['h']==0 else violates(inv,w['h'])):
    w['unsigned_A0_to_A5_B0_to_B5']=inv;break
  else:raise AssertionError('Final padding failed necessary local filters')
 return{'status':'FORMAL_FEASIBLE_NOT_GEOMETRIC','support':sorted(support),'witness':path,'history':hist,'seconds':time.monotonic()-start,'N':135,'filters':'unsigned affine-line chord caps; central boundary-line inventories'}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--support',default='0,1,2,3');p.add_argument('--seconds',type=float,default=120);a=p.parse_args()
 support=list(map(int,a.support.split(',')));result=run(support,a.seconds)
 out=Path(__file__).with_name('support_'+('_'.join(map(str,support)))+'.json');out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
