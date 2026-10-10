#!/usr/bin/env python3
"""Independent rational replay. No import of the C++ or Python search.
Rebuilds all six corner candidates by the cosine rule, local residual rays,
and every external-side candidate in a finite boundary-path relaxation.
The only non-elementary project input is the proved blocked-c boundary lemma.
"""
from fractions import Fraction as Q
from collections import Counter
from functools import lru_cache
from itertools import permutations
from math import isqrt,gcd
from pathlib import Path
import json,sys,time
class Invalid(ValueError): pass
def need(c,s):
 if not c:raise Invalid(s)
def point(p):return tuple(Q(x) for x in p)
def add(p,q):return p[0]+q[0],p[1]+q[1]
def sub(p,q):return p[0]-q[0],p[1]-q[1]
def mul(k,p):return k*p[0],k*p[1]
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def ori(p,q,r):return det(sub(q,p),sub(r,p))
def edges(t):return tuple(zip(t,t[1:]+t[:1]))
def norm(p,D):return p[0]**2+D*p[1]**2
def rt(q):
 need(q>=0,'negative square');a,b=isqrt(q.numerator),isqrt(q.denominator)
 need(a*a==q.numerator and b*b==q.denominator,'nonrational required square root');return Q(a,b)
def ccw(t):
 t=tuple(t);d=ori(*t);need(d!=0,'zero area')
 if d<0:t=(t[0],t[2],t[1])
 i=min(range(3),key=lambda i:t[i]);return t[i:]+t[:i]
def inside(t,p):return all(ori(a,b,p)>=0 for a,b in edges(t))
def bounds(t):return min(p[0] for p in t),max(p[0] for p in t),min(p[1] for p in t),max(p[1] for p in t)
def intersects_box(x,y):return x[1]>y[0] and y[1]>x[0] and x[3]>y[2] and y[3]>x[2]
def separated(t,s):
 return any(all(ori(a,b,p)<=0 for p in other) for one,other in ((t,s),(s,t)) for a,b in edges(one))
def direction(d):
 den=d[0].denominator*d[1].denominator//gcd(d[0].denominator,d[1].denominator)
 x,y=int(d[0]*den),int(d[1]*den);g=gcd(x,y);need(g!=0,'zero ray');return x//g,y//g

def check_sector(target,placed,row):
 p,d,e=point(row['x']),point(row['d']),point(row['e']);need(det(d,e)>0,'not convex')
 rays=Counter()
 # Reconstruct only the local residual germ, independently of the generator's global boundary.
 for T,sg in [(target,1)]+[(t,-1) for t in placed]:
  for a,b in edges(T):
   if min(a,b)<=p<=max(a,b) and ori(a,b,p)==0:
    if b!=p:rays[direction(sub(b,p))]+=sg
    if a!=p:rays[direction(sub(a,p))]-=sg
 need(all(abs(n)<=1 for n in rays.values()),'local multiplicity')
 need(rays[direction(d)]==1 and rays[direction(e)]==-1,'not residual boundary rays')
 need(not any(n and det(d,r)>0 and det(r,e)>0 for r,n in rays.items()),'unaccounted interior ray')
 return p,d,e

