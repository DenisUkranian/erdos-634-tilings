"""Targeted logical tests: allocation growth, scope/rebuild, and strict empty-node gate.

The selected synthetic placements intentionally overlap; these tests exercise the
population projection only and do not constitute geometric tiling controls.
"""
from pathlib import Path
from types import SimpleNamespace
import tempfile,sys
HERE = Path(__file__).resolve().parent
BASE = HERE.parent/'global-endpoints'/'integer'
sys.path[:0] = [str(BASE), str(HERE)]
import global_core_sat as base
from phase_budget import PhaseBudget
from population_search import make_population_search_class
PopulationSearch=make_population_search_class(base,PhaseBudget)

def opts(out,strict=False):return SimpleNamespace(sides=[33,7,37],out=out,random_seed=1776,point_checkpoint=None,proof=False,timeout_ms=10000,minimize_core=False,no_phase_empty=strict)
def literal(bit,value):return bit if value else '(not '+bit+')'
def fixcount(record,value):return ['(assert '+literal(bit,value&(1<<k))+')'for k,bit in enumerate(record['bits'])]
def query(s,assertions,expected):
 s.enqueue('(push 1)');s.flush();answer=s.smt.run('\n'.join(assertions)+'\n(check-sat)');assert answer==expected,answer
 s.enqueue('(pop 1)') # match the base run loop: pop is flushed with the next query

def main():
 with tempfile.TemporaryDirectory(prefix='scope-pop-')as tmp:
  s=PopulationSearch(opts(tmp));g=s.g;c=g.c
  def ordinary(i):return ((c*(40+i)+1,c*200,1),0,0,1)
  first=s.insert(ordinary(0));record=s.population_nodes[0][s.phase_budgets[0].node(ordinary(0)[0],0)];core=s.population_nodes[0][(0,0,0)]
  query(s,fixcount(record,3),'unsat') # current-pool normalized cap is 2
  query(s,fixcount(core,1),'unsat') # no known core placements
  for i in range(1,75):s.insert(ordinary(i))
  fixes=['(assert x'+str(i)+')'for i in range(75)]+fixcount(record,3)
  query(s,fixes,'sat') # previous cap 2 has been popped
  query(s,['(assert x'+str(i)+')'for i in range(75)]+fixcount(record,2),'unsat')
  for i in range(28):s.insert(((40+i,220,0),0,0,1))
  fixes=['(assert x'+str(i)+')'for i in range(len(s.tiles))]+fixcount(record,3)+fixcount(core,1)
  query(s,fixes,'sat') # core cap grows from 0 to 1
  query(s,['(assert x'+str(i)+')'for i in range(len(s.tiles))]+fixcount(core,0),'unsat')
  s.rebuild(1)
  query(s,fixes,'sat')
  query(s,fixcount(record,4),'unsat') # current cap remains live after rebuild
  query(s,['(assert '+record['flag']+')','(assert '+record['excuse']+')']+fixcount(record,0),'sat')
  s.smt.close();s.journal.close()
 with tempfile.TemporaryDirectory(prefix='scope-strict-')as tmp:
  s=PopulationSearch(opts(tmp,True));s.insert(ordinary(0));record=s.population_nodes[0][s.phase_budgets[0].node(ordinary(0)[0],0)]
  query(s,['(assert '+record['flag']+')','(assert '+record['excuse']+')']+fixcount(record,0),'unsat')
  s.rebuild(1)
  query(s,['(assert '+record['flag']+')','(assert '+record['excuse']+')']+fixcount(record,0),'unsat')
  s.smt.close();s.journal.close()
 try:PhaseBudget(base.Geometry(16,5,19),1)
 except AssertionError:pass
 else:raise AssertionError('Unsupported even-short-side shape accepted')
 print('PASS: pool caps grow after pop; core and ordinary capacities; rebuild preserves current caps; strict empty gate; odd-input guard.')
if __name__=='__main__':main()
