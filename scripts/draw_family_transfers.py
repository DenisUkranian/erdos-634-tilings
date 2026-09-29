#!/usr/bin/env python3
"""Draw the three exact macrodissections used by the eventual theorem.

The representative shape uses (u,v)=(1,2); the identities are uniform.
These are conditional transfers, not claims that the blue unit inputs tile.
"""
from pathlib import Path
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Patch

ROOT=Path(__file__).resolve().parents[1]
BLUE='#c1d8e5'; GOLD='#ead8a1'; ROSE='#ddb7a2'; INK='#314854'


def draw(ax,pieces,outer,names,title,equation):
    for points,color,label in pieces:
        ax.add_patch(Polygon(points,closed=True,facecolor=color,edgecolor=INK,lw=1.05))
        x=sum(p[0] for p in points)/3; y=sum(p[1] for p in points)/3
        ax.text(x,y,label,ha='center',va='center',fontsize=11,color=INK)
    xs=[p[0] for p in outer];ys=[p[1] for p in outer]
    span=max(xs)-min(xs)
    margin=span*.13
    ax.set_xlim(min(xs)-margin,max(xs)+margin)
    ax.set_ylim(min(ys)-max(ys)*.20,max(ys)*1.20)
    ax.set_aspect('equal');ax.axis('off')
    loop=outer+[outer[0]]
    ax.plot([p[0] for p in loop],[p[1] for p in loop],c=INK,lw=1.6)
    center=(sum(xs)/3,sum(ys)/3)
    for i,name in enumerate(names):
        p,q=outer[i],outer[(i+1)%3]
        x,y=(p[0]+q[0])/2,(p[1]+q[1])/2
        dx,dy=x-center[0],y-center[1]
        norm=math.hypot(dx,dy)
        x+=margin*.46*dx/norm;y+=margin*.46*dy/norm
        ax.text(x,y,name,ha='center',va='center',fontsize=10.5,color=INK,
                bbox=dict(fc='white',ec='none',pad=1.5))
    ax.set_title(title,fontsize=16,color=INK,pad=10)
    ax.text(.5,-.15,equation,ha='center',va='top',transform=ax.transAxes,fontsize=11,color=INK)


def main():
    plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none'})
    h=1.5*math.sqrt(15)
    A=(0,0);C=(3,0);B=(1.5,h);D=(7,0);E=(-4,0)
    fig,axes=plt.subplots(1,3,figsize=(13,5.2))
    fig.subplots_adjust(left=.03,right=.97,bottom=.27,top=.73,wspace=.24)
    draw(axes[0],[([A,B,C],BLUE,r'$\Theta_T$'),([B,C,D],GOLD,r'$vT\cdot\mathcal{T}$')],
         [A,B,D],[r'$bvT$',r'$v^3T$',r'$uQT$'],r'$\Theta_T\ \longrightarrow\ W_T$',
         r'$bT^2+(vT)^2=QT^2$')
    draw(axes[1],[([A,B,C],BLUE,r'$\Theta_T$'),([B,C,D],GOLD,r'$vT\cdot\mathcal{T}$'),
                  ([E,A,B],ROSE,r'$vT\cdot\mathcal{T}$')],
         [E,B,D],[r'$v^3T$',r'$v^3T$',r'$uPT$'],r'$\Theta_T\ \longrightarrow\ B_T$',
         r'$bT^2+2(vT)^2=PT^2$')
    # Rotate the alpha construction so its long outer side is horizontal.
    AA=(9,0);BB=(21,0);CC=(10.5,h);EE=(0,0)
    draw(axes[2],[([AA,BB,CC],BLUE,r'$\Theta_{vK}$'),([EE,AA,CC],GOLD,r'$bK\cdot\mathcal{T}$')],
         [EE,CC,BB],[r'$bcK$',r'$bcK$',r'$bQK$'],r'$\Theta_{vK}\ \longrightarrow\ A_K$',
         r'$b(vK)^2+(bK)^2=bQK^2$')
    fig.text(.5,.94,'Three transfers from a theta-isosceles tiling',ha='center',
             fontsize=21,fontweight='semibold',color=INK)
    fig.text(.5,.88,'Attach standard quadratic copies of the same tile along a complete side.',
             ha='center',fontsize=11.5,color='#64737d')
    fig.legend(handles=[Patch(facecolor=BLUE,edgecolor=INK,label='Already tiled input'),
                        Patch(facecolor=GOLD,edgecolor=INK,label='Quadratic tile block'),
                        Patch(facecolor=ROSE,edgecolor=INK,label='Second quadratic block')],
               loc='lower center',bbox_to_anchor=(.5,.085),ncol=3,frameon=False,fontsize=10.5)
    fig.text(.5,.035,'Conditional macrodissections; the blue unit-scale input need not itself be tileable. Panels are fitted independently.',
             ha='center',fontsize=9.5,color='#64737d')
    out=ROOT/'figures';out.mkdir(exist_ok=True)
    for ext in ('svg','png'):
        p=out/f'family-transfers.{ext}';fig.savefig(p,dpi=200,facecolor='white');print(p)
    plt.close(fig)


if __name__=='__main__':main()
