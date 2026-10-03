#!/usr/bin/env python3
"""Independent exact macro checks for the F2 and F3 corner-core transfers."""
from fractions import Fraction as F
from math import gcd,isqrt
from pathlib import Path
import json
from verify_reversed import area2,det,clip,sides2
ROOT=Path(__file__).resolve().parent

def add(p,q):return(p[0]+q[0],p[1]+q[1])
def sub(p,q):return(p[0]-q[0],p[1]-q[1])
def scale(s,p):return(s*p[0],s*p[1])
def mul(p,q):return(p[0]*q[0]-p[1]*q[1],p[0]*q[1]+p[1]*q[0]+p[1]*q[1])
def conj(p):return(p[0]+p[1],-p[1])
def ccw(p):return p if area2(p)>0 else p[::-1]

def partition(target,regions):
 target=ccw(target);regions=[ccw(p)for p in regions]
 assert all(all(det(target[j],target[(j+1)%3],p)>=0 for j in range(3)for p in reg)for reg in regions)
 assert sum(area2(p)for p in regions)==area2(target)
 for i,p in enumerate(regions):
  for q in regions[:i]:
   # Only one region can have four vertices.
   section=clip(p,q) if len(q)==3 else clip(q,p)
   assert len(section)<3 or area2(section)==0

def check(a,b,c,m):
 S=c*c;h=a+2*b;k=2*a+b;t=a-b;Z=(F(a),F(b));Z2=mul(Z,Z)
 X=(F(0),F(0));Y=(F(m*S),F(0));I=scale(m*a,Z);J=scale(m,Z2);T=scale(F(m*a*h,S),Z2)
 corner=[(F(m*a*t),F(0)),(F(m*S),F(0)),(F(m*a*a),F(m*a*b)),(F(m*a*t),F(m*b*t))]
 v2=(F(b*k,S),F(-a*h,S))
 reflected=[add(Y,mul(v2,conj(sub(p,Y))))for p in corner]
 assert reflected==[T,Y,I,J]
 core=[Y,I,J,T]
 assert abs(area2(core))==3*a*a*b*b*m*m
 assert sides2([X,Y,I])==sorted([(m*a*c)**2,(m*b*c)**2,(m*S)**2])
 assert sides2([X,I,J])==sorted([(m*a*c)**2,(m*b*c)**2,(m*S)**2])
 assert sides2([X,Y,T])==sorted([(m*a*h)**2,(m*b*k)**2,(m*S)**2])
 partition([X,Y,T],[core,[X,Y,I],[X,I,J]])
 K=scale(F(m*h,S),mul(Z2,Z))
 assert sub(K,T)==scale(F(h,k),sub(T,Y))
 assert sides2([X,T,K])==sorted([(m*a*h)**2,(m*b*h)**2,(m*c*h)**2])
 assert sides2([X,Y,K])==sorted([(m*S)**2,(m*c*h)**2,(3*m*b*(a+b))**2])
 partition([X,Y,K],[core,[X,Y,I],[X,I,J],[X,T,K]])
 return {'tile':[a,b,c],'multiplier':m,'F2_count':h*k*m*m,'F3_count':3*h*(a+b)*m*m}

def main():
 cases=[]
 for a in range(2,401):
  for b in range(1,a):
   if gcd(a,b)!=1:continue
   c=isqrt(a*a+a*b+b*b)
   if c*c!=a*a+a*b+b*b:continue
   for m in (1,2):cases.append(check(a,b,c,m))
 report={'status':'PASS','scope':'Exact macro partition, Q reflection, target sides and counts for F2/F3; no claim the Q is tiled at m1','primitive_triples':len(cases)//2,'instances':len(cases),'arithmetic':'exact rational','examples':[case for case in cases if case['tile']==[8,7,13]],'full_Erdos634_solved':False}
 (ROOT/'target_bridges_verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
