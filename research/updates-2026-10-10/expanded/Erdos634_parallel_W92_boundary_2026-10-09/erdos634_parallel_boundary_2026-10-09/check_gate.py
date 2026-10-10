#!/usr/bin/env python3
"""Independent finite all-row arithmetic overlist for the small counts 14,56.
The exhaustion theorem is a stated external/project classification input.
The program does not assert tiling existence from an arithmetic candidate.
"""
from math import gcd,isqrt
import json
from pathlib import Path

def sq(n):return n>=0 and isqrt(n)**2==n
def heron(t):
 a,b,c=t;return (a+b+c)*(-a+b+c)*(a-b+c)*(a+b-c)
def gate(N):
 classical=[]
 for k in [1,2,3,6]:
  if N%k==0 and sq(N//k):classical.append([k,isqrt(N//k)])
 for a in range(1,isqrt(N)+1):
  if sq(N-a*a):classical.append(['sum_two_squares',a,isqrt(N-a*a)])
 rows={}
 def add(branch,tile,target,D,params):
  if D<=0 or N%D or not sq(N//D):return
  m=isqrt(N//D);target=tuple(m*x for x in target)
  if min(tile+target)<=0:raise ValueError('nonpositive')
  if gcd(gcd(tile[0],tile[1]),tile[2])!=1:raise ValueError('nonprimitive')
  if heron(target)!=N*N*heron(tile) or heron(tile)<=0:raise ValueError('area')
  r={'branch':branch,'tile':tile,'target':target,'scale':m,'parameters':params}
  rows[(branch,tuple(sorted(tile)),tuple(sorted(target)))]=r
 # This bound is deliberately elementary rather than the source code's divisor gate.
 # For theta/double-angle D=v²-u²>=2v-1; every other Group1 D>v².
 for v in range(2,N+1):
  for u in range(1,v):
   if gcd(u,v)!=1:continue
   a=u*v;b=v*v-u*u;c=v*v;Q=2*v*v-u*u;P=3*v*v-u*u;tile=(a,b,c)
   add('W',tile,(v**3,u*Q,v*b),Q,(u,v))
   add('beta',tile,(v**3,v**3,u*P),P,(u,v))
   add('theta',tile,(b*v,b*v,b*u),b,(u,v))
   add('alpha',tile,(b*c,b*c,b*Q),b*Q,(u,v))
   add('QP',tile,(c*c,c*Q,b*P),Q*P,(u,v))
   if v<2*u:add('double-angle',(u*u,b,u*v),(b*u,b*u,b*v),b,(u,v))
 # All seven norm row coefficients are at least max(a,b).
 for a in range(1,N+1):
  for b in range(1,N+1):
   if gcd(a,b)!=1:continue
   if sq(a*a-a*b+b*b):
    c=isqrt(a*a-a*b+b*b);add('E60',(a,b,c),(a*b,)*3,a*b,(a,b))
   if not sq(a*a+a*b+b*b):continue
   c=isqrt(a*a+a*b+b*b);tile=(a,b,c)
   add('E120',tile,(a*b,)*3,a*b,(a,b))
   add('F1',tile,(a*b,b*c,b*(a+b)),b*(a+b),(a,b))
   add('I120',tile,(b*c,b*c,b*(a+2*b)),b*(a+2*b),(a,b))
   add('F2',tile,(a*(a+2*b),b*(2*a+b),c*c),(a+2*b)*(2*a+b),(a,b))
   add('F3',tile,(c*c,c*(a+2*b),3*b*(a+b)),3*(a+b)*(a+2*b),(a,b))
   add('F4',tile,(a*c,b*(2*a+b),c*(a+b)),(2*a+b)*(a+b),(a,b))
 full=sorted(rows.values(),key=lambda r:(r['branch'],r['tile']))
 remaining=[r for r in full if not(r['branch'] in ('theta','double-angle') and r['scale']==1)]
 return {'N':N,'classical_witnesses':classical,'all_candidates':full,'after_proved_scale_one_isosceles_exclusions':remaining}
if __name__=='__main__':
 rows=[gate(N) for N in [14,56]]
 assert not any(r['classical_witnesses'] for r in rows)
 assert [(r['branch'],r['scale'],sorted(r['tile'])) for r in rows[0]['after_proved_scale_one_isosceles_exclusions']]==[('W',1,[5,6,9])]
 assert {(r['branch'],r['scale'],tuple(sorted(r['tile']))) for r in rows[1]['after_proved_scale_one_isosceles_exclusions']}=={('W',2,(5,6,9)),('E120',1,(7,8,13))}
 out={'status':'PASS','classification_is_external_input':True,'counts':rows}
 Path(__file__).with_name('gate_report.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
