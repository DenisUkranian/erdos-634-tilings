"""Exact loads for the primitive F2 staircase, no solver or external dependency."""
from collections import Counter
from math import gcd


def sharp_limit(v, g):
    return 4*v*v - (4*v if g == 3 and v % 3 == 2 else 0)


def construction(u, v):
    if gcd(u,v) != 1 or not u*u-v*v > v*(2*u+v) > 0:
        raise ValueError('ordered coprime Eisenstein parameters required')
    g=gcd(u-v, 3)
    a=(u*u-v*v)//g
    b=v*(2*u+v)//g
    c=(u*u+u*v+v*v)//g
    assert gcd(a,b)==1 and c*c==a*a+a*b+b*b
    if u > sharp_limit(v,g):
        return None
    M=u-2*v
    if c<=2*b:
        bins=[(2*v,M)]
    elif u<4*v:
        assert u>=3*v
        if g==1:
            # Each m is 1, distribute n=2v over M bins.
            bins=[(1,1)]*(2*M-2*v)+[(2,1)]*(2*v-M)
        else:
            n5=(2*v-M)//3
            bins=[(5,2)]*n5+[(1,1)]*(M-2*n5)
    else:
        h,k=divmod((M-2*v)//g,2*v)
        bins=[(1,1+g*h)]*(2*v-k)+[(1,1+g*(h+1))]*k
    assert sum(n for n,m in bins)==2*v and sum(m for n,m in bins)==M
    out=[]
    for n,m in bins:
        assert (n-m)%g==0
        r,s,t=(v*n+(u+v)*m)//g,(u*n-v*m)//g,(u*m-v*n)//g
        assert 0<=r<=b and 0<=s<=a and t>=0 and a*r-b*s==c*t
        out.append((r,s,t))
    assert tuple(map(sum,zip(*out)))==(c-b,c-a,a-b)
    return out


def independent_dp(u,v):
    g=gcd(u-v,3)
    a=(u*u-v*v)//g
    b=v*(2*u+v)//g
    c=(u*u+u*v+v*v)//g
    R,S=c-b,c-a
    possible=[]
    for s in range(S+1):
        r=(b*s*pow(a,-1,c))%c
        if 0<=r<=b and r+s>0 and a*r>=b*s:
            possible.append((r,s))
    if S==0:return False
    # counts r via bit vectors indexed by s.
    masks=[0]*(S+1);masks[0]=1
    for s in range(S+1):
        if masks[s]:
            for dr,ds in possible:
                assert ds>0
                if s+ds<=S:
                    masks[s+ds] |= masks[s]<<dr
    return bool((masks[S]>>R)&1)


if __name__=='__main__':
    stats=Counter()
    for u in range(3,351):
        for v in range(1,u):
            if gcd(u,v)!=1 or u*u-v*v<=v*(2*u+v): continue
            z=construction(u,v)
            stats['ordered shapes']+=1
            stats['constructed' if z else 'outside staircase']+=1
            if u<=24:
                assert bool(z)==independent_dp(u,v)
                stats['independent integer DPs']+=1
    print(stats)
    for a,b in [(649,455),(3325,2291),(7289,5031),(33,7)]:
        matches=[(u,v,construction(u,v)) for u in range(2,200) for v in range(1,u)
                 if gcd(u,v)==1 and (u*u-v*v)//gcd(u-v,3)==a and v*(2*u+v)//gcd(u-v,3)==b]
        for u,v,blocks in matches:
            print(a,b,'u,v,g',u,v,gcd(u-v,3), 'load frequencies', Counter(blocks or []))
