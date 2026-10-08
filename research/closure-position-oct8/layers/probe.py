#!/usr/bin/env python3
"""Necessary affine-line capacity check; exploratory, exact integer arithmetic."""
from functools import lru_cache
from fractions import Fraction as F
import json

def comp(n,k):
    if k==1:yield(n,);return
    for x in range(n+1):
        for t in comp(n-x,k-1):yield(x,)+t

def mul(a,b):
    x,y=a;u,v=b
    return x*u-y*v,x*v+y*u+y*v

def dirs(h):
    z=(F(8,13),F(7,13)) if h>=0 else (F(15,13),F(-7,13))
    a=(F(1),F(0))
    for _ in range(abs(h)):a=mul(a,z)
    out=[]
    for _ in range(3):out.append(a);a=mul(a,(0,1))
    return out

def cap(h,j):
    x,y=dirs(h)[j]
    vals=(0,-154*y,56*x-49*y)
    return F(8624)/(max(vals)-min(vals))

# Atomic zero-sum multisets in residues +8,-8,+7,-7 mod 13.
atoms=[]
for n in range(1,14):
    for p in comp(n,4):
        if (8*(p[0]-p[1])+7*(p[2]-p[3]))%13:continue
        if any(all(a<=b for a,b in zip(q,p)) for q in atoms):continue
        atoms.append(p)

@lru_cache(None)
def max_lines(total,wanted,cap_floor):
    if sum(total)==0:return 0
    best=-1000000
    for p in atoms:
        if not all(a<=b for a,b in zip(p,total)):continue
        if 8*p[0]+7*p[2]>cap_floor or 8*p[1]+7*p[3]>cap_floor:continue
        tail=tuple(b-a for a,b in zip(p,total))
        best=max(best,max_lines(tail,wanted,cap_floor)+(p[wanted]>0))
    return best

def edge(j,length):return (j%3,(0 if length==8 else 2)+(j>=3))
edges=[(edge(j,8 if t==0 else 7),edge((j+5)%6,7 if t==0 else 8)) for t in range(2) for j in range(6)]
def violates(inv,h):
    total=[[0]*4 for _ in range(3)]
    for n,ee in zip(inv,edges):
        for j,t in ee:total[j][t]+=n
    for i,(n,ee) in enumerate(zip(inv,edges)):
        if not n:continue
        limits=[max_lines(tuple(total[j]),t,int(cap(h,j))) for j,t in ee]
        if min(limits)<0 or n>limits[0]*limits[1]:return {'orientation':i,'count':n,'limits':limits,'totals':total}
    return None

def actuals(A,B,n):
    inv=[0]*12
    for t,vec in enumerate((A,B)):
        for j,v in enumerate(vec):inv[6*t+j if v>=0 else 6*t+j+3]=abs(v)
    d=n-sum(inv)
    if d<0 or d%2:return
    for q in comp(d//2,6):
        out=inv.copy()
        for k,v in enumerate(q):out[6*(k//3)+k%3]+=v;out[6*(k//3)+k%3+3]+=v
        yield tuple(out)

if __name__=='__main__':
    from pathlib import Path
    inp=Path(__file__).resolve().parents[2]/'closure-position-oct7/oct8-structural/all_height_direction_probe.json'
    report={'status':'EXPLORATORY','atoms':atoms,'records':[]}
    for rec in json.loads(inp.read_text())['records']:
        if 'witness' not in rec:continue
        r={'support':rec['support'],'levels':[]}
        for w in rec['witness']:
            if w['h']==0:continue
            tried=0;good=0;example=None
            for inv in actuals(w['A'],w['B'],w['n']):
                tried+=1
                if not violates(inv,w['h']):good+=1;example=inv
            r['levels'].append({'h':w['h'],'n':w['n'],'expanded':tried,'surviving':good,'example':example})
        report['records'].append(r)
    print(json.dumps(report,indent=2))
