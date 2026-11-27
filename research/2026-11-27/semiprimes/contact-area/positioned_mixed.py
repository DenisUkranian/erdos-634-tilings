"""Positioned physical cuts at the first global mixed endpoints on both boards."""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import subprocess
import sys

from four_gates import solve
from mixed_control import run as full_control
from saturation import triples
from two_current import run as verify_duals

SOURCE=Path(__file__).resolve().parents[3]/'2026-11-26/semiprimes/charged-contour'
sys.path.insert(0,str(SOURCE))
from geometry import HEADINGS, chart, conjugate, exact_divide, layout, multiply, subtract
from grammar import boolean, program, restrict_edges, shifted_program
from area import encode, evaluate, select


@lru_cache(maxsize=128)
def instructions(profile,q,a,c,s,directions,shifts,exception):
    # A long side in the parent short mesh rotates by s headings modulo a.
    axes=tuple((j+(s if i>=3 and q==a else 0))%3 for i,j in enumerate(HEADINGS))
    if exception is not None:
        axes+=(axes[exception],)
    for axis in range(3):
        if sum(n*d[int(axis!=0)] for n,d,k in zip(profile,directions,axes) if k==axis)%q:
            return None
    rules,displacements=program(profile,q,c,s,directions,axes)
    offsets=shifted_program(rules,shifts)
    return rules,offsets,encode(rules,displacements,offsets,q,c,len(profile))


@lru_cache(maxsize=32)
def profiles(dirs,bank,exception):
    def displacement(v,moves):
        return tuple(sum(n*d[k] for n,d in zip(v,moves)) for k in (0,1))
    extra=int(exception is not None)
    first=extra and exception<3
    low={displacement(v,dirs[:3]):v for v in triples(bank+first)}
    assert len(low)==(bank+first+1)*(bank+first+2)//2
    target=dirs[exception] if extra else (0,0)
    result=[]
    for high in triples(bank+extra-first):
        required=subtract(target,displacement(high,dirs[3:6]))
        if required in low:
            result.append(low[required]+high+((1,) if extra else ()))
    return result


def forced_sites(params,case,dirs,shifts,edges):
    a,b,c,l=params
    if case[0]:
        return []
    _,pi,xmin,ymin,stride,_=layout(*params,*case)
    start=(231,120) if c==37 else (455,240)
    wall=[]
    for k in range(l+1):
        point=(start[0]-c*k,start[1]+c*k)
        x,y=exact_divide(multiply(conjugate(pi),subtract(point,(case[2],0))),c)
        wall.append((y-ymin)*stride+x-xmin)
    for direction,shift,i in zip(dirs,shifts,range(len(edges))):
        if direction==(-c,c):
            continue
        for site in wall[:-1]:
            edges[i]&=~(1<<site)
        for site in wall[1:]:
            if site>=shift:
                edges[i]&=~(1<<(site-shift))
    return wall


def check(binary,params,case):
    a,b,c,l=params
    _,s,_=case
    counts=Counter()
    for exception in (range(6) if c==37 else [None]):
        dirs,shifts,edges,domain=chart(*params,*case,reverse_parent=True,exceptional=exception)
        wall=forced_sites(params,case,dirs,shifts,edges)
        for profile in profiles(dirs,c-a+b,exception):
            orders=(a,b) if c==37 else (a,)
            recipes=[(q,instructions(profile,q,a,c,s,dirs,shifts,exception)) for q in orders]
            if any(r is None for _,r in recipes):
                counts['abelian']+=1
                continue
            live=domain
            while live:
                before=live
                for q,(rules,offsets,code) in recipes:
                    good=boolean(rules,offsets,restrict_edges(edges,shifts,live),live)
                    if good==live:
                        sites,scores=evaluate(binary,code,rules,shifts,edges,live)
                        floor_blocks=10 if c==37 else 12
                        good=select(sites,scores>=floor_blocks*(a*b//q))
                    live=good
                    if any(not ((live>>site)&1) for site in wall):
                        live=0
                    if not live or live!=before:
                        break
                if live==before:
                    break
            counts['retained' if live else 'empty']+=1
    return counts


def main():
    data={'duals':verify_duals(),'control143':{w:full_control(w) for w in ('known','macro')}}
    with TemporaryDirectory() as temp:
        binary=Path(temp)/'area'
        subprocess.run(['c++','-std=c++17','-O3',SOURCE/'area.cpp','-o',binary],check=True)
        for params,limit,wall_label in [((33,7,37,3),173,34),((35,13,43,5),213,28)]:
            a,b,c,_=params
            rows=solve(a,b,c,limit,False,collect=True)
            native_cost = 49 if c==37 else 63
            assert rows==[dict(mixed=[-1,-1],far=1,trunk=0,deepest=[0,-1],
                               native=[(-c,0,0,0,native_cost),(0,c,0,0,c)],
                               residual=[0]*6,shell=[0,0])]
            cases=[(0,-1,wall_label)]+[(1,s,t) for s in (1,-1) for t in range(c)
                                       if (s,t)!=(1,b*(2*a+b)%c)]
            with ThreadPoolExecutor(max_workers=4) as pool:
                results=list(pool.map(lambda case:check(binary,params,case),cases))
            summary={name:sum((r for case,r in zip(cases,results) if case[0]==w),Counter())
                     for w,name in enumerate('AC')}
            assert all(r['empty'] and not r['retained'] for r in summary.values())
            data[str(c)]=dict(profile=rows[0],cases=len(cases),outcomes=summary)
    return data


if __name__=='__main__':
    print(json.dumps(main(),indent=2))
