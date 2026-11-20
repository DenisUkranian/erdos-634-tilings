"""Independent phase-node check using exact Eisenstein prime division, not Hensel roots."""
from pathlib import Path
from random import Random
import sys
HERE = Path(__file__).resolve().parent
BASE = HERE.parent/'global-endpoints'/'integer'
sys.path[:0] = [str(BASE), str(HERE)]
from global_core_sat import Geometry
from phase_budget import PhaseBudget

def mul(p,q):return(p[0]*q[0]-p[1]*q[1],p[1]*q[0]+p[0]*q[1]+p[1]*q[1])
def conj(p):return(p[0]+p[1],-p[1])
def vp(point,prime,c):
 x,y,e=point
 if not x and not y:return 10**9
 v=-e
 while True:
  u,w=mul((x,y),conj(prime))
  if u%c or w%c:return v
  x,y=u//c,w//c;v+=1

def main():
 rng=Random(230731)
 total=0
 for abc,positive in [((5,3,7),(3,-1)),((33,7,37),(7,-3)),((35,13,43),(6,1))]:
  g=Geometry(*abc)
  for sign in (1,-1):
   prime=positive if sign==1 else conj(positive);pb=PhaseBudget(g,sign)
   assert vp((g.a,g.b,1),prime,g.c)==sign
   for repeat in range(700):
    p=g.point(rng.randrange(-10000,10001),rng.randrange(-10000,10001),rng.randrange(7))
    q=g.point(rng.randrange(-10000,10001),rng.randrange(-10000,10001),rng.randrange(7))
    if repeat%2==0:
     h=rng.randrange(-8,9)
     q=g.add(p,g.scale(rng.randrange(1,100),g.unit(sign*h,rng.randrange(6))))
    d=g.sub(p,q)
    for level in range(-9,10):
     assert (pb.node(p,level)==pb.node(q,level))==(vp(d,prime,g.c)>=level)
     total+=1
    eextra=rng.randrange(1,5); pp=(p[0]*g.c**eextra,p[1]*g.c**eextra,p[2]+eextra)
    for level in range(-5,6):assert pb.node(p,level)==pb.node(pp,level)
    h=rng.randrange(-7,8);tile=(p,h,rng.randrange(6),rng.choice((-1,1)))
    height=sign*h;got=set(pb.required(tile));expected=set()
    start=min(1-p[2],1+min(sign*k for _,_,k,_ in g.walls()))
    for level in range(min(start-12,height-12),height+1):
     free=all(level>sign*k or vp(g.sub(p,w),prime,g.c)<level for w,_,k,_ in g.walls())
     if free:expected.add(pb.node(p,level))
     if level<start:assert not free
    assert got==expected
   print('PASS',abc,'sign',sign,'prime',prime,'canonical nodes, representation invariance, and exterior-free ancestors')
 print('PASS independent valuation comparisons:',total)
if __name__=='__main__':main()
