#!/usr/bin/env python3
"""Build an exact CP-SAT model for a bitmap-surviving E135 placement pool.
A negative solver status is scoped to the supplied band, not global.
"""
import argparse,json,math,os,subprocess,sys,time
from pathlib import Path

def add(a,b):return(a[0]+b[0],a[1]+b[1])
def mul(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]+a[1]*b[1])
def scale(a,n):return(a[0]*n,a[1]*n)
def rot(a):return(-a[1],a[0]+a[1])
def power(a,n):
 r=(1,0)
 for _ in range(n):r=mul(r,a)
 return r

def main():
 p=argparse.ArgumentParser();p.add_argument('prefix',type=Path);p.add_argument('--seconds',type=float,default=120);p.add_argument('--endpoint-executable',default='/tmp/634-endpoint-pool');a=p.parse_args();prefix=str(a.prefix);j=json.loads(Path(prefix+'.json').read_text());L,U=j['L'],j['U'];r=j.get('basis_rotation',0);inv=mul(power((2,1),-L),power((3,-1),U))
 for _ in range(r):inv=rot(inv)
 target=[(0,0),scale(inv,45),scale(rot(inv),45)];templates=[]
 for h in range(L,U+1):
  u=mul(power((2,1),h-L),power((3,-1),U-h))
  for _ in range(r):u=rot(u)
  for order in range(2):
   v=scale(u,5 if order else 3);w=scale(rot(rot(u)),3 if order else 5)
   for rotation in range(6):templates.append([(0,0),v,w]);v=rot(v);w=rot(w)
 pts=target[:];ids={v:i for i,v in enumerate(pts)};triangles=[];heights=[]
 with open(prefix+'.remaining.txt') as f:
  first=next(f)
  for line in f:
   o,x,y=map(int,line.split());tri=[add((x,y),v) for v in templates[o]];t=[]
   for v in tri:
    if v not in ids:ids[v]=len(pts);pts.append(v)
    t.append(ids[v])
   triangles.append(t);heights.append(L+o//12)
 assert all(abs(h)<=4 for h in heights), 'The reused endpoint reducer currently accepts heights only from -4 to4.'
 with open(prefix+'.geometry.txt','w') as f:
  f.write(f'1 {len(pts)} {len(triangles)}\n')
  for x,y in pts:f.write(f'{x} {y}\n')
  for t,h in zip(triangles,heights):f.write(f'{t[0]} {t[1]} {t[2]} {h} 0\n')
 subprocess.run([a.endpoint_executable,prefix+'.geometry.txt',prefix+'.model.txt','0'],check=True)
 red=json.loads(Path(prefix+'.model.txt.json').read_text())
 if red['restricted_pool_conflict']:
  print('Exact 0/1 propagation contradicts this complete band.');return
 if os.environ.get('ERDOS_ORTOOLS_PATH'):sys.path.insert(0,os.environ['ERDOS_ORTOOLS_PATH'])
 from ortools.sat.python import cp_model
 model=cp_model.CpModel();selected=[];var_source=[]
 with open(prefix+'.model.txt') as f:
  nv,nsel=map(int,next(f).split());vs=[model.new_bool_var('') for _ in range(nv)];var_source=[None]*nv
  for _ in range(nv+nsel):
   v,source,mirror,h=map(int,next(f).split());assert mirror==0
   if v<0:selected.append(source)
   else:var_source[v]=source
  rows=0
  for line in f:
   b,n,*lits=map(int,line.split());assert len(lits)==n;model.add(cp_model.LinearExpr.weighted_sum([vs[abs(z)-1] for z in lits],[1 if z>0 else -1 for z in lits])==b);rows+=1
 model.add(sum(vs)+len(selected)==135)
 solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=a.seconds;solver.parameters.num_search_workers=1;solver.parameters.linearization_level=0;solver.parameters.symmetry_level=0;solver.parameters.random_seed=634;solver.parameters.log_search_progress=True
 start=time.monotonic();status=solver.solve(model);result={'status':solver.status_name(status),'variables':nv,'rows':rows,'selected_by_propagation':len(selected),'seconds':time.monotonic()-start,'band':[L,U],'global_E135_decided':False}
 if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
  selected += [var_source[k] for k,v in enumerate(vs) if solver.value(v)];assert len(selected)==135
  result['selected_indices']=selected
  cert={'format':'eisenstein_integer_frame_v1','frame_squared_scale':7**(U-L),'tile':[3,5,7],'target':[list(v) for v in target],'triangles':[[list(pts[v]) for v in triangles[k]] for k in selected],'tile_count':135,'band':[L,U],'basis_rotation':r};Path(prefix+'.certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
 Path(prefix+'.cpsat.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

if __name__=='__main__':main()
