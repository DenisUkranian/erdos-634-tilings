"""Plot verified axial coordinates; the irrational scale is used only for display."""
import json
from math import sqrt
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.patches import Polygon, Rectangle

here = Path(__file__).resolve().parent
raw = json.loads((here.parent/"audit"/"transfer280"/"packing277.json").read_text())
den = raw["denominator"]
def cart(points):
    return [(x/den,sqrt(2)*y/den) for x,y in points]
tiles = [cart(triangle) for triangle in raw["tiles_scaled"]]
hole = cart([(630,180),(720,180),(690,240),(648,216),(645,210),(699,210)])
fig,(all_tiles,detail) = plt.subplots(1,2,figsize=(10.4,4.3),gridspec_kw={"width_ratios":[1.53,1]},layout="constrained")
for ax in (all_tiles,detail):
    ax.add_collection(PolyCollection(tiles,facecolors=["#d9e6e8"]*100+["#e4ebf3"]*177,
                                     edgecolors="#627582",linewidths=0.45))
    ax.add_patch(Polygon(hole,facecolor="#fae6af",edgecolor="#9d5a23",linewidth=1.25))
    ax.set_aspect("equal")
    ax.axis("off")
all_tiles.set_xlim(-2,142);all_tiles.set_ylim(-1,58)
all_tiles.add_patch(Polygon(cart(raw["target_scaled"]),fill=False,edgecolor="#263747",linewidth=1.2))
all_tiles.add_patch(Rectangle((67.5,25.5),15.5,15,fill=False,edgecolor="#664d3e",linestyle="--",linewidth=.9))
detail.set_xlim(67.5,83);detail.set_ylim(25.5,40.5)
a,b=hole[3:5]
detail.plot([a[0],b[0]],[a[1],b[1]],color="#a42128",linewidth=3,solid_capstyle="round")
detail.annotate("Length 1",xy=((a[0]+b[0])/2,(a[1]+b[1])/2),xytext=(68.2,37.7),
                arrowprops={"arrowstyle":"-","color":"#751923","lw":1},fontsize=10,color="#751923")
all_tiles.set_title("277 congruent tiles in the 280 target",loc="left",fontsize=12,fontweight="bold")
detail.set_title("Remaining hexagon",loc="left",fontsize=12,fontweight="bold")
fig.savefig(here/"packing277.png",dpi=165,bbox_inches="tight",facecolor="white")
