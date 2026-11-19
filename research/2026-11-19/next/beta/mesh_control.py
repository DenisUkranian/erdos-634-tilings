"""Replay outward-rounded vertex stars on 1475 actual tiles, including non-grid anchors."""
from fractions import Fraction as F
from pathlib import Path
import json
from mesh_stars import Mesh,fl
from vertex_stars import Model,add,mul,sc as scale,sub,cross,norm

def grid_cells(block):
    points=[tuple(F(*a) for a in v) for v in block["vertices"]]
    origin=points[0]
    triangular=block["type"]=="triangle_grid"
    rows=block["n"] if triangular else block["rows"]
    cols=rows if triangular else block["columns"]
    u=scale(F(1,rows),sub(points[1],origin))
    v=scale(F(1,cols),sub(points[-1],origin))
    def site(i,j):return add(origin,add(scale(i,u),scale(j,v)))
    for i in range(rows):
        for j in range(rows-i if triangular else cols):
            a,b,c=site(i,j),site(i+1,j),site(i,j+1)
            if not triangular and block["diagonal"]=="sum":
                yield a,b,site(i+1,j+1)
                yield a,c,site(i+1,j+1)
            else:
                yield a,b,c
                if not triangular or i+j+1<rows:yield site(i+1,j+1),b,c

doc=json.loads(Path(__file__).with_name("control1475-blocks.json").read_text())
converter=lambda q:(q[0],2*q[1])
target=[converter(tuple(F(*c) for c in p)) for p in doc['target']]
if cross(sub(target[1],target[0]),sub(target[2],target[0]))<0:target.reverse()
p,q=max(zip(target,target[1:]+target[:1]),key=lambda e:norm(sub(e[1],e[0])))
u=scale(F(1,1180),sub(q,p));inv=(u[0],-u[1])
align=lambda p0:mul(sub(converter(p0),p),inv)
orient=Model(-2,2,5)
tiles=[]
for block in doc['blocks']:
    for tile in grid_cells(block):
        t=[align(v) for v in tile]
        vs=[scale(orient.d,v) for v in t]
        assert all(z.denominator==1 for point in vs for z in point)
        loc,=orient.entry([(int(x),int(y)) for x,y in vs])
        k,x,y=loc
        tiles.append((orient.shapes[k],(F(x,orient.d),F(y,orient.d)),(F(0),F(0)) in t))
assert len(tiles)==1475 and sum(v[2] for v in tiles)==1
report=[]
for Q in [7,11,25]:
    m=Mesh(2,Q,5)
    cells=[(m.shapes.index(s),*fl(scale(Q,p)),z) for s,p,z in tiles]
    assert len(cells)==len(set((k,x,y) for k,x,y,_ in cells))
    assert all(m.pos[k][y]>>x&1 for k,x,y,_ in cells)
    off_grid=sum(any((v*Q).denominator!=1 for v in p) for s,p,_ in tiles)
    m.pos=[[0]*m.h for _ in m.shapes]
    for k,x,y,_ in cells:m.pos[k][y]|=1<<x
    dead=m.turn()
    assert not dead and m.count()==1475
    for k,x,y,is_corner in cells:
        if is_corner:m.pos[k][y]&=~(1<<x)
    dead=m.turn()
    assert (0,0) in dead
    report.append({'Q':Q,'specified_placements':len(cells),'off_grid_anchor_count':off_grid,
                   'survivors_with_complete_witness':1475,
                   'absent_origin_after_corner_tile_removed':True})
print(json.dumps(report,indent=2))
