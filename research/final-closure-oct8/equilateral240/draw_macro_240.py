#!/usr/bin/env python3
import json,math
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from macro_240 import construct,area2
HERE=Path(__file__).resolve().parent
triangles,counts=construct();regions=json.loads((HERE/'macro_grid_regions.json').read_text())['regions']
def xy(p):return((p[0]+p[1]/2)/7,math.sqrt(3)*p[1]/14)
colors=['#a7cce1','#eed4a0','#a9d4c7','#d3bfdc','#f5beaa','#c2d39e','#a6bad9','#e4c6d5','#c4dcd4','#e4ba91','#b7c7e6','#d4d891','#c9b4d9','#ead89f','#abc7bd']
fig,ax=plt.subplots(figsize=(7.2,6.6));ax.set_aspect('equal');ax.axis('off')
for color,g in zip(colors,regions):ax.add_patch(Polygon([xy(p)for p in g['polygon']],closed=True,facecolor=color,edgecolor='none'))
for t in triangles:ax.add_patch(Polygon([xy(p)for p in t],closed=True,facecolor='none',edgecolor='#66707b',linewidth=.32))
for g in regions:
 p=g['polygon'];ax.add_patch(Polygon([xy(q)for q in p],closed=True,facecolor='none',edgecolor='#182e40',linewidth=1.3))
 aa=area2(p);cross=lambda a,b:a[0]*b[1]-a[1]*b[0]
 cx=sum((a[0]+b[0])*cross(a,b)for a,b in zip(p,p[1:]+p[:1]))/(3*aa);cy=sum((a[1]+b[1])*cross(a,b)for a,b in zip(p,p[1:]+p[:1]))/(3*aa)
 x,y=xy((cx,cy));ax.text(x,y,str(g['count']),ha='center',va='center',fontsize=8 if g['count']==1 else 10,color='#142634',weight='bold',bbox={'facecolor':'white','edgecolor':'none','alpha':.75,'pad':1})
ax.set_xlim(-3,63);ax.set_ylim(-3,60*math.sqrt(3)/2+4);ax.set_title('240 tiles in fifteen convex grid regions',fontsize=15,color='#142b3b',pad=16)
fig.text(.5,.04,'Labels count unit (3,5,7) triangles in each region.',ha='center',fontsize=10,color='#465967');fig.subplots_adjust(left=.02,right=.98,bottom=.085,top=.9)
fig.savefig(HERE/'figures/macro_240.svg',format='svg',facecolor='white');fig.savefig('/tmp/macro_240_preview.png',dpi=130,facecolor='white');print('Saved macro_240.svg')
