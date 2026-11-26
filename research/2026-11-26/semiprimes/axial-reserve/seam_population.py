"""Verify the axial tile budget on the surviving A seam with all gate translations."""
import gzip
import json
from pathlib import Path

import numpy as np

from reserve import HERE
from geometry import GENERATORS, UNITS, add, det, multiply, repaired_boundary, scale, subtract


def check(a,b,c,l,s):
    records=json.loads(gzip.decompress((HERE/'seam-tables.json.gz').read_bytes()))[f'{c}/{s}']
    lower=[0]*c
    def axis(p,q):
        return next(k for k in range(3) if det(UNITS[k],subtract(q,p))==0)
    segments=repaired_boundary(a,b,c,l,0)
    area=sum(det(p,q) for p,q in segments)//(a*b)
    assert area==(465 if c==37 else 925)
    basic_pairs=[]
    for i in range(3):
        for j in range(i+1,3):
            for A,B in ((a,b),(b,a)):
                u,w=scale(A,UNITS[i]),scale(B,UNITS[j])
                basic_pairs.append([(0,0),u,add(u,w),w])
    for den,raw in records:
        assert den>0 and len(raw)==3*c*c+1 and max(map(abs,raw))<10**6
        f=np.array(raw[:-1],dtype=np.int64).reshape(3,c,c)
        def weight(p,q):
            k=axis(p,q)
            return int(f[k,q[0]%c,q[1]%c]-f[k,p[0]%c,p[1]%c])
        for poly in basic_pairs:
            scores=np.zeros((c,c),dtype=np.int64)
            for p,q in zip(poly,poly[1:]+poly[:1]):
                F=f[axis(p,q)]
                scores+=np.roll(F,scale(-1,q),axis=(0,1))-np.roll(F,scale(-1,p),axis=(0,1))
            assert np.max(scores)<=2*den
        # The parent singles have sign -1, short hand s, and one long endpoint
        # on the zero gate after translating the entire core by -(t,0).
        for k in range(c):
            u=scale(k,GENERATORS[c,s])
            for j in range(6):
                if s*(-1)**j!=-1:
                    continue
                q=add(u,scale(a,UNITS[j]))
                w=add(q,scale(b,UNITS[(j+s)%6]))
                assert s*(weight(u,q)+weight(q,w))+raw[-1]<=den
        for t in range(int(s==1),c):
            projected=sum(weight(subtract(p,(t,0)),subtract(q,(t,0))) for p,q in segments)
            value=(projected+raw[-1]*(a-b)+den-1)//den
            lower[t]=max(lower[t],value)
    bounds=lower[int(s==1):]
    upper=(area-min(bounds))//c
    upper-=int(upper%2==0)
    assert upper<=(7 if c==37 else 15)
    return dict(translations=len(bounds),minimum_required_axial_population=min(bounds),
                maximum_terminal_odd_blocks=upper)


if __name__=='__main__':
    if not __debug__:
        raise SystemExit("Enable Python assertions.")
    print(json.dumps({str(c):{str(s):check(a,b,c,l,s) for s in (1,-1)}
                      for a,b,c,l in ((33,7,37,3),(35,13,43,5))},indent=2))
