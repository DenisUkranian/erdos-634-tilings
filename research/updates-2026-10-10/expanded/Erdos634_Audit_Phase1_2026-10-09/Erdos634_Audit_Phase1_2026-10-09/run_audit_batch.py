from pathlib import Path
import shutil,subprocess,sys,time,json,concurrent.futures
B=Path(__file__).resolve().parent
S=B/'source_snapshots'; R=B/'replay_workspace'; L=B/'fresh_logs';L.mkdir(exist_ok=True)
if not R.exists():shutil.copytree(S,R)
W=R/'Erdos634_W_beta_unrestricted_2026-10-09/Erdos634_W_beta_unrestricted'
C=R/'Erdos634_class14_complete_2026-10-09/Erdos634_class14_complete_2026-10-09'
E=R/'erdos634_effective_density_2026-10-09/effective-density'
F=R/'F3_14430_no61_height_2026-10-09(1)/F3_14430_no61'
G=R/'erdos634_14430_independent_attack'
T=R/'Erdos634_small_scale_audit_2026-10-09/Erdos634_small_scale_audit_2026-10-09'
tasks=[('class14_full',C,['reproduce.py'],300),('W_symbolic',W,['check_symbolic.py'],180),('W_1656_all_pairs',W,['verify.py','W_1656.json','--all-pairs','--report',str(L/'W_1656.report.json')],120),('beta_2556_all_pairs',W,['verify.py','beta_2556.json','--all-pairs','--report',str(L/'beta_2556.report.json')],120),('no61',F,['verify_no61.py'],120),('14430_currents',G,['verify_14430.py'],120),('density',E,['check_density.py','--limit','3000','--output',str(L/'density.report.json')],180),('six_small',T,['verify_certificate.py',*sorted(p.name for p in T.glob('*refutation.json'))],120),('six_small_controls',T,['check_controls.py'],120)]
def run(item):
 name,cwd,args,lim=item;st=time.monotonic();cmd=[sys.executable,*args]
 try:
  with (L/(name+'.log')).open('w') as log:r=subprocess.run(cmd,cwd=cwd,stdout=log,stderr=subprocess.STDOUT,timeout=lim)
  status='COMPLETED_ZERO_EXIT' if r.returncode==0 else 'FAILED';rc=r.returncode
 except subprocess.TimeoutExpired:status='TIME_LIMIT_NO_RESULT';rc=None
 except Exception as e:status='ERROR';rc=None;(L/(name+'.exception')).write_text(repr(e))
 out={'name':name,'status':status,'exit_code':rc,'seconds':round(time.monotonic()-st,3),'command':cmd,'cwd':str(cwd),'log':str(L/(name+'.log'))}
 (L/(name+'.task.json')).write_text(json.dumps(out,indent=2));print(json.dumps(out),flush=True);return out
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:out=list(ex.map(run,tasks))
(L/'batch_report.json').write_text(json.dumps({'scope':'Finite fresh replays only; universal lemmas and external classification not machine-proved','tasks':out},indent=2))
