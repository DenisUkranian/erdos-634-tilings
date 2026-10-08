#!/usr/bin/env python3
"""Exact base-junction fan templates; exploratory necessary filter."""
from fractions import Fraction as F
from functools import lru_cache
from collections import Counter
import json
import base_profiles as bp

def mul(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]+a[1]*b[1])
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def sc(a,k):return(a[0]*k,a[1]*k)
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def shift(T,v):return tuple(sub(p,v) for p in T)
def norm(a):
    q=a[0]*a[0]+a[0]*a[1]+a[1]*a[1]
    for d in (7,8,13):
        if q==d*d:return d
    raise ValueError(q)
def unit(a):return sc(a,F(1,norm(a)))
def directions(h):
    z=(F(8,13),F(7,13)) if h>=0 else(F(15,13),F(-7,13))
    q=(F(1),F(0))
    for _ in range(abs(h)):q=mul(q,z)
    for j in range(6):yield q;q=mul(q,(0,1))
def key(T):return tuple(sorted(T))
TEMPLATES=[];BYSHAPE={};BYFIRST={}
for h in range(-4,5):
 for typ in range(2):
  for j,d in enumerate(directions(h)):
   v1=sc(d,8 if typ==0 else 7);v2=mul(sc(d,7 if typ==0 else 8),(-1,1));T=((F(0),F(0)),v1,v2)
   for vertex in range(3):
    t=shift(T,T[vertex]);r=[p for p in t if p!=(0,0)]
    if any(p[1]<0 for p in r):continue
    if det(*r)<0:r.reverse()
    first,last=map(unit,r)
    item=(h,typ*6+j,first,last,key(t))
    TEMPLATES.append(item);BYSHAPE[key(t)]=item;BYFIRST.setdefault(first,[]).append(item)

@lru_cache(None)
def between(first,last):
    if first==last:return ((),)
    out=[]
    for it in BYFIRST.get(first,()):
        end=it[3]
        if det(end,last)<0:continue
        for rest in between(end,last):out.append(((it[0],it[1]),)+rest)
    return tuple(out)

def fans(a,b):
    left=tuple(sc(p,F(1,13)) for p in bp.triangle(a,-bp.DATA[a][3]))
    right=tuple(sc(p,F(1,13)) for p in bp.triangle(b,0))
    end_first=BYSHAPE[key(right)][3];start_last=BYSHAPE[key(left)][2]
    if det(end_first,start_last)<0:return ()
    return between(end_first,start_last)

def viable(a,b,inventory):
    for fan in fans(a,b):
        c=Counter(fan)
        if all(n<=inventory.get(h,[0]*12)[i] for (h,i),n in c.items()):return True
    return False

if __name__=='__main__':
 from pathlib import Path
 root=Path(__file__).resolve().parents[1]
 for p in (root/'layers').glob('filtered*.json'):
    try:d=json.loads(p.read_text());inv={w['h']:w['unsigned_A0_to_A5_B0_to_B5'] for w in d['witness']}
    except KeyError:continue
    allowed={(a,b):viable(a,b,inv) for a in range(6) for b in range(6)}
    print(p.name,sum(allowed.values()),'A3,A3',allowed[4,4])
 print('fan_counts',[[len(fans(a,b)) for b in range(6)] for a in range(6)])
