#!/usr/bin/env python3
"""Independently check the surviving four-tile bitmap control using integer geometry."""
import argparse,json,math
from pathlib import Path

def add(a,b):return(a[0]+b[0],a[1]+b[1])
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def mul(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]+a[1]*b[1])
def scale(a,n):return(a[0]*n,a[1]*n)
def rot(a):return(-a[1],a[0]+a[1])
def power(a,n):
 r=(1,0)
 for _ in range(n):r=mul(r,a)
 return r

def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def norm(a):return a[0]**2+a[0]*a[1]+a[1]**2

def currents(triangles):
 result={}
 for t in triangles:
  for a,b in zip(t,t[1:]+t[:1]):
   v=sub(b,a);g=math.gcd(*v);d=(v[0]//g,v[1]//g)
   if d<(0,0):d=scale(d,-1)
   for p,s in [(a,1),(b,-1)]:
    key=(d,p);result[key]=result.get(key,0)+s
 return {k:v for k,v in result.items() if v}

def run(prefix):
 report=json.loads(Path(str(prefix)+'.json').read_text());assert not report['conflict'] and not report['incomplete'];L,U=report['L'],report['U'];r=report.get('basis_rotation',0);m=report['control_scale'];assert m==2
 transform=mul(power((3,1),-L),power((4,-1),U))
 for _ in range(r):transform=rot(transform)
 target=[(0,0),scale(transform,8*m),scale(rot(rot(transform)),7*m)]
 templates=[]
 for h in range(L,U+1):
  u=mul(power((3,1),h-L),power((4,-1),U-h))
  for _ in range(r):u=rot(u)
  for order in range(2):
   a=scale(u,7 if order else 8);b=scale(rot(rot(u)),8 if order else 7)
   for rotation in range(6):templates.append([(0,0),a,b]);a=rot(a);b=rot(b)
 lines=Path(str(prefix)+'.remaining.txt').read_text().splitlines();assert list(map(int,lines[0].split()))==[L,U,4]
 triangles=[]
 for line in lines[1:]:
  o,x,y=map(int,line.split());triangles.append([add((x,y),v) for v in templates[o]])
 assert len(triangles)==4
 q=13**(U-L);area=0
 for t in triangles:
  assert sorted(norm(sub(t[i],t[(i+1)%3])) for i in range(3))==[49*q,64*q,169*q]
  det=cross(sub(t[1],t[0]),sub(t[2],t[0]));assert det==56*q;area+=det
  for p in t:
   assert all(cross(sub(target[(k+1)%3],target[k]),sub(p,target[k]))>=0 for k in range(3))
 pairs=0
 for i,a in enumerate(triangles):
  for b in triangles[i+1:]:
   assert any(all(cross(sub(t[(k+1)%3],t[k]),sub(p,t[k]))<=0 for p in u) for t,u in [(a,b),(b,a)] for k in range(3));pairs+=1
 assert area==cross(sub(target[1],target[0]),sub(target[2],target[0]))
 assert currents(triangles)==currents([target])
 assert currents(triangles[:-1])!=currents([target])
 assert currents(triangles+[triangles[0]])!=currents([target])
 return {'status':'EXACT_PASS','tile_count':4,'band':[L,U],'basis_rotation':r,'pair_checks':pairs,'boundary_current':'PASS','reject_missing_tile':True,'reject_duplicate_tile':True}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('prefix',type=Path);p.add_argument('--output',type=Path);a=p.parse_args();j=run(a.prefix);s=json.dumps(j,indent=2)+'\n';print(s,end='')
 if a.output:a.output.write_text(s)
