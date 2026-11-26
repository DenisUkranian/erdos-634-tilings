"""Replay the two target bounds, exact slant inequality and the coordinate controls."""
from collections import Counter
from functools import lru_cache
from itertools import combinations, product
import hashlib
import json
import numpy as np
from duals import HERE, both_walls, full_ordinary, gate, load_tables, projected_core
from hull import profiles
from check_coordinates import control


def middle43():
    base=HERE.parents[2]/'2026-11-21/semiprimes/gate-model/final_cuts_5063.dat'
    raw=base.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == '344a6da476a7551fddf9ad0bd2c97ef85f5ceed170eee5bb43704e24dc73cfbd'
    lines=raw.decode().splitlines()[1:]
    D=np.array(lines[::3],dtype=np.int64)
    W=np.array([[list(map(int,u.split())),list(map(int,v.split()))]
                for u,v in zip(lines[1::3],lines[2::3])],dtype=np.int64)
    assert W.shape==(780,2,43) and max(abs(W).flat)<10**10
    @lru_cache(None)
    def fits(n, q):
        a,b,*rest=q
        rest=[x for x in rest if x]
        # The smaller-budget case has one star with two identical extra currents.
        # Larger stars with distinct extras can safely pass to the independent core test.
        if len(rest)>1 and rest!=[22,22]:
            return True
        labels=[(h,r) for h in range(2) for r in range(1,43)]
        for placement in combinations(labels,len(rest)):
            for k in (12,120,780):
                lhs=0
                for h,charge in enumerate((a,b)):
                    weights=W[:k,h]
                    score=charge*weights
                    for amount,(owner,r) in zip(rest,placement):
                        if h==owner:
                            score+=amount*np.roll(weights,-r,axis=1)
                    lhs+=score.max(axis=1)
                if np.any(lhs>n*43*D[:k]):
                    break
            else:
                return True
        return False
    return fits


def middle37(tables):
    for table in tables:
        gate(33,7,37,table)
    W=np.array([row['table'][3*37:] for row in tables],dtype=np.int64)
    D=np.array([row['den'] for row in tables],dtype=np.int64)
    @lru_cache(None)
    def fits(n,q):
        u,v,*other=q
        extra=[x for x in other if x]
        if len(extra)>1:
            return True
        for h,r in (product(range(2),range(1,37)) if extra else [(0,0)]):
            for hand in range(2):
                own,opposite=(u,v) if hand==0 else (v,u)
                value=own*W[:,:37]
                if extra and h==hand:
                    value+=extra[0]*np.roll(W[:,:37],-r,axis=1)
                elif extra:
                    opposite+=extra[0]
                if np.any(value.max(axis=1)+opposite*W[:,37]>n*37*D):
                    break
            else:
                return True
        return False
    return fits


def replay():
    tables=load_tables()
    native=full_ordinary('N',tables['N'])
    bank=[full_ordinary(k,tables[k]) for k in ('B','T')]
    assert sum(x for x,_ in bank)<2*43**2*100000
    fit=middle43()
    small=profiles(43,22,7)
    survivors=[(p[0],p[1]) for _,_,p in small if fit(*p[0])]
    assert sorted(survivors)==[((6,(43,-43)),(2,())),((9,(86,-43)),(2,()))]
    large=profiles(43,22,8)
    edge43=[b for g,b,p in large if g==-1 and fit(*p[0])]
    assert set(edge43)=={(-43,(22,)),(-21,()),(0,(-21,))}
    fit=middle37(tables['middle37'])
    edge37=[]
    census={}
    for K,allowed in ((6,None),(7,0)):
        cases=profiles(37,26,K)
        chosen=[(g,b,p) for g,b,p in cases if allowed is None or g==allowed]
        remaining=[(g,b) for g,b,p in chosen if fit(*p[0])]
        if K==6:
            assert all(g==-1 for g,b,p in chosen)
        edge37.extend((101 if K==6 else 64,b) for g,b in remaining)
        census[str(K)]=[len(chosen),len(remaining)]
    assert set(edge37)=={(101,(-37,(26,))),(64,(0,(26,))),(64,(26,()))}
    core37=[]
    configs={(43,75,b) for b in edge43}|{(37,n,b) for n,b in edge37}
    for c,n,(native_gate,remote) in sorted(configs):
        a,b=(33,7) if c==37 else (35,13)
        Q=-native_gate
        V=-sum(remote)
        assert len(remote)<=1
        labels=projected_core(a,b,c,n,Q,V,tables[f'core{c}_{Q}_{V}'])
        if (c,n)==(37,101):
            assert labels==[(1,0),(1,26),(1,27)]
            core37=[both_walls(r,tables[f'wall{r}']) for _,r in labels]
        else:
            assert not labels
    assert (3431-2*37*42,5063-2*43*54)==(323,419)
    return dict(original_3431='OPEN', original_5063='OPEN', maximum_occupied_ordinary_lifts=[41,53],
                minimum_ordinary_excess_5063=8, middle_only_charge_population_5063=473,
                native_lower_bound=native, slant_bank_upper_bounds=bank,
                required_slant_projection=2*43**2, relaxed_stars_5063_K_le_7=len(small),
                after_middle_cuts_5063_K_le_7=survivors,
                census_3431_before_and_after_middle_cuts=census,
                wall_bounds_3431_at_101=core37,
                complete_143_controls={k:control(k) for k in ('known','macro')})


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Enable Python assertions.')
    print(json.dumps(replay(),indent=2))
