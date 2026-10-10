#!/usr/bin/env python3
"""Replay only necessary root-boundary support eliminations, NOT an UNSAT tree.

The geometric inputs are the two-c adjacency lemma and the exhaustive ccaa
root split for adjacent W parameters at scale two. Interior searches remain
INCOMPLETE and are never accepted as full nonexistence certificates here.
"""
from pathlib import Path
from fractions import Fraction as Q
import json,sys,time
from verify_base import Replay,point,ccw,edges,norm,sub,mul,add,det,rt,need

class SupportReplay(Replay):
 def make_roots(self,kind,k):
  need(kind=='W_adjacent_two' and self.fam=='W','root kind')
  need(self.m==2 and self.u==self.v-1 and self.v>=3 and k in (0,1),'root domain')
  u,v,m=self.u,self.v,self.m;a,b,c=self.sides
  alpha2=theta=None
  for j,p in enumerate(self.target):
   op=rt(norm(sub(self.target[(j+1)%3],self.target[(j+2)%3]),self.D))
   if op==m*u*(2*v*v-u*u):alpha2=p
   if op==m*v**3:theta=p
  need(alpha2 is not None and theta is not None,'corner labels')
  length=rt(norm(sub(theta,alpha2),self.D));axis=mul(1/length,sub(theta,alpha2))
  third=next(p for p in self.target if p not in (alpha2,theta))
  sign=1 if det(sub(theta,alpha2),sub(third,alpha2))>0 else -1
  roots=[];pos=0
  for s,r,opp in [(c,b,a),(c,b,a) if k==0 else (c,a,b),(a,b,c),(a,b,c)]:
   proj=Q(s*s+r*r-opp*opp,2*s);h=rt(Q(r*r-proj*proj,self.D))
   perp=(-self.D*axis[1],axis[0])
   at=add(alpha2,mul(pos,axis));last=add(at,add(mul(proj,axis),mul(sign*h,perp)))
   roots.append(ccw((at,add(at,mul(s,axis)),last)));pos+=s
  need(pos==length,'boundary word length')
  # Check the unique inventory independently rather than only reading it.
  inventories=[]
  for C in range(2,int(length)//c+1):
   for B in range((int(length)-C*c)//b+1):
    R=int(length)-C*c-B*b
    if R%a==0:inventories.append((R//a,B,C))
  need(inventories==[(2,0,2)],'ccaa inventory is not unique')
  return roots

def check(path:Path,root:int):
 start=time.monotonic();data=json.loads(path.read_text())
 need((data['u'],data['v'],data['m'],data['branch'])==(3,4,2,'W'),'wrong experiment')
 need(data['status']=='INCOMPLETE','This file is expected to remain an incomplete interior search')
 r=SupportReplay(data,'W_adjacent_two',root)
 need(r.boundary_possible(),'root already fails original relaxation')
 for i,t in enumerate(data['root_filters']):
  tri=ccw(tuple(map(point,t)))
  matches=[k for k,b in enumerate(r.bcs) if b[0]==tri]
  need(matches and any(r.ban[k]==0 for k in matches),'not a surviving supported tile')
  r.push(tri)
  rejected=not r.boundary_possible()
  r.pop()
  need(rejected,'candidate has not been justified impossible')
  for k in matches:r.ban[k]+=1
  if (i+1)%100==0:print('replayed',i+1,'seconds',round(time.monotonic()-start,2),flush=True)
 report={'scope':'root-boundary candidate eliminations only', 'u':3,'v':4,'m':2,'branch':'W',
  'N':92,'root':root,'status':'PASS', 'initial_boundary_candidates':len(r.bcs),
  'certified_eliminated_supported_tiles':len(data['root_filters']),
  'boundary_candidates_not_banned_after_replay':sum(x==0 for x in r.ban),
  'original_sidewise_relaxation_still_feasible':r.boundary_possible(),
  'W92_tiling_or_nonexistence_proved':False,'full_problem_solved':False,
  'seconds':time.monotonic()-start}
 path.with_suffix('.support_verified.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2),flush=True)
 return report
if __name__=='__main__':check(Path(sys.argv[1]),int(sys.argv[2]))
