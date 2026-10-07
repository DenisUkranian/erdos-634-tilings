#!/usr/bin/env python3
"""Exact exploratory 154 search with a complete pure-long 91-side root set.

New necessary test rounds partial orientation populations to the proved
modulo-13 populations. A timeout remains INCOMPLETE. This search output
is not an independently replayed nonexistence certificate.
"""
from collections import Counter
from functools import lru_cache
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
from pathlib import Path
import argparse
import json
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

def build():
    spec = spec_from_file_location('pure_long_engine', ROOT/'research/n105/search/exact_engine.py')
    e = module_from_spec(spec); spec.loader.exec_module(e)
    Q=e.Q
    e.N=154
    e.SEM={7*a+8*b+13*c for a in range(23) for b in range(20)
           for c in range(12) if 7*a+8*b+13*c<=154}
    # Counterclockwise target, with one length-91 side horizontal.
    e.OUT=(e.point(0,0),e.point(91,0),e.point(Q(1078,13),Q(1232,13)))
    e.OUT_EDGES=tuple((e.OUT[k],e.OUT[(k+1)%3]) for k in range(3))
    lengths=(91,91,154)

    @lru_cache(None)
    def positions(p):
        out=[]
        for k,(s,t) in enumerate(e.OUT_EDGES):
            if e.orient(s,t,p):continue
            # Signed Euclidean distance along the target edge.
            axis=0 if e.XY[s][0]!=e.XY[t][0] else 1
            q=(e.XY[p][axis]-e.XY[s][axis])/(e.XY[t][axis]-e.XY[s][axis])
            out.append((k,q*lengths[k]))
        return tuple(out)

    @lru_cache(None)
    def vertex_ok(p):
        return e.inside(p) and all(s.denominator==1 and s in e.SEM and lengths[k]-s in e.SEM
                                  for k,s in positions(p))

    # Reflect the canonical target and rotate its selected length-91 side
    # onto the horizontal axis. The old horizontal base then has height -1.
    exceptional=-1
    dirs={}
    for sign in (-1,1):
        v=(1,0)
        for mag in range(2*e.N+3):
            h=sign*mag;w=v
            for _ in range(6):
                dirs[w]=h;w=(-w[1],w[0]+w[1])
            v=e.normalize(*e.product(v,(8,7) if sign==1 else (15,-7)))

    @lru_cache(None)
    def height(t):
        vs=e.TRI[t]
        for i in range(3):
            p,q=vs[i],vs[(i+1)%3]
            if e.norm2(p,q) in (49,64):
                return dirs[e.direction(p,q)]
        raise AssertionError('Tile lacks a short edge')

    counters=Counter()
    def elementary_reject(ts):
        marked=set(e.OUT);ces=[]
        pos=[{Q(0),Q(L)} for L in lengths]
        counts=Counter(height(t) for t in ts)
        needed=sum(13*((n+12)//13) for h,n in counts.items() if h!=exceptional)
        n=counts.get(exceptional,0)
        needed+=11+13*max(0,(n-11+12)//13)
        if needed>154:
            counters['HEIGHT_POPULATION_BUDGET']+=1
            return ('HEIGHT_POPULATION_BUDGET',needed,sorted(counts.items()))
        for t in ts:
            marked.update(e.MARK[t]);ces.extend(e.CEDGES[t])
            for dst,src in zip(pos,e.BPOS[t]):dst.update(src)
        for p,q in ces:
            if p in marked and q in marked:return ('BOUNDARY_MARKS',p,q)
        for k,ss in enumerate(pos):
            ordered=sorted(ss)
            for p,q in zip(ordered,ordered[1:]):
                if q-p not in e.SEM:return ('BOUNDARY_GAP',k,str(p),str(q))
        return None

    e.positions=positions;e.vertex_ok=vertex_ok;e.elementary_reject=elementary_reject
    return e,counters,height

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--seconds',type=float,default=120)
    ap.add_argument('--per-root',type=float,default=8)
    ap.add_argument('--nodes',type=int,default=100000)
    args=ap.parse_args()
    e,counters,height=build()
    roots=[]
    for flips in product((0,1),repeat=7):
        ts=tuple(sorted(e.base_tile(13*i,13,f) for i,f in enumerate(flips)))
        if not all(e.vertex_ok(p) for t in ts for p in e.TRI[t]):continue
        if any(e.overlap(t,u) for i,t in enumerate(ts) for u in ts[:i]):continue
        if e.elementary_reject(ts):continue
        roots.append((flips,ts))
    print('complete pure-long roots',len(roots),flush=True)
    search=e.Search(seconds=args.seconds,nodes=args.nodes)
    results=[];end=time.monotonic()+args.seconds
    for flips,ts in roots:
        if time.monotonic()>=end:break
        search.deadline=min(end,time.monotonic()+args.per_root)
        try:
            yes=search.run(ts,e.add_tiles(e.OUT_EDGES,ts))
            status='TILING_CANDIDATE' if yes else 'EXHAUSTED_REQUIRES_INDEPENDENT_REPLAY'
        except TimeoutError:status='INCOMPLETE'
        results.append({'flips':flips,'status':status})
        print(flips,status,search.visited,flush=True)
        if search.solution is not None:break
    report={'scope':'Only the pure-c length-91 boundary row. Exact exploratory search, no negative claim.',
            'N':154,'tile':[8,7,13],'target_sides':[91,91,154],
            'status':'TILING_CANDIDATE' if search.solution is not None else 'INCOMPLETE',
            'root_count':len(roots),'results':results,'visited_nodes':search.visited,
            'maximum_placed_tiles':max(search.depth,default=0),'pruning':dict(counters),
            'seconds':round(time.monotonic()-search.start,3),
            'exceptional_height':-1,'full_Erdos634_solved':False}
    if search.solution is not None:
        report['triangles']=[[[str(x) for x in e.XY[p]] for p in e.TRI[t]] for t in search.solution]
    (HERE/'pure-long-report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('triangles','results')},indent=2))

if __name__=='__main__':main()
