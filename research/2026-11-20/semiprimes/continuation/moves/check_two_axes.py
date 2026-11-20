"""Exact boundary-word diagnostic for at most two effective F2 directions."""
from itertools import combinations, product
from functools import reduce
from math import gcd,lcm
import numpy as np
import sympy as S


def rotate(v,j):
    """Multiply an Eisenstein pair by rho to the j-th power."""
    x,y=v
    for _ in range(j % 6): x,y=-y,x+y
    return x,y


def coeff(w, h, j):
    """Multiply the five complex coefficients by rho minus its conjugate."""
    a,b,c=w
    levels=[(-b,a),(-c,2*c),(b-a,a)]
    row=[0]*10
    for k,v in enumerate(levels):
        i=2*(k+h)
        row[i:i+2]=rotate(v,j)
    return row


def words(a,b,c,length):
    return [(i,j,(length-a*i-b*j)//c) for i in range(length//a+1)
            for j in range((length-i*a)//b+1)
            if length-a*i-b*j>=c and (length-a*i-b*j)%c==0]


def integral(v):
    v=[S.Rational(x) for x in v]
    d=lcm(*[q.q for q in v]);x=[int(q*d) for q in v]
    g=reduce(gcd,x)
    return [q//g for q in x]


def product_rows(rows):
    x,y,s=[np.asarray(r,dtype=np.int64) for r in rows]
    return (x[:,None,None,:]+y[None,:,None,:]+s[None,None,:,:]).reshape(-1,10)


def tile_flow(X,Y,Z,directions,diffs,n):
    T=np.zeros((7,3,3),dtype=np.int64)
    for (h,j),word,sign in [((0,0),X,1),((0,1),Y,-1),((2,1),Z,1)]+[(ij,w,-1) for ij,w in zip(directions,diffs)]:
        T[h+2,j,:]+=sign*np.array(word)
    prev=[np.zeros(3,dtype=np.int64),np.zeros(3,dtype=np.int64)]
    total=0
    for k in range(1,len(T)):
        A=T[k,:,0];B=T[k,:,1]
        U=prev[-2]+T[k-1,:,2]+A
        D=A-U
        pred=np.array([-U[2],U[0],U[1]])+np.array([D[1],D[2],-D[0]])
        if not np.array_equal(B,pred):return False
        prev.append(U)
        total+=np.sum(abs(U))+np.sum(abs(D))
    tail_empty = not np.any(prev[-2:])
    return tail_empty and total <= n and (n-total)%2 == 0


def tests(a,b,c,u,v,g):
    X=words(a,b,c,b*(2*a+b));Y=words(a,b,c,a*(a+2*b));Z=words(a,b,c,c*c)
    E=product_rows([[coeff(q,h,j) for q in rows] for rows,h,j in [(X,0,0),(Y,0,4),(Z,2,1)]])
    base=(v,-u,v)
    alt=(u+v,v,-u)
    if g==3:alt=tuple((p+q)//3 for p,q in zip(base,alt))
    assert all(a*i+b*j+c*k==0 for i,j,k in (base,alt))
    nall=0;nint=0;types={};examples=[]
    for ij in combinations(product(range(3), range(3)),2):
        if ij[0][0]==ij[1][0] and ij[0][0]!=1:continue
        M=S.Matrix([coeff(w,h,j) for h,j in ij for w in (base,alt)]).T
        N=np.asarray([integral(n) for n in M.T.nullspace()],dtype=np.int64)
        assert int(np.abs(E).max())*sum(map(abs,map(int,N.flatten())))<2**62
        keep=np.arange(len(E))
        for nr in N:
            if not len(keep):break
            keep=keep[(E[keep]@nr)==0]
        nall+=len(keep)
        if not len(keep):continue
        # For independent columns the unique coefficients must be integers.
        assert M.rank()==4
        ids=M.T.rref()[1]; W=M[list(ids),:].inv()
        den=lcm(*[w.q for w in W]);K=np.asarray(W*den,dtype=np.int64)
        assert int(np.abs(E).max())*sum(map(abs,map(int,K.flatten())))<2**62
        mult=E[keep][:,list(ids)]@K.T
        mask=np.all(mult%den==0,axis=1)
        keep=keep[mask];mult=mult[mask]//den
        nx,ny,ns=np.unravel_index(keep,(len(X),len(Y),len(Z)))
        outer=np.asarray(X)[nx]+np.asarray(Y)[ny]+np.asarray(Z)[ns]
        net=mult@np.array([base,alt,base,alt],dtype=np.int64)
        parity=np.all((net+outer)%2==((a+2*b)*(2*a+b))%2,axis=1)
        keep=keep[parity];mult=mult[parity]
        mask=[]
        for k,m in zip(keep,mult):
            x,y,z=np.unravel_index(k,(len(X),len(Y),len(Z)))
            diffs=np.array(m).reshape((2,2))@np.array([base,alt])
            mask.append(tile_flow(X[x],Y[y],Z[z],ij,diffs,(a+2*b)*(2*a+b)))
        keep=keep[np.array(mask,dtype=bool)];mult=mult[np.array(mask,dtype=bool)]
        nint+=len(keep)
        if len(keep):
            types[ij]=len(keep)
            for kk,m in zip(keep,mult):
                xi,yi,si=map(int,np.unravel_index(kk,(len(X),len(Y),len(Z))))
                assert ij==((0,0),(1,0)) and Y[yi]==(0,a-b,c) and Z[si]==(0,0,c)
                examples.append((ij,X[xi],Y[yi],Z[si],m.tolist()))
    assert (nall,nint)=={(33,7,37):(84,15),(35,13,43):(149,30)}[a,b,c]
    m=u+2*v if g==1 else u
    d=a-b
    short_norm=min(x+y+d+c-z for x,y,z in X)
    count_bound=sum(((m-2)*q+m-1)//m for q in (short_norm,2*c+d))
    assert count_bound=={(33,7,37):130,(35,13,43):123}[a,b,c]
    print((a,b,c),list(map(len,(X,Y,Z))),nall,nint,types, 'T bound',count_bound)
    print('example:',examples[:2]);return types
if __name__=='__main__':
    tests(33,7,37,10,1,3);tests(35,13,43,6,1,1)
