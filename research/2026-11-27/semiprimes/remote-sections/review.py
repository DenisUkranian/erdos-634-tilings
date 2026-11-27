"""Independent Fraction/NumPy audit of selected lattices; --all checks every lattice."""
import argparse
from collections import Counter
import json
import sys

import numpy as np

from contours import HERE, SOURCE, repair
sys.path.insert(0,str(SOURCE/'attached'))
from sections import objects, rotate, section


def probes(polygon,c,dense):
    axes = []
    for axis in range(3):
        coords = sorted(set(rotate(polygon,axis)[0].tolist()))
        axes.append([2*x+1 for x in coords[:-1]]+[2*x-1 for x in coords[:0:-1]])
    lines = [(j,axis[i]) for i in range(max(map(len,axes)))
             for j,axis in enumerate(axes) if i<len(axis)]
    if dense:
        for j,axis in enumerate(axes):
            left,right = axis[0],max(axis)
            while left<right:
                lines.extend([(j,left),(j,right)])
                left,right = left+6*c,right-6*c
    return lines


def check(record,sides,all_lattices):
    a,b,c = sides
    corners = repair(record['word'],*sides)
    if corners is None:
        assert 'rejection' in record
        return Counter()
    assert [list(p) for p in corners]==record['residual']
    poly = c*np.array(corners,dtype=np.int64)
    B = objects(poly,0,0,sides)
    lines = probes(poly,c,record['family']=='two_owner')
    counts = Counter()
    lattices = [(h,t) for h in (-1,1) for t in range(c)] if all_lattices else [(-1,0)]
    for h,t in lattices:
        C = objects(poly,h,t,sides)
        shapes = np.concatenate((B['pairs'],B[h,t],C['pairs'],C['singles']))
        for axis,pos in lines*3:
            shapes = section(poly,shapes,axis,pos)
            if shapes is None:
                counts['section_disconnections']+=1
                break
            # Read hand-lattice membership anew from the first short edge.
            child = shapes[np.any((shapes[:,1]-shapes[:,0])%c!=0,axis=1)]
            pairs = np.any(child[:,0]!=child[:,3],axis=1)
            if len(child)+np.count_nonzero(pairs)<2*c:
                counts['child_capacity_failures']+=1
                break
        else:
            raise AssertionError((h,t,record['word']))
    for key,n in counts.items():
        assert (n==record[key] if all_lattices else 0<n<=record[key])
    return counts


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Enable assertions.')
    parser = argparse.ArgumentParser()
    parser.add_argument('--all',action='store_true')
    parser.add_argument('--board',choices=('3431','5063'))
    args = parser.parse_args()
    data = json.loads((HERE/'RESULT.json').read_text())
    for board,sides in [('3431',(33,7,37)),('5063',(35,13,43))]:
        if args.board and args.board!=board:
            continue
        total = Counter()
        for record in data[board]:
            total.update(check(record,sides,args.all))
        print(board,dict(total),flush=True)
