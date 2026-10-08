#!/usr/bin/env python3
"""Positive exact placement search for a (3,5,7) ideal trapezoid.

No failure here excludes arbitrary tilings. Positions are on a specified
two-level Eisenstein lattice; nonnegative integral boundary solutions give
genuine tilings, independently checked by verify.py.
"""
import argparse, json, math, time
from pathlib import Path
import numpy as np
from scipy.sparse import csc_matrix
from scipy.optimize import milp, Bounds, LinearConstraint

def rho(p): return (-p[1],p[0]+p[1])
def main():
    ap=argparse.ArgumentParser();ap.add_argument('x',type=int);ap.add_argument('leg',type=int)
    ap.add_argument('--seconds',type=float,default=300);ap.add_argument('--lp',action='store_true')
    ap.add_argument('--levels',default='0,1');ap.add_argument('--macro',action='store_true');ap.add_argument('--no-heuristics',action='store_true');ap.add_argument('--save-model',action='store_true');ap.add_argument('--simplex',action='store_true');a=ap.parse_args();start=time.monotonic()
    root=Path(__file__).resolve().parent;label=f'T{a.x}_{a.leg}_{a.levels.replace(",","-")}'+('_macro' if a.macro else '')
    c=7;r=2;P=np.array([(0,0),(c*(a.x+a.leg),0),(c*a.x,c*a.leg),(0,c*a.leg)],dtype=np.int64)
    points=np.array([(i,j) for j in range(c*a.leg+1) for i in range((r*j)%c,c*(a.x+a.leg)-j+1,c)],dtype=np.int64)
    if a.macro:points=points[(points[:,0]%7==0)&(points[:,1]%7==0)]
    variants=[];expansions=[]
    for h in map(int,a.levels.split(',')):
        assert h in (0,1)
        if a.macro and h!=0:continue
        for x,y in ((3,5),(5,3)):
            u=(c*x,0) if h==0 else (3*x,5*x)
            v=(-c*y,c*y) if h==0 else (-8*y,3*y)
            for rot in range(6):
                variants.append((h,rot,x,y,((0,0),u,v)));expansions.append([((0,0),u,v)]);u=rho(u);v=rho(v)
    if a.macro:
        import importlib.util,sys
        src=root.parents[1]/'group2-trapezoids';sys.path.insert(0,str(src))
        spec=importlib.util.spec_from_file_location('macro_verifier',src/'verify.py');checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)
        for aa,bb in ((3,5),(5,3)):
            seed=json.loads((src/f'certificates/seed_{aa}_{bb}_7.json').read_text());base=[]
            for block in seed['blocks'][1:4]:base.extend(checker.check_block(block,[aa,bb,7],True)[2])
            assert len(base)==35
            polygon=[(bb,aa),(8*bb,aa),(7*bb,0),(49,0),(bb*bb,15)]
            outer=[(0,0),(49,0),(bb*bb,15)]
            for polygon,base,origin in [(polygon,base,(bb,aa)),(outer,checker.triangle_grid(outer,7),(0,0))]:
                for reflect in (False,True):
                    poly=[(7*(u-origin[0]),7*(v-origin[1])) for u,v in polygon]
                    tris=[[(int(7*(u-origin[0])),int(7*(v-origin[1]))) for u,v in t] for t in base]
                    if reflect:
                        poly=[(u+v,-v) for u,v in poly][::-1];tris=[[(u+v,-v) for u,v in t][::-1] for t in tris]
                    for rot in range(6):
                        variants.append((2,rot,len(base),reflect,tuple(poly)));expansions.append(tris)
                        poly=[rho(p) for p in poly];tris=[[rho(p) for p in t] for t in tris]
    blocks=[]
    for *_,V in variants:
        mask=np.ones(len(points),dtype=bool)
        for sh in V:
            shifted=points+sh
            for i in range(4):
                e=P[(i+1)%4]-P[i];w=shifted-P[i]
                mask &= e[0]*w[:,1]-e[1]*w[:,0]>=0
        blocks.append(points[mask])
    def segments(T):
        T=list(T)
        for p,q in zip(T,T[1:]+T[:1]):
            dx=int(q[0]-p[0]);dy=int(q[1]-p[1]);g=math.gcd(dx,dy);ux=dx//g;uy=dy//g
            k=c//math.gcd(c,ux-r*uy);assert g%k==0;n=g//k;d=(ux*k,uy*k);sg=1
            if d<(0,0):d=(-d[0],-d[1]);sg=-1
            for j in range(n):
                w=(int(p[0])+j*ux*k,int(p[1])+j*uy*k)
                if sg<0:w=(w[0]-d[0],w[1]-d[1])
                yield w,d,sg
    S=[list(segments(V)) for *_,V in variants];tar=list(segments(P));dirs=sorted({d for z in S+[tar] for _,d,_ in z});D={d:i for i,d in enumerate(dirs)}
    xmax=int(P[:,0].max())+1;ymax=int(P[:,1].max())+1
    def key(d,x,y):return (D[d]*xmax+x)*ymax+y
    counts=[len(b) for b in blocks];N=sum(counts);nz=sum(n*len(s) for n,s in zip(counts,S))
    keys=np.empty(nz,dtype=np.int64);data=np.empty(nz,dtype=np.int8);indptr=np.empty(N+1,dtype=np.int64);indptr[0]=0
    ptr=col=0
    for ct,pts,segs in zip(counts,blocks,S):
        z=len(segs);kb=keys[ptr:ptr+ct*z].reshape(ct,z);db=data[ptr:ptr+ct*z].reshape(ct,z)
        for j,(p,d,sg) in enumerate(segs):kb[:,j]=key(d,pts[:,0]+p[0],pts[:,1]+p[1]);db[:,j]=sg
        indptr[col+1:col+ct+1]=ptr+z*np.arange(1,ct+1,dtype=np.int64);ptr+=ct*z;col+=ct
    tk=np.array([key(d,p[0],p[1]) for p,d,_ in tar],dtype=np.int64)
    uniq,inv=np.unique(np.concatenate([keys,tk]),return_inverse=True)
    b=np.zeros(len(uniq),dtype=np.int32)
    for ri,(_,_,sg) in zip(inv[nz:],tar):b[ri]+=sg
    B=csc_matrix((data,inv[:nz],indptr),shape=(len(uniq),N));B.sum_duplicates()
    report={'target_short_base':a.x,'target_leg':a.leg,'tile':[3,5,7],'levels':[-1,0,1] if a.macro else list(map(int,a.levels.split(','))),
            'lattice':'integer macro translations' if a.macro else '(i+j*rho)/7 with i=2j mod 7','macro_mode':a.macro,'placements':N,'rows':B.shape[0],'entries':int(B.nnz),'lattice_points':len(points)}
    print(json.dumps(report),flush=True)
    R=B.tocsr();lo=R.minimum(0).sum(axis=1).A.ravel().astype(int);hi=R.maximum(0).sum(axis=1).A.ravel().astype(int)
    rhs=b.copy();values=np.full(N,-1,dtype=np.int8);from collections import deque
    queue=deque(np.flatnonzero((rhs<=lo)|(rhs>=hi)));queued=np.zeros(len(b),bool);queued[list(queue)]=True;conflict=None
    while queue:
        row=queue.popleft();queued[row]=False
        if rhs[row]<lo[row] or rhs[row]>hi[row]:conflict=int(row);break
        if rhs[row]!=lo[row] and rhs[row]!=hi[row]:continue
        low=rhs[row]==lo[row]
        for k in range(R.indptr[row],R.indptr[row+1]):
            col=R.indices[k]
            if values[col]>=0:continue
            val=int(R.data[k]<0) if low else int(R.data[k]>0);values[col]=val
            inds=B.indices[B.indptr[col]:B.indptr[col+1]];sg=B.data[B.indptr[col]:B.indptr[col+1]]
            rhs[inds]-=sg*val;lo[inds]+=(sg<0);hi[inds]-=(sg>0)
            for rr in inds[(~queued[inds])&((rhs[inds]<=lo[inds])|(rhs[inds]>=hi[inds]))]:queue.append(rr);queued[rr]=True
    unknown=np.flatnonzero(values<0);report.update(propagation_conflict=conflict,assigned=int(sum(values>=0)),forced_ones=int(sum(values==1)),remaining=len(unknown))
    print(json.dumps(report),flush=True)
    if conflict is not None:report['status']='RESTRICTED_PROPAGATION_INFEASIBLE'
    else:
        rr=np.flatnonzero((lo!=0)|(hi!=0)|(rhs!=0));M=B[rr,:][:,unknown].astype(float)
        if a.save_model:
            from scipy.sparse import save_npz
            save_npz(root/(label+'_reduced_matrix.npz'),M);np.save(root/(label+'_reduced_rhs.npy'),rhs[rr])
        if a.simplex:
            from scipy.optimize import linprog
            a.lp=True
            cost=np.random.default_rng(634).uniform(0,1,len(unknown))
            result=linprog(cost,A_eq=M,b_eq=rhs[rr],bounds=(0,1),method='highs-ds',options={'time_limit':a.seconds,'presolve':True,'disp':True})
        else:result=milp(np.zeros(len(unknown)),integrality=np.zeros(len(unknown)) if a.lp else np.ones(len(unknown)),
                    bounds=Bounds(0,1),constraints=LinearConstraint(M,rhs[rr],rhs[rr]),
                    options={'time_limit':a.seconds,'presolve':True,'disp':True,**({'mip_heuristic_effort':0.0} if a.no_heuristics else {})})
        report.update(solver_status=int(result.status),solver_message=result.message,lp_relaxation=a.lp)
        if result.x is not None and np.max(np.abs(result.x-np.rint(result.x)))<1e-6:
            values[unknown]=np.rint(result.x).astype(np.int8);assert np.all(B@values==b)
            chosen=np.flatnonzero(values==1);offset=np.cumsum([0]+counts);triangles=[]
            for col in chosen:
                vi=int(np.searchsorted(offset,col,side='right')-1);p=blocks[vi][col-offset[vi]]
                triangles.extend([[[int(t) for t in p+q] for q in tri] for tri in expansions[vi]])
            cert={'format':'exact_trapezoid_unit_v1','denominator':7,'tile':[3,5,7],'target':P.tolist(),'triangles':triangles,'levels':report['levels']}
            (root/(label+'_certificate.json')).write_text(json.dumps(cert));report['status']='EXACT_INTEGRAL_BOUNDARY_SOLUTION';report['tiles']=len(triangles)
        elif result.status==2:report['status']='RESTRICTED_SOLVER_INFEASIBLE_UNCERTIFIED'
        elif a.lp and result.status==0:report['status']='FRACTIONAL_FEASIBLE_ONLY'
        else:report['status']='INCOMPLETE'
    report['seconds']=time.monotonic()-start
    (root/(label+('_lp' if a.lp else '')+'_report.json')).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)

if __name__=='__main__':main()
