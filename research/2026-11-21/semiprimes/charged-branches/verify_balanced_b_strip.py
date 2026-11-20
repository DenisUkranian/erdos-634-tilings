#!/usr/bin/env python3
"""Exact local balanced strip with 2b parent teeth, not a full F2 tiling.

This is an obstruction to inferring a 2a-parent lower bound from local
mixed-cycle geometry alone. No completion or universal full-tiling
counterexample is claimed.
"""
import argparse
from collections import Counter,defaultdict
from fractions import Fraction as F
import json
from pathlib import Path

U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))


def add(p,q): return p[0]+q[0],p[1]+q[1]
def sub(p,q): return p[0]-q[0],p[1]-q[1]
def scale(k,p): return k*p[0],k*p[1]
def mul(p,q):
    x,y=p;v,w=q
    return x*v-y*w,x*w+y*v+y*w
def norm(p): return p[0]*p[0]+p[0]*p[1]+p[1]*p[1]
def det(p,q): return p[0]*q[1]-p[1]*q[0]
def area2(poly):return sum(det(poly[i],poly[(i+1)%len(poly)]) for i in range(len(poly)))
def contains(poly,q,strict=False):
    values=[det(sub(poly[(i+1)%len(poly)],poly[i]),sub(q,poly[i])) for i in range(len(poly))]
    return all(v>0 for v in values) if strict else all(v>=0 for v in values)
def disjoint_interiors(p,q):
    return any(all(det(sub(poly[(i+1)%3],poly[i]),sub(v,poly[i]))<=0 for v in other) for poly,other in ((p,q),(q,p)) for i in range(3))
def integral(p):return all(F(v).denominator==1 for v in p)
def serial(p):return [str(F(v)) for v in p]


def verify(a,b,c):
    assert a*a+a*b+b*b==c*c
    z=(F(a,c),F(b,c));zinv=(F(a+b,c),F(-b,c))
    shift=add(z,(22*c,3*c))
    across=(a,b);along=(0,b*c)
    region=(shift,add(shift,across),add(add(shift,across),along),add(shift,along))
    B=a*(a+2*b)
    board=((F(0),F(0)),(F(c*c),F(0)),scale(B,mul(z,z)))
    assert area2(board)>0 and area2(region)==2*a*b*c
    placements=[]
    def insert(q,h,j,s,role):
        factor=(F(1),F(0)) if h==0 else z
        u=add(q,scale(-a,mul(factor,U[j])))
        w=add(q,scale(b,mul(factor,U[(j+s)%6])))
        polygon=(u,q,w) if s==1 else (u,w,q)
        assert area2(polygon)==a*b
        lengths=sorted(norm(sub(polygon[(i+1)%3],polygon[i])) for i in range(3))
        assert lengths==sorted((a*a,b*b,c*c))
        assert all(contains(board,p,strict=True) for p in polygon)
        if role=='interior':
            assert h==0 and all(integral(sub(p,shift)) for p in polygon)
            assert all(contains(region,p) for p in polygon)
        else:
            assert h==1 and all(integral(mul(zinv,p)) for p in polygon)
        placements.append({'q':q,'h':h,'j':j,'s':s,'sign':s*(-1 if j%2 else 1),'role':role,'vertices':polygon,'long':tuple(sorted((u,w)))})
    for k in range(c):
        insert(add(shift,(0,(k+1)*b)),0,3,1,'interior')
        insert(add(shift,(a,(k+1)*b)),0,0,1,'interior')
    for k in range(b):
        beta=add(shift,(0,(k+1)*c))
        insert(sub(beta,scale(b,z)),1,1,-1,'left_bank')
        beta=add(add(shift,across),(0,k*c))
        insert(add(beta,scale(b,z)),1,4,-1,'right_bank')
    for i,p in enumerate(placements):
        for q in placements[i+1:]:
            assert disjoint_interiors(p['vertices'],q['vertices'])
    interiors=[p for p in placements if p['role']=='interior']
    banks=[p for p in placements if p['role']!='interior']
    assert len(interiors)==2*c and len(banks)==2*b
    assert Counter(p['sign'] for p in interiors)==Counter({1:c,-1:c})
    assert Counter(p['sign'] for p in banks)==Counter({1:b,-1:b})
    assert sum(area2(p['vertices']) for p in interiors)==area2(region)
    long=defaultdict(list)
    for p in interiors:long[p['long']].append(p)
    assert Counter(len(v) for v in long.values())==Counter({2:c-1,1:2})
    for pair in long.values():
        if len(pair)==2:
            p,q=pair
            assert p['sign']==-q['sign'] and p['s']==q['s']
            assert p['j']==(q['j']+3)%6
            ends=p['long']
            assert add(p['q'],q['q'])==add(ends[0],ends[1])
    for k in range(b):
        left=placements[2*c+2*k];right=placements[2*c+2*k+1]
        assert left['long']==tuple(sorted((add(shift,(0,k*c)),add(shift,(0,(k+1)*c)))))
        assert right['long']==tuple(sorted((add(add(shift,across),(0,k*c)),add(add(shift,across),(0,(k+1)*c)))))
    assert integral(mul(zinv,shift)) and not integral(shift)
    # This exact class is L_1^-=z+R in the path-frame normal form.
    assert integral(sub(shift,z))
    N=(2*a+b)*(a+2*b)
    summary={'tile':[a,b,c],'N':N,'status':'PASS','interior_tiles':2*c,'interior_charge':0,'interior_signs':{'+':c,'-':c},'interior_whole_long_pairs':c-1,'interior_unmatched_long_sides':2,'actual_parent_tiles':2*b,'parent_signs':{'+':b,'-':b},'parent_short_height':1,'interior_short_height':0,'interior_class':'z+R (nonnative)','parent_class':'zR (native)','strict_board_containment':True,'all_pairwise_interiors_disjoint':True,'scope':__doc__}
    certificate={'summary':summary,'shift':serial(shift),'region':[serial(p) for p in region],'board':[serial(p) for p in board],'placements':[dict(q=serial(p['q']),h=p['h'],j=p['j'],s=p['s'],sign=p['sign'],role=p['role'],vertices=[serial(v) for v in p['vertices']]) for p in placements]}
    return summary,certificate


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out-dir',type=Path,default=Path(__file__).resolve().parent);args=p.parse_args()
    reports=[]
    for shape in ((33,7,37),(35,13,43)):
        report,certificate=verify(*shape);reports.append(report)
        (args.out_dir/f"balanced_b_strip_{report['N']}.json").write_text(json.dumps(certificate,indent=2)+'\n')
    (args.out_dir/'BALANCED_B_STRIP_REPLAY.json').write_text(json.dumps(reports,indent=2)+'\n')
    print(json.dumps(reports,indent=2))
