#!/usr/bin/env python3
"""Exact small balanced-cell exclusions and rigid six-tile cylinder controls.

The standard library and a C++17 compiler suffice. Discovery optimizers and
the original residual-search implementation are not imported.
"""
import argparse
from collections import Counter, defaultdict
from itertools import combinations
import json
from pathlib import Path
import subprocess
import tempfile

HERE=Path(__file__).resolve().parent
U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))
ORI=tuple((j,s) for j in range(6) for s in (-1,1))
POS=tuple(o for o in ORI if o[1]*(-1 if o[0]%2 else 1)==1)
NEG=tuple(((j+3)%6,s) for j,s in POS)
ABSENT=(2,4,8,10,14)

def det(p,q):return p[0]*q[1]-p[1]*q[0]
def minus(p,q):return p[0]-q[0],p[1]-q[1]
def norm(p):return p[0]*p[0]+p[0]*p[1]+p[1]*p[1]
def eps(label):return label[3]*(-1 if label[2]%2 else 1)

def vertices(a,b,label):
    x,y,j,s=label
    V=[(x,y),(x-a*U[j][0],y-a*U[j][1]),(x+b*U[(j+s)%6][0],y+b*U[(j+s)%6][1])]
    if det(minus(V[1],V[0]),minus(V[2],V[0]))<0:V[1],V[2]=V[2],V[1]
    return V

def endpoints(a,b,c,label,mode='torus'):
    V=vertices(a,b,label);out=Counter();lengths=[]
    for i in range(3):
        p,q=V[i],V[(i+1)%3];d=minus(q,p);lengths.append(norm(d))
        if norm(d)==c*c:continue
        assert norm(d) in (a*a,b*b)
        axis=next(j for j in range(3) if det(d,U[j])==0)
        def key(p):
            x,y=p
            if mode=='torus':return axis,x%c,y%c
            if mode=='physical':return axis,x,y
            if axis==0:return axis,y,x%c
            if axis==1:return axis,x,y%c
            return axis,x+y,y%c
        out[key(p)]-=1;out[key(q)]+=1
    assert sorted(lengths)==sorted((a*a,b*b,c*c))
    return {r:v for r,v in out.items() if v}

def moment_signature(a,b,c,ori):
    j,s=ori;D=[0,0,0];sign=s*(-1 if j%2 else 1)
    D[j%3]+=a*sign;D[(j+s)%3]-=b*sign
    return tuple(x%c for x in D)

def compositions(k):
    # Stars-and-bars implementation, independent of the recursive discovery.
    for bars in combinations(range(k+5),5):
        stops=(-1,)+bars+(k+5,)
        yield tuple(stops[i+1]-stops[i]-1 for i in range(6))

def transformed(label,rotation,reflection,c):
    x,y,j,s=label
    if reflection:x,y=x+y,-y;j,s=-j,-s
    for _ in range(rotation):x,y=-y,x+y
    return x%c,y%c,(j+rotation)%6,s

