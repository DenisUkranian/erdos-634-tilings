"""Basis-preserving numerical LP wrapper; exact certificates remain independent."""
import time
import numpy as np
from scipy.sparse import vstack
from scipy.optimize import OptimizeResult
from scipy.optimize._highspy import _core as hs


class WarmLP:
    def __init__(self):
        self.basis = None
        self.col_ids = None
        self.row_ids = None

    def solve(self, cost, *, A_eq, b_eq, A_ub, b_ub, bounds, layout,
              method=None, options=None):
        nr, nc, artificial = layout
        ne = A_eq.shape[0]
        nu = A_ub.shape[0]
        # Identity persists when real columns are inserted before artificials.
        col_ids = list(range(nc))
        if artificial:
            col_ids += [10**9+i for i in range(nr)]
            col_ids += [2*10**9+i for i in range(nr)]
        row_ids = list(range(nr))
        row_ids += [10**9+i for i in range(ne-nr)]
        row_ids += [2*10**9+i for i in range(nu)]
        matrix = vstack([A_eq, A_ub], format='csc')
        lp = hs.HighsLp()
        lp.num_col_ = len(cost)
        lp.num_row_ = ne+nu
        lp.col_cost_ = np.asarray(cost, dtype=float)
        lp.col_lower_ = np.array([0 if v[0] is None else v[0] for v in bounds], dtype=float)
        lp.col_upper_ = np.array([hs.kHighsInf if v[1] is None else v[1] for v in bounds], dtype=float)
        lp.row_lower_ = np.r_[b_eq, np.full(nu,-hs.kHighsInf)]
        lp.row_upper_ = np.r_[b_eq,b_ub]
        lp.a_matrix_.format_ = hs.MatrixFormat.kColwise
        lp.a_matrix_.start_ = matrix.indptr.astype(np.int32)
        lp.a_matrix_.index_ = matrix.indices.astype(np.int32)
        lp.a_matrix_.value_ = matrix.data
        engine = hs._Highs()
        engine.setOptionValue('output_flag',False)
        engine.setOptionValue('threads',1)
        engine.setOptionValue('solver','simplex')
        engine.setOptionValue('time_limit',float((options or {}).get('time_limit',60)))
        engine.passModel(lp)
        warm = False
        if self.basis is not None:
            old_c = dict(zip(self.col_ids,self.basis.col_status))
            old_r = dict(zip(self.row_ids,self.basis.row_status))
            basis = hs.HighsBasis()
            basis.col_status = [old_c.get(i,hs.HighsBasisStatus.kLower) for i in col_ids]
            basis.row_status = [old_r.get(i,hs.HighsBasisStatus.kBasic) for i in row_ids]
            warm = engine.setBasis(basis) == hs.HighsStatus.kOk
        start = time.time()
        engine.run()
        status = engine.getModelStatus()
        solution = engine.getSolution()
        info = engine.getInfo()
        success = status == hs.HighsModelStatus.kOptimal
        if success:
            self.basis = engine.getBasis()
            self.col_ids = col_ids
            self.row_ids = row_ids
        return OptimizeResult(success=success,
            message=engine.modelStatusToString(status),
            fun=engine.getObjectiveValue(),
            x=np.array(solution.col_value),
            eqlin=OptimizeResult(marginals=np.array(solution.row_dual[:ne])),
            ineqlin=OptimizeResult(marginals=np.array(solution.row_dual[ne:])),
            warm_start=warm,seconds=time.time()-start,
            nit=info.simplex_iteration_count)


if __name__ == '__main__':
    from scipy.sparse import csr_matrix
    problem = WarmLP()
    for n in (1,2):
        r=problem.solve(np.r_[np.zeros(n),1,1],
            A_eq=csr_matrix([[*([1]*n),1,-1]]),b_eq=np.array([1.5]),
            A_ub=csr_matrix([[*([1]*n),0,0]]),b_ub=np.array([2]),
            bounds=[(0,1)]*n+[(0,None)]*2,layout=(1,n,True))
        assert r.success
        assert abs(r.fun-(.5 if n==1 else 0))<1e-8
        print(n,r.fun,r.x.tolist(),r.warm_start,r.nit)
