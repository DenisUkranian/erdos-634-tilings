from pathlib import Path
from fractions import Fraction as F
root=Path(__file__).resolve().parent

def mul(p,q):
 x,y=p;u,v=q
 return x*u-y*v,x*v+y*u+y*v

def scale(n,p):return n*p[0],n*p[1]
def det(p,q):return p[0]*q[1]-p[1]*q[0]
for a,b,c,eta in [(33,7,37,(7,-4)),(35,13,43,(7,-1)),(5,3,7,(3,-2))]:
 templates=[]
 def unit(h,j):
  p=eta
  for _ in range(h):p=mul(p,(F(a,c),F(b,c)))
  for _ in range(j%6):p=mul(p,(0,1))
  assert all(int(x)==x for x in p)
  return tuple(map(int,p))
 for h in (0,1):
  for j in range(6):
   for sign in (-1,1):
    x,y=scale(a,unit(h,j)),scale(b,unit(h,j+2*sign))
    if det(x,y)<0:x,y=y,x
    templates.append(((0,0),x,y))
 H=b*(2*a+b);V=a*(a+2*b);N=(a+2*b)*(2*a+b)
 shape=[(0,0),scale(H,eta),mul((0,V),eta)]
 def row(pts):return ' '.join(str(v) for p in pts for v in p)
 (root/f'board{N}.in').write_text('\n'.join([f'{len(shape)} 24',row(shape)]+[row(t) for t in templates])+'\n')
 # Standard grid at height zero, 64 tiles.
 shape=[scale(8,p) for p in templates[0]]
 (root/f'control{N}.in').write_text('\n'.join([f'3 24',row(shape)]+[row(t) for t in templates])+'\n')
 print(N,shape)
