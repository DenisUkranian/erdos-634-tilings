#!/usr/bin/env python3
"""Exploratory macro search only; no unrestricted tiling exclusion."""
from pathlib import Path
import sys,time,json,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'f3-primitive-oct7'))
from macro_search import Search,E,F
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--max-macros',type=int,default=5)
parser.add_argument('--seconds',type=float,default=100)
parser.add_argument('--output')
args=parser.parse_args()
S=Search(24,11,31,max_macros=args.max_macros,min_scale=1,seconds=args.seconds)
conv=lambda p:(F(p[0])+F(p[1],2),F(p[1],2))
S.target=tuple(map(conv,[(312,0),(961,0),(576,264),(312,143)]));S.n=792
unit_sg=[False]*1000
unit_sg[0]=True
for x in range(1,len(unit_sg)):
 unit_sg[x]=any(x>=k and unit_sg[x-k] for k in (24,11,31))
old=S.dfs
def filtered(placed,scales):
 for u,v in E.atomic_boundary(S.target,placed,S.check):
  if any(E.on_segment(a,b,u) and E.on_segment(a,b,v) for a,b in E.edges(S.target)):
   length=E.rational_sqrt(E.dot(E.sub(v,u),E.sub(v,u),3))
   if length.denominator!=1 or not unit_sg[int(length)]:return False
 return old(placed,scales)
S.dfs=filtered
S.start=time.monotonic()
try:r=S.dfs((),())
except(E.BudgetExceeded,RecursionError):r=None
out={'status':'FOUND' if r else 'RESTRICTED_EXHAUSTED' if r is False else 'INCOMPLETE','nodes':S.nodes,'deepest':S.deepest,'seconds':time.monotonic()-S.start,'target':E.encode_tri(S.target),'max_macros':S.max_macros,'macros':None if S.found is None else [{'scale':k,'vertices':E.encode_tri(t)} for t,k in zip(*S.found)]}
out.update({'tile':[24,11,31],'count':792,'coordinate_field':'(x,y) means x+i*y*sqrt(3)','scope':'EXPLORATORY integer-grid macro recipe search only','full_Erdos634_solved':False})
if args.output:Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='macros'}))
