"""Lift a verified grid-block topology to another rational 120-degree tile."""
from pathlib import Path
from fractions import Fraction as F
from math import gcd,isqrt
from itertools import product
import sys,json
import sympy as sp
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from verify_macro import read_certificate,det,sub,norm

src=sys.argv[1]; a,b,c=map(int,sys.argv[2:5]);stem=sys.argv[5]
N0,D,blocks=read_certificate(src); a0,b0,c0=5,3,7
N=(a+2*b)*(2*a+b);A=a*(a+2*b);B=b*(2*a+b)
def cmul(p,q):return(p[0]*q[0]-p[1]*q[1],p[1]*q[0]+p[0]*q[1]+p[1]*q[1])
def conj(p):return(p[0]+p[1],-p[1])
def sc(k,p):return(k*p[0],k*p[1])
def add(p,q):return(p[0]+q[0],p[1]+q[1])
def unit(aa,bb,cc,h,j):
 z=(F(aa,cc),F(bb,cc));r=(F(1),F(0))
 for i in range(abs(h)):r=cmul(r,z if h>0 else conj(z))
 for i in range(j%6):r=(-r[1],r[0]+r[1])
 return r
u0={(h,j):unit(a0,b0,c0,h,j)for h in range(-5,6)for j in range(6)}
def transfer(vec,length):
 assert norm(vec)==(length*D)**2
 h,j=next(k for k,v in u0.items()if sc(length*D,v)==vec)
 ll={a0:a,b0:b,c0:c}[length]
 return sc(ll,unit(a,b,c,h,j))
