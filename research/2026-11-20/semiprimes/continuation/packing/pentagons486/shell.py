"""Lift fillings of a family of 38 polygons to a complete 3431 tiling."""
from argparse import ArgumentParser
from fractions import Fraction
from itertools import permutations
from math import lcm
import gzip
import json
from pathlib import Path
from geometry import (boundary_identity, ccw, check_tiles, det, diff, doubled_area, edges,
                      integer_vertices, norm, scaled, simple, translated)

HERE = Path(__file__).resolve().parent
DEN = 37
SHIFT = (-4662,6105)


def add(p,q):
    return p[0]+q[0],p[1]+q[1]


def times(u,n):
    return n*u[0],n*u[1]


def grid_parallelogram(poly):
    origin=poly[0]
    v,w=diff(poly[1],origin),diff(poly[3],origin)
    assert add(origin,add(v,w))==poly[2]
    for a,b,c in permutations([7,33,37]):
        for n in range(1,100):
            if norm(v)!=(DEN*n*a)**2: continue
            for m in range(1,100):
                if norm(w)!=(DEN*m*b)**2: continue
                u=(v[0]//n,v[1]//n)
                z=(w[0]//m,w[1]//m)
                assert times(u,n)==v and times(z,m)==w
                diagonal=(DEN*c)**2
                if norm(diff(u,z))==diagonal:
                    cell=(((0,0),u,z),(add(u,z),z,u))
                elif norm(add(u,z))==diagonal:
                    cell=(((0,0),u,add(u,z)),((0,0),add(u,z),z))
                else: continue
                tiles=[]
                for i in range(n):
                    for j in range(m):
                        base=add(origin,add(times(u,i),times(z,j)))
                        tiles.extend(translated(ccw(t),base) for t in cell)
                boundary_identity(tiles,poly)
                check_tiles(tiles,DEN,2*n*m)
                return tiles
    raise ValueError('No elementary grid for these vertices.')


def family(t):
    if not 0<=t<=37: raise ValueError('The parameter t must lie between 0 and 37.')
    with gzip.open(HERE/'hex538.json.gz','rt') as stream:
        data=json.load(stream)
    outer=[ccw(integer_vertices(s)) for s in data['fixed_triangles']]
    board=integer_vertices(data['board'])
    hexagon=integer_vertices(data['polygon'])
    assert board==((0,0),(511*DEN,0),(0,1551*DEN))
    check_tiles(outer,DEN,2355)
    boundary_identity(outer+[hexagon,translated(hexagon,SHIFT)],board)
    x=14245-259*t
    polygon=[(14245,6105),(x,6105),(x,0),(18907,0),(17885,3102)]
    if t==0: polygon.pop(0)
    polygon=tuple(polygon)
    simple(polygon)
    assert all(det(diff(p,polygon[i-1]),diff(polygon[(i+1)%len(polygon)],p))>0 for i,p in enumerate(polygon))
    n=116+10*t
    assert doubled_area(polygon)==n*231*DEN**2
    added=grid_parallelogram(((14245,6105),(17885,3102),(16863,6204),(13223,9207)))
    if t<37:
        added+=grid_parallelogram(((4662,0),(x,0),(x,6105),(4662,6105)))
    boundary_identity(added+[polygon],hexagon)
    fixed=outer+added+[translated(tile,SHIFT) for tile in added]
    check_tiles(fixed,DEN,3431-2*n)
    boundary_identity(fixed+[polygon,translated(polygon,SHIFT)],board)
    return n,polygon,fixed,board


def serve(t,candidate,output,shell_output):
    n,poly,fixed,board=family(t)
    print(f't={t}, region area {n}, fixed tiles {len(fixed)}, vertices {poly}, denominator {DEN}')
    if shell_output:
        spec=dict(region_size=n,polygon=poly,fixed_triangles=fixed,shift=SHIFT,board=board,denominator=DEN,side_lengths=[7,33,37])
        with shell_output.open('x') as stream:
            json.dump(spec,stream,separators=(',',':'))
    if candidate is None:
        if output is not None:raise ValueError('Provide a candidate to export a complete board.')
        return
    data=json.loads(candidate.read_text())
    d=data['denominator'];assert type(d) is int and d>0
    common=lcm(d,DEN)
    fill=[ccw(scaled(integer_vertices(t),common//d)) for t in data['triangles']]
    check_tiles(fill,common,n)
    boundary_identity(fill,scaled(poly,common//DEN))
    shift=times(SHIFT,common//DEN)
    full=[scaled(t,common//DEN) for t in fixed]+fill+[translated(t,shift) for t in fill]
    check_tiles(full,common,3431)
    boundary_identity(full,scaled(board,common//DEN))
    print('Verified a complete 3431 tiling.')
    if output:
        with output.open('x') as stream:
            json.dump(dict(denominator=common,triangles=full),stream,separators=(',',':'))


if __name__=='__main__':
    if not __debug__:raise SystemExit('Assertions must be enabled.')
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('t',type=int)
    parser.add_argument('candidate',nargs='?',type=Path)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--shell-output',type=Path)
    args=parser.parse_args()
    serve(args.t,args.candidate,args.output,args.shell_output)
