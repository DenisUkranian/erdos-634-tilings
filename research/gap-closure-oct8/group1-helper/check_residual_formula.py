#!/usr/bin/env python3
"""Exact endpoint-current and unit-type checks of explicit residual examples."""
from collections import Counter
from hashlib import sha256
from math import gcd
from pathlib import Path
import json
from residual_formula import generate


def require(ok,message):
    if not ok:raise RuntimeError(message)


def events(poly):
    for a,b in zip(poly,poly[1:]+poly[:1]):
        dx,dy=b[0]-a[0],b[1]-a[1]
        g=gcd(dx,dy);require(g>0,'zero edge')
        dx//=g;dy//=g
        if dx<0 or(dx==0 and dy<0):dx,dy=-dx,-dy
        yield (dx,dy,a[0],a[1]),1
        yield (dx,dy,b[0],b[1]),-1


def verify(data):
    u,t,v=data['u'],data['t'],data['v'];current=Counter();seen=set()
    for tri in data['triangles']:
        record=tuple(sorted(tuple(p)for p in tri))
        require(record not in seen,'duplicate tile');seen.add(record)
        determinant=(tri[1][0]-tri[0][0])*(tri[2][1]-tri[0][1])-(tri[1][1]-tri[0][1])*(tri[2][0]-tri[0][0])
        require(determinant==u*v,'nonpositive or wrong tile area')
        found=False
        for p in tri:
            others=[q for q in tri if q!=p]
            vectors=[(q[0]-p[0],q[1]-p[1])for q in others]
            for w,h in((u,v),(v,u)):
                for s in(-1,1):
                    if set(vectors)=={(s*w,0),(0,s*h)}:found=True
        require(found,'not a translated A/B tile or half-turn')
        for key,value in events(tri):current[key]+=value
    for key,value in events(data['target']):current[key]-=value
    require(not any(current.values()),'positioned boundary mismatch')
    return dict(u=u,t=t,tiles=len(data['triangles']),status='PASS',
                all_units_exact_A_or_B=True,all_orientations_positive=True,
                duplicate_free=True,positioned_boundary_identity=True)


def main():
    records=[]
    for u in range(3,9):
        for t in range(2,u):records.append(verify(generate(u,t)))
    result=dict(status='PASS',cases=records,total_cases=len(records),
                generator_sha256=sha256(Path(__file__).with_name('residual_formula.py').read_bytes()).hexdigest(),
                scope='Exact examples supplement the uniform written dissection; no finite-sample inference')
    Path(__file__).with_name('residual_examples_verified.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','cases':len(records),'largest_tiles':max(x['tiles']for x in records)}))


if __name__=='__main__':main()
