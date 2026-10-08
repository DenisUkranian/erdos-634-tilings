#!/usr/bin/env python3
"""Exact positive search on a finite corner-generated macro-placement pool."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
from math import isqrt,gcd,lcm
import sys,json,time,argparse,os
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root.parents[1]/'f3-primitive-oct7'))
from macro_search import Search,E
parser=argparse.ArgumentParser();parser.add_argument('--generation',type=float,default=120);parser.add_argument('--seconds',type=float,default=120);parser.add_argument('--depth',type=int,default=2);args=parser.parse_args()
S=Search(24,11,31,seconds=args.generation);conv=lambda p:(F(p[0])+F(p[1],2),F(p[1],2))
S.target=tuple(map(conv,[(0,0),(649,0),(264,264),(0,143)]));S.n=792
pool={};first=[]
start=time.monotonic()
for sec in E.convex_sectors(E.atomic_boundary(S.target,()),3):
 for k in range(28,0,-1):
  for t in E.placements(S.templates[k],sec,S.target,(),3):pool[t]=k;first.append((t,k))
# A finite heuristic pool, not an exhaustive search over all dissections.
stop=False;expanded=0;deep=1;front=[((t,),(k,)) for t,k in first]
while deep<args.depth and front:
 nxt=[]
 for placed,scales in front:
  if time.monotonic()-start>=args.generation:stop=True;break
  try:secs=E.convex_sectors(E.atomic_boundary(S.target,placed),3)
  except ArithmeticError:continue
  kmax=isqrt(792-sum(k*k for k in scales))
  for sec in secs:
   for k in range(kmax,0,-1):
    for t in E.placements(S.templates[k],sec,S.target,placed,3):
     if t not in pool:
      pool[t]=k
      if args.depth>2:nxt.append((placed+(t,),scales+(k,)))
  expanded+=1
 deep+=1
 if stop:break
 front=nxt
print('pool',len(pool),'expanded',expanded,'generation_seconds',time.monotonic()-start,flush=True)
# Use the derivative of each collinear boundary current: at every endpoint,
# sum signed starts minus signed ends is prescribed. This is equivalent to
# equality on all atomic intervals and avoids enumerating every cut pair.
def edge_keys(p,q):
 dx,dy=E.sub(q,p);den=lcm(dx.denominator,dy.denominator);u,v=int(dx*den),int(dy*den);g=gcd(u,v);u,v=u//g,v//g
 sign=1
 if (u,v)<(0,0):u,v=-u,-v;sign=-1
 off=u*p[1]-v*p[0]
 return (u,v,off,p),(u,v,off,q),1
rows=defaultdict(dict);rhs=defaultdict(int)
triangles=list(pool)
for j,t in enumerate(triangles):
 for p,q in E.edges(t):
  a,b,sg=edge_keys(p,q)
  rows[a][j]=rows[a].get(j,0)+sg;rows[b][j]=rows[b].get(j,0)-sg
for p,q in E.edges(S.target):
 a,b,sg=edge_keys(p,q);rhs[a]+=sg;rhs[b]-=sg
for k in rhs:rows[k]
sys.path.insert(0,os.environ.get('ERDOS_ORTOOLS_PATH','/tmp/erdos634-ortools'))
from ortools.sat.python import cp_model
model=cp_model.CpModel();x=[model.new_bool_var('') for _ in triangles]
for key,row in rows.items():model.add(cp_model.LinearExpr.weighted_sum([x[j] for j in row],[int(z) for z in row.values()])==rhs[key])
model.add(cp_model.LinearExpr.weighted_sum(x,[pool[t]**2 for t in triangles])==792)
solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=args.seconds;solver.parameters.num_search_workers=1;solver.parameters.linearization_level=0;solver.parameters.symmetry_level=0;solver.parameters.random_seed=4830
status=solver.solve(model)
report={'target':'sufficient Q792','tile':[24,11,31],'pool':len(pool),'rows':len(rows),'generation_depth':args.depth,'expanded_states':expanded,'generation_stopped':stop,'status':solver.status_name(status),'scope':'Finite heuristic macro pool only. No unrestricted nonexistence claim.','seconds':time.monotonic()-start}
if status in(cp_model.OPTIMAL,cp_model.FEASIBLE):
 selected=[j for j,v in enumerate(x) if solver.value(v)]
 # Replay all boundary equations with exact rational keys.
 for key,row in rows.items():assert sum(row.get(j,0) for j in selected)==rhs[key]
 report['macros']=[{'scale':pool[triangles[j]],'vertices':E.encode_tri(triangles[j])} for j in selected]
 report['target']=E.encode_tri(S.target)
(root/f'macro_pool_depth{args.depth}_report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
