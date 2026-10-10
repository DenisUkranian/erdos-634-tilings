#!/usr/bin/env python3
"""Recheck only the completed arithmetic and support eliminations."""
from pathlib import Path
import json
from check_gate import gate
from verify_support import check

base=Path(__file__).resolve().parent
reports=[]
for N in (23,92):
 r=gate(N);keep=[]
 if r['classical_witnesses']:
  raise RuntimeError('Unexpected classical count')
 for row in r['all_candidates']:
  u,v=row['parameters'];m=row['scale']
  if row['branch'] in ('theta','double-angle'):
   necessary=u*v if row['branch']=='theta' else u*u
   if m*(v*v-u*u)<necessary:continue
  keep.append(row)
 expected=[('W',(3,4),1 if N==23 else 2),('beta',(2,3),1 if N==23 else 2)]
 actual=[(x['branch'],x['parameters'],x['scale']) for x in keep]
 if actual!=expected:raise RuntimeError((N,actual,expected))
 reports.append({'N':N,'status':'ARITHMETIC_GATE_PASS','surviving_instances':keep})
for root in (0,1):
 reports.append(check(base/f'W92_supported_root{root}.json',root))
combined={'status':'COMPLETED_SUBCHECKS_PASS','N92_decided':False,
 'full_Erdos634_solved':False,'reports':reports}
(base/'reproduction_report.json').write_text(json.dumps(combined,indent=2)+'\n')
print('\nCOMPLETED SUBCHECKS PASS. W92 and N92 remain UNDECIDED.')
