#!/usr/bin/env python3
"""Bounded LP probe; report NO only with an exactly replayed integer ray."""
import argparse
from array import array
from fractions import Fraction
import json, os, sys, time
from pathlib import Path
sys.path.insert(0, os.environ.get('ERDOS_CERT_SOLVERS_PATH','/tmp/erdos634-cert-solvers'))
import highspy
import numpy as np
from scipy.sparse import csr_matrix


def load(path, count):
    starts=array('i',[0]); indices=array('i'); values=array('b'); rhs=array('q')
    with open(path) as src:
        nv,nsel=map(int,next(src).split())
        for _ in range(nv+nsel):next(src)
        for line in src:
            b,n,*lits=map(int,line.split())
            assert n==len(lits)
            rhs.append(b)
            for z in lits:
                assert 1<=abs(z)<=nv
                indices.append(abs(z)-1);values.append(1 if z>0 else -1)
            starts.append(len(indices))
    if count is not None:
        rhs.append(count-nsel)
        indices.extend(range(nv));values.extend([1]*nv);starts.append(len(indices))
    B=csr_matrix((np.frombuffer(values,dtype=np.int8),
                  np.frombuffer(indices,dtype=np.int32),
                  np.frombuffer(starts,dtype=np.int32)),shape=(len(rhs),nv))
    return nv,nsel,B,np.frombuffer(rhs,dtype=np.int64)


def integer_ray(B,b,ray,prefix):
    r=np.asarray(ray,dtype=np.float64)
    mx=float(np.max(np.abs(r)))
    if not np.isfinite(mx) or mx==0:return None
    r=r/mx
    for scale in [1,2,3,4,5,6,8,10,12,16,20,24,32,48,64,96,128,256,512,1024,
                  100,1000,10000,100000,1000000,10000000,100000000,1000000000]:
        for sign in [1,-1]:
            y=np.rint(r*(scale*sign)).astype(np.int64)
            # Exact int64 arithmetic is safe: each |y_i|<=1e9, nnz<2^31,
            # and this instance's sum(abs(b)) is checked before multiplication.
            assert len(B.data)*scale < 2**63
            assert sum(abs(int(z)) for z in b)*scale < 2**63
            coefficients=B.T@y
            assert coefficients.dtype==np.int64
            lhs=int(y@b)
            rhs=sum(max(int(z),0) for z in coefficients)
            if lhs>rhs:
                pairs=[[int(i),int(y[i])] for i in np.flatnonzero(y)]
                cert=dict(format='integer_interval_farkas_v1',row_multipliers=pairs,
                          lhs=lhs,rhs=rhs,gap=lhs-rhs,scale=scale,sign=sign)
                Path(str(prefix)+'.exact_ray.json').write_text(json.dumps(cert)+'\n')
                return {k:cert[k] for k in ['lhs','rhs','gap','scale','sign']}|{'support':len(pairs)}
    return None


def main():
    p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('prefix')
    p.add_argument('--seconds',type=float,default=180);p.add_argument('--count',type=int,default=135)
    p.add_argument('--solver',choices=['simplex','ipm'],default='simplex');a=p.parse_args()
    start=time.monotonic();nv,nsel,B,b=load(a.source,a.count)
    print(json.dumps(dict(stage='loaded',variables=nv,selected=nsel,rows=B.shape[0],nonzeros=B.nnz,seconds=time.monotonic()-start)),flush=True)
    h=highspy.Highs();h.setOptionValue('threads',1);h.setOptionValue('parallel','off')
    h.setOptionValue('time_limit',a.seconds);h.setOptionValue('solver',a.solver)
    h.setOptionValue('random_seed',634);h.setOptionValue('presolve','on')
    h.setOptionValue('simplex_strategy',1)
    lp=highspy.HighsLp();lp.num_col_=nv;lp.num_row_=B.shape[0]
    lp.col_cost_=np.zeros(nv);lp.col_lower_=np.zeros(nv);lp.col_upper_=np.ones(nv)
    lp.row_lower_=b.astype(float);lp.row_upper_=b.astype(float)
    lp.a_matrix_.format_=highspy.MatrixFormat.kRowwise
    lp.a_matrix_.start_=B.indptr;lp.a_matrix_.index_=B.indices
    lp.a_matrix_.value_=B.data.astype(float)
    assert h.passModel(lp)==highspy.HighsStatus.kOk
    h.run();status=h.getModelStatus();report=dict(status=h.modelStatusToString(status),
        variables=nv,rows=B.shape[0],nonzeros=B.nnz,selected=nsel,count=a.count,
        seconds=time.monotonic()-start,solver=a.solver,highs_version=h.version(),
        exact_certificate=False,global_E135_decided=False)
    if status==highspy.HighsModelStatus.kInfeasible:
        ray_status,exists,ray=h.getDualRay();report['dual_ray_exists']=exists
        report['dual_ray_status']=str(ray_status)
        if exists:
            np.save(str(a.prefix)+'.float_ray.npy',ray)
            cert=integer_ray(B,b,ray,a.prefix)
            if cert is not None:
                report['exact_certificate']=True;report['integer_ray']=cert
    elif status==highspy.HighsModelStatus.kOptimal:
        sol=h.getSolution();x=np.asarray(sol.col_value)
        report['max_equation_error']=float(np.max(np.abs(B@x-b)))
        report['support_above_1e-8']=int(np.count_nonzero(x>1e-8))
        np.savez_compressed(str(a.prefix)+'.fractional_solution.npz',x=x)
    report['total_seconds']=time.monotonic()-start
    Path(str(a.prefix)+'.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report),flush=True)


if __name__=='__main__':main()
