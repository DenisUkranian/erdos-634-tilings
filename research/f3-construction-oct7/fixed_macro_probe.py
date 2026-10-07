#!/usr/bin/env python3
"""Restricted prescribed-scale probe, not an unrestricted nonexistence test."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'f3-primitive-oct7'))
from macro_search import Search,E
class Fixed(Search):
 def __init__(self,scales,seconds=15):
  super().__init__(24,11,31,max_macros=len(scales),min_scale=min(scales),seconds=seconds)
  self.inventory=tuple(sorted(scales));self.remaining_nodes=0
  assert sum(k*k for k in self.inventory)==self.n
 def dfs(self,placed,scales):
  self.check();self.nodes+=1;self.deepest=max(self.deepest,len(placed))
  remain=list(self.inventory)
  for k in scales:remain.remove(k)
  if not remain:self.found=(placed,scales);return True
  key=tuple(sorted(placed))
  if key in self.dead:return False
  B=E.atomic_boundary(self.target,placed,self.check)
  sectors=E.convex_sectors(B,3)
  best=None
  for sector in sectors[:min(4,len(sectors))]:
   ps=[]
   for k in set(remain):ps.extend((k,t) for t in E.placements(self.templates[k],sector,self.target,placed,3,self.check))
   if best is None or len(ps)<len(best):best=ps
   if not best:break
  for k,t in best:
   if self.dfs(placed+(t,),scales+(k,)):return True
  self.dead.add(key);return False
if __name__=='__main__':
 r=[]
 for scales in ((31,31,31,31,31,5),(43,31,31,31,7,7)):
  out=Fixed(scales).run();out['prescribed_scales']=scales;r.append(out)
 print(json.dumps({'status':'EXPLORATORY','results':r,'full_Erdos634_solved':False},indent=2))
