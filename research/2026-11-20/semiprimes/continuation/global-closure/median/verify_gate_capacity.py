#!/usr/bin/env python3
"""Independent exact gate-capacity replay; Python standard library only.

Reconstructs CCW short edges for every q in (Z/cZ)^2 and all 12 shapes.
Does not import either LP/model generator. Tests two complete 143 controls.
"""
from pathlib import Path
from fractions import Fraction
from collections import Counter
import argparse,hashlib,json,sys

HERE=Path(__file__).resolve().parent
U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))

def cross(p,q):return p[0]*q[1]-p[1]*q[0]
def diff(p,q):return p[0]-q[0],p[1]-q[1]
def phi(a,b,c,p):return (a*p[1]-b*p[0])%c

def weight(certificate,q,j,s):
    a,b,c=certificate['tile'];F=certificate['endpoint_tables']
    u=(q[0]-a*U[j][0],q[1]-a*U[j][1])
    w=(q[0]+b*U[(j+s)%6][0],q[1]+b*U[(j+s)%6][1])
    polygon=[u,q,w] if s==1 else [w,q,u]
    assert sum(cross(p,r)for p,r in zip(polygon,polygon[1:]+polygon[:1]))==a*b
    result=0;shorts=0
    for p,r in zip(polygon,polygon[1:]+polygon[:1]):
        x,y=diff(r,p);norm=x*x+x*y+y*y
        if norm==c*c:continue
        assert norm in (a*a,b*b)
        length=a if norm==a*a else b
        axes=[k for k in range(3) if (x,y) in ((length*U[k][0],length*U[k][1]),(-length*U[k][0],-length*U[k][1]))]
        assert len(axes)==1;axis=axes[0];shorts+=1
        result+=F[axis][phi(a,b,c,r)]-F[axis][phi(a,b,c,p)]
    assert shorts==2
    eps=s*(-1 if j%2 else 1)
    gate=(s==1 and phi(a,b,c,u)==0)
    return result,eps,gate

def verify_certificate(cert):
    a,b,c=cert['tile'];D=cert['denominator'];P=cert['positive_coefficient'];M=cert['negative_coefficient']
    assert a*a+a*b+b*b==c*c and D>0 and P+M==D
    F=cert['endpoint_tables'];assert len(F)==3 and all(len(row)==c for row in F)
    minimum=None;columns=0
    for x in range(c):
        for y in range(c):
            for j in range(6):
                for s in (-1,1):
                    v,eps,gate=weight(cert,(x,y),j,s)
                    slack=v+(P if eps>0 else M)-D*(eps>0 and gate)
                    assert slack>=0,(a,b,c,x,y,j,s,slack)
                    minimum=slack if minimum is None else min(minimum,slack)
                    columns+=1
    capacity=Fraction(c*(2*P+M),D)
    nmax=3*c//(a-b)
    remaining=([n for n in range(nmax+1) if 2*c-(a-b)*n<=capacity]
               if (a,b,c) in ((33,7,37),(35,13,43)) else None)
    return {'tile':[a,b,c],'exact_two_dimensional_columns':columns,
            'minimum_integer_slack':minimum,'capacity_at_populations_2c_c':str(capacity),
            'integer_gate_capacity':capacity.numerator//capacity.denominator,
            'remaining_upper_parameters_under_3c':remaining,
            'status':'PASS'}

def find_continuation():
    for ancestor in HERE.parents:
        for candidate in (ancestor,ancestor/'repo/research/2026-11-20/semiprimes/continuation'):
            if (candidate/'global-endpoints/integer/global_core_sat.py').exists():return candidate
    raise FileNotFoundError('Pass --continuation.')

def full_controls(cert,continuation,macro):
    # Reconstruct Geometry placements independently from the macro triangles.
    sys.path.insert(0,str(continuation/'global-endpoints/integer'))
    from global_core_sat import Geometry
    g=Geometry(*cert['tile']);assert g.N==143
    sources=[('repository',continuation/'global-endpoints/tiling_143.json'),('macro',macro)]
    result=[]
    for name,source in sources:
        data=json.loads(source.read_text())
        if 'tiles' in data:tiles=[(tuple(t[0]),*t[1:])for t in data['tiles']]
        else:
            denominator=data['denominator'];e=0
            while g.c**e<denominator:e+=1
            assert g.c**e==denominator
            tiles=[]
            for raw in data['triangles']:
                vs={g.point(x,y,e)for x,y in raw};found=[]
                for q in vs:
                    for h in (0,1):
                        for j in range(6):
                            for s in(-1,1):
                                t=q,h,j,s
                                if set(g.vertices(t))==vs:found.append(t)
                assert len(found)==1;tiles.append(found[0])
        assert len(tiles)==143 and len(set(tiles))==143
        C=g.scale(g.B,g.unit(2,0))
        transformed=[]
        for q,h,j,s in tiles:
            qc=(q[0]+q[1],-q[1],q[2])
            qp=g.sub(C,g.mult(g.unit(2,1),qc))
            transformed.append((qp,2-h,(4-j)%6,-s))
        selected=[t for t in transformed if t[1]==1]
        nplus=nminus=gate=total=0
        for q,h,j,s in selected:
            q0=g.mult(q,g.unit(-1,0));assert q0[2]==0
            v,eps,isgate=weight(cert,q0[:2],j,s);total+=v
            nplus+=eps>0;nminus+=eps<0;gate+=eps>0 and isgate
        assert total==0
        rhs=cert['positive_coefficient']*nplus+cert['negative_coefficient']*nminus
        assert cert['denominator']*gate<=rhs
        # All actual positive upper-median banks must satisfy this, but the
        # complete gated population can contain additional paired tiles.
        result.append({'source':name,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                       'height_one_population':len(selected),'positive':nplus,'negative':nminus,
                       'positive_native_up_gate_population':gate,
                       'exact_endpoint_sum':total,'capacity':str(Fraction(rhs,cert['denominator'])),
                       'status':'PASS'})
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('--certificates',type=Path,default=HERE/'gate_capacity_certificates.json')
    p.add_argument('--continuation',type=Path);p.add_argument('--macro',type=Path)
    p.add_argument('--out',type=Path,default=HERE/'GATE_CAPACITY_REPLAY.json');args=p.parse_args()
    certs=json.loads(args.certificates.read_text());report={'certificates':[verify_certificate(c)for c in certs]}
    continuation=args.continuation or find_continuation()
    if args.macro:macro=args.macro
    else:
        candidates=[HERE/'macro143_certificate.json',HERE.parents[1]/'charge-transport/geometry/macro143_certificate.json',continuation/'global-closure/median/macro143_certificate.json',continuation/'charge-transport/geometry/macro143_certificate.json']
        macro=next(path for path in candidates if path.exists())
    report['complete_143_controls']=full_controls(next(c for c in certs if c['tile']==[5,3,7]),continuation,macro)
    report['scope']='Exact universal endpoint gate capacities and positive controls; no global target exclusion.'
    args.out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    if not __debug__:raise SystemExit('Run without -O.')
    main()
