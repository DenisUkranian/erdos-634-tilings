#!/usr/bin/env python3
"""Coefficientwise polynomial checks, using only integer arithmetic.

These check algebraic identities, not the geometric classification or placement
lemmas. Laurent exponents are permitted in the formal signature tests.
"""
import json
from pathlib import Path

class Poly(dict):
    def __init__(self,x=0):
        if isinstance(x,int):x={(0,0,0):x} if x else {}
        super().__init__((e,c) for e,c in x.items() if c)
    def __add__(self,other):
        out=dict(self)
        for e,c in Poly(other).items():out[e]=out.get(e,0)+c
        return Poly(out)
    __radd__=__add__
    def __neg__(self):return Poly({e:-c for e,c in self.items()})
    def __sub__(self,other):return self+-Poly(other)
    def __rsub__(self,other):return Poly(other)+-self
    def __mul__(self,other):
        out={}
        for e,c in self.items():
            for f,d in Poly(other).items():
                g=tuple(x+y for x,y in zip(e,f));out[g]=out.get(g,0)+c*d
        return Poly(out)
    __rmul__=__mul__
    def __pow__(self,n):
        if not isinstance(n,int) or n<0:raise ValueError('Use monomial() for Laurent inverses')
        out=Poly(1)
        for _ in range(n):out=out*self
        return out

def monomial(i=0,j=0,k=0):return Poly({(i,j,k):1})
u,v,z=monomial(1),monomial(0,1),monomial(0,0,1)

def H(s):
    a,b,c=s
    return (a+b+c)*(-a+b+c)*(a-b+c)*(a+b-c)

def reduce_norm(poly,sign):
    a,b,c=u,v,z;out=Poly()
    for (i,j,k),co in poly.items():
        if min(i,j,k)<0:raise ValueError('Not an ordinary norm polynomial')
        out+=co*monomial(i,j,k%2)*(a*a+sign*a*b+b*b)**(k//2)
    return out

def main():
    identities=[]
    def check(name,poly):
        if poly:raise ValueError((name,dict(poly)))
        identities.append({'name':name,'nonzero_residual_coefficients':0})
    a=u*v;b=v*v-u*u;c=v*v;Q=b+c;P=b+2*c
    rows=[('W',(v**3,u*Q,v*b),Q),('beta',(v**3,v**3,u*P),P),
          ('theta',(b*v,b*v,b*u),b),('alpha',(b*c,b*c,b*Q),b*Q),
          ('other-scalene',(c*c,c*Q,b*P),Q*P)]
    for name,target,n in rows:check('Group1 '+name+' area',H(target)-n*n*H((a,b,c)))
    check('Double-angle area',H((b*u,b*u,b*v))-b*b*H((u*u,b,u*v)))
    # The complete directional signatures, with Laurent z.
    p=c+b*z*z-a*z**3;pstar=c+b*monomial(k=-2)-a*monomial(k=-3)
    hW=u*Q+v*b*z-v**3*monomial(k=-3)
    hB=u*P-v**3*(z**3+monomial(k=-3))
    hT=b*(u+v*(z+monomial(k=-1)))
    check('Tile signature factorization',p-(v-u*z)*(v*z*z+u*z+v))
    check('W formal boundary identity',hW-v*(monomial(k=-1)-monomial(k=-3))*p-u*z*z*pstar)
    check('Beta formal boundary identity',hB-v*(monomial(k=-1)-monomial(k=-3))*p-(u*z*z-v*z**3)*pstar)
    check('Theta formal boundary identity',hT-v*monomial(k=-1)*p-u*z*z*pstar)
    # Algebra in Q[a,b,c]/(c^2-a^2-sign*a*b-b^2).
    a,b,c=u,v,z
    for sign in (-1,1):check('Equilateral area, norm sign '+str(sign),reduce_norm(H((a*b,a*b,a*b))-(a*b)**2*H((a,b,c)),sign))
    rows=[('F1',(a*b,b*c,b*(a+b)),b*(a+b)),('I',(b*c,b*c,b*(a+2*b)),b*(a+2*b)),
          ('F3',(c*c,c*(a+2*b),3*b*(a+b)),3*(a+2*b)*(a+b)),
          ('F4',(a*c,b*(2*a+b),c*(a+b)),(2*a+b)*(a+b)),
          ('F2',(a*(a+2*b),b*(2*a+b),c*c),(a+2*b)*(2*a+b))]
    for name,target,n in rows:check(name+' area',reduce_norm(H(target)-n*n*H((a,b,c)),1))
    X=c+a-b;Y=c+b-a
    check('F1 first character simplification',reduce_norm(b*(2*a+b-c)-X*(c-a),1))
    check('F1 second character simplification',reduce_norm(b*(2*a+b+c)-Y*(c+a),1))
    check('Isosceles first character simplification',reduce_norm(b*(a+2*b-2*c)-X*(c-a-b),1))
    check('Isosceles second character simplification',reduce_norm(b*(a+2*b+2*c)-Y*(c+a+b),1))
    report={'status':'PASS_COEFFICIENTWISE','identities':identities,'count':len(identities),
            'meaning':'Exact polynomial identities, not sampled evaluations; geometric hypotheses are proved separately.'}
    Path(__file__).with_name('symbolic_checks.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
