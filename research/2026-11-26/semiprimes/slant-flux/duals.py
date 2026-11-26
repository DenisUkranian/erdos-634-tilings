"""Verify integer potentials on every residue, orientation and hand."""
from functools import lru_cache
from itertools import product
from pathlib import Path
import gzip
import json
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent/'axial-reserve'))
from reserve import UNITS, add, multiply, scale, subtract, gate
import numpy as np


@lru_cache(None)
def columns(a, b, c, form):
    """Full torus if form is absent, otherwise the quotient x + form*y."""
    size = c*c if form is None else c
    def residue(p):
        x,y = p
        return x%c*c+y%c if form is None else (x+form*y)%c
    rows, signs, orientations, minus, plus = [], [], [], [], []
    for t, j, h in product(range(size), range(6), (-1,1)):
        q = divmod(t,c) if form is None else (t,0)
        u = subtract(q,scale(a,UNITS[j]))
        v = add(q,scale(b,UNITS[(j+h)%6]))
        rows.append((j%3*size+residue(q), j%3*size+residue(u),
                     (j+h)%3*size+residue(v), (j+h)%3*size+residue(q)))
        signs.append(h*(-1)**j)
        orientations.append((j,h))
        minus.append((a*u[0]-b*u[1])%c)
        plus.append((a*u[1]-b*u[0])%c)
    return (np.array(rows).T, np.array(signs), np.array(orientations).T,
            np.array(minus), np.array(plus))


def scores(potential, a, b, c, form=None):
    y = np.array(potential, dtype=np.int64)
    assert len(y) == len(potential) and max(abs(y)) < 10**9
    rows, sign, (j,h), down, up = columns(a,b,c,form)
    i,k,l,m = rows
    short = h*(y[i]-y[k]+y[l]-y[m])
    return y,short,sign,j,h,down,up


def full_ordinary(mode, y):
    a,b,c = 35,13,43
    y, short, sign, j, hand, down, up = scores(y,a,b,c)
    # The stored positive-hand form is the real coordinate of (a+b*bar(rho))*u.
    # It is - (a+b)/b times (a*u_y-b*u_x) modulo c.
    plus_label = (-(a+b)*pow(b,-1,c)*up)%c
    label = np.where(hand == 1,c+plus_label,down)
    value = short + sign*y[3*c*c+label]
    assert len(y) == 3*c*c+2*c
    if mode == 'N':
        target = int(2*c*y[-2*c]-c*y[-c])
        den = int(max(value))
        assert den > 0 and target > 9*c*den
        return [target, den]
    is_middle = mode == 'B'
    vectors = [scale(c,U) if is_middle else multiply((a,b),U) for U in UNITS]
    heading_score = np.array([2*x+v for x,v in vectors])
    reward = np.where(label == (0 if is_middle else c),heading_score[j],0)
    # Every tile contributes at most D to potential + 100000 * reward.
    D = max(0,int(max(value+100000*reward)))
    count = c*(6 if is_middle else 2)
    target = int(c*(y[-c]-y[-2*c])) if is_middle else 0
    return [count*D-target,100000]


def core_source(y, a, b, c, form):
    A,H = b*(2*a+b),a*(a+2*b)
    size = c*c if form is None else c
    x_end = A%c*c if form is None else A%c
    y_end = H%c if form is None else form*H%c
    return int(y[x_end]-y[0]+y[size]-y[size+y_end])


def projected_core(a,b,c,n,Q,V,tables):
    """Native standard current Q with at most one further current V."""
    forms = {-1: -b*pow(a,-1,c)%c, 1: -a*pow(b,-1,c)%c}
    native = -a*a*(a+2*b)*pow(b,-1,c)%c
    checked = []
    for hand in (-1,1):
        w = forms[hand]
        for rec in tables[str(hand)]:
            y, short, sign, j, h, down, up = scores(rec['table'],a,b,c,w)
            label = down*pow(a,-1,c)%c if hand == -1 else (-up*pow(b,-1,c))%c
            value = short+sign*y[3*c+np.where(h==hand,label,c)]
            assert len(y)==4*c+1 and 0<int(max(value))<=rec['den']
            fixed = core_source(y,a,b,c,w) + int(Q*y[3*c+(native if hand==1 else c)])
            checked.append((hand,n*rec['den']-fixed,y[3*c:]))
    allowed = []
    for h,label in (product((-1,1),range(c)) if V else [(0,0)]):
        if h==1 and label==native:
            continue
        if all(V*int(y[label if hand==h else c])<=slack for hand,slack,y in checked):
            allowed.append((h,label))
    return allowed


def both_walls(extra, potential):
    a,b,c=33,7,37
    y,short,sign,j,h,down,up=scores(potential,a,b,c)
    label=np.where(h==1,(-up*pow(b,-1,c))%c,c+down)
    H=a*(a+2*b)
    native=-a*H*pow(b,-1,c)%c
    target=core_source(y,a,b,c,None)+37*int(y[3*c*c+native])-26*int(y[3*c*c+extra])
    cost=short+sign*y[3*c*c+label]
    D=int(max(cost))
    endpoint_target=target
    offset=3*c*c+2*c
    for k,origin,length in ((0,(0,0),b*(2*a+b)),(4,(0,H),H)):
        target+=int(y[offset+length]-y[offset])
        for i in range(length):
            p=add(origin,scale(i,UNITS[k]))
            for step in (a,b,c):
                if i+step>length:
                    continue
                increment=int(y[offset+i+step]-y[offset+i])
                if step==c:
                    assert increment<=0
                    continue
                end=add(p,scale(step,UNITS[k]))
                for hand in (-1,1):
                    if step==a:
                        q,heading=(end,k) if hand==1 else (p,k+3)
                    else:
                        q,heading=(p,k-1) if hand==1 else (end,k+4)
                    col=((q[0]%c*c+q[1]%c)*6+heading%6)*2+int(hand==1)
                    D=max(D,int(cost[col])+increment)
        offset+=length+1
    assert offset==len(y) and D>0 and target>101*D
    # Independently eliminate all wall-state multipliers. Pay each owner's
    # deficit D - cost and minimize it over complete boundary words.
    for k,origin,length in ((0,(0,0),b*(2*a+b)),(4,(0,H),H)):
        distance=[None]*(length+1)
        distance[0]=0
        for t in range(1,length+1):
            options=[]
            for step in (a,b,c):
                i=t-step
                if i<0 or distance[i] is None:
                    continue
                if step==c:
                    options.append(distance[i])
                    continue
                p=add(origin,scale(i,UNITS[k]))
                end=add(origin,scale(t,UNITS[k]))
                owners=((end,k,1),(p,k+3,-1)) if step==a else ((p,k-1,1),(end,k+4,-1))
                for q,j,s in owners:
                    index=((q[0]%c*c+q[1]%c)*6+j%6)*2+int(s==1)
                    options.append(distance[i]+D-int(cost[index]))
            if options:
                distance[t]=min(options)
        endpoint_target+=distance[-1]
    assert endpoint_target>=target>101*D
    return [target,D,endpoint_target]


def load_tables():
    return json.loads(gzip.decompress((HERE/'potentials.json.gz').read_bytes()))
