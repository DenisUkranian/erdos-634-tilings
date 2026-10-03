"""Minimal exact Laurent-polynomial arithmetic for symbolic identities.

This is not used by the geometric generator/checker. A polynomial is a
finite mapping of three integral exponents to rational coefficients;
division is allowed only by a nonzero monomial.
"""
from fractions import Fraction


class Polynomial:
    def __init__(self,data=0):
        source=data if type(data) is dict else {(0,0,0):Fraction(data)}
        self.terms={p:Fraction(c) for p,c in source.items() if c}
    def __add__(self,other):
        other=coerce(other);out=dict(self.terms)
        for p,c in other.terms.items():out[p]=out.get(p,0)+c
        return Polynomial(out)
    __radd__=__add__
    def __neg__(self):return Polynomial({p:-c for p,c in self.terms.items()})
    def __sub__(self,other):return self+-coerce(other)
    def __rsub__(self,other):return coerce(other)+-self
    def __mul__(self,other):
        other=coerce(other);out={}
        for p,c in self.terms.items():
            for q,d in other.terms.items():
                key=tuple(x+y for x,y in zip(p,q))
                out[key]=out.get(key,0)+c*d
        return Polynomial(out)
    __rmul__=__mul__
    def __truediv__(self,other):
        other=coerce(other)
        if len(other.terms)!=1:raise ValueError('Division requires a monomial')
        q,d=next(iter(other.terms.items()))
        return Polynomial({tuple(x-y for x,y in zip(p,q)):c/d for p,c in self.terms.items()})
    def __rtruediv__(self,other):return coerce(other)/self
    def __pow__(self,n):
        if type(n) is not int or n<0:raise ValueError('Nonnegative integral power required')
        out=Polynomial(1)
        for _ in range(n):out*=self
        return out
    def __bool__(self):return bool(self.terms)
    def __repr__(self):return repr(self.terms)


def coerce(value):return value if isinstance(value,Polynomial) else Polynomial(value)
u=Polynomial({(1,0,0):1})
v=Polynomial({(0,1,0):1})
T=Polynomial({(0,0,1):1})


class Vector(tuple):
    def __new__(cls,x,y):return tuple.__new__(cls,(coerce(x),coerce(y)))
    def __add__(self,q):return Vector(self[0]+q[0],self[1]+q[1])
    def __sub__(self,q):return Vector(self[0]-q[0],self[1]-q[1])
    def __mul__(self,k):return Vector(self[0]*k,self[1]*k)
    def __rmul__(self,k):return self*k

