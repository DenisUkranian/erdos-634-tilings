"""Exclude simultaneous 16-owner contacts of a four-block branch and its child."""
from collections import Counter
from terminal import UNITS,add,det,scale,projected_events,width_obstruction


def outer_shell(word,rotation,hand,a,b,c):
    """Child union enlarged by the parent owners along its boundary."""
    rows=[Counter() for _ in range(3)]
    p=(0,0)
    for token in word:
        j=token%6
        steps=[(j,c)] if token<6 else [(j,a),((j+1)%6,b)]
        for axis,length in steps:
            axis=(rotation+hand*axis)%6
            rows[axis%3][det(UNITS[axis%3],p)]+=hand*(1 if axis<3 else -1)*length
            p=add(p,scale(length,UNITS[axis]))
    assert p==(0,0)
    return rows


def some_shift(left,right,allowed):
    # Between consecutive integral jumps the tested width is constant.
    # All disjoint-support shifts give the same set of width values.
    left={t:v for t,v in left.items() if v}
    right={t:v for t,v in right.items() if v}
    if not left or not right:
        shifts=[0]
    else:
        shifts=range(min(left)-max(right)-1,max(left)-min(right)+2)
    for offset in shifts:
        jumps=Counter(left)
        for t,v in right.items():
            jumps[t+offset]-=v
        width=0
        for t in sorted(jumps):
            width+=jumps[t]
            if width not in allowed:
                break
        else:
            assert width==0
            return True
    return False


def independent_shift(left,right,allowed,bound):
    # On all possible physical offsets, compare the values at every integer
    # level via explicit arrays, independently of the event merge.
    import numpy as np
    offsets=np.arange(-bound,bound+1)
    first=min([0,*left,*right])-bound-1
    last=max([0,*left,*right])+bound+1
    def widths(row):
        jumps=np.zeros(last-first+1,dtype=int)
        for t,v in row.items():
            jumps[t-first]=v
        return np.cumsum(jumps)
    fixed,moving=widths(left),widths(right)
    ok=np.ones(len(offsets),dtype=bool)
    # Include both nonzero supports. clamping outside the stored array gives zero.
    for i,v in enumerate(fixed):
        if not ok.any():
            return False
        diff=v-moving[np.clip(i-offsets,0,len(moving)-1)]
        # Membership table for the integer lengths.
        if i==0:
            low=min(0,int(fixed.min()-moving.max()))
            high=max(max(allowed),int(fixed.max()-moving.min()))
            table=np.array([k in allowed for k in range(low,high+1)])
        ok &= table[diff-low]
    return bool(ok.any())


def nested(shapes):
    a,b,c=33,7,37
    inner={w for k,w in shapes if k==1 and not width_obstruction(a,b,c,w)}
    outer={w for k,w in shapes if k==2}
    assert len(inner)==2 and len(outer)==24
    assert all(width_obstruction(a,b,c,w) for w in outer)
    total=moment_pass=width_pass=0
    for w in outer:
        rows=projected_events(a,b,c,w)[1]
        for v in inner:
            singles=sum(t<6 for t in w)+sum(t>=6 for t in v)
            assert singles%2==0
            pairs=(2*c-singles)//2
            allowed={a*i+b*j for i in range(pairs+1) for j in range(pairs-i+1)}
            for hand in (1,-1):
                for rotation in range(6):
                    shell=outer_shell(v,rotation,hand,a,b,c)
                    moments=[sum(t*m for t,m in right.items())-sum(t*m for t,m in left.items())
                             for left,right in zip(rows,shell)]
                    assert all(sum(row.values())==0 for row in rows+shell)
                    assert sum(moments)==2*a*b*pairs
                    total+=1
                    if any(j%(a*b) or not 0<=j<=a*b*pairs for j in moments):
                        continue
                    moment_pass+=1
                    passes=all(some_shift(left,right,allowed) for left,right in zip(rows,shell))
                    reviewed=all(independent_shift(left,right,allowed,16*(a+b))
                                 for left,right in zip(rows,shell))
                    assert not reviewed and not passes
                    if passes:
                        width_pass+=1
    assert (total,moment_pass,width_pass)==(576,32,0)
    return [total,moment_pass,width_pass]
