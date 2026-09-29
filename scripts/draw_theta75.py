#!/usr/bin/env python3
"""Render the exact75-tile certificate. Optional dependency: matplotlib."""
import json,math
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['svg.hashsalt']='erdos634-theta75'
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
ROOT=Path(__file__).resolve().parents[1]
obj=json.loads((ROOT/'data/theta-75.json').read_text());den=obj['denominator'];sq=math.sqrt(15)
xy=lambda p:(p[0]/den,p[1]/den*sq)
colors=['#cbdff5','#b1ceec','#f4df9e','#ebc4d4','#bce1d4','#d0cbed','#dfc8a7','#f1b6ab','#efd2b7','#b7dce3']
fig,axes=plt.subplots(1,2,figsize=(12.4,8.4),gridspec_kw={'width_ratios':[.86,1.14]})
fig.patch.set_facecolor('white')
for ax,patchonly in zip(axes,[False,True]):
 for c,color in zip(obj['components'],colors):
  if patchonly and c['first']<49:continue
  batch=obj['tiles'][c['first']:c['first']+c['count']]
  for tri in batch:ax.add_patch(Polygon([xy(p) for p in tri],closed=True,facecolor=color,edgecolor='#526273',linewidth=.65))
  # Recover exact component boundary by canceling whole directed segments only
  # for drawing: atomize at integer coordinate points to retain T-junctions.
  net={}
  for tri in batch:
   for a,b in zip(tri,tri[1:]+tri[:1]):
    dx,dy=b[0]-a[0],b[1]-a[1];g=math.gcd(abs(dx),abs(dy));sx,sy=dx//g,dy//g
    for k in range(g):
     p=(a[0]+k*sx,a[1]+k*sy);q=(p[0]+sx,p[1]+sy)
     key=(p,q) if p<q else(q,p);net[key]=net.get(key,0)+(1 if p<q else-1)
  for (p,q),val in net.items():
   if val:ax.plot([xy(p)[0],xy(q)[0]],[xy(p)[1],xy(q)[1]],color='#334155',lw=1.15)
 ax.autoscale();ax.set_aspect('equal');ax.axis('off');ax.margins(.045)
axes[0].set_title('75 congruent triangles',fontweight='bold',fontsize=16,pad=16)
axes[1].set_title('The 26-tile completion',fontweight='bold',fontsize=16,pad=16)
axes[0].text(.5,-.035,'Tile sides: 2, 3, 4  ·  Target sides: 30, 30, 15',transform=axes[0].transAxes,ha='center',va='top',fontsize=10,color='#475569')
axes[1].text(.5,-.035,'One quadratic block, four grid blocks, two single tiles',transform=axes[1].transAxes,ha='center',va='top',fontsize=10,color='#475569')
fig.subplots_adjust(left=.015,right=.99,top=.92,bottom=.09,wspace=.12)
(ROOT/'figures').mkdir(exist_ok=True)
fig.savefig(ROOT/'figures/theta-75.svg',metadata={'Date':None},bbox_inches='tight')
fig.savefig(ROOT/'figures/theta-75.png',dpi=200,bbox_inches='tight')
