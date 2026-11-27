"""Check the two tables as inductive certificates, without executing their recurrence."""
import numpy as np


def review(model, N, tree, forest):
    c, d, A, D = model.c, model.d, model.A, model.D
    cap = N//c+1
    terminal, single = ((91,22),(3810,1002)) if c==37 else ((83,13),(4304,1001))
    split = []
    for p in (0,1):
        xs,ys = model.ranges[p],model.ranges[1-p]
        X,Y = np.meshgrid(np.array(xs),np.array(ys),indexing='ij')
        assert np.all(forest[p]<=tree[p])
        minima = np.full(X.shape,cap)
        for i,x in enumerate(xs):
            for j,y in enumerate(ys):
                U,V = x-X,y-Y
                valid = ((X!=0)|(Y!=0)) & ((U!=0)|(V!=0))
                valid &= (U>=xs.start)&(U<xs.stop)&(V>=ys.start)&(V<ys.stop)
                if np.any(valid):
                    total = tree[p][valid]+forest[p][U[valid]-xs.start,V[valid]-ys.start]
                    minima[i,j] = min(cap,int(total.min()))
        assert np.all(forest[p]<=minima)
        split.append(minima)

    for p in (0,1):
        xs,ys = model.ranges[p],model.ranges[1-p]
        # For each root charge x-z enumerate candidate positive and negative
        # populations directly, testing every possible y at once.
        Y,Z = np.meshgrid(np.array(ys),np.array(xs),indexing='ij')
        for i,x in enumerate(xs):
            k = x-Z
            u,v = c*x-d*Y,d*Y-c*Z
            bound = tree[p][i,:,None]
            required = (x!=0)|(Y!=0)
            for n in range(2,cap):
                P,M = c*(n+k)//2,c*(n-k)//2
                allowed = ((n-k)%2==0)&(P>=0)&(M>=0)
                if n==2 and c==43:
                    allowed &= (P>0)&(M>0)
                allowed &= P>=np.maximum(0,u)+np.maximum(0,v)
                allowed &= M>=np.maximum(0,-u)+np.maximum(0,-v)
                def gate(q):
                    return D*abs(q)<=np.where(q>=0,A*P+(D-A)*M,A*M+(D-A)*P)
                admissible = required & allowed & gate(u)
                assert np.all(~admissible | (bound<=n+split[1-p]))
                one = admissible & gate(v) & ((Y!=0)|(Z!=0))
                one &= ((u!=0)&(v!=0))|(n*single[1]>=abs(k)*single[0])
                assert np.all(~one | (bound<=n+tree[1-p]))
                if x and n>=abs(x) and (n-x)%2==0:
                    # No child with nonzero vector. Distinguish a genuine
                    # terminal from a root with occupied neutral descendants.
                    b = tree[p][i,-ys.start]
                    if n*terminal[1]>=abs(x)*terminal[0]:
                        assert b<=n
                    if n*single[1]>=abs(x)*single[0]:
                        assert b<=n+2
