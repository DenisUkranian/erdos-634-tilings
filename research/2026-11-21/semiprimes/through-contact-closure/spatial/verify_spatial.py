#!/usr/bin/env python3
"""Independent rational checks of the optional interior-point cuts."""
from collections import defaultdict
from fractions import Fraction as F
import json
from pathlib import Path

from spatial_search import core, grid_points


HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'CONTRIBUTING.md').exists())


def expected_points(g,tile,step):
    pts=tuple((F(x,g.c**e),F(y,g.c**e)) for x,y,e in g.vertices(tile))
    def interior(x,y):
        return all((u-x0)*(y-y0)-(v-y0)*(x-x0)>0
                   for (x0,y0),(u,v) in zip(pts,pts[1:]+pts[:1]))
    result=set()
    for ix in range(int(min(x for x,y in pts)//step),int(max(x for x,y in pts)//step)+1):
        for iy in range(int(min(y for x,y in pts)//step),int(max(y for x,y in pts)//step)+1):
            if interior(ix*step,iy*step):result.add((ix*step,iy*step))
    return result


def main():
    source=ROOT/'research/2026-11-20/semiprimes/continuation/global-endpoints/tiling_143.json'
    raw=json.loads(source.read_text())
    g=core.Geometry(*raw['sides'])
    groups=defaultdict(list)
    checks=0
    for i,(q,h,j,s) in enumerate(raw['tiles']):
        tile=tuple(q),h,j,s
        for step in (1,2,3):
            actual=set(grid_points(g,tile,step))
            assert actual==expected_points(g,tile,step)
            checks+=1
            if step==1:
                for point in actual:groups[point].append(i)
    assert all(len(ids)==1 for ids in groups.values())
    high_denominator_checks=0
    for h in (-7,-3,0,3,7):
        for j in range(6):
            for s in (-1,1):
                tile=((18,17,0),h,j,s)
                assert set(grid_points(g,tile,1))==expected_points(g,tile,1)
                high_denominator_checks+=1
    report=dict(status='PASS',rational_grid_enumeration_checks=checks,
                arbitrary_height_and_denominator_checks=high_denominator_checks,
                actual_143_unique_interior_points=len(groups),
                actual_143_point_clique_violations=0,
                scope='Necessary interior-point exclusions only; no grid restriction on tiles and no target exclusion.')
    (HERE/'SPATIAL_REPLAY.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
