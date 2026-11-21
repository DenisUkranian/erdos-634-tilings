#!/usr/bin/env python3
"""Independent integer checks of native even-core endpoint certificates."""
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'scripts').is_dir() and (p/'research').is_dir())
U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))


def column(a,b,c,x,y,j,s):
    q=x,y;u=x-a*U[j][0],y-a*U[j][1]
    w=x+b*U[(j+s)%6][0],y+b*U[(j+s)%6][1]
    row=Counter()
    for ax,p,value in ((j,q,s),(j,u,-s),(j+s,w,s),(j+s,q,-s)):
        row[(ax%3)*c*c+(p[0]%c)*c+p[1]%c]+=value
    return row,s*(-1)**j,(a*u[0]-b*u[1])%c,(u[0]+w[0]-x,u[1]+w[1]-y,(j+3)%6,s)


def source(a,b,c):
    A=b*(2*a+b);B=a*(a+2*b)
    rhs=Counter()
    for axis,p,v in ((0,(0,0),1),(0,(B,0),-1),(1,(B,0),1),(1,(B,-A),-1)):
        rhs[axis*c*c+(p[0]%c)*c+p[1]%c]+=v
    return rhs


def check_certificate(path):
    data=json.loads(path.read_text());a,b,c=data['tile'];d=a-b
    assert c*c==a*a+a*b+b*b
    f=data['endpoint_weights'];t=data['charge_weight'];D=data['denominator']
    assert len(f)==3*c*c and isinstance(D,int) and D>0
    assert all(isinstance(v,int) for v in f) and isinstance(t,int)
    singles=pairs=0;maximum_single=maximum_pair=-10**50
    for x in range(c):
        for y in range(c):
            for j in range(6):
                for s in (-1,1):
                    row,eps,gate,mate=column(a,b,c,x,y,j,s)
                    W=sum(v*f[r] for r,v in row.items())
                    if s==-1 and gate==0:
                        score=W+t*eps
                        assert score<=D
                        maximum_single=max(maximum_single,score);singles+=1
                    key=(x,y,j,s);mate_res=(mate[0]%c,mate[1]%c,mate[2],s)
                    if key<mate_res:
                        other,e2,_,back=column(a,b,c,*mate_res)
                        assert eps+e2==0 and (back[0]%c,back[1]%c,back[2],s)==key
                        score=W+sum(v*f[r] for r,v in other.items())
                        assert score<=2*D
                        maximum_pair=max(maximum_pair,score);pairs+=1
    rhs=source(a,b,c);g=data['native_charge_units'];G=d+c*g
    numerator=sum(v*f[r] for r,v in rhs.items())+t*G
    assert numerator==data['numerator'] and G==data['charge']
    supplied={r:v for r,v in data['rhs_nonzero']};assert supplied==dict(rhs)|{3*c*c:G}
    N=(a+2*b)*(2*a+b)
    rp=((N+d)*pow(2,-1,c))%c;rm=((N-d)*pow(2,-1,c))%c
    delta=(G-rp+rm)//c;assert rp-rm+c*delta==G
    base=rp+rm+c*abs(delta)
    extra=max(0,-((-(numerator-D*base))//(2*c*D)))
    rounded=base+2*c*extra
    assert rounded*D>=numerator and (rounded==base or (rounded-2*c)*D<numerator)
    expected={(37,-2):212,(37,-3):397,(37,-4):582,(43,-3):677}
    assert rounded==expected[c,g]
    return dict(tile=[a,b,c],native_charge_units=g,charge=G,single_columns=singles,pair_columns=pairs,maximum_single=maximum_single,maximum_pair=maximum_pair,exact_bound=str(F(numerator,D)),rounded_population=rounded,core_sign_residues=[rp,rm],certificate_sha256=hashlib.sha256(path.read_bytes()).hexdigest())


def positive_control():
    data=json.loads((ROOT/'research/2026-11-20/semiprimes/continuation/global-endpoints/tiling_143.json').read_text())
    a,b,c=data['sides'];B=a*(a+2*b)
    tiles=set()
    # F(q)/z^2 = B-rho*conjugate(q) on a standard height-zero core.
    for (x,y,e),h,j,s in data['tiles']:
        if h!=0:continue
        x=F(x,c**e);y=F(y,c**e)
        q=B-y,-x
        # rho*conjugate(x+y*rho) = y+x*rho.
        assert all(v.denominator==1 for v in q)
        tiles.add((int(q[0]),int(q[1]),(4-j)%6,-s))
    assert len(tiles)==38
    total=Counter();charge=0;paired=set();singles=0
    for key in tiles:
        row,eps,gate,mate=column(a,b,c,*key);total.update(row);charge+=eps
        if key[-1]==-1 and gate==0:singles+=1
        else:
            assert mate in tiles
            paired.add(tuple(sorted((key,mate))))
    assert all(total[r]==source(a,b,c)[r] for r in set(total)|set(source(a,b,c)))
    assert charge==a-b==2
    return dict(N=143,core_population=len(tiles),core_charge=charge,native_single_tiles=singles,forced_whole_pairs=len(paired),exact_inhomogeneous_endpoint_identity=True)


def main():
    # List proof inputs explicitly: this directory also contains our replay.
    paths=[HERE/name for name in (
        'CORE_3431_G_MINUS2.json', 'CORE_3431_G_MINUS3.json',
        'CORE_3431_G_MINUS4.json', 'CORE_5063_G_MINUS3.json')]
    report=dict(status='PASS',scope='Necessary even-node bounds under one native odd mesh at height one and no other short heights than 0,1,2; no full target exclusion.',certificates=[check_certificate(p) for p in paths],positive_control_143=positive_control(),targets={'3431':'OPEN','5063':'OPEN'})
    (HERE/'CORE_BUDGET_REPLAY.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    if not __debug__:raise SystemExit('Use Python with assertions enabled.')
    main()
