"""Optional sparse certificate pricing direction for endpoint LP relaxations.

This does not decide tileability. It finds another feasible dual of a finite
current LP with positive objective, minimizing its endpoint support L1 norm.
"""
import time
import numpy as np
from scipy.sparse import coo_matrix,hstack,vstack
from scipy.optimize import linprog

def sparsify(mat,heads,ub,limits,cost,valid_positive,negative,objective,
             endpoint_cap=1.0,keep_fraction=0.5,time_limit=30):
    nr,nc=mat.shape
    select=np.flatnonzero(np.asarray(valid_positive,dtype=bool)|np.asarray(negative,dtype=bool))
    pos=np.flatnonzero(np.asarray(valid_positive,dtype=bool)[select])
    K=len(select);np0=len(pos);nu=ub.shape[0]
    S=mat[:,select].T.tocsc();Q=ub[:,select].T.tocsc()
    upper=coo_matrix((-np.ones(np0),(pos,np.arange(np0))),shape=(K,np0)).tocsc()
    constr=hstack([S,-S,-Q,upper],format='csc')
    goal=max(0.0,float(objective)*keep_fraction)
    margin=np.r_[-np.asarray(heads),np.asarray(heads),np.asarray(limits),np.ones(np0)]
    constraints=vstack([constr,coo_matrix(margin.reshape(1,-1))],format='csc')
    rhs=np.r_[np.asarray(cost)[select],-goal]
    weight=np.r_[np.ones(2*nr),np.full(nu,0.001),np.full(np0,0.001)]
    bounds=[(0,endpoint_cap)]*(2*nr)+[(0,None)]*(nu+np0)
    start=time.time()
    result=linprog(weight,A_ub=constraints,b_ub=rhs,bounds=bounds,method='highs-ds',options={'threads':1,'time_limit':time_limit})
    if not result.success:return None,dict(status=result.message,seconds=time.time()-start)
    u=result.x;y=u[:nr]-u[nr:2*nr];penalties=u[2*nr:2*nr+nu]
    profit=float(np.asarray(heads)@y-np.asarray(limits)@penalties-u[2*nr+nu:].sum())
    worst=float(np.max(constraints@u-rhs))
    if profit<=0 or worst>1e-6:return None,dict(status='nonpositive or inaccurate sparse candidate',profit=profit,worst=worst)
    return (y,-penalties),dict(status='feasible sparse dual',profit=profit,L1=float(abs(y).sum()),support=int(np.count_nonzero(abs(y)>1e-10)),seconds=time.time()-start)
