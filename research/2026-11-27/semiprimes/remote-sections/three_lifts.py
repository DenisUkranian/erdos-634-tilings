"""Exhaust the possible occupied short lifts in a 222-tile, 24-owner branch."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from itertools import combinations
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from contours import HERE, repair, two_owner_words
from replay import compile_cpp, run

SIDES = 33,7,37
LABELS = range(74)


def coordinates(polygon):
    return ' '.join(str(v) for p in polygon for v in p)


def batch(exe,mode,header,cases):
    lines = [header]+[' '.join(map(str,row)) for row in cases]
    out = [tuple(map(int,line.split())) for line in
           run([exe,mode],'\n'.join(lines)+'\n').splitlines()]
    assert [row[:3] for row in out]==cases
    return out


def trials(exe,mode,header,cases,workers):
    # Each chunk shares the geometry of its outer contour.
    chunks = [cases[i:i+80] for i in range(0,len(cases),80)]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        return [row for group in pool.map(lambda chunk:batch(exe,mode,header,chunk),chunks)
                for row in group]


def check(two,three,word,workers):
    polygon = repair(word,*SIDES,blocks=6)
    assert polygon is not None
    low = sum(j<6 for j in word)
    header = f'{len(polygon)} {74-low} {coordinates(polygon)}'
    # With two occupied lifts the child can have 74 or 148 tiles.
    twodata = f'{len(polygon)} 1 {coordinates(polygon)}'
    results = [tuple(map(int,x.split())) for x in run([two,*SIDES],twodata).splitlines()]
    assert [(h,t) for h,t,_,_ in results]==[(h,t) for h in (-1,1) for t in range(37)]
    assert all(result in (1,2) for _,_,result,_ in results)

    # One root neighbor and arbitrary deeper material, or two root neighbors.
    representatives = [(1,g,-1) for g in LABELS]+[(0,g,k) for g,k in combinations(LABELS,2)]
    first = trials(three,'open',header,representatives,workers)
    counts = Counter((s,result) for s,g,k,result in first)
    rest = []
    for s,g,k,result in first:
        if not result:
            rest.extend([(1,g,t) for t in LABELS] if s else [(0,g,k)])
    second = trials(three,'exact',header,rest,workers)
    final = Counter((s,result) for s,g,k,result in second)
    def histogram(count):
        return [[topology,outcome,n] for (topology,outcome),n in sorted(count.items())]
    return dict(word=word,far_owners=low,residual=polygon,
                two_lift_outcomes=sorted(Counter(t[2] for t in results).items()),
                relaxed_three_lift_outcomes=histogram(counts),
                exact_three_lift_outcomes=histogram(final),
                unresolved=[list(row[:3]) for row in second if row[3]==0])


def coordinate_controls(exe):
    from controls_marked import controls
    return controls(exe)


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Enable assertions.')
    parser = argparse.ArgumentParser()
    parser.add_argument('--workers',type=int,default=1)
    args = parser.parse_args()
    words = sorted(w for w in two_owner_words(*SIDES,blocks=6) if len(w)==24)
    assert len(words)==2
    with TemporaryDirectory() as d:
        two,three = Path(d)/'slices',Path(d)/'marked'
        compile_cpp(HERE/'slices.cpp',two)
        compile_cpp(HERE/'marked.cpp',three)
        print(json.dumps(dict(cases=[check(two,three,w,args.workers) for w in words],
                              control143=coordinate_controls(three)),indent=2))
