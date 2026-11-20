"""Integer path inventories and the height-2 vector current on the seven controls."""
from math import gcd

CONTROLS = ((33,7,37,97),(35,13,43,129),(85,11,91,217),(143,25,157,393),
            (161,15,169,385),(323,37,343,801),(533,27,547,1177))


def ceildiv(n,d):
    return -(-n//d)


def signed_axes(x,y,character):
    # x=n0-n2, y=n1+n2, character=n0-n1+n2.
    third=character-x+y
    if third%3:
        return None
    n2=third//3
    return x+n2, y-n2, n2


def hex_distance(x,y):
    return max(abs(x),abs(y),abs(x+y))


def net_displacements(a,b,c,cap):
    # m is the upper-alphabet displacement, n its middle-alphabet complement.
    # n+z*m=(a+b,-b); integrality first gives a*x-b*y=0 modulo c.
    coefficient=a*pow(b,-1,c)%c
    for x in range(-cap,cap+1):
        bottom,top=max(-cap,-cap-x),min(cap,cap-x)
        first=bottom+(coefficient*x-bottom)%c
        for y in range(first,top+1,c):
            rx,ry=a*x-b*y,b*x+(a+b)*y
            assert rx%c==0 and ry%c==0
            X,Y=a+b-rx//c,-b-ry//c
            if hex_distance(x,y)+hex_distance(X,Y)<=cap:
                yield x,y,X,Y


def replay(a,b,c,target):
    assert a>=2*b and c*c==a*a+a*b+b*b and gcd(a,b)==1
    d,p,q=a-b,a+2*b,2*a+b
    assert target==4*c-2*d+1
    # If L exceeds cap, the lower path alone already puts us above target.
    cap=target-c
    nets=list(net_displacements(a,b,c,cap))
    best=None
    for plus in range(-cap+(d+cap)%(c-d),cap+1,c-d):
        for minus in range(-cap+(d+cap)%(c+d),cap+1,c+d):
            if (plus-minus)%2:
                continue
            J,K=(plus+minus)//2,(plus-minus)//2
            for x,y,X,Y in nets:
                m,n=signed_axes(x,y,K),signed_axes(X,Y,J)
                if m is None or n is None:
                    continue
                length=sum(abs(z) for z in m+n)
                if length>cap:
                    continue
                # Residual signed length on the three height-2 axes.
                r=(-a*p+a*n[0]+b*n[1]+c*m[0],
                   b*q+a*n[1]+b*n[2]+c*m[1],
                   a*n[2]-b*n[0]+c*m[2])
                assert r[0]-r[1]+r[2]==-(c*c+3*a*b)+d*J+c*K
                extra=max(ceildiv(abs(r[0]-r[1]+r[2]),c),
                          ceildiv(sum(map(abs,r)),a+b),ceildiv(max(map(abs,r)),c))
                bound=c+length+extra
                bound+=int(bound%2==0)
                if best is None or bound<best:
                    best=bound
    assert best==target
    print(f'{p*q}: analytic lower bound {target}, integer inventory relaxation {best}')


if __name__=='__main__':
    for control in CONTROLS:
        replay(*control)
