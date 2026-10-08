#!/usr/bin/env python3
"""Replay complete finite signed-direction checks for bands of 8--12 heights."""
import json
from collections import Counter
from pathlib import Path
from directional_dp_probe import run_variable

def replay(r):
    current=Counter();count=0
    for block in r['witness']:
        h=block['h'];n=block['n'];pop=[0]*12
        for t,key in enumerate(['A','B']):
            for j,x in enumerate(block[key]):pop[6*t+j+(3 if x<0 else 0)]=abs(x)
        extra=n-sum(pop)
        assert extra>=0 and extra%2==0 and n>0 and n%13==(11 if h==0 else 0)
        pop[0]+=extra//2;pop[3]+=extra//2
        for t,(x,y) in enumerate([(8,7),(7,8)]):
            for j in range(6):
                k=pop[6*t+j]
                edges=[(h,j,x),(h-1,j+3,13),(h,j+5,y)] if t==0 else [(h,j,x),(h+1,j+2,13),(h,j+5,y)]
                for eh,ej,le in edges:
                    ej%=6;current[eh,ej%3]+=(1 if ej<3 else -1)*k*le
        count+=sum(pop)
    assert {key:v for key,v in current.items() if v}=={(0,0):154,(1,2):91,(-1,1):-91}
    assert count==154

def main():
    records=[]
    for K in [12,11,10,9,8]:
        rows=[]
        for L in range(1-K,1):
            r=run_variable(L,L+K-1,seconds=300)
            assert r['status']==('EXACT_FORMAL_FEASIBLE' if K==8 else 'EXACT_UNSAT')
            if K==8:replay(r)
            rows.append(r)
        records.extend(rows)
        print(json.dumps({'height_count':K,'checked_supports':len(rows),'status':'PASS'}),flush=True)
    report={'status':'PASS','scope':'Complete signed-direction inventory; no geometric sufficiency','full_Erdos634_solved':False,'case154_solved':False,'excluded_supports':42,'positive_formal_controls':8,'records':records}
    Path(__file__).with_name('directional_supports_verified.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':
    if not __debug__:raise RuntimeError('Run without -O so exact replay assertions execute.')
    main()
