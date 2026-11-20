#!/usr/bin/env python3
"""Check rational periodic primal witnesses and their exact matching duals.

Uniform lifting over ker(psi) verifies every full two-coordinate endpoint
row. Such a witness is not a finite polygon, positive packing, or tiling.
"""
import argparse
from collections import defaultdict
from fractions import Fraction
import json
from pathlib import Path

from verify_terminal_gate import check, norm, UNITS


def verify(data):
    dual=check(data)
    a,b,c=data['tile']
    psi=lambda p:(a*p[0]-b*p[1])%c
    inva=pow(a,-1,c)
    currents=defaultdict(Fraction)
    population=Fraction(0);charge=Fraction(0);lifted=0
    def record(q,j,s,weight):
        nonlocal population,charge,lifted
        x,y=q
        u=(x-a*UNITS[j][0],y-a*UNITS[j][1])
        w=(x+b*UNITS[(j+s)%6][0],y+b*UNITS[(j+s)%6][1])
        polygon=(u,q,w) if s==1 else (u,w,q)
        for k in range(3):
            start=polygon[k];end=polygon[(k+1)%3]
            vec=(end[0]-start[0],end[1]-start[1]);length2=norm(vec)
            if length2==c*c:continue
            assert length2 in (a*a,b*b)
            length=a if length2==a*a else b
            direction=UNITS.index((vec[0]//length,vec[1]//length))
            assert vec==(length*UNITS[direction][0],length*UNITS[direction][1])
            axis=direction%3
            currents[axis,end[0]%c,end[1]%c]+=weight
            currents[axis,start[0]%c,start[1]%c]-=weight
        population+=weight;charge+=weight*s*(-1 if j%2 else 1);lifted+=1
        return u,w
    for labels,numerator,denominator in data['periodic_primal_support']:
        assert numerator>0 and denominator>0
        weight=Fraction(numerator,denominator*c)
        assert len(labels) in (1,2)
        r,j,s,_=labels[0]
        assert 0<=r<c and 0<=j<6 and s in (-1,1)
        for y in range(c):
            q=((inva*(r+b*y))%c,y)
            assert psi(q)==r
            u,w=record(q,j,s,weight)
            if len(labels)==1:
                assert s==-1 and psi(u)==0
            else:
                mate=(u[0]+w[0]-q[0],u[1]+w[1]-q[1])
                other=labels[1]
                assert other[:3]==[psi(mate),(j+3)%6,s]
                record(mate,(j+3)%6,s,weight)
    assert all(value==0 for value in currents.values())
    assert charge==c
    assert population==Fraction(data['exact_periodic_primal_population'])
    assert population==Fraction(c*data['charge_multiplier'],data['D'])
    return {'tile':[a,b,c],'status':'PASS','exact_periodic_population':str(population),'exact_population_per_charge':str(population/charge),'reduced_support_columns':len(data['periodic_primal_support']),'lifted_tile_occurrences':lifted,'full_endpoint_rows':3*c*c,'all_full_endpoint_rows_zero':True,'charge':int(charge),'matches_independently_checked_dual':True,'scope':'An exact fractional periodic endpoint projection, not a finite-support configuration, packing, complete tiling, or semiprime decision.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('witnesses',type=Path,nargs='+');p.add_argument('--out',type=Path);args=p.parse_args()
    result=[verify(json.loads(path.read_text())) for path in args.witnesses];text=json.dumps(result,indent=2)+'\n'
    if args.out:args.out.write_text(text)
    print(text)