class Replay:
 def __init__(self,data,root_kind,root_id):
  self.d=data;self.u=data['u'];self.v=data['v'];self.m=data['m'];self.fam=data['branch'];self.D=data['D'];self.N=data['N']
  u,v,m=self.u,self.v,self.m
  need(m>0 and (0<u<v and gcd(u,v)==1 and self.fam in ('W','beta') or u>0 and v>0 and self.fam=='E120'),'parameters')
  self.sides=(u,v,isqrt(u*u+u*v+v*v)) if self.fam=='E120' else (u*v,v*v-u*u,v*v);a,b,c=self.sides
  if self.fam=='E120':need(c*c==a*a+a*b+b*b and gcd(a,b)==1 and a!=b and self.D==3,'invalid 120-degree tile')
  need(self.D>0,'wrong quadratic field')
  self.target=ccw(tuple(map(point,data['target'])))
  expected=([m*v**3,m*u*(2*v*v-u*u),m*v*b] if self.fam=='W' else [m*v**3,m*v**3,m*u*(3*v*v-u*u)])
  if self.fam=='E120':expected=[a*b*m]*3
  need(sorted(norm(sub(q,p),self.D) for p,q in edges(self.target))==sorted(k*k for k in expected),'target sides')
  N=(2*v*v-u*u if self.fam=='W' else 3*v*v-u*u)*m*m
  if self.fam=='E120':N=a*b*m*m
  need(self.N==N,'N')
  need(4*self.D*ori(*self.target)**2==N*N*(a+b+c)*(-a+b+c)*(a-b+c)*(a+b-c),'target area')
  self.basic=[]
  for s,r,t in permutations(self.sides):
   proj=Q(s*s+r*r-t*t,2*s);ht=rt(Q(r*r-proj*proj,self.D))
   self.basic.append((s,r,t,proj,ht))
  self.pc={};self.bcs=[];self.steps=[];self.extlen=[];self.sidekeys=[]
  for side,(x,y) in enumerate(edges(self.target)):
   n=rt(norm(sub(y,x),self.D));need(n.denominator==1,'nonintegral target edge');L=int(n);self.extlen.append(L)
   steps=[[] for _ in range(L+1)];axis=mul(1/n,sub(y,x));perp=(-self.D*axis[1],axis[0])
   for pos in range(L):
    at=add(x,mul(pos,axis))
    for s,r,t,proj,ht in self.basic:
     end=pos+s
     if end>L:continue
     if pos==0 and not self.angleok(side,t):continue
     if end==L and not self.angleok((side+1)%3,r):continue
     other=add(mul(proj,axis),mul(ht,perp));tri=ccw((at,add(at,mul(s,axis)),add(at,other)))
     if not all(inside(self.target,p) for p in tri):continue
     k=len(self.bcs);self.bcs.append((tri,bounds(tri),side,pos,end,s==c,t==c,r==c));steps[pos].append(k)
   self.steps.append(steps)
  self.ban=[0]*len(self.bcs);self.conflict={};self.placed=[];self.boxes=[];self.undos=[]
  self.root_kind=root_kind;self.root_id=root_id;self.roots=[] if root_kind in ('control','empty') else self.make_roots(root_kind,root_id)
  for t in self.roots:self.push(t)
  self.visited=set();self.stats=Counter();self.start=time.monotonic()
 def angleok(self,j,opposite):
  if self.fam=='E120':return opposite in self.sides[:2]
  op=rt(norm(sub(self.target[(j+1)%3],self.target[(j+2)%3]),self.D));u,v,m=self.u,self.v,self.m;a,b,c=self.sides
  if self.fam=='W':
   if op==m*v*b:return opposite==b
   if op==m*u*(2*v*v-u*u):return opposite==a
   return opposite in (a,b)
  return opposite==a if op==m*u*(3*v*v-u*u) else opposite==b
 def tri_on(self,at,axis,s,r,opp):
  proj=Q(s*s+r*r-opp*opp,2*s);h=rt(Q(r*r-proj*proj,self.D));perp=(-self.D*axis[1],axis[0]);other=add(mul(proj,axis),mul(h,perp))
  return ccw((at,add(at,mul(s,axis)),add(at,other))),mul(Q(1,r),other)
 def make_roots(self,kind,k):
  a,b,c=self.sides
  if kind=='W_short':
   need(self.fam=='W' and k in (0,1),'root kind')
   # Identify the 2-alpha corner using its opposite side, not a stored picture.
   for j,p in enumerate(self.target):
    opposite=rt(norm(sub(self.target[(j+1)%3],self.target[(j+2)%3]),self.D))
    if opposite==56:C=p
    if opposite==54:A=p
   axis=mul(Q(1,30),sub(A,C));pos=0;roots=[]
   for s,r,op in [(c,b,a),(c,b,a) if k==0 else (c,a,b),(a,b,c),(a,b,c)]:
    at=add(C,mul(pos,axis));t,_=self.tri_on(at,axis,s,r,op);roots.append(t);pos+=s
   need(pos==30,'word length');return roots
  need(kind=='beta_apex' and self.fam=='beta' and 0<=k<8,'beta root kind')
  for j in range(3):
   if rt(norm(sub(self.target[(j+1)%3],self.target[(j+2)%3]),self.D))==92:apex=j
  at=self.target[apex];d=sub(self.target[(apex+1)%3],at);axis=mul(1/rt(norm(d,self.D)),d);roots=[]
  for i in range(3):
   s=c if k>>i&1 else b;r=b if s==c else c;t,axis=self.tri_on(at,axis,s,r,a);roots.append(t)
  d=sub(self.target[(apex+2)%3],at);need(det(axis,d)==0 and axis[0]*d[0]+axis[1]*d[1]>0,'apex fan does not close');return roots
 def compatible(self,t,bb=None):
  bb=bounds(t) if bb is None else bb
  return all(not intersects_box(bb,b) or separated(t,z) for z,b in zip(self.placed,self.boxes))
 def push(self,t):
  need(sorted(norm(sub(p,q),self.D) for p,q in edges(t))==sorted(s*s for s in self.sides),'tile metric')
  need(all(inside(self.target,p) for p in t),'tile outside');bb=bounds(t);need(self.compatible(t,bb),'overlap')
  self.placed.append(t);self.boxes.append(bb)
  if t not in self.conflict:
   self.conflict[t]=[k for k,(tri,b,*_) in enumerate(self.bcs) if tri!=t and intersects_box(bb,b) and not separated(t,tri)]
  bad=self.conflict[t];self.undos.append(bad)
  for k in bad:self.ban[k]+=1
 def pop(self):
  for k in self.undos.pop():self.ban[k]-=1
  self.placed.pop();self.boxes.pop()
 def possible(self,s):
  p,d,e=s;key=(p,direction(d))
  if key not in self.pc:
   axis=mul(1/rt(norm(d,self.D)),d);perp=(-self.D*axis[1],axis[0]);out=[]
   for si,r,op,proj,ht in self.basic:
    v=add(mul(proj,axis),mul(ht,perp));t=ccw((p,add(p,mul(si,axis)),add(p,v)))
    if all(inside(self.target,x) for x in t):out.append((v,t,bounds(t)))
   self.pc[key]=out
  return {t for v,t,b in self.pc[key] if det(v,e)>=0 and self.compatible(t,b)}
 def boundary_possible(self):
  for e,L in enumerate(self.extlen):
   # State stores (previous c-start blocked or None, previous gamma endpoint, seen cc).
   reachable=[set() for _ in range(L+1)];reachable[0].add((None,False,False))
   for pos in range(L):
    for k in self.steps[e][pos]:
     if self.ban[k]:continue
     tri,bb,side,start,end,is_c,start_g,end_g=self.bcs[k]
     for blocked,prev_g,cc in reachable[pos]:
      if prev_g and start_g:continue
      if blocked is True and start_g:continue
      newblocked=(pos==0 or prev_g) if is_c else None
      reachable[end].add((newblocked,end_g,cc or(is_c and blocked is not None)))
   if not any(cc and blocked is not True for blocked,g,cc in reachable[L]):return False
  return True
 def walk(self,k):
  rows=self.d['proof'];need(isinstance(k,int) and 0<=k<len(rows),'bad index');need(k not in self.visited,'cycle or repeated proof node')
  self.visited.add(k);row=rows[k];self.stats['nodes']+=1;self.stats['maximum_depth']=max(self.stats['maximum_depth'],len(self.placed));need(len(self.placed)<self.N,'full placement in refutation')
  reason=row['reason'];kids=row['children']
  if reason=='boundary':
   need(not kids,'boundary leaf has children');need(not self.boundary_possible(),'boundary refutation is not justified');self.stats['boundary_leaves']+=1;return
  need(reason in ('branch','no_corner_tile'),'unsupported pruning')
  s=check_sector(self.target,self.placed,row);poss=self.possible(s);advert=[ccw(tuple(map(point,x[0]))) for x in kids]
  need(len(advert)==len(set(advert)) and set(advert)==poss,'missing or extra geometric branch')
  if not kids:self.stats['corner_leaves']+=1
  for t,(_,n) in zip(advert,kids):self.push(t);self.walk(n);self.pop()
  if len(self.visited)%1000==0:print('replayed',len(self.visited),'elapsed',round(time.monotonic()-self.start,2),flush=True)
 def run(self):
  need(self.d['status']=='EXHAUSTED','not a complete proof');self.walk(self.d['proof_root']);need(len(self.visited)==len(self.d['proof']),'unreachable records')
  return {'status':'PASS','family':self.fam,'u':self.u,'v':self.v,'m':self.m,'N':self.N,'root_kind':self.root_kind,'root_id':self.root_id,'boundary_candidates':len(self.bcs),**dict(self.stats),'seconds':time.monotonic()-self.start,'whole_problem_solved':False,'direction_bound':None,'uses_reverse_apex':False,'independent_implementation':'Python fractions vs C++ GMP'}
if __name__=='__main__':
 p=Path(sys.argv[1]);kind=sys.argv[2];ix=int(sys.argv[3]);d=json.loads(p.read_text());rep=Replay(d,kind,ix).run();print(json.dumps(rep),flush=True);p.with_suffix('.verified.json').write_text(json.dumps(rep,indent=2)+'\n')
