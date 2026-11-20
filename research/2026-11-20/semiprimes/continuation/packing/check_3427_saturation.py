"""An exact inradius bound for both holes of the 3427 packing."""
import json
from math import ceil
from fractions import Fraction as F
from pathlib import Path
from check_3427 import in_pentagon
from check_boards import contained
from packing_replay import edges,area

L=37*64
R2=(19*L//8)**2

def distances(polygon):
    records=[]
    for (x,y),(u,v) in edges(polygon):
        a,b=u-x,v-y
        records.append((x,y,u,v,a,b,a*a+a*b+b*b))
    return records

def sq(x,y):
    return x*x+x*y+y*y

def near_obstacle(x,y,bounds,es):
    left,right,low,high=bounds
    if not(left<=x<=right and low<=y<=high):
        return False
    inside=True
    for ax,ay,bx,by,a,b,n in es:
        dx,dy=x-ax,y-ay
        cross=a*dy-b*dx
        if cross<0:
            inside=False
        projected=(2*a+b)*dx+(2*b+a)*dy
        if projected<0:
            near=sq(dx,dy)<=R2
        elif projected>2*n:
            near=sq(x-bx,y-by)<=R2
        else:
            near=3*cross*cross<=4*n*R2
        if near:
            return True
    return inside

def run():
    from check_boards import HERE as folder
    cert=Path(__file__).with_name('pentagon14.json')
    tiles=in_pentagon(json.loads(cert.read_text()))
    obs=[]
    for tri in tiles:
        center=[sum(p[i] for p in tri)/3 for i in (0,1)]
        # Move each vertex slightly inward. Exact containment certifies that
        # these inexpensive integer triangles really lie in the placed tile.
        inner=[tuple(round((F(999,1000)*x+F(1,1000)*m)*L) for x,m in zip(p,center)) for p in tri]
        assert area(inner)>0 and contained([(F(x,L),F(y,L)) for x,y in inner],tri)
        xx,yy=zip(*inner)
        # At distance <=19/8 both axial coordinate offsets are <3.
        bounds=min(xx)-3*L,max(xx)+3*L,min(yy)-3*L,max(yy)+3*L
        obs.append((bounds,distances(inner)))
    rows=(folder/'remaining_region.txt').read_text().splitlines()
    v=list(map(int,rows[1].split()[1:]))
    hull=[(x*64,y*64) for x,y in zip(v[::2],v[1::2])]
    es=distances(hull)
    assert area(hull)>0
    xx,yy=zip(*hull);step=L//4
    checked=0
    for i in range(min(xx)//step,ceil(F(max(xx),step))+1):
        x=i*step
        for j in range(min(yy)//step,ceil(F(max(yy),step))+1):
            y=j*step;checked+=1
            # One of the closed outside half-planes is within 19/8.
            covered=False
            for ax,ay,bx,by,a,b,n in es:
                cross=a*(y-ay)-b*(x-ax)
                if cross<=0 or 3*cross*cross<=4*n*R2:
                    covered=True;break
            assert covered or any(near_obstacle(x,y,bd,edges_) for bd,edges_ in obs)
    assert 19**2 < 3*11**2  # 19/8 + sqrt(3)/8 < 3 sqrt(3)/2
    print(checked,'quarter-grid sample points covered; both holes admit no further tile.')

if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    run()
