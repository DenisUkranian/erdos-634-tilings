#!/usr/bin/env python3
"""Independent exact coordinate audit for standard-frame 5063 cell caps."""
from fractions import Fraction as F
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent


def add(u,v):return u[0]+v[0],u[1]+v[1]
def neg(u):return -u[0],-u[1]
def sub(u,v):return add(u,neg(v))
def scale(u,t):return u[0]*t,u[1]*t
def mul(u,v):
    return u[0]*v[0]-u[1]*v[1],u[0]*v[1]+u[1]*v[0]+u[1]*v[1]
def conj(u):return u[0]+u[1],-u[1]
def norm(u):return u[0]*u[0]+u[0]*u[1]+u[1]*u[1]


def main():
    a,b,c=35,13,43
    A,B=b*(2*a+b),a*(a+2*b)
    rho=(F(0),F(1))
    z=(F(a,c),F(b,c))
    z2=mul(z,z)
    cinvz=scale(conj(z),c)
    assert norm(z)==1
    def frame(w):return sub(scale(z2,B),mul(mul(rho,z2),conj(w)))
    assert frame((F(A),F(0)))==(F(c*c),F(0))
    def labels(u):
        assert u[0].denominator==u[1].denominator==1
        return int(a*u[1]-b*u[0])%c,int(a*u[0]-b*u[1])%c
    determinant=(b*b-a*a)%c
    assert determinant==19 and pow(determinant,-1,c)*determinant%c==1
    seen=set()
    for x in range(c):
        for y in range(c):
            U=(F(x),F(y))
            q=add((F(A),F(0)),scale(mul(z,U),F(1,c)))
            reconstructed=mul(cinvz,sub(q,(F(A),F(0))))
            assert reconstructed==U
            pair=labels(U)
            assert pair not in seen
            seen.add(pair)
            pathU=mul(cinvz,frame(q))
            expected=((-pair[1])%c,(-pair[0])%c)
            assert labels(pathU)==expected
            assert (pair==(0,0))==(x==0 and y==0)
    assert len(seen)==c*c
    directions=[(F(1),F(0))]
    for _ in range(5):directions.append(mul(directions[-1],rho))
    increments=0
    powers=[(F(1),F(0)),z,z2]
    for h in range(3):
        for j in range(6):
            for s in (-1,1):
                delta=[scale(mul(powers[h],directions[j]),-a),
                       scale(mul(powers[h],directions[(j+s)%6]),b)]
                for v in delta:
                    dv=mul(cinvz,v)
                    assert dv[0].denominator==dv[1].denominator==1
                    if h==1:assert labels(dv)==(0,0)
                    increments+=1
                eps=s*(-1 if j%2 else 1)
                hp,jp,sp=2-h,(4-j)%6,-s
                epsp=sp*(-1 if jp%2 else 1)
                assert hp in (0,1,2) and epsp==-eps
    matrices=[]
    for x in range(1,43):
        matrix=[[(x,x),(43-x,43-x)],[(43-x,43-x),(x,43+x)]]
        plus=sum(v[0] for row in matrix for v in row)
        minus=sum(v[1] for row in matrix for v in row)
        assert (plus,minus)==(86,129)
        for part in (0,1):
            for index,expected in ((0,(43,43)),(1,(43,86))):
                bank=matrix[index] if part==0 else [matrix[i][index] for i in range(2)]
                assert tuple(sum(v[k] for v in bank) for k in (0,1))==expected
        matrices.append(x)
    result={"status":"PASS","tile":[a,b,c],"phase_representatives":len(seen),
            "label_map_determinant_mod43":determinant,"vertex_increments_checked":increments,
            "old_four_cell_parameters_checked":matrices,
            "standard_odd_sign_populations":[86,129],
            "scope":"Exact coordinate and complete-population-cap audit only; no physical tiling or target exclusion.",
            "full_5063_excluded":False}
    (HERE/"PHASE_COORDINATES_REPLAY.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    if not __debug__:raise SystemExit("Run with assertions enabled.")
    main()
