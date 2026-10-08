#!/usr/bin/env python3
"""Draw exact-coordinate macro construction (SVG and PNG)."""
from pathlib import Path
from fractions import Fraction as F
from math import sqrt
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

D=Path(__file__).resolve().parent
q=json.loads((D/'q480_macro.json').read_text());full=json.loads((D/'f3_4830_macro.json').read_text());rest=json.loads((D/'f3_4830_corner480_reduction.json').read_text())
COL=['#5477b2','#d3aa54','#91ba83','#c78ca4','#80b5b5','#aaa1c5','#e0bb80','#93b5d1','#bcce8d','#cc9c86']
def xy(p):x,y=map(F,p);return float(x+y/2),float(y)*sqrt(3)/2
def hull(ps):
 ps=sorted(set(tuple(map(F,p))for p in ps))
 def cross(a,b,c):return (b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-b[0])
 lo=[];hi=[]
 for p in ps:
  while len(lo)>=2 and cross(lo[-2],lo[-1],p)<=0:lo.pop()
  lo.append(p)
 for p in reversed(ps):
  while len(hi)>=2 and cross(hi[-2],hi[-1],p)<=0:hi.pop()
  hi.append(p)
 return lo[:-1]+hi[:-1]
def panel(ax,regions,target,title):
 for i,(count,poly)in enumerate(regions):
  pts=list(map(xy,poly));ax.add_patch(Polygon(pts,closed=True,facecolor=COL[i%len(COL)],edgecolor='#24303f',linewidth=1.2));xx=sum(p[0]for p in pts)/len(pts);yy=sum(p[1]for p in pts)/len(pts);ax.text(xx,yy,str(count),ha='center',va='center',fontsize=11,fontweight='bold',bbox=dict(facecolor='white',edgecolor='none',alpha=.75,pad=2))
 ax.add_patch(Polygon(list(map(xy,target)),closed=True,fill=False,edgecolor='#172432',linewidth=2));ax.autoscale_view();ax.set_aspect('equal');ax.axis('off');ax.set_title(title,fontsize=14,pad=14)

fig,ax=plt.subplots(figsize=(12,6));panel(ax,[(p['count'],p['polygon'])for p in q['parts']],q['target'],'The 480-tile corner: five ordinary grid regions');fig.text(.5,.025,'124 + 121 + 121 + 22 + 92 = 480     |     tile (24, 11, 31)',ha='center',fontsize=12);fig.tight_layout(rect=(0,.06,1,1));fig.savefig(D/'q480_five_regions.svg');fig.savefig(D/'q480_five_regions.png',dpi=160);plt.close(fig)

counts=[961,961,961,1104,363,124,121,121,22,92];regions=[];offset=0
for count in counts:
 ps=[p for t in full['triangles'][offset:offset+count]for p in t];regions.append((count,hull(ps)));offset+=count
if offset!=4830:raise RuntimeError('count')
fig,ax=plt.subplots(figsize=(12,9));panel(ax,regions,full['target'],'4830 congruent triangles: a direct positive construction');fig.text(.5,.025,'Target sides (961, 1155, 1426)     |     tile (24, 11, 31)',ha='center',fontsize=12);fig.tight_layout(rect=(0,.06,1,1));fig.savefig(D/'f3_4830_macro.svg');fig.savefig(D/'f3_4830_macro.png',dpi=160);plt.close(fig)
