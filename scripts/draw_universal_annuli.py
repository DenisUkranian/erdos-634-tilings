"""Optional Matplotlib illustration; exact construction is in the checker."""
from pathlib import Path
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

ROOT=Path(__file__).resolve().parents[1]
plt.rcParams.update({"font.family":"DejaVu Sans","svg.fonttype":"none",
                     "savefig.facecolor":"#f7f9fc"})
u,v=3,4
a,b,c=u*v,v*v-u*u,v*v
root=math.sqrt(4*v*v-u*u)
blue,orange,purple,green="#8db9e8","#f1bb77","#c0a2dd","#a8d3bb"
ink="#172a40"


def physical(p):return (p[0],p[1]*root)
def draw(ax,points,pieces,title,subtitle,rotate=False):
    points={k:physical(p) for k,p in points.items()}
    if rotate:
        origin=points["A"]
        ux,uy=u/(2*v),-root/(2*v)
        def tf(p):
            x,y=p[0]-origin[0],p[1]-origin[1]
            return (x*ux+y*uy,x*uy-y*ux)
        points={k:tf(p) for k,p in points.items()}
    for labels,color,text in pieces:
        poly=[points[k] for k in labels]
        ax.add_patch(Polygon(poly,facecolor=color,edgecolor=ink,lw=1.15,joinstyle="round"))
        x=sum(p[0] for p in poly)/len(poly)
        y=sum(p[1] for p in poly)/len(poly)
        ax.text(x,y,text,ha="center",va="center",fontsize=10,color=ink,
                bbox=dict(facecolor=color,edgecolor="none",alpha=.88,pad=2))
    xs=[p[0] for p in points.values()]; ys=[p[1] for p in points.values()]
    width=max(xs)-min(xs);height=max(ys)-min(ys)
    for k,(x,y) in points.items():
        dy=-12 if y<min(ys)+height*.08 else 10
        ax.annotate(k,(x,y),xytext=(0,dy),textcoords="offset points",
                    ha="center",va="center",fontsize=10,color=ink)
    ax.set_xlim(min(xs)-width*.06,max(xs)+width*.06)
    ax.set_ylim(min(ys)-height*.37,max(ys)+height*.40)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title+"\n"+subtitle,fontsize=12,color=ink,pad=18,linespacing=1.6)


fig,axes=plt.subplots(2,1,figsize=(12,7.8),facecolor="#f7f9fc")
T=14
points=dict(A=(0,0),C=(u*b*(T+u),0),B=(u*u*b/2,u*b/2),
            E=(u*u*b/2+u*b*T,u*b/2))
points.update(D=(points["B"][0]+a*a,points["B"][1]),R=(c*c,0),
              S=(points["E"][0]-b*b,points["E"][1]))
draw(axes[0],points,
     [("ABD",blue,"scale a = 12"),("ADR",orange,"scale c = 16"),
      ("SEC",purple,"scale b\n7"),("RDSC",green,"mixed b/c strips\n101 × 112")],
     "Fix the apex: add u = 3","θ₁₄ → θ₁₇   ·   3 similar triangles + 1 parallelogram")
T=9
points=dict(A=(u*b*(T+v)/2,b*(T+v)/2),B=(u*b*(T+v),0),
            C=(u*b*T,0),D=(u*b*T/2,b*T/2),
            E=(u*b*T-u*u*u*v/2,u*u*v/2))
points["G"]=(points["E"][0]+u*b*v/2,points["E"][1]+b*v/2)
draw(axes[1],points,
     [("BCE",blue,"scale a = 12"),("BEG",orange,"scale c = 16"),
      ("ADEG",green,"mixed b/c strips\n108 × 112")],
     "Fix a base vertex: add v = 4","θ₉ → θ₁₃   ·   2 similar triangles + 1 parallelogram",True)
fig.suptitle("Two coprime additions for the tile (12, 7, 16)",
             x=.5,y=.985,fontsize=18,fontweight="bold",color=ink)
fig.text(.5,.02,"Exact geometry. Colored triangles use ordinary quadratic grids; green regions use b-by-c cells.",
         ha="center",fontsize=10,color="#485b70")
fig.subplots_adjust(top=.86,bottom=.08,hspace=.56,left=.04,right=.96)
for ext in ("svg","png"):
    fig.savefig(ROOT/"figures"/("universal-annuli."+ext),dpi=180,
                metadata={"Date":None} if ext=="svg" else None)
