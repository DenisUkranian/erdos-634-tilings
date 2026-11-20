"""Exact side inventories and purity checks for the four unit-F2 notch reductions."""
from math import gcd

def words(length,a,b,c):
    return [(x,(length-x*a-z*c)//b,z) for x in range(length//a+1)
            for z in range((length-x*a)//c+1) if (length-x*a-z*c)%b==0]

def check(u,t,k):
    g=gcd(3,u-1)
    a,b,c=(u*u-1)//g,(2*u+1)//g,(u*u+u+1)//g
    K=a//u
    assert a>b and a*a+a*b+b*b == c*c and t*a>k*c>0
    length=t*c-k*a
    assert length%b==0 and 0<length<a*b
    for n in range(1,K+1):
        for i,side in enumerate([a,b,c]):
            counts=[0,0,0]
            counts[i]=n
            assert words(n*side,a,b,c)==[tuple(counts)]
    ws=words(length,a,b,c)
    assert all(x==z and length//b==y+u*z and z<=min(K,t-1) for x,y,z in ws)
    if k<=min(K,t-1):
        assert words(k*b,a,b,c)==[(0,k,0)]
    print((a+2*b)*(2*a+b),t*t-k*k,(a,b,c),t,k,length,'max c',max(z for x,y,z in ws),'wall words',ws)

if __name__=='__main__':
    for row in [(10,13,8),(10,26,23),(6,11,2),(6,22,17)]:check(*row)
