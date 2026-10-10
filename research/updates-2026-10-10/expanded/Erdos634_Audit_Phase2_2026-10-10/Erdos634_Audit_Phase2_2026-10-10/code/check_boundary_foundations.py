"""Crash/regression audit of corner completeness and boundary-word DP.
Truth controls are actual full positive tilings, rechecked by new exact clipping.
Imports the PRIOR generator to supply controls and the PRIOR negative verifier
as the object being tested, not as an independent oracle for truth.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict,Counter
from itertools import permutations,combinations
from math import isqrt,gcd
import importlib.util,json,random,time,sys
from exact_geometry import *
ROOT=Path(__file__).resolve().parents[1]

def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
con=load('prior_gen',ROOT/'inputs'/'construct_prior.py')
old=load('old_neg',ROOT/'inputs'/'verify_prior_negative.py')

def require(ok,msg):
 if not ok:raise ValueError(msg)
def canon(poly):
 poly=ccw(poly);i=min(range(len(poly)),key=lambda i:poly[i]);return tuple(poly[i:]+poly[:i])
def rt(x):
 x=F(x);a=isqrt(x.numerator);b=isqrt(x.denominator)
 require(a*a==x.numerator and b*b==x.denominator,'irrational operation in fixed control');return F(a,b)
def norm(x,D):return x[0]*x[0]+D*x[1]*x[1]
def direction(x):
 den=x[0].denominator*x[1].denominator//gcd(x[0].denominator,x[1].denominator);a=int(x[0]*den);b=int(x[1]*den);g=gcd(abs(a),abs(b))
 require(g>0,'zero direction');return (a//g,b//g)
def is_same_ray(a,b):return det(a,b)==0 and a[0]*b[0]+a[1]*b[1]>0

def convert(doc,reflected=False):
 u,v=doc['u'],doc['v'];bb=v*v-u*u;P=3*v*v-u*u;D=4*v*v-u*u;s=1;k=2
 while k*k<=D:
  while D%(k*k)==0:D//=k*k;s*=k
  k+=1
 den=doc['coordinate_denominator']
 def f(pt):
  x,y=(F(n,den) for n in pt);a=v*x+F(u*P,2*v*v)*y;b=F(bb*s,2*v*v)*y
  return (-(a+F(1,7)) if reflected else a+F(1,7),b-F(2,11))
 target=canon([f(p) for p in doc['target']]);tiles=[canon([f(p) for p in t]) for t in doc['triangles']]
 data={'u':u,'v':v,'m':doc['m'],'branch':doc['branch'],'D':D,'N':len(tiles),'target':[[str(a),str(b)] for a,b in target]}
 return data,target,tiles

def residual_atoms(target,placed):
 events=defaultdict(Counter);lookup={}
 for poly,weight in [(target,1)]+[(t,-1) for t in placed]:
  for a,b in zip(poly,poly[1:]+poly[:1]):
   d=direction(sub(b,a));d=d if d>(0,0) else (-d[0],-d[1]);line=(d,det(d,a));lo,hi=sorted((a,b));sgn=weight if a<b else -weight
   events[line][lo]+=sgn;events[line][hi]-=sgn
 out=[]
 for line,c in events.items():
  pts=sorted(c);level=0
  for a,b in zip(pts,pts[1:]):
   level+=c[a];require(abs(level)<=1,'control multiplicity')
   if level:out.append((a,b) if level>0 else (b,a))
  require(level+c[pts[-1]]==0,'unbalanced finite edge')
 return out

def sectors(atoms):
 germ=defaultdict(dict)
 for a,b in atoms:
  germ[a][direction(sub(b,a))]=1;germ[b][direction(sub(a,b))]=-1
 out=[]
 for p,rays in germ.items():
  for d,sd in rays.items():
   if sd!=1:continue
   for e,se in rays.items():
    if se!=-1 or det(d,e)<=0:continue
    if any(det(d,z)>0 and det(z,e)>0 for z in rays):continue
    out.append((p,d,e))
 return out

def independent_choices(sec,target,placed,sides,D):
 p0,d,e=sec;ln=rt(norm(d,D));axis=mul(1/ln,d);perp=(-D*axis[1],axis[0]);out=set()
 for s,r,opp in permutations(sides):
  proj=F(s*s+r*r-opp*opp,2*s);height=rt(F(r*r-proj*proj,D));second=add(mul(proj,axis),mul(height,perp))
  if det(second,e)<0:continue
  tr=canon([p0,add(p0,mul(s,axis)),add(p0,second)])
  if not all(inside_convex(target,x) for x in tr):continue
  bx=box(tr)
  if any(boxes_overlap(bx,box(t)) and intersect_area2(tr,t)>0 for t in placed):continue
  out.add(tr)
 return out

def independent_dictionary(data,target,sides):
 u,v,m,D=data['u'],data['v'],data['m'],data['D'];a,b,c=sides
 allowed=[]
 for j in range(3):
  opposite=rt(norm(sub(target[(j+1)%3],target[(j+2)%3]),D))
  if data['branch']=='beta':allowed.append({a} if opposite==m*u*(3*v*v-u*u) else {b})
  elif opposite==m*v*b:allowed.append({b})
  elif opposite==m*u*(2*v*v-u*u):allowed.append({a})
  else:allowed.append({a,b})
 out=set()
 for sideid,(start,end) in enumerate(zip(target,target[1:]+target[:1])):
  L=int(rt(norm(sub(end,start),D)));axis=mul(F(1,L),sub(end,start));perp=(-D*axis[1],axis[0])
  for k in range(L):
   at=add(start,mul(k,axis))
   for edge,radial,opposite in permutations(sides):
    if k+edge>L or (k==0 and opposite not in allowed[sideid]) or (k+edge==L and radial not in allowed[(sideid+1)%3]):continue
    proj=F(edge*edge+radial*radial-opposite*opposite,2*edge);h=rt(F(radial*radial-proj*proj,D));third=add(at,add(mul(proj,axis),mul(h,perp)))
    tri=canon([at,add(at,mul(edge,axis)),third])
    if intersect_area2(tri,target)!=signed2(tri):continue
    out.add((tri,sideid,k,k+edge,edge==c,opposite==c,radial==c))
 return out

def true_side_paths(rep,tiles):
 result=[]
 for a,b in zip(rep.target,rep.target[1:]+rep.target[:1]):
  D=rep.D;L=rt(norm(sub(b,a),D));axis=mul(1/L,sub(b,a));supported=[]
  for tr in tiles:
   for i,(x,y) in enumerate(zip(tr,tr[1:]+tr[:1])):
    if side(a,b,x)==0 and side(a,b,y)==0:
     dot=lambda z:(z[0]*axis[0]+D*z[1]*axis[1])
     l,r=sorted((dot(sub(x,a)),dot(sub(y,a))))
     supported.append((l,r,tr,x,y))
  supported.sort()
  require(supported and supported[0][0]==0 and supported[-1][1]==L,'true boundary gaps')
  require(all(r==l2 for (_,r,*_), (l2,*_) in zip(supported,supported[1:])),'true side partition')
  result.append(supported)
 return result

def brute_paths(rep,bans):
 """Traverse without automaton state; inspect each COMPLETE word afterwards."""
 all_ok=True;words=0
 for sid,L in enumerate(rep.extlen):
  found=False
  def acceptable(word):
   if not any(rep.bcs[x][5] and rep.bcs[y][5] for x,y in zip(word,word[1:])):return False
   for k,(i,j) in enumerate(zip(word,word[1:])):
    if rep.bcs[i][7] and rep.bcs[j][6]:return False
   for k,i in enumerate(word):
    if not rep.bcs[i][5]:continue
    left=(k==0 or rep.bcs[word[k-1]][7]);right=(k==len(word)-1 or rep.bcs[word[k+1]][6])
    if left and right:return False
   return True
  def dfs(pos,word):
   nonlocal found,words
   if pos==L:
    words+=1
    if acceptable(word):found=True
    return
   for i in rep.steps[sid][pos]:
    if not bans[i]:dfs(rep.bcs[i][4],word+[i])
  dfs(0,[]);all_ok&=found
 return all_ok,words

def main():
 start=time.monotonic();rng=random.Random(6340210);reports=[];total_sectors=0;overruns=[];non_supported_gamma=[];total_pairs=0;dp_trials=0;full_words=0;bad_mark_witnesses=[]
 # Small but genuine controls in both chiralities and several target scales.
 for u,v,m,beta,refl in [(1,2,2,False,False),(1,2,2,True,True),(2,3,3,False,False),(2,3,3,True,True),(2,3,4,False,True)]:
  doc=con.construction(u,v,m,beta);data,target,tiles=convert(doc,refl);rep=old.Replay(data,'control',0);D=data['D']
  # Independently enumerate the full supported boundary dictionary.
  independent=independent_dictionary(data,target,rep.sides)
  current={(canon(tri),sid,start,end,ic,sg,eg) for tri,bx,sid,start,end,ic,sg,eg in rep.bcs}
  require(independent==current,'supported boundary dictionaries disagree')
  # Validate the entire truth control independently by exact clipping.
  pair_tests=0;clips=0
  for tr in tiles:
   require(all(inside_convex(target,x) for x in tr),'truth containment')
   require(sorted(norm(sub(a,b),D) for a,b in zip(tr,tr[1:]+tr[:1]))==sorted(x*x for x in rep.sides),'truth metric')
  for a,b in combinations(tiles,2):
   pair_tests+=1
   if boxes_overlap(box(a),box(b)):
    clips+=1;require(intersect_area2(a,b)==0,'truth overlap')
  require(sum(signed2(t) for t in tiles)==signed2(target),'truth area')
  paths=true_side_paths(rep,tiles)
  gamma_points={tr[i] for tr in tiles for i in range(3) if norm(sub(tr[(i+1)%3],tr[(i+2)%3]),D)==max(rep.sides)**2}
  for sid,path in enumerate(paths):
   supported_marks={tr[i] for lo,hi,tr,a0,b0 in path for i in range(3) if tr[i] in (a0,b0) and norm(sub(tr[(i+1)%3],tr[(i+2)%3]),D)==max(rep.sides)**2}
   for lo,hi,tr,a0,b0 in path:
    if hi-lo!=max(rep.sides):continue
    proper_block=lambda x:x in target or x in supported_marks
    wrong_block=lambda x:x in target or x in gamma_points
    require(not(proper_block(a0) and proper_block(b0)), 'blocked-c lemma contradicted by truth control')
    if wrong_block(a0) and wrong_block(b0):
     witness={'u':u,'v':v,'m':m,'beta':beta,'side_index':sid,'c_edge':[[str(q) for q in z] for z in (a0,b0)],'correct_blocked':[proper_block(a0),proper_block(b0)],'incorrect_blocked':[True,True]}
     bad_mark_witnesses.append(witness)
     if len(bad_mark_witnesses)==1:
      w=dict(witness,data=data,triangles=[[[str(q) for q in z] for z in t0] for t0 in tiles],scope='Counterexample to marking every touching gamma vertex, NOT to the actual supported-edge lemma')
      (ROOT/'results'/'wrong_mark_counterexample.json').write_text(json.dumps(w,indent=2)+'\n')
  for sidepath in paths:
   # Find a gamma vertex that merely touches an exterior side, not a supported edge.
   spoints={x for lo,hi,tr,a,b in sidepath for x in (a,b)}
   supported_tiles={r[2] for r in sidepath}
   for tr in tiles:
    if tr in supported_tiles:continue
    for i,x in enumerate(tr):
     if x in spoints and norm(sub(tr[(i+1)%3],tr[(i+2)%3]),D)==max(rep.sides)**2:
      non_supported_gamma.append({'u':u,'v':v,'m':m,'beta':beta,'point':[str(z) for z in x]})
  control_sectors=0;partials=0
  for attempt in range(16):
   ix=rng.sample(range(len(tiles)),rng.randrange(len(tiles)))
   placed=[tiles[i] for i in ix];unplaced=[tiles[i] for i in range(len(tiles)) if i not in ix]
   atoms=residual_atoms(target,placed);secs=sectors(atoms)
   # all sectors on the two smallest controls; deterministic capped sample on larger controls
   if len(secs)>9:secs=rng.sample(secs,9)
   rep.placed=list(placed);rep.boxes=[old.bounds(t) for t in placed]
   for sec in secs:
    srow={'x':[str(z) for z in sec[0]],'d':[str(z) for z in sec[1]],'e':[str(z) for z in sec[2]]}
    old.check_sector(rep.target,rep.placed,srow)
    choices=independent_choices(sec,target,placed,rep.sides,D)
    old_choices={canon(t) for t in rep.possible(sec)}
    require(choices==old_choices,'corner enumerators disagree')
    completions=set(unplaced)&choices
    require(completions,'all true completions lost')
    p0,d,e=sec
    atom=next((sub(q,p0) for p,q in atoms if p==p0 and is_same_ray(sub(q,p0),d)),None)
    if atom is not None:
     for tr in completions:
      for x in tr:
       dx=sub(x,p0)
       if dx!=(0,0) and is_same_ray(dx,d) and norm(dx,D)>norm(atom,D):
        overruns.append({'u':u,'v':v,'m':m,'beta':beta,'x':[str(z) for z in p0],'atom_length':str(rt(norm(atom,D))),'full_edge_length':str(rt(norm(dx,D)))})
    control_sectors+=1
   partials+=1
  # independent whole-word oracle for small target dictionaries
  if len(tiles)<=44:
   rep.placed=[];rep.boxes=[]
   for trial in range(12):
    bans=[int(rng.random()<(.0 if trial==0 else .14+trial*.02)) for _ in rep.bcs];rep.ban=bans
    direct,count=brute_paths(rep,bans);require(rep.boundary_possible()==direct,'boundary automaton mismatch');dp_trials+=1;full_words+=count
  reports.append({'N':len(tiles),'family':data['branch'],'transformed':True,'reflected':refl,'supported_dictionary_entries':len(independent),'all_pairs_considered':pair_tests,'positive_AABB_pairs_clipped':clips,'partial_placements':partials,'convex_sectors_checked':control_sectors})
  total_sectors+=control_sectors;total_pairs+=pair_tests
 # Formal-angle inventory exhaust: avoid floating comparisons of irrational angles.
 inventories={}
 # Multiply coefficients of pi,alpha by 2 in Group 1.
 alpha=(0,2);beta=(1,-3);gamma=(1,1)
 for label,target_coeff in [('alpha',alpha),('beta',beta),('theta',(1,-1)),('2alpha',(0,4)),('3alpha',(0,6)),('flat',(2,0))]:
  sol=[]
  for na in range(8):
   for nb in range(8):
    for ng in range(8):
     if (nb+ng,2*na-3*nb+ng)==target_coeff:sol.append([na,nb,ng])
  inventories[label]=sol
 require(inventories['flat']==[[1,1,1],[3,2,0]],'flat inventory')
 require(overruns,'no actual T-overrun control reached')
 report={'status':'PASS','positive_controls':reports,'full_pairs_considered':total_pairs,'convex_sectors_checked':total_sectors,'exact_counterparts_survived_all_sectors':True,'actual_full_edge_overrun_witnesses':len(overruns),'first_overruns':overruns[:5],'wrong_mark_rule_rejects_true_c_edges':len(bad_mark_witnesses),'first_wrong_mark_witness':bad_mark_witnesses[0] if bad_mark_witnesses else None,'non_supported_gamma_contacts_found':len(non_supported_gamma),'gamma_examples':non_supported_gamma[:3],'boundary_DP_trials':dp_trials,'complete_words_examined_by_separate_oracle':full_words,'group1_exact_angle_inventories':inventories,'seconds':round(time.monotonic()-start,3),'scope':'finite regression and soundness audit, not verification of every possible tiling'}
 (ROOT/'results'/'boundary_foundations.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
