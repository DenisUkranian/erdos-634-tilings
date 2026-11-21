#!/usr/bin/env python3
"""Independent geometric integer audit of the exceptional-core duals."""
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'research').is_dir() and (p/'scripts').is_dir())
CORE=HERE.parent/'core-budget'
U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))

def axis(v):
    if v[1]==0:return 0
    if v[0]==0:return 1
    if v[0]+v[1]==0:return 2
    return None

def sub(p,q):return(p[0]-q[0],p[1]-q[1])
def mul(p,q):return(p[0]*q[0]-p[1]*q[1],p[0]*q[1]+p[1]*q[0]+p[1]*q[1])
def norm(v):return v[0]*v[0]+v[0]*v[1]+v[1]*v[1]

def endpoint_row(q,j,s,a,b,c):
    u=(q[0]-a*U[j][0],q[1]-a*U[j][1]);w=(q[0]+b*U[(j+s)%6][0],q[1]+b*U[(j+s)%6][1])
    poly=(u,q,w)if s==1 else(w,q,u)
    assert sum(p[0]*r[1]-p[1]*r[0]for p,r in zip(poly,poly[1:]+poly[:1]))==a*b
    out=Counter()
    for p,r in zip(poly,poly[1:]+poly[:1]):
        if norm(sub(r,p))==c*c:continue
        i=axis(sub(r,p));assert i is not None
        out[i*c*c+(r[0]%c)*c+r[1]%c]+=1
        out[i*c*c+(p[0]%c)*c+p[1]%c]-=1
    return out,u,w

def boundary(a,b,c):
    A=b*(2*a+b);B=a*(a+2*b);poly=((0,0),(B,-A),(B,0));out=Counter()
    assert norm((B,-A))==c**4
    for p,q in zip(poly,poly[1:]+poly[:1]):
        i=axis(sub(q,p))
        if i is None:continue
        out[i*c*c+(q[0]%c)*c+q[1]%c]+=1
        out[i*c*c+(p[0]%c)*c+p[1]%c]-=1
    return out

def verify_dual(path):
    d=json.loads(path.read_text());a,b,c=d['tile'];D=d['denominator'];f=d['endpoint_weights'];t=d['charge_weight'];charge=a-b+c*d['native_charge_units'];assert charge==d['charge'] and D>0 and len(f)==3*c*c
    labels=[];scores=[];mates=[];singles=[]
    for x in range(c):
        for y in range(c):
            for j in range(6):
                for s in (-1,1):
                    row,u,w=endpoint_row((x,y),j,s,a,b,c)
                    labels.append((x,y,j,s));scores.append(sum(v*f[k]for k,v in row.items())+s*(-1)**j*t)
                    mates.append(((u[0]+w[0]-x)%c,(u[1]+w[1]-y)%c,(j+3)%6,s))
                    singles.append(s==-1 and (a*u[0]-b*u[1])%c==0)
    index={p:k for k,p in enumerate(labels)};singles_scores=[score for score,allow in zip(scores,singles)if allow];pairs=[]
    for k,mate in enumerate(mates):
        other=index[mate];assert mates[other]==labels[k] and other!=k
        if k<other:pairs.append(scores[k]+scores[other])
    assert len(singles_scores)==6*c and len(pairs)==6*c*c
    assert max(singles_scores)<=D and max(pairs)<=2*D
    bd=boundary(a,b,c);rhs=[[k,v]for k,v in sorted(bd.items())if v]+[[3*c*c,charge]]
    assert rhs==d['rhs_nonzero']
    numerator=sum(v*f[k]for k,v in bd.items())+charge*t;assert numerator==d['numerator']
    rp,rm=((8,19)if c==37 else(27,5))
    # Direct search of nonnegative core sign counts is exact after a proved
    # finite upper witness. It also checks the closed congruence rounding.
    candidates=[]
    for excess in range(100):
        p=rp+c*excess;q=p-charge
        if q>=rm and (q-rm)%c==0 and (p+q)*D>=numerator:candidates.append((p+q,p,q))
    assert candidates;population,p,q=min(candidates)
    expected={(37,-2):212,(37,-3):397,(37,-4):582,(43,-3):677}
    assert population==expected[c,d['native_charge_units']]
    period=2*c;assert population-period<0 or (population-period)*D<numerator
    return {'file':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'tile':[a,b,c],'core_charge':charge,'single_checks':len(singles_scores),'pair_checks':len(pairs),'boundary_current_matches':True,'integer_dual_numerator':numerator,'integer_dual_denominator':D,'rounded_population':population,'rounded_sign_counts':[p,q]}

def positive_143():
    path=ROOT/'research/2026-11-21/semiprimes/continued-rigidity/physical/CONTROL_143.json';d=json.loads(path.read_text());a,b,c=d['sides'];z=(F(a,c),F(b,c));rho=(0,1);conjz=(z[0]+z[1],-z[1]);B=a*(a+2*b);tiles=set()
    for (x,y,e),h,j,s in d['tiles']:
        if h!=0:continue
        q=(F(x,c**e),F(y,c**e));cq=(q[0]+q[1],-q[1]);v=mul(rho,cq);qn=(B-v[0],-v[1])
        assert all(t.denominator==1 for t in qn)
        tiles.add((int(qn[0]),int(qn[1]),(4-j)%6,-s))
    assert len(tiles)==38
    endpoint=Counter();gated=0;pairs=set();charge=0
    for x,y,j,s in tiles:
        row,u,w=endpoint_row((x,y),j,s,a,b,c);endpoint.update(row);charge+=s*(-1)**j
        accessible=s==-1 and (a*u[0]-b*u[1])%c==0
        if accessible:gated+=1
        else:
            mate=(u[0]+w[0]-x,u[1]+w[1]-y,(j+3)%6,s);assert mate in tiles
            pairs.add(tuple(sorted(((x,y,j,s),mate))))
    assert {k:v for k,v in endpoint.items()if v}=={k:v for k,v in boundary(a,b,c).items()if v}
    assert charge==2
    # Accessible pairs may have been counted as singles. The indicated groups
    # are nonetheless an exact allowed single/pair decomposition.
    assert gated+2*len(pairs)==38
    return {'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'N':143,'native_even_core_population':38,'core_charge':charge,'accessible_downward_singles':gated,'compulsory_other_pairs':len(pairs),'exact_exceptional_boundary_current':True}

def main():
    certificate_names=('CORE_3431_G_MINUS2.json','CORE_3431_G_MINUS3.json',
                       'CORE_3431_G_MINUS4.json','CORE_5063_G_MINUS3.json')
    out={'status':'PASS','scope':'Independent integer-column and boundary-source audit of conditional native exceptional-core bounds; no target exclusion.','certificates':[verify_dual(CORE/name)for name in certificate_names],'positive_control':positive_143()}
    assert len(out['certificates'])==4
    (HERE/'CORE_BUDGET_INDEPENDENT_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
