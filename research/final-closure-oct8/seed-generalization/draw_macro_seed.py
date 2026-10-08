#!/usr/bin/env python3
"""Render the exact macro data as a vector SVG; floats are for display only."""
import math
from pathlib import Path
from macro_seed import PATCHES,TARGET,construct
triangles,_=construct()
colors=['#a8d5e2','#f4cb89','#bad6a5','#b8dce8','#d8b6e7','#f2af9c','#c6b7e7','#ebd584','#94cbbb','#b3c6ea','#ddbacb']
scale=11.6

def p(v):return(44+scale*(v[0]+v[1]/2)/7,366-scale*math.sqrt(3)*v[1]/14)
def poly(v):return' '.join(f'{x:.4f},{y:.4f}' for x,y in map(p,v))
s=['<svg xmlns="http://www.w3.org/2000/svg" width="850" height="440" viewBox="0 0 850 440">','<rect width="850" height="440" fill="white"/>','<text x="44" y="31" font-size="22" font-family="sans-serif" fill="#182632">T(30,30): eleven ordinary triangular-grid regions</text>']
for i,(_,_,_,_,pts,n) in enumerate(PATCHES):s.append(f'<polygon points="{poly(pts)}" fill="{colors[i]}"/>')
for t in triangles:s.append(f'<polygon points="{poly(t)}" fill="none" stroke="#6e7376" stroke-width="0.55"/>')
for i,(_,_,_,_,pts,n) in enumerate(PATCHES):
 s.append(f'<polygon points="{poly(pts)}" fill="none" stroke="#202a35" stroke-width="1.7"/>')
 # Area centroid is used only for display placement.
 aa=sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(pts,pts[1:]+pts[:1]))
 cx=sum((a[0]+b[0])*(a[0]*b[1]-a[1]*b[0]) for a,b in zip(pts,pts[1:]+pts[:1]))/(3*aa)
 cy=sum((a[1]+b[1])*(a[0]*b[1]-a[1]*b[0]) for a,b in zip(pts,pts[1:]+pts[:1]))/(3*aa)
 x,y=p((cx,cy));fs=11 if n==1 else 14
 s.append(f'<text x="{x:.3f}" y="{y+4:.3f}" font-size="{fs}" text-anchor="middle" font-family="sans-serif" font-weight="bold" fill="#111" stroke="white" stroke-width="3" paint-order="stroke">{n}</text>')
s.append(f'<polygon points="{poly(TARGET)}" fill="none" stroke="#172536" stroke-width="2.8"/>')
s.append('<text x="44" y="405" font-size="16" font-family="sans-serif" fill="#283442">Labels count unit (3,5,7) triangles in each region; total 180.</text>')
s.append('<text x="44" y="428" font-size="13" font-family="sans-serif" fill="#5f6973">All geometry is specified exactly by the integer table in MACRO_PROOF.md.</text>')
s.append('</svg>')
Path(__file__).with_name('macro_seed.svg').write_text('\n'.join(s)+'\n')
print('Wrote macro_seed.svg')
