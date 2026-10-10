from pathlib import Path
import sys,importlib.util,json,time
B=Path(__file__).resolve().parent; W=B/'replay_workspace/Erdos634_W_beta_unrestricted_2026-10-09/Erdos634_W_beta_unrestricted';O=B/'stress_generated';O.mkdir(exist_ok=True)
def load(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
co=load('stress_construct',W/'construct.py');ve=load('stress_verify',W/'verify.py');r=[];st=time.monotonic()
for u,v,m,beta in [(1,2,2,False),(1,3,3,True),(2,3,4,False),(2,5,6,False),(2,11,12,False),(3,10,12,False),(4,5,8,False),(5,8,12,True),(4,6,9,False),(2,5,10,False)]:
 d=co.construction(u,v,m,beta);p=O/f'{u}_{v}_{m}_{"beta" if beta else "W"}.json';p.write_text(json.dumps(d,separators=(',',':')))
 x=ve.verify(p,False);x['seed_t']=d['seed_t'];x['construction_stats']=d['construction_stats'];r.append(x);print(json.dumps({k:x[k] for k in ('u','v','m','branch','N','status')}),flush=True)
res={'scope':'Fresh reconstruction from parameters then supplied separate verifier; no new tiling counts or universal proof by sampling','cases':r,'total_tiles':sum(x['N'] for x in r),'seconds':round(time.monotonic()-st,3)};(B/'fresh_logs/stress_report.json').write_text(json.dumps(res,indent=2));print('total',res['total_tiles'])
