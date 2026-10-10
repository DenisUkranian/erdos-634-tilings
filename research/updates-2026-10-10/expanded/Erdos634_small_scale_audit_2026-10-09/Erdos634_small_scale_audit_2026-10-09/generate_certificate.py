#!/usr/bin/env python3
"""Export a complete fixed-instance convex-corner refutation tree.
Resource exhaustion is never recorded as a refutation. No chain, packing,
direction-band, component-area or reverse-apex hypothesis is used.
"""
from pathlib import Path
from time import monotonic
import json
import exact_small_search as g

class CertificateSearch(g.Search):
    def __init__(self, I, seconds=30):
        super().__init__(I,seconds,1000000,prune=False)
        self.records=[]
    def visit(self, placed, boundary, boxes):
        self.checktime(); self.nodes+=1
        if len(placed)==self.N: raise RuntimeError('TILING EXISTS; cannot export negative proof')
        sec,_=g.sectors(boundary,self.D)
        choice=None; choices=None
        for s in sec:
            ps=self.placements(s,placed,boxes)
            if choices is None or len(ps)<len(choices):choice,choices=s,ps
            if len(ps)<=1:break
        if choice is None:raise RuntimeError('invalid positive-area residual')
        _,v,out,inc=choice
        ix=len(self.records)
        row={'sector':g.encode((v,g.add(v,out),g.add(v,inc))), 'children':[]}
        self.records.append(row)
        for t in choices:
            child=self.visit(placed+[t],g.boundary_add(boundary,t),boxes+[g.bbox(t)])
            row['children'].append({'triangle':g.encode(t),'node':child})
        return ix

def generate(u,v,m,branch,out):
    I=g.make_instance(u,v,m,branch); s=CertificateSearch(I)
    s.visit([],tuple(sorted(g.edges(I['target']))),[])
    data={'format':'fixed-triangle-convex-corner-refutation-v1','scope':'one specified tile and target; not global N classification',
          'parameters':{'u':u,'v':v,'m':m,'branch':branch},'D':I['D'],'N':I['N'],'tile':I['tile'],'target':g.encode(I['target']),
          'nodes':s.records,'search_seconds':monotonic()-s.start,
          'uses_packing_or_prime_candidate':False,'has_direction_cutoff':False}
    Path(out).write_text(json.dumps(data,indent=2)+'\n')
    print(out,len(s.records),'nodes',flush=True)

if __name__=='__main__':
    for u,v,m,branch in [(1,2,1,'W'),(1,2,1,'beta'),(2,3,1,'W'),(2,3,1,'beta'),(1,3,1,'W'),(1,3,1,'beta')]:
        generate(u,v,m,branch,Path(__file__).with_name(f'{branch}_{u}_{v}_{m}_refutation.json'))
