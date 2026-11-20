"""Exact permitted boundary placements from the fractional jumps in slice width."""
from math import lcm
from collections import defaultdict
from fractions import Fraction as F
from itertools import permutations
from math import lcm
def y(a, b, p):
    return (a + b) * p[0] + b * p[1]

def mul(p, q):
    x, y = p
    u, v = q
    return (x*u-y*v, x*v+y*u+y*v)

def jumps(levels, abc, mass):
    return {t: F(mass*abc**2, (levels[(i+1) % 3]-t)*(levels[(i+2) % 3]-t))
            for i,t in enumerate(levels)}

def produce(a,b,c):
 w=a+b;out=[];ls=[b*(2*a+b),c*c,a*(a+2*b)];N=(a+2*b)*(2*a+b)
 z=(F(a,c),F(b,c));dirs=[(1,0),mul((0,1),mul(z,z)),(0,-1)]
 shift=[0,w*ls[0],b*ls[2]]; demand={t:v%1 for t,v in jumps(shift,a*b*c,N).items()}
 records=[];tm=[];types=list(permutations([a,b,c]));events=defaultdict(list);by=defaultdict(list);den=1
 for e in range(3):
  d=dirs[e];stride=y(a,b,d);ts=[]
  for k,(L,S,T) in enumerate(types):
   dx=F(L*L+S*S-T*T-a*b,2*L);dy=F(a*b,L);Y=[0,y(a,b,mul(d,(L,0))),y(a,b,mul(d,(dx,dy)))]
   if len(set(Y))==3: vals={t:n%1 for t,n in jumps(Y,a*b*c,1).items() if n%1}
   else:vals={}
   for v in vals.values():den=lcm(den,v.denominator)
   ts.append((vals,Y))
   for x in range(0,ls[e]-L+1):
    t0=shift[e]+stride*x
    if not all(0<=t0+ty<=shift[1] for ty in Y):continue
    Id=len(records);records.append((e,k,x,x+L));by[e,x].append(Id)
    for ty,v in vals.items():events[t0+ty].append((Id,v))
  tm.append(ts)
 for d in demand.values():den=lcm(den,d.denominator)
 evt=[(t,[(i,int(v*den)) for i,v in rr],int(demand.get(t,0)*den)) for t,rr in events.items()]
 return ls,types,records,by,den,evt
def solve(a,b,c):
 ls,T,rec,by,D,E=produce(a,b,c);live=set(range(len(rec)));deadA=[]
 def trim():
  for e,L in enumerate(ls):
   left={0};right={L}
   for x in range(L):
    if x in left:left.update(rec[i][3] for i in by[e,x] if i in live)
   for x in reversed(range(L)):
    if any(i in live and rec[i][3] in right for i in by[e,x]):right.add(x)
   if L not in left:raise ValueError('empty boundary')
   live.difference_update(j for j,(u,k,x,z) in enumerate(rec) if u==e and not(x in left and z in right))
 def models(items):
  # Disjoint intervals along a side, all subsets allowed.
  out={0:(0,0)}
  stack=[(0,-1,0,0)]
  while stack:
   k,end,s,m=stack.pop()
   if k==len(items):
    old=out.get(s)
    out[s]=(m if old is None else old[0]|m,m if old is None else old[1]&m)
    continue
   x,z,v,ind=items[k]
   stack.append((k+1,end,s,m))
   if x>=end:stack.append((k+1,z,(s+v)%D,m|(1<<ind)))
  return out
 def sat(items,target):
  bys=[[],[],[]]
  for j,(i,v) in enumerate(items):
   e,k,x,z=rec[i];bys[e].append((x,z,v,j))
  M=sorted((models(sorted(b)) for b in bys),key=len)
  uni=0;inter=None
  for s,(u,it) in M[0].items():
   for v,(a,b) in M[1].items():
    vals=M[2].get((target-s-v)%D)
    if vals is not None:
     uu,ii=vals;uni|=u|a|uu
     st=it|b|ii;inter=st if inter is None else inter&st
  if inter is None:raise ValueError('unsatisfied impulse')
  return ([i for j,(i,v) in enumerate(items) if not (uni>>j)&1],[i for j,(i,v) in enumerate(items) if (inter>>j)&1])
 for r in range(100):
  n=len(live);trim();todo=set()
  for t,rr,tar in E:
   inp=[(i,v) for i,v in rr if i in live]
   if not tar and not inp:continue
   bad,forced=sat(inp,tar);live.difference_update(bad);todo.update(forced)
  for i in todo:
   e,k,x,z=rec[i]
   for xx in range(max(x-c+1,0),z):
    live.difference_update(v for v in by[e,xx] if v!=i and rec[v][3]>x)
  print('round',a,r,n,len(live),len(todo),flush=True)
  if len(live)==n:break
 print('inventory',[[sum(1 for i in live if rec[i][:2]==(e,k)) for k in range(6)] for e in range(3)],flush=True)
 expected=[[False,True,True,False,True,False],
           [True,False,False,True,False,True],
           [False,True,True,False,True,False]]
 obtained=[[any(rec[i][:2]==(e,k) for i in live) for k in range(6)] for e in range(3)]
 assert obtained==expected

 return live
if __name__=='__main__':
 for abc in [(33,7,37),(35,13,43)]:
  solve(*abc)
