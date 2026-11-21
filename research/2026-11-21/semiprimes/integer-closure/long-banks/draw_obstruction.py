#!/usr/bin/env python3
"""Draw the exact two-choice obstruction; plotting is not part of the proof."""
from fractions import Fraction as F
import json
from math import sqrt
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

import long_bank_completion as bank

HERE=Path(__file__).resolve().parent


def rational(poly):return [tuple(F(v) for v in p) for p in poly]


def clip(subject,polygon):
    result=subject[:]
    for p,q in zip(polygon,polygon[1:]+polygon[:1]):
        output=[]
        for u,v in zip(result,result[1:]+result[:1]):
            du=bank.det(bank.sub(q,p),bank.sub(u,p))
            dv=bank.det(bank.sub(q,p),bank.sub(v,p))
            if du>=0:output.append(u)
            if (du>0 and dv<0) or (du<0 and dv>0):
                output.append(bank.add(u,bank.scale(du/(du-dv),bank.sub(v,u))))
        result=output
        if not result:break
    return result


def cart(poly):return [(float(x+y/2),float(y)*sqrt(3)/2) for x,y in poly]


def main():
    data=json.loads((HERE/'LONG_BANK_REPLAY.json').read_text())
    case=next(v for v in data['exact_configurations'] if v['name']=='compact_charged_13')
    evidence=case['direct_two_choice_obstruction']
    edge=rational(evidence['segment'])
    fig,axes=plt.subplots(1,2,figsize=(10.6,7.1),facecolor='#f8fafc')
    for k,ax in enumerate(axes):
        ax.set_facecolor('#f8fafc')
        candidate=rational(evidence['candidate_triangles'][k])
        blocker=rational(evidence['blocking_odd_triangles'][k][0])
        intersection=clip(candidate,blocker)
        assert len(intersection)>=3
        assert abs(sum(bank.det(p,q) for p,q in zip(intersection,intersection[1:]+intersection[:1])))>0
        ax.add_patch(Polygon(cart(blocker),closed=True,facecolor='#93c5fd',edgecolor='#2563eb',linewidth=2,label='Existing odd tile'))
        ax.add_patch(Polygon(cart(candidate),closed=True,facecolor='#fdba74',edgecolor='#c2410c',alpha=.72,linewidth=2,label='Required neighbor option'))
        ax.add_patch(Polygon(cart(intersection),closed=True,facecolor='#dc2626',edgecolor='#991b1b',linewidth=1.2,label='Positive-area overlap'))
        line=cart(edge);ax.plot([p[0] for p in line],[p[1] for p in line],color='#0f172a',linewidth=4,label='Mandatory edge, length 7')
        for point,label in zip(line,('(0,0)','(0,7)')):
            ax.scatter(*point,color='#0f172a',s=25,zorder=5)
            ax.annotate(label,point,xytext=(-9,7),textcoords='offset points',ha='right',fontsize=10,color='#0f172a')
        ax.set_title(f'Neighbor option {k+1}: impossible',loc='left',fontsize=13,color='#0f172a',pad=13)
        ax.set_aspect('equal');ax.set_xlim(-2,6.1);ax.set_ylim(-5,7.2);ax.axis('off')
    fig.suptitle('A whole mandatory edge has no possible neighbor',x=.06,ha='left',fontsize=19,fontweight='bold',color='#0f172a',y=.98)
    handles,labels=axes[0].get_legend_handles_labels()
    fig.legend(handles,labels,loc='lower center',bbox_to_anchor=(.5,.095),ncol=2,frameon=False,fontsize=11)
    fig.text(.06,.035,'Exact (5,3,7) control. Both neighbors overlap the same existing odd tile.\nThis excludes the displayed complete cell, not all configurations of 3431 or 5063.',fontsize=10,color='#475569',ha='left')
    fig.subplots_adjust(top=.88,bottom=.20,wspace=.23,left=.07,right=.97)
    svg=HERE/'mandatory_neighbor_obstruction.svg'
    fig.savefig(svg,metadata={'Date':None})
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
    fig.savefig(HERE/'mandatory_neighbor_obstruction.png',dpi=160)
    plt.close(fig)


if __name__=='__main__':main()
