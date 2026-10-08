#!/usr/bin/env python3
"""Independent exact finite controls for the proved general addition rule."""
from fractions import Fraction as F
from math import gcd
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def need(x, message):
    if not x:
        raise RuntimeError(message)


def add(p, q): return p[0]+q[0], p[1]+q[1]
def sub(p, q): return p[0]-q[0], p[1]-q[1]
def mul(k, p): return k*p[0], k*p[1]
def det(p, q): return p[0]*q[1]-p[1]*q[0]
def norm(p, D): return p[0]*p[0]+D*p[1]*p[1]


def area2(poly):
    return sum(det(poly[i], poly[(i+1) % len(poly)]) for i in range(len(poly)))


def ccw(poly):
    return poly if area2(poly)>0 else poly[::-1]


def inside(p, triangle):
    return all(det(sub(triangle[(i+1)%3],triangle[i]),sub(p,triangle[i]))>=0
               for i in range(3))


def separated(p, q):
    for first, second in [(p,q),(q,p)]:
        for i, a in enumerate(first):
            e=sub(first[(i+1)%len(first)],a)
            if all(det(e,sub(b,a))<=0 for b in second):
                return True
    return False


def geometry(u, v, T, branch):
    a,b,c=u*v,v*v-u*u,v*v
    D=4*v*v-u*u
    Q,P=2*v*v-u*u,3*v*v-u*u
    coefficient=Q if branch=='W' else P
    # Original beta corner is zero. Move the other vertex to the origin
    # to match the abstract addition partition in the proof.
    corner=(F(u*P,2),F(b,2))
    A=sub((F(u*coefficient),F(0)),corner)
    B=mul(-1,corner)
    O=(F(0),F(0))
    r,s=v,T
    outer=ccw([O,mul(r+s,A),mul(r+s,B)])
    first=ccw([O,mul(r,A),mul(r,B)])
    second=ccw([mul(r,A),mul(r+s,A),add(mul(r,A),mul(s,B))])
    para=ccw([mul(r,A),mul(r,B),mul(r+s,B),add(mul(r,A),mul(s,B))])
    pieces=[first,second,para]
    need(all(inside(p,outer) for poly in pieces for p in poly),'Containment')
    need(all(separated(pieces[i],pieces[j]) for i in range(3) for j in range(i)),'Overlap')
    need(sum(area2(p) for p in pieces)==area2(outer),'Area partition')
    e1=mul(F(r,coefficient),sub(B,A))
    e2=mul(F(s,T*v),B)
    need(norm(e1,D)==a*a and norm(e2,D)==c*c and norm(sub(e1,e2),D)==b*b,
         'Parallelogram cell not the original tile')
    tile_area2=abs(det(e1,e2))
    expected=[coefficient*v*v,coefficient*T*T,2*coefficient*T*v]
    need([area2(poly)/tile_area2 for poly in pieces]==expected,'Piece counts')
    need(area2(outer)/tile_area2==coefficient*(T+v)**2,'Outer count')


def conductor(u):
    C=u*((u+1)//2)+1
    bound=2*C+3*u
    generated=set()
    for p in range(bound//(u+2)+1):
        for q in range(bound//(u+1)+1):
            if p+q==0: continue
            seed=p*(u+2)+q*(u+1)
            generated.update(range(seed,bound+1,u))
    w=[u*((u+1)//2)+u]+[u*((j+1)//2)+j for j in range(1,u)]
    need(all((n in generated)==(n>=w[n%u]) for n in range(1,bound+1)),'Apery set')
    need(C-1 not in generated and all(n in generated for n in range(C,bound+1)),'Conductor')
    old=3 if u==2 else u*u-u if u%2==0 else u*u+1
    need(C<=old,'Not an improvement')
    return dict(u=u, old_sufficient_conductor=old, new_sufficient_conductor=C,
                residue_minima=w)


def main():
    n=0
    for v in range(2,14):
        for u in range(1,v):
            if gcd(u,v)!=1: continue
            for T in range(1,9):
                for branch in ['W','beta']:
                    geometry(u,v,T,branch)
                    n+=1
    rows=[conductor(u) for u in range(2,65)]
    report=dict(status='PASS', exact_macro_checks=n, conductor_checks=rows,
                general_proof='SEED_EXTENSION.md',
                omitted_scales_not_declared_impossible=True,
                new_complete_square_class_claimed=False)
    (HERE/'seed_extension_checked.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',exact_macro_checks=n,conductor_parameters=len(rows))))


if __name__=='__main__': main()
