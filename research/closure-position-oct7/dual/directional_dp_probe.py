#!/usr/bin/env python3
"""Exact signed-direction DP for a fixed population vector; resource-bounded."""
from collections import defaultdict
import json,time,argparse
from pathlib import Path

def r2(v):return (-v[1],-v[2],v[0])
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def scale(k,a):return tuple(k*x for x in a)
def norm(v):return sum(map(abs,v))
def s0(v):return sub(scale(8,v),scale(7,r2(v)))
def s1(v):return sub(scale(7,v),scale(8,r2(v)))
def target(h):return (154,0,0) if h==0 else (0,0,91) if h==1 else (0,-91,0) if h==-1 else (0,0,0)

def run_variable(L,U,seconds=60,maxstates=1000000):
    K=U-L+1;start=time.time();lim=154-(11+13*(K-1))+13;groups=defaultdict(list)
    for x in range(-lim,lim+1):
      for y in range(-lim+abs(x),lim-abs(x)+1):
       rem=lim-abs(x)-abs(y)
       for z in range(-rem,rem+1):
        B=(x,y,z);S=s1(B);groups[tuple(v%13 for v in S)].append((B,norm(B),S))
    A=tuple(-v//13 for v in target(L-1));zero=(0,0,0)
    states={(A,zero):(0,[])};history=[]
    for h in range(L,U+1):
        new={};F=target(h);suffix=sum(11 if k==0 else 13 for k in range(h+1,U+1))
        for (A,Bprev),(used,path) in states.items():
            left=s0(A);required=tuple((f-v)%13 for f,v in zip(F,left));available=154-used-suffix-norm(A)
            if available<0:continue
            for B,bnorm,right in groups.get(required,[]):
                if bnorm>available:continue
                size=norm(A)+bnorm
                n=11+13*max(0,(size-11+12)//13) if h==0 else 13*max(1,(size+12)//13)
                if (n-size)%2:n+=13
                if used+n+suffix>154:continue
                if h==U and scale(13,r2(B))!=target(U+1):continue
                q=sub(add(left,right),F);assert all(v%13==0 for v in q)
                Anext=add(tuple(v//13 for v in q),r2(Bprev))
                if h==U and Anext!=zero:continue
                if h<U and norm(Anext)>154-used-n-(suffix-(11 if h+1==0 else 13)):continue
                key=(Anext,B);total=used+n
                if key not in new or total<new[key][0]:new[key]=(total,path+[{'h':h,'A':A,'B':B,'n':n}])
        states=new;history.append({'height':h,'states':len(states),'seconds':time.time()-start})
        if not states:return {'status':'EXACT_UNSAT','support':[L,U],'history':history}
        if len(states)>maxstates or time.time()-start>seconds:return {'status':'INCOMPLETE','support':[L,U],'history':history}
    total,path=min(states.values())
    assert (154-total)%26==0
    path[-L]['n']+=154-total
    return {'status':'EXACT_FORMAL_FEASIBLE','support':[L,U],'history':history,'witness':path}

def run(L,pops,seconds=60,maxstates=1000000):
    U=L+len(pops)-1;start=time.time();lim=max(pops);groups=defaultdict(list)
    for x in range(-lim,lim+1):
      for y in range(-lim+abs(x),lim-abs(x)+1):
       rem=lim-abs(x)-abs(y)
       for z in range(-rem,rem+1):
        B=(x,y,z);S=s1(B);groups[tuple(v%13 for v in S)].append((B,norm(B),S))
    A=tuple(-v//13 for v in target(L-1));zero=(0,0,0)
    states={(A,zero):None};history=[]
    for i,n in enumerate(pops):
        h=L+i;new={};F=target(h)
        for (A,Bprev) in states:
            left=s0(A);required=tuple((f-v)%13 for f,v in zip(F,left));available=n-norm(A)
            if available<0:continue
            for B,bnorm,right in groups.get(required,[]):
                if bnorm>available or (bnorm-available)%2:continue
                if h==U and scale(13,r2(B))!=target(U+1):continue
                q=sub(add(left,right),F);assert all(v%13==0 for v in q)
                Anext=add(tuple(v//13 for v in q),r2(Bprev))
                if h==U and Anext!=zero:continue
                if h<U and norm(Anext)>pops[i+1]:continue
                new[Anext,B]=(A,Bprev)
        states=new;history.append({'height':h,'states':len(states),'seconds':time.time()-start})
        print(json.dumps(history[-1]),flush=True)
        if not states:return {'status':'EXACT_UNSAT','support':[L,U],'pops':pops,'history':history}
        if len(states)>maxstates or time.time()-start>seconds:return {'status':'INCOMPLETE','support':[L,U],'pops':pops,'history':history}
    return {'status':'FORMAL_FEASIBLE','support':[L,U],'pops':pops,'history':history}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--lo',type=int,default=0);p.add_argument('--hi',type=int);p.add_argument('--pops',default='24,'+','.join(['13']*10));p.add_argument('--seconds',type=int,default=60);p.add_argument('--output',default='directional_dp_0_10.json');a=p.parse_args()
    result=run(a.lo,list(map(int,a.pops.split(','))),a.seconds) if a.hi is None else run_variable(a.lo,a.hi,a.seconds)
    Path(__file__).with_name(a.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
