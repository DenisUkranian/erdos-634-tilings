#!/usr/bin/env python3
"""Construct F3 from the new semigroup criterion, without any solver input."""
from fractions import Fraction as F
from pathlib import Path
import argparse,json,hashlib
from reduce_corner import reduction
from construct_mixed_corner import construct


def full(a,b,c,q=None):
    patch=construct(a,b,c,q);rest=reduction(a,b,c)
    o,u,v=[tuple(map(F,rest['embedding'][key]))for key in ('origin','u','v')]
    def embed(p):
        x,y=map(F,p)
        return tuple(o[i]+(x+y)*u[i]/a+y*v[i]/b for i in (0,1))
    def ccw(t):
        p0,p1,p2=map(lambda p:tuple(map(F,p)),t)
        area=(p1[0]-p0[0])*(p2[1]-p0[1])-(p1[1]-p0[1])*(p2[0]-p0[0])
        if area==0:raise RuntimeError('degenerate')
        return t if area>0 else [t[0],t[2],t[1]]
    triangles=[ccw(t)for t in rest['partial_triangles']]+[ccw([[str(x),str(y)]for x,y in map(embed,t)])for t in patch['triangles']]
    if len(triangles)!=rest['count']:raise RuntimeError('count')
    return {'format':'ERDOS634_F3_UNIT_TRIANGLES_V1','coordinate_metric':'x^2+x*y+y^2','tile':[a,b,c],'multiplier':1,'count':rest['count'],'target':rest['target'],'triangles':triangles,'construction':'solver-free five-region mixed gamma corner and positive F3 transport','parameters':patch['parameters'],'component_counts':dict(rest['counts'],mixed_corner=patch['count'])}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--a',type=int,default=24);ap.add_argument('--b',type=int,default=11);ap.add_argument('--c',type=int,default=31);ap.add_argument('--q',type=int);ap.add_argument('--output',type=Path,default=Path(__file__).with_name('f3_4830_macro.json'));ar=ap.parse_args();d=full(ar.a,ar.b,ar.c,ar.q);ar.output.write_text(json.dumps(d,separators=(',',':'))+'\n');print(json.dumps({'count':d['count'],'parameters':d['parameters'],'sha256':hashlib.sha256(ar.output.read_bytes()).hexdigest()}))
if __name__=='__main__':main()
