#!/usr/bin/env python3
"""Vector drawings of exact certificates; floating point is used for rendering only."""
import json,math
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
HERE=Path(__file__).resolve().parent

def xy(p,d):return((p[0]+p[1]/2)/d,math.sqrt(3)*p[1]/(2*d))
def norm(v):return v[0]*v[0]+v[0]*v[1]+v[1]*v[1]
def height(t,d):
 for i in range(3):
  u=(t[(i+1)%3][0]-t[i][0],t[(i+1)%3][1]-t[i][1])
  if norm(u) in (9*d*d,25*d*d):return 0 if u[0]==0 or u[1]==0 or u[0]+u[1]==0 else 1
 raise ValueError('No short side')

def draw(count):
 obj=json.loads((HERE/f'equilateral_{count}.json').read_text());d=obj['denominator'];side=obj['target_side']
 fig,ax=plt.subplots(figsize=(7.2,6.6));ax.set_aspect('equal');ax.axis('off')
 for i,t in enumerate(obj['triangles']):
  color=('#f1d394' if height(t,d)==0 else '#8abbd7') if count==240 else ('#9fc8de' if i<240 else '#b7d5ab')
  ax.add_patch(Polygon([xy(p,d) for p in t],closed=True,facecolor=color,edgecolor='#42525c',linewidth=.42))
 ax.add_patch(Polygon([xy(p,d) for p in obj['target']],closed=True,fill=False,edgecolor='#142b3b',linewidth=1.6))
 if count==375:
  p,q=xy((0,105),7),xy((420,105),7);ax.plot([p[0],q[0]],[p[1],q[1]],color='#142b3b',linewidth=1.5)
  ax.text(side/2,40,'240-tile seed',ha='center',va='center',fontsize=12,bbox={'facecolor':'white','edgecolor':'none','alpha':.85,'pad':3})
  ax.text(side/2,6.5,'135-tile classical band',ha='center',va='center',fontsize=11,bbox={'facecolor':'white','edgecolor':'none','alpha':.85,'pad':2})
 ax.set_xlim(-3,side+3);ax.set_ylim(-5,side*math.sqrt(3)/2+5)
 ax.set_title(f'{count} congruent (3,5,7) triangles\nEquilateral side {side}',fontsize=15,pad=14,color='#142b3b')
 caption='Two short-edge direction classes; exact coordinate certificate.' if count==240 else 'A translated side-60 seed plus T(60,15); exact positive partition.'
 fig.text(.5,.04,caption,ha='center',fontsize=10,color='#465967');fig.subplots_adjust(left=.02,right=.98,bottom=.085,top=.88)
 out=HERE/'figures'/f'equilateral_{count}.svg';fig.savefig(out,format='svg',facecolor='white');fig.savefig(f'/tmp/equilateral_{count}_preview.png',dpi=130,facecolor='white');plt.close(fig);print(out.name)
if __name__=='__main__':
 for count in (240,375):draw(count)