vars=[];exprs=[];sizes=[];sizebounds=[];known={};units=[]
for ib,bl in enumerate(blocks):
 x,y=sp.symbols(f'x{ib} y{ib}');vars += [x,y]
 ps=bl['points'];m=bl['m'];n=bl['n'];k=sp.Symbol(f'k{ib}');vars.append(k);sizes.append(k)
 if bl['kind']=='T':
  us=[]
  for p in ps[1:]:
   v=sub(p,ps[0]);rt=isqrt(norm(v));assert rt*rt==norm(v)and rt%(D*m)==0
   ell=rt//(D*m);us.append(transfer((v[0]//m,v[1]//m),ell))
  u,v=us;local=[(x,y),(x+k*u[0],y+k*u[1]),(x+k*v[0],y+k*v[1])];sizebounds.append(isqrt(N));units.append((u,v))
 else:
  ell=[];us=[]
  for p,dim in [(ps[1],m),(ps[3],n)]:
   v=sub(p,ps[0]);rt=isqrt(norm(v));assert rt*rt==norm(v)and rt%(D*dim)==0
   ll=rt//(D*dim);us.append(transfer((v[0]//dim,v[1]//dim),ll))
  l=sp.Symbol(f'l{ib}');vars.append(l);sizes.append(l);sizebounds.extend([max(A,B)//min(a,b)]*2)
  u,v=us;local=[(x,y),(x+k*u[0],y+k*u[1]),(x+k*u[0]+l*v[0],y+k*u[1]+l*v[1]),(x+l*v[0],y+l*v[1])];units.append((u,v))
 exprs.append(local)
 for p,e in zip(ps,local):known.setdefault(p,[]).append(e)

eq=[]
for p,ex in known.items():
 for e in ex[1:]:eq.extend([e[i]-ex[0][i]for i in (0,1)])
ref={p:v[0]for p,v in known.items()}
for p,target in [((0,0),(0,0)),((D*b0*(2*a0+b0),0),(B,0)),((0,D*a0*(a0+2*b0)),(0,A))]:
 assert p in ref;eq.extend([ref[p][i]-target[i]for i in (0,1)])
ineq=[];touches=0
for ib,bl in enumerate(blocks):
 ps=bl['points'];es=exprs[ib]
 for i,p in enumerate(ps):
  q=ps[(i+1)%len(ps)];e,f=es[i],es[(i+1)%len(ps)];d=sub(q,p)
  # New unit heading of this edge is obtained from its symbolic vector; divide by its size variable.
  if bl['kind']=='T':variable=sp.Symbol(f'k{ib}')
  else:variable=sp.Symbol(f'k{ib}' if i%2==0 else f'l{ib}')
  newd=tuple(sp.simplify((f[z]-e[z])/variable)for z in(0,1))
  # A known touching vertex stays on the edge and between its endpoints.
  for t,g in ref.items():
   if min(p,q)<t<max(p,q)and det(d,sub(t,p))==0:
    eq.append(newd[0]*(g[1]-e[1])-newd[1]*(g[0]-e[0]));touches+=1
    ineq.extend([newd[0]*(g[0]-e[0])+newd[1]*(g[1]-e[1]),newd[0]*(f[0]-g[0])+newd[1]*(f[1]-g[1])])
 for x,y in es:ineq.extend([x,y,A*B-A*x-B*y])
M,rhs=sp.linear_eq_to_matrix(eq,vars); print('vars',len(vars),'equations',M.rows,'rank',M.rank(),'touches',touches,flush=True)
aug=M.row_join(rhs);rref,piv=aug.rref()
if len(vars)in piv:
 print('INCONSISTENT exact linear equations');Path(stem+'.status').write_text('inconsistent\n');raise SystemExit
# Normalize exact equalities to integer rows before numerical MILP; remove zero rows.
rows=[];targets=[]
for i in range(rref.rows):
 row=list(rref.row(i));
 if not any(row):continue
 den=sp.ilcm(*[v.q for v in row]);inte=[int(v*den)for v in row];g=0
 for v in inte:g=gcd(g,v)
 inte=[v//g for v in inte];rows.append(inte[:-1]);targets.append(inte[-1])
Im,Ir=sp.linear_eq_to_matrix(ineq,vars)
Am=np.array(rows,dtype=float);bb=np.array(targets,dtype=float);Ai=np.array(Im,dtype=float);bi=np.array(Ir,dtype=float).reshape(-1)
lo=np.full(len(vars),-np.inf);hi=np.full(len(vars),np.inf);integrality=np.zeros(len(vars));cost=np.zeros(len(vars))
for v,up in zip(sizes,sizebounds):
 j=vars.index(v);lo[j]=1;hi[j]=up;integrality[j]=1;cost[j]=1e-3
for j,v in enumerate(vars):
 if str(v).startswith(('x','y')):lo[j]=0;hi[j]=max(A,B)
print('integer sizes',len(sizes),'constraints',len(rows),len(ineq),flush=True)
res=milp(cost,integrality=integrality,bounds=Bounds(lo,hi),constraints=[LinearConstraint(Am,bb,bb),LinearConstraint(Ai,bi,np.inf)],options={'time_limit':30})
print(res.message,flush=True)
if res.x is None:Path(stem+'.status').write_text(res.message+'\n');raise SystemExit
assignment={v:int(round(res.x[vars.index(v)]))for v in sizes};print('sizes',assignment,flush=True)
solution=sp.linsolve([e.subs(assignment)for e in eq],[v for v in vars if v not in assignment]);tu=next(iter(solution));other=[v for v in vars if v not in assignment]
assert all(not v.free_symbols for v in tu), 'free origins still need rational choice'
assignment.update(zip(other,tu));vertices=[]
for es in exprs:vertices.append([tuple(sp.simplify(v.subs(assignment))for v in e)for e in es])
den=sp.ilcm(*[v.q for ps in vertices for p in ps for v in p]);total=0;out=[]
for ib,(bl,ps)in enumerate(zip(blocks,vertices)):
 m=assignment[sp.Symbol(f'k{ib}')];n=assignment[sp.Symbol(f'l{ib}')]if bl['kind']=='P'else 0;ar=m*m if not n else 2*m*n;total+=ar
 coords=[int(den*v)for p in ps for v in p];out.append(' '.join(map(str,[bl['kind'],m,n,ar,len(ps),*coords])))
print('area',total,'expected',N,'denominator',den,flush=True)
Path(stem+'.out').write_text(f'YES {N} {den} {len(blocks)}\n'+'\n'.join(out)+'\n')
Path(stem+'.status').write_text('candidate needs exact verification\n')
