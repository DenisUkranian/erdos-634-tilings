"""Verify local endpoint duals and the boundary inventory of the exceptional lift."""
from collections import Counter
from itertools import product
from pathlib import Path
import json
import gzip
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/"charged-contour"))
from geometry import UNITS, add, scale, subtract, multiply


def wall_inventories(a,b,c,positive,negative):
    def side(length):
        return [(i,j) for i in range(positive+1) for j in range(negative+1)
                if a*i+b*j<=length and (length-a*i-b*j)%c==0]
    return [(x,y) for x,y in product(side(b*(2*a+b)),side(a*(a+2*b)))
            if x[0]+y[0]<=positive and x[1]+y[1]<=negative]


def endpoints(a,b,c,j,h,pt,linear):
    u=subtract(pt,scale(a,UNITS[j]))
    w=add(pt,scale(b,UNITS[(j+h)%6]))
    def index(axis,p):
        return axis%3*c+linear(p)%c
    return [(index(j,pt),h),(index(j,u),-h),(index(j+h,w),h),(index(j+h,pt),-h)]


def score(potential,column):
    return sum(potential[i]*k for i,k in column)


def gate_column(a,b,c,r,j,h,w):
    sign=h*(-1)**j
    phi=lambda p:p[0]+w*p[1]
    col=endpoints(a,b,c,j,h,(r,0),phi)
    gate=(r-a*phi(UNITS[j]))%c if h==-1 else c
    col.append((3*c+gate,sign))
    return col


def gate(a,b,c,record):
    w=(-b*pow(a,-1,c))%c
    den,y=record["den"],record["table"]
    assert den>0 and len(y)==4*c+1 and all(type(x) is int for x in y)
    for r,j,h in product(range(c),range(6),(-1,1)):
        assert score(y,gate_column(a,b,c,r,j,h,w))<=den
    return y[3*c],y[4*c],den


def wall(a,b,c,pos,neg,inventory,record):
    den,y,w=record["den"],record["table"],record["form"]
    size=c*c if w==-1 else c
    def residue(p):
        if w==-1:
            return (p[0]%c)*c+p[1]%c
        return (p[1] if w==c else p[0]+w*p[1])%c
    A=b*(2*a+b)
    B=a*(a+2*b)
    target=y[residue((A,0))]-y[0]+y[size]-y[size+residue((0,B))]+(pos-neg)*y[3*size]
    def ordinary(q,j,h):
        u=subtract(q,scale(a,UNITS[j]))
        v=add(q,scale(b,UNITS[(j+h)%6]))
        def value(axis,p):
            return y[axis%3*size+residue(p)]
        return h*(value(j,q)-value(j,u)+value(j+h,v)-value(j+h,q))+h*(-1)**j*y[3*size]
    for r,j,h in product(range(size),range(6),(-1,1)):
        q=divmod(r,c) if w==-1 else ((0,r) if w==c else (r,0))
        assert ordinary(q,j,h)<=den
    offset=3*size+1
    for heading,origin,(I,J) in zip((0,4),((0,0),(0,B)),inventory):
        def node(i,j):
            return offset+i*(J+1)+j
        target+=y[node(I,J)]-y[node(0,0)]
        for i,j in product(range(I+1),range(J+1)):
            p=add(origin,scale(a*i+b*j,UNITS[heading]))
            for short,length in enumerate((a,b)):
                ni,nj=i+int(short==0),j+int(short==1)
                if ni>I or nj>J:
                    continue
                end=add(p,scale(length,UNITS[heading]))
                for h in (-1,1):
                    if short==0:
                        apex,k=(end,heading) if h==1 else (p,heading+3)
                    else:
                        apex,k=(p,heading-1) if h==1 else (end,heading+4)
                    edge=ordinary(apex,k%6,h)
                    assert edge+y[node(ni,nj)]-y[node(i,j)]<=den
        offset+=(I+1)*(J+1)
    assert offset==len(y) and den>0 and target>den*(pos+neg)
    return [target,den]


def isolated_opposite_support(a,b,c,pos_hand):
    """Peel one-sign endpoint rows. Enumerate both hands and every rotation at the intersecting gate lines."""
    cols=[]
    for x,y,j,h in product(range(c),range(c),range(6),(-1,1)):
        if (h*(-1)**j==1)!=(h==pos_hand):
            continue
        pt=(x,y)
        u=subtract(pt,scale(a,UNITS[j]))
        znum=(a+b,-b) if h==1 else (a,b)
        if multiply(znum,u)[0]%c:
            continue
        w=add(pt,scale(b,UNITS[(j+h)%6]))
        col=Counter()
        for axis,p,sg in ((j,pt,h),(j,u,-h),(j+h,w,h),(j+h,pt,-h)):
            col[axis%3,p[0]%c,p[1]%c]+=sg
        cols.append({key:value for key,value in col.items() if value})
    sizes=[len(cols)]
    while cols:
        signs={}
        for col in cols:
            for key,n in col.items():
                signs[key]=signs.get(key,0)|(1 if n>0 else 2)
        keep=[col for col in cols if all(signs[k]==3 for k in col)]
        assert len(keep)<len(cols)
        cols=keep
        sizes.append(len(cols))
    return sizes


def check():
    records=json.loads((HERE/"duals.json").read_text())
    wall_tables=json.loads(gzip.decompress((HERE/"second-wall-tables.json.gz").read_bytes()))
    result={}
    for a,b,c,pos,neg,R in ((33,7,37,19,8,42),(35,13,43,5,27,55)):
        N=(a+2*b)*(2*a+b)
        tables=records[str(c)]
        inv=wall_inventories(a,b,c,pos,neg)
        assert len(inv)==len(tables['walls'])==(5 if c==37 else 0)
        walls=[wall(a,b,c,pos,neg,v,rec) for v,rec in zip(inv,tables['walls'])]
        ep,en=(56,8) if c==37 else (5,70)
        extra_iv=wall_inventories(a,b,c,ep,en)
        assert len(extra_iv)==len(wall_tables[str(c)])
        extra_bounds=[wall(a,b,c,ep,en,v,rec) for v,rec in zip(extra_iv,wall_tables[str(c)])]
        remaining=(19,45) if c==37 else (48,27)
        assert sum(remaining)==pos+neg+c
        A,D,den=gate(a,b,c,tables['single'])
        assert A*c>3*c*den
        if c==43:
            assert A*c>4*c*den
        B,E,den2=gate(a,b,c,tables['native'])
        assert (2*B-E)*c>7*c*den2
        core=pos+neg+c
        initial=(N-core-3*c)//(2*c)
        assert (N-core-6*c)//(2*c)==R
        extra=(N-core)//c-2*initial
        assert extra==(3 if c==37 else 4)
        result[str(N)]={"minimum_core":core,"signs_at_minimum_core":remaining,
                        "other_minimum_size_inventory_excluded":[ep,en],
                        "second_wall_bounds":extra_bounds,"minimum_ordinary_excess_blocks":6,"single_gate_numerator_per_charge":A,
                        "single_gate_denominator":den,"native_unit_lower_bound":[(2*B-E)*c,den2],
                        "wall_inventories":inv,"wall_bound_fractions":walls,
                        "opposite_support_sizes":[isolated_opposite_support(a,b,c,s) for s in (1,-1)],
                        "maximum_occupied_ordinary_lifts":R,"original_status":"OPEN"}
    from control143 import controls
    result['complete_143_controls']=controls()
    return result


if __name__=='__main__':
    if not __debug__:
        raise SystemExit("Enable Python assertions.")
    print(json.dumps(check(),indent=2))
