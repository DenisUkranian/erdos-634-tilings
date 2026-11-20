"""CRT formula versus a breadth-first search for the whole-board pair bound."""
from collections import deque
from math import gcd


def distance(modulus, side, c):
    def nearest(m, parity):
        residue=side%m
        if residue%2!=parity:
            residue+=m
        return min(residue,2*m-residue)
    s,t=gcd(modulus,c-side),gcd(modulus,c+side)
    assert s*t==modulus and gcd(s,t)==1
    return min(max(nearest(s,e),nearest(t,e)) for e in (0,1))


def bfs(modulus, side, c):
    lam=side*pow(c,-1,modulus)%modulus
    steps=(1,-1,lam,-lam)
    dist={0:0}
    todo=deque([0])
    while todo:
        x=todo.popleft()
        if x==side%modulus:
            return dist[x]
        for d in steps:
            y=(x+d)%modulus
            if y not in dist:
                dist[y]=dist[x]+1
                todo.append(y)
    raise AssertionError('unit step lost')


def main():
    count=0
    for u in range(2,82,2):
        for v in range(1,u,2):
            if gcd(u,v)!=1:
                continue
            g=gcd(3,u-v)
            a,b,c=(u*u-v*v)//g,v*(2*u+v)//g,(u*u+u*v+v*v)//g
            if a<=b:
                continue
            da,db=distance(a,b,c),distance(b,a,c)
            assert (da,db)==(bfs(a,b,c),bfs(b,a,c))
            if g==3:
                assert 3*da>=u+v-v*v
                if v==1:
                    assert 3*da==u+2
            count+=1
    print(f'CRT and residue-graph distances agree on {count} primitive odd triples')
    for a,b,c in [(33,7,37),(35,13,43),(161,15,169)]:
        da,db=distance(a,b,c),distance(b,a,c)
        print(f'{(a+2*b)*(2*a+b)}: distances ({da}, {db}), at least {2*max(da,db)+1} unpaired along c')


if __name__=='__main__':
    main()
