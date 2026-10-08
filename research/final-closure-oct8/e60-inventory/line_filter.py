"""Necessary affine-line counts for short edges, with exact chord capacities."""
from functools import lru_cache
from fractions import Fraction as F

def comp(n,k):
 if k==1:yield(n,);return
 for x in range(n+1):
  for q in comp(n-x,k-1):yield(x,)+q

def product(p,q):
 x,y=p;u,v=q
 return(x*u-y*v,x*v+y*u+y*v)
@lru_cache(None)
def cap(h,j):
 z=(F(3,7),F(5,7)) if h>=0 else(F(8,7),F(-5,7));v=(F(1),F(0))
 for _ in range(abs(h)):v=product(v,z)
 for _ in range(j):v=product(v,(0,1))
 x,y=v;vals=(0,-30*y,30*x)
 return int(F(900)/(max(vals)-min(vals)))
atoms=[]
for n in range(1,8):
 for p in comp(n,4):
  if(3*(p[0]-p[1])+5*(p[2]-p[3]))%7:continue
  if any(all(x<=y for x,y in zip(q,p)) for q in atoms):continue
  atoms.append(p)
@lru_cache(None)
def max_lines(total,wanted,cap_floor):
 if not any(total):return 0
 best=-100000
 for p in atoms:
  if not all(x<=y for x,y in zip(p,total)):continue
  if 3*p[0]+5*p[2]>cap_floor or 3*p[1]+5*p[3]>cap_floor:continue
  tail=tuple(y-x for x,y in zip(p,total))
  best=max(best,max_lines(tail,wanted,cap_floor)+(p[wanted]>0))
 return best

def edge(j,length):return(j%3,(0 if length==3 else 2)+(j>=3))
EDGES=[(edge(j,3 if t==0 else 5),edge((j+5)%6,5 if t==0 else 3)) for t in range(2) for j in range(6)]

def actuals(A,B,n):
 inv=[0]*12
 for t,v in enumerate((A,B)):
  for j,w in enumerate(v):inv[6*t+j if w>=0 else 6*t+j+3]=abs(w)
 d=n-sum(inv)
 if d<0 or d%2:return
 for q in comp(d//2,6):
  out=inv.copy()
  for k,w in enumerate(q):out[6*(k//3)+k%3]+=w;out[6*(k//3)+k%3+3]+=w
  yield tuple(out)

def violates(inv,h):
 total=[[0]*4 for _ in range(3)]
 for n,ee in zip(inv,EDGES):
  for j,t in ee:total[j][t]+=n
 for n,ee in zip(inv,EDGES):
  if not n:continue
  limits=[max_lines(tuple(total[j]),t,cap(h,j)) for j,t in ee]
  if min(limits)<0 or n>limits[0]*limits[1]:return True
 return False

BOUNDARY=[(x,y,z) for x in range(11) for y in range(7) for z in range(5) if 3*x+5*y+7*z==30]
def central_violates(inv):
 total=[[0]*4 for _ in range(3)]
 for n,ee in zip(inv,EDGES):
  for j,t in ee:total[j][t]+=n
 choices=[]
 for j in range(3):
  bank=0 if j in (0,2) else 1;opts=[]
  for x,y,z in BOUNDARY:
   g=[0]*4;g[bank]=x;g[bank+2]=y
   if any(a>b for a,b in zip(g,total[j])):continue
   rest=tuple(b-a for a,b in zip(g,total[j]));li=tuple(max_lines(rest,t,30) for t in range(4))
   if min(li)<0:continue
   opts.append((g,li))
  if not opts:return True
  choices.append(opts)
 # Constraints only remove impossible outer-line inventory choices.
 changed=True
 while changed:
  changed=False
  interior=[[max(q[1][t] for q in opts) for t in range(4)] for opts in choices]
  all_lines=[[max(q[1][t]+(q[0][t]>0) for q in opts) for t in range(4)] for opts in choices]
  for n,ee in zip(inv,EDGES):
   if n>all_lines[ee[0][0]][ee[0][1]]*all_lines[ee[1][0]][ee[1][1]]:return True
  for j in range(3):
   capkind=[0]*4
   for n,ee in zip(inv,EDGES):
    for e,o in ((ee[0],ee[1]),(ee[1],ee[0])):
     if e[0]==j:capkind[e[1]]+=min(n,interior[o[0]][o[1]])
   opts=[q for q in choices[j] if all(x<=y for x,y in zip(q[0],capkind))]
   if not opts:return True
   if len(opts)<len(choices[j]):choices[j]=opts;changed=True
 if sum(min(sum(q[0]) for q in opts) for opts in choices)>sum(inv):return True
 return False

@lru_cache(None)
def feasible(h,A,B,n):
 return any(not (central_violates(inv) if h==0 else violates(inv,h)) for inv in actuals(A,B,n))
