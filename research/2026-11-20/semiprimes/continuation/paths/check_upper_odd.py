from math import gcd
def solve(a,b,c):
    K=2*c;d=a-b;h=lambda x,y:max(abs(x),abs(y),abs(x+y))
    ax,by=a+b,-b
    ans=[];best=K
    for x in range(-K,K+1):
        res=(a*x)*pow(b,-1,c)%c
        y0=-K+(res+K)%c
        for y in range(y0,K+1,c):
            if h(x,y)>best:continue
            X=ax-(a*x-b*y)//c;Y=by-(b*x+(a+b)*y)//c
            if h(X,Y)+h(x,y)>best:continue
            for f in range(-best+(d+best)%(c-d),best+1,c-d):
              for g in range(-best+(d+best)%(c+d),best+1,c+d):
                if (f-g)%2 or f%2==0:continue
                J1,J2=(f+g)//2,(f-g)//2
                rs=[];ok=True
                for X0,Y0,J in [(X,Y,J1),(x,y,J2)]:
                    if (J-X0+Y0)%3:ok=False;break
                    l=(J-X0+Y0)//3
                    rs.append((X0+l,Y0-l,l))
                if not ok:continue
                cost=sum(abs(v) for r in rs for v in r)
                if cost<=best:
                    if cost<best:best=cost;ans=[]
                    ans.append(rs)
    return best,ans
if __name__=='__main__':
 for u,v in [(10,1),(6,1),(12,1),(16,1),(22,1),(18,1),(40,1),(44,3),(62,3),(122,5)]:
    g=gcd(u-v,3);a,b,c=(u*u-v*v)//g,v*(2*u+v)//g,(u*u+u*v+v*v)//g
    m,x=solve(a,b,c);print(u,v,a+b,m,x[:5],flush=True)
