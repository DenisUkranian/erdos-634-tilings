#!/usr/bin/env python3
"""Independent exact 14-tile balanced terminal patch with two parent tiles.

This refutes the unrestricted local lower bound parent_count >= 2b.
It does not settle the corresponding bound at either target shape.
"""
from collections import Counter,defaultdict
from fractions import Fraction as F
from math import gcd,lcm
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))
NODE_LABELS=((-7,2,2,1),(-7,2,4,-1),(-7,7,1,-1),(-5,-8,1,-1),
             (-5,-3,1,-1),(-5,-3,5,-1),(-5,-3,5,1),(-4,2,2,-1),
             (-4,2,2,1),(-4,2,4,-1),(-4,7,4,-1),(-2,-8,4,-1),
             (-2,-3,1,-1),(-2,-3,5,1))
PARENT_VERTICES=(((F(-4),F(12)),(F(-4),F(5)),(F(-13,7),F(60,7))),
                 ((F(-5),F(-13)),(F(-5),F(-6)),(F(-50,7),F(-67,7))))


def add(p,q):return p[0]+q[0],p[1]+q[1]
def sub(p,q):return p[0]-q[0],p[1]-q[1]
def scale(k,p):return k*p[0],k*p[1]
def mul(p,q):return p[0]*q[0]-p[1]*q[1],p[0]*q[1]+p[1]*q[0]+p[1]*q[1]
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def norm(p):return p[0]*p[0]+p[0]*p[1]+p[1]*p[1]
def integral(p):return all(F(x).denominator==1 for x in p)
def conjugate(p):return p[0]+p[1],-p[1]
def edges(poly):return list(zip(poly,poly[1:]+poly[:1]))
def area2(poly):return sum(det(p,q) for p,q in edges(poly))


def ccw(poly):
    poly=tuple((F(x),F(y)) for x,y in poly)
    return poly if area2(poly)>0 else poly[::-1]


def triangle(q,h,j,s):
    z=(F(5,7),F(3,7));zi=(F(8,7),F(-3,7))
    factor=(F(1),F(0)) if h==0 else z if h==1 else zi
    return ccw((q,add(q,scale(-5,mul(factor,U[j]))),add(q,scale(3,mul(factor,U[(j+s)%6])))))


def separated(A,B):
    return any(max(det(sub(q,p),sub(v,p)) for v in other)<=0
               for poly,other in ((A,B),(B,A)) for p,q in edges(poly))


def line_key(p,q):
    dx,dy=sub(q,p);den=lcm(dx.denominator,dy.denominator)
    x,y=int(dx*den),int(dy*den);g=gcd(abs(x),abs(y));x//=g;y//=g
    if (x,y)<(0,0):x,y=-x,-y
    return x,y,F(x*p[1]-y*p[0])


def contact(A,B):
    for p,q in edges(A):
        for r,s in edges(B):
            if line_key(p,q)!=line_key(r,s):continue
            axis=0 if p[0]!=q[0] else 1
            if max(min(p[axis],q[axis]),min(r[axis],s[axis]))<min(max(p[axis],q[axis]),max(r[axis],s[axis])):return True
    return False


def serial(poly):return [[str(x),str(y)] for x,y in poly]


