#!/usr/bin/env python3
"""Independent exact convex geometry audit of explicit Eisenstein-coordinate tilings.

No construction, search, current matrix, or other geometric verifier is imported.
The input coordinates represent (x+y*rho)/denominator, rho=exp(i*pi/3).
"""
import argparse,hashlib,json,time
from pathlib import Path

def subtract(p,q):return (p[0]-q[0],p[1]-q[1])
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def turn(p,q,r):return det(subtract(q,p),subtract(r,p))
def norm2(p):return p[0]*p[0]+p[0]*p[1]+p[1]*p[1]
def doubled_area(poly):return sum(det(p,q) for p,q in zip(poly,poly[1:]+poly[:1]))

def require(condition,message):
    if not condition:raise ValueError(message)

def normalize_polygon(poly):
    require(isinstance(poly,list) and len(poly)>=3,'Malformed polygon.')
    require(all(isinstance(p,list) and len(p)==2 and all(isinstance(c,int) and not isinstance(c,bool) for c in p) for p in poly),'Noninteger coordinate.')
    out=[tuple(p) for p in poly]
    if doubled_area(out)<0:out.reverse()
    require(doubled_area(out)>0,'Degenerate polygon.')
    require(all(turn(out[i],out[(i+1)%len(out)],out[(i+2)%len(out)])>0 for i in range(len(out))),'Target or tile is not strictly convex.')
    require(all(turn(p,q,r)>=0 for p,q in zip(out,out[1:]+out[:1]) for r in out),'Polygon has a vertex outside an edge half-plane.')
    return out

def separate(a,b):
    # For convex polygons, their edge normals form a complete set of separating axes.
    # Equality permits a shared edge, endpoint, or T-junction.
    for p,q in zip(a,a[1:]+a[:1]):
        if all(turn(p,q,r)<=0 for r in b):return True
    for p,q in zip(b,b[1:]+b[:1]):
        if all(turn(p,q,r)<=0 for r in a):return True
    return False

def audit(path):
    start=time.perf_counter();raw=path.read_bytes();certificate=json.loads(raw)
    denominator=certificate['denominator'];require(isinstance(denominator,int) and denominator>0,'Invalid denominator.')
    tile=certificate['tile'];require(len(tile)==3 and all(isinstance(s,int) and s>0 for s in tile),'Invalid tile sides.')
    expected_norms=sorted(s*s*denominator*denominator for s in tile)
    target=normalize_polygon(certificate['target'])
    triangles=[];boxes=[];sum_area=0
    for i,entry in enumerate(certificate['triangles']):
        require(len(entry)==3,f'Tile {i} does not have three vertices.')
        t=normalize_polygon(entry)
        lengths=sorted(norm2(subtract(t[j],t[(j+1)%3])) for j in range(3))
        require(lengths==expected_norms,f'Tile {i} is not congruent: {lengths}.')
        require(all(turn(p,q,v)>=0 for p,q in zip(target,target[1:]+target[:1]) for v in t),f'Tile {i} not contained in target.')
        sum_area+=doubled_area(t);triangles.append(t)
        boxes.append((min(p[0] for p in t),max(p[0] for p in t),min(p[1] for p in t),max(p[1] for p in t)))
    pair_count=0;quick=0;sat=0
    for i,a in enumerate(triangles):
        aminx,amaxx,aminy,amaxy=boxes[i]
        for j in range(i):
            pair_count+=1;bminx,bmaxx,bminy,bmaxy=boxes[j]
            if amaxx<=bminx or bmaxx<=aminx or amaxy<=bminy or bmaxy<=aminy:
                quick+=1;continue
            require(separate(a,triangles[j]),f'Positive-area overlap between tiles {j} and {i}.');sat+=1
    require(sum_area==doubled_area(target),'Tile area sum differs from target area.')
    return {'status':'PASS','certificate':str(path),'sha256':hashlib.sha256(raw).hexdigest(),
            'denominator':denominator,'tile':tile,'tiles':len(triangles),
            'exact_squared_lengths_checked':3*len(triangles),'contained_triangles':len(triangles),
            'pairwise_interior_disjointness_checks':pair_count,'affine_box_separations':quick,
            'exact_edge_separating_axis_checks':sat,'target_determinant_area':doubled_area(target),
            'sum_tile_determinant_areas':sum_area,'coverage':'Exact: containment + pairwise disjoint interiors + equal area.',
            'independence':'No construction code, matrix, solver, or existing geometric verifier imported.',
            'seconds':time.perf_counter()-start}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('certificate',type=Path);ap.add_argument('--output',type=Path);args=ap.parse_args()
    report=audit(args.certificate);rendered=json.dumps(report,indent=2)+'\n'
    if args.output:args.output.write_text(rendered)
    print(rendered,end='')
