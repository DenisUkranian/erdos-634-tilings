"""Test whole pairs and individual owners, allowing all translates and both hands."""
from itertools import combinations, product
import gzip
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]/'axial-reserve'))
from reserve import UNITS, add, scale, subtract

a,b,c = 35,13,43
plus,minus = -a*pow(b,-1,c)%c, -b*pow(a,-1,c)%c


def tile(t,j,h,full):
    q = divmod(t,c) if full else (t,0)
    u = subtract(q,scale(a,UNITS[j]))
    w = add(q,scale(b,UNITS[(j+h)%6]))
    def residue(p):
        x,y = p
        return (x%c)*c+y%c if full else (x+plus*y)%c
    size = c*c if full else c
    rows = [(j%3*size+residue(q),h),(j%3*size+residue(u),-h),
            ((j+h)%3*size+residue(w),h),((j+h)%3*size+residue(q),-h)]
    g = (u[0]+(plus if h==1 else minus)*u[1])%c
    mate = residue(subtract(add(u,w),q)), (j+3)%6, h
    return rows,g,mate


def degree_bound(label,weights):
    full = label==-1
    size = c*c if full else c
    assert len(weights)==3*size+2
    scores = {}
    D = 1
    for t,j,h in product(range(size),range(6),(-1,1)):
        rows,g,mate = tile(t,j,h,full)
        first = h==1 and g==0
        other = (h==-1 and g==0) if full else (h==1 and g==label)
        value = sum(weights[i]*n for i,n in rows)
        if first or other:
            value += h*(-1)**j * weights[3*size+int(other)]
            D = max(D,value)
        scores[t,j,h] = value,mate
    for value,mate in scores.values():
        D = max(D,(value+scores[mate][0]+1)//2)
    target = c*weights[3*size]
    assert target>5*c*D
    return [target,D]


def outside_bound(weights,vector,same_hand_only=False):
    positioned = vector is not None
    assert len(weights)==4*c+2+2*positioned
    scores = {}
    for t,j,h in product(range(c),range(6),(-1,1)):
        rows,g,mate = tile(t,j,h,False)
        label = g if h==1 else c
        val = sum(weights[i]*n for i,n in rows) + weights[3*c+label]*h*(-1)**j + weights[-1]
        if positioned and label==0:
            val += sum(x*y for x,y in zip(weights[-3:-1],UNITS[j]))
        counts = 0 < label < c if same_hand_only else label != 0
        assert val <= 100000*int(counts)
        scores[t,j,h] = val,mate
    assert all(val+scores[mate][0]<=0 for val,mate in scores.values())
    target = c*weights[3*c]+5*c*weights[-1]
    if positioned:
        target += sum(x*y for x,y in zip(vector,weights[-3:-1]))
    return target



def same_hand_degree():
    """Cover all pairs of secondary labels, allowing every opposite-hand single."""
    tables = json.loads(gzip.decompress((HERE/'same_hand.json.gz').read_bytes()))
    pairs = set(combinations(range(1,c),2))
    rotations = (1,(plus-1)%c,(plus-1)**2%c)
    for weights in tables:
        assert len(weights)==4*c+1 and all(type(x) is int for x in weights)
        scores = {}
        maxima = [None]*(c+1)
        for t,j,h in product(range(c),range(6),(-1,1)):
            rows,g,mate = tile(t,j,h,False)
            label = g if h==1 else c
            val = sum(weights[i]*n for i,n in rows)+weights[3*c+label]*h*(-1)**j
            scores[t,j,h] = val,mate
            if maxima[label] is None or val>maxima[label]:
                maxima[label] = val
        threshold = (c*weights[3*c]-1)//(5*c)
        assert max(maxima[0],maxima[c])<=threshold
        assert all(val+scores[mate][0]<=2*threshold for val,mate in scores.values())
        covered = [k for k in range(1,c) if maxima[k]<=threshold]
        for m in rotations:
            labels = sorted(m*k%c for k in covered)
            pairs.difference_update(combinations(labels,2))
    assert not pairs
    return len(tables)


def check():
    records = json.loads(gzip.decompress((HERE/'degree_duals.json.gz').read_bytes()))
    results = {int(k):degree_bound(int(k),v) for k,v in records.items()}
    orbit = lambda k: min(k, k*(plus-1)%c, k*(plus-1)**2%c)
    assert set(results)=={-1}|{orbit(i) for i in range(1,c)}
    plain = outside_bound(json.loads((HERE/'outside.json').read_text()),None)
    fixed = outside_bound(json.loads((HERE/'outside_positioned.json').read_text()),(27,-10))
    assert plain>19*100000 and fixed>40*100000
    same = outside_bound(json.loads((HERE/'outside_same.json').read_text()),None,True)
    fixed_same = outside_bound(json.loads((HERE/'outside_same_positioned.json').read_text()),(27,-10),True)
    assert same>17*100000 and fixed_same>30*100000
    return dict(two_gate_lower_bounds=results, same_hand_cover_tables=same_hand_degree(),
                outside_numerators=[plain,fixed],same_hand_outside_numerators=[same,fixed_same],
                outside_denominator=100000)


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Assertions must be enabled.')
    print(json.dumps(check(),indent=2))
