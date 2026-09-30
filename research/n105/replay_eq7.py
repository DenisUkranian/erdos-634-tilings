#!/usr/bin/env python3
"""Separate certificate checker: homogeneous convex clipping, not separating axes.
All arithmetic is exact. Angle fans are enumerated by geometric rotation without
using the search engine's angle-quota recursion. No search-engine import.
"""
from fractions import Fraction as F
from math import gcd,lcm,isqrt
from itertools import permutations
from functools import lru_cache
from collections import defaultdict,deque
from pathlib import Path
import json,sys,time,hashlib

class Checker:
 def __init__(self,data):
  self.data=data;self.xy=[];self.h=[];self.pi={};self.t=[];self.ti={};self.box=[]
  for expected,p in enumerate(data['points']):
   i=self.pt(F(p[0]),F(p[1]))
   if i!=expected:raise ValueError('duplicate certificate point')
  for expected,t in enumerate(data['triangles']):
   k=self.tri(tuple(t))
   if k!=expected:raise ValueError('duplicate certificate triangle')
  self.out=tuple(data['outer'])
  if tuple(self.xy[p] for p in self.out)!=((F(0),F(0)),(F(105),F(0)),(F(0),F(105))):raise ValueError('wrong target')
  if data['tile']!=[7,13,15]:raise ValueError('wrong tile')
  self.sem={7*a+13*b+15*c for a in range(16) for b in range(9) for c in range(8) if 7*a+13*b+15*c<=105}
  self.angles={};u=(1,0)
  # Enumerate counts of short, 60-degree and obtuse angles independently.
  while True:
   v=u
   while True:
    w=v
    while True:
     if w!=(1,0):self.angles[w]=True
     z=self.normdir(self.mult(w,(-8,15)))
     if not self.angle_lt(w,z):break
     w=z
    z=self.normdir(self.mult(v,(0,1)))
    if not self.angle_lt(v,z):break
    v=z
   z=self.normdir(self.mult(u,(8,7)))
   if not self.angle_lt(u,z):break
   u=z

 def pt(self,x,y):
  k=(F(x),F(y))
  if k in self.pi:return self.pi[k]
  i=len(self.xy);self.pi[k]=i;self.xy.append(k);d=lcm(k[0].denominator,k[1].denominator)
  self.h.append((k[0].numerator*(d//k[0].denominator),k[1].numerator*(d//k[1].denominator),d));return i
 @staticmethod
 def hom_orient(p,q,r):
  x,y,d=p;a,b,e=q;u,v,f=r
  return (a*d-x*e)*(v*d-y*f)-(b*d-y*e)*(u*d-x*f)
 @lru_cache(maxsize=700000)
 def det(self,p,q,r):return self.hom_orient(self.h[p],self.h[q],self.h[r])
 @lru_cache(maxsize=100000)
 def dir(self,p,q):
  x,y,d=self.h[p];a,b,e=self.h[q];return self.normdir((a*d-x*e,b*d-y*e))
 @staticmethod
 def normdir(z):
  d=gcd(z[0],z[1])
  if not d:raise ValueError('zero direction')
  return(z[0]//d,z[1]//d)
 @staticmethod
 def mult(u,v):return(u[0]*v[0]-u[1]*v[1],u[0]*v[1]+u[1]*v[0]+u[1]*v[1])
 @staticmethod
 def conj(u):return(u[0]+u[1],-u[1])
 @staticmethod
 def angle_lt(u,v):
  def half(z):return 0 if z[1]>0 or(z[1]==0 and z[0]>0) else 1
  if half(u)!=half(v):return half(u)<half(v)
  return u[0]*v[1]-u[1]*v[0]>0
 def tri(self,t):
  if self.det(*t)<0:t=(t[0],t[2],t[1])
  t=min((t,t[1:]+t[:1],t[2:]+t[:2]),key=lambda t:tuple(self.xy[p] for p in t))
  if t in self.ti:return self.ti[t]
  i=len(self.t);self.ti[t]=i;self.t.append(t);self.box.append(tuple((min(self.xy[p][j] for p in t),max(self.xy[p][j] for p in t)) for j in (0,1)));return i
 @lru_cache(None)
 def sides2(self,t):
  vs=self.t[t];out=[]
  for p,q in zip(vs,vs[1:]+vs[:1]):
   x,y,d=self.h[p];a,b,e=self.h[q];u=a*d-x*e;v=b*d-y*e
   out.append(F(u*u+u*v+v*v,d*d*e*e))
  return tuple(out)
 @lru_cache(None)
 def bpositions(self,p):
  x,y=self.xy[p];z=[]
  if y==0:z.append((0,x))
  if x+y==105:z.append((1,y))
  if x==0:z.append((2,y))
  return tuple(z)
 @lru_cache(None)
 def admissible_point(self,p):
  if any(self.det(self.out[j],self.out[(j+1)%3],p)<0 for j in range(3)):return False
  return all(s.denominator==1 and s in self.sem and [105,105,105][j]-s in self.sem for j,s in self.bpositions(p))
 @lru_cache(None)
 def validate_triangle(self,t):
  if sorted(self.sides2(t))!=[49,169,225]:raise ValueError('noncongruent triangle')
  p,q,r=self.t[t];den=self.h[p][2]**2*self.h[q][2]*self.h[r][2]
  if self.det(p,q,r)!=105*den:raise ValueError('wrong triangle area')
  if not all(self.admissible_point(p) for p in self.t[t]):raise ValueError('invalid point')
 @lru_cache(maxsize=100000)
 def line(self,p,q):
  x,y,d=self.h[p];a,b,e=self.h[q];A=y*e-b*d;B=a*d-x*e;C=x*b-a*y;g=gcd(gcd(A,B),C)
  return(A//g,B//g,C//g)
 @staticmethod
 def normalize_h(z):
  x,y,d=z
  if not d:raise ValueError('infinite clipped point')
  if d<0:x,y,d=-x,-y,-d
  g=gcd(gcd(x,y),d);return(x//g,y//g,d//g)
 @lru_cache(maxsize=900000)
 def intersect(self,i,j):
  if i==j:return True
  a,b=self.box[i],self.box[j]
  if any(a[k][1]<=b[k][0] or b[k][1]<=a[k][0] for k in(0,1)):return False
  poly=[self.h[p] for p in self.t[i]];vs=self.t[j]
  for p,q in zip(vs,vs[1:]+vs[:1]):
   if not poly:return False
   A,B,C=self.line(p,q);res=[]
   for u,v in zip(poly,poly[1:]+poly[:1]):
    du=A*u[0]+B*u[1]+C*u[2];dv=A*v[0]+B*v[1]+C*v[2]
    if du>=0:res.append(u)
    if (du>0 and dv<0) or (du<0 and dv>0):
     res.append(self.normalize_h(tuple(du*v[k]-dv*u[k] for k in range(3))))
   poly=res
  if len(poly)<3:return False
  p=poly[0];q=next((r for r in poly if r!=p),None)
  if q is None:return False
  return any(self.hom_orient(p,q,r)!=0 for r in poly)
 def overlap(self,i,j):return self.intersect(min(i,j),max(i,j))
 def valid_state(self,ts):
  if len(ts)!=len(set(ts)):raise ValueError('duplicate triangle in state')
  for i,t in enumerate(ts):
   self.validate_triangle(t)
   if any(self.overlap(t,u) for u in ts[:i]):raise ValueError('overlapping state')
 @lru_cache(None)
 def marks(self,t):
  ga=[];ce=[];vs=self.t[t]
  for k,v in enumerate(vs):
   p,q=vs[(k+1)%3],vs[(k+2)%3]
   if self.sides2(t)[(k+1)%3]!=225:continue
   # The obtuse angle Gamma must have an actual boundary edge incident to it.
   for j in range(3):
    a,b=self.out[j],self.out[(j+1)%3]
    if self.det(a,b,v)==0 and (self.det(a,b,p)==0 or self.det(a,b,q)==0):ga.append(v)
    if self.det(a,b,p)==self.det(a,b,q)==0:ce.append((p,q))
  return tuple(ga),tuple(ce)
 def elementary(self,ts):
  marked=set(self.out);cedges=[];bp=[{F(0),F(105)},{F(0),F(105)},{F(0),F(105)}]
  for t in ts:
   a,b=self.marks(t);marked.update(a);cedges.extend(b)
   for p in self.t[t]:
    for j,s in self.bpositions(p):bp[j].add(s)
  if any(p in marked and q in marked for p,q in cedges):return True
  for ss in bp:
   s=sorted(ss)
   if any(q-p not in self.sem for p,q in zip(s,s[1:])):return True
  return False
 @lru_cache(maxsize=700000)
 def contains(self,p,q,r):
  if self.det(p,q,r):return False
  return all(min(self.xy[p][k],self.xy[q][k])<=self.xy[r][k]<=max(self.xy[p][k],self.xy[q][k]) for k in(0,1))
 def boundary(self,ts):
  vv=set(self.out);ee=list(zip(self.out,self.out[1:]+self.out[:1]))
  for t in ts:
   vs=self.t[t];vv.update(vs);ee.extend((q,p) for p,q in zip(vs,vs[1:]+vs[:1]))
  cnt=defaultdict(int)
  for p,q in ee:
   pp=sorted((r for r in vv if self.contains(p,q,r)),key=lambda r:self.xy[r],reverse=self.xy[p]>self.xy[q])
   for a,b in zip(pp,pp[1:]):
    key=(a,b) if a<b else(b,a);cnt[key]+=1 if a<b else -1
  out=[]
  for (p,q),k in cnt.items():
   if abs(k)>1:raise ValueError('boundary multiplicity')
   if k:out.append((p,q) if k>0 else(q,p))
  return out
 def gaps(self,ts):
  out=defaultdict(list);inc=defaultdict(list)
  for p,q in self.boundary(ts):out[p].append(q);inc[q].append(p)
  gg=[]
  for v,qq in out.items():
   if len(qq)==1 and len(inc[v])==1:
    q,p=qq[0],inc[v][0];rel=self.normdir(self.mult(self.dir(v,p),self.conj(self.dir(v,q))))
    if rel not in self.angles:return None
    if self.det(p,v,q)>0:gg.append((v,q,p))
  if all(len(z)==1 for z in out.values()) and all(len(z)==1 for z in inc.values()):
   unused=set(out);areas=[]
   while unused:
    start=next(iter(unused));v=start;seq=[]
    while True:
     if v not in unused:raise ValueError('invalid cycles')
     unused.remove(v);seq.append(v);v=out[v][0]
     if v==start:break
    areas.append(sum(self.xy[p][0]*self.xy[q][1]-self.xy[p][1]*self.xy[q][0] for p,q in zip(seq,seq[1:]+seq[:1])))
   if areas and all(a>0 for a in areas) and any((a/105).denominator!=1 for a in areas):return None
  return sorted(gg,key=lambda x:(self.xy[x[0]][1],self.xy[x[0]][0]))
 @lru_cache(maxsize=100000)
 def candidate(self,v,d):
  x,y=d;ss=x*x+x*y+y*y;k=isqrt(ss)
  if k*k!=ss:raise ValueError('irrational direction')
  u=(F(x,k),F(y,k));normal=(-u[0]-2*u[1],2*u[0]+u[1]);a,b=self.xy[v];ans=[]
  for ell,s,t in permutations((7,13,15)):
   proj=F(ell*ell+s*s-t*t,2*ell)
   p=self.pt(a+ell*u[0],b+ell*u[1]);q=self.pt(a+proj*u[0]+F(105,2*ell)*normal[0],b+proj*u[1]+F(105,2*ell)*normal[1])
   if self.admissible_point(p) and self.admissible_point(q):ans.append((self.tri((v,p,q)),self.dir(v,q)))
  return ans
 @lru_cache(maxsize=80000)
 def rawfans(self,v,begin,end,near):
  ans=set()
  def dfs(ray,old):
   if ray==end:ans.add(tuple(sorted(old)));return
   for t,nr in self.candidate(v,ray):
    if ray[0]*nr[1]-ray[1]*nr[0]<=0:raise ValueError('tile fan orientation')
    if nr[0]*end[1]-nr[1]*end[0]<0:continue
    # Necessary residual-sector test; still geometric fan enumeration, not
    # the search program's quota-state recursion.
    if nr!=end and self.normdir(self.mult(end,self.conj(nr))) not in self.angles:continue
    if any(self.overlap(t,u) for u in near) or any(self.overlap(t,u) for u in old):continue
    dfs(nr,old+(t,))
  dfs(begin,());return tuple(sorted(ans))
 def options(self,gap,ts):
  v,q,p=gap;x,y=self.xy[v]
  near=tuple(t for t in ts if self.box[t][0][1]>=x-42 and self.box[t][0][0]<=x+42 and self.box[t][1][1]>=y-42 and self.box[t][1][0]<=y+42)
  return [f for f in self.rawfans(v,self.dir(v,q),self.dir(v,p),near) if not self.elementary(tuple(sorted(set(ts)|set(f))))]
 @lru_cache(maxsize=600000)
 def comp(self,f,h):return all(i==j or not self.overlap(i,j) for i in f for j in h)
 def domains(self,gaps,ts):
  ds=[self.options(g,ts) for g in gaps]
  if any(not d for d in ds):return None
  while True:
   todo=deque((i,j) for i in range(len(ds)) for j in range(len(ds)) if i!=j)
   while todo:
    i,j=todo.popleft();new=[f for f in ds[i] if any(self.comp(f,h) for h in ds[j])]
    if len(new)!=len(ds[i]):
     if not new:return None
     ds[i]=new;todo.extend((k,i) for k in range(len(ds)) if k not in(i,j))
   binary=[i for i,d in enumerate(ds) if len(d)==2];adj=[set() for _ in range(2*len(binary))]
   for x,i in enumerate(binary):
    for y in range(x+1,len(binary)):
     j=binary[y]
     for a in(0,1):
      for b in(0,1):
       if not self.comp(ds[i][a],ds[j][b]):
        adj[2*x+a].add(2*y+1-b);adj[2*y+b].add(2*x+1-a)
   def reachable(start,end):
    seen={start};stack=[start]
    while stack:
     v=stack.pop()
     for w in adj[v]:
      if w==end:return True
      if w not in seen:seen.add(w);stack.append(w)
    return False
   change=[]
   for x,i in enumerate(binary):
    bad0=reachable(2*x,2*x+1);bad1=reachable(2*x+1,2*x)
    if bad0 and bad1:return None
    if bad0:change.append((i,ds[i][1]))
    elif bad1:change.append((i,ds[i][0]))
   if not change:return ds
   for i,f in change:ds[i]=[f]
 def reconstruct_roots(self):
  roots=[]
  def select(v,w,other):
   options=[]
   for t,d in self.candidate(v,self.dir(v,w)):
    vs=self.t[t]
    if w not in vs:continue
    p=next(p for p in vs if p not in(v,w))
    x,y=self.xy[p][0]-self.xy[v][0],self.xy[p][1]-self.xy[v][1]
    if x*x+x*y+y*y==other*other:options.append(t)
   if len(options)!=1:raise ValueError('non-unique boundary triangle')
   return options[0]
  for tail in sorted(set(permutations((7,7,7,7,7,7,7,13,13)))):
   if tail[-1]!=7:continue
   word=(15,15)+tail;tiles=set();x=0
   for ell in word:
    other=7 if ell in(13,15) else 13
    tiles.add(select(self.pt(x,0),self.pt(x+ell,0),other));x+=ell
   for side in(1,2):
    A=self.xy[self.out[side]];B=self.xy[self.out[(side+1)%3]]
    for pos in(0,15):
     v=self.pt(*(A[j]+F(pos,105)*(B[j]-A[j]) for j in(0,1)))
     w=self.pt(*(A[j]+F(pos+15,105)*(B[j]-A[j]) for j in(0,1)))
     tiles.add(select(v,w,7))
   roots.append(tuple(sorted(tiles)))
  raw={}; sides=(7,13,15)
  def extend(x,counts,ts,word,flips):
   if not any(counts):
    if any(word[j]==word[j+1]==15 for j in range(8)):raw[(word,flips)]=tuple(sorted(ts))
    return
   v=self.pt(x,0)
   for t,ray in self.candidate(v,(1,0)):
    vs=self.t[t];w=next((p for p in vs if p!=v and self.xy[p][1]==0),None)
    if w is None:continue
    ell=self.xy[w][0]-x
    if ell not in sides:continue
    ell=int(ell);j=sides.index(ell)
    if not counts[j] or any(self.overlap(t,u) for u in ts):continue
    r=next(p for p in vs if p not in(v,w))
    dx,dy=self.xy[r][0]-x,self.xy[r][1];osq=dx*dx+dx*dy+dy*dy
    others=[a for a in sides if a!=ell];flip=0 if osq==others[0]**2 else 1
    corner=v if x==0 else(w if x+ell==105 else None)
    if corner is not None:
     pp=[p for p in vs if p!=corner];u1,u2=self.xy[pp[0]],self.xy[pp[1]];dx,dy=u1[0]-u2[0],u1[1]-u2[1]
     if dx*dx+dx*dy+dy*dy!=169:continue
    ns=tuple(sorted(ts+(t,)))
    if self.elementary(ns):continue
    cc=list(counts);cc[j]-=1;extend(x+ell,tuple(cc),ns,word+(ell,),flips+(flip,))
  extend(0,(3,3,3),(),(),())
  roots.extend(raw[k] for k in sorted(raw));return roots
 def verify(self):
  sides=(7, 13, 15)
  rows=[]
  for A in range(1,106//sides[0]):
   for B in range(106//sides[1]):
    for C in range(2,106//sides[2]):
     if sides[0]*A+sides[1]*B+sides[2]*C==105:rows.append((A,B,C))
  if set(rows)!=set([(7, 2, 2), (3, 3, 3)]):raise ValueError('arithmetic root coverage mismatch')
  started=time.monotonic();roots=self.reconstruct_roots()
  if len(roots)!=1788:raise ValueError('initial coverage mismatch')
  eligible={i for i,t in enumerate(roots) if not self.elementary(t)}
  if len(eligible)!=1788:raise ValueError('boundary reconstruction mismatch')
  nodes=self.data['nodes'];states=[tuple(sorted(n['tiles'])) for n in nodes];where={s:i for i,s in enumerate(states)}
  if len(where)!=len(states):raise ValueError('duplicate states')
  done=set();entered=[0]
  def check(i):
   if i in done:return
   entered[0]+=1
   if entered[0]%100==0:print('checking',entered[0],'completed',len(done),'seconds',round(time.monotonic()-started,2),flush=True)
   ts=states[i];self.valid_state(ts);n=nodes[i]
   if self.elementary(ts):done.add(i);return
   gaps=self.gaps(ts)
   if gaps is None:done.add(i);return
   ds=self.domains(gaps,ts)
   if ds is None:done.add(i);return
   if n['rule']=='FORCED':
    j=n['child'];child=states[j];forced={t for d in ds if len(d)==1 for t in d[0]}
    if not set(ts)<set(child) or not(set(child)-set(ts))<=forced:raise ValueError('unjustified forced placement')
    check(j)
   elif n['rule']=='BRANCH':
    gap=tuple(n['gap'])
    if gap not in gaps:raise ValueError('invalid branch corner')
    options=set(ds[gaps.index(gap)]);stored=[tuple(sorted(f)) for f in n['fans']]
    if not options<=set(stored) or len(stored)!=len(n['children']):raise ValueError('incomplete branching')
    for f,j in zip(stored,n['children']):
     if f not in options:continue
     if states[j]!=tuple(sorted(set(ts)|set(f))) or len(states[j])<=len(ts):raise ValueError('invalid child')
     check(j)
   else:raise ValueError('unreproduced rejection '+str(n.get('reason')))
   done.add(i)
   if len(done)%200==0:print('replayed',len(done),'seconds',round(time.monotonic()-started,2),flush=True)
  accepted=[];unknown=[]
  for rs,status in self.data['root_results'].items():
   r=int(rs);definition=self.data['root_definitions'][rs]
   if r not in eligible or roots[r]!=tuple(sorted(definition['tiles'])):raise ValueError('wrong root identity')
   if status=='REFUTED':
    if roots[r] not in where:raise ValueError('missing root proof')
    check(where[roots[r]]);accepted.append(r);print('ACCEPT_ROOT',r,flush=True)
   elif status=='INCOMPLETE':unknown.append(r)
   else:raise ValueError('Separate checker needed for existence certificate')
  return {'result':'ACCEPT_DECLARED_REFUTATIONS','certified_root_ids':accepted,'incomplete_root_ids':unknown,'all_1788_roots_excluded':set(accepted)==eligible,'replayed_nodes':len(done),'stored_nodes':len(nodes),'seconds':round(time.monotonic()-started,6),'method':'exact homogeneous polygon clipping; independent geometric fan enumeration','full_problem_solved':False}

if __name__=='__main__':
 source=Path(sys.argv[1]);raw=source.read_bytes();data=json.loads(raw)
 if data.get('format')!='f1-integer-predicates-v3':raise ValueError('wrong certificate format')
 check=Checker(data);report=check.verify();report['certificate_sha256']=hashlib.sha256(raw).hexdigest();report['certificate']=source.name
 output=source.with_name(source.stem+'_replay.json');output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
