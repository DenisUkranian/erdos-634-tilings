#!/usr/bin/env python3
"""Independent exact replay of an all-remote-balanced population certificate.

No LP/model generator is imported. Every translated CCW triangle is rebuilt
from its two short sides, and the resulting integer column score is checked.
The two complete 143 controls separately validate the projection semantics.
"""
from pathlib import Path
from fractions import Fraction
from collections import Counter
import argparse,json,sys,hashlib

HERE=Path(__file__).resolve().parent
U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))

def det(p,q):return p[0]*q[1]-p[1]*q[0]
def diff(p,q):return p[0]-q[0],p[1]-q[1]
def polygon(a,b,q,j,s):
    u=(q[0]-a*U[j][0],q[1]-a*U[j][1])
    w=(q[0]+b*U[(j+s)%6][0],q[1]+b*U[(j+s)%6][1])
    vertices=[u,q,w] if s==1 else [w,q,u]
    assert sum(det(p,r)for p,r in zip(vertices,vertices[1:]+vertices[:1]))==a*b
    return vertices,u

def short_edges(a,b,c,vertices):
    result=[]
    for p,r in zip(vertices,vertices[1:]+vertices[:1]):
        x,y=diff(r,p);n=x*x+x*y+y*y
        if n==c*c:continue
        assert n in(a*a,b*b)
        length=a if n==a*a else b
        axes=[k for k in range(3)if (x,y)in((length*U[k][0],length*U[k][1]),(-length*U[k][0],-length*U[k][1]))]
        assert len(axes)==1
        result.append((axes[0],p,r))
    assert len(result)==2
    return result

def gate(a,b,c,u,s):
    return ((a*u[1]-b*u[0]) if s>0 else (a*u[0]-b*u[1]))%c

def certificate_check(cert):
    a,b,c=cert['tile'];assert a*a+a*b+b*b==c*c
    D=cert['D'];t=cert['charge_multiplier_t'];F=cert['endpoint_tables']
    up=cert['up_remote_weights'];down=cert['down_remote_weights']
    assert isinstance(D,int)and D>0 and isinstance(t,int)
    assert len(up)==len(down)==c and up[0]==down[0]==0
    assert len(F)==3 and all(len(table)==c and all(len(row)==c for row in table)for table in F)
    assert all(isinstance(v,int)for table in F for row in table for v in row)
    assert all(isinstance(v,int)for v in up+down)
    minscore=maxscore=None;columns=0
    for x in range(c):
        for y in range(c):
            for j in range(6):
                for s in(-1,1):
                    vertices,u=polygon(a,b,(x,y),j,s)
                    W=0
                    for axis,p,r in short_edges(a,b,c,vertices):
                        W+=F[axis][r[0]%c][r[1]%c]-F[axis][p[0]%c][p[1]%c]
                    eps=s*(-1 if j%2 else 1)
                    r=gate(a,b,c,u,s)
                    score=W+eps*((up if s>0 else down)[r]+t)
                    assert score<=D,(a,b,c,x,y,j,s,score,D)
                    minscore=score if minscore is None else min(minscore,score)
                    maxscore=score if maxscore is None else max(maxscore,score)
                    columns+=1
    lower=Fraction(c*t,D)
    return {'tile':[a,b,c],'exact_columns':columns,'minimum_score':minscore,'maximum_score':maxscore,
            'column_upper_bound_D':D,'charge_multiplier_t':t,'population_lower_bound_at_G_c':str(lower),
            'strictly_excludes_population_3c':t>3*D,'status':'PASS'}

def find_continuation():
    for ancestor in HERE.parents:
        for p in(ancestor,ancestor/'repo/research/2026-11-20/semiprimes/continuation'):
            if(p/'global-endpoints/integer/global_core_sat.py').exists():return p
    raise FileNotFoundError('Pass --continuation.')

def check_controls(continuation,macro):
    sys.path.insert(0,str(continuation/'global-endpoints/integer'))
    from global_core_sat import Geometry
    g=Geometry(5,3,7);a,b,c=g.a,g.b,g.c
    out=[]
    for source in(continuation/'global-endpoints/tiling_143.json',macro):
        raw=json.loads(source.read_text())
        if 'tiles'in raw:tiles=[(tuple(t[0]),*t[1:])for t in raw['tiles']]
        else:
            D=raw['denominator'];e=0
            while c**e<D:e+=1
            assert c**e==D;tiles=[]
            for triangle in raw['triangles']:
                corners={g.point(x,y,e)for x,y in triangle};found=[]
                for q in corners:
                    for h in(0,1):
                        for j in range(6):
                            for s in(-1,1):
                                tile=q,h,j,s
                                if set(g.vertices(tile))==corners:found.append(tile)
                assert len(found)==1;tiles.append(found[0])
        assert len(tiles)==143 and len(set(tiles))==143
        C=g.scale(g.B,g.unit(2,0));current=Counter();Qup=Counter();Qdown=Counter();signed=population=0
        for q,h,j,s in tiles:
            if h!=1:continue
            qc=q[0]+q[1],-q[1],q[2]
            q=g.sub(C,g.mult(g.unit(2,1),qc));j=(4-j)%6;s=-s
            q=g.mult(q,g.unit(-1,0));assert q[2]==0
            vertices,u=polygon(a,b,q[:2],j,s)
            for axis,p,r in short_edges(a,b,c,vertices):
                current[axis,p[0]%c,p[1]%c]-=1
                current[axis,r[0]%c,r[1]%c]+=1
            eps=s*(-1 if j%2 else 1);signed+=eps;population+=1
            (Qup if s>0 else Qdown)[gate(a,b,c,u,s)]+=eps
        assert signed==c and all(value==0 for value in current.values())
        assert {r:v for r,v in Qup.items()if v}=={0:2*c}
        assert {r:v for r,v in Qdown.items()if v}=={0:-c}
        out.append({'source':source.name,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                    'population':population,'signed_charge':signed,'native_up_current':Qup[0],
                    'native_down_current':Qdown[0],'all_remote_signed_currents_zero':True,
                    'all_short_endpoint_rows_zero':True,'status':'PASS'})
    return out

def main():
    p=argparse.ArgumentParser();p.add_argument('certificate',type=Path)
    p.add_argument('--continuation',type=Path);p.add_argument('--macro',type=Path)
    p.add_argument('--out',type=Path,default=HERE/'REMOTE_ZERO_MINIMUM_REPLAY.json');args=p.parse_args()
    raw=json.loads(args.certificate.read_text());cert=raw.get('certificate',raw)
    report={'certificate':certificate_check(cert)}
    continuation=args.continuation or find_continuation()
    if args.macro:macro=args.macro
    else:
        candidates=[HERE/'macro143_certificate.json',HERE.parents[1]/'charge-transport/geometry/macro143_certificate.json',continuation/'charge-transport/geometry/macro143_certificate.json']
        macro=next(p for p in candidates if p.exists())
    report['positive_143_projection_controls']=check_controls(continuation,macro)
    report['scope']='Exact population inequality under zero remote signed gate currents; neither target is globally excluded.'
    args.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

if __name__=='__main__':
    if not __debug__:raise SystemExit('Run without -O.')
    main()
