#!/usr/bin/env python3
"""Exact F1 continuation. Integer homogeneous predicates, rational constructions.
No floating-point exclusion. The boundary marking lemma uses only boundary-
supported 120-degree angles, never a merely touching interior tile.
"""
from fractions import Fraction as Q
from math import gcd,lcm,isqrt
from itertools import permutations
from functools import lru_cache
from collections import defaultdict,deque,Counter
from pathlib import Path
import json,time,os,sys

SIDES=(7,8,13); AREA=56; N=105
SEM={7*a+8*b+13*c for a in range(16) for b in range(14) for c in range(9) if 7*a+8*b+13*c<=105}
XY=[]; HOM=[]; POINT_ID={}; TRI=[]; TRI_ID={}; BOX=[]; MARK=[]; CEDGES=[]; BPOS=[]

def point(x,y):
 x,y=Q(x),Q(y);key=(x,y)
 if key in POINT_ID:return POINT_ID[key]
 i=len(XY);POINT_ID[key]=i;XY.append(key);d=lcm(x.denominator,y.denominator)
 HOM.append((x.numerator*(d//x.denominator),y.numerator*(d//y.denominator),d));return i
OUT=(point(0,0),point(56,0),point(-49,105))
@lru_cache(maxsize=500000)
def orient(p,q,r):
 x,y,d=HOM[p];u,v,e=HOM[q];a,b,f=HOM[r]
 return x*(v*f-e*b)-y*(u*f-e*a)+d*(u*b-v*a)
def normalize(x,y):
 g=gcd(x,y)
 if not g:raise ValueError('zero direction')
 return(x//g,y//g)
@lru_cache(maxsize=200000)
def direction(p,q):
 x,y,d=HOM[p];a,b,e=HOM[q];return normalize(a*d-x*e,b*d-y*e)
def norm2(p,q):
 x=XY[p][0]-XY[q][0];y=XY[p][1]-XY[q][1];return x*x+x*y+y*y
@lru_cache(None)
def inside(p):return all(orient(OUT[k],OUT[(k+1)%3],p)>=0 for k in range(3))
@lru_cache(None)
def positions(p):
 x,y=XY[p];out=[]
 if y==0:out.append((0,x))
 if x+y==56:out.append((1,y))
 if 15*x+7*y==0:out.append((2,13*y/15))
 return tuple(out)
@lru_cache(None)
def vertex_ok(p):
 if not inside(p):return False
 return all(s.denominator==1 and s.numerator in SEM and L-s in SEM for k,s in positions(p) for L in ([56,105,91][k],))
def canonical_vertices(t):
 t=tuple(t)
 if orient(*t)<0:t=(t[0],t[2],t[1])
 return min((t,t[1:]+t[:1],t[2:]+t[:2]),key=lambda z:tuple(XY[v] for v in z))
def triangle(t):
 t=canonical_vertices(t)
 if t in TRI_ID:return TRI_ID[t]
 i=len(TRI);TRI_ID[t]=i;TRI.append(t)
 BOX.append((min(XY[p][0] for p in t),max(XY[p][0] for p in t),min(XY[p][1] for p in t),max(XY[p][1] for p in t)))
 mark=[];ce=[];bp=[set(),set(),set()]
 for k,p in enumerate(t):
  q,r=t[(k+1)%3],t[(k+2)%3]
  for j,s in positions(p):bp[j].add(s)
  if norm2(q,r)==169:
   # This support condition is mathematically essential.
   if any(orient(OUT[j],OUT[(j+1)%3],p)==0 and (orient(OUT[j],OUT[(j+1)%3],q)==0 or orient(OUT[j],OUT[(j+1)%3],r)==0) for j in range(3)):mark.append(p)
   if any(orient(OUT[j],OUT[(j+1)%3],q)==0 and orient(OUT[j],OUT[(j+1)%3],r)==0 for j in range(3)):ce.append((q,r))
 MARK.append(tuple(mark));CEDGES.append(tuple(ce));BPOS.append(tuple(tuple(sorted(s)) for s in bp));return i
@lru_cache(maxsize=1000000)
def _overlap(a,b):
 if a==b:return True
 ba,bb=BOX[a],BOX[b]
 if ba[1]<=bb[0] or bb[1]<=ba[0] or ba[3]<=bb[2] or bb[3]<=ba[2]:return False
 for t,u in ((TRI[a],TRI[b]),(TRI[b],TRI[a])):
  for j in range(3):
   if all(orient(t[j],t[(j+1)%3],v)<=0 for v in u):return False
 return True
def overlap(a,b):return _overlap(min(a,b),max(a,b))
@lru_cache(maxsize=400000)
def on_segment(p,q,r):
 if orient(p,q,r):return False
 return all(min(XY[p][k],XY[q][k])<=XY[r][k]<=max(XY[p][k],XY[q][k]) for k in (0,1))

def add_tiles(boundary,new):
 newv={v for t in new for v in TRI[t]};oldv={v for e in boundary for v in e};counts=defaultdict(int)
 def insert(p,q,pool):
  cuts=sorted({p,q}|{v for v in pool if on_segment(p,q,v)},key=lambda v:XY[v],reverse=XY[p]>XY[q])
  for a,b in zip(cuts,cuts[1:]):
   if a<b:counts[a,b]+=1
   else:counts[b,a]-=1
 for p,q in boundary:insert(p,q,newv)
 for t in new:
  vs=TRI[t]
  for j in range(3):insert(vs[(j+1)%3],vs[j],oldv|newv)
 out=[]
 for (p,q),m in counts.items():
  if abs(m)>1:raise ValueError('boundary multiplicity')
  if m:out.append((p,q) if m>0 else(q,p))
 return tuple(sorted(out))
OUT_EDGES=tuple((OUT[k],OUT[(k+1)%3]) for k in range(3))

def product(u,v):return(u[0]*v[0]-u[1]*v[1],u[0]*v[1]+u[1]*v[0]+u[1]*v[1])
def conjugate(v):return(v[0]+v[1],-v[1])
def half(v):return 0 if v[1]>0 or(v[1]==0 and v[0]>0) else 1
def argless(u,v):
 if half(u)!=half(v):return half(u)<half(v)
 return u[0]*v[1]-u[1]*v[0]>0
ANGLES={};u=(1,0);m=0
while True:
 v=u;n=0
 while True:
  if v!=(1,0):ANGLES[v]=(m,n)
  z=normalize(*product(v,(8,7)))
  if not argless(v,z):break
  v=z;n+=1
 z=normalize(*product(u,(7,8)))
 if not argless(u,z):break
 u=z;m+=1

def boundary_info(boundary):
 outgoing=defaultdict(list);incoming=defaultdict(list)
 for p,q in boundary:outgoing[p].append(q);incoming[q].append(p)
 gaps=[]
 for v,qq in outgoing.items():
  if len(qq)==1 and len(incoming[v])==1:
   q,p=qq[0],incoming[v][0];start,end=direction(v,q),direction(v,p)
   relative=normalize(*product(end,conjugate(start)))
   if relative not in ANGLES:return None,('ANGLE',v,relative)
   if orient(p,v,q)>0:gaps.append((v,q,p))
 # Only apply component-area test when all loops are ordinary simple cycles,
 # and no negatively oriented hole is present.
 if all(len(qs)==1 for qs in outgoing.values()) and all(len(ps)==1 for ps in incoming.values()):
  unused=set(outgoing);areas=[]
  while unused:
   s=next(iter(unused));v=s;seq=[]
   while True:
    if v not in unused:raise ValueError('inconsistent cycles')
    unused.remove(v);seq.append(v);v=outgoing[v][0]
    if v==s:break
   area=sum(XY[p][0]*XY[q][1]-XY[p][1]*XY[q][0] for p,q in zip(seq,seq[1:]+seq[:1]));areas.append(area)
  if areas and all(a>0 for a in areas):
   if any((a/AREA).denominator!=1 for a in areas):return None,('COMPONENT_AREA',[str(a/AREA) for a in areas])
 return sorted(gaps,key=lambda g:(XY[g[0]][1],XY[g[0]][0])),None

def elementary_reject(ts):
 marked=set(OUT);ces=[];pos=[{Q(0),Q(56)},{Q(0),Q(105)},{Q(0),Q(91)}]
 for t in ts:
  marked.update(MARK[t]);ces.extend(CEDGES[t])
  for a,b in zip(pos,BPOS[t]):a.update(b)
 for p,q in ces:
  if p in marked and q in marked:return('BOUNDARY_MARKS',p,q)
 for j,s in enumerate(pos):
  a=sorted(s)
  for p,q in zip(a,a[1:]):
   if q-p not in SEM:return('BOUNDARY_GAP',j,str(p),str(q))
 return None

@lru_cache(maxsize=100000)
def candidates(v,d):
 dx,dy=d;z=isqrt(dx*dx+dx*dy+dy*dy)
 if z*z!=dx*dx+dx*dy+dy*dy:raise ValueError('nonrational direction')
 wx,wy=Q(dx,z),Q(dy,z);vx,vy=XY[v];out=[]
 for ell,s,t in permutations(SIDES):
  x=Q(s*s+ell*ell-t*t-AREA,2*ell);y=Q(AREA,ell)
  p=point(vx+ell*wx,vy+ell*wy);q=point(vx+wx*x-wy*y,vy+wx*y+wy*x+wy*y)
  if vertex_ok(p) and vertex_ok(q):
   tri=triangle((v,p,q));cost=(1,0) if t==8 else((0,1) if t==7 else(2,2))
   out.append((tri,direction(v,q),cost))
 return tuple(out)

@lru_cache(maxsize=80000)
def raw_fans(v,start,end,near):
 angle=normalize(*product(end,conjugate(start)))
 if angle not in ANGLES:return()
 m,n=ANGLES[angle];out=set()
 def grow(d,m,n,placed):
  if m==n==0:
   if d!=end:raise ValueError('angle quota inconsistency')
   out.add(tuple(sorted(placed)));return
  for t,nxt,(a,b) in candidates(v,d):
   if a>m or b>n:continue
   if any(overlap(t,u) for u in near):continue
   if any(overlap(t,u) for u in placed):continue
   grow(nxt,m-a,n-b,placed+(t,))
 grow(start,m,n,())
 return tuple(sorted(out))

def fans(gap,ts):
 v,q,p=gap;x,y=XY[v]
 near=tuple(t for t in ts if BOX[t][1]>=x-16 and BOX[t][0]<=x+16 and BOX[t][3]>=y-16 and BOX[t][2]<=y+16)
 fs=raw_fans(v,direction(v,q),direction(v,p),near)
 return [f for f in fs if elementary_reject(tuple(sorted(set(ts)|set(f)))) is None]
@lru_cache(maxsize=600000)
def compatible(f,h):return all(t==u or not overlap(t,u) for t in f for u in h)

def propagate(gaps,ts):
 ds=[fans(g,ts) for g in gaps]
 if any(not d for d in ds):return None,('EMPTY_FAN',gaps[next(i for i,d in enumerate(ds) if not d)])
 near={i:[j for j in range(len(gaps)) if i!=j and abs(XY[gaps[i][0]][0]-XY[gaps[j][0]][0])<=32 and abs(XY[gaps[i][0]][1]-XY[gaps[j][0]][1])<=32] for i in range(len(gaps))}
 while True:
  todo=deque((i,j) for i in near for j in near[i])
  while todo:
   i,j=todo.popleft();out=[f for f in ds[i] if any(compatible(f,h) for h in ds[j])]
   if len(out)<len(ds[i]):
    if not out:return None,('INCOMPATIBLE_FANS',gaps[i],gaps[j])
    ds[i]=out;todo.extend((k,i) for k in near[i] if k!=j)
  binary=[i for i,d in enumerate(ds) if len(d)==2];size=2*len(binary)
  reach=[1<<i for i in range(size)]
  for x,i in enumerate(binary):
   for y in range(x+1,len(binary)):
    j=binary[y]
    if j not in near[i]:continue
    for a in (0,1):
     for b in (0,1):
      if not compatible(ds[i][a],ds[j][b]):
       reach[2*x+a]|=1<<(2*y+1-b)
       reach[2*y+b]|=1<<(2*x+1-a)
  # Exact implication closure. If a choice implies its opposite, it is impossible.
  for k in range(size):
   for i in range(size):
    if (reach[i]>>k)&1:reach[i]|=reach[k]
  forced=[]
  for x,i in enumerate(binary):
   bad0=bool(reach[2*x]&(1<<(2*x+1)));bad1=bool(reach[2*x+1]&(1<<(2*x)))
   if bad0 and bad1:return None,('BINARY_FAN_CYCLE',gaps[i])
   if bad0:forced.append((i,ds[i][1]))
   elif bad1:forced.append((i,ds[i][0]))
  if not forced:return ds,None
  for i,f in forced:ds[i]=[f]

@lru_cache(None)
def base_tile(x,ell,flip):
 s,t=[z for z in SIDES if z!=ell]
 if flip:s,t=t,s
 qx=Q(s*s+ell*ell-t*t-AREA,2*ell);qy=Q(AREA,ell)
 return triangle((point(x,0),point(x+ell,0),point(x+qx,qy)))
def root_key(ts):return tuple(sorted(tuple(XY[p] for p in TRI[t]) for t in ts))
def roots():
 allroots={}
 for word in sorted(set(permutations((7,7,8,8,13,13)))):
  def extend(i,x,ts,flips):
   if i==6:
    state=tuple(sorted(ts));allroots[root_key(state)]=(state,word,flips);return
   ell=word[i]
   for flip in (0,1):
    t=base_tile(x,ell,flip)
    if all(inside(p) for p in TRI[t]) and all(not overlap(t,u) for u in ts):extend(i+1,x+ell,ts+(t,),flips+(flip,))
  extend(0,0,(),())
 return [allroots[k] for k in sorted(allroots)]

class Search:
 def __init__(self,seconds=180,nodes=20000):
  self.start=time.monotonic();self.seconds=seconds;self.cap=nodes;self.deadline=self.start+seconds;self.node_stop=nodes;self.visited=0;self.cert={};self.solution=None;self.depth=Counter()
 def run(self,ts,boundary):
  if ts in self.cert:return False
  if len(ts)==N:self.solution=ts;return True
  if self.visited>=self.node_stop or time.monotonic()>=self.deadline:raise TimeoutError
  self.visited+=1;self.depth[len(ts)]+=1
  if self.visited%100==0:print('nodes',self.visited,'tiles',len(ts),'seconds',round(time.monotonic()-self.start,2),'triangles',len(TRI),flush=True)
  er=elementary_reject(ts)
  if er:self.cert[ts]=('REJECT',er);return False
  gaps,er=boundary_info(boundary)
  if er:self.cert[ts]=('REJECT',er);return False
  ds,er=propagate(gaps,ts)
  if er:self.cert[ts]=('REJECT',er);return False
  if not ds:raise RuntimeError('No usable convex corner; no exclusion inferred')
  forced=set(t for d in ds if len(d)==1 for t in d[0])-set(ts)
  if forced:
   nxt=tuple(sorted(set(ts)|forced));nb=add_tiles(boundary,tuple(sorted(forced)))
   ans=self.run(nxt,nb)
   if not ans:self.cert[ts]=('FORCED',nxt)
   return ans
  top=os.environ.get('BRANCH_POLICY')=='top'
  anchors={(Q(0),Q(0)):0,(Q(globals().get("CURRENT_JOIN",13)),Q(0)):1,(Q(-49),Q(105)):2}
  if os.environ.get('BRANCH_POLICY')=='anchors':
   i=min(range(len(ds)),key=lambda i:(anchors.get(XY[gaps[i][0]],3),len(ds[i]),XY[gaps[i][0]][1],-min(map(len,ds[i]))))
  else:
   i=min(range(len(ds)),key=lambda i:(len(ds[i]),(-1 if top else 1)*XY[gaps[i][0]][1],-min(map(len,ds[i]))))
  order=ds[i]
  if os.environ.get('FAN_ORDER')=='simple':
   order=sorted(order,key=lambda f:(sum(HOM[v][2].bit_length() for t in f for v in TRI[t]),-len(f),f))
  for f in order:
   added=tuple(sorted(set(f)-set(ts)));nxt=tuple(sorted(set(ts)|set(f)))
   if not added:raise ValueError('non-increasing step')
   if self.run(nxt,add_tiles(boundary,added)):return True
  self.cert[ts]=('BRANCH',gaps[i],ds[i]);return False

 def save(self,path,rr,rootdata):
  ordered=sorted(self.cert,key=lambda ts:(len(ts),ts));index={ts:i for i,ts in enumerate(ordered)};records=[]
  for ts in ordered:
   rule=self.cert[ts];r={'tiles':ts,'rule':rule[0]}
   if rule[0]=='REJECT':r['reason']=rule[1]
   elif rule[0]=='FORCED':r['child']=index[rule[1]]
   else:
    r['gap']=rule[1];r['fans']=rule[2];r['children']=[index[tuple(sorted(set(ts)|set(f)))] for f in rule[2]]
   records.append(r)
  data={'format':'f1-integer-predicates-v3','tile':SIDES,'outer':OUT,
        'points':[[str(x),str(y)] for x,y in XY],'triangles':TRI,'nodes':records,
        'root_results':rr,'root_definitions':rootdata,'solution':self.solution,
        'stats':{'visited':self.visited,'certified_nodes':len(self.cert),'seconds':time.monotonic()-self.start,'tile_counts':dict(self.depth)},
        'scope':'Only the declared boundary configurations of (56,91,105) with tile (7,8,13). A timeout is not a refutation.'}
  Path(path).write_text(json.dumps(data,separators=(',',':'))+'\n')

if __name__=='__main__':
 rootlist=roots();retained=[i for i,(s,w,f) in enumerate(rootlist) if elementary_reject(s) is None]
 print('geometry_roots',len(rootlist),'retained',len(retained),flush=True)
 if len(rootlist)!=840 or len(retained)!=120:raise ValueError('Root reconstruction mismatch')
 ids=[int(i) for i in sys.argv[1:]] or [651]
 search=Search(float(os.environ.get('SECONDS_LIMIT','180')),int(os.environ.get('NODE_LIMIT','20000')))
 rr={};defs={}
 for i in ids:
  state,word,flips=rootlist[i];defs[i]={'tiles':state,'word':word,'flips':flips}
  search.deadline=time.monotonic()+search.seconds;search.node_stop=search.visited+search.cap
  try:result=search.run(state,add_tiles(OUT_EDGES,state));rr[i]='TILING' if result else 'REFUTED'
  except TimeoutError:rr[i]='INCOMPLETE'
  print('ROOT',i,rr[i],'nodes',search.visited,'seconds',time.monotonic()-search.start,flush=True)
  checkpoint=os.environ.get('OUTFILE',str(Path(__file__).with_name('continuation_certificate.json')))
  search.save(checkpoint,rr,defs)
  if rr[i]=='TILING':break
 out=os.environ.get('OUTFILE',str(Path(__file__).with_name('continuation_certificate.json')))
 search.save(out,rr,defs)
 print('SAVED',out,'RESULTS',rr,flush=True)
