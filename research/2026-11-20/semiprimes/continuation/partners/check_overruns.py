"""Check optimal overshoots by minimization on the original (r,s) loads."""
from math import gcd


def minimum(u,v):
    g=gcd(3,u-v)
    a=(u*u-v*v)//g
    b=v*(2*u+v)//g
    c=(u*u+u*v+v*v)//g
    R,S=c-b,c-a
    widths=[i*b*pow(a,-1,c)%c for i in range(S+1)]
    # R < c. At every partial s the accumulated r must therefore equal widths[s].
    best=[None]*(S+1)
    best[0]=0
    for s in range(1,S+1):
        if widths[s]>R:
            continue
        for j in range(s):
            if best[j] is None or widths[j]+widths[s-j]!=widths[s]:
                continue
            cost=best[j]+max(0,widths[s-j]-b)**2
            if best[s] is None or cost<best[s]:
                best[s]=cost
    assert widths[S]==R and best[S] is not None
    n=2*v
    low=1+g*((u-2*v-n)//(g*n))
    high_count=(u-2*v-n*low)//g
    values=[low]*(n-high_count)+[low+g]*high_count
    assert len(values)==n and sum(values)==u-2*v
    assert all(v+(u+v)*m>0 and u-v*m>=0 for m in values)
    proposal=sum(max(0,(v+(u+v)*m)//g-b)**2 for m in values)
    assert best[S]==proposal
    return proposal


if __name__=="__main__":
    if not __debug__:
        raise SystemExit("Run with assertions enabled.")
    checked=0
    for u in range(4,82,2):
        for v in range(1,u,2):
            g=gcd(3,u-v)
            bound=4*v*(v-1) if g==3 and v%3==2 else 4*v*v
            if gcd(u,v)==1 and u>bound and u*u-v*v>v*(2*u+v):
                minimum(u,v)
                checked+=1
    for u,v in [(6,1),(10,1),(44,3),(122,5),(268,7)]:
        print(u,v,minimum(u,v))
    print("Small residual parameter pairs checked:",checked)
