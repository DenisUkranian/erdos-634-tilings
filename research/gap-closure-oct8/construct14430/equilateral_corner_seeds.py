#!/usr/bin/env python3
"""Enumerate all two-tile alpha/beta fans at the origin in a saved pool."""
import argparse,json
from pathlib import Path
from itertools import combinations

def mul(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]+a[1]*b[1])
def rot(a):return(-a[1],sum(a))
def times(a,n):return(a[0]*n,a[1]*n)
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def same(a,b):return cross(a,b)==0 and a[0]*b[0]+a[1]*b[1]>0

def main():
 ap=argparse.ArgumentParser();ap.add_argument('prefix');ar=ap.parse_args();prefix=ar.prefix
 r=json.loads(Path(prefix+'.json').read_text());q=r['family_parameter'];L,U=r['L'],r['U'];rotcount=r['basis_rotation']
 a=q*(3*q+2);b=2*q+1;eta=(2*q+1,-q);bar=(q+1,q)
 def power(p,n):
  out=(1,0)
  for i in range(n):out=mul(out,p)
  return out
 inv=mul(power(eta,-L),power(bar,U))
 for i in range(rotcount):inv=rot(inv)
 rays=[inv,rot(inv)];candidates={};ori=0
 for h in range(L,U+1):
  u=mul(power(eta,h-L),power(bar,U-h))
  for i in range(rotcount):u=rot(u)
  for order in [0,1]:
   x=times(u,b if order else a);y=times(rot(rot(u)),a if order else b)
   for j in range(6):
    t=[(0,0),x,y]
    for k in [1,2]:
     p=t[k];cone=(sub(t[(k+1)%3],p),sub(t[(k+2)%3],p))
     candidates[(ori,-p[0],-p[1])]=cone
    ori+=1;x=rot(x);y=rot(y)
 found={}
 with open(prefix+'.remaining.txt')as f:
  next(f)
  for line in f:
   record=tuple(map(int,line.split()))
   if record in candidates:found[record]=candidates[record]
 fans=[]
 for s,c in found.items():
  if not same(c[0],rays[0]):continue
  for t,d in found.items():
   if same(c[1],d[0]) and same(d[1],rays[1]):fans.append([s,t])
 for i,fan in enumerate(fans):Path(prefix+f'.corner{i}.txt').write_text('2\n'+'\n'.join(' '.join(map(str,s))for s in fan)+'\n')
 Path(prefix+'.corner_fans.json').write_text(json.dumps(fans)+'\n');print(json.dumps({'fans':fans,'available_corner_tiles':len(found)}))
if __name__=='__main__':main()
