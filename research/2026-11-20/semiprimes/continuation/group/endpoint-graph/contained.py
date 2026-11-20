"""Exact orientation-free containment and the area spectrum of triangular subregions."""
from short_tails import shapes,multiply
from fractions import Fraction as F
from math import isqrt
from itertools import product
def sub(p,q):return p[0]-q[0],p[1]-q[1]
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def norm(p):x,y=p;return x*x+x*y+y*y
def conj(p):return p[0]+p[1],-p[1]
def scale(u,p):return u*p[0],u*p[1]
def edges(P):return list(zip(P,P[1:]+P[:1]))
def side_length(p):l=isqrt(int(norm(p)));assert l*l==norm(p);return l
def fit(src,board):
 # Barycentric gradients multiplied by det(board). For each orientation their
 # three minima add to the optimal translation/dilation test without any rounding.
 outer=[sub(q,p)for p,q in edges(board)];D=det(outer[0],outer[1]);assert D>0
 for source in (src,[conj(p)for p in src]):
  for d in [sub(q,p)for p,q in edges(source)]:
   for e in outer:
    u=scale(F(1,side_length(d)*side_length(e)),multiply(e,conj(d)))
    zz=[multiply(u,p)for p in source]
    for sign in (-1,1):
     needed=-sum(min(sign*det(axis,p) for p in zz)for axis in outer)
     if needed<=D:return True
 return False
def boundary_pass(src,a,b,c):
 phases={}
 for e in (-1,1):
  v=(1,0)
  for i in range(6):
   z=v
   for j in range(6):
    phases[z]=(i*e,j);z=multiply(z,(0,1))
   v=multiply(v,(F(a,c),F(b,c))if e==1 else(F(a+b,c),F(-b,c)))
 sums=[0,0];w=[[],[]]
 for p,q in edges(src):
  d=sub(q,p);l=side_length(d);h,j=phases[scale(F(1,l),d)]
  sums[0]+=l*(-1)**j;sums[1]+=l*(1 if (j+h)%2==0 else -1)
  for wi,order,idx,f in [(w[0],a,h+j,b),(w[1],b,j,a)]:
   idx%=6;r=l*pow(f*pow(c,-1,order)%order,h,order)*(1 if idx<3 else -1)
   if wi and wi[-1][0]==idx%3:r+=wi.pop()[1]
   if r%order:wi.append((idx%3,r%order))
 return not any(w) and not sums[0]%(a-b-c) and not sums[1]%(a-b+c)
def spectrum(a,b,c):
 board=[(0,0),(b*(2*a+b),0),(0,a*(a+2*b))]
 n=(a+2*b)*(2*a+b);D=det(board[1],board[2]);assert D==n*a*b
 sup=set();inside=[];passed=[]
 for sides,area in shapes(a,b,c):
  for k in range(1,isqrt(int(F(n,area)))+1):
   A,B,C=(x*k for x in sides);size=area*k*k
   if size.denominator!=1:continue
   if max(A,B,C)>max(a*(a+2*b),b*(2*a+b),c*c):continue
   possible={0}
   for j in range(max(A,B,C)+1):
    if j in possible:possible.update(j+t for t in (a,b,c))
   if any(t not in possible for t in (A,B,C)):continue
   # Take the length C side horizontal. det of the two emanating sides is size*a*b.
   y=F(size*a*b,C);x=(F(B*B+C*C-A*A,C)-y)/2
   src=[(0,0),(C,0),(x,y)]
   assert norm(src[2])==B*B and norm(sub(src[2],src[1]))==A*A
   sup.add(int(size))
   if fit(src,board):
    inside.append((int(size),(A,B,C)))
    if boundary_pass(src,a,b,c):passed.append(inside[-1])
 assert (n,tuple(sorted((b*(2*a+b),c*c,a*(a+2*b))))) in inside
 print('board',n,'smallest fitting shapes',sorted(inside)[:3])
 print('arithmetic spectrum',len(sup),'fitting spectrum',len({i for i,q in inside}),'largest proper candidates',sorted((i,q) for i,q in inside if i<n)[-8:])
 print('word and signed spectra',len({i for i,q in passed}),sorted((i,q) for i,q in passed if i<n)[-8:])
if __name__=='__main__':
 spectrum(33,7,37);spectrum(35,13,43)
