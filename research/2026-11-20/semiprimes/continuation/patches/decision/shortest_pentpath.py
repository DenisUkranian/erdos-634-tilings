"""Test all shortest net inventories in the two-height median cut alphabet."""
from functools import lru_cache
def add(p,q):return p[0]+q[0],p[1]+q[1]
def sub(p,q):return p[0]-q[0],p[1]-q[1]
def tb(n,p):return n*p[0],n*p[1]
def cr(p,q):return p[0]*q[1]-p[1]*q[0]
def mul(p,q):return p[0]*q[0]-p[1]*q[1],p[0]*q[1]+p[1]*q[0]+p[1]*q[1]
def positive(P):return P if cr(sub(P[1],P[0]),sub(P[2],P[0]))>0 else P[::-1]
def disjoint(P,Q):
    return any(all(cr(sub(t,s),sub(x,s))<=0 for x in Y)
               for X,Y in ((P,Q),(Q,P)) for s,t in zip(X,X[1:]+X[:1]))
def pent(a,b,c,t,k,j):
    O=(0,0);Y=(0,(j*c+t*b)*c);W=(t*a*c-k*c*c,Y[1])
    D=(t*a*c-k*a*a,Y[1]-k*a*b)
    E=(D[0]+j*a*b,D[1]+j*(b*b-c*c))
    return [O,Y,W,D,E] if j else [O,Y,W,D]
from path_bound import netmin

def scan(a,b,c,t,k,j,ceiling=None,stop_after_witness=False):
    board=pent(a,b,c,t,k,j);O=board[0];W=board[2];unit=a*b*c*c
    N=-sum(cr(p,q) for p,q in zip(board,board[1:]+board[:1]))//unit
    def inside(p):
        return all(cr(sub(q,r),sub(p,r))<=0 for r,q in zip(board,board[1:]+board[:1]))
    r=(1,0);moves={}
    for i in range(6):
        for vec,ap,h in [((c,0),(a*a,a*b),0),((a,b),(a*c,0),1)]:
            moves[h,i]=(mul(r,tb(c,vec)),mul(r,ap))
        r=mul(r,(0,1))
    arc=t*(a-b)-(k+j)*c
    F0=(k+j)*c-t*(a-b);F1=t*c-(k+j)*(a-b)
    def valid(size,B,Z):
        d=a-b
        if B%(d-c) or Z%(d+c):return False
        D,Dstar=B//(d-c),Z//(d+c)
        return (size-D)%2==0 and (size-Dstar)%2==0
    best,hist=netmin(a,b,c,t,k,j,ceiling)
    out=[]
    def counts():
        def allocations(n,slots):
            if slots==1:
                yield (n,)
                return
            for i in range(n+1):
                for tail in allocations(n-i,slots-1):yield (i,)+tail
        for d0,d1 in hist:
            delta=best-sum(abs(i) for i in d0+d1)
            if delta%2:continue
            for extra in allocations(delta//2,6):
                idx=[];qty=[]
                for h,d in enumerate((d0,d1)):
                    for i,v in enumerate(d):
                        spare=extra[3*h+i]
                        for rot,num in [(i,max(v,0)+spare),(i+3,max(-v,0)+spare)]:
                            if num:idx.append((h,rot));qty.append(num)
                yield d0,d1,idx,tuple(qty)
    for d0,d1,idx,qty in counts():
        total=arc+sum(c*(-1)**i*n for (h,i),n in zip(idx,qty))
        star=arc+sum(c*(-1)**(i+h)*n for (h,i),n in zip(idx,qty))
        def children(P,r):
            for i,n in enumerate(r):
                if not n:continue
                v,ap=moves[idx[i]]; Q=add(P,v); A=add(P,ap)
                if not inside(Q) or not inside(A):continue
                rr=list(r);rr[i]-=1;rr=tuple(rr)
                yield i,Q,A,rr
        @lru_cache(None)
        def areas(P,r):
            if not any(r):
                assert P==O
                return {0}
            acc=set()
            for i,Q,A,rr in children(P,r):
                off=cr(P,Q)
                acc.update(off+v for v in areas(Q,rr))
            return acc
        base=cr(board[1],W)
        raw=areas(W,qty)
        integral={v for v in raw if (v+base)%unit==0}
        def admissible(v):
            n=-(v+base)//unit
            return valid(n,total,star) and valid(N-n,F0+F1+total,F0-F1+star)
        validareas=poss={r for r in integral if admissible(r)}
        def exact(P,r,area,tiles,word,seen):
            if not any(r):return list(word)
            for i,Q,A,rr in children(P,r):
                if Q in seen:continue
                tr=positive((P,Q,A));area1=area+cr(P,Q)
                if not any(z+area1 in validareas for z in areas(Q,rr)):continue
                if any(not disjoint(tr,T) for T in tiles):continue
                z=exact(Q,rr,area1,tiles+[tr],word+[idx[i]],seen|{Q})
                if z is not None:return z
        word=exact(W,qty,0,[],[],{W}) if poss else None
        out.append((d0,d1,len(raw),sorted(-(v+base)//unit for v in integral),sorted(-(v+base)//unit for v in poss),word))
        if stop_after_witness and word is not None:break
    return best,out
if __name__=='__main__':
    for aa in [(33,7,37,13,8,1),(35,13,43,11,2,1),(33,7,37,26,23,1),(35,13,43,22,17,1)]:
        print(aa,scan(*aa),flush=True)
