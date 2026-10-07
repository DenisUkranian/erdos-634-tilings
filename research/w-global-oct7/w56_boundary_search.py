#!/usr/bin/env python3
"""Exact W56 search rooted at the proved short-side boundary word 9,9,6,6.

Root completeness relies on ADJACENT_C_EDGES.md, not a packing normal form.
Resource limits give INCOMPLETE. A completed exclusion still requires an
independently replayable full refutation before promotion to a theorem.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import argparse,json,sys,time
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'group1-global-scales'))
from pruned_search import E,Instance,PrunedSearch

def p(x,y):return F(x),F(y)/40

def enc(t):return [[str(x),str(40*y)] for x,y in t]

P=[p(46,20),p(49,14),p(52,8),p(54,4),p(56,0)]

def supported_triangle(s,A,B,rA,rB):
    v=E.sub(B,A)
    L2=E.dot(v,v,s.D)
    k=(rA*rA+L2-rB*rB)/(2*L2)
    h=-E.orient(*s.template)/L2
    normal=(-s.D*v[1],v[0])
    R=E.add(A,E.add(E.scale(v,k),E.scale(normal,h)))
    return E.triangle((A,B,R))

def all_roots(s):
    # The first c-edge has alpha at C; both a-edges have gamma first.
    # Only the orientation of the second c-edge remains free.
    roots=[];reports=[]
    for pair in [(5,6),(6,5)]:
        tri=[supported_triangle(s,P[0],P[1],F(5),F(6)),
             supported_triangle(s,P[1],P[2],*map(F,pair)),
             supported_triangle(s,P[2],P[3],F(5),F(9)),
             supported_triangle(s,P[3],P[4],F(5),F(9))]
        contained=all(E.inside(s.target,z) for t in tri for z in t)
        disjoint=not any(E.overlap(tri[i],tri[j]) for i in range(4) for j in range(i))
        metrics=all(sorted(E.dot(E.sub(a,b),E.sub(a,b),s.D) for a,b in E.edges(t))==[25,36,81] for t in tri)
        if not metrics:raise AssertionError('Boundary root tile metric')
        r={'second_c_start_angle':('alpha' if pair==(5,6) else 'beta'),
           'tiles':[enc(t) for t in tri],'contained':contained,'disjoint':disjoint}
        if contained and disjoint: roots.append(tuple(tri));r['status']='ADMISSIBLE_ROOT'
        else:r['status']='REJECTED_GEOMETRY'
        reports.append(r)
    return roots,reports

def run(seconds, root_index=None):
    s=PrunedSearch(Instance('G1-W',(6,5,9),(54,56,30),56,(2,3),2),
                   seconds=seconds,use_angles=True)
    roots,root_reports=all_roots(s)
    results=[]
    for i,root in enumerate(roots):
        if root_index is not None and i != root_index: continue
        before=s.nodes;start=time.monotonic()
        try:r=s.dfs(root)
        except (E.BudgetExceeded,RecursionError) as exc:
            r=None;resource_stop=type(exc).__name__
        else:resource_stop=None
        results.append({'root':i,'status':'TILING_FOUND' if r is True else 'EXHAUSTED' if r is False else 'INCOMPLETE',
                        'nodes':s.nodes-before,'seconds':round(time.monotonic()-start,6),'resource_stop':resource_stop})
        if r is True or r is None:break
    status='TILING_FOUND' if s.found is not None else 'EXHAUSTED' if len(results)==len(roots) and all(r['status']=='EXHAUSTED' for r in results) else 'INCOMPLETE'
    return {'status':status,'boundary_word':[9,9,6,6],'boundary_vertices':[enc([x])[0] for x in P],
            'boundary_roots':root_reports,'selected_root':root_index,'runs':results,'nodes':s.nodes,'maximum_placed':s.deepest,
            'seconds':round(time.monotonic()-s.start,6),'pruning_rejections':dict(s.rejected),
            'tile_coordinates':[enc(t) for t in s.found] if s.found else None,
            'metric':'dx²+2dy²','uses_adjacency_lemma':True,'full_Erdos634_solved':False}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=240);ap.add_argument('--output',type=Path);ap.add_argument('--root',type=int,choices=[0,1])
    args=ap.parse_args();report=run(args.seconds,args.root)
    text=json.dumps(report,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    print(text,end='')
