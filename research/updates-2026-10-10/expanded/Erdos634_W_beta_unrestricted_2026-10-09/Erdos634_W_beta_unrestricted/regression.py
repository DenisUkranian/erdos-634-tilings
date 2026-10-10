#!/usr/bin/env python3
"""Fresh unit-coordinate checks for all residues, caps and boundary cases.
The verifier imports no constructor. These examples are controls, not the proof
of the infinite quantifier. Default pair checks cover every unordered pair.
"""
from pathlib import Path
import json,argparse,time,tempfile
from construct import construction
from verify import verify

CASES=[(1,2,2,False),(1,2,3,True),(1,5,6,False),
 (2,3,4,False),(2,5,5,False),(2,5,6,False),(2,5,6,True),(2,5,8,False),
 (3,7,8,False),(3,7,9,False),(3,10,11,False),(3,10,12,False),(3,10,14,False),
 (3,10,11,True),(2,11,12,False),(2,11,12,True),
 (4,6,9,False),(4,6,9,True),(5,8,9,False),(5,8,10,False),(5,8,11,False),(5,8,12,False)]

def run(paircheck=True):
 reports=[];st=time.monotonic()
 with tempfile.TemporaryDirectory(prefix='w_beta_regression_') as td:
  for u,v,m,beta in CASES:
   doc=construction(u,v,m,beta)
   path=Path(td)/f'{"beta" if beta else "W"}_{u}_{v}_{m}.json'
   path.write_text(json.dumps(doc,separators=(',',':')))
   out=verify(path,all_pairs=paircheck);reports.append(out)
   print(u,v,m,'beta' if beta else 'W','N',out['N'],'PASS',flush=True)
  controls=[]
  base=construction(2,5,6)
  for corruption in ['duplicate','deform','reverse']:
   doc=json.loads(json.dumps(base))
   if corruption=='duplicate':doc['triangles'][0]=doc['triangles'][1]
   if corruption=='deform':doc['triangles'][0][0][0]+=1
   if corruption=='reverse':doc['triangles'][0][0],doc['triangles'][0][1]=doc['triangles'][0][1],doc['triangles'][0][0]
   p=Path(td)/f'bad_{corruption}.json';p.write_text(json.dumps(doc))
   try:verify(p)
   except (AssertionError,ValueError):controls.append({'corruption':corruption,'rejected':True})
   else:raise AssertionError('Accepted corruption '+corruption)
 summary={'status':'PASS','case_count':len(reports),'total_unit_tiles':sum(r['N'] for r in reports),
  'total_all_pairs_checked':sum(r['all_pairs_checked'] for r in reports),
  'negative_controls':controls,'elapsed_seconds':round(time.monotonic()-st,3),
  'all_parameter_statement_proved_by':'PROOF.md; not inferred from this finite regression',
  'external_peer_review':False,'full_Erdos634_solved':False,'reports':reports}
 Path('regression_report.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps({k:v for k,v in summary.items() if k!='reports'},indent=2))
 return summary

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--skip-all-pairs',action='store_true');args=ap.parse_args()
 run(not args.skip_all_pairs)
