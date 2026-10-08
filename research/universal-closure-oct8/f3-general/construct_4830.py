#!/usr/bin/env python3
"""Join exact Q480 tiling to the proved positive F3 corner reduction."""
from fractions import Fraction as F
from pathlib import Path
from math import gcd,lcm
import argparse,hashlib,json

DIR=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--corner',type=Path,default=DIR.parent/'4830-position/q480_tiling.json');ap.add_argument('--reduction',type=Path,default=DIR/'f3_4830_corner480_reduction.json');ap.add_argument('--output',type=Path,default=DIR/'f3_4830.json');ar=ap.parse_args()
    r=json.loads(ar.reduction.read_text());q=json.loads(ar.corner.read_text());a,b,c=r['tile']
    if q['tile']!=[a,b,c]or q['count']!=r['omitted_count']:raise ValueError('wrong corner tile/count')
    target=[tuple(map(F,p))for p in q['target']];expected=[tuple(map(F,p))for p in r['canonical_corner']]
    if target!=expected:raise ValueError('wrong canonical corner target')
    o,u,v=[tuple(map(F,r['embedding'][key]))for key in ('origin','u','v')]
    def image(p):
        x,y=map(F,p)
        return tuple(o[i]+(x+y)*u[i]/a+y*v[i]/b for i in (0,1))
    triangles=list(r['partial_triangles'])+[[[str(x),str(y)]for x,y in map(image,t)]for t in q['triangles']]
    if len(triangles)!=r['count']:raise ValueError('count mismatch')
    data={'format':'ERDOS634_F3_UNIT_TRIANGLES_V1','coordinate_metric':'x^2+x*y+y^2','tile':[a,b,c],'multiplier':1,'count':r['count'],'target':r['target'],'triangles':triangles,'construction':'Three c-fold grids, first-cell reflected interchange, and exact mixed-direction convex corner','component_counts':dict(r['counts'],mixed_corner=q['count']),'source_sha256':{'corner':hashlib.sha256(ar.corner.read_bytes()).hexdigest(),'reduction':hashlib.sha256(ar.reduction.read_bytes()).hexdigest()}}
    ar.output.write_text(json.dumps(data,separators=(',',':'))+'\n')
    den=lcm(*(F(x).denominator for t in triangles+[r['target']]for p in t for x in p))
    integer={'format':'ERDOS634_INTEGER_EISENSTEIN_TILING_V1','denominator':den,'tile':[a,b,c],'count':r['count'],'target':[[int(F(x)*den)for x in p]for p in r['target']],'triangles':[[[int(F(x)*den)for x in p]for p in t]for t in triangles]}
    integer_path=ar.output.with_name(ar.output.stem+'_integer.json');integer_path.write_text(json.dumps(integer,separators=(',',':'))+'\n')
    print(json.dumps({'count':len(triangles),'certificate':str(ar.output),'integer_certificate':str(integer_path),'denominator':den,'component_counts':data['component_counts'],'sha256':hashlib.sha256(ar.output.read_bytes()).hexdigest()}))
if __name__=='__main__':main()
