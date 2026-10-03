#!/usr/bin/env python3
"""Regenerate and verify the full reversed F4 unit examples."""
from pathlib import Path
import copy,json
from construct_reversed import construct,construct_f2
from verify_f2 import verify as verify_f2
from verify_reversed import verify
ROOT=Path(__file__).resolve().parent

def main():
 results=[]
 for m in (2,3):
  path=ROOT/'certificates'/f'f4_reversed_8_7_13_m{m}.json'
  frozen=json.loads(path.read_text())
  assert construct(8,7,13,m)==frozen, 'Frozen certificate differs from generator'
  results.append(verify(frozen))
 # The construction theorem permits nonprimitive triples; the interval iff does not.
 results.append(verify(construct(16,14,26,1)))
 try:construct(8,7,13,1)
 except ValueError:pass
 else:raise AssertionError('Primitive scale-one semigroup gap was accepted')
 base=json.loads((ROOT/'certificates/f4_reversed_8_7_13_m2.json').read_text())
 rejected=[]
 for name in ('missing','duplicate','moved','count'):
  bad=copy.deepcopy(base)
  if name=='missing':bad['triangles'].pop()
  elif name=='duplicate':bad['triangles'][-1]=bad['triangles'][0]
  elif name=='moved':bad['triangles'][0][0][0]='-1234567'
  else:bad['count']+=1
  try:verify(bad)
  except ValueError:rejected.append(name)
  else:raise AssertionError('Corruption accepted: '+name)
 f2=json.loads((ROOT/'certificates/f2_balanced_8_7_13_m2.json').read_text())
 assert construct_f2(8,7,13,2)==f2
 f2_result=verify_f2(f2)
 report={'status':'PASS','construction_domain':'a>b>0; c²=a²+ab+b²; m(bc−a²) in <a,b>','balanced_theorem':'b<a≤4b/3 implies every m≥2','unit_certificate_checks':results,'F2_unit_certificate_check':f2_result,'mutation_rejections':rejected,'primitive_m1_gap_rejected':True,'full_Erdos634_solved':False,'external_peer_review':False}
 (ROOT/'balanced_f4_verification.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
