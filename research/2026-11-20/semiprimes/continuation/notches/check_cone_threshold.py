"""Integer replay of the two-orientation square-cell construction."""
from math import gcd

def first_scale(a,c,k):
    # One staircase of a-by-c rectangles and another of c-by-a rectangles.
    cells=[(i,j) for j in range((k-1)//c+1)
           for i in range((k-1-j*c)//a+1)]
    return max((i+1)*c+(j+1)*a for i,j in cells)

if __name__=='__main__':
    trials=0
    for a in range(1,27):
        for c in range(a+1,38):
            if gcd(a,c)!=1:continue
            for k in range(1,81):
                assert first_scale(a,c,k)==a+c*((k+a-1)//a)
                trials+=1
    print(trials,"exact staircase bounds")
    for a,c,t,k in [(33,37,13,8),(35,43,11,2),(33,37,26,23),(35,43,22,17)]:
        print(a,c,t,k,first_scale(a,c,k))

    for a,c,t,k in [(33,37,13,8),(35,43,11,2),(33,37,26,23),(35,43,22,17)]:
        for d,e in [(a,c),(c,a)]:
            jumps=[0]*e
            jumps[0]+=t-1
            for j in range(1,t):
                jumps[j % e]-=1
            levels=[];running=0
            for jump in jumps:
                running=(running+jump)%d
                levels.append(running)
            cost=min(sum((v+shift)%d for v in levels) for shift in range(d))
            budget=(t*t-k*k-t-k)//2
            assert cost >= t*(t-1)//2 > budget
            print("upper-bar cost",a,c,t,k,d,e,cost,"pair budget",budget)

    pairs=0
    for u in range(6,655,2):
        for v in range(1,u,2):
            g=gcd(3,u-v)
            if gcd(u,v)>1 or u<=4*v*(v-1 if g==3 and v%3==2 else v):
                continue
            a=(u*u-v*v)//g; b=(2*u*v+v*v)//g; c=(u*u+u*v+v*v)//g
            for copies in (1,2):
                if copies==2 and u<10*v:continue
                s=(c-a)//copies;k=(c-b)//copies-b
                assert s*a-s*(s+1)//2 < k*(k+1)
                pairs+=1
    print(pairs,"families of pentagon row bounds")
