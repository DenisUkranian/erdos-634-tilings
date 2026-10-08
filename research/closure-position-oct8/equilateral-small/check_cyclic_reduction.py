#!/usr/bin/env python3
"""Check the conditional three-trapezoid partition, not the missing tiling."""
from fractions import Fraction as F
from pathlib import Path
import importlib.util,json
p=Path(__file__).resolve().parents[2]/'general-spectra'/'verify_certificate.py'
s=importlib.util.spec_from_file_location('G',p);G=importlib.util.module_from_spec(s);s.loader.exec_module(G)
def rot(p,k):
    u,v=p
    for _ in range(k):u,v=-u-v,u
    return u,v
def trap(x,L):return list(map(lambda p:tuple(map(F,p)),[(0,0),(x+L,0),(x,L),(0,L)]))
def case(r,s,t):
    S=15*(r+s+t);target=[(F(0),F(0)),(F(S),F(0)),(F(0),F(S))]
    specs=[(15*r,15*t,(15*s,0),0),(15*t,15*s,(0,15*(s+t)),2),(15*s,15*r,(15*(s+r),15*t),1)]
    polys=[[G.add(o,rot(v,k)) for v in trap(x,L)] for x,L,o,k in specs]
    for poly in polys:
        assert all(G.inside(v,target) for v in poly)
        assert all(G.orient(poly[i-1],poly[i],poly[(i+1)%4])>0 for i in range(4))
    for i in range(3):
        for j in range(i):
            q=G.clip(polys[i],polys[j]);assert len(q)<3 or G.area2(q)==0
    counts=[G.area2(p)/15 for p in polys]
    assert sum(G.area2(p) for p in polys)==G.area2(target)
    assert sum(counts)==F(S*S,15)
    return {'side':S,'tile_count':S*S//15,'trapezoids':[{'short_base':x,'leg':L,'count':int(n),'vertices':[[str(a),str(b)] for a,b in p]} for (x,L,o,k),n,p in zip(specs,counts,polys)],'result':'CONDITIONAL_PARTITION_VERIFIED','missing_tilings':[[x,L] for x,L,o,k in specs if x==30]}
if __name__=='__main__':
    result={'scope':'Does not construct the missing trapezoids','cases':[case(2,3,3),case(2,2,3)]}
    out=Path(__file__).with_name('cyclic_reduction_report.json');out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
