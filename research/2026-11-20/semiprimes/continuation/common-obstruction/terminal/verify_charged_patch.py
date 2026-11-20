#!/usr/bin/env python3
"""Exact checks for CHARGED_TERMINAL_PATCH.md; not a full F2 certificate."""
import argparse
import json
from pathlib import Path


def sub(p,q):
    return p[0]-q[0],p[1]-q[1]


def cross(p,q):
    return p[0]*q[1]-p[1]*q[0]


def norm(p):
    return p[0]*p[0]+p[0]*p[1]+p[1]*p[1]


def area2(poly):
    return sum(cross(p,poly[(i+1)%len(poly)]) for i,p in enumerate(poly))


def disjoint_open(p,q):
    for first,second in ((p,q),(q,p)):
        for i,u in enumerate(first):
            v=first[(i+1)%len(first)]
            if all(cross(sub(v,u),sub(w,u))<=0 for w in second):
                return True
    return False


def check(a,b,c):
    assert a*a+a*b+b*b==c*c
    W=(a*a,a*b); B=(c*c,0)
    macro=[((0,0),B,W)]
    for i in range(a):
        macro.append(((i*a,i*b),((i+1)*a,(i+1)*b),(i*a,(i+1)*b)))
    for i in range(b):
        p=(a*a+i*(a+b),a*b-i*a)
        macro.append((p,(p[0]+a+b,p[1]-a),(p[0]+b,p[1])))
    assert sorted(norm(sub(macro[0][(i+1)%3],macro[0][i])) for i in range(3)) == \
        sorted([a*a*c*c,b*b*c*c,c**4])
    assert area2(macro[0])==a*b*c*c
    for triangle in macro[1:]:
        assert area2(triangle)==a*b
        assert sorted(norm(sub(triangle[(i+1)%3],triangle[i])) for i in range(3)) == \
            sorted([a*a,b*b,c*c])
    for i,p in enumerate(macro):
        for q in macro[i+1:]:
            assert disjoint_open(p,q)
    total=c*c+a+b
    assert sum(map(area2,macro))==total*a*b
    negative=c*(c+1)//2; positive=c*(c-1)//2
    assert negative+positive==c*c and positive-negative==-c
    A=b*(2*a+b); H=a*(a+2*b)
    def transform(p):
        x,y=p
        return y,c*c-x-y
    for triangle in macro:
        moved=tuple(map(transform,triangle))
        assert area2(moved)==area2(triangle)
        for x,y in moved:
            assert x>=0 and y>=0 and H*x+A*y<=A*H
    roots=[r for r in range(c) if (r*r-r+1)%c==0]
    root=next(r for r in roots if (a+b*r)%c==0)
    assert (A % c)!=0
    assert all((x+root*y)%c==0 for x,y in map(transform,macro[0]))
    return {'tile':[a,b,c],'terminal_polygon_node_population':c*c,
            'terminal_polygon_node_G':-c,'parent_teeth':a+b,'partial_packing_tiles':total,
            'target_N':(a+2*b)*(2*a+b),'macro_pieces':len(macro),
            'F2_containment':'exactly verified',
            'macro_pieces_native':[
                {'kind':'standard_triangle_grid' if i==0 else 'unit_triangle',
                 'scale':c if i==0 else 1,'short_height':1 if i==0 else 0,
                 'vertices':[list(transform(p)) for p in triangle]}
                for i,triangle in enumerate(macro)],
            'scope':'The polygon is tiled. The F2 packing is partial; completion and continued terminality are not claimed.'}


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Run without -O.')
    parser=argparse.ArgumentParser()
    parser.add_argument('--write-certificate',action='store_true')
    args=parser.parse_args()
    cases=[check(33,7,37),check(35,13,43)]
    path=Path(__file__).with_name('charged_patch_certificate.json')
    if args.write_certificate:
        path.write_text(json.dumps(cases,indent=2)+'\n')
    elif path.exists():
        assert json.loads(path.read_text())==cases
    print(json.dumps([{k:v for k,v in row.items() if k!='macro_pieces_native'}
                      for row in cases],indent=2))
