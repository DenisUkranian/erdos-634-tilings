"""Disjoint short populations, gate owners and corrected even charge variation."""
import sys
from functools import lru_cache
import json
from pathlib import Path

def ceil(n,d):return -(-n//d)

def solve(c,d,a,b,N,W,offset,split):
    limit=W//2
    budget=N-(c+d)*W+d+3*c
    if budget<0:return None,[]
    @lru_cache(None)
    def options(kind,e,own=None,arrive=0):
        # Shift the two exceptional costs to make every cost nonnegative.
        k=abs(e)
        G=c*e+(d if kind=='C' else 0)
        sign=1 if G>=0 else -1
        R=sign*(d*e+(2*c if kind=='C' else -c if kind=='T' else 0))
        shift=d+2*c if kind=='C' else c if kind=='T' else 0
        m0=0
        if kind=='C':
            m0=(19 if G>=0 else 8) if c==37 else (5 if G>=0 else 27)
        elif k==1 or (k==2 and c==43):
            m0=c
        out={}
        for m in range(m0,(budget+(c+d)*k-shift-abs(G)-abs(R))//2+1,c):
            n=abs(G)+2*m
            if kind=='C' and n<(64 if c==37 else 75):continue
            if kind!='C' and n==c:continue
            p=m+(a*abs(G)+(offset if kind=='C' else 0))//b
            for l in range(1,2*c+1):
                if own is not None and not -m<=sign*own<=p:continue
                native=sign*own if own is not None else 0
                J=max(0,ceil(abs(G)-native-(l-(own is not None))*p,d))
                remaining=R-sign*arrive
                if J and p<d:continue
                gates=ceil(J,p//d) if J else 0
                if kind!='C' and l==1 and n*(1002 if c==37 else 1001)<abs(G)*(3810 if c==37 else 4304):
                    gates=max(1,gates)
                if gates+l>2*c:continue
                cost=n+2*(2 if c==37 else 3)*c*gates+abs(arrive)+max(abs(remaining),2*c*J-remaining)-(c+d)*k+shift
                assert cost>=0
                if cost<=budget:
                    out[2-l]=min(out.get(2-l,budget+1),cost)
        return prune(out)
    def prune(out):
        best=budget+1;ans={}
        for s in sorted(out,reverse=True):
            if out[s]<best:
                best=ans[s]=out[s]
        return ans
    def combine(x,y):
        z={}
        for i,u in x.items():
            for j,v in y.items():
                if u+v<=budget:z[i+j]=min(z.get(i+j,budget+1),u+v)
        return prune(z)
    reg={k:options('ordinary',k) for k in range(1,limit+1)}
    group=[{0:0}]
    for total in range(1,limit+1):
        out={}
        for k in range(1,total+1):
            for s,v in combine(group[total-k],reg[k]).items():out[s]=min(v,out.get(s,budget+1))
        group.append(prune(out))
    C={e:options('C',e) for e in range(-limit,limit+1)}
    T={e:options('T',e) for e in range(-limit,limit+1)}
    @lru_cache(None)
    def side(kind,charge,P,M):
        e=charge+P-M
        rest=combine(group[P],group[M])
        result={}
        V=39 if c==37 else 59
        for o in range(-(V-1)//2,(V+1)//2+1):
            I=kind=='C'
            own=c*e+d*I-d*o
            arrive=d*e-c*o+(2*c if I else -c)
            minimum=budget+1
            for l,v in options(kind,charge,own,arrive).items():
                for s,u in rest.items():
                    if l+s>=1:
                        minimum=min(minimum,v+u)
            if minimum<=budget:result[o]=minimum
        return result
    @lru_cache(None)
    def middle(q,r):
        # Positive and negative B populations are independent multiples of c.
        lowerP=ceil(max(q,0)+max(r,0),c)
        lowerM=ceil(max(-q,0)+max(-r,0),c)
        best=N+1
        for size in range(lowerP+lowerM,N//c+1):
            if size*c-abs(q)-abs(r)>=best:break
            if size==1:continue
            for pos in range(lowerP,size-lowerM+1):
                neg=size-pos
                if a*c*pos+(b-a)*c*neg>=b*max(0,q,r) and a*c*neg+(b-a)*c*pos>=b*max(0,-q,-r):
                    g=pos-neg
                    outside=abs(g-(q+r)//c)
                    assert (q+r)%c==0
                    base=c*size-abs(q)-abs(r)
                    if outside:
                        odd=max(c*outside,3*c if outside==1 else 0)
                        fee=odd+2*c*ceil(d*outside,c)
                        base+=fee
                    best=min(best,base)
        return best
    best_surplus=None
    results=[]
    for e,x in C.items():
        for f,y in T.items():
            P=limit-max(e,0)-max(f,0); M=limit-max(-e,0)-max(-f,0)
            if min(P,M)<0:continue
            joined=combine(combine(x,y),combine(group[P],group[M]))
            if not joined:continue
            score=max(joined)
            best_surplus=score if best_surplus is None else max(best_surplus,score)
            if score<2 or not split:continue
            best=2*(budget+1)
            for i in range(P+1):
                for j in range(M+1):
                    L=side('C',e,i,j)
                    E=e+i-j
                    for o,l in L.items():
                        for t,r in side('T',f,P-i,M-j).items():
                            if l+r>budget:continue
                            if abs(o)+abs(t)+abs(1-o-t)>(39 if c==37 else 59):continue
                            best=min(best,l+r+middle(d*E-c*o+2*c,-d*E-c*t-c))
            results.append((e,f,best))
    return best_surplus,results
def control(cert,offset,name):
    from verify import branch, cell, geom, reconstruct, step
    from collections import Counter
    g=geom.Geometry(*cert['tile'])
    tiles,_=geom.read_tiles(g,name)
    polys,*_=geom.check_full_tiling(g,tiles)
    lifts,T=reconstruct(g,tiles,polys)
    C=T[:1]
    owners=Counter()
    counts=Counter()
    received=Counter()
    charges=Counter()
    for i,tile in enumerate(tiles):
        v=lifts[i]
        w=step(v,cell(g,tile[1]+tile[3],g.vertices(tile)[-1]))
        sign=-geom.eps(tile)
        owners[v,w,sign]+=1
        counts[v,sign]+=1
        charges[v]+=sign
        received[w]+=sign
    for (v,w,sign),num in owners.items():
        right=(cert['positive_coefficient']*counts[v,sign]+
               cert['negative_coefficient']*counts[v,-sign]+offset*(v==C))
        assert num*cert['denominator']<=right
    for v in {w for w,_ in counts}|set(received)|{C,T}:
        if v[-1][0]%2:continue
        d=g.a-g.b
        e=(charges[v]-d*(v==C))//g.c
        assert g.c*e==charges[v]-d*(v==C)
        assert received[v]==d*e+2*g.c*(v==C)-g.c*(v==T)
    B=T[:-1]
    def current(v,w):
        return owners[v,w,1]-owners[v,w,-1]
    native=[]
    for root in (C,T):
        chosen=[i for i in range(len(tiles)) if lifts[i]!=B and branch(B,lifts[i])==root]
        even=sum(-geom.eps(tiles[i]) for i in chosen if tiles[i][1]%2==0)
        odd=sum(-geom.eps(tiles[i]) for i in chosen if tiles[i][1]%2==1)
        e=(even-d*(root==C))//g.c
        o=odd//g.c
        assert current(root,B)==even-d*o
        assert current(B,root)==d*e-g.c*o+(2*g.c if root==C else -g.c)
        native.append(current(B,root))
    outside=sum(charges[v] for v in charges if v!=B and branch(B,v) not in (C,T)
                and v[-1][0]%2)
    assert sum(native)-charges[B]==outside
    return dict(tiles=len(tiles),occupied_signed_gates=len(owners),native=native,
                axial_received=received[C],slant_received=received[T])


def replay():
    from remote_sectors import sectors
    root=Path(__file__).resolve().parents[3]
    median=root/'2026-11-20/semiprimes/continuation/global-closure/median'
    sys.path.insert(0,str(median))
    from verify_gate_capacity import verify_certificate
    results={}
    for cert in json.loads((median/'gate_capacity_certificates.json').read_text()):
        verify_certificate(cert)
        a,b,c=cert['tile']
        offset=2*max(max(row)-min(row) for row in cert['endpoint_tables'])
        if c==7:
            results['controls']={name:control(cert,offset,name) for name in ('known','macro')}
            continue
        cap=40 if c==37 else 60
        N=(2*a+b)*(a+2*b)
        d=a-b
        A,B=cert['positive_coefficient'],cert['denominator']
        degrees={}
        for W in range(56 if c==37 else 80,cap-1,-2):
            best,pairs=solve(c,d,A,B,N,W,offset,W==cap)
            degrees[W]=best
            if W>cap:assert best is None or best<2
            else:assert best==2 and pairs and min(z for _,_,z in pairs)>N-(c+d)*W+d+3*c
        results[str(N)]=dict(maximum_even_variation=cap-2,source_allowance=offset,
          relaxed_surplus=degrees,boundary_cases_at_excluded_value=pairs,
          exterior_free=sectors(c,d,A,B,N,cap-2,39 if c==37 else 59,offset))
    return results


if __name__=='__main__':
    if not __debug__:raise SystemExit('Enable assertions.')
    print(json.dumps(replay(),indent=2))
