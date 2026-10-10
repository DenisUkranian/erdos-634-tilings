# Run this validation with Python assertions enabled.
if not __debug__:
    raise RuntimeError('Run without the -O option.')
from fractions import Fraction as Q
from pathlib import Path
import sys,json,random,copy,time,importlib.util
from verify import Replay,ccw,point,edges,norm,sub,ori,det,direction,Invalid,need
base=Path(__file__).parent/'dependencies'
spec=importlib.util.spec_from_file_location('prior_construction',base/'prior_positive_constructor.py');con=importlib.util.module_from_spec(spec);spec.loader.exec_module(con)
def convert(d):
 u,v,m=d['u'],d['v'],d['m'];b=v*v-u*u;P=3*v*v-u*u;D=4*v*v-u*u;root=1;p=2
 while p*p<=D:
  while D%(p*p)==0:D//=p*p;root*=p
  p+=1
 den=d['coordinate_denominator']
 def f(x):
  x,y=(Q(c,den) for c in x);return [str(v*x+Q(u*P,2*v*v)*y),str(Q(b*root,2*v*v)*y)]
 return {'u':u,'v':v,'m':m,'branch':d['branch'],'D':D,'N':d['tile_count'],'target':[f(p) for p in d['target']],'triangles':[[f(p) for p in t] for t in d['triangles']]}
reps=[];rng=random.Random(634);start=time.monotonic()
for m,beta in [(3,False),(3,True),(4,False),(4,True)]:
 d=convert(con.construction(2,3,m,beta));r=Replay(d,'control',0);tiles=[ccw(tuple(map(point,t))) for t in d['triangles']]
 # Check nonoverlap and boundary cancellation, not just the side relaxation.
 for t in tiles:r.push(t)
 ev={}
 from collections import defaultdict,Counter
 ev=defaultdict(Counter)
 for t,sg in [(r.target,1)]+[(t,-1) for t in tiles]:
  for a,b in edges(t):
   dr=direction(sub(b,a))
   if dr<(0,0):dr=(-dr[0],-dr[1])
   key=(dr,det(dr,a));lo,hi=sorted((a,b));s=sg*(1 if a<b else -1);ev[key][lo]+=s;ev[key][hi]-=s
 need(all(not any(v for v in c.values()) for c in ev.values()),'control does not cover')
 need(r.boundary_possible(),'full positive rejected')
 for _ in tiles:r.pop()
 # Every prefix and its reverse remain compatible with an actual completion.
 checks=1
 for order in [tiles,list(reversed(tiles))]:
  for t in order:r.push(t);need(r.boundary_possible(),'positive prefix rejected');checks+=1
  for _ in order:r.pop()
 for j in range(30):
  subset=rng.sample(tiles,rng.randrange(len(tiles)+1))
  for t in subset:r.push(t)
  need(r.boundary_possible(),'positive subset rejected');checks+=1
  for _ in subset:r.pop()
 reps.append({'N':len(tiles),'family':r.fam,'m':m,'positive_subset_checks':checks,'status':'PASS'})
 print(reps[-1],flush=True)
# Fault injection for the proof data.
faults=[]
d=json.loads(Path(__file__).with_name('W56proof1.json').read_text())
for kind in ['delete_branch','cycle','spurious_boundary','moved_tile']:
 z=copy.deepcopy(d)
 if kind=='delete_branch':
  k=next(i for i,r in enumerate(z['proof']) if len(r['children'])>=2);z['proof'][k]['children'].pop()
 elif kind=='cycle':z['proof'][0]['children'][0][1]=0
 elif kind=='spurious_boundary':z['proof'][0]['reason']='boundary';z['proof'][0]['children']=[]
 else:
  z['proof'][0]['children'][0][0][0][0]=str(Q(z['proof'][0]['children'][0][0][0][0])+1)
 try:Replay(z,'W_short',1).run()
 except Invalid as e:faults.append({'mutation':kind,'status':'REJECTED','reason':str(e)})
 else:raise RuntimeError('mutation not rejected: '+kind)
report={'status':'PASS','positive_controls':reps,'fault_injections':faults,'seconds':time.monotonic()-start}
Path(__file__).with_name('controls_new.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
