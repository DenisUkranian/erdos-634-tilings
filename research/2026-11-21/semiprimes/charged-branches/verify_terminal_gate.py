#!/usr/bin/env python3
"""Independently check exact endpoint certificates for one accessible gate.

Uses only integer polygon reconstruction and standard-library arithmetic.
No LP code is imported. This checks all residue classes; the accompanying
proof supplies the geometric pairing/localization hypotheses.
"""
import argparse
from fractions import Fraction
import json
from pathlib import Path

UNITS = ((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))


def norm(p):
    x,y=p
    return x*x+x*y+y*y


def check(data):
    a,b,c=data['tile']
    D=data['D']; t=data['charge_multiplier']; tables=data['endpoint_tables']
    assert all(isinstance(v,int) for table in tables for row in table for v in row)
    assert len(tables)==3 and all(len(table)==c and all(len(row)==c for row in table) for table in tables)
    assert a*a+a*b+b*b==c*c and D>0 and t>0
    def f(axis,p): return tables[axis][p[0]%c][p[1]%c]
    def tile(x,y,j,s):
        q=(x,y)
        u=(x-a*UNITS[j][0],y-a*UNITS[j][1])
        w=(x+b*UNITS[(j+s)%6][0],y+b*UNITS[(j+s)%6][1])
        polygon=(u,q,w) if s==1 else (u,w,q)
        determinant=sum(polygon[k][0]*polygon[(k+1)%3][1]-polygon[k][1]*polygon[(k+1)%3][0] for k in range(3))
        assert determinant==a*b
        weight=0; lengths=[]
        for k in range(3):
            start=polygon[k]; end=polygon[(k+1)%3]
            vec=(end[0]-start[0],end[1]-start[1]); length2=norm(vec);lengths.append(length2)
            if length2==c*c: continue
            assert length2 in (a*a,b*b)
            length=a if length2==a*a else b
            direction=UNITS.index((vec[0]//length,vec[1]//length))
            assert vec==(length*UNITS[direction][0],length*UNITS[direction][1])
            weight+=f(direction%3,end)-f(direction%3,start)
        assert sorted(lengths)==sorted((a*a,b*b,c*c))
        sign=s*(-1 if j%2 else 1)
        gate=(a*u[0]-b*u[1])%c if s==-1 else (a*u[1]-b*u[0])%c
        mate=(x-a*UNITS[j][0]+b*UNITS[(j+s)%6][0],y-a*UNITS[j][1]+b*UNITS[(j+s)%6][1],(j+3)%6,s)
        return weight,sign,gate,mate
    singles=0;pairs=0; min_single=None;min_pair=None;max_single=None;max_pair=None
    for x in range(c):
        for y in range(c):
            for j in range(6):
                for s in (-1,1):
                    weight,sign,gate,mate=tile(x,y,j,s)
                    if s==-1 and gate==0:
                        score=weight+t*sign
                        assert score<=D, (x,y,j,s,score,D)
                        singles+=1
                        min_single=score if min_single is None else min(min_single,score)
                        max_single=score if max_single is None else max(max_single,score)
                    mate_weight,mate_sign,mate_gate,_=tile(*mate)
                    assert mate_sign==-sign and mate_gate==gate
                    score=weight+mate_weight
                    assert score<=2*D, (x,y,j,s,score,2*D)
                    pairs+=1
                    min_pair=score if min_pair is None else min(min_pair,score)
                    max_pair=score if max_pair is None else max(max_pair,score)
    assert singles==6*c and pairs==12*c*c
    bounds={}
    for g in (1,2,3,4):
        numerator=t*g
        blocks=(numerator+D-1)//D
        if (blocks-g)%2: blocks+=1
        bounds[str(g)]={'charge_magnitude':c*g,'minimum_blocks':blocks,'minimum_tiles':blocks*c}
    # Positive geometric control: the standard c-grid of the scale-c tile.
    # In short-height-normalized coordinates its vertices are 0,cV,cW,
    # V=(a+b,-b), W=(a,0). This is the actual charged triangle used in
    # the prior charged-terminal polygon construction. Apply a half-turn
    # so that its charge is +c for the supplied dual.
    control=set()
    for i in range(c):
        for j in range(c-i):
            x=i*(a+b)+j*a;y=-i*b
            control.add((-(x+a),-y,3,-1))
            if i+j<c-1:
                control.add((-(x+a+b),-(y-b),0,-1))
    assert len(control)==c*c
    control_weight=0;control_charge=0;control_unpaired=0
    for label in control:
        weight,sign,gate,mate=tile(*label)
        control_weight+=weight;control_charge+=sign
        if mate not in control:
            assert gate==0
            control_unpaired+=1
    assert control_weight==0 and control_charge==c and control_unpaired==c
    assert t*control_charge <= D*len(control)
    positive_control={'population':len(control),'charge':control_charge,'unpaired_long_sides':control_unpaired,'all_unpaired_sides_at_selected_gate':True,'endpoint_weight_sum':control_weight,'scope':'Scale-c triangle is a positive tiled one-gate domain. It is not a complete target F2 tiling or a proof of completion.'}
    return {'tile':[a,b,c], 'status':'PASS', 'D':D,'charge_multiplier':t,'per_charge_block_bound':str(Fraction(t,D)), 'single_columns':singles, 'directed_pair_checks':pairs, 'distinct_pairs':pairs//2,'single_score_range':[min_single,max_single], 'pair_score_range':[min_pair,max_pair], 'rounded_bounds':bounds,'positive_control':positive_control,'scope':'All residue single and half-turn pair inequalities checked with integers. Geometric gate-isolation proof is separate; this is not a full-tiling existence or impossibility certificate.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('certificates',type=Path,nargs='+');p.add_argument('--out',type=Path)
    args=p.parse_args();result=[check(json.loads(path.read_text())) for path in args.certificates]
    output=json.dumps(result,indent=2)+'\n'
    if args.out: args.out.write_text(output)
    print(output)
