#!/usr/bin/env python3
"""Regression tests for the logical and geometric kernels.
These do not replace replaying each declared refutation certificate.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/"search"))
import exact_engine as g
from replay_exact import Checker
from pathlib import Path
from itertools import product
import random,json,copy,time
HERE=Path(__file__).resolve().parent

def implication_tests():
 rng=random.Random(634105);checks=0
 original_fans,original_comp=g.fans,g.compatible
 try:
  for n in (2,3,4):
   gaps=[]
   for i in range(n):
    v=g.point(2*i,20);q=g.point(2*i+1,20);p=g.point(2*i,21);gaps.append((v,q,p))
   for repetition in range(50):
    forbidden=set()
    for i in range(n):
     for j in range(i+1,n):
      for a,b in product((0,1),repeat=2):
       if rng.randrange(5)==0:forbidden.add((2*i+a,2*j+b))
    def fans(gap,ts):
     i=gaps.index(gap);return[(2*i,),(2*i+1,)]
    def compatible(f,h):return tuple(sorted((f[0],h[0]))) not in forbidden
    g.fans=fans;g.compatible=compatible
    actual,reason=g.propagate(gaps,())
    solutions=[s for s in product((0,1),repeat=n) if all((2*i+s[i],2*j+s[j]) not in forbidden for i in range(n) for j in range(i+1,n))]
    if not solutions:
     if actual is not None:raise AssertionError('missed unsatisfiable binary instance')
    else:
     if actual is None:raise AssertionError('false binary contradiction')
     for i,d in enumerate(actual):
      values={f[0]%2 for f in d};expected={s[i] for s in solutions}
      if values!=expected:raise AssertionError('incorrect forced literal')
    checks+=1
 finally:g.fans=original_fans;g.compatible=original_comp
 return checks

def geometry_tests():
 data=json.loads((HERE/'data'/'f1_8_7_13.json').read_text());c=Checker(data)
 count=min(180,len(data['triangles']));mapping=[]
 for i in range(count):mapping.append(g.triangle(tuple(g.point(*c.xy[v]) for v in c.t[i])))
 pairs=positive=0
 for i in range(count):
  for j in range(i):
   a=g.overlap(mapping[i],mapping[j]);b=c.overlap(i,j)
   if a!=b:raise AssertionError(('intersection disagreement',i,j))
   positive+=int(a);pairs+=1
 C=c.pt(-49,105);P=c.pt(-42,90);R=c.pt(-42,98);W=c.pt(-35,83)
 T=c.tri((C,P,R));U=c.tri((P,R,W));c.valid_state((T,U))
 if P in c.marks(U)[0] or c.elementary((T,U)):raise AssertionError('interior vertex incorrectly marked')
 if c.overlap(T,U) or not c.overlap(T,T):raise AssertionError('edge-contact regression')
 return {'intersection_pairs':pairs,'positive_area_pairs':positive,'boundary_mark_regression':'PASS'},data

def malformed_tests(data):
 rejected=[]
 def reject(name,d):
  try:Checker(d).verify()
  except (ValueError,KeyError,IndexError) as err:rejected.append({'test':name,'result':'REJECTED','reason':str(err)})
  else:raise AssertionError('invalid data accepted: '+name)
 d=copy.deepcopy(data);d['tile']=[7,8,14];reject('wrong tile',d)
 d=copy.deepcopy(data);d['points'][d['outer'][1]][0]='57';reject('wrong target',d)
 d=copy.deepcopy(data);r=next(iter(d['root_results']));d['root_definitions'][r]['tiles']=d['root_definitions'][r]['tiles'][:-1];reject('wrong initial state',d)
 return rejected

if __name__=='__main__':
 start=time.monotonic();logical=implication_tests();geometry,data=geometry_tests();bad=malformed_tests(data)
 report={'result':'PASS','binary_formula_cases_checked_against_all_assignments':logical,'geometry':geometry,'malformed_certificates':bad,'seconds':time.monotonic()-start,'scope':'Regression tests, not formal verification or a solution of the full problem.'}
 text=json.dumps(report,indent=2)+'\n';print(text);(HERE/'verification'/'selftest.json').write_text(text)
