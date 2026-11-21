#!/usr/bin/env python3
"""Independent, standard-library replay of the full periodic integer image.

The certificate concerns SIGNED integer multiplicities. In particular it is
not a certificate of a nonnegative integer kernel or physical tiling.
"""
from __future__ import annotations

from collections import Counter
import gzip
import json
from math import gcd
from pathlib import Path

HERE=Path(__file__).resolve().parent
U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))


def expand(description,c):
    if description[0]=='six':
        _,seed,tx,ty=description
        return [((x+tx)%c,(y+ty)%c,j,s,m) for x,y,j,s,m in seed]
    if description[0]=='uniform':
        _,j,s=description
        return [(x,y,j,s,1) for x in range(c) for y in range(c)]
    assert description[0]=='fan'
    turns=description[1];out=[]
    for r in range(c):
        for j,s in ((0,-1),(0,1),(4,1)):
            x,y=0,r
            for _ in range(turns):x,y=-y,x+y
            out.append((x%c,y%c,(j+turns)%6,s,1))
    return out


def evaluate(columns,a,b,c):
    endpoints=Counter();gates=[0]*(2*c);positive=negative=0
    for x,y,j,s,multiplicity in columns:
        assert all(isinstance(v,int) for v in (x,y,j,s,multiplicity))
        assert 0<=x<c and 0<=y<c and 0<=j<6 and s in (-1,1)
        ax,ay=U[j];bx,by=U[(j+s)%6]
        ux,uy=(x-a*ax)%c,(y-a*ay)%c
        wx,wy=(x+b*bx)%c,(y+b*by)%c
        for axis,xx,yy,coefficient in ((j,x,y,s),(j,ux,uy,-s),
                (j+s,wx,wy,s),(j+s,x,y,-s)):
            endpoints[axis%3,xx,yy]+=coefficient*multiplicity
        sign=s*(-1 if j%2 else 1)
        gate=(a*uy-b*ux)%c if s==1 else c+(a*ux-b*uy)%c
        gates[gate]+=sign*multiplicity
        if sign==1:positive+=multiplicity
        else:negative+=multiplicity
    assert sum(gates)==positive-negative
    return endpoints,gates,positive,negative


def determinant(matrix):
    """Fraction-free Bareiss elimination; exact divisions are asserted."""
    A=[list(row) for row in matrix];n=len(A)
    assert n and all(len(row)==n for row in A)
    sign=1;previous=1
    for k in range(n-1):
        pivot=next((i for i in range(k,n) if A[i][k]),None)
        if pivot is None:return 0
        if pivot!=k:A[k],A[pivot]=A[pivot],A[k];sign=-sign
        value=A[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                numerator=A[i][j]*value-A[i][k]*A[k][j]
                assert numerator%previous==0
                A[i][j]=numerator//previous
            A[i][k]=0
        previous=value
    return sign*A[-1][-1]


def charge_potential(a,b,c):
    t=pow(a-b,-1,c)
    def potential(axis,x,y):
        return t*(x if axis==0 else -y if axis==1 else y)
    checked=0
    # The potential is linear over F_c. Translation adds a constant to
    # each endpoint pair and cancels, so one anchor per orientation suffices.
    for j in range(6):
        for s in (-1,1):
            ax,ay=U[j];bx,by=U[(j+s)%6]
            score=-s*potential(j%3,-a*ax,-a*ay)+s*potential((j+s)%3,b*bx,b*by)
            assert (score-s*(-1 if j%2 else 1))%c==0
            checked+=1
    return checked


def index_case(case):
    a,b,c=case['tile'];assert a*a+a*b+b*b==c*c
    assert case['projected_rows']==2*c+1
    potentials=charge_potential(a,b,c)
    vectors=[]
    for description in case['kernel_catalogue']:
        columns=expand(description,c)
        assert all(col[-1]>0 for col in columns)
        endpoints,gates,P,N=evaluate(columns,a,b,c)
        assert not any(endpoints.values())
        assert (P-N)%c==0
        vectors.append(gates+[P])
    divisors=[];g=0
    for minor in case['minors']:
        indices=minor['column_indices']
        assert len(indices)==len(set(indices))==2*c+1
        matrix=[[vectors[j][i] for j in indices] for i in range(2*c+1)]
        value=determinant(matrix)
        assert value and abs(value)==abs(minor['residual_determinant'])
        divisors.append(value);g=gcd(g,value)
    assert g==c==case['gcd_of_absolute_determinants']
    return {'tile':[a,b,c],'chart_dimension':2*c+1,
        'positive_endpoint_kernels_checked':len(vectors),
        'exact_square_determinants':divisors,'determinant_gcd':g,
        'orientation_potential_checks':potentials,
        'integer_image_characterized':True}


def witness_case(target):
    with gzip.open(HERE/f'FULL_INTEGER_IMAGE_{target}.json.gz','rt') as stream:certificate=json.load(stream)
    a,b,c=certificate['tile'];columns=certificate['signed_tile_columns']
    endpoints,gates,P,N=evaluate(columns,a,b,c)
    assert not any(endpoints.values())
    expected=[0]*(2*c)
    expected[0],expected[c]=certificate['profile']
    assert gates==expected
    assert (P,N)==(certificate['positive'],certificate['negative'])
    assert (P,N)==((74,37) if target==3431 else (129,86))
    assert any(col[-1]<0 for col in columns)
    return {'target':target,'profile':certificate['profile'],
        'signed_positive_count':P,'signed_negative_count':N,
        'nonzero_tile_columns':len(columns),
        'negative_tile_columns':sum(col[-1]<0 for col in columns),
        'maximum_absolute_multiplicity':max(abs(col[-1]) for col in columns),
        'exact_endpoint_rows':3*c*c,'exact_gate_rows':2*c,
        'scope':'Signed integer witness only; not a nonnegative integer packing.'}


def main():
    with gzip.open(HERE/'GATE_IMAGE_INDEX_CERTIFICATE.json.gz','rt') as stream:certificate=json.load(stream)
    report={'status':'PASS','image_cases':[index_case(case) for case in certificate['cases']],
        'signed_witnesses':[witness_case(target) for target in (3431,5063)],
        'conclusion':'The full periodic endpoint/gate signed integer image has exactly the charge divisibility obstruction c | (P-N), together with sum(gates)=P-N. Nonnegative coefficients and actual placement remain additional requirements; both target tiling problems remain open.'}
    (HERE/'INTEGER_GATE_IMAGE_REPLAY.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
