"""Rebuild all finite contours, section certificates and complete-tiling controls."""
from collections import Counter
from math import gcd, lcm
from pathlib import Path
import json
import subprocess
import sys
from tempfile import TemporaryDirectory

from contours import HERE, SOURCE, cases


def compile_cpp(src, dst):
    subprocess.run(['c++','-O3','-std=c++17',str(src),'-o',str(dst)],check=True)


def run(command, data):
    return subprocess.run(list(map(str,command)),input=data,capture_output=True,
                          check=True,text=True).stdout


def controls(exe):
    sys.path.insert(0,str(SOURCE/'attached'))
    from section_control import geom, check
    answers = {}
    for name in ('known','macro'):
        independent = check(name)
        g = geom.Geometry(5,3,7)
        tiles,_ = geom.read_tiles(g,name)
        polys,centres,origin,*_ = geom.check_full_tiling(g,tiles)
        matched,pairs = geom.long_pairs(g,tiles,polys,centres,origin)
        shapes = [p for i,p in enumerate(polys) if i not in matched]
        shapes += [polys[i]+[polys[j][1]] for i,j in pairs]
        size = lcm(*(v.denominator for p in polys for point in p for v in point))
        shapes = [[(int(x*size),int(y*size)) for x,y in poly] for poly in shapes]
        denominator = 2
        for poly in shapes:
            for (u,v),(x,y) in zip(poly,poly[1:]+poly[:1]):
                dx,dy = x-u,y-v
                div = gcd(dx,dy)
                for step in (dx,dy,dx+dy):
                    if step:
                        denominator = lcm(denominator,2*abs(step)//div)
        board = [(0,0),(size*g.A,0),(0,size*g.B)]
        tokens = [denominator,len(board),len(shapes),*(z for p in board for z in p)]
        for poly in shapes:
            tokens.extend([len(poly),*(z for p in poly for z in p)])
        actual = list(map(int,run([exe,'--control'],' '.join(map(str,tokens))).split()))
        assert actual == independent['sections']
        answers[name] = independent
    return answers


def target(join,exe,sides):
    a,b,c = sides
    records = []
    for kind,word,polygon in cases(join,sides):
        row = dict(family=kind,contact=len(word),far_owners=sum(j<6 for j in word),
                   word=list(word))
        if polygon is None:
            row['rejection'] = 'overlapping prescribed owners'
        else:
            row['residual'] = polygon
            data = ' '.join(map(str,[len(polygon),int(kind=='two_owner'),
                                      *(z for p in polygon for z in p)]))
            trials = [tuple(map(int,line.split()))
                      for line in run([exe,a,b,c],data).splitlines()]
            assert [(h,t) for h,t,_,_ in trials] == [(h,t) for h in (-1,1) for t in range(c)]
            counts = Counter(outcome for _,_,outcome,_ in trials)
            assert not set(counts)-{1,2}
            row.update(section_disconnections=counts[1],child_capacity_failures=counts[2],
                       maximum_number_of_probes=max(step for _,_,_,step in trials))
        records.append(row)
    return records


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Enable assertions.')
    with TemporaryDirectory() as d:
        join,exe = Path(d)/'join',Path(d)/'slices'
        compile_cpp(SOURCE/'word_join.cpp',join)
        compile_cpp(HERE/'slices.cpp',exe)
        result = {'original_status':{'3431':'OPEN','5063':'OPEN'},'control143':controls(exe)}
        for sides in [(33,7,37),(35,13,43)]:
            a,b,c = sides
            result[str((2*a+b)*(a+2*b))] = target(join,exe,sides)
        print(json.dumps(result,indent=2))
