"""Two defect edges on an exterior-free cut, below the order-a word threshold."""
from collections import Counter,defaultdict
from itertools import combinations
import json
from terminal import UNITS,add,scale,det


def run(axis,k):
    return [(axis+(3 if k<0 else 0))%6]*abs(k)


def group(word,m,a,b,c):
    stack=[]
    for j in word:
        if j>=6:
            # Tokens six and nine are the positive and negative rotated step.
            axis = 1 if m==a else 0
            exponent = ((b if m==a else a)*pow(c,-1,m))%m
            if j==9:
                exponent=-exponent
        else:
            axis=j%3
            exponent=1 if j<3 else -1
        if stack and stack[-1][0]==axis:
            exponent+=stack.pop()[1]
        if exponent%m:
            stack.append((axis,exponent%m))
    return stack


def evaluate(a,b,c,P,Q):
    word=[6,*P,9,*[(j+3)%6 for j in reversed(Q)]]
    assert not group(word,a,a,b,c) and not group(word,b,a,b,c)
    p=(0,0)
    vertices=[]
    area=0
    for j in word:
        vertices.append(p)
        step=scale(1 if j==6 else -1,(a,b)) if j>=6 else scale(c,UNITS[j])
        area+=det(p,step)
        p=add(p,step)
    assert p==(0,0) and area%(2*c*a*b)==0
    if area<=0 or len(set(vertices))!=len(vertices):
        return None
    # Exact proper or tangential intersection of nonconsecutive segments.
    def orient(p,q,r):
        return det((q[0]-p[0],q[1]-p[1]),(r[0]-p[0],r[1]-p[1]))
    n=len(vertices)
    for i,j in combinations(range(n),2):
        if j-i in (1,n-1):
            continue
        p,q=vertices[i],vertices[(i+1)%n]
        r,s=vertices[j],vertices[(j+1)%n]
        if any(max(p[k],q[k])<min(r[k],s[k]) or max(r[k],s[k])<min(p[k],q[k])
               for k in (0,1)):
            continue
        if orient(p,q,r)*orient(p,q,s)<=0 and orient(r,s,p)*orient(r,s,q)<=0:
            return None
    return area//(a*b),len(word)


def census(a,b,c):
    t=b*pow(c,-1,a)%a
    assert 0<t<a/2 and (a-1-2*t)//2<b and a*pow(c,-1,b)%b==b-1
    rows=defaultdict(Counter)
    def record(P,Q):
        result=evaluate(a,b,c,P,Q)
        if result:
            population,length=result
            rows[population][length]+=1
    for n in range(b,(a-1)//2+1,b):
        record(run(1,n),run(1,n))
    limit=(a-1-2*t)//2
    for sign in (1,-1):
        # Q represents (X^-1 Y^-t)^k; sign is the sign of k.
        def bodies(U,axis):
            residue=(-sign if axis==0 else -sign*t)%b
            for e in range(-limit,limit+1):
                if not e or e%b!=residue or len(U)+abs(e)>limit:
                    continue
                new=U+run(axis,e)
                if axis==0:
                    yield new
                yield from bodies(new,1-axis)
        for U in bodies([],0):
            for i in range(-a,a+1):
                if i%b!=(0 if sign==1 else t%b):
                    continue
                for j in range(-a,a+1):
                    if j%b!=((-t)%b if sign==1 else 0):
                        continue
                    if 2*len(U)+abs(i)+abs(i-t)+abs(j)+abs(j+t)>=a:
                        continue
                    P=run(1,i-t)+U+run(1,j+t)
                    Q=run(1,i)+U+run(1,j)
                    record(P,Q)
    return {n:dict(sorted(counts.items())) for n,counts in sorted(rows.items())}


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Enable assertions.')
    print(json.dumps({c:census(a,b,c) for a,b,c in ((33,7,37),(35,13,43))},indent=2))
