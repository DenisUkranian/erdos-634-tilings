"""Verify the reference packing, reconstruct the paired hull input, and check nesting."""
from collections import defaultdict
from pathlib import Path
import sys

base = Path(__file__).resolve().parent
arguments = iter(map(int, (base/'reference.txt').read_text().split()))
a,b,c,total = (next(arguments) for _ in range(4))
assert (a,b,c,total) == (35,13,43,5059)
unit = a*b*c*c

def edges(p): return zip(p, p[1:]+p[:1])
def cross(p,q,r): return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
def area(p): return sum(x*v-y*u for (x,y),(u,v) in edges(p))
def norm(p,q):
    x,y=q[0]-p[0],q[1]-p[1]
    return x*x+x*y+y*y

def positive(p): return p if area(p)>0 else p[::-1]
def inside(q,p): return all(cross(x,y,z)>=0 for x,y in edges(p) for z in q)
def separated(p,q): return any(all(cross(x,y,z)<=0 for z in q) for x,y in edges(p))
def triangle(): return positive([(next(arguments),next(arguments)) for _ in range(3)])
tiles=[triangle() for _ in range(total)]
holes=[[triangle() for _ in range(next(arguments))] for _ in range(2)]
assert next(arguments,None) is None
board=[(0,0),(1079*c,0),(0,2135*c)]
for t in tiles:
    assert sorted(norm(x,y) for x,y in edges(t))==sorted((n*c)**2 for n in (a,b,c))
    assert area(t)==unit
assert [sum(map(area,h)) for h in holes]==[2*unit,2*unit]
T=(-11180,13545)
def shift(t): return [(x-T[0],y-T[1]) for x,y in t]
assert {tuple(sorted(t)) for t in holes[0]}=={tuple(sorted(shift(t))) for t in holes[1]}
allcells=tiles+holes[0]+holes[1]
assert sum(map(area,allcells))==area(board)
bins=defaultdict(list)
for i,t in enumerate(allcells):
    assert area(t)>0 and inside(t,board)
    xs,ys=zip(*t)
    nearby=set()
    for ix in range(min(xs)//2000,max(xs)//2000+1):
        for iy in range(min(ys)//2000,max(ys)//2000+1):
            box=bins[ix,iy];nearby.update(box);box.append(i)
    for j in nearby: assert separated(t,allcells[j]) or separated(allcells[j],t)
print('Verified 5059 congruent reference tiles and two congruent two-tile holes.')
if sys.argv[1]=='prepare':
    both={tuple(sorted(t)):t for t in tiles+[shift(t) for t in tiles]};points=sorted({p for t in holes[0] for p in t})
    with open(sys.argv[2],'w') as f:
        print(len(both),file=f)
        for t in both.values(): print(*(v for p in t for v in p),file=f)
        print(len(points),*(v for p in points for v in p),file=f)
    sys.exit(0)
assert sys.argv[1]=='check'
rows=[]
for line in Path(sys.argv[2]).read_text().splitlines():
    mass,vertices,*xy=map(int,line.split());p=list(zip(xy[::2],xy[1::2]));assert len(p)==vertices and area(p)==mass*unit
    assert all(inside(t,p) for t in holes[0]);rows.append((mass,p))
assert len(rows)==len({tuple(p) for _,p in rows})
for j in (1,2,3,4):
    p=positive([(22360,(4-j)*1849),(22360,13545),(35217,13545),(36465,12635),(36465+j*455,12635-j*1680)])
    mass=area(p)//unit;local=[t for t in tiles if inside(t,p)]
    assert all(inside(t,p) for t in holes[0]) and len(local)*unit+2*unit==area(p)
    count=0
    for n,q in rows:
        if inside(q,p):
            assert sum(inside(t,q) for t in local)==n-2;count+=1
    print(f'{j} row(s): area {mass}, contains {count} of {len(rows)} enumerated cavities.')
    if j==3:assert count==len(rows)
