#!/usr/bin/env python3
"""Expand the exact 240-tile seed and classical bands to every multiplier m>=4.
The search program and its verdict are not imported.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse,hashlib,importlib.util,json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SEED=HERE.parent/'equilateral-search/cpsat_count/E60_0-1_certificate.json'
OLD=ROOT/'research/closure-position-oct8/equilateral-small/construct_new.py'
spec=importlib.util.spec_from_file_location('classical_bands',OLD)
bands=importlib.util.module_from_spec(spec);spec.loader.exec_module(bands)

def require(condition,message):
 if not condition:raise ValueError(message)

def seed_triangles():
 data=json.loads(SEED.read_text());den=data['denominator']
 require(data['tile']==[3,5,7] and den==7,'Unexpected seed normalization')
 require(data['target']==[[0,0],[420,0],[0,420]],'Unexpected seed target')
 require(len(data['triangles'])==240,'Unexpected seed count')
 return [tuple(tuple(F(v,den) for v in p) for p in tri) for tri in data['triangles']]

def generate(m):
 require(isinstance(m,int) and m>=4,'This theorem applies at integer m>=4')
 triangles=seed_triangles();blocks=[{'kind':'exact_E60_seed','count':240,'first_tile_index':0,'translation':[0,15*(m-4)]}]
 # Build upwards in side length. The previous equilateral triangle moves up
 # by15 while the new T(15k,15) fills the bottom band.
 for k in range(4,m):
  triangles=[tuple(bands.add(p,(0,15)) for p in t) for t in triangles]
  band=bands.one_band(15*k);first=len(triangles);triangles.extend(band)
  blocks.append({'kind':'classical_ideal_trapezoid','short_base':15*k,'leg':15,'count':len(band),'first_tile_index':first,'translation':[0,15*(m-k-1)]})
 require(len(triangles)==15*m*m,'Wrong generated count')
 side=15*m
 return {'format':'exact_polygon_unit_v1','coordinate_convention':'(u,v)/denominator denotes (u+v/2,sqrt(3)*v/2)/denominator','denominator':7,'tile':[3,5,7],'target':[[0,0],[7*side,0],[0,7*side]],'triangles':bands.encode(triangles),'tile_count':len(triangles),'target_side':side,'multiplier':m,'construction_blocks':blocks,'seed_sha256':hashlib.sha256(SEED.read_bytes()).hexdigest(),'claim':'A positive tiling of the specified equilateral triangle; no converse about arbitrary tile counts.'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--m',type=int,nargs='*',default=[4,5]);args=p.parse_args()
 for m in args.m:
  obj=generate(m);path=HERE/f"equilateral_{obj['tile_count']}.json";path.write_text(json.dumps(obj,indent=2)+'\n');print(path.name,obj['tile_count'])
if __name__=='__main__':main()
