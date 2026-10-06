#!/usr/bin/env python3
"""Exact prime allocation for even nonsaturated kernels and odd multipliers.

YES uses an existing every-integer construction. NO means all classified
coefficient rows are absent. UNKNOWN retains geometric small-scale cases.
This is a per-input tool, NOT an implementation of the S-unit support solver.
"""
from __future__ import annotations
import argparse
import importlib.util
import json
from math import gcd
from pathlib import Path

_path = Path(__file__).resolve().parents[1] / 'square-class-tails' / 'classify.py'
_spec = importlib.util.spec_from_file_location('square_class_tails', _path)
tails = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tails)


def factored_divisors(fs):
    """Return (divisor, its factorization), without refactoring large products."""
    out = [(1, {})]
    for p, e in sorted(fs.items()):
        out = [(n*p**r, g | ({p:r} if r else {}))
               for n, g in out for r in range(e+1)]
    return sorted(out)


def coprime_pairs(fs):
    """Assign each whole prime power to exactly one of two ordered factors."""
    out = [(1, 1)]
    for p, e in sorted(fs.items()):
        if e:
            z = p**e
            out = [(a*z,b) for a,b in out] + [(a,b*z) for a,b in out]
    return out


def allocated_witnesses(D, fs):
    """All nine primitive product rows; fs is the exact factorization of D."""
    product = 1
    for p,e in fs.items():
        product *= p**e
    if product != D:
        raise ValueError('inconsistent coefficient factorization')
    hits = {}

    def group(branch, u2, v2, x, y):
        u, v = tails.root(u2), tails.root(v2)
        if u is not None and v is not None and 0<u<v and gcd(u,v)==1:
            hits[(branch,u,v)] = dict(branch=branch,u=u,v=v,coefficient=D,
                                     allocation=[x,y])

    def norm(branch, a, b, x, y, sign=1):
        if a<=0 or b<=0 or gcd(a,b)!=1:
            return
        c = tails.root(a*a+sign*a*b+b*b)
        if c is not None:
            hits[(branch,a,b,c)] = dict(branch=branch,a=a,b=b,c=c,
                                       coefficient=D,allocation=[x,y])

    for x,y in coprime_pairs(fs):
        group('alpha',y-2*x,y-x,x,y)
        group('QP',2*y-3*x,y-x,x,y)
        norm('E60',x,y,x,y,-1)
        norm('E120',x,y,x,y)
        norm('F1',y-x,x,x,y)
        norm('I120',y-2*x,x,x,y)
        if (2*y-x)%3==0 and (2*x-y)%3==0:
            norm('F2',(2*y-x)//3,(2*x-y)//3,x,y)
        norm('F4',y-x,2*x-y,x,y)
    if fs.get(3,0):
        reduced = dict(fs)
        reduced[3] -= 1
        for x,y in coprime_pairs(reduced):
            norm('F3',2*x-y,y-x,x,y)
    return [hits[k] for k in sorted(hits)]


def classify(d, m):
    fsd = tails.validate_kernel(d)
    if d%2 or m<1 or m%2==0:
        raise ValueError('requires an even squarefree d and a positive odd m')
    if tails.tail(d)['status'] != 'NOT_COFINITE':
        raise ValueError('this tool requires a kernel failing the cofinal tail test')
    witnesses = []
    for s, fss in factored_divisors(tails.factor(m)):
        fsD = {p:fsd.get(p,0)+2*fss.get(p,0) for p in fsd.keys()|fss.keys()}
        D, t = d*s*s, m//s
        for w in allocated_witnesses(D,fsD):
            T = tails.threshold(w)
            witnesses.append(dict(w,s=s,t=t,sufficient_multiplier=T,
                                  construction_certified_by_tail=t>=T))
    positive = [w for w in witnesses if w['construction_certified_by_tail']]
    status = 'YES' if positive else 'UNKNOWN' if witnesses else 'NO'
    return dict(d=d,m=m,N=d*m*m,status=status,
                scope='even nonsaturated d, odd m; all nine surviving product rows',
                witnesses=witnesses,positive_witness=positive[0] if positive else None,
                unknown_means='some coefficient witnesses are below sufficient construction bounds',
                fixed_support_S_unit_solver_executed=False,full_Erdos634_solved=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('d',type=int)
    parser.add_argument('m',type=int)
    args = parser.parse_args()
    try:
        result = classify(args.d,args.m)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
