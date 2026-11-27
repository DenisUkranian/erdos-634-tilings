"""Verify integer displacement exclusions at a two-block ordinary lift."""
from itertools import product
import gzip
import json
from pathlib import Path
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]/'axial-reserve'))
from reserve import UNITS, gate_column


def inventories(a,b,c,charge,limit):
    """Net unit headings on a negative-hand bank; displacement fits the other mesh."""
    result = {}
    for x,y in product(range(-limit,limit+1),repeat=2):
        t, rem = divmod(y-x-charge,3)
        if rem:
            continue
        cost = abs(x+t)+abs(y-t)+abs(t)
        X, rx = divmod((a+b)*x+b*y,c)
        Y, ry = divmod(-b*x+a*y,c)
        if not rx and not ry and cost<=limit and max(abs(x),abs(y),abs(x+y))<=c:
            result[x,y] = cost
            assert (a*X-b*Y,b*X+(a+b)*Y) == (c*x,c*y)
    return result


def projected_columns(a,b,c,labels):
    w = -b * pow(a,-1,c) % c
    cols = []
    for r,j,h in product(range(c),range(6),(-1,1)):
        v = [0]*(4*c+1+2*len(labels))
        records = gate_column(a,b,c,r,j,h,w)
        for i,n in records:
            v[i] += n
        g = records[-1][0]-3*c
        if g in labels:
            pos = 4*c+1+2*labels.index(g)
            v[pos:pos+2] = UNITS[j]
        cols.append(v)
    return np.array(cols,dtype=np.int64)


def retain(a,b,c,labels,targets,tables):
    columns = projected_columns(a,b,c,labels)
    start = 4*c+1
    for record in tables:
        y = np.array(record,dtype=np.int64)
        assert y.shape==(columns.shape[1],) and max(abs(y))<10**8
        D = max(1,int(max(columns@y)))
        offset = (a-b)*(int(y[3*c])-int(y[3*c+labels[1]]))
        targets = [t for t in targets if offset+sum(v*int(z) for v,z in zip(t,y[start:],strict=True))<=2*c*D]
    return targets


def verify_histogram():
    c = 43
    labels = list(range(c))
    columns = projected_columns(35,13,c,labels)
    data = json.loads((HERE/'projected_histogram.json').read_text())
    total = np.zeros(columns.shape[1],dtype=np.int64)
    assert sum(n for r,j,h,n in data)==86
    for r,j,h,n in data:
        assert 0<=r<c and 0<=j<6 and h in (-1,1) and 0<n<=86
        total += n*columns[(6*r+j)*2+(h==1)]
    required = np.zeros_like(total)
    required[3*c], required[3*c+8] = 22,-22
    start = 4*c+1
    required[start:start+2] = -25,3
    required[start+16:start+18] = 25,-3
    assert np.array_equal(total,required)
    return len(data)


def check():
    records = json.loads(gzip.decompress((HERE/'transfer_duals.json.gz').read_bytes()))
    output = {}
    for a,b,c,k in ((33,7,37,4),(35,13,43,8)):
        d = a-b
        P,N = (inventories(a,b,c,t,2*c) for t in (d,-d))
        targets = [p+n for p,h in P.items() for n,l in N.items() if h+l<=2*c]
        initial = len(targets)
        candidates = retain(a,b,c,[0,k],targets,records['first'][str(c)])
        assert candidates == ([] if c==37 else [(-25,3,17,10),(-25,3,25,-3),(-17,-10,25,-3),(-12,-2,12,2)])
        excluded = []
        if c==43:
            for i,(labels,tables) in records['second'].items():
                v = candidates[int(i)]
                remaining = 2*c-P[v[:2]]-N[v[2:]]
                bank = inventories(a,b,c,0,remaining)
                family = [v+p+n for p,h in bank.items() for n,l in bank.items() if h+l<=remaining]
                assert family and not retain(a,b,c,[0,k,*labels],family,tables)
                excluded.append(v)
        output[c] = dict(initial_pairs=initial,after_first_tests=candidates,
                         remaining=[v for v in candidates if v not in excluded])
    output[43]["nonempty_bins_in_projected_witness"] = verify_histogram()
    return output


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Assertions must be enabled.')
    print(json.dumps(check(),indent=2))
