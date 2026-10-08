#!/usr/bin/env python3
"""Decode the five-variable residual solution, independently checking geometry."""
import collections
from fractions import Fraction as F
import itertools
import json
from pathlib import Path
import re
import struct

HERE = Path(__file__).resolve().parent

def add(p,q): return (p[0]+q[0],p[1]+q[1])
def sub(p,q): return (p[0]-q[0],p[1]-q[1])
def mul(p,q): return (p[0]*q[0]-p[1]*q[1],p[0]*q[1]+p[1]*q[0]+p[1]*q[1])
def rot(p): return (-p[1],p[0]+p[1])
def scale(p,n): return (p[0]*n,p[1]*n)
def cross(p,q): return p[0]*q[1]-p[1]*q[0]
def norm(p): return p[0]**2+p[0]*p[1]+p[1]**2
def determinant(t): return cross(sub(t[1],t[0]),sub(t[2],t[0]))
def edge_pairs(p): return zip(p,p[1:]+p[:1])

def overlap(a,b):
    # Separation along each edge normal; equality is boundary-only contact.
    for p in (a,b):
        for x,y in edge_pairs(p):
            d=sub(y,x)
            if max(cross(d,sub(z,x)) for z in (b if p is a else a)) <= 0:
                return False
    return True

def boundary(polygons):
    # An oriented straight segment current is determined by its endpoint
    # jumps in each unoriented direction, retaining exact position.
    from math import gcd,lcm
    d=collections.Counter()
    for p in polygons:
        for a,b in edge_pairs(p):
            v=sub(b,a); den=lcm(v[0].denominator,v[1].denominator)
            x,y=int(v[0]*den),int(v[1]*den); g=gcd(x,y)
            x,y=x//g,y//g
            if x<0 or (x==0 and y<0): x,y=-x,-y
            d[(x,y,a)]+=1; d[(x,y,b)]-=1
    return {k:v for k,v in d.items() if v}

def main():
    model=(HERE/'q480_residual.pbtxt').read_text()
    constraints=[]
    for v,c,b in re.findall(r'vars:\[([^]]*)\] coeffs:\[([^]]*)\] domain:\[(-?\d+),-?\d+\]',model):
        constraints.append((list(map(int,v.split(','))),list(map(int,c.split(','))),int(b)))
    solutions=[x for x in itertools.product(range(2),repeat=5)
               if all(sum(x[i]*j for i,j in zip(v,c))==b for v,c,b in constraints)]
    assert len(solutions)==3
    mapping=list(struct.iter_unpack('iiii',(HERE/'q480_residual.mapping.bin').read_bytes()))
    templates=[]
    for h,u in ((-1,(6,-1)),(0,(5,1))):
        u=rot(u)
        for a,b in ((24,11),(11,24)):
            x,y=scale(u,a),scale(rot(rot(u)),b)
            for r in range(6):
                templates.append(((0,0),x,y)); x,y=rot(x),rot(y)
    inverse=(F(5,31),F(-6,31)) # inverse of rho*(5+rho)=(-1,6)
    q=[tuple(map(F,p)) for p in [(22,0),(528,0),(-242,242),(-48,48)]]
    x=solutions[0]
    triangles=[tuple(mul(add((ax,ay),p),inverse) for p in templates[o])
               for group,o,ax,ay in mapping if group<0 or x[group]]
    assert len(triangles)==480
    for t in triangles:
        assert determinant(t)==264
        assert sorted(norm(sub(b,a)) for a,b in edge_pairs(t))==[121,576,961]
        for v in t:
            assert all(cross(sub(b,a),sub(v,a))>=0 for a,b in edge_pairs(q))
    assert boundary(triangles)==boundary([q])
    pairs=0
    for i,a in enumerate(triangles):
        for b in triangles[:i]:
            assert not overlap(a,b),(i,b)
            pairs+=1
    cert={'format':'ERDOS634_RATIONAL_EISENSTEIN_TILING_V1','tile':[24,11,31],
          'count':480,'target':[[str(v) for v in p] for p in q],
          'triangles':[[[str(v) for v in p] for p in t] for t in triangles],
          'short_height_band':[-1,0],'residual_boolean_solution':list(x)}
    (HERE/'q480_tiling.json').write_text(json.dumps(cert,separators=(',',':'))+'\n')
    report={'status':'PASS','count':480,'pairwise_checks':pairs,'exact_lengths':True,
            'exact_containment':True,'exact_oriented_boundary':True,'pairwise_interior_disjoint':True,
            'solutions_in_compressed_model':len(solutions)}
    (HERE/'q480_verified.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))

if __name__=='__main__': main()
