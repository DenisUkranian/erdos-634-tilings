#!/usr/bin/env python3
"""Recover and independently verify exact rational first-moment witnesses."""
from fractions import Fraction as F
from pathlib import Path
import json
from moment_lp import build,cross,sub,add


def recover(source,output):
    raw=json.loads(Path(source).read_text());a,b,c,low,high=raw['parameters'];types,target,N,eq,rhs,ub,ubr,labels=build(a,b,c,low,high)
    xx=raw['x'];chosen=[i for i in range(len(types)) if xx[3*i]>1e-6];counts={i:round(xx[3*i]) for i in chosen}
    assert all(abs(xx[3*i]-counts[i])<1e-7 for i in chosen)
    columns=[3*i+k for i in chosen for k in (1,2)]
    basis={}
    def insert(row,value):
        row=list(row)+[value]
        for pivot,brow in sorted(basis.items()):
            if row[pivot]:
                f=row[pivot];row=[x-f*y for x,y in zip(row,brow)]
        piv=next((k for k,v in enumerate(row[:-1]) if v),None)
        if piv is None:
            assert row[-1]==0
            return False
        f=row[piv];row=[x/f for x in row]
        for pivot,brow in list(basis.items()):
            if brow[piv]:
                f=brow[piv];basis[pivot]=[x-f*y for x,y in zip(brow,row)]
        basis[piv]=row
        return True
    for row,v in zip(eq,rhs):
        insert([row[k] for k in columns],v-sum(row[3*i]*n for i,n in counts.items()))
    candidates=sorted(range(len(ub)),key=lambda i:abs(sum(float(v)*q for v,q in zip(ub[i],xx))))
    for r in candidates:
        row=[ub[r][k] for k in columns]
        if not any(row):continue
        reduced=list(row)
        for pivot,brow in sorted(basis.items()):
            if reduced[pivot]:
                f=reduced[pivot];reduced=[x-f*y for x,y in zip(reduced,brow)]
        if any(reduced):
            insert(row,-sum(ub[r][3*i]*n for i,n in counts.items()))
            if len(basis)==len(columns):break
    assert len(basis)==len(columns)
    solution=[basis[k][-1] for k in range(len(columns))]
    exact=[F(0)]*len(xx)
    for i,n in counts.items():exact[3*i]=F(n)
    for j,k in enumerate(columns):exact[k]=F(solution[j])
    assert all(sum(v*q for v,q in zip(row,exact))==r for row,r in zip(eq,rhs))
    assert all(sum(v*q for v,q in zip(row,exact))<=r for row,r in zip(ub,ubr))
    out={'statement':'Integer multiplicities and individually contained translated triangles satisfy every directed-edge zeroth and first moment. Overlaps are allowed; this is not a tiling.','parameters':[a,b,c],'target':[[str(v) for v in p] for p in target],'count':N,'types':[]}
    for i in chosen:
        t=types[i];n=counts[i];translation=[exact[3*i+k]/n for k in (1,2)]
        out['types'].append({'height':t['height'],'rotation':t['rotation'],'chirality':t['chirality'],'multiplicity':n,'translation':[str(v) for v in translation]})
    Path(output).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':'EXACT_PASS','types':len(chosen),'count':N,'equalities':len(eq),'containment_inequalities':len(ub)},sort_keys=True))


def verify(source):
    data=json.loads(Path(source).read_text());a,b,c=data['parameters'];low=min(t['height'] for t in data['types']);high=max(t['height'] for t in data['types']);types,target,N,eq,rhs,ub,ubr,labels=build(a,b,c,low,high)
    idx={(t['height'],t['rotation'],t['chirality']):i for i,t in enumerate(types)}
    exact=[F(0)]*(3*len(types));heights={}
    for t in data['types']:
        i=idx[(t['height'],t['rotation'],t['chirality'])];n=t['multiplicity'];assert isinstance(n,int) and n>0;exact[3*i]=F(n)
        exact[3*i+1]=n*F(t['translation'][0]);exact[3*i+2]=n*F(t['translation'][1]);heights[t['height']]=heights.get(t['height'],0)+n
    assert sum(heights.values())==N==data['count']
    assert all(sum(v*q for v,q in zip(row,exact))==r for row,r in zip(eq,rhs))
    assert all(sum(v*q for v,q in zip(row,exact))<=r for row,r in zip(ub,ubr))
    assert all(n%c==0 for h,n in heights.items() if h!=2)
    print(json.dumps({'status':'EXACT_PASS','count':N,'height_populations':heights,'distinct_placements':len(data['types']),'note':'Repeated identical placements overlap; this is only a moment relaxation witness.'},sort_keys=True))

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('--recover-to');v=p.parse_args()
    if v.recover_to:recover(v.source,v.recover_to)
    else:verify(v.source)
