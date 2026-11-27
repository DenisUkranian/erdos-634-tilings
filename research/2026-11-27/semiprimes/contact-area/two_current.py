"""Integer endpoint duals for ordinary short-lift charge at any two adjacent gates."""
from itertools import product
from pathlib import Path
import base64
import json
import zlib

U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))
HERE=Path(__file__).resolve().parent


def add(p,q):
    return p[0]+q[0],p[1]+q[1]


def scale(k,p):
    return k*p[0],k*p[1]


def certificate(a,b,c,offset,w):
    both=offset==-1
    size=c*c if both else c
    assert len(w)==3*size+2 and all(type(x)==int for x in w)
    plus,minus=-a*pow(b,-1,c)%c,-b*pow(a,-1,c)%c

    def point(p):
        x,y=p
        return (x%c)*c+y%c if both else (x+plus*y)%c

    scores={}
    mates={}
    limit=1
    outside=0
    for t,j,h in product(range(size),range(6),(-1,1)):
        q=divmod(t,c) if both else (t,0)
        u=add(q,scale(-a,U[j]))
        end=(j+h)%6
        v=add(q,scale(b,U[end]))
        first,second=(j%3)*size,(end%3)*size
        value=h*(w[first+point(q)]-w[first+point(u)]+w[second+point(v)]-w[second+point(q)])
        g=(u[0]+(plus if h==1 else minus)*u[1])%c
        primary=h==1 and g==0
        secondary=(h==-1 and g==0) if both else (h==1 and g==offset)
        if primary or secondary:
            value+=h*(-1)**j*w[3*size+int(secondary)]
            limit=max(limit,value)
        else:
            outside=max(outside,value)
        scores[t,j,h]=value
        mates[t,j,h]=(point(add(add(u,v),scale(-1,q))),(j+3)%6,h)
    for k,v in scores.items():
        limit=max(limit,(v+scores[mates[k]]+1)//2)
    # For an opposite-hand pair, negative conjugation interchanges the
    # normalized gates without changing sign. Average the two inequalities.
    assert both or w[-2]==w[-1]
    weight=w[-2]+w[-1]
    return weight,2*limit,2*max(0,outside-limit)


def run():
    packed=(HERE/'TWO_CURRENT.duals').read_bytes().strip()
    data=json.loads(zlib.decompress(base64.b85decode(packed)))
    result={}
    for a,b,c in ((33,7,37),(35,13,43)):
        tables=data[str(c)]
        assert set(map(int,tables))=={-1,*range(1,c)}
        costs=[]
        overhead=[]
        for k,w in tables.items():
            weight,limit,excess=certificate(a,b,c,int(k),w)
            num,den=(10,3) if c==37 else (39,10)
            assert weight*den>limit*num
            # Outside single signs can differ from the full signed charge.
            overhead.append((den*excess+num*limit+den*limit-1)//(den*limit))
            costs.append((c*(weight-3*limit)+excess+weight-1)//(excess+weight))
        result[str(c)]=dict(tables=len(tables),charge_coefficient=[num,den],
                            outside_penalty=max(overhead),outside_at_three_blocks=min(costs))
    return result


if __name__=='__main__':
    print(run())
