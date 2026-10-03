"""Reversed F4 construction via the free-k reflected-beta corner shave.
Exact Eisenstein coordinates x+y*rho, rho=exp(i*pi/3).
Construction condition: k*c >= m*(a-b), with m*b*c-a*a*k in <a,b>.
"""
from fractions import Fraction as F
from math import gcd
import json,argparse
from pathlib import Path

def add(p,q):return (p[0]+q[0],p[1]+q[1])
def sub(p,q):return (p[0]-q[0],p[1]-q[1])
def smul(k,p):return (k*p[0],k*p[1])
def cmul(p,q):return (p[0]*q[0]-p[1]*q[1],p[0]*q[1]+p[1]*q[0]+p[1]*q[1])
def grid(p,q,r,n):
 u=smul(F(1,n),sub(q,p));v=smul(F(1,n),sub(r,p))
 for i in range(n):
  for j in range(n-i):
   o=add(p,add(smul(i,u),smul(j,v)));x=add(o,u);y=add(o,v)
   yield[o,x,y]
   if i+j<n-1:yield[x,add(x,v),y]

def semigroup_witness(a,b,c,m,k):
 n=m*b*c-a*a*k;g=gcd(a,b)
 if not(k>=1 and k*c>=m*(a-b)) or n<0 or n%g:
  raise ValueError('The free-k corner-shave condition fails')
 aa,bb,nn=a//g,b//g,n//g
 A=0 if bb==1 else (nn*pow(aa,-1,bb))%bb
 B=(n-A*a)//b
 if B<0:raise ValueError('The free-k corner-shave condition fails')
 assert A*a+B*b==n and m*c>a*k
 return A,B

def choose_k(a,b,c,m):
 low=(m*(a-b)+c-1)//c
 # Primitive case: the first possible k is optimal.  For nonprimitive
 # triples membership need not be monotone, so check every finite candidate.
 for k in range(low,(m*b*c)//(a*a)+1):
  try:
   semigroup_witness(a,b,c,m,k)
   return k
  except ValueError:pass
 raise ValueError('No free-k corner-shave witness exists')

def q_tiles(a,b,c,m,k):
 t=a-b;r=m*b*c-a*a*k
 Acoef,Bcoef=semigroup_witness(a,b,c,m,k)
 assert min(Acoef,Bcoef)>=0 and Acoef*a+Bcoef*b==r
 z=(F(a,c),F(b,c))
 origin=(F(0),F(0));A=(F(m*c*c),F(0));B=(F(m*a*a),F(m*a*b))
 C=(F(m*a*t),F(m*b*t));E=(F(k*a*c),F(0));D=add(C,E)
 U=add(C,smul(k*a*a,z));V=add(E,smul(a*(m*c-k*a),z))
 # Low kc-by-mt parallelogram, with its mt-by-mt grid corner removed.
 u=(F(a),F(0));v=(F(a),F(b));n=m*t
 for i in range(k*c):
  for j in range(n):
   o=add(smul(i,u),smul(j,v));x=add(o,u);y=add(o,v)
   if i+j>=n:yield[o,x,y]
   if i+j>=n-1:yield[x,add(x,v),y]
 yield from grid(C,D,U,k*a)
 yield from grid(E,A,V,m*c-k*a)
 # High parallelogram U-D-V-B: a width decomposition along z.
 w=smul(F(1,k*a*b),sub(D,U))
 offset=0
 for count,width,height in ((Acoef,a,b),(Bcoef,b,a)):
  for _ in range(count):
   base=add(U,smul(offset,z));du=smul(width,z);dv=smul(height,w)
   for j in range(k*a*b//height):
    o=add(base,smul(j,dv));x=add(o,du);y=add(o,dv);xy=add(x,dv)
    yield[o,x,xy];yield[o,xy,y]
   offset+=width
 assert offset==r

def construct(a,b,c,m,k=None):
 if not(0<b<a and c*c==a*a+a*b+b*b and m>0):raise ValueError('Require a>b>0, norm square and m>0')
 if k is None:k=choose_k(a,b,c,m)
 witness=semigroup_witness(a,b,c,m,k)
 u=(F(b),F(a));O=(F(0),F(0));A=(F(b*c),F(0));D=(F((a+b)*c),F(0))
 C=smul(F(b*(2*a+b),c),u);E=add(A,smul(F(a*b,c),u));H=add(A,(F(0),F(b*c)))
 Bbig=smul(m*c,u);rot=smul(F(-1,c),u)
 triangles=[[add(Bbig,cmul(rot,p)) for p in tri] for tri in q_tiles(a,b,c,m,k)]
 qcount=len(triangles)
 assert qcount==3*a*b*m*m
 for p,q,r,n in ((A,D,E,m*a),(D,C,E,m*a),(H,A,E,m*b)):
  triangles.extend(grid(smul(m,p),smul(m,q),smul(m,r),n))
 def enc(p):return[[str(x),str(y)]for x,y in p]
 return {'format':'ERDOS634_F4_UNIT_TRIANGLES_V1','coordinate_metric':'x^2+x*y+y^2','tile':[a,b,c],'multiplier':m,'count':(2*a+b)*(a+b)*m*m,'target':enc([smul(m,p)for p in(O,D,C)]),'triangles':[enc(p)for p in triangles],'construction':'free-k reflected-beta corner shave','semigroup_witness':{'a_coefficient':witness[0],'b_coefficient':witness[1],'r_k':m*b*c-a*a*k,'free_k':k},'Q_count':qcount}



def construct_f2(a,b,c,m,k=None):
 """Same corner grid, reflected into F2 and joined to two cR grids."""
 if not(0<b<a and c*c==a*a+a*b+b*b and m>0):raise ValueError('Require a>b>0, norm square and m>0')
 if k is None:k=choose_k(a,b,c,m)
 witness=semigroup_witness(a,b,c,m,k)
 S=c*c;U=a+2*b;V=2*a+b;z=(F(a),F(b));z2=cmul(z,z)
 origin=(F(0),F(0));B=(F(m*S),F(0));I=smul(m*a,z);J=smul(m,z2);C=smul(F(m*a*U,S),z2)
 v2=smul(F(1,S),cmul((F(-a-b),F(a)),(F(-a-b),F(a))))
 def conj(w):return (w[0]+w[1],-w[1])
 def reflect(w):return add(B,cmul(v2,conj(sub(w,B))))
 triangles=[[reflect(p)for p in tri]for tri in q_tiles(a,b,c,m,k)]
 triangles.extend(grid(origin,B,I,m*c));triangles.extend(grid(origin,I,J,m*c))
 def enc(p):return[[str(x),str(y)]for x,y in p]
 return {'format':'ERDOS634_F2_UNIT_TRIANGLES_V1','coordinate_metric':'x^2+x*y+y^2','tile':[a,b,c],'multiplier':m,'count':U*V*m*m,'target':enc([origin,B,C]),'triangles':[enc(p)for p in triangles],'construction':'free-k reflected-beta corner shave, reflected F2 residual','semigroup_witness':{'a_coefficient':witness[0],'b_coefficient':witness[1],'r_k':m*b*c-a*a*k,'free_k':k}}


if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('a',type=int);ap.add_argument('b',type=int);ap.add_argument('c',type=int);ap.add_argument('m',type=int);ap.add_argument('--k',type=int);ap.add_argument('--family',choices=['F4','F2'],default='F4');ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
 data=(construct if args.family=='F4' else construct_f2)(args.a,args.b,args.c,args.m,args.k);args.output.write_text(json.dumps(data)+'\n');print('wrote',data['count'],'tiles')
