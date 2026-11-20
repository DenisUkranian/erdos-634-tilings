#!/usr/bin/env python3
"""Both native long gates of a three-height spine layer, with closed pairs.

This is a necessary residue projection, not a geometric tiling model.
"""
from collections import defaultdict
from pathlib import Path
import argparse
import json
import time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix,vstack,hstack

U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))


def model(a,b,c):
    labels=[];ii=[];jj=[];vv=[]
    def gate(q,j,s):
        x=q[0]-a*U[j][0];y=q[1]-a*U[j][1]
        return ((a*y-b*x) if s==1 else (a*x-b*y))%c==0
    def tile_rows(q,j,s):
        x,y=q;u=x-a*U[j][0],y-a*U[j][1]
        k=(j+s)%6;w=x+b*U[k][0],y+b*U[k][1]
        for axis,p,coef in ((j,q,s),(j,u,-s),(k,w,s),(k,q,-s)):
            yield (axis%3)*c*c+(p[0]%c)*c+p[1]%c,coef
    def append(q,j,s,pair):
        row=defaultdict(int)
        for r,v in tile_rows(q,j,s):row[r]+=v
        eps=s*(-1 if j%2 else 1)
        if pair:
            k=(j+s)%6
            mate=(q[0]-a*U[j][0]+b*U[k][0],
                  q[1]-a*U[j][1]+b*U[k][1])
            assert not gate(mate,(j+3)%6,s)
            for r,v in tile_rows(mate,(j+3)%6,s):row[r]+=v
            positive=negative=1
        else:
            positive=int(eps==1);negative=int(eps==-1)
        col=len(labels);labels.append((q[0],q[1],j,s,int(pair),positive,negative))
        row[3*c*c]+=positive;row[3*c*c+1]+=negative
        for r,v in row.items():
            if v:ii.append(r);jj.append(col);vv.append(v)
    for x in range(c):
        for y in range(c):
            for j in range(6):
                for s in (-1,1):
                    opened=gate((x,y),j,s)
                    if opened or j<3:
                        append((x,y),j,s,not opened)
    matrix=coo_matrix((vv,(ii,jj)),shape=(3*c*c+2,len(labels))).tocsc()
    assert sum(not label[4] for label in labels)==12*c
    assert sum(label[4] for label in labels)==6*c*(c-1)
    return matrix,labels


def solve(a,b,c,time_limit):
    matrix,labels=model(a,b,c)
    rhs=np.r_[np.zeros(3*c*c),2*c,c]
    start=time.monotonic()
    result=linprog(np.zeros(matrix.shape[1]),A_eq=matrix,b_eq=rhs,
                   bounds=(0,None),method='highs',options={'time_limit':time_limit})
    report={'tile':[a,b,c],'rows':matrix.shape[0],'columns':matrix.shape[1],
            'open_singles':12*c,'closed_pairs':6*c*(c-1),
            'status':int(result.status),'message':result.message,
            'seconds':time.monotonic()-start,
            'scope':'Necessary full-spine residue projection with both native gates; fractional feasibility is not a tiling.'}
    if result.x is not None:
        report['maximum_float_residual']=float(np.max(abs(matrix@result.x-rhs)))
        report['support']=[list(labels[k])+[float(v)] for k,v in enumerate(result.x) if v>1e-8]
    if result.status==2:
        # Seek a bounded endpoint potential with free sign multipliers.
        dual_cost=np.r_[np.zeros(3*c*c),2*c,c]
        dual=linprog(dual_cost,A_ub=-matrix.T,b_ub=np.zeros(matrix.shape[1]),
                     bounds=[(-1,1)]*(3*c*c)+[(None,None)]*2,
                     method='highs',options={'time_limit':time_limit})
        report['dual_status']=int(dual.status)
        if dual.x is not None:
            report['dual_objective']=float(dual.fun)
            f=np.rint(dual.x[:-2]*1000000).astype(np.int64)
            scores=np.asarray(matrix[:-2].T@f,dtype=np.int64)
            # Round sign multipliers upward, then independently increase
            # both until every integer column inequality holds.
            P,Q=np.ceil(dual.x[-2:]*1000000).astype(np.int64)
            sign_rows=matrix[-2:].toarray().astype(np.int64)
            residual=scores+P*sign_rows[0]+Q*sign_rows[1]
            correction=max(0,int(-min(residual)))
            P+=correction;Q+=correction
            exact=scores+P*sign_rows[0]+Q*sign_rows[1]
            assert min(exact)>=0
            score=int(2*c*P+c*Q)
            report['exact_certificate']={'endpoint_tables':f.reshape(3,c,c).tolist(),
                                         'sign_bounds':[int(P),int(Q)],
                                         'weighted_population':score,
                                         'all_column_inequalities':True}
            report['exact_exclusion']=score<0
    return report


def minimum(a,b,c,time_limit):
    matrix,labels=model(a,b,c)
    endpoint=matrix[:-2]
    positive=np.asarray(matrix[-2].toarray()).ravel()
    negative=np.asarray(matrix[-1].toarray()).ravel()
    cost=positive+negative
    charge=positive-negative
    equation=vstack((endpoint,coo_matrix(charge.reshape(1,-1)))).tocsc()
    rhs=np.r_[np.zeros(3*c*c),c]
    start=time.monotonic()
    result=linprog(cost,A_eq=equation,b_eq=rhs,bounds=(0,None),
                   method='highs',options={'time_limit':time_limit})
    report={'tile':[a,b,c],'rows':equation.shape[0],'columns':equation.shape[1],
            'status':int(result.status),'message':result.message,
            'seconds':time.monotonic()-start,
            'scope':'Minimum-population necessary full-spine residue projection with charge c; no geometric realization asserted.'}
    if result.x is not None:
        report['floating_population']=float(result.fun)
        report['floating_blocks']=float(result.fun/c)
    if result.status==0:
        y=np.asarray(result.eqlin.marginals)
        f=np.rint(y[:-1]*1000000).astype(np.int64)
        t=int(round(y[-1]*1000000))
        scores=np.asarray(endpoint.T@f,dtype=np.int64)+t*charge.astype(np.int64)
        integer_cost=cost.astype(np.int64)
        D=max(1,max(-((-int(score))//int(weight)) for score,weight in zip(scores,integer_cost)))
        assert np.all(scores<=D*integer_cost)
        report['exact_certificate']={'endpoint_tables':f.reshape(3,c,c).tolist(),
                                     'charge_multiplier':t,'tile_bound':D,
                                     'population_lower_numerator':c*t,
                                     'population_lower_denominator':D,
                                     'all_column_inequalities':True}
        report['exact_exclusion_3c']=t>3*D
        report['exact_lower_fraction']=f'{c*t}/{D}'
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('a',type=int);p.add_argument('b',type=int);p.add_argument('c',type=int)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--time-limit',type=float,default=20)
    p.add_argument('--minimize-population',action='store_true')
    args=p.parse_args()
    report=(minimum if args.minimize_population else solve)(args.a,args.b,args.c,args.time_limit)
    args.out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('support','exact_certificate')},indent=2))


if __name__=='__main__':
    main()
