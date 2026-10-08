#!/usr/bin/env python3
"""Exact comparison of reduced bands in one physical coordinate frame.

Coordinates are normalized to denominator7^8 and vertices of each triangle
are sorted. Optional reference pool tests literal containment, with reflection
(x,y)->(y,x) in the equilateral target also tested.
"""
import argparse,hashlib,json,struct
from collections import Counter
from pathlib import Path

if not __debug__:
 raise RuntimeError("Run this exact verifier without Python -O or -OO.")

DENOMINATOR=7**8
PACK=struct.Struct('<6q')
def add(a,b):return a[0]+b[0],a[1]+b[1]
def multiply(a,b):return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]+a[1]*b[1]
def scale(a,n):return a[0]*n,a[1]*n
def rotate(a):return -a[1],a[0]+a[1]
def power(a,n):
 r=(1,0)
 for _ in range(n):r=multiply(r,a)
 return r

def pool(prefix):
 j=json.loads(Path(str(prefix)+'.json').read_text());assert not j['incomplete'] and not j['conflict'];L,U=j['L'],j['U'];r=j['basis_rotation'];assert U-L<=8
 frame=multiply(power((2,1),-L),power((3,-1),U))
 for _ in range(r):frame=rotate(frame)
 norm=frame[0]**2+frame[0]*frame[1]+frame[1]**2;assert norm==7**(U-L)
 inverse_numerator=(frame[0]+frame[1],-frame[1]);factor=DENOMINATOR//norm;assert factor*norm==DENOMINATOR
 templates=[]
 for h in range(L,U+1):
  u=multiply(power((2,1),h-L),power((3,-1),U-h))
  for _ in range(r):u=rotate(u)
  for order in range(2):
   a=scale(u,5 if order else 3);b=scale(rotate(rotate(u)),3 if order else 5)
   for _ in range(6):templates.append(((0,0),a,b));a=rotate(a);b=rotate(b)
 result=set();counts=Counter()
 with Path(str(prefix)+'.remaining.txt').open() as f:
  lo,hi,n=map(int,next(f).split());assert (lo,hi,n)==(L,U,j['remaining'])
  for line in f:
   o,x,y=map(int,line.split());vs=[]
   for p in templates[o]:
    v=scale(multiply(add((x,y),p),inverse_numerator),factor)
    assert v[0]>=0 and v[1]>=0 and v[0]+v[1]<=45*DENOMINATOR
    vs.append(v)
   v=tuple(z for p in sorted(vs) for z in p);assert v not in result;result.add(v);counts[L+o//12]+=1
 assert len(result)==n
 return result,dict(sorted(counts.items()))

def digest(items):
 h=hashlib.sha256()
 for row in sorted(items):h.update(PACK.pack(*row))
 return h.hexdigest()

def reflect(t):
 return tuple(c for p in sorted([(t[1],t[0]),(t[3],t[2]),(t[5],t[4])]) for c in p)

def main():
 p=argparse.ArgumentParser();p.add_argument('prefixes',nargs='+',type=Path);p.add_argument('--reference',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 reference,counts=pool(a.reference);assert all(reflect(t) in reference for t in reference)
 report={'coordinate_denominator':DENOMINATOR,'binary_record':'six little-endian signed64 integers, lexicographically sorted triangle vertices and triangle records','reference_prefix':str(a.reference),'reference_count':len(reference),'reference_sha256':digest(reference),'reference_reflection_invariant':True,'reference_by_height':counts,'pools':[]}
 for prefix in a.prefixes:
  items,heights=pool(prefix);missing=items-reference;reflected_missing={reflect(t) for t in items}-reference
  assert not missing and not reflected_missing, (prefix,len(missing),len(reflected_missing))
  report['pools'].append({'prefix':str(prefix),'count':len(items),'normalized_sha256':digest(items),'contained_in_reference':True,'reflection_contained_in_reference':True,'by_height':heights})
  print(prefix,len(items),'contained and reflected-contained',flush=True)
 a.output.write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
