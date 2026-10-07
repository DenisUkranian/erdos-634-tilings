#!/usr/bin/env python3
"""Exact finite local propagation from ccaa; no global exclusion is inferred."""
from fractions import Fraction as F
from pathlib import Path
import json,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'group1-global-scales'))
from pruned_search import E, Instance,PrunedSearch

def setup(v,reverse=False):
 u=v-1;a=u*v;b=v*v-u*u;c=v*v;Q=b+c
 s=PrunedSearch(Instance('G1-W',(a,b,c),(2*v**3,2*u*Q,2*v*b),4*Q,(u,v),2))
 s.D=4*v*v-u*u
 s.template=E.triangle(((F(0),F(0)),(F(b),F(0)),(F(Q,2),F(u,2))))
 C=(F(0),F(0)); A=(F(2*v*b),F(0)); O=(F(2*v**4-4*v*v*u*u+u**4,v),F(u*Q,v))
 s.target=E.triangle((C,A,O))
 def supported(x,L,r0,r1):
  xx=F(r0*r0+L*L-r1*r1,2*L)
  yy=E.orient(*s.template)/L
  return E.triangle(((F(x),F(0)),(F(x+L),F(0)),(x+xx,yy)))
 root=(supported(0,c,b,a),supported(c,c,a,b) if reverse else supported(c,c,b,a),supported(2*c,a,b,c),supported(2*c+a,a,b,c))
 assert all(E.inside(s.target,p) for t in root for p in t)
 assert not any(E.overlap(t,z) for i,t in enumerate(root) for z in root[:i])
 return s,root

def force(v,reverse=False):
 s,root=setup(v,reverse); placed=root; history=[]
 while len(placed)<s.I.n:
  B=E.atomic_boundary(s.target,placed)
  if not s.residual_valid(B):return {'v':v,'reverse':reverse,'status':'FILTER_REJECTED','placed':len(placed),'history':history}
  secs=E.convex_sectors(B,s.D)
  choices=[(len(ts),sec,ts) for sec in secs for ts in [E.placements(s.template,sec,s.target,placed,s.D)]]
  k,sec,ts=min(choices,key=lambda r:r[0])
  if k!=1:return {'v':v,'reverse':reverse,'status':'NO_PLACEMENT' if k==0 else 'BRANCHING_REQUIRED','placed':len(placed),'min_choices':k,'history':history,'branches':[[E.encode_tri(t) for t in row[2]] for row in choices if row[0]==k]}
  history.append(E.encode_tri(ts[0]));placed+=(ts[0],)
 return {'v':v,'reverse':reverse,'status':'FOUND','placed':len(placed),'history':history}
if __name__=='__main__':
 rows=[force(v,rev) for v in range(3,13) for rev in [False,True]]
 Path(__file__).with_name('local-propagation.json').write_text(json.dumps(rows,indent=2)+'\n')
 print(json.dumps([{k:v for k,v in r.items() if k not in ('history','branches')} for r in rows],indent=2))
