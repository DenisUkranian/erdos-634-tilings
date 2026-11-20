"""Replay the midpoint switch and every independent full-rhombus choice, exactly."""
from collections import defaultdict, Counter
from fractions import Fraction
from math import ceil, floor, gcd, isqrt


def plus(p,q): return p[0]+q[0],p[1]+q[1]
def minus(p,q): return p[0]-q[0],p[1]-q[1]
def times(n,p): return n*p[0],n*p[1]
def det(p,q): return p[0]*q[1]-p[1]*q[0]
def norm(p): return p[0]**2+p[0]*p[1]+p[1]**2


def compute(a,b,c):
    assert a>b>0 and gcd(a,b)==1 and c*c==a*a+a*b+b*b and a*b%2
    p,q=a+2*b,2*a+b
    H,V=b*q,a*p
    # Physical lengths in numerator coordinates are multiplied by 2c.
    den=2*c
    e=(-2*(a+b),2*a)
    f=(-2*b,2*(a+b))
    u,v=times(a*b,e),times(a*b,f)
    O=minus((H*c,V*c),((u[0]+v[0])//2,(u[1]+v[1])//2))
    board=[(0,0),(H*den,0),(0,V*den)]
    assert det(times(b,e),times(a,f))!=0
    assert det(plus(times(b,e),times(a,f)),minus(board[2],board[1]))==0
    assert all(x>=0 and y>=0 for x,y in (O,plus(O,u),plus(O,v),plus(plus(O,u),v)))

    def count_grid(xside,yside):
        X,Y=times(xside,e),times(yside,f)
        # The sum diagonal is the long tile side in both grids.
        assert sorted((norm(X),norm(Y),norm(plus(X,Y))))==sorted((den*t)**2 for t in (a,b,c))
        D=det(X,Y)
        xy=[(Fraction(det(minus(P,O),Y),D),Fraction(det(X,minus(P,O)),D)) for P in board]
        def inside(i,j):
            x,y=plus(O,plus(times(i,X),times(j,Y)))
            return x>=0 and y>=0 and V*x+H*y<=H*V*den
        counts=Counter()
        for i in range(floor(min(x for x,y in xy))-1,ceil(max(x for x,y in xy))+1):
            for j in range(floor(min(y for x,y in xy))-1,ceil(max(y for x,y in xy))+1):
                if inside(i,j) and inside(i+1,j+1):
                    half_count=int(inside(i+1,j))+int(inside(i,j+1))
                    counts[i//(a*b//xside),j//(a*b//yside)]+=half_count
        return counts

    old=count_grid(a,b)
    new=count_grid(b,a)
    assert old[0,0]==a*b-a and new[0,0]==a*b
    indices=set(old)|set(new)
    everywhere=sum(max(old[k],new[k]) for k in indices)
    print(f'{p*q}: midpoint {old[0,0]} -> {new[0,0]}, '
          f'full board {sum(old.values())} -> {sum(old.values())+a}; '
          f'new-direction grid alone {sum(new.values())}; independent choices {everywhere}.')
    return sum(old.values()),sum(new.values()),everywhere


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    compute(33,7,37)
    compute(35,13,43)
