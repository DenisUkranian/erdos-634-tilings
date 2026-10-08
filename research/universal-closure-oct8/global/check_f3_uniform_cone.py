#!/usr/bin/env python3
"""Complete exact arithmetic proof certificate for the sharp new F3 cone."""
from pathlib import Path
from math import gcd
from fractions import Fraction as Q
import json

def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def main():
 A,B,C=2725,1139,3439
 need(C*C==A*A+A*B+B*B,'endpoint norm')
 need(Q(A,B)<Q(12,5)and Q(C,B)<Q(31,10),'ratio upper bounds')
 need(1+2*Q(A,B)-Q(A,B)**2==Q(79246,1297321)>Q(3,50),'quadratic lower bound')
 need(Q(121,48)<Q(64,25)and Q(289,145)<Q(64,25),'parameter bounds')
 need(9-Q(31,1500)>Q(44,5),'large-size threshold')
 records=[];seen=set();failures=[]
 for p in range(2,240):
  for q in range(1,p):
   if gcd(p,q)!=1 or(p-q)%3==0:continue
   a0=p*p-q*q;b0=q*(2*p+q);c=p*p+p*q+q*q;a,b=max(a0,b0),min(a0,b0)
   if not(2*b<a and 1139*a<=2725*b and b<22500):continue
   need(c*c==a*a+a*b+b*b and gcd(a,b)==1,'norm/primitivity')
   need((a,b,c)not in seen,'duplicate tile');seen.add((a,b,c));d=b*b+2*a*b-a*a-c
   j=d*pow(b0,-1,a0)%a0;k=0
   while j>=p or k>=p or(j>=p-q and k>=p-q):
    old=j*b0+k*c
    if j>=p:j-=p;k+=q
    elif k>=p:k-=p;j+=q
    else:j-=p-q;k-=p-q
    new=j*b0+k*c;need(0<=new<old and(old-new)%a0==0,'Apéry reduction invalid')
   weight=j*b0+k*c;need((weight-d)%a0==0,'wrong residue')
   if weight>d:
    failures.append(dict(p=p,q=q,tile=[a,b,c],D_minus_c=d,apery_pair=[j,k],apery_weight=weight));continue
   i=(d-weight)//a0
   if a0!=a:i,j=j,i
   need(min(i,j,k)>=0 and i*a+j*b+k*c==d,'direct semigroup witness fails')
   need(1139*a<2725*b,'unexpected successful endpoint')
   records.append(dict(p=p,q=q,tile=[a,b,c],D_minus_c=d,coefficients=[i,j,k]))
 need(len(records)==710 and len(failures)==1,'finite coverage differs')
 endpoint=failures[0];need(endpoint==dict(p=42,q=25,tile=[A,B,C],D_minus_c=75807,apery_pair=[34,11],apery_weight=130479),'unexpected failure')
 representatives=[(j,k,j*A+k*C)for j in range(42)for k in range(42)if not(j>=17 and k>=17)and(j*A+k*C-75807)%B==0]
 need(representatives==[(34,11,130479)],'endpoint Apéry residue not unique')
 out=dict(status='PASS',theorem='D belongs to c+<a,b,c> for every primitive2<a/b<2725/1139',large_b_threshold=22500,complete_p_range=[2,239],finite_closed_cone_cases=len(seen),successful_strict_cone_cases=len(records),endpoint_failure=endpoint,records=records)
 Path(__file__).with_name('f3_uniform_cone_verified.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(status='PASS',complete_p_range=[2,239],finite_closed_cone_cases=len(seen),successful_strict_cone_cases=len(records),endpoint_failure=endpoint)))
if __name__=='__main__':main()
