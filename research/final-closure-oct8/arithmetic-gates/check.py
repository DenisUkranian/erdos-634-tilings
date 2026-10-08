#!/usr/bin/env python3
'''Independently cross-check all angular candidates for60,135,154.
The geometric/classification inputs are identified in README.md.
'''
from pathlib import Path
import importlib.util,json,sys
from dataclasses import asdict
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'research/uniform-reduction'))
from candidates import enumerate_candidates,classical
spec=importlib.util.spec_from_file_location('independent_sweep',ROOT/'research/final-closure-oct8/class15/reduce_class15.py')
sweep=importlib.util.module_from_spec(spec);spec.loader.exec_module(sweep)

def run():
 result=[]
 for n in [60,135,154]:
  rows=enumerate_candidates(n)
  keys={(z.branch,tuple(sorted(z.tile)),tuple(sorted(z.target))) for z in rows}
  other=sweep.independent(n)
  if keys!=other:raise AssertionError((n,keys^other))
  if classical(n) is not None:raise AssertionError(('unexpected classical witness',n))
  if n==154:
   expected={('I120',(7,8,13),(91,91,154))}
   if keys!=expected:raise AssertionError('unique154 candidate failed')
  result.append(dict(N=n,classical_witness=None,independent_enumerations_agree=True,candidates=[asdict(z) for z in rows],candidate_count=len(rows)))
 return dict(status='PASS',method1='factor/divisor sieve',method2='independently implemented bounded parameter sweep',cases=result,geometric_nonexistence_inferred_here=False,classification_inputs='Published exhaustive angular classification and rationality, with classical cases separated; uniform-reduction/PROOF.md and references')
if __name__=='__main__':
 r=run();p=Path(__file__).with_name('checked.json');p.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='cases'},indent=2))
