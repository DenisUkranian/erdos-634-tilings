#!/usr/bin/env python3
"""Independent integer check of the two-native-gate population certificates.

Uses CCW polygons and exact metric edge recognition; imports neither the
numerical generator nor NumPy/SciPy. Also projects a complete 143 tiling.
"""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import argparse
import json

U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))


def add(p,q):return p[0]+q[0],p[1]+q[1]
def sub(p,q):return p[0]-q[0],p[1]-q[1]
def mul(p,q):return p[0]*q[0]-p[1]*q[1],p[0]*q[1]+p[1]*q[0]+p[1]*q[1]
def scale(k,p):return k*p[0],k*p[1]
def conj(p):return p[0]+p[1],-p[1]
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def norm(p):return p[0]*p[0]+p[0]*p[1]+p[1]*p[1]
def eps(tile):return tile[3]*(-1 if tile[2]%2 else 1)


def polygon(a,b,tile):
    x,y,j,s=tile;q=x,y
    u=sub(q,scale(a,U[j]));w=add(q,scale(b,U[(j+s)%6]))
    vertices=(u,q,w)
    assert abs(det(sub(q,u),sub(w,u)))==a*b
    return vertices if det(sub(q,u),sub(w,u))>0 else vertices[::-1]


def gate(a,b,c,tile):
    x,y,j,s=tile
    u=(x-a*U[j][0],y-a*U[j][1])
    factor=(a+b,-b) if s==1 else (a,b)
    product=mul(u,factor)
    direct=all(t%c==0 for t in product)
    one_prime=((a*u[1]-b*u[0]) if s==1 else (a*u[0]-b*u[1]))%c==0
    assert direct==one_prime
    return direct


def mate(a,b,tile):
    x,y,j,s=tile;k=(j+s)%6
    return x-a*U[j][0]+b*U[k][0],y-a*U[j][1]+b*U[k][1],(j+3)%6,s


def short_rows(a,b,c,tile):
    poly=polygon(a,b,tile)
    rows=Counter()
    for p,q in zip(poly,poly[1:]+poly[:1]):
        v=sub(q,p);length2=norm(v)
        if length2==c*c:
            continue
        assert length2 in (a*a,b*b)
        L=a if length2==a*a else b
        j=next(j for j in range(6) if v==scale(L,U[j]))
        rows[j%3,q[0]%c,q[1]%c]+=1
        rows[j%3,p[0]%c,p[1]%c]-=1
    return rows


def verify_certificate(path):
    data=json.loads(path.read_text());a,b,c=data['tile']
    assert c*c==a*a+a*b+b*b
    cert=data['exact_certificate'];tables=cert['endpoint_tables']
    assert len(tables)==3 and all(len(t)==c and all(len(row)==c for row in t) for t in tables)
    assert all(type(v) is int for t in tables for row in t for v in row)
    t,D=cert['charge_multiplier'],cert['tile_bound']
    assert type(t) is int and type(D) is int and D>0
    def weight(tile):
        return sum(coefficient*tables[axis][x][y]
                   for (axis,x,y),coefficient in short_rows(a,b,c,tile).items())
    singles=pairs=0;max_single=None;max_pair=None
    for x in range(c):
        for y in range(c):
            for j in range(6):
                for s in (-1,1):
                    tile=x,y,j,s
                    if gate(a,b,c,tile):
                        score=weight(tile)+t*eps(tile)
                        assert score<=D,(path,tile,score,D)
                        max_single=score if max_single is None else max(max_single,score)
                        singles+=1
                    elif j<3:
                        other=mate(a,b,tile)
                        assert not gate(a,b,c,other) and eps(other)==-eps(tile)
                        assert mate(a,b,other)==tile
                        score=weight(tile)+weight(other)
                        assert score<=2*D,(path,tile,score,2*D)
                        max_pair=score if max_pair is None else max(max_pair,score)
                        pairs+=1
    assert singles==12*c and pairs==6*c*(c-1)
    assert cert['population_lower_numerator']==c*t
    assert cert['population_lower_denominator']==D
    assert t>3*D
    blocks=1
    while blocks*D<t or blocks%2==0:
        blocks+=1
    return {'tile':[a,b,c],'open_singles_checked':singles,
            'closed_pairs_checked':pairs,'charge_multiplier':t,'tile_bound':D,
            'largest_single_score':max_single,'largest_pair_score':max_pair,
            'population_lower_fraction':f'{c*t}/{D}',
            'minimum_odd_c_blocks':blocks,'rounded_population':blocks*c,
            'all_integer_inequalities':'PASS'}


def find_continuation():
    for ancestor in Path(__file__).resolve().parents:
        for candidate in (ancestor,ancestor/'repo/research/2026-11-20/semiprimes/continuation'):
            if (candidate/'global-endpoints/tiling_143.json').exists():return candidate
    raise FileNotFoundError('Pass --continuation.')


def control(continuation):
    data=json.loads((continuation/'global-endpoints/tiling_143.json').read_text())
    a,b,c=data['sides'];assert(a,b,c)==(5,3,7)
    B=a*(a+2*b);z=F(a,c),F(b,c);rho=(0,1)
    selected=set()
    for q,h,j,s in data['tiles']:
        if h!=1:continue
        x,y,e=q;point=F(x,c**e),F(y,c**e)
        # Path isometry divided by z: B*z-rho*z*conjugate(q).
        native=sub(scale(B,z),mul(mul(rho,z),conj(point)))
        assert all(v.denominator==1 for v in native)
        selected.add((int(native[0]),int(native[1]),(4-j)%6,-s))
    assert len(selected)==105
    remaining=set(selected);currents=Counter();plus=minus=0;singles=pairs=0
    for tile in selected:
        currents.update(short_rows(a,b,c,tile))
        if eps(tile)==1:plus+=1
        else:minus+=1
    while remaining:
        tile=remaining.pop()
        if gate(a,b,c,tile):
            singles+=1
        else:
            other=mate(a,b,tile)
            assert other in remaining
            remaining.remove(other)
            pairs+=1
    assert not any(currents.values())
    assert plus==56 and minus==49 and plus-minus==c
    assert singles+2*pairs==105
    return {'actual_height_one_tiles':105,'positive':plus,'negative':minus,
            'open_single_columns':singles,'actual_closed_pair_columns':pairs,
            'all_residue_current_rows_zero':True,
            'scope':'Projection of the previously independently verified complete 143 tiling.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--continuation',type=Path)
    parser.add_argument('--out',type=Path)
    parser.add_argument('certificates',nargs='*',type=Path)
    args=parser.parse_args()
    paths=args.certificates or [Path(__file__).resolve().parent/f'BOTH_GATE_MIN_{c}.json' for c in(37,43)]
    report={'scope':'Exact conditional exclusion of odd population3c in the entire two-tree exterior-spine class; unrestricted targets remain open.',
            'certificates':[verify_certificate(p) for p in paths],
            'positive_143_control':control(args.continuation or find_continuation()),
            'checks':'PASS'}
    text=json.dumps(report,indent=2)+'\n'
    if args.out:args.out.write_text(text)
    print(text,end='')


if __name__=='__main__':
    if not __debug__:raise SystemExit('Run without -O.')
    main()