def coverage(a,b,c,n):
    signatures=[moment_signature(a,b,c,o) for o in POS]
    grouped=defaultdict(list)
    for vector in compositions(n//2):
        sigma=tuple(sum(vector[i]*signatures[i][r] for i in range(6))%c for r in range(3))
        grouped[sigma].append(vector)
    representatives=set();raw=0
    for vectors in grouped.values():
        for positive in vectors:
            for negative in vectors:
                raw+=1;D=dict(zip(POS,positive));D.update(zip(NEG,negative))
                orbit=[]
                for reflection in (False,True):
                    for rotation in range(6):
                        E={transformed((0,0,*o),rotation,reflection,c)[2:]:v for o,v in D.items()}
                        vector=tuple(E[o] for o in ORI)
                        assert sum(vector)==n
                        assert sum(v*s*(-1 if j%2 else 1) for v,(j,s) in zip(vector,ORI))==0
                        assert all(sum(v*moment_signature(a,b,c,o)[r] for v,o in zip(vector,ORI))%c==0 for r in range(3))
                        orbit.append(vector)
                representatives.add(min(orbit))
    return raw,sorted(representatives)

def verify_column_arithmetic(a,b,c):
    inv=pow(a-b,-1,c);checked=0
    def potential(row):
        axis,x,y=row
        return inv*(x if axis==0 else (-y if axis==1 else y))
    for x in range(c):
        for y in range(c):
            for j,s in ORI:
                label=x,y,j,s;C=endpoints(a,b,c,label)
                assert sum(v*potential(r) for r,v in C.items())%c==eps(label)%c
                moments=[]
                for axis in range(3):
                    def f(row):
                        i,xx,yy=row
                        return 0 if i!=axis else (xx if axis==0 else (-yy if axis==1 else yy))
                    moments.append(sum(v*f(r) for r,v in C.items())%c)
                assert tuple(moments)==moment_signature(a,b,c,(j,s))
                checked+=1
    # Check the dihedral generators on every orientation and nonzero anchors.
    for x,y in ((0,0),(1,2),(c-1,c-2)):
        for ori in ORI:
            label=x,y,*ori;C=endpoints(a,b,c,label)
            for rotation,reflection in ((1,False),(0,True)):
                D=Counter()
                for (axis,px,py),v in C.items():
                    xx,yy,_,_=transformed((px,py,0,1),rotation,reflection,c)
                    # A reflection reverses CCW boundary orientation.
                    newaxis=((-axis if reflection else axis)+rotation)%3
                    D[(newaxis,xx,yy)]+=(-v if reflection else v)
                expected=endpoints(a,b,c,transformed(label,rotation,reflection,c))
                assert {r:v for r,v in D.items() if v}==expected
    return checked

def rigid_six(a,b,c,center):
    L=2*c;x,y=center
    anchors=((-L,L),(0,L),(L,0),(L,-L),(0,-L),(-L,0))
    turns=((0,1),(0,-1),(4,1),(4,-1),(2,1),(2,-1))
    labels=[(x+u,y+v,j,s) for (u,v),(j,s) in zip(anchors,turns)]
    assert sum(eps(t) for t in labels)==0
    sums={mode:Counter() for mode in ('torus','cylinder','physical')}
    determinants=[];B=a*(a+2*b)
    for t in labels:
        for mode in sums:sums[mode].update(endpoints(a,b,c,t,mode))
        for xx,yy in vertices(a,b,t):
            determinants.extend((b*xx+(a+b)*yy,b*xx-a*yy,c*B-(a+b)*xx-b*yy))
    assert all(v==0 for v in sums['torus'].values())
    assert all(v==0 for v in sums['cylinder'].values())
    assert min(determinants)>0
    distances=[norm(minus(t[:2],u[:2])) for i,t in enumerate(labels) for u in labels[i+1:]]
    assert min(distances)==4*c*c>4*a*a
    physical_rows=sum(v!=0 for v in sums['physical'].values());assert physical_rows>0
    return {'placements':[list(t) for t in labels],'positive':3,'negative':3,'cylinder_residual_rows':0,'physical_short_residual_rows':physical_rows,'minimum_anchor_distance_squared':min(distances),'strict_board_halfplane_minimum':min(determinants),'nonoverlap_reason':'Every tile is in the radius-a disk about its obtuse vertex; all anchor distances are at least 2c>2a.','scope':'A contained rigid six-tile partial packing, not a realizable cell of a complete target tiling. Gate/node completion is not asserted.'}

def verify_periodic_sixteen(a,b,c,path):
    if not path.exists():return None
    records=[json.loads(line) for line in path.read_text().splitlines()]
    hit=next((r for r in records if r.get('found')),None)
    if hit is None:return None
    labels=hit['support'];assert len(labels)==16 and sum(eps(t) for t in labels)==0
    C=Counter()
    for t in labels:C.update(endpoints(a,b,c,t))
    assert all(v==0 for v in C.values())
    return {'placements':labels,'positive':8,'negative':8,'torus_residual_rows':0,'scope':'Integer periodic countercontrol to a 6/2c population-semigroup conjecture; no cylinder lift or nonoverlap is asserted.'}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,default=HERE/'SMALL_BALANCED_CELLS_REPLAY.json');args=parser.parse_args()
    report={'status':'PASS','excluded_balanced_populations':list(ABSENT),'targets':[],'scope':'Exact finite necessary exclusions for one isolated short-height Euclidean class with zero exterior endpoint current. Neither complete tile count is excluded.'}
    with tempfile.TemporaryDirectory(prefix='balanced-kernel-replay-') as temp:
        exe=Path(temp)/'verify_balanced_kernels'
        subprocess.run(['g++','-std=c++17','-O3',str(HERE/'verify_balanced_kernels.cpp'),'-o',str(exe)],check=True)
        for a,b,c,center in ((33,7,37,(800,0)),(35,13,43,(1000,0))):
            item={'tile':[a,b,c],'column_charge_and_moment_checks':verify_column_arithmetic(a,b,c),'small_exclusions':[]}
            wheel=tuple(int(j%2==0) for j,s in ORI)
            positive_input=f'{a} {b} {c} 6 1\n'+' '.join(map(str,wheel))+'\n'
            positive_run=subprocess.run([str(exe)],input=positive_input,text=True,capture_output=True,check=True)
            positive_rows=[json.loads(line) for line in positive_run.stdout.splitlines()]
            assert positive_rows[0]['found'] and len(positive_rows[0]['support'])==6
            positive_current=Counter()
            for label in positive_rows[0]['support']:positive_current.update(endpoints(a,b,c,label))
            assert all(v==0 for v in positive_current.values())
            assert sum(eps(t) for t in positive_rows[0]['support'])==0
            item['independent_search_positive_six_control']=True
            established=set()
            for n in ABSENT:
                assert n<c and n%6!=0
                assert {k for k in range(2,n,2) if k%6!=0}<=established
                raw,representatives=coverage(a,b,c,n)
                inp=f'{a} {b} {c} {n} {len(representatives)}\n'+'\n'.join(' '.join(map(str,v)) for v in representatives)+'\n'
                run=subprocess.run([str(exe)],input=inp,text=True,capture_output=True,check=True)
                rows=[json.loads(line) for line in run.stdout.splitlines()]
                assert len(rows)==len(representatives)+1
                assert rows[-1]['all_inventories_absent']
                assert all(r['index']==i and r['found'] is False for i,r in enumerate(rows[:-1]))
                item['small_exclusions'].append({'population':n,'raw_moment_inventories':raw,'dihedral_orbits':len(representatives),'independent_search_states':rows[-1]['states'],'all_absent':True,'component_induction_checked':True})
                established.add(n)
            item['rigid_balanced_six']=rigid_six(a,b,c,center)
            item['periodic_balanced_sixteen']=verify_periodic_sixteen(a,b,c,HERE/f'CPP_BALANCED_{c}_16.jsonl')
            if c==43:assert item['periodic_balanced_sixteen'] is not None
            report['targets'].append(item)
    args.out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'excluded_balanced_populations':list(ABSENT),'target_shapes':2,'rigid_six_controls':2,'full_3431_excluded':False,'full_5063_excluded':False},indent=2))

if __name__=='__main__':main()
