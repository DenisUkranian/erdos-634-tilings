"""Exclude the two charged equality words by a forced straight wall and marked sections."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

from contours import HERE, SOURCE
from replay import compile_cpp, run
from controls_marked import controls
sys.path.insert(0,str(SOURCE.parent/'charged-contour'))
from geometry import UNITS, add, conjugate, det, multiply, repaired_boundary, scale, shapes, subtract


def polygon(a,b,c,l,word):
    chain = Counter()
    for p,q in repaired_boundary(a,b,c,l,word):
        delta = subtract(q,p)
        u = next(u for u in UNITS if det(u,delta)==0 and multiply(conjugate(u),delta)[0]>0)
        while p!=q:
            v = add(p,u)
            key = tuple(sorted((p,v)))
            chain[key] += 1 if p==key[0] else -1
            p = v
    successor = {}
    for (p,q),val in chain.items():
        if val:
            assert abs(val)==1
            if val<0:
                p,q=q,p
            assert p not in successor
            successor[p]=q
    assert set(successor)==set(successor.values())
    p=start=min(successor)
    boundary=[]
    while p in successor:
        boundary.append(p)
        p=successor.pop(p)
    assert not successor and p==start
    return [q for i,q in enumerate(boundary)
            if det(subtract(q,boundary[i-1]),subtract(boundary[(i+1)%len(boundary)],q))]


def forced_wall(a,b,c,l,points):
    for i,p in enumerate(points):
        q=points[(i+1)%len(points)]
        if subtract(q,p)!=(-l*c,l*c):
            continue
        assert det(subtract(p,points[i-1]),subtract(q,p))>0
        assert det(subtract(q,p),subtract(points[(i+2)%len(points)],q))>0
        reps=[(x,y,(l*c-x*a-y*b)//c) for x in range(l*c//a+1)
              for y in range((l*c-x*a)//b+1) if (l*c-x*a-y*b)%c==0]
        assert reps==[(0,0,l)]
        labels=[]
        for w in (-a*pow(b,-1,c),-b*pow(a,-1,c)):
            labels.append((p[0]+w*p[1])%c)
            assert labels[-1]==(q[0]+w*q[1])%c
        for h,label in zip((1,-1),labels):
            factor=(a,b) if h==1 else (a+b,-b)
            direct=[t for t in range(c)
                    if all(v%c==0 for v in multiply(conjugate(factor),subtract(p,(t,0))))]
            assert direct==[label]
        X,Y=(b*(2*a+b),0),(0,a*(a+2*b))
        assert all(v%c==0 for v in multiply(conjugate((a,b)),subtract(Y,X)))
        assert labels[0]==X[0]%c
        return dict(start=p,end=q,side_inventory=reps[0],hand_labels=labels)
    raise AssertionError('missing convex-ended wall')


def check_signs(a,b,c):
    # Compute each tile relative to its obtuse corner in two independent charts.
    for s in (-1,1):
        old=shapes(a,b,c,s)
        for owner in (0,1):
            chart=(c,0) if owner==0 else ((a,b) if s==1 else (a+b,-b))
            hand=s if owner==0 else -s
            actual=set()
            for j in range(6):
                if hand*(-1)**j==-1:
                    u=scale(-a,multiply(chart,UNITS[j]))
                    v=scale(b,multiply(chart,UNITS[(j+hand)%6]))
                    actual.add(tuple(sorted((u,v))))
            expected={tuple(sorted((subtract(u,q),subtract(v,q))))
                      for u,q,v in (old[3:] if owner==0 else old[:3])}
            assert expected==actual


def small_population(a,b,c,limit,base):
    # pi > 3.141 and sqrt(3) > 1.732. Each neutral branch has an even
    # number of c-blocks. At 16 owners its population is exactly 2c.
    def upper(m):
        if m==16:
            return 2*c
        return 2*c*((10**6*(m*c)**2)//(3141*1732*a*b*2*c))
    cap=limit-base
    count=cap//16
    result={'max_remote_lifts':count,'one_lift_max_tiles':upper(cap)}
    if count==2:
        costs=[(p,q) for p in range(16,cap+1,2) for q in range(p,cap+1,2) if p+q<=cap]
        result['two_lifts_max_subtree']=upper(cap-16)
        result['two_lifts_max_distinct_tiles']=max(upper(p)+upper(q) for p,q in costs)
    return result


def check(exe,sides,workers):
    a,b,c,l=sides
    A,C=[polygon(a,b,c,l,k) for k in (0,1)]
    totals=(471,693) if c==37 else (935,1365)
    for p,total in zip((A,C),totals):
        assert sum(det(x,y) for x,y in zip(p,p[1:]+p[:1]))==a*b*(total-2*l)
    wall=forced_wall(a,b,c,l,A)
    check_signs(a,b,c)
    # The corrected pre-existing census leaves word C only at c=43, hand -1.
    prior=json.loads((SOURCE.parent/'charged-contour/STATUS.json').read_text())
    board=prior[str((2*a+b)*(a+2*b))]
    native=b*(2*a+b)%c
    expected=[('A',A,-1,wall['hand_labels'][1])]
    for h in (-1,1):
        rows=board['by_outer_word'][f'C hand {h:+d}']
        assert sorted(t for row in rows for t in row['translations'])==[
            t for t in range(c) if h==-1 or t!=native]
        for row in rows:
            if row['profile_and_max_odd_blocks']:
                expected.extend(('C',C,h,t) for t in row['translations'])
    def trial(args):
        word,p,h,t=args
        tokens=[a,b,c,len(p),*(v for pt in p for v in pt),h,t]
        s,k,failure=map(int,run([exe],' '.join(map(str,tokens))).split())
        assert (s,k)==(h,t)
        return [word,h,t,failure]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results=list(pool.map(trial,expected))
    return dict(native_positive_label=native,forced_wall=wall,section_trials=results,
                small_unmatched_population=small_population(a,b,c,149 if c==37 else 171,
                                                            107 if c==37 else 149),
                unresolved=[row[:3] for row in results if not row[3]])


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Enable assertions.')
    parser=argparse.ArgumentParser()
    parser.add_argument('--workers',type=int,default=1)
    args=parser.parse_args()
    with TemporaryDirectory() as d:
        exe=Path(d)/'charged';compile_cpp(HERE/'charged_sections.cpp',exe)
        data={str(n):check(exe,sides,args.workers) for n,sides in [
            (3431,(33,7,37,3)),(5063,(35,13,43,5))]}
        data['control143']=controls(exe,exact_only=True)
        print(json.dumps(data,indent=2))
