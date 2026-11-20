"""Independently enumerate small triangles by two integer sides and their included angle."""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from math import isqrt

def check(a,b,c,cap):
 # Store a unit complex number as (cos(theta), sin(theta)/sqrt(3)).
 def product(w,z):return w[0]*z[0]-3*w[1]*z[1],w[0]*z[1]+w[1]*z[0]
 angles=set()
 for i in range(4):
  for j in range(4):
   r=(1,0)
   for k in range(i):r=product(r,(F(a+2*b,2*c),F(a,2*c)))
   for k in range(j):r=product(r,(F(2*a+b,2*c),F(b,2*c)))
   if r[1]>0:angles.add(r)
 cosines={p for p,q in angles}
 maxside=isqrt(cap*a*(2*a+b))
 ok={0}
 for l in range(1,maxside+1):
  if any(l-m in ok for m in (a,b,c)):ok.add(l)
 sides=sorted(ok-{0}); counts=set()
 for cosine,sine in angles:
  top=2*sine.numerator;bottom=a*b*sine.denominator
  for v,w in combinations_with_replacement(sides,2):
   num=top*v*w
   if num>cap*bottom or num%bottom:continue
   n=num//bottom
   d=v*v+w*w-2*v*w*cosine
   if d.denominator!=1:continue
   z=isqrt(int(d))
   if z*z!=d or z not in ok:continue
   if F(w*w+z*z-v*v,2*w*z) not in cosines or F(v*v+z*z-w*w,2*v*z) not in cosines:continue
   counts.add(int(n))
 print((a,b,c),'independent integer-side scan',maxside,sorted(counts))
 assert counts=={k*k for k in range(1,isqrt(cap)+1)}
if __name__=='__main__':
 check(33,7,37,167);check(35,13,43,72)
