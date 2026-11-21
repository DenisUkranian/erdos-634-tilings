#!/usr/bin/env python3
"""Construct signed full periodic witnesses from exact endpoint kernels.

This is a signed lattice-image calculation, not a positive packing search.
"""
from __future__ import annotations

import argparse
from collections import Counter
import gzip
import json
from pathlib import Path

from probe_integer_image import eliminate

HERE=Path(__file__).resolve().parent
U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))


def endpoint(columns,a,b,c):
    result=Counter()
    for x,y,j,s,m in columns:
        u=(x-a*U[j][0],y-a*U[j][1])
        w=(x+b*U[(j+s)%6][0],y+b*U[(j+s)%6][1])
        for axis,(xx,yy),v in ((j,(x,y),s),(j,u,-s),(j+s,w,s),(j+s,(x,y),-s)):
            result[axis%3,xx%c,yy%c]+=m*v
    return {k:v for k,v in result.items() if v}


def feature(columns,a,b,c):
    row=Counter()
    for x,y,j,s,m in columns:
        eps=s*(-1 if j%2 else 1)
        ux=x-a*U[j][0];uy=y-a*U[j][1]
        r=((a*uy-b*ux)%c if s>0 else c+(a*ux-b*uy)%c)
        row[r]+=eps*m
        row[2*c+(eps<0)]+=m
    return {k:v for k,v in row.items() if v}


def rotate(columns,k,c):
    out=[]
    for x,y,j,s,m in columns:
        for _ in range(k):x,y=-y,x+y
        out.append((x%c,y%c,(j+k)%6,s,m))
    return tuple(sorted(out))


def generators(a,b,c):
    d=a+b
    seeds=[[(0,0,j,s,1) for j in (0,2,4) for s in (-1,1)],
        [(0,0,0,1,1),(0,0,2,-1,1),(0,0,2,1,1),(-d,0,3,1,1),(-d,0,5,-1,1),(-d,0,5,1,1)],
        [(0,0,0,-1,1),(0,0,0,1,1),(0,0,2,-1,1),(d,-d,3,-1,1),(d,-d,3,1,1),(d,-d,5,-1,1)],
        [(0,0,0,-1,1),(0,0,0,1,1),(0,0,4,1,1),(0,d,1,1,1),(0,d,3,-1,1),(0,d,3,1,1)]]
    seeds=sorted({rotate(seed,k,c) for seed in seeds for k in range(6)})
    output=[];keys=[]
    for seed in seeds:
        assert not endpoint(seed,a,b,c)
        for x in range(c):
            for y in range(c):
                columns=tuple(((xx+x)%c,(yy+y)%c,j,s,m) for xx,yy,j,s,m in seed)
                output.append(columns);keys.append(['six',list(seed),x,y])
    fan=[(0,r,j,s,1) for r in range(c) for j,s in ((0,-1),(0,1),(4,1))]
    for k in range(6):
        columns=rotate(fan,k,c)
        assert not endpoint(columns,a,b,c)
        output.append(columns);keys.append(['fan',k])
    for j in range(6):
        for s in (-1,1):
            columns=tuple((x,y,j,s,1) for x in range(c) for y in range(c))
            assert not endpoint(columns,a,b,c)
            output.append(columns);keys.append(['uniform',j,s])
    return output,keys


def run(target):
    a,b,c=(33,7,37) if target==3431 else (35,13,43)
    P,N=(74,37) if c==37 else (129,86)
    up,down=2*c-2*(a-b),-c+2*(a-b)
    kernels,keys=generators(a,b,c)
    rows=[{} for _ in range(2*c+2)]
    for k,kernel in enumerate(kernels):
        for r,v in feature(kernel,a,b,c).items():rows[r][k]=v
    rhs=[0]*len(rows);rhs[0]=up;rhs[c]=down;rhs[-2:]=[P,N]
    answer=eliminate(rows,rhs,len(kernels),small_witness=True)
    answer.update(tile=[a,b,c],target=target,profile=[up,down],positive=P,negative=N,
        generators=len(kernels),scope='Signed integer full periodic endpoint/gate image. Negative multiplicities are allowed; no positive integer kernel, physical packing, or tiling is asserted.')
    if 'signed_integer_witness' in answer:
        current=Counter();used=[]
        for k,m in answer.pop('signed_integer_witness'):
            used.append([m,keys[k]])
            for x,y,j,s,v in kernels[k]:current[x,y,j,s]+=m*v
        columns=sorted((*key,m) for key,m in current.items() if m)
        assert not endpoint(columns,a,b,c)
        assert feature(columns,a,b,c)=={r:v for r,v in enumerate(rhs) if v}
        answer.update(signed_tile_columns=columns,generator_combination=used,
            nonzero_tile_columns=len(columns),negative_tile_columns=sum(col[-1]<0 for col in columns),
            maximum_absolute_tile_multiplicity=max(abs(col[-1]) for col in columns),
            full_endpoint_rows_verified=3*c*c,gate_rows_verified=2*c)
    return answer


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target',type=int,choices=(3431,5063),required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();answer=run(args.target)
    data=(json.dumps(answer,indent=2)+'\n').encode()
    if str(args.out).endswith('.gz'):
        with gzip.GzipFile(filename=str(args.out),mode='wb',mtime=0) as stream:stream.write(data)
    else:args.out.write_bytes(data)
    print(json.dumps({k:v for k,v in answer.items() if k not in ('remaining','signed_tile_columns','generator_combination')},indent=2))

if __name__=='__main__':main()
