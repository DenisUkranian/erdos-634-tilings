#!/usr/bin/env python3
"""Exact integer checks for a native two-height residue dual and a full 143 control."""
from collections import Counter
from pathlib import Path
import argparse,json,sys
U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))
def add(p,q,c):return((p[0]+q[0])%c,(p[1]+q[1])%c)
def mul(k,p,c):return(k*p[0]%c,k*p[1]%c)
def events(a,b,c,j,s,q):
    u=add(q,mul(-a,U[j],c),c);v=add(q,mul(b,U[(j+s)%6],c),c)
    return (((j%3,q),s),((j%3,u),-s),(((j+s)%3,v),s),(((j+s)%3,q),-s))
def pair_events(a,b,c,j,s,q):
    mate=add(add(q,mul(-a,U[j],c),c),mul(b,U[(j+s)%6],c),c)
    return events(a,b,c,j,s,q)+events(a,b,c,(j+3)%6,s,mate)
def root(a,b,c):return next(r for r in range(c)if(r*r-r+1)%c==0 and(a+b*r)%c==0)
def gate(a,b,c,j,q):
    u=add(q,mul(-a,U[j],c),c);r=root(a,b,c)
    return(u[0]+r*u[1])%c==0

def check_dual(case):
    a,b,c=case['tile'];D=case['denominator'];f=case['weights'];assert D>0 and len(f)==3*c*c+1
    def value(es):return sum(v*f[j*c*c+q[0]*c+q[1]]for(j,q),v in es)
    singles=pairs=0;required=0
    for j in range(6):
      for x in range(c):
       for y in range(c):
        q=x,y
        if gate(a,b,c,j,q):
         v=value(events(a,b,c,j,1,q))+(-1)**j*f[-1]
         required=max(required,v);assert v<=D,(j,q,v,D);singles+=1
    for s in(-1,1):
     for j in range(3):
      for x in range(c):
       for y in range(c):
        v=value(pair_events(a,b,c,j,s,(x,y)))
        required=max(required,-(-v//2));assert v<=2*D,(s,j,x,y,v,D);pairs+=1
    base=sum(value(events(a,b,c,0,-1,((i*(a+b)+a)%c,(-i*b)%c)))for i in range(c))
    numerator=c*D-base+2*c*f[-1]
    blocks=-(-numerator//(D*c))
    if blocks%2==0:blocks+=1
    return dict(tile=[a,b,c],single_checks=singles,pair_checks=pairs,lower_numerator=numerator,lower_denominator=D,odd_c_multiple_bound=blocks*c,required_denominator=required)

def check_known_143(base):
    base=Path(base);sys.path[:0]=[str(base/'global-endpoints/integer')]
    from global_core_sat import Geometry
    g=Geometry(5,3,7);a,b,c=g.a,g.b,g.c
    data=json.loads((base/'global-endpoints/tiling_143.json').read_text())
    rho=g.unit(0,1);z2=g.unit(2,0);shift=g.scale(a*(a+2*b),z2)
    tiles=set()
    for q,h,j,s in data['tiles']:
        barq=(q[0]+q[1],-q[1],q[2])
        qn=g.sub(shift,g.mult(g.mult(rho,z2),barq))
        # Coordinates after rotation by 1/z; h1 anchors must be integral.
        qr=g.mult(qn,g.unit(-1,0));H=2-h;J=(4-j)%6;S=-s
        if H==1:
            assert qr[2]==0,qr
            tiles.add((qr[:2],J,S))
        else:
            assert H==2 and g.mult(qn,g.unit(-2,0))[2]==0
    base_tiles={(((i*(a+b)+a),(-i*b)),0,-1)for i in range(c)}
    assert base_tiles<=tiles
    assert len(tiles)==105
    assert sum(s*(-1)**j for q,j,s in tiles)==c
    residual=Counter();singles=Counter();pairs=Counter();seen=set(base_tiles)
    for q,j,s in base_tiles:
        for key,v in events(a,b,c,j,s,(q[0]%c,q[1]%c)):residual[key]+=v
    for t in sorted(tiles-base_tiles):
        if t in seen:continue
        q,j,s=t;qm=(q[0]%c,q[1]%c)
        if s==1 and gate(a,b,c,j,qm):
            singles[j,qm]+=1;seen.add(t)
            for key,v in events(a,b,c,j,s,qm):residual[key]+=v
        else:
            mateq=(q[0]-a*U[j][0]+b*U[(j+s)%6][0],q[1]-a*U[j][1]+b*U[(j+s)%6][1])
            mate=(mateq,(j+3)%6,s)
            assert mate in tiles and mate not in base_tiles,(t,mate)
            assert mate not in seen,(t,mate)
            if j>=3:q,j=mateq,j-3
            qm=q[0]%c,q[1]%c;pairs[j,s,qm]+=1;seen.update((t,mate))
            for key,v in pair_events(a,b,c,j,s,qm):residual[key]+=v
    assert seen==tiles and not any(residual.values())
    assert len(base_tiles)+sum(singles.values())+2*sum(pairs.values())==105
    assert sum((-1)**j*n for(j,q),n in singles.items())==2*c
    return dict(N=143,native_h1=105,native_h2=38,base_teeth=len(base_tiles),single_up=sum(singles.values()),interior_pairs=sum(pairs.values()),exact_torus_residual=0)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('certificates',nargs='*');p.add_argument('--known-base');args=p.parse_args()
    if args.known_base:print(json.dumps(check_known_143(args.known_base)))
    for path in args.certificates:print(json.dumps(check_dual(json.loads(Path(path).read_text()))))
