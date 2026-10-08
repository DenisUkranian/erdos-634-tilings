#!/usr/bin/env python3
'''Exact arithmetic reduction for all fifteen-square counts below the new tail.
No bounded geometric failure is promoted to global nonexistence.
'''
from dataclasses import asdict
from math import gcd,isqrt
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'research/uniform-reduction'))
from candidates import enumerate_candidates,classical,square_root,Instance

def independent(n):
    ans=set()
    def put(branch,tile,target,coefficient,tmin=1):
        if n%coefficient:return
        m=square_root(n//coefficient)
        if m is not None and m>=tmin:
            ans.add((branch,tuple(sorted(tile)),tuple(sorted(t*m for t in target))))
    for v in range(2,(n+1)//2+1):
      for u in range(1,v):
        if gcd(u,v)>1:continue
        b=v*v-u*u;a=u*v;c=v*v
        if b<=n:
          put('G1-theta',(a,b,c),(b*v,b*v,b*u),b,2)
          if v<2*u:put('double-angle',(u*u,b,u*v),(b*u,b*u,b*v),b,2)
        q=b+c;p=b+2*c
        if q<=n:
          put('G1-W',(a,b,c),(v**3,u*q,v*b),q)
          put('G1-beta',(a,b,c),(v**3,v**3,u*p),p)
          put('G1-alpha',(a,b,c),(b*c,b*c,b*q),b*q)
          put('G1-other-scalene',(a,b,c),(c*c,c*q,b*p),q*p)
    for a in range(1,n+1):
      for b in range(1,n+1):
        if gcd(a,b)>1:continue
        c=square_root(a*a+a*b+b*b)
        if c is not None:
          tile=(a,b,c)
          put('E120',tile,(a*b,)*3,a*b)
          put('F1-120',tile,(a*b,b*c,b*(a+b)),b*(a+b))
          put('I120',tile,(b*c,b*c,b*(a+2*b)),b*(a+2*b))
          put('F3-120',tile,(c*c,c*(a+2*b),3*b*(a+b)),3*(a+2*b)*(a+b))
          put('F4-120',tile,(a*c,b*(2*a+b),c*(a+b)),(2*a+b)*(a+b))
          put('F2-120',tile,(a*(a+2*b),b*(2*a+b),c*c),(a+2*b)*(2*a+b))
        c=square_root(a*a-a*b+b*b)
        if c is not None and min(a,b)>=2:
          put('E60',(a,b,c),(a*b,)*3,a*b)
    return ans

def two_c_representations(length,tile):
    a,b,c=tile
    return [(A,B,C) for C in range(2,length//c+1)
       for B in range((length-C*c)//b+1)
       for A in [(length-C*c-B*b)//a]
       if a*A+b*B+c*C==length]

def main():
    rows=[]
    for m in range(1,6):
      n=15*m*m
      if classical(n) is not None:raise AssertionError(('unexpected classical count',n))
      candidates=enumerate_candidates(n)
      keys={(z.branch,tuple(sorted(z.tile)),tuple(sorted(z.target))) for z in candidates}
      if keys!=independent(n):raise AssertionError(('independent sieve discrepancy',n))
      case=[]
      for z in candidates:
        obj=asdict(z);obj['status']='UNRESOLVED'
        if z.branch=='G1-theta':
          u,v=z.parameters;b=v*v-u*u
          if z.multiplier*b<u*v:
            obj.update(status='EXCLUDED',reason='theta long-seam bound',lhs=z.multiplier*b,rhs=u*v)
          elif not two_c_representations(z.target[2],z.tile):
            obj.update(status='EXCLUDED',reason='base cannot contain two whole longest edges',base=z.target[2])
        elif z.branch=='double-angle':
          u,v=z.parameters;b=v*v-u*u
          if z.multiplier*b<u*u:
            obj.update(status='EXCLUDED',reason='double-angle long-seam bound',lhs=z.multiplier*b,rhs=u*u)
        elif z.branch=='E120' and m==2:
          obj.update(status='EXCLUDED',reason='complete at-most-four-height theorem and independently replayed exhaustive position refutations; ../e60-position/PROOF.md')
        elif z.branch=='E120' and m>=4:
          obj.update(status='CONSTRUCTED',reason='independently verified E60 seed and explicit T(15m,15) stacking')
        elif z.branch=='E120' and m==1:
          if two_c_representations(15,z.tile):raise AssertionError('boundary exclusion failed')
          obj.update(status='EXCLUDED',reason='two-c boundary lemma; independently replayed full102-node proof')
        case.append(obj)
      rows.append(dict(m=m,N=n,status='YES' if any(c['status']=='CONSTRUCTED' for c in case) else 'NO' if all(c['status']=='EXCLUDED' for c in case) else 'UNRESOLVED',candidates=case))
    report=dict(verdict='PASS_EXACT_REDUCTION',square_class=15,positive_tail='m>=4, by the independently verified E60 construction and T(15m,15) stacking',cases=rows,remaining_counts=[r['N'] for r in rows if r['status']=='UNRESOLVED'],full_classification=False,dependencies=['Published exhaustive angular classification and rationality, as documented in uniform-reduction/PROOF.md','docs/long-seams-density.md Theorem1','docs/theta-branch.md Section2(two-longest-edge lemma)','final-closure-oct8/equilateral-search/cpsat_count/E60_0-1_certificate.json','final-closure-oct8/e60-position/PROOF.md'])
    dest=Path(__file__).with_name('arithmetic_reduction.json');dest.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='cases'},indent=2))
if __name__=='__main__':main()
