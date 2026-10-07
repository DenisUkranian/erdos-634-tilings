#!/usr/bin/env python3
"""Recheck the exact theta-base C>=2 count criterion; no tiling sufficiency."""
from math import gcd
from pathlib import Path
import argparse,json

def run(max_v=25,max_scale=20):
    checks=0
    for v in range(2,max_v+1):
        for u in range(1,v):
            if gcd(u,v)>1:continue
            a=u*v;b=v*v-u*u;c=v*v
            for t in range(1,max_scale+1):
                L=u*t*b;q=u*t//v;K=b*q-2*v
                criterion=K>=0 and any((K-A*u)%v==0 for A in range(K//u+1))
                simplified=q >= (2 if v-u==1 else 1)
                direct=any((L-B*b-C*c)>=0 and (L-B*b-C*c)%a==0
                    for C in range(2,L//c+1) for B in range((L-C*c)//b+1))
                if criterion!=direct or simplified!=direct:
                    raise AssertionError((u,v,t,criterion,direct,simplified))
                checks+=1
    return {'status':'PASS','primitive_v_at_most':max_v,'scales':list(range(1,max_scale+1)),
            'exact_count_equivalences':checks,'checks_simplified_threshold':True,
            'scope':'Arithmetic boundary counts only; no tiling sufficiency','full_Erdos634_solved':False}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);args=ap.parse_args()
    report=json.dumps(run(),indent=2)+'\n'
    if args.output:args.output.write_text(report)
    print(report,end='')
