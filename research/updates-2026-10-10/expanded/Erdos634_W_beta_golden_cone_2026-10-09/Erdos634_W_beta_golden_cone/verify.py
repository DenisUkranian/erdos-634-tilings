#!/usr/bin/env python3
"""Independent exact certificate verifier. Does not import the constructor.
Standard-library boundary-current proof; optional independent all-pairs SAT via numba.
"""
if not __debug__:
    raise RuntimeError('Assertions must be enabled; do not run with python -O')

import argparse,json,hashlib,time
from math import gcd
from pathlib import Path
from collections import defaultdict

def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])

def verify(path,all_pairs=False):
    st=time.monotonic();raw=Path(path).read_bytes();p=json.loads(raw)
    ts=p['triangles'];outer=p['target'];N=p['tile_count'];u=p['u'];v=p['v'];m=p['m']
    den=p['coordinate_denominator']
    assert p['branch'] in ('W','beta')
    assert all(type(x) is int for x in (u,v,m,den,N)) and 0<u<v and m>0 and den>0
    assert len(outer)==3
    assert all(len(tri)==3 and all(len(P)==2 and all(type(x) is int for x in P) for P in tri) for tri in ts+[outer])
    a=u*v;b=v*v-u*u;c=v*v;P=3*v*v-u*u;Q=2*v*v-u*u
    assert p['tile_sides']==[a,b,c]
    assert p['metric_integer']==[v**3,u*P,v**3] and p['metric_common_divisor']==v
    assert len(ts)==N and N==(Q if p['branch']=='W' else P)*m*m
    def norm2(x,y):return v**3*(x*x+y*y)+u*P*x*y
    wanted=sorted(v*den*den*s*s for s in (a,b,c))
    assert cross(*outer)>0
    expect_target=sorted(v*den*den*s*s for s in (
        (m*v**3,m*u*Q,m*v*b) if p['branch']=='W' else (m*v**3,m*v**3,m*u*P)))
    assert sorted(norm2(outer[i][0]-outer[(i+1)%3][0],outer[i][1]-outer[(i+1)%3][1]) for i in range(3))==expect_target
    events=defaultdict(int)
    def edge(A,B,coefficient):
        dx,dy=B[0]-A[0],B[1]-A[1]
        h=gcd(abs(dx),abs(dy));assert h>0
        dx//=h;dy//=h
        if dx<0 or (dx==0 and dy<0):dx=-dx;dy=-dy
        line=(dx,dy,dy*A[0]-dx*A[1])
        t1=dx*A[0]+dy*A[1];t2=dx*B[0]+dy*B[1]
        s=1 if t2>t1 else -1
        lo,hi=sorted((t1,t2))
        events[line+(lo,)]+=coefficient*s
        events[line+(hi,)]-=coefficient*s
    area=0
    for i,tri in enumerate(ts):
        ar=cross(*tri);assert ar>0,('orientation',i);area+=ar
        lengths=sorted(norm2(tri[j][0]-tri[(j+1)%3][0],tri[j][1]-tri[(j+1)%3][1]) for j in range(3))
        assert lengths==wanted,('metric',i,lengths,wanted)
        for A in tri:
            assert all(cross(outer[j],outer[(j+1)%3],A)>=0 for j in range(3)),('containment',i,A)
        for j in range(3):edge(tri[j],tri[(j+1)%3],1)
    assert area==cross(*outer),('area',area,cross(*outer))
    for j in range(3):edge(outer[j],outer[(j+1)%3],-1)
    nonzero=[(k,w) for k,w in events.items() if w]
    assert not nonzero,('positioned-boundary',nonzero[:5])
    report={'status':'PASS','file':str(Path(path).name),'sha256':hashlib.sha256(raw).hexdigest(),
        'branch':p['branch'],'u':u,'v':v,'m':m,'N':N,
        'metric':'exact integer PASS','containment':'exact integer PASS',
        'area':'exact integer PASS','positioned_boundary':'exact integer PASS',
        'nonzero_boundary_events':0,'distinct_boundary_events_checked':len(events),
        'all_pairs_checked':0,'external_review':False,'full_problem_solved':False}
    if all_pairs:
        import numpy as np
        from numba import njit
        arr=np.array(ts,dtype=np.int64)
        diameter=int(arr.max()-arr.min())
        assert 2*diameter*diameter<2**63-1,'int64 determinant overflow risk'
        @njit
        def paircheck(arr):
            n=len(arr)
            for i in range(n):
                for j in range(i):
                    separated=False
                    for which in range(2):
                        k1=i if which==0 else j;k2=j if which==0 else i
                        for e in range(3):
                            A=arr[k1,e];B=arr[k1,(e+1)%3]
                            all_right=True
                            for k in range(3):
                                C=arr[k2,k]
                                val=(B[0]-A[0])*(C[1]-A[1])-(B[1]-A[1])*(C[0]-A[0])
                                if val>0:all_right=False;break
                            if all_right:separated=True;break
                        if separated:break
                    if not separated:return i,j
            return -1,-1
        collision=paircheck(arr)
        assert collision==(-1,-1),('overlap',collision)
        report['all_pairs_checked']=N*(N-1)//2
        report['all_pairs_status']='exact integer separating-axis PASS'
    report['elapsed_seconds']=round(time.monotonic()-st,3)
    return report
if __name__=='__main__':
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('certificate',type=Path)
    a.add_argument('--all-pairs',action='store_true');a.add_argument('--report',type=Path)
    p=a.parse_args();r=verify(p.certificate,p.all_pairs);print(json.dumps(r,indent=2))
    if p.report:p.report.write_text(json.dumps(r,indent=2)+'\n')
