#!/usr/bin/env python3
'''Positive search in a fully enumerated three-height placement model.
Negative solver statuses are scoped diagnostics, not global nonexistence.
'''
from pathlib import Path
import sys,os,json,time,argparse
if os.environ.get('ERDOS_ORTOOLS_PATH'):sys.path.insert(0,os.environ['ERDOS_ORTOOLS_PATH'])
from ortools.sat.python import cp_model

def rot(p):return (-p[1],p[0]+p[1])
def template(o):
 h=o//12-1;order=(o%12)//6;r=o%6
 u=(7,0) if h==0 else (3,5) if h==1 else (8,-5)
 v=rot(rot(u));a=5 if order else 3;b=3 if order else 5
 p=(a*u[0],a*u[1]);q=(b*v[0],b*v[1])
 for _ in range(r):p=rot(p);q=rot(q)
 return ((0,0),p,q)

def main():
 p=argparse.ArgumentParser();p.add_argument('prefix');p.add_argument('--seconds',type=int,default=120);p.add_argument('--output',required=True);args=p.parse_args();start=time.monotonic();prefix=Path(args.prefix)
 out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
 prop=json.loads(prefix.with_suffix('.json').read_text())
 if prop['conflict'] or prop['incomplete']:
  prop['scope']='Complete prescribed three-height placement pool; not a global N135 exclusion';out.write_text(json.dumps(prop,indent=2)+'\n');print(json.dumps(prop));return
 model=cp_model.CpModel()
 with open(str(prefix)+'.model.txt') as f:
  nv,nones,center=map(int,next(f).split());variables=[model.new_bool_var('') for _ in range(nv)];places=[]
  for _ in range(nv+nones):places.append(tuple(map(int,next(f).split())))
  nrows=0
  for line in f:
   nums=list(map(int,line.split()));rhs,size=nums[:2];lits=nums[2:]
   if len(lits)!=size:raise AssertionError('row size')
   model.add(cp_model.LinearExpr.weighted_sum([variables[abs(z)-1] for z in lits],[1 if z>0 else -1 for z in lits])==rhs);nrows+=1
 model.add(sum(variables)==135-nones)
 print(json.dumps(dict(stage='model_loaded',variables=nv,rows=nrows,forced_tiles=nones,seconds=time.monotonic()-start)),flush=True)
 solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=args.seconds;solver.parameters.num_search_workers=1;solver.parameters.linearization_level=0;solver.parameters.symmetry_level=0;solver.parameters.random_seed=634;solver.parameters.log_search_progress=True
 status=solver.solve(model);name=solver.status_name(status)
 result=dict(solver_status=name,center=center,variables=nv,rows=nrows,forced_tiles=nones,seconds=time.monotonic()-start,scope='Complete prescribed three-height placement pool; a negative status is not a global N135 exclusion',N135_decided=False)
 if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
  tris=[]
  for idx,x,y,o,h in places:
   if idx<0 or solver.value(variables[idx]):
    t=[(x+u,y+v) for u,v in template(o)]
    if center:t=[(3*a-5*b,5*a+8*b) for a,b in t]
    tris.append(t)
  if len(tris)!=135:raise AssertionError('count')
  den=49 if center else 7;X=45*den
  cert=dict(format='exact_trapezoid_unit_v1',tile=[3,5,7],denominator=den,target=[(0,0),(X,0),(0,X)],triangles=tris,source='CP-SAT full three-height lattice model with explicit135-tile count',direction_band=[center-1,center+1])
  cp=out.with_name(out.stem+'_certificate.json');cp.write_text(json.dumps(cert,separators=(',',':'))+'\n');result['candidate_certificate']=cp.name
 out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