def main():
    if not __debug__:raise RuntimeError('Assertions must be enabled.')
    a,b,c=5,3,7;z=(F(5,7),F(3,7));zi=(F(8,7),F(-3,7))
    node=[triangle((F(x),F(y)),0,j,s) for x,y,j,s in NODE_LABELS]
    parents=[ccw(row) for row in PARENT_VERTICES]
    all_polys=node+parents
    for poly in all_polys:
        assert area2(poly)==a*b
        assert sorted(norm(sub(q,p)) for p,q in edges(poly))==[b*b,a*a,c*c]
    pairs_checked=0
    for i,poly in enumerate(all_polys):
        for other in all_polys[:i]:assert separated(poly,other);pairs_checked+=1
    signs=Counter(s*(-1)**j for x,y,j,s in NODE_LABELS)
    assert signs==Counter({1:7,-1:7})
    assert all(integral(point) for poly in node for point in poly)
    assert all(integral(mul(point,z)) for poly in parents for point in poly)
    parent_labels=[]
    for poly in parents:
        matches=[]
        for q in poly:
            for j in range(6):
                for s in (-1,1):
                    if set(triangle(q,-1,j,s))==set(poly):matches.append((q,-1,j,s))
        assert len(matches)==1;parent_labels+=matches
    assert sum(t[3]*(-1)**t[2] for t in parent_labels)==0
    # Exact whole half-turn pairing outside the one allowed parent gate.
    label_set=set(NODE_LABELS);long_groups=defaultdict(list);outside=0
    for i,(x,y,j,s) in enumerate(NODE_LABELS):
        u=(x-a*U[j][0],y-a*U[j][1]);w=(x+b*U[(j+s)%6][0],y+b*U[(j+s)%6][1])
        long_groups[tuple(sorted((u,w)))].append(i)
        allowed=s==-1 and (a*u[0]-b*u[1])%c==0
        if not allowed:
            outside+=1
            mate=(x-a*U[j][0]+b*U[(j+s)%6][0],y-a*U[j][1]+b*U[(j+s)%6][1],(j+3)%6,s)
            assert mate in label_set
    long_pairs=[ids for ids in long_groups.values() if len(ids)==2]
    long_singles=[ids[0] for ids in long_groups.values() if len(ids)==1]
    assert len(long_pairs)==4 and len(long_singles)==6
    for i in long_singles:
        x,y,j,s=NODE_LABELS[i];u=(x-a*U[j][0],y-a*U[j][1])
        assert s==-1 and (a*u[0]-b*u[1])%c==0
    # The node's complete short current is canceled by the two parent long edges.
    currents=Counter()
    for index,poly in enumerate(all_polys):
        for p,q in edges(poly):
            is_long=norm(sub(q,p))==c*c
            if (index<len(node) and is_long) or (index>=len(node) and not is_long):continue
            line=line_key(p,q);currents[line,p]+=1;currents[line,q]-=1
    assert not any(currents.values())
    # The complete physical patch is connected through positive-length contacts.
    adjacency={i:[] for i in range(len(all_polys))}
    for i,poly in enumerate(all_polys):
        for j,other in enumerate(all_polys[:i]):
            if contact(poly,other):adjacency[i].append(j);adjacency[j].append(i)
    seen={0};todo=[0]
    while todo:
        for j in adjacency[todo.pop()]:
            if j not in seen:seen.add(j);todo.append(j)
    assert len(seen)==len(all_polys)
    # Reflect to put the parent at height+1, then choose a nonnative node shift.
    shift=add(z,(35,14));assert integral(mul(shift,zi)) and not integral(shift)
    physical=[ccw([add(conjugate(point),shift) for point in poly]) for poly in all_polys]
    board=ccw(((0,0),(49,0),scale(55,mul(z,z))))
    strict_determinants=[det(sub(q,p),sub(v,p)) for p,q in edges(board) for poly in physical for v in poly]
    assert min(strict_determinants)>0
    assert all(integral(sub(v,shift)) for poly in physical[:14] for v in poly)
    assert all(integral(mul(v,zi)) for poly in physical[14:] for v in poly)
    report=dict(status='PASS',tile=[a,b,c],balanced_terminal_population=14,parent_population=2,
                claimed_universal_floor_2b=6,node_signs=dict(signs),whole_long_pairs=4,
                unmatched_long_edges=6,outside_parent_gate_tiles_checked=outside,
                exact_triangle_pair_checks=pairs_checked,positive_length_contact_connected=True,
                node_class='z+R at short height0',parent_class='zR at short height1',
                strict_containment_in_original_143_path_board=True,
                minimum_containment_determinant=str(min(strict_determinants)),
                full_3431_excluded=False,full_5063_excluded=False,
                scope=__doc__,node_labels=[list(t) for t in NODE_LABELS],
                normalized_parent_polygons=[serial(p) for p in parents],
                shift=[str(v) for v in shift],physical_polygons=[serial(p) for p in physical],
                board=serial(board))
    (HERE/'BALANCED_TWO_PARENT_CONTROL.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('node_labels','normalized_parent_polygons','physical_polygons','board')},indent=2))


if __name__=='__main__':main()
