"""Physical unmatched-owner floors when the odd population attains its minimum."""
from functools import lru_cache
from pathlib import Path
import json
import numpy as np
from charged_cut import direction_options,signed_axes


def profile_filter():
    cuts=next((Path(__file__).resolve().parents[4]/"research/2026-11-21/semiprimes/gate-model").glob("final_cuts_5063.dat"))
    lines=cuts.read_text().splitlines()[1:]
    D=np.array(lines[::3],dtype=np.int64)
    weights=np.array([[list(map(int,u.split())),list(map(int,v.split()))]
                      for u,v in zip(lines[1::3],lines[2::3])],dtype=np.int64)
    assert weights.shape==(780,2,43) and max(abs(weights).flat)<10**10
    def fits(up,down,S):
        for hand in (0,1):
            for index in (range(1,43) if S else (0,)):
                lhs=np.zeros(len(D),dtype=np.int64)
                for side,charge in enumerate((up,down)):
                    value=charge*weights[:,side]
                    if side==hand and S:
                        value=value-22*S*np.roll(weights[:,side],-index,axis=1)
                    lhs+=value.max(axis=1)
                if np.all(lhs<=215*D):
                    return True
        return False
    return fits


def bounds(a,b,c,k):
    d=a-b
    pos,neg=c*(k-1)//2,c*(k+1)//2
    alpha,beta=(43,222) if c==37 else (8,43)
    plus=(alpha*pos+(beta-alpha)*neg)//beta
    minus=(alpha*neg+(beta-alpha)*pos)//beta
    fit=profile_filter() if c==43 else None
    cap=8*c
    vectors={i:direction_options(a,b,c,i,cap) for i in (1,2)}
    @lru_cache(None)
    def bank(i,p,q):
        lower=cap+1
        for u,v,x,y in vectors[i]:
            left,right=signed_axes(u,v,-p),signed_axes(x,y,q)
            if left is not None and right is not None:
                lower=min(lower,sum(map(abs,left+right)))
        return lower
    out={}
    for s in range(-3*c,3*c+1):
        p=-2*c+d*s
        if not -minus<=p<=plus:continue
        for t in range(-3*c,3*c+1):
            q=c+d*t
            if not -minus<=q<=plus:continue
            S=-s-t
            for R in range(abs(S),k*c//d+1,2):
                if max(0,p)+max(0,q)+d*((R+S)//2)>pos:continue
                if max(0,-p)+max(0,-q)+d*((R-S)//2)>neg:continue
                if fit and R<=1 and not fit(-p,-q,S):continue
                M=bank(1,p,-d+c*s)+bank(2,c*t,q)+(c+d)*R
                if R==0 and (c==37 or s!=3):
                    M+=16
                out[R]=min(out.get(R,M),M)
    return dict(sorted(out.items()))


if __name__=="__main__":
    result={"3431":bounds(33,7,37,3),"5063":bounds(35,13,43,5)}
    assert result["3431"]=={0:175,1:181,2:233,3:307}
    assert result["5063"][0]==217 and result["5063"][1]==235
    print(json.dumps(result,indent=2))
