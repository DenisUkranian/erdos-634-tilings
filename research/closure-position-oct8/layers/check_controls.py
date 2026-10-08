#!/usr/bin/env python3
"""Replay formal surviving controls; independently check chord formula by clipping."""
import json,sys
from fractions import Fraction as F
from pathlib import Path
from collections import defaultdict
from probe import dirs,cap,violates,atoms,comp
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'central'))
from probe_central_24 import classify

def det(a,b):return a[0]*b[1]-a[1]*b[0]
def sub(a,b):return a[0]-b[0],a[1]-b[1]

def clipped_max_chord(h,j):
    d=dirs(h)[j];poly=[(0,0),(154,0),(49,56)];values=[]
    assert d[0]*d[0]+d[0]*d[1]+d[1]*d[1]==1
    for vertex in poly:
        lo=None;hi=None
        for p,q in zip(poly,poly[1:]+poly[:1]):
            e=sub(q,p);constant=det(e,sub(vertex,p));coefficient=det(e,d)
            if coefficient>0:
                b=-F(constant)/coefficient;lo=b if lo is None else max(lo,b)
            elif coefficient<0:
                b=-F(constant)/coefficient;hi=b if hi is None else min(hi,b)
            else:assert constant>=0
        assert lo is not None and hi is not None and lo<=hi
        values.append(hi-lo)
    return max(values)

def check_report(path):
    report=json.loads(path.read_text());assert report['status']=='EXACT_FORMAL_FEASIBLE'
    currents=defaultdict(lambda:[0,0,0]);total=0
    for w in report['witness']:
        h=w['h'];inv=w['unsigned_A0_to_A5_B0_to_B5'];assert len(inv)==12 and all(isinstance(x,int) and x>=0 for x in inv)
        assert sum(inv)==w['n'];total+=sum(inv)
        assert [inv[j]-inv[j+3] for j in range(3)]==w['A']
        assert [inv[j+6]-inv[j+9] for j in range(3)]==w['B']
        assert w['n']>= (24 if h==0 else 26)
        assert w['n']%13==(11 if h==0 else 0)
        assert classify(inv) if h==0 else not violates(inv,h)
        for typ in range(2):
            for j in range(6):
                n=inv[typ*6+j]
                edge_data=[(h,j,8 if typ==0 else 7),(h,(j+5)%6,7 if typ==0 else 8),
                           (h-1,(j+3)%6,13) if typ==0 else (h+1,(j+2)%6,13)]
                for eh,rotation,length in edge_data:
                    currents[eh][rotation%3]+=n*length*(1 if rotation<3 else -1)
    assert total==154
    for h,vector in currents.items():
        assert vector==([154,0,0] if h==0 else [0,0,91] if h==1 else [0,-91,0] if h==-1 else [0,0,0]),(h,vector)
    return {'path':path.name,'support':report['support'],'total':total,'local_geometric_inequalities':'PASS','global_direction_currents':'PASS','placement_claimed':False}

def main():
    chords=0
    for h in range(-4,5):
        for j in range(3):assert cap(h,j)==clipped_max_chord(h,j);chords+=1
    # Independently test that all <=13 zero sums contain one of the reported minimal atoms.
    zeros=0
    for n in range(1,14):
        for v in comp(n,4):
            if (8*(v[0]-v[1])+7*(v[2]-v[3]))%13==0:
                assert any(all(a<=b for a,b in zip(atom,v)) for atom in atoms);zeros+=1
    root=Path(__file__).resolve().parent
    records=[check_report(root/name) for name in ('filtered_0_4.json','filtered_m1_3.json','filtered_m2_2.json')]
    return {'status':'PASS','chords_independently_clipped':chords,'zero_sum_multisets_checked':zeros,'minimal_atoms':len(atoms),'records':records,'N154_solved':False}

if __name__=='__main__':print(json.dumps(main(),indent=2))
