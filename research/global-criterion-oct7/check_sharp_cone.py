#!/usr/bin/env python3
"""Exact checks for the sharp initial nested-corner cone; no geometry inference."""
from __future__ import annotations
import argparse
from heapq import heappop, heappush
import json
from math import gcd
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def normalized(p, q):
    require(p > q > 0 and gcd(p, q) == 1, 'bad conic parameters')
    g = 3 if (p-q) % 3 == 0 else 1
    tile = ((p*p-q*q)//g, q*(2*p+q)//g, (p*p+p*q+q*q)//g)
    if g == 3:
        P, Q = (p+2*q)//3, (p-q)//3
    else:
        P, Q = p, q
    require(P > Q > 0 and gcd(P,Q) == 1 and (P-Q)%3, 'bad conversion')
    canonical = (P*P-Q*Q, Q*(2*P+Q), P*P+P*Q+Q*Q)
    require(sorted(tile) == sorted(canonical), 'normalization changed tile')
    require(canonical[2]**2 == canonical[0]**2+canonical[0]*canonical[1]+canonical[1]**2,
            'norm equation failed')
    return canonical, P, Q, g


def dijkstra_apery(a, b, c):
    """Independent shortest paths on residues modulo a, using positive b/c edges."""
    inf = (a+1)*(b+c+1)
    dist = [inf]*a
    dist[0] = 0
    queue = [(0,0)]
    while queue:
        val, r = heappop(queue)
        if val != dist[r]:
            continue
        for x in (b,c):
            n = (r+x)%a
            nv = val+x
            if nv < dist[n]:
                dist[n] = nv
                heappush(queue,(nv,n))
    require(max(dist) < inf, 'residue graph disconnected')
    return dist


def l_apery(p,q):
    a,b,c = p*p-q*q,q*(2*p+q),p*p+p*q+q*q
    out = [None]*a
    for j in range(p):
        for k in range(p):
            if j >= p-q and k >= p-q:
                continue
            val = j*b+k*c
            require(out[val%a] is None, 'duplicate L residue')
            out[val%a] = val
    require(all(x is not None for x in out), 'missing L residue')
    return out


def coin_witness(x,a,b,c):
    if x < 0:
        return None
    inv = pow(a,-1,b)
    for k in range(x//c+1):
        rest = x-k*c
        i = (rest*inv)%b
        if i*a <= rest:
            j = (rest-i*a)//b
            return (i,j,k)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', type=Path)
    args = ap.parse_args()
    normalization_count = factor_three_count = apery_count = 0
    for p in range(2,81):
        for q in range(1,p):
            if gcd(p,q) != 1:
                continue
            tile,P,Q,g = normalized(p,q)
            normalization_count += 1
            factor_three_count += (g == 3)
    for p in range(2,36):
        for q in range(1,p):
            if gcd(p,q) != 1 or (p-q)%3 == 0:
                continue
            a,b,c = p*p-q*q,q*(2*p+q),p*p+p*q+q*q
            predicted = l_apery(p,q)
            actual = dijkstra_apery(a,b,c)
            require(predicted == actual, f'wrong Apery set at {p,q}')
            require(max(actual)-a == (p-q-1)*b+(p-1)*c-a, 'wrong Frobenius')
            apery_count += 1
    seen = set()
    cone_count = new_count = 0
    new_examples = []
    for p in range(2,181):
        for q in range(1,p):
            if gcd(p,q) != 1:
                continue
            tile,P,Q,g = normalized(p,q)
            a0,b0,c = tile
            a,b = max(a0,b0),min(a0,b0)
            if (a,b,c) in seen or not (b<a and 32*a<45*b):
                continue
            seen.add((a,b,c))
            x=b*c-a*a
            witness=coin_witness(x,a,b,c)
            require(witness is not None, f'cone failed at {a,b,c}')
            require(sum(t*v for t,v in zip(witness,(a,b,c))) == x, 'bad witness')
            F=(P-Q-1)*b0+(P-1)*c-a0
            if b>=1444:
                require(x>F, 'large-size proof bound failed')
            if 5*a>7*b:
                require(b>1444, 'Farey gap failed')
                new_count += 1
                new_examples.append({'tile':[a,b,c], 'parameters':[P,Q],
                                     'remainder':x, 'Frobenius':F,
                                     'coin_witness':list(witness)})
            cone_count += 1
    endpoint=(45,32,67)
    require(67*67==45*45+45*32+32*32,'endpoint norm failed')
    require(coin_witness(119,*endpoint) is None,'endpoint was representable')
    require(119*38> (35*1024)//8, 'size constant failed')
    new_examples.sort(key=lambda z:z['tile'][1])
    report={'status':'PASS', 'arithmetic':'exact integer',
            'normalization_cases':normalization_count,
            'factor_three_conversions':factor_three_count,
            'independent_apery_comparisons':apery_count,
            'distinct_cone_tiles_checked':cone_count,
            'new_interval_tiles_checked':new_count,
            'new_interval_examples':new_examples[:6],
            'endpoint_tile':list(endpoint), 'endpoint_remainder':119,
            'endpoint_nested_criterion':False,
            'uniform_theorem':'1<A/B<45/32 implies all positive multipliers for reversed F4, F2, and both F3 orientations',
            'sharpness_scope':'initial ratio cone for the nested-corner unit criterion only',
            'full_Erdos634_solved':False,
            'arbitrary_endpoint_tiling_excluded':False}
    text=json.dumps(report,indent=2)+'\n'
    if args.report:
        args.report.write_text(text)
    print(text,end='')

if __name__=='__main__':
    main()
