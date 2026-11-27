"""Rational mixed-area certificates covering every orientation of a physical cut."""
from fractions import Fraction as F
from functools import cmp_to_key
from itertools import combinations
from math import gcd
from pathlib import Path
import json
import numpy as np
from saturation import letters,UNITS

HERE=Path(__file__).resolve().parent

def det(p,q): return p[0]*q[1]-p[1]*q[0]
def edges(P): return [(b[0]-a[0],b[1]-a[1]) for a,b in zip(P,P[1:]+P[:1])]
def mixed_edges(P,ee): return sum(max(det(p,e) for p in P) for e in ee)
def mul(p,q): return (p[0]*q[0]-p[1]*q[1],p[0]*q[1]+p[1]*q[0]+p[1]*q[1])
def angle_cmp(p,q):
    hp=p[1]<0 or (p[1]==0 and p[0]<0)
    hq=q[1]<0 or (q[1]==0 and q[0]<0)
    if hp!=hq: return int(hp)-int(hq)
    d=det(p,q)
    return (d<0)-(d>0)

def sorted_polygon(vectors):
    x=y=0
    P=[]
    for u,v in sorted(vectors,key=cmp_to_key(angle_cmp)):
        if u or v:
            P.append((x,y)); x+=u; y+=v
    assert x==y==0
    return P

def templates(W,dirs):
    yield W
    for v in dirs: yield [(0,0),v]
    for x,y,z in combinations(sorted(dirs,key=cmp_to_key(angle_cmp)),3):
        h,k,l=det(y,z),det(z,x),det(x,y)
        if min(h,k,l)<=0: continue
        d=gcd(h,gcd(k,l))
        yield [(0,0),(x[0]*(h//d),x[1]*(h//d)),(-z[0]*(l//d),-z[1]*(l//d))]

def rotation(sector,r):
    # (1+r*rho)/(1+r*conj(rho)), followed by a sixth turn.
    k,d=r.numerator,r.denominator
    den=d*d+d*k+k*k
    u,v=mul(UNITS[sector],(d*d-k*k,2*k*d+k*k))
    return u,v,den

def choose(G):
    # Floating proposals only. The integer weights are checked below.
    v=np.zeros(len(G)); v[0]=1.
    for _ in range(160):
        g=G@v
        i=int(np.argmax(g)); j=int(np.argmin(np.where(v>1e-10,g,np.inf)))
        gain=g[i]-g[j]
        if gain<1e-10 or i==j: break
        curvature=2*G[i,j]-G[i,i]-G[j,j]
        step=min(v[j],gain/curvature) if curvature>0 else v[j]
        v[i]+=step; v[j]-=step
    return [max(0,round(x*100000)) for x in v]

def certify(a,b,c,vectors,dirs,threshold):
    A,B=b*(2*a+b),a*(a+2*b)
    T=[(0,0),(A,0),(0,B)]
    W=sorted_polygon(vectors)
    shapes=list(templates(W,dirs)); ee=list(map(edges,shapes)); count=len(shapes)+1
    costs=[A*B]+[mixed_edges(W,g) for g in ee]
    raw=[[0]*count for _ in range(count)]
    raw[0][0]=A*B
    for i,P in enumerate(shapes,1):
        for j,g in enumerate(ee,1): raw[i][j]=mixed_edges(P,g)
    assert all(raw[i][j]==raw[j][i] for i in range(1,count) for j in range(1,count))
    target=threshold*a*b
    denom=np.outer(np.array(costs,dtype=float),costs)
    G=np.array(raw,dtype=float)*target/denom
    leaves=0
    def interval(sector,lo,hi,T):
        nonlocal leaves
        angles=[rotation(sector,r) for r in (lo,(lo+hi)/2,hi)]
        tris=[[mul((u,v),p) for p in T] for u,v,d in angles]
        mid=tris[1]; den=angles[1][2]
        # Freeze one support vertex per template edge on this whole interval.
        choices=[[max(range(3),key=lambda k:det(mid[k],e)) for e in g] for g in ee]
        for j,(g,ks) in enumerate(zip(ee,choices),1):
            val=sum(det(mid[k],e) for k,e in zip(ks,g))/den
            G[0,j]=G[j,0]=val*target/denom[0,j]
        weights=choose(G)
        w=[F(k,d) for k,d in zip(weights,costs)]
        used=[i for i in range(1,count) if weights[i]]
        fixed=raw[0][0]*w[0]**2+sum(w[i]*w[j]*raw[i][j] for i in used for j in used)
        rhs=sum(weights)**2
        vals=[]
        for h in (0,2):
            val=sum(w[i]*sum(det(tris[h][k],e) for k,e in zip(choices[i-1],ee[i-1])) for i in used)
            vals.append(F(val,angles[h][2]))
        cross=min(vals)
        if rhs and cross>=0 and target*(fixed+2*w[0]*cross)>rhs:
            leaves+=1
            return True
        if hi-lo<=F(1,512): return False
        middle=(lo+hi)/2
        return interval(sector,lo,middle,T) and interval(sector,middle,hi,T)
    for hand in (T,[(x+y,-y) for x,y in T]):
        for k in range(6):
            if not interval(k,F(0),F(1),hand): return False
    assert leaves>=12
    return True

def run():
    a,b,c=33,7,37
    rows=[]
    for one,file,bound in [(False,'SATURATION.json',2701),(True,'ONE_DEFECT.json',2849)]:
        data=json.loads((HERE/file).read_text())
        cases=data['3431']['profiles'] if one else data['37']
        for row in cases:
            dirs,_=letters(a,b,c,a)
            counts=list(row['prefix'] if one else row['inventory'])
            if one:
                d=dirs[row['exception_axis']]
                dirs.append((-d[0],-d[1]));counts.append(1)
            vectors=[(x*k,y*k) for (x,y),k in zip(dirs,counts)]
            old=row['cap'] if one else row['population_cap']
            threshold=bound
            if old>=threshold and not certify(a,b,c,vectors,dirs,threshold):
                threshold+=2*c
                if old>=threshold:
                    assert certify(a,b,c,vectors,dirs,threshold)
            rows.append(dict(owners=sum(counts),counts=counts,exception=row.get('exception_axis'),
                             cap=min(old,threshold-2*c)))
    return dict(maximum={m:max(r['cap'] for r in rows if r['owners']==m) for m in (63,65)},cases=rows)

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
