from fractions import Fraction as Q
from math import isqrt,gcd

def add(p,q): return p[0]+q[0],p[1]+q[1]
def sub(p,q): return p[0]-q[0],p[1]-q[1]
def mul(p,t): return p[0]*t,p[1]*t
def cross(p,q): return p[0]*q[1]-p[1]*q[0]
def norm(p): return p[0]*p[0]+p[0]*p[1]+p[1]*p[1]
def area(P): return sum(cross(P[i],P[(i+1)%len(P)]) for i in range(len(P)))
def ccw(P): return P if area(P)>0 else P[::-1]
def inside(p,P):return all(cross(sub(P[(i+1)%len(P)],P[i]),sub(p,P[i]))>=0 for i in range(len(P)))
def sep(P,R):
    for S,T in [(P,R),(R,P)]:
        for i in range(len(S)):
            a,b=S[i],S[(i+1)%len(S)]
            if all(cross(sub(b,a),sub(p,a))<=0 for p in T):return True
    return False
def sides(P):return sorted(norm(sub(P[i],P[(i+1)%3])) for i in range(3))
def check(a,b,c):
    assert 0<a<b and c*c==a*a+a*b+b*b
    u=(Q(b),Q(a)); O=(Q(0),Q(0)); A=(Q(b*c),Q(0))
    B=mul(u,c); D=(Q((a+b)*c),Q(0)); C=mul(u,Q(b*(2*a+b),c))
    E=add(A,mul(u,Q(a*b,c))); F=add(A,(Q(0),Q(b*c)))
    target=ccw([O,D,C]); polys=list(map(ccw,[[O,A,B],[A,D,E],[D,C,E],[A,E,C,B]]))
    base=sorted([a*a,b*b,c*c])
    for P,k in [(polys[0],c),(polys[1],a),(polys[2],a),([F,A,E],b),([F,B,C],b-a)]:
        assert sides(P)==[k*k*z for z in base],(a,b,c,P,k)
    assert B==add(F,mul(sub(A,F),Q(b-a,b)))
    assert C==add(F,mul(sub(E,F),Q(b-a,b)))
    for P in polys:
        assert area(P)>0 and all(inside(p,target) for p in P)
    assert sum(map(area,polys))==area(target)
    assert all(sep(P,R) for i,P in enumerate(polys) for R in polys[:i])
    assert area(target)/Q(a*b)==(2*a+b)*(a+b)
    return {'tile':[a,b,c], 'count':(2*a+b)*(a+b), 'macro_counts':[c*c,a*a,a*a,b*b-(b-a)**2]}

if __name__=='__main__':
    checked=[]
    for a in range(1,301):
        for b in range(a+1,501):
            if gcd(a,b)>1:continue
            c=isqrt(a*a+a*b+b*b)
            if c*c==a*a+a*b+b*b:checked.append(check(a,b,c))
    print('Verified exact convex macro partition for',len(checked),'primitive triples')
    print(checked[:12])
