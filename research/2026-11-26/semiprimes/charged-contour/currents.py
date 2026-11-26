"""Integer separation of the two pair currents and physical contour conservation."""
from collections import Counter

import numpy as np
from scipy.sparse import coo_matrix, csc_matrix, hstack

from area import indices
from geometry import UNITS, add, conjugate, det, exact_divide, layout, multiply, scale, shapes, subtract
from grammar import restrict_edges


def axis_of(p, q):
    d = subtract(q,p)
    return next(i for i in range(3) if det(UNITS[i],d)==0)


def terms(totals, frame, p, q, a, b):
    axis = axis_of(p,q)
    for m in (a,b):
        totals[('end',frame,m,axis,p[0]%m,p[1]%m)] -= 1
        totals[('end',frame,m,axis,q[0]%m,q[1]%m)] += 1


def system(a,b,c,l,word_id,s,t,profile,edges,shifts,active):
    segments,pi,xmin,ymin,stride,_ = layout(a,b,c,l,word_id,s,t)
    znum = (a,b) if s==1 else (a+b,-b)
    target = Counter({('count',i):n for i,n in enumerate(profile)})
    for p,q in segments:
        terms(target,0,p,q,a,b)
    row_index = {}
    rows,cols,values = [],[],[]
    column = 0
    def local(point,frame):
        if frame==0:
            return exact_divide(point,c)
        return exact_divide(multiply(conjugate(znum),subtract(point,(c*t,0))),c*c)
    for i,(shape,mask) in enumerate(zip(shapes(a,b,c,s),restrict_edges(edges,shifts,active))):
        for site in indices(mask):
            site=int(site)
            p=add((t,0),multiply(pi,(xmin+site%stride,ymin+site//stride)))
            tail=scale(c,p)
            apex=add(tail,shape[1])
            head=add(tail,shape[2])
            # On a terminal single the physical contour follows the CCW long side.
            # On a parent single it follows that side backwards.
            fr=int(i<3)
            u,w=(head,tail) if fr else (tail,head)
            coeff=Counter({('count',i):1,('site',site):-1,('site',site+shifts[i]):1})
            terms(coeff,fr,local(u,fr),local(apex,fr),a,b)
            terms(coeff,fr,local(apex,fr),local(w,fr),a,b)
            terms(coeff,1-fr,local(w,1-fr),local(u,1-fr),a,b)
            for key,value in coeff.items():
                if value:
                    rows.append(row_index.setdefault(key,len(row_index)))
                    cols.append(column)
                    values.append(value)
            column+=1
    for key,value in target.items():
        if value:
            row_index.setdefault(key,len(row_index))
    M=coo_matrix((values,(rows,cols)),shape=(len(row_index),column),dtype=np.int64).tocsc()
    return M,np.array([target[key] for key in row_index],dtype=np.int64)


def gap(matrix,rhs,y):
    assert y.shape==rhs.shape and y.dtype==np.int64
    bound=max(map(abs,map(int,y)),default=0)*(int(abs(matrix).sum())+int(abs(rhs).sum()))
    assert bound<2**62
    return int(y@rhs-np.maximum(0,matrix.T@y).sum())


def discover(matrix,rhs):
    """Propose a certificate. The replay needs only integer verification."""
    from scipy.optimize import linprog
    model=hstack([matrix,csc_matrix(rhs.reshape(-1,1))],format='csc')
    objective=np.r_[np.zeros(matrix.shape[1]),1.]
    result=linprog(objective,A_eq=model,b_eq=rhs,bounds=(0,1),method='highs',
                   options={'time_limit':30})
    if not result.success or result.fun < 1e-6:
        return None
    # Prefer small coefficients. A successful threshold or rescaling still
    # undergoes the full integer comparison over every matrix column.
    for factor in (1,3,10,30,100,1000,100000,10000000):
        y=np.rint(result.eqlin.marginals*factor).astype(np.int64)
        if gap(matrix,rhs,y)>0:
            return y
    return None
