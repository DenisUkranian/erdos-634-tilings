"""Build endpoint matrix on the supplied complete candidate pool. Explicit axis dictionary."""
import argparse
from math import gcd
from pathlib import Path
import gzip
import numpy as np
from scipy.sparse import coo_matrix, csr_matrix

def axis(dx,dy):
    g=gcd(dx,dy)
    if (dx,dy)<(0,0): g=-g
    return dx//g,dy//g

def matrix(path):
    with path.open() as stream: D,N,nc=map(int,stream.readline().split())
    P=np.loadtxt(path,skiprows=1,dtype=np.int64,ndmin=2)
    shapes=np.loadtxt(str(path)+'.shapes',skiprows=1,dtype=np.int64,ndmin=2)
    assert len(P)==nc and D==729 and N==180
    shapes=[[(0,0),(int(qx),int(qy)),(int(rx),int(ry))] for qx,qy,rx,ry in shapes]
    board=[(0,0),(60*D,0),(30*D,60*D)]
    axes=sorted({axis(q[0]-p[0],q[1]-p[1]) for C in shapes+[board] for p,q in zip(C,C[1:]+C[:1])})
    axisnum={a:i for i,a in enumerate(axes)}
    rows=np.empty((nc,6),np.int64); target=[]
    for o,C in enumerate(shapes+[board]):
        if o<len(shapes):
            ids=np.flatnonzero(P[:,0]==o); x=P[ids,1]; y=P[ids,2]
        else: x=0;y=0
        for i,(p,q) in enumerate(zip(C,C[1:]+C[:1])):
            a=axisnum[axis(q[0]-p[0],q[1]-p[1])]
            for j,(dx,dy) in enumerate((p,q)):
                u=x+dx;v=y+dy
                assert np.all((u>=0)&(u<65536)&(v>=0)&(v<65536))
                k=a*2**32+u*65536+v
                if o<len(shapes): rows[ids,i*2+j]=k
                else: target.append(k)
    un,ids=np.unique(np.r_[rows.ravel(),target],return_inverse=True)
    b=np.zeros(len(un),np.int32);np.add.at(b,ids[-6:],(1,-1)*3)
    A=coo_matrix((np.tile(np.array((1,-1)*3,np.int8),nc),(ids[:-6],np.repeat(np.arange(nc),6))),shape=(len(un),nc)).tocsr()
    return axes,un,b,A

def warm(path,scale,axes,un):
    dic={a:i for i,a in enumerate(axes)}; out=np.zeros(len(un),np.int64)
    with gzip.open(path,'rt') as f:
        dat=np.loadtxt(f,dtype=np.int64)
    for a,i in dic.items():
        idx=(dat[:,2]==a[0])&(dat[:,3]==a[1]);d=dat[idx]; k=i*2**32+d[:,0]*(65536*scale)+d[:,1]*scale
        ii=np.searchsorted(un,k);keep=ii<len(un);ii=ii[keep];kk=k[keep];dd=d[keep,4];good=un[ii]==kk
        out[ii[good]]=dd[good]
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('pool',type=Path);ap.add_argument('out',type=Path);ap.add_argument('--iterations',type=int,default=40000);ap.add_argument('--step',type=float,default=47);ap.add_argument('--warm',type=int,choices=(0,9,27),default=0);args=ap.parse_args()
    axes,un,b,A=matrix(args.pool);AT=A.T.tocsr();n=A.shape[1]
    print('shape',A.shape,'nnz',A.nnz,'degrees',dict(zip(*np.unique(np.diff(A.indptr),return_counts=True))),flush=True)
    weights={0:np.zeros(len(un),np.int64)}
    for d,s in [(9,''),(27,'-d27')]:
        path=Path(__file__).resolve().parents[1]/'alpha'/'tiles659'/('grid180'+s+'-weights.tsv.gz')
        w=warm(path,729//d,axes,un);weights[d]=w; positive=np.maximum(AT@w-1000000,0)
        print('lift',d,'demand',int(b@w),'excess',int(positive.sum()),'lower',int(b@w)-int(positive.sum()),flush=True)
    K=A.astype(float);KT=K.T.tocsr();sigma=args.step/np.maximum(1,np.diff(K.indptr));tau=1/(6*args.step);y=weights[args.warm].astype(float)/1e6;x=np.zeros(n);z=x.copy();best=-np.inf
    for it in range(1,args.iterations+1):
        y+=sigma*(b-K@z);w=KT@y; old=x;x=np.clip(x+tau*(w-1),0,1);z=2*x-old
        if it%100==0:
            ys=np.rint(1e6*y).astype(np.int64);demand=int(ys@b);cap=int(np.maximum(AT@ys-1000000,0).sum());val=demand-cap
            if it%500==0 or val>180e6: print(it,'lower',val/1e6,'demand',demand/1e6,'excess',cap/1e6,flush=True)
            if val>best:best=val
            if val>180e6:
                with gzip.open(args.out,'wt') as f:
                    for k,v in zip(un[ys!=0],ys[ys!=0]):
                        a=int(k>>32);p=(int(k)>>16)&65535;q=int(k)&65535; print(p,q,*axes[a],v,file=f)
                return
    print('best',best/1e6,flush=True)

if __name__=='__main__': main()
