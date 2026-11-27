"""Test exact and relaxed marked reachability with the two complete 143 tilings."""
from math import gcd, lcm
import subprocess
import sys

from contours import SOURCE
sys.path.insert(0,str(SOURCE.parent/'joint-cell-tree'))
from controls import cell, geom, reconstruct, step


def controls(exe, exact_only=False):
    result = {}
    for name in ('known','macro'):
        g = geom.Geometry(5,3,7)
        tiles,_ = geom.read_tiles(g,name)
        polys,centres,origin,*_ = geom.check_full_tiling(g,tiles)
        matched,pairs = geom.long_pairs(g,tiles,polys,centres,origin)
        lifts,slant = reconstruct(g,tiles,polys)
        axial = slant[:1]
        ids = {axial:0}
        def label(lift):
            return ids.setdefault(lift,len(ids))
        physical = []
        for i,tile in enumerate(tiles):
            if i not in matched:
                v = lifts[i]
                long = step(v,cell(g,tile[1]+tile[3],g.vertices(tile)[-1]))
                physical.append((polys[i],label(v),label(long)))
        for i,j in pairs:
            assert lifts[i]==lifts[j]
            h = label(lifts[i])
            physical.append((polys[i]+[polys[j][1]],h,h))
        size = lcm(*(v.denominator for poly in polys for p in poly for v in p))
        shapes = [([(int(x*size),int(y*size)) for x,y in poly],h,k)
                  for poly,h,k in physical]
        den = 2
        sites = [set(),set(),set()]
        for poly,h,k in shapes:
            for (x,y),(u,v) in zip(poly,poly[1:]+poly[:1]):
                dx,dy = u-x,v-y
                div = gcd(dx,dy)
                for j,(pos,delta) in enumerate([(x,dx),(-y,-dy),(-x-y,-dx-dy)]):
                    sites[j].add(pos)
                    if delta:
                        den = lcm(den,2*abs(delta)//div)
        lines = [(j,2*x+1) for j,coords in enumerate(sites) for x in sorted(coords)[:-1]]
        board = [(0,0,0),(size*g.A,0,label(slant)),(0,size*g.B,0)]
        counts = {}
        for wildcard in ((False,) if exact_only else (False,True)):
            tag = (lambda h:int(h!=0)) if wildcard else (lambda h:h)
            # In the relaxed test erase interiors wholly beyond the axial lift.
            trial = [(poly,tag(h),tag(k)) for poly,h,k in shapes
                     if not wildcard or h==0 or k==0]
            data = [den,3,len(trial),int(wildcard)]
            for x,y,h in board:
                data += [x,y,tag(h)]
            for poly,h,k in trial:
                data += [len(poly),h,k,*(z for p in poly for z in p)]
            data += [len(lines),*(v for line in lines for v in line)]
            proc = subprocess.run([str(exe),'controls'],input=' '.join(map(str,data)),
                                  capture_output=True,text=True,check=True)
            assert int(proc.stdout)==len(lines)
            counts['relaxed' if wildcard else 'exact'] = len(trial)
        result[name] = dict(sections=len(lines),retained_objects=counts)
    return result
