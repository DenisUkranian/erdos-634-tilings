#!/usr/bin/env python3
"""Render the exact five-tile 86/13 obstruction; plotting is not a proof dependency."""
from fractions import Fraction as F
import json
from math import sqrt
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'owned'))
from legacy import core
from verify_area_cycles import check_physical,check_witness


def main():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon
    data=json.loads((HERE/'ISOMETRY_SEEDS_5063.json').read_text())
    g=core.Geometry(*data['sides'])
    tiles=[(g.point(*t[0]),*t[1:]) for t in data['tiles']]
    witness=next(w for w in data['general_area_cycle_cuts']
                 if w['tile_area_ratio']=='86/13' and len(w['indices'])==5)
    chosen=witness['indices']
    check_physical(g,tiles,chosen)
    check_witness(g,tiles,chosen,witness)
    def xy(point):
        x,y,e=point
        x,y=F(x,g.power(e)),F(y,g.power(e))
        return float(x+y/2),float(y)*sqrt(3)/2
    colors={-1:'#bd6b43',0:'#497b9c',1:'#678b54'}
    fig,ax=plt.subplots(figsize=(8,4.8),layout='constrained')
    for number,index in enumerate(chosen,1):
        tile=tiles[index]
        points=[xy(p) for p in g.vertices(tile)]
        ax.add_patch(Polygon(points,facecolor=colors[tile[1]],edgecolor='#24333d',
                             linewidth=1.4,alpha=.85))
        cx=sum(p[0] for p in points)/3;cy=sum(p[1] for p in points)/3
        ax.text(cx,cy,f'T{number}\nh = {tile[1]}',ha='center',va='center',fontsize=10,
                color='white',weight='bold')
    hole=[xy(p) for p in witness['vertices'][:-1]]
    ax.add_patch(Polygon(hole,facecolor='#fff4d2',edgecolor='#804c12',
                         linewidth=1.8,hatch='////',zorder=3))
    area2=sum(p[0]*q[1]-p[1]*q[0] for p,q in zip(hole,hole[1:]+hole[:1]))
    center=[sum((p[k]+q[k])*(p[0]*q[1]-p[1]*q[0])
                for p,q in zip(hole,hole[1:]+hole[:1]))/(3*area2) for k in (0,1)]
    ax.annotate('Hole: 86/13 tile areas',xy=center,xytext=(.99,.94),textcoords='axes fraction',
                ha='right',va='top',fontsize=11,color='#623b10',
                bbox=dict(boxstyle='round,pad=.45',facecolor='white',edgecolor='#b49a72'),
                arrowprops=dict(arrowstyle='->',color='#804c12',linewidth=1.4),zorder=5)
    ax.autoscale_view();ax.margins(.12);ax.set_aspect('equal');ax.set_axis_off()
    ax.set_title('A forbidden patch of five whole tiles',loc='left',fontsize=16,pad=18)
    fig.text(.5,.01,'Tile sides (35, 13, 43). Exact nonoverlap and hole area are checked separately.',
             ha='center',fontsize=9,color='#465461')
    for suffix in ('svg','png'):
        fig.savefig(HERE/f'FIVE_TILE_HOLE_5063.{suffix}',dpi=160,bbox_inches='tight',facecolor='white')
    print('EXACT_FIVE_TILE_OBSTRUCTION_RENDERED')


if __name__=='__main__':main()
