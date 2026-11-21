#!/usr/bin/env python3
"""Exact, dependency-free universal lifting check for the 3431 projection.

This certifies a positive linear map from periodic fractional tile weights
into contained fractional tile weights preserving all first transverse
endpoint moments. It does not check disjointness and is not a tiling.
"""
from collections import Counter
from pathlib import Path
import argparse,json

A,B,C=33,7,37
U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))
CENTER2=(1601,1)  # twice the common mean anchor in the path frame / z
D=4*C*C
BOARD=((0,0),(C*C*(A+B),-C*C*B),(A*A*(A+2*B),A*B*(A+2*B)))

def det(p,q,r):
    return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])

def transverse(axis,p):
    return (p[1],p[0],p[0]+p[1])[axis]

def rows(q,j,s):
    u=(q[0]-A*U[j][0],q[1]-A*U[j][1])
    k=(j+s)%6
    w=(q[0]+B*U[k][0],q[1]+B*U[k][1])
    for axis,p,v in ((j,q,s),(j,u,-s),(k,w,s),(k,q,-s)):
        axis%=3
        yield (axis,p[0]%C,p[1]%C),v,transverse(axis,p)

def gate(q,j,s):
    u=(q[0]-A*U[j][0],q[1]-A*U[j][1])
    return ((A*u[1]-B*u[0]) if s>0 else (A*u[0]-B*u[1]))%C

def lifts(res):
    lo=[res[i]+C*((CENTER2[i]-2*res[i])//(2*C)) for i in range(2)]
    d=[CENTER2[i]-2*lo[i] for i in range(2)]
    assert all(0<t<2*C for t in d)
    result=[]
    for ix in (0,1):
        for iy in (0,1):
            q=(lo[0]+C*ix,lo[1]+C*iy)
            wx=d[0] if ix else 2*C-d[0]
            wy=d[1] if iy else 2*C-d[1]
            result.append((q,wx*wy))
    assert sum(w for _,w in result)==D
    for i in range(2):assert 2*sum(w*q[i] for q,w in result)==D*CENTER2[i]
    return result

def verify():
    minimum_det=None
    columns=0;contained=0;minimum_weight=D
    for x in range(C):
      for y in range(C):
        lifted=lifts((x,y))
        minimum_weight=min(minimum_weight,*(v for _,v in lifted))
        for j in range(6):
          for s in (-1,1):
            eps=s*(-1 if j%2 else 1)
            base=Counter()
            for row,v,t in rows((x,y),j,s):base[row]+=v
            current=Counter();moment2=Counter()
            for q,weight in lifted:
                assert q[0]%C==x and q[1]%C==y
                assert gate(q,j,s)==gate((x,y),j,s)
                for row,v,t in rows(q,j,s):
                    current[row]+=weight*v
                    moment2[row]+=2*weight*v*t
                u=(q[0]-A*U[j][0],q[1]-A*U[j][1])
                k=(j+s)%6
                w=(q[0]+B*U[k][0],q[1]+B*U[k][1])
                assert abs(det(u,q,w))==A*B
                for point in (u,q,w):
                    p=(C*point[0],C*point[1])
                    for i in range(3):
                        value=det(BOARD[i],BOARD[(i+1)%3],p)
                        assert value>0
                        minimum_det=value if minimum_det is None else min(minimum_det,value)
                contained+=1
            for row in set(base)|set(current)|set(moment2):
                assert current[row]==D*base[row]
                assert moment2[row]==D*transverse(row[0],CENTER2)*base[row]
            columns+=1
    assert columns==12*C*C and contained==4*columns
    return {
        'tile':[A,B,C],
        'scope':'Exact universal fractional lifting, not a packing or a tiling; no nonoverlap or integral multiplicities are asserted.',
        'common_mean_anchor_twice':list(CENTER2),
        'lifting_weight_denominator':D,
        'minimum_lifting_weight_numerator':minimum_weight,
        'periodic_columns':columns,
        'contained_lifted_columns':contained,
        'minimum_strict_board_halfplane_determinant':minimum_det,
        'all_weights_strictly_positive':True,
        'all_mean_anchors_exact':True,
        'all_endpoint_current_columns_preserved':True,
        'all_first_transverse_moment_columns_preserved':True,
        'all_signed_gate_bins_preserved':True,
        'checks':'PASS',
        'rational_111_mass_witness_dependency':'../../global-invariant/N3431_PROFILE_LIMIT.md and ../../global-invariant/N3431_RATIONAL_PROJECTION_CERTIFICATE.json'
    }

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',type=Path,default=Path(__file__).with_name('FIRST_MOMENT_LIFT_REPLAY.json'))
    args=p.parse_args();report=verify();args.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':
    if not __debug__:raise SystemExit('Run with Python assertions enabled.')
    main()
