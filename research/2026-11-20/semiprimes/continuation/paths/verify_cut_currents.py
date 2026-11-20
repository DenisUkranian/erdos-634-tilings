"""Enumerate short upper-cut signed inventories with exact boundary currents."""
from math import gcd

def residues(lo, hi, a, mod):
    return range(lo + (a-lo) % mod, hi+1, mod)

def hexnorm(x,y):
    return max(abs(x),abs(y),abs(x+y))

def inventory(x,y,j):
    # Axes 1,rho,rho^2 carry character signs +,-,+.
    offset=j-x+y
    if offset%3:
        return None
    third=offset//3
    return x+third,y-third,third

def verify(u,v):
    g=gcd(u-v,3)
    a,b,c=(u*u-v*v)//g,v*(2*u+v)//g,(u*u+u*v+v*v)//g
    assert gcd(a,b)==1 and a%2 and b%2 and u>=6*v
    d=a-b
    F=(u-v)//g
    hi=a+b+max(2*v-1, min(v*F-1, 12))
    found=False
    for x in range(-hi,hi+1):
        for y in residues(-hi,hi,a*pow(b,-1,c)*x,c):
            net_u=(a*x-b*y,b*x+(a+b)*y)
            assert all(t%c==0 for t in net_u)
            X,Y=a+b-net_u[0]//c,-b-net_u[1]//c
            if hexnorm(X,Y)+hexnorm(x,y)>hi:
                continue
            for total in residues(-hi,hi,d,c-d):
                for diff in residues(-hi,hi,d,c+d):
                    if (total-diff)%2:
                        continue
                    first=inventory(X,Y,(total+diff)//2)
                    second=inventory(x,y,(total-diff)//2)
                    if first is None or second is None:
                        continue
                    cost=sum(map(abs,first+second))
                    if cost>hi:
                        continue
                    found=True
                    excess=cost-a-b
                    assert excess>=0
                    if excess<v*F:
                        assert excess%2==0
                    if excess<2*v:
                        assert (first,second)==((a,0,-b),(0,0,0))
    assert found
    print(f"{(u,v)}: N={(a+2*b)*(2*a+b)}, shortest={a+b}, tested through {hi}")

if __name__=='__main__':
    for args in [(6,1),(10,1),(12,1),(16,1),(22,3),(26,3),(32,5),(44,3)]:
        verify(*args)
