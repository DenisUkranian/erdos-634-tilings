#!/usr/bin/env python3
from pathlib import Path
import json,subprocess,time,sys
root=Path(__file__).resolve().parent;start=time.monotonic();out=[]
for K in(10,9,8):
 for a in range((K-1)//2+1):
  L=-a;U=K-1-a;support=list(range(L,U+1));name='support_'+('_'.join(map(str,support)))+'.json'
  remaining=180-(time.monotonic()-start)
  if remaining<3:r={'status':'INCOMPLETE','support':support,'reason':'batch180s budget reached'}
  else:
   limit=min(12,remaining-1)
   try:
    p=subprocess.run([sys.executable,str(root/'direction_dp.py'),'--support='+','.join(map(str,support)),'--seconds',str(limit)],capture_output=True,text=True,timeout=min(limit+5,remaining))
    if p.returncode:raise RuntimeError(p.stderr)
    r=json.loads((root/name).read_text())
   except subprocess.TimeoutExpired:r={'status':'INCOMPLETE','support':support,'reason':'process budget reached'}
   except Exception as e:r={'status':'ERROR','support':support,'reason':str(e)}
  (root/name).write_text(json.dumps(r,indent=2)+'\n')
  out.append({'support':support,'status':r['status'],'file':name,'seconds':r.get('seconds'),'reason':r.get('reason')})
  print(json.dumps(out[-1]),flush=True)
(root/'batch_report.json').write_text(json.dumps({'N':135,'target_side':45,'records':out,'seconds':time.monotonic()-start,'scope':'Necessary finite-band inventories, not positioned tilings'},indent=2)+'\n')
