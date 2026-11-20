"""Compute exact shortest net word subject to both boundary characters."""
from itertools import product

def netmin(a,b,c,t,k,j,ceiling=None):
    # W to X': displacement c*(k,−j) −t*(a,b).
    target=(k*c-t*a,-j*c-t*b)
    A=t*(a-b)-(k+j)*c
    d=a-b
    def h(x,y):return max(abs(x),abs(y),abs(x+y))
    def signed(x,y,J):
        if (J-x+y)%3:return
        l=(J-x+y)//3
        return (x+l,y-l,l)
    # k steps +c, j steps −rho*c and t steps −cz give an exact
    # linear word, although those placements need not fit the polygon.
    lim=k+j+t if ceiling is None else ceiling
    best=lim;ans=[]
    for x,y in product(range(-lim,lim+1),repeat=2):
        if h(x,y)>lim:continue
        p,q=target[0]-(a*x-b*y),target[1]-(b*x+(a+b)*y)
        if p%c or q%c:continue
        X,Y=p//c,q//c
        if h(x,y)+h(X,Y)>best:continue
        for f in range(-best,best+1):
            if (A+c*f)%(c-d):continue
            for g in range(-best,best+1):
                if (A+c*g)%(c+d) or (f-g)%2:continue
                J0,J1=(f+g)//2,(f-g)//2
                r0=signed(X,Y,J0);r1=signed(x,y,J1)
                if r0 is None or r1 is None:continue
                length=sum(abs(i) for i in r0+r1)
                if length>best:continue
                if ceiling is None and length<best:best=length;ans=[]
                ans.append((r0,r1))
    assert ans or ceiling is not None
    return best,ans
if __name__=='__main__':
    for v in [(33,7,37,13,8,1),(35,13,43,11,2,1),(33,7,37,26,23,1),(35,13,43,22,17,1)]:
       m,n=netmin(*v);print(v,'net minimum',m,'signed inventories',n)
