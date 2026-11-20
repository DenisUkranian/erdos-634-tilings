"""Enumerate the small triangular tail sizes allowed by all corner angles and side lengths."""
from fractions import Fraction as F
from itertools import product
from math import gcd,lcm,isqrt
from functools import reduce
def multiply(p,q):
 x,y=p;u,v=q
 return (x*u-y*v,x*v+y*(u+v))
def shapes(a,b,c):
 # cis(beta)=(a+b*rho)/c and cis(alpha)=rho*conjugate(cis(beta)).
 beta=(F(a,c),F(b,c));alpha=(F(b,c),F(a,c))
 angles={}
 for i,j in product(range(4),repeat=2):
  p=(1,0)
  for v in (alpha,)*i+(beta,)*j:p=multiply(p,v)
  angles[i,j]=p[1] # 2*sin(angle)/sqrt(3)
 data=set()
 for I in product(range(4),repeat=3):
  if sum(I)!=3:continue
  for J in product(range(4),repeat=3):
   if sum(J)!=3:continue
   s=[angles[i,j] for i,j in zip(I,J)]
   if min(s)<=0:continue
   D=lcm(*(F(x).denominator for x in s))
   q=[int(x*D)for x in s];g=reduce(gcd,q);q=[x//g for x in q]
   area=F(q[0]*q[1]*s[2],a*b)
   data.add((tuple(sorted(q)),area))
 return data

def solve(a,b,c):
 data=shapes(a,b,c)
 bound=F(4*c*c*(2*c+2*a+b),3*a*b*b);cap=int(bound)+2
 sums={0}
 maxside=max((max(sides)*isqrt(int(F(cap,area))) for sides,area in data if area<=cap),default=0)
 for n in range(1,maxside+1):
  if any(n-k in sums for k in (a,b,c)):sums.add(n)
 allowed=set();entries=[]
 for q,r in sorted(data):
  for k in range(1,isqrt(int(F(cap,r)))+1):
   ar=k*k*r
   if ar.denominator==1 and all(k*l in sums for l in q):
    allowed.add(int(ar));entries.append((int(ar),tuple(k*l for l in q)))
 pairs=sorted(t for t in allowed if t+2 in allowed)
 print(a,b,c,'angle shapes',len(data),'bound',bound,'areas',sorted(allowed),'pairs',pairs)
 print('shapes at those pairs',sorted((v,q)for v,q in entries if v in pairs or v-2 in pairs))
 return pairs
if __name__=='__main__':
 solve(33,7,37);solve(35,13,43)
