#!/usr/bin/env python3
"""Independent exact six-corner incompatibility replay, one fixed collar.

No search/generator imports. Re-enumerates every possible complete fan at six
specified convex sectors; Fraction clipping verifies all retained choices and
all eliminations. The completeness argument is in docs/n105-six-corner-obstruction.md.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import permutations, product
from hashlib import sha256
import json
from verify_n105_collar_refutations import empty_sector, length, vsub, area2, clipping
from verify_n105_local_fans import verify as verify_local_fans

if not __debug__:raise SystemExit('Run without -O')
DATA=Path(__file__).resolve().parents[1]/'data'

def cross(u,v):return u[0]*v[1]-u[1]*v[0]
def cmul(z,w):return z[0]*w[0]-3*z[1]*w[1],z[0]*w[1]+z[1]*w[0]
def key(t):return tuple(sorted(t))
def fkey(f):return tuple(sorted(key(t) for t in f))
def rotate(u,z):
 x,y=u[0]+u[1]/2,u[1]/2
 xx,yy=z[0]*x-3*z[1]*y,z[1]*x+z[0]*y
 return xx-yy,2*yy

def main(data_directory):
 cp=data_directory/'n105-local-fan-collar-5-21-19.json';xp=data_directory/'n105-six-corner-refutation.json'
 raw=cp.read_bytes();assert sha256(raw).hexdigest()=='8a58a8bbb6a4b69d8372c87ade860cda43c7b311dd7e54d2c9a14e2fd4718792'
 obj=json.loads(raw);pr=json.loads(xp.read_text());base_report=verify_local_fans(data_directory)
 ts=tuple(tuple(tuple(Q(v,obj['scale']) for v in p) for p in t) for t in obj['triangles'])
 a,b,c=5,21,19
 angles=((Q(37,38),Q(5,38)),(Q(-11,38),Q(21,38)),(Q(1,2),Q(1,2)))
 assert 2*angles[0][0]==Q(37,19) and Q(37,19).denominator!=1
 lengths=((b,c),(a,c),(a,b));decompositions={
  cmul(angles[0],angles[2]):((1,0,1),),
  cmul(angles[2],angles[2]):((0,0,2),(1,1,0)),
  angles[1]:((0,1,0),)}
 allfans={};candidate_counts={};clip_tests=0
 for ident,row in zip(pr['sector_indices'],pr['sectors']):
  P=tuple(Q(v,19) for v in row['point']);u=tuple(map(Q,row['outgoing']));w=tuple(map(Q,row['incoming_back']))
  theta=empty_sector(P,u,w,ts);assert theta in decompositions
  start=tuple(v/length(u) for v in u);finish=tuple(v/length(w) for v in w)
  generated={};tried=0
  for counts in decompositions[theta]:
   seqs=set(permutations([k for k in range(3) for _ in range(counts[k])]))
   for seq in sorted(seqs):
    for swaps in product((0,1),repeat=len(seq)):
     tried+=1;cur=start;fan=[];good=True
     for k,sw in zip(seq,swaps):
      nxt=rotate(cur,angles[k]);l,m=lengths[k][sw],lengths[k][1-sw]
      t=(P,(P[0]+l*cur[0],P[1]+l*cur[1]),(P[0]+m*nxt[0],P[1]+m*nxt[1]));cur=nxt
      assert area2(t)==105
      if any(x<0 or y<0 or x+y>105 for x,y in t):good=False;break
      for old in ts+tuple(fan):
       clip_tests+=1
       if area2(clipping(t,old))>0:good=False;break
      if not good:break
      fan.append(t)
     if good:
      assert cur==finish;generated[fkey(fan)]=tuple(fan)
  supplied=[tuple(tuple(tuple(Q(v,361) for v in p) for p in t) for t in fan) for fan in row['fans']]
  assert len(supplied)==2 and len({fkey(f) for f in supplied})==2
  assert set(generated)=={fkey(f) for f in supplied},('Incomplete fan domain',ident)
  allfans[ident]=supplied;candidate_counts[str(ident)]=tried
 domains={i:[0,1] for i in allfans};conflicts_checked=0;strict_points=[]
 for step in pr['elimination_trace']:
  i,x,j=step['sector'],step['option'],step['blocked_by_sector']
  assert i!=j and i in domains and j in domains and x in domains[i]
  assert step['remaining_options']==domains[j] and domains[j]
  for y in domains[j]:
   witness=None
   for ti,t in enumerate(allfans[i][x]):
    for ui,u in enumerate(allfans[j][y]):
     if key(t)==key(u):continue
     clip_tests+=1;inter=clipping(t,u)
     if area2(inter)>0:
      P=tuple(sum(p[k] for p in inter)/len(inter) for k in range(2))
      assert all(cross(vsub(z[(k+1)%3],z[k]),vsub(P,z[k]))>0 for z in (t,u) for k in range(3))
      witness=dict(left=[i,x,ti],right=[j,y,ui],strict_common_interior_point=[str(v) for v in P]);break
    if witness:break
   assert witness is not None,('Unsupported conflict',i,x,j,y)
   strict_points.append(witness);conflicts_checked+=1
  domains[i].remove(x)
 assert any(not d for d in domains.values())
 out=dict(verdict='PASS_FIXED_COLLAR_SIX_CORNER_INCOMPATIBILITY',tile=[5,21,19],placed_tiles=45,
          collar_sha256=sha256(raw).hexdigest(),core_sha256=sha256(xp.read_bytes()).hexdigest(),
          convex_sectors=6,admissible_fans_per_sector=2,raw_fan_candidates=candidate_counts,
          elimination_steps=len(pr['elimination_trace']),pair_conflicts_checked=conflicts_checked,
          rational_clipping_tests=clip_tests,strict_overlap_witnesses=strict_points,
          complete_for_fixed_collar=True,global_N105_decided=False,search_imported=False,
          node_cap=None,initial_collar_pair_tests=base_report['collar_pair_tests'])
 print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':
 import sys
 if len(sys.argv)>2: raise SystemExit('Usage: verify_n105_joint_fans.py [DATA_DIRECTORY]')
 main(Path(sys.argv[1]).resolve() if len(sys.argv)==2 else DATA)
