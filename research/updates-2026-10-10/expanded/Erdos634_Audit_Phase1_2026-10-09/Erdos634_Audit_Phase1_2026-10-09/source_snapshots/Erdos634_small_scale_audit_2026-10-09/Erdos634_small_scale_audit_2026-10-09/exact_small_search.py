#!/usr/bin/env python3
"""Exact convex-corner exploration; timeout is INCOMPLETE, never impossibility.
All coordinates are rational in metric x²+D y². No assumed direction band.
Written for a small-scale investigation, not a proof assistant.
"""
from fractions import Fraction as F
from collections import defaultdict,Counter
from functools import cmp_to_key,lru_cache
from math import isqrt,gcd
from time import monotonic
import json,argparse,sys,signal
P=lambda x,y:(F(x),F(y))
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def sub(a,b):return (a[0]-b[0],a[1]-b[1])
def smul(a,s):return (a[0]*s,a[1]*s)
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def orient(a,b,c):return cross(sub(b,a),sub(c,a))
def norm(a,D):return a[0]**2+D*a[1]**2
def dot(a,b,D):return a[0]*b[0]+D*a[1]*b[1]
def cmul(a,b,D):return (a[0]*b[0]-D*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def conj(a):return (a[0],-a[1])
@lru_cache(None)
def sqrtr(x):
 p,q=isqrt(x.numerator),isqrt(x.denominator)
 if p*p!=x.numerator or q*q!=x.denominator: raise ValueError(('nonrational length',x))
 return F(p,q)
def edges(t):return tuple(zip(t,t[1:]+t[:1]))
def ccw(t):
 t=tuple(t)
 if orient(*t)==0:raise ValueError('degenerate tile')
 if orient(*t)<0:t=(t[0],t[2],t[1])
 k=min(range(3),key=lambda i:t[i]);return t[k:]+t[:k]
def inside(T,p):return all(orient(a,b,p)>=0 for a,b in edges(T))
def overlap(T,U):
 for V,W in ((T,U),(U,T)):
  for a,b in edges(V):
   if all(orient(a,b,p)<=0 for p in W):return False
 return True

def bbox(t):return (min(p[0] for p in t),max(p[0] for p in t),min(p[1] for p in t),max(p[1] for p in t))
def bboverlap(x,y):return not(x[1]<=y[0] or y[1]<=x[0] or x[3]<=y[2] or y[3]<=x[2])
def onseg(a,b,p):return min(a,b)<=p<=max(a,b) and orient(a,b,p)==0

def linekey(a,b):
 dx,dy=sub(b,a)
 if dx==0:return ('v',a[0])
 r=dy/dx;return ('s',r,a[1]-r*a[0])

def boundary_add(B,t):
 # B retains interval endpoints; collinear cancellation is exact.
 lines=defaultdict(list)
 for a,b in B:lines[linekey(a,b)].append((a,b))
 for a,b in edges(t):lines[linekey(a,b)].append((b,a))
 out=[]
 for segs in lines.values():
  ev=Counter()
  for a,b in segs:
   lo,hi=sorted((a,b));sign=1 if a==lo else -1;ev[lo]+=sign;ev[hi]-=sign
  at=0;prev=None
  for p in sorted(ev):
   if prev is not None and at:
    if abs(at)!=1:raise ValueError('invalid multiplicity')
    out.append((prev,p) if at==1 else (p,prev))
   at+=ev[p];prev=p
  if at:raise ValueError('nonclosed event line')
 # Merge collinear adjacent intervals, except preserve junction vertices of other lines.
 vv=set(p for e in out for p in e)
 split=[]
 for a,b in out:
  pts=sorted((p for p in vv if onseg(a,b,p)),reverse=a>b)
  split.extend(zip(pts,pts[1:]))
 return tuple(sorted(set(split)))

def polcmp(a,b):
 a,b=a[0],b[0]
 ha=0 if a[1]>0 or(a[1]==0 and a[0]>=0) else 1
 hb=0 if b[1]>0 or(b[1]==0 and b[0]>=0) else 1
 if ha!=hb:return -1 if ha<hb else 1
 d=cross(a,b)
 return -1 if d>0 else 1 if d<0 else 0

def sectors(B,D):
 inc=defaultdict(list)
 for a,b in B:
  inc[a].append((sub(b,a),'out',b));inc[b].append((sub(a,b),'in',a))
 sec=[];nextedge={}
 for x,rs in inc.items():
  rs.sort(key=cmp_to_key(polcmp))
  for j,(d,typ,end) in enumerate(rs):
   if typ!='out':continue
   e,typ2,start=rs[(j+1)%len(rs)]
   if typ2!='in':raise ValueError('nonalternating rays')
   nextedge[(start,x)]=(x,end)
   if cross(d,e)>0:
    # sorting only: acute/narrow sectors first, no decisions use approximate angles
    cosine=dot(d,e,D)/(sqrtr(norm(d,D))*sqrtr(norm(e,D)))
    sec.append((cosine,x,d,e))
 return sorted(sec,reverse=True),nextedge

def encode(t):return [[str(x),str(y)] for x,y in t]

def squarefreepart(D):
 g=1;p=2
 while p*p<=D:
  while D%(p*p)==0:D//=p*p;g*=p
  p+=1
 return D,g

def make_instance(u,v,m,branch):
 a=u*v;b=v*v-u*u;c=v*v;Q=b+c;Pp=b+2*c
 D=4*v*v-u*u;D,root=squarefreepart(D)
 # gamma-based triangle; cos gamma=-u/(2v)
 T=ccw((P(0,0),P(a,0),P(-F(b*u,2*v),F(b*root,2*v))))
 if branch=='W':
  # CCW triangle using canonical z² and z^-2 directions
  tar=ccw((P(0,0),P(-F(v*Q*m,2),-F(u*v*m*root,2)),P(-F(b*Q*m,2*v),F(u*b*m*root,2*v))))
  N=Q*m*m
 else:
  tar=ccw((P(0,0),P(u*Pp*m,0),P(F(u*Pp*m,2),F(b*m*root,2))))
  N=Pp*m*m
 if abs(orient(*tar))!=N*abs(orient(*T)):raise ValueError('area')
 return dict(u=u,v=v,m=m,branch=branch,tile=[a,b,c],target=tar,template=T,D=D,N=N)

class Stop(Exception):pass
class Search:
 def __init__(self,I,seconds=120,maxnodes=1000000,prune=True):
  self.I=I;self.T=I['target'];self.tpl=I['template'];self.D=I['D'];self.N=I['N'];self.limit=seconds;self.maxnodes=maxnodes;self.prune=prune
  self.start=monotonic();self.nodes=0;self.deep=0;self.dead=set();self.found=None;self.prunes=Counter();self.best=[]
  self.st=[(a,b,sub(b,a)) for a,b in edges(self.T)]
  self.tsides=I['tile'];self.semigroup=self.coins(max(int(sqrtr(norm(sub(a,b),self.D))) for a,b in edges(self.T)))
  self.shapes=[]
  for i in range(3):
   for j in range(3):
    if i==j:continue
    k=3-i-j;d=sub(self.tpl[j],self.tpl[i]);e=sub(self.tpl[k],self.tpl[i]);length=sqrtr(norm(d,self.D))
    for flip in (0,1):
     dd=conj(d) if flip else d;ee=conj(e) if flip else e
     # ratio of third ray to the unit outgoing direction
     ratio=smul(cmul(ee,conj(dd),self.D),F(1,length))
     if ratio[1]>0:self.shapes.append((length,ratio))
  self.shapes=sorted(set(self.shapes))
 def coins(self,upto):
  ans=[False]*(upto+1);ans[0]=True
  for i in range(1,upto+1):ans[i]=any(i>=a and ans[i-a] for a in self.tsides)
  return ans
 def checktime(self):
  if monotonic()-self.start>self.limit or self.nodes>=self.maxnodes:raise Stop()
 def placements(self,s,placed,bb):
  _,x,dr,insidev=s
  l=sqrtr(norm(dr,self.D));unit=smul(dr,1/l);res=[]
  for side,ratio in self.shapes:
   q=cmul(unit,ratio,self.D)
   if cross(q,insidev)<0:continue
   cand=ccw((x,add(x,smul(unit,side)),add(x,q)))
   if not all(inside(self.T,p) for p in cand):continue
   cb=bbox(cand)
   if any(bboverlap(cb,b) and overlap(cand,t) for t,b in zip(placed,bb)):continue
   res.append(cand)
  return sorted(set(res))
 def rayblocked(self,x,d,placed):
  for a,b,e in self.st:
   if orient(a,b,x)==0 and cross(e,d)<0:return True
  for t in placed:
   signs=[orient(a,b,x) for a,b in edges(t)]
   if all(s>=0 for s in signs):
    if all(s>0 or cross(sub(b,a),d)>0 for s,(a,b) in zip(signs,edges(t))):return True
  return False
 def lengths_ok(self,B,placed):
  # Maximal chains in boundary supporting lines. We never infer a capped endpoint
  # merely from an angle diagram or from the desired grid.
  lines=defaultdict(list)
  for a,b in B:lines[linekey(a,b)].append((a,b))
  for segs in lines.values():
   sv=sorted((min(a,b),max(a,b),1 if a<b else -1) for a,b in segs)
   merged=[]
   for lo,hi,sg in sv:
    if merged and merged[-1][1]==lo and merged[-1][2]==sg:merged[-1]=(merged[-1][0],hi,sg)
    else:merged.append((lo,hi,sg))
   for a,b,sg in merged:
    d=sub(b,a)
    if not self.rayblocked(a,smul(d,-1),placed):continue
    if not self.rayblocked(b,d,placed):continue
    ll=sqrtr(norm(d,self.D))
    if ll.denominator!=1:return False
    n=int(ll)
    if n<len(self.semigroup) and not self.semigroup[n]:return False
  return True
 def components_ok(self,B,nx):
  unused=set(B);areas=[]
  while unused:
   e=next(iter(unused));cur=e;area=F(0);count=0
   while True:
    if cur not in unused:
     if cur!=e:raise ValueError('cycle clash')
     break
    unused.remove(cur);area+=cross(*cur);cur=nx[cur];count+=1
    if count>len(B):raise ValueError('cycle')
   if area==0:continue
   areas.append(area)
  if any(a<0 for a in areas):return True
  t=abs(orient(*self.tpl))
  return all((a/t).denominator==1 for a in areas)
 def dfs(self,placed,B,bb):
  self.checktime();self.nodes+=1
  if len(placed)>self.deep:self.deep=len(placed);self.best=list(placed)
  if len(placed)==self.N:
   if B:raise ValueError('nonempty final boundary')
   self.found=list(placed);return True
  # A canonical remaining boundary completely determines the residual domain.
  key=B
  if key in self.dead:self.prunes['cached']+=1;return False
  if self.prune and not self.lengths_ok(B,placed):self.prunes['chain']+=1;self.dead.add(key);return False
  ss,nx=sectors(B,self.D)
  if self.prune and not self.components_ok(B,nx):self.prunes['area']+=1;self.dead.add(key);return False
  best=None
  for s in ss:
   ps=self.placements(s,placed,bb)
   if best is None or len(ps)<len(best):best=ps
   if len(ps)<=1:break
  if best is None:raise ValueError('no convex corner')
  if not best:self.prunes['no_corner_tile']+=1
  for t in best:
   NB=boundary_add(B,t)
   if self.dfs(placed+[t],NB,bb+[bbox(t)]):return True
  self.dead.add(key);return False
 def run(self):
  try:r=self.dfs([],tuple(sorted(edges(self.T))),[]);status='TILING_FOUND' if r else 'EXHAUSTED'
  except Stop:status='INCOMPLETE'
  return {'status':status,'u':self.I['u'],'v':self.I['v'],'m':self.I['m'],'branch':self.I['branch'],'N':self.N,
   'nodes':self.nodes,'seconds':round(monotonic()-self.start,3),'maximum_placed':self.deep,'prunes':dict(self.prunes),'tile':self.tsides,'D':self.D,
   'target':encode(self.T),'triangles':[encode(t) for t in self.found] if self.found else None,'last_deepest_partial':[encode(t) for t in self.best],
   'no_direction_bound':True,'scope':'fixed tile and target only; exploratory search, not independently replayed proof'}

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--u',type=int,required=True);ap.add_argument('--v',type=int,required=True);ap.add_argument('--m',type=int,required=True);ap.add_argument('--branch',default='W');ap.add_argument('--seconds',type=float,default=120);ap.add_argument('--max-nodes',type=int,default=1000000);ap.add_argument('--no-prune',action='store_true');ap.add_argument('--out',required=True);a=ap.parse_args()
 I=make_instance(a.u,a.v,a.m,a.branch);s=Search(I,a.seconds,a.max_nodes,not a.no_prune)
 def alarm(*args):raise Stop()
 signal.signal(signal.SIGALRM,alarm);signal.setitimer(signal.ITIMER_REAL,a.seconds)
 r=s.run();signal.setitimer(signal.ITIMER_REAL,0);open(a.out,'w').write(json.dumps(r,indent=2));print(json.dumps({k:v for k,v in r.items() if k not in ('triangles','last_deepest_partial','target')},indent=2))
