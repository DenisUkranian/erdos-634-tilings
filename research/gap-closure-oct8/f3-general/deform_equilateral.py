#!/usr/bin/env python3
"""Try one sufficient 15-region grid topology at a new norm triple."""
from pathlib import Path
from fractions import Fraction as F
from math import gcd
import argparse,json,time
from ortools.sat.python import cp_model

BASE=Path(__file__).resolve().parents[3]
SOURCE=BASE/'research/final-closure-oct8/equilateral240/macro_grid_regions.json'
def mul(p,q):return(p[0]*q[0]-p[1]*q[1],p[0]*q[1]+p[1]*q[0]+p[1]*q[1])
def rot(p):return(-p[1],p[0]+p[1])
def sub(p,q):return(p[0]-q[0],p[1]-q[1])
def cross(p,q):return p[0]*q[1]-p[1]*q[0]
def orient(p):return p if sum(cross(p[i],p[(i+1)%len(p)])for i in range(len(p)))>0 else list(reversed(p))
def direction(old,short,a,b,c):
 for h,base in ((0,(7,0)),(1,(3,5))):
  p=base
  for j in range(6):
   if tuple(short*x for x in p)==tuple(old):
    new=(c,0)if h==0 else(a,b)
    for _ in range(j):new=rot(new)
    return tuple((a if short==3 else b)*x for x in new),[h,j]
   p=rot(p)
 raise ValueError(('direction',old,short))
def inside(p,poly):
 sg=1 if sum(cross(poly[i],poly[(i+1)%len(poly)])for i in range(len(poly)))>0 else -1
 return all(sg*cross(sub(poly[(i+1)%len(poly)],q),sub(p,q))>=0 for i,q in enumerate(poly))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--a',type=int,default=9);ap.add_argument('--b',type=int,default=56);ap.add_argument('--c',type=int,default=61);ap.add_argument('--side',type=int,default=504);ap.add_argument('--seconds',type=float,default=60);ap.add_argument('--output',type=Path,default=Path(__file__).with_name('E504_deformed.json'));ar=ap.parse_args();a,b,c,L=ar.a,ar.b,ar.c,ar.side
 if c*c!=a*a+a*b+b*b:raise ValueError('norm')
 src=json.loads(SOURCE.read_text());rs=src['regions'];ps=sorted(set(tuple(p)for r in rs for p in r['polygon']));ids={p:i for i,p in enumerate(ps)};model=cp_model.CpModel();xy=[(model.new_int_var(0,c*L,f'x{i}'),model.new_int_var(0,c*L,f'y{i}'))for i in range(len(ps))]
 for (x,y),old in zip(xy,ps):
  model.add(x+y<=c*L)
  if old[0]==0:model.add(x==0)
  if old[1]==0:model.add(y==0)
  if sum(old)==420:model.add(x+y==c*L)
 parts=[]
 for ri,r in enumerate(rs):
  u,hu=direction(r['u'],3,a,b,c);v,hv=direction(r['v'],5,a,b,c);verts=[ids[tuple(p)]for p in r['polygon']];grid=r['grid_polygon'];steps=[]
  for k,vi in enumerate(verts):
   vj=verts[(k+1)%len(verts)];delta=sub(grid[(k+1)%len(grid)],grid[k]);gg=gcd(*map(abs,delta));d=(delta[0]//gg,delta[1]//gg);n=model.new_int_var(1,2*L,f'n{ri}_{k}');vec=tuple(d[0]*u[t]+d[1]*v[t]for t in (0,1));steps.append((n,d))
   for t in (0,1):model.add(xy[vj][t]-xy[vi][t]==n*vec[t])
   op=ps[vi];oq=ps[vj];ov=sub(oq,op)
   for oi,p in enumerate(ps):
    if oi in(vi,vj)or cross(ov,sub(p,op))!=0:continue
    if not all(min(op[t],oq[t])<=p[t]<=max(op[t],oq[t])for t in(0,1)):continue
    model.add(vec[0]*(xy[oi][1]-xy[vi][1])-vec[1]*(xy[oi][0]-xy[vi][0])==0)
    t=0 if vec[0] else 1
    if vec[t]>0:model.add(xy[oi][t]>=xy[vi][t]+1);model.add(xy[oi][t]<=xy[vj][t]-1)
    else:model.add(xy[oi][t]<=xy[vi][t]-1);model.add(xy[oi][t]>=xy[vj][t]+1)
  parts.append((u,v,verts,steps))
 solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=ar.seconds;solver.parameters.num_search_workers=4;t=time.time();st=solver.solve(model);report={'status':solver.status_name(st),'seconds':time.time()-t,'tile':[a,b,c],'side':L,'vertices':len(ps),'region_count':len(parts),'scope':'one fixed positive grid-macro topology; infeasibility is not a tiling obstruction'}
 if st in(cp_model.OPTIMAL,cp_model.FEASIBLE):
  alltiles=[];macros=[]
  for u,v,verts,steps in parts:
   poly=[tuple(solver.value(x)for x in xy[i])for i in verts];gp=[(0,0)]
   for n,d in steps[:-1]:gp.append(tuple(gp[-1][t]+solver.value(n)*d[t]for t in(0,1)))
   o=poly[0];ts=[]
   def physical(p):return(o[0]+p[0]*u[0]+p[1]*v[0],o[1]+p[0]*u[1]+p[1]*v[1])
   for i in range(min(p[0]for p in gp)-1,max(p[0]for p in gp)+1):
    for j in range(min(p[1]for p in gp)-1,max(p[1]for p in gp)+1):
     for tri in [[(i,j),(i+1,j),(i,j+1)],[(i+1,j),(i+1,j+1),(i,j+1)]]:
      cent=tuple(F(sum(p[t]for p in tri),3)for t in(0,1))
      if inside(cent,gp):ts.append(orient([physical(p)for p in tri]))
   alltiles.extend(ts);macros.append({'polygon':poly,'grid_polygon':gp,'u':u,'v':v,'count':len(ts)})
  cert={'format':'ERDOS634_INTEGER_EISENSTEIN_TILING_V1','tile':[a,b,c],'count':len(alltiles),'denominator':c,'target':[[0,0],[c*L,0],[0,c*L]],'triangles':alltiles,'macros':macros};ar.output.write_text(json.dumps(cert,separators=(',',':'))+'\n');report['count']=len(alltiles);report['macro_counts']=[r['count']for r in macros]
 ar.output.with_suffix('.report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
