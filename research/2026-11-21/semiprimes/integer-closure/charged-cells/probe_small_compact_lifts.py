#!/usr/bin/env python3
"""Finite exploratory search for compact c=7 lifts, never an exclusion proof."""
from collections import Counter,defaultdict
from fractions import Fraction
import argparse
import itertools
import json
from pathlib import Path
import random
import sys

from verify_charged_countercontrols import U,separated,check
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'long-banks'))
from long_bank_completion import complete_bank

ORIENT=[(0,1),(2,1),(4,1),(4,1),(5,1),(2,1),(2,1),
        (4,-1),(4,1),(1,-1),(1,1),(2,1),(2,1)]


def support(v):
    t,h,i,w,vv,r,s=v
    T,H,I,W,V,R,S=7*t,5+7*h,4+7*i,2+7*w,1+7*vv,4+7*r,5+7*s
    q=[(0,0),(T,0),(0,T),(0,H),(I-W,W),(I,0),(H-V,V),
       (R,V),(R,H-R),(S,0),(S,H-S),(H,0),(T-W,W)]
    return [(*p,j,s) for p,(j,s) in zip(q,ORIENT)]


def polygons(su):
    return [[(x,y),(x-5*U[j][0],y-5*U[j][1]),
             (x+3*U[(j+s)%6][0],y+3*U[(j+s)%6][1])] for x,y,j,s in su]


def bank_capacity(su):
    events=defaultdict(Counter)
    for x,y,j,s in su:
        u=x-5*U[j][0],y-5*U[j][1];w=x+3*U[(j+s)%6][0],y+3*U[(j+s)%6][1]
        for ax,p,v in ((j,(x,y),s),(j,u,-s),(j+s,w,s),(j+s,(x,y),-s)):
            ax%=3;tr=(p[1],p[0],sum(p))[ax];lg=p[0] if ax==0 else p[1]
            events[(ax,tr)][lg]+=v
    failure=0;segments=0
    for line,ev in events.items():
        byres=defaultdict(Counter)
        for t,v in ev.items():
            if v:byres[t%7][t//7]+=v
        starts=defaultdict(list)
        for res,es in byres.items():
            assert sum(es.values())==0
            k=0
            for n in range(min(es),max(es)+1):
                k+=es[n]
                if k:
                    segments+=abs(k)
                    failure+=abs(k)>1
                    starts[k>0].append(7*n+res)
        for ss in starts.values():
            ss.sort()
            failure+=sum(t-s<7 for s,t in zip(ss,ss[1:]))
    return failure,segments


def run(samples,span):
    rng=random.Random(634)
    stats=Counter();best=None;best_report=None;capacity_pass_reports=[]
    candidates=itertools.chain(
        ((0,h,i,w,0,h,s) for h,i,w,s in itertools.product(range(-span,span+1),repeat=4)),
        (tuple(rng.randint(-span,span) for _ in range(7)) for _ in range(samples)))
    for v in candidates:
        stats['candidates']+=1;su=support(v);ps=polygons(su)
        if any(not separated(p,q) for k,p in enumerate(ps) for q in ps[:k]):
            stats['odd_overlap']+=1;continue
        stats['nonoverlapping']+=1
        conflicts,count=bank_capacity(su)
        key=(conflicts,count)
        if best is None or key<best:
            best=key;best_report={'parameters':list(v),'support':[list(x) for x in su],
                'bank_capacity_conflicts':conflicts,'long_segment_multiplicity':count}
        if conflicts:stats['capacity_failure']+=1;continue
        stats['capacity_pass']+=1
        report=complete_bank(ps,5,3,7)
        capacity_pass_reports.append({'parameters':list(v),'support':[list(x) for x in su],
                                      'complete_bank_report':report})
        if key==best and best_report['parameters']==list(v):
            best_report['complete_bank_report']=report
        print(json.dumps({'capacity_pass_parameters':v,'report':report}),flush=True)
        if report.get('status')=='compatible_mandatory_bank':
            check(5,3,7,su)
            break
    return {'statistics':dict(stats),'best':best_report,'capacity_pass_reports':capacity_pass_reports,
        'random_samples':samples,'span':span,
        'scope':'Finite selected lift search; absence is not an impossibility proof.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--samples',type=int,default=10000)
    p.add_argument('--span',type=int,default=3);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();o=run(a.samples,a.span);a.out.write_text(json.dumps(o,indent=2,default=str)+'\n')
    print(json.dumps(o,indent=2,default=str))
