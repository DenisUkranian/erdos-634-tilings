"""Exact verification of two mixed-direction partial patches and the shortest net vectors."""
from itertools import combinations
from math import gcd
from chain_bounds import hexnorm, minimum


def add(p, q):
    return p[0] + q[0], p[1] + q[1]


def sub(p, q):
    return p[0] - q[0], p[1] - q[1]


def scale(factor, p):
    return factor*p[0], factor*p[1]


def multiply(p, q):
    return p[0]*q[0] - p[1]*q[1], p[0]*q[1] + p[1]*q[0] + p[1]*q[1]


def cross(p, q):
    return p[0]*q[1] - p[1]*q[0]


def norm(p):
    x,y = p
    return x*x+x*y+y*y


def positive(tri):
    return tri if cross(sub(tri[1],tri[0]),sub(tri[2],tri[0]))>0 else tri[::-1]


def separated(first, second):
    for one, other in ((first,second),(second,first)):
        for p,q in zip(one, one[1:]+one[:1]):
            if all(cross(sub(q,p),sub(r,p))<=0 for r in other):
                return True
    return False


def check(a,b,c,word):
    # Coordinates are in the (1,rho) frame after division by z, multiplied by c.
    base = (a+b, -b)
    placements = [positive([scale(c,add(scale(i,base),p)) for p in [(0,0),base,(a,0)]])
                  for i in range(c)]
    start = (0,0)
    twice_area = 0
    for symbol in word:
        ray = (1,0) if symbol in ('E','F') else (1,-1)
        if symbol in ('E','S'):
            end = add(start,multiply(ray,(c,0)))
            apex = multiply(ray,(a*a,a*b))
        else:
            assert symbol in ('F','T')
            end = add(start,multiply(ray,(a,b)))
            apex = multiply(ray,(a*c,0))
        placements.append(positive([scale(c,start),scale(c,end),add(scale(c,start),apex)]))
        assert end[0]>start[0]
        twice_area -= cross(start,end)
        start = end
    assert start == scale(c,base)
    assert twice_area%(a*b*c)==0
    for tri in placements:
        assert all((a+b)*y>=-b*x and a*y<=b*x and (a+b)*x+b*y<=c*c*a*(a+2*b) for x,y in tri)
        assert sorted(norm(sub(q,p)) for p,q in zip(tri,tri[1:]+tri[:1]))==[b*b*c*c,a*a*c*c,c**4]
    assert all(separated(p,q) for p,q in combinations(placements,2))
    low,high=minimum(a,b,c,True)[0],minimum(a,b,c)[0]
    assert low==c and high==len(word)
    below=twice_area//(a*b)
    print((a+2*b)*(2*a+b), 'placed',len(placements),'path',high,'areas',below,(a+2*b)*(2*a+b)-below)


def audit():
    cases=0
    for u in range(4,81,2):
        for v in range(1,11,2):
            if gcd(u,v)!=1:
                continue
            g=gcd(3,u-v)
            if u<=4*v*v-(4*v if g==3 and v%3==2 else 0):
                continue
            a,b,c=(u*u-v*v)//g,v*(2*u+v)//g,(u*u+u*v+v*v)//g
            t=(2*v-1)//g
            f=(u-v)//g
            d=(2*u+v)//g
            nets=[]
            for j in range((v*t+f-1)//f,(b-u*t)//f+1):
                x=u*t+d*j
                y=f*j-v*t-x
                nets.append((a+b-x-v*t,-b+u*t+f*j,x,y))
            length,actual=minimum(a,b,c)
            assert (length, sorted(actual))==(a+b-v*t,sorted(nets))
            cases+=1
    print('Displacement optimum and full inventories checked on',cases,'residual shapes.')


if __name__ == '__main__':
    check(33,7,37,'EEEEEEEEEEEEEEEEEEEEEEEEEEEEESSFTSTTTFFS')
    check(35,13,43,'EEEEEEEEEEEEEEEEEEEEEEEEEEFFFTTTTTTTSTTTTTTTFTS')
    audit()
