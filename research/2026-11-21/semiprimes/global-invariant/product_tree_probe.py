#!/usr/bin/env python3
"""Exact chains in a product of Bass--Serre trees.

This is an auxiliary group invariant, not a physical tiling verifier.
An edge ((prefix, factor), group) is oriented from its factor-coset
vertex to its group vertex. Unit physical edges map A-then-B when
j mod 6 is 0, 1 or 2, and B-then-A otherwise; reversal is exact.
"""
from collections import defaultdict
from functools import lru_cache
from math import gcd

def mul(g,i,e,m):
 e%=m
 if not e:return g
 if g and g[-1][0]==i:
  k=(g[-1][1]+e)%m
  return g[:-1]+(((i,k),) if k else ())
 return g+((i,e),)

def edge_path(g,i,e,m):
 h=mul(g,i,e,m)
 if h==g:return h,[]
 star=(g[:-1] if g and g[-1][0]==i else g,i)
 return h,[((star,g),-1),((star,h),1)]

def rootpath(g,m):
 out=[];state=()
 for i,e in g:
  state,path=edge_path(state,i,e,m);out+=path
 return out

def label(h,j,a,b,c):
 ss=b*pow(c,-1,a)%a;tt=a*pow(c,-1,b)%b
 k=(j+h)%6;l=j%6
 return (k%3,(-1 if k>=3 else 1)*pow(ss,h%2,a)),(l%3,(-1 if l>=3 else 1)*pow(tt,h%2,b))

def develop(segments,a,b,c):
 ga=gb=();C=defaultdict(int);boundary=defaultdict(int)
 def amove(g,idx,e):
  nonlocal ga
  ga,p=edge_path(ga,idx,e,a)
  for ea,va in p:
   boundary[('A',ea,('G',gb))]+=va
   for eb,vb in rootpath(gb,b):C[ea,eb]-=va*vb
 def bmove(g,idx,e):
  nonlocal gb
  gb,p=edge_path(gb,idx,e,b)
  for eb,vb in p:boundary[('B',('G',ga),eb)]+=vb
 for L,h,j in segments:
  al,bl=label(h,j,a,b,c)
  for _ in range(L):
   if j%6<3:
    amove(ga,*al);bmove(gb,*bl)
   else:
    bmove(gb,*bl);amove(ga,*al)
 assert ga==gb==(),(ga,gb)
 return ({k:v for k,v in C.items() if v},
         {k:v for k,v in boundary.items() if v})

def fill(segments,a,b,c):
 return develop(segments,a,b,c)[0]

def square_boundary(chain):
 """Independently take the cellular boundary of a square 2-chain."""
 boundary=defaultdict(int)
 for (ea,eb),v in chain.items():
  sa,ga=ea;sb,gb=eb
  boundary[('A',ea,('S',sb))]+=v
  boundary[('A',ea,('G',gb))]-=v
  boundary[('B',('G',ga),eb)]+=v
  boundary[('B',('S',sa),eb)]-=v
 return {k:v for k,v in boundary.items() if v}

def stats(C):
 blocks=defaultdict(lambda:[0,0,0])
 for (ea,eb),v in C.items():
  k=(ea[0],eb[0]);blocks[k][0]+=abs(v);blocks[k][1]+=v;blocks[k][2]+=1
 return {'norm':sum(abs(v) for v in C.values()),'support':len(C),'max':max(map(abs,C.values()),default=0),'blocks':dict(blocks)}

if __name__=='__main__':
 for a,b,c in [(5,3,7),(33,7,37),(35,13,43)]:
  N=(a+2*b)*(2*a+b);A=b*(2*a+b);B=a*(a+2*b)
  boundary=fill([(A,0,0),(c*c,2,1),(B,0,4)],a,b,c)
  tile=fill([(a,0,0),(b,0,1),(c,1,3)],a,b,c)
  normb=stats(boundary);normt=stats(tile)
  print((a,b,c),N,'board',normb,'tile',normt,'ratio',normb['norm']/normt['norm'],flush=True)
