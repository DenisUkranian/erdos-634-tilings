#!/usr/bin/env python3
"""Draw the theta-isosceles certificates, preserving their exact coordinates.

This is a renderer, not a certificate verifier. Both panels use the same
physical scale. No external illustration or image-generation service is used.
"""
from pathlib import Path
import argparse
import json
import math

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.patches import Patch

COLORS = {
    'green': '#b8d8cf',
    'blue': '#b9cfe1',
    'yellow': '#eadcae',
    'red': '#dcae9e',
    'pink': '#d6bfd9',
    'base_parallelogram': '#b6c3b5',
    'cap_a_strips': '#d7d1bd',
    'cap_b_strips': '#c2bdcf',
}
LABELS = {
    'green':'Block A', 'blue':'Block B', 'yellow':'Block C',
    'red':'Block D', 'pink':'Block E',
    'base_parallelogram':'Base strip', 'cap_a_strips':'Cap strips',
    'cap_b_strips':'Cap strips B',
}


def panel(ax, data):
    den,D=data['denominator'],data['D']
    width=data['target'][1][0]/den
    def point(p):
        return (p[0]/den-width/2, p[1]*math.sqrt(D)/den)
    tiles=[[point(p) for p in t] for t in data['tiles']]
    colors=['#eeeeee']*len(tiles)
    legend=[]
    for comp in data['components']:
        if not comp['count']: continue
        first,count=comp['first'],comp['count']
        col=COLORS[comp['name']]
        colors[first:first+count]=[col]*count
        legend.append(Patch(facecolor=col,edgecolor='#596471',linewidth=.6,
                            label=f"{LABELS[comp['name']]}  ·  {count}"))
    coll=PolyCollection(tiles,facecolors=colors,edgecolors='#53616b',
                        linewidths=.47,antialiaseds=True)
    ax.add_collection(coll)
    target=[point(p) for p in data['target']]
    loop=target+[target[0]]
    ax.plot([p[0] for p in loop],[p[1] for p in loop],color='#263949',lw=1.6)
    # Dimension labels lie outside each equal leg and below the base.
    side=round(math.dist(target[0],target[2]))
    for sign, i in ((-1,0),(1,1)):
        a,b=target[i],target[2]
        mid=((a[0]+b[0])/2+sign*2.5,(a[1]+b[1])/2)
        ax.text(*mid,str(side),ha='center',va='center',fontsize=12.5,
                color='#263949',bbox=dict(fc='white',ec='none',pad=1.4))
    ax.text(0,-2.25,str(round(width)),ha='center',va='center',fontsize=12.5,
            color='#263949')
    ax.set_xlim(-19,19)
    ax.set_ylim(-4.1,57)
    ax.set_aspect('equal')
    ax.axis('off')
    n=data['N']
    scale=round(math.sqrt(n/3))
    ax.set_title(f"{n} congruent triangles",fontsize=18,fontweight='semibold',
                 color='#25394a',y=1.075,pad=0)
    ax.text(.5,1.025,f"t = {scale}  ·  target ({side}, {side}, {round(width)})",
            transform=ax.transAxes,ha='center',va='bottom',fontsize=11,
            color='#62707b')
    ax.legend(handles=legend,loc='upper center',bbox_to_anchor=(.5,-.045),
              ncol=2,frameon=False,fontsize=10.4,handlelength=1.15,
              columnspacing=1.8,labelspacing=.9)


def main():
    root=Path(__file__).resolve().parents[1]
    parser=argparse.ArgumentParser()
    parser.add_argument('--certificate-dir',type=Path,default=root/'data')
    parser.add_argument('--output-dir',type=Path,default=root/'figures')
    args=parser.parse_args()
    plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none',
                         'savefig.facecolor':'white'})
    fig,axes=plt.subplots(1,2,figsize=(11,11.3))
    fig.subplots_adjust(left=.055,right=.945,bottom=.225,top=.825,wspace=.13)
    for ax,n in zip(axes,(147,243)):
        source=args.certificate_dir/f'theta-{n}.json'
        data=json.loads(source.read_text())
        assert data['N']==n and len(data['tiles'])==n
        assert (data['a'],data['b'],data['c'])==(2,3,4)
        panel(ax,data)
    fig.text(.5,.959,'Two isosceles tilings',ha='center',fontsize=25,
             color='#25394a',fontweight='semibold')
    fig.text(.5,.925,'Congruent tile (2, 3, 4)  ·  apex α, base angles α + β',
             ha='center',fontsize=12,color='#62707b')
    fig.text(.5,.071,'The panels share one physical scale. Labels give actual side lengths.',
             ha='center',fontsize=10.3,color='#62707b')
    fig.text(.5,.045,'Individual edges and component colours are drawn from the exact coordinate certificates.',
             ha='center',fontsize=9.7,color='#62707b')
    args.output_dir.mkdir(parents=True,exist_ok=True)
    for ext in ('svg','png'):
        path=args.output_dir/f'theta-147-243.{ext}'
        fig.savefig(path,dpi=220)
        print(path)
    plt.close(fig)


if __name__=='__main__':
    main()
