"""Fresh adversarial checks. Never interprets a timeout or exception as a tiling theorem."""
from pathlib import Path
import copy,hashlib,importlib.util,json,subprocess,sys,tempfile,time
from math import gcd
B=Path(__file__).resolve().parent; R=B/'replay_workspace'; L=B/'fresh_logs';L.mkdir(exist_ok=True)
W=R/'Erdos634_W_beta_unrestricted_2026-10-09/Erdos634_W_beta_unrestricted'
C=R/'Erdos634_class14_complete_2026-10-09/Erdos634_class14_complete_2026-10-09'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
wv=module('w_verify_audit',W/'verify.py');cv=module('class14_verify_audit',C/'verify.py')
res=[];start=time.monotonic()
def reject(name,fn,expected):
 try:fn()
 except expected as e:
  res.append({'test':name,'outcome':'REJECTED_AS_EXPECTED','reason':str(e)[:300]})
 else:raise RuntimeError('Unsound acceptance in '+name)
p=json.loads((W/'W_1656.json').read_text())
with tempfile.TemporaryDirectory() as tmp:
 t=Path(tmp)/'test.json'
 for kind in ('replace_tile_by_duplicate','move_vertex','flip_orientation','wrong_scale','wrong_denominator','wrong_branch'):
  z=copy.deepcopy(p)
  if kind=='replace_tile_by_duplicate':z['triangles'][0]=copy.deepcopy(z['triangles'][1])
  if kind=='move_vertex':z['triangles'][0][0][0]+=1
  if kind=='flip_orientation':z['triangles'][0][0],z['triangles'][0][1]=z['triangles'][0][1],z['triangles'][0][0]
  if kind=='wrong_scale':z['m']+=1
  if kind=='wrong_denominator':z['coordinate_denominator']+=1
  if kind=='wrong_branch':z['branch']='beta'
  t.write_text(json.dumps(z));reject('positive_'+kind,lambda:wv.verify(t),AssertionError)
 # Translation covariance: move target and all tiles together, keep exact metric.
 z=copy.deepcopy(p)
 for tri in [z['target']]+z['triangles']:
  for xy in tri:xy[0]+=17;xy[1]-=31
 t.write_text(json.dumps(z));r=wv.verify(t);res.append({'test':'translated_positive','outcome':r['status'],'N':r['N']})
 # Double coordinate numerators AND common denominator; same physical tiling.
 z=copy.deepcopy(p);z['coordinate_denominator']*=2
 for tri in [z['target']]+z['triangles']:
  for xy in tri:xy[0]*=2;xy[1]*=2
 t.write_text(json.dumps(z));r=wv.verify(t);res.append({'test':'redundant_denominator_positive','outcome':r['status'],'N':r['N']})
 # Optimized Python must not bypass the verifier's assertions.
 opt=subprocess.run([sys.executable,'-O',str(W/'verify.py'),str(W/'W_1656.json')],capture_output=True,text=True)
 if opt.returncode==0 or 'Assertions must be enabled' not in opt.stderr:raise RuntimeError('-O guard failed')
 res.append({'test':'python_O_guard','outcome':'REJECTED_AS_EXPECTED','reason':'explicit __debug__ guard'})
d=json.loads((C/'W56proof1.json').read_text())
for kind in ('deleted_branch','cycle','unjustified_boundary','shifted_triangle','unreachable_record','wrong_N','incomplete_status'):
 z=copy.deepcopy(d)
 if kind=='deleted_branch':
  k=next(i for i,x in enumerate(z['proof']) if len(x['children'])>=2);z['proof'][k]['children'].pop()
 if kind=='cycle':z['proof'][0]['children'][0][1]=0
 if kind=='unjustified_boundary':z['proof'][0]['reason']='boundary';z['proof'][0]['children']=[]
 if kind=='shifted_triangle':z['proof'][0]['children'][0][0][0][0]=str(cv.Q(z['proof'][0]['children'][0][0][0][0])+1)
 if kind=='unreachable_record':z['proof'].append(copy.deepcopy(z['proof'][-1]))
 if kind=='wrong_N':z['N']+=1
 if kind=='incomplete_status':z['status']='INCOMPLETE'
 reject('negative_'+kind,lambda:cv.Replay(z,'W_short',1).run(),cv.Invalid)
# Stronger statements sometimes made in prose must explicitly FAIL.
u,v=2,5;a,b,c=u*v,v*v-u*u,v*v
assert u*c==v*a and u<v
res.append({'test':'short_c_does_not_mean_c_only','outcome':'COUNTEREXAMPLE_TO_STRENGTHENING','u':u,'v':v,'equation':f'{u}*{c}={v}*{a}','not_a_tiling':True})
assert v*c ==5*a+3*c
res.append({'test':'equal_side_no_b_does_not_mean_c_only','outcome':'COUNTEREXAMPLE_TO_ARITHMETIC_INFERENCE','equation':f'{v}*{c}=5*{a}+3*{c}','not_a_tiling':True})
# At the excluded endpoint n=v the no-b conclusion can fail: v*c=u*a+v*b.
assert v*c==u*a+v*b
res.append({'test':'short_c_strict_bound_necessary','outcome':'COUNTEREXAMPLE_TO_WEAKENED_HYPOTHESIS','n':v,'A':u,'B':v,'C':0,'equation':f'{v}*{c}={u}*{a}+{v}*{b}'})
out={'scope':'Finite certificate integrity, geometric verification covariance, and arithmetic counterexamples to stronger claims. Not a full theorem audit.','tests':res,'seconds':round(time.monotonic()-start,3)}
(L/'fresh_crash_tests.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n');print(json.dumps(out,indent=2,ensure_ascii=False))
