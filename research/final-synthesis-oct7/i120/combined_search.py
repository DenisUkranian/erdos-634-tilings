#!/usr/bin/env python3
"""Bounded 154 search with necessary integer-seam pruning.

The existing n105 engine supplies complete corner-fan branching, arc
consistency and binary implication pruning. This adapter changes the
target and adds the proved integer-atom necessary condition. A timeout
is INCOMPLETE; this file is not an independent refutation checker.
"""
from functools import lru_cache
from importlib.util import module_from_spec, spec_from_file_location
from math import isqrt
from pathlib import Path
from collections import Counter
import argparse
import json
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seconds', type=float, default=300)
    ap.add_argument('--nodes', type=int, default=100000)
    args = ap.parse_args()
    source = ROOT / 'research/n105/search/exact_engine.py'
    spec = spec_from_file_location('i120_integer_engine', source)
    e = module_from_spec(spec)
    spec.loader.exec_module(e)
    Q = e.Q
    e.N = 154
    e.SEM = {7*a+8*b+13*c for a in range(23) for b in range(20)
             for c in range(12) if 7*a+8*b+13*c <= 154}
    e.OUT = (e.point(0,0),e.point(154,0),e.point(49,56))
    e.OUT_EDGES = tuple((e.OUT[k],e.OUT[(k+1)%3]) for k in range(3))

    @lru_cache(None)
    def positions(p):
        x,y = e.XY[p]
        out = []
        if y == 0: out.append((0,x))
        if 8*x+15*y == 1232: out.append((1,13*y/8))
        if 8*x-7*y == 0: out.append((2,13*y/8))
        return tuple(out)

    @lru_cache(None)
    def vertex_ok(p):
        return e.inside(p) and all(s.denominator == 1 and s.numerator in e.SEM
                    and [154,91,91][k]-s in e.SEM for k,s in positions(p))

    dirs = {}
    for sign in (-1,1):
        vec=(1,0)
        for mag in range(2*e.N+3):
            h=sign*mag; rot=vec
            for _ in range(6):
                dirs[rot]=h; rot=(-rot[1],rot[0]+rot[1])
            vec=e.normalize(*e.product(vec,(8,7) if sign==1 else (15,-7)))
    @lru_cache(None)
    def height(t):
        vs=e.TRI[t]
        for i in range(3):
            p,q=vs[i],vs[(i+1)%3]
            if e.norm2(p,q) in (49,64):return dirs[e.direction(p,q)]
        raise AssertionError('No short edge')
    height_rejections=Counter()
    def elementary_reject(ts):
        counts=Counter(height(t) for t in ts)
        needed=11+13*max(0,(counts.get(0,0)-11+12)//13)
        needed+=sum(13*((n+12)//13) for h,n in counts.items() if h!=0)
        hs=sorted(set(counts)|{0})
        needed+=13*sum(max(0,(b-a+1)//2-1) for a,b in zip(hs,hs[1:]))
        if needed>154:
            height_rejections['connected_height_budget']+=1
            return ('CONNECTED_HEIGHT_BUDGET',needed)

        marked = set(e.OUT); ces = []
        pos = [{Q(0),Q(154)},{Q(0),Q(91)},{Q(0),Q(91)}]
        for t in ts:
            marked.update(e.MARK[t]); ces.extend(e.CEDGES[t])
            for dst,src in zip(pos,e.BPOS[t]): dst.update(src)
        for p,q in ces:
            if p in marked and q in marked: return ('BOUNDARY_MARKS',p,q)
        for j,ss in enumerate(pos):
            ordered = sorted(ss)
            for p,q in zip(ordered,ordered[1:]):
                if q-p not in e.SEM: return ('BOUNDARY_GAP',j,str(p),str(q))
        return None

    e.positions = positions
    e.vertex_ok = vertex_ok
    e.elementary_reject = elementary_reject
    counters = Counter()

    @lru_cache(maxsize=1000000)
    def integral_length(p,q):
        n = e.norm2(p,q)
        return n.denominator == 1 and isqrt(n.numerator)**2 == n.numerator

    old_overlap = e.overlap

    @lru_cache(maxsize=1000000)
    def seam_conflict(a,b):
        aa,bb = e.BOX[a],e.BOX[b]
        if aa[1]<bb[0] or bb[1]<aa[0] or aa[3]<bb[2] or bb[3]<aa[2]:
            return False
        for t,u in ((e.TRI[a],e.TRI[b]),(e.TRI[b],e.TRI[a])):
            for v in t:
                for j,p in enumerate(u):
                    q = u[(j+1)%3]
                    if v not in (p,q) and e.on_segment(p,q,v):
                        counters['vertex_on_edge_checks'] += 1
                        if not integral_length(p,v):
                            counters['distinct_pair_seam_conflicts'] += 1
                            return True
        return False

    def incompatible(a,b):
        if old_overlap(a,b): return True
        return seam_conflict(min(a,b),max(a,b))

    original_boundary_info = e.boundary_info
    def boundary_info(boundary):
        for p,q in boundary:
            if not integral_length(p,q):
                counters['rejected_noninteger_boundaries'] += 1
                return None,('NONINTEGER_BOUNDARY_LENGTH',p,q,str(e.norm2(p,q)))
        return original_boundary_info(boundary)

    # Test the new geometric condition on every pair of a known actual
    # 990-tiling, including all vertex-on-edge contacts. Only this test's
    # coordinates are loaded; no target-specific fans are generated.
    fixture = json.loads((ROOT/'research/group2-nested-corners/f3-990.json').read_text())
    fixture_ids = [e.triangle(tuple(e.point(*p) for p in tri)) for tri in fixture['triangles']]
    for i,t in enumerate(fixture_ids):
        for u in fixture_ids[i+1:]:
            if seam_conflict(min(t,u),max(t,u)):
                raise AssertionError('Rejected an existing positive fixture')
    fixture_contacts = counters['vertex_on_edge_checks']
    counters.clear()
    e.overlap = incompatible
    e.boundary_info = boundary_info
    search = e.Search(seconds=args.seconds,nodes=args.nodes)
    try:
        found = search.run((),e.OUT_EDGES)
        status = 'TILING_CANDIDATE' if found else 'EXHAUSTED_REQUIRES_INDEPENDENT_REPLAY'
    except TimeoutError:
        status = 'INCOMPLETE'
    report = {
        'status': status, 'tile': [8,7,13], 'target_sides': [91,91,154],
        'full_Erdos634_solved': False,
        'N': 154, 'root': 'empty; all target-corner fans covered',
        'source_engine': str(source.relative_to(ROOT)),
        'new_pruning': 'Integer seam conditions plus connected height-population budget; apex-first branch order',
        'positive_fixture_990_pairs_checked': 990*989//2,
        'positive_fixture_vertex_on_edge_contacts_checked': fixture_contacts,
        'visited_nodes': search.visited,
        'maximum_placed_tiles': max(search.depth,default=0),
        'partial_dead_states': len(search.cert),
        'new_pruning_counts': dict(counters), 'height_pruning_counts': dict(height_rejections),
        'seconds': round(time.monotonic()-search.start,3),
        'limit_seconds': args.seconds, 'limit_nodes': args.nodes,
        'scope': 'Exact search probe; no nonexistence claim without independent replay.'
    }
    if search.solution is not None:
        report['triangles'] = [[[str(x) for x in e.XY[p]] for p in e.TRI[t]]
                               for t in search.solution]
    (HERE/'combined-search-report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k != 'triangles'},indent=2))


if __name__ == '__main__':
    main()
