"""Run with the existing windmill certificate directory, which provides ears.cpp and local/cases*.json."""
from collections import Counter
from functools import cache
from fractions import Fraction as F
from pathlib import Path
import json
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
BASE = Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT.parent
sys.path.insert(0,str(BASE))
from replay import angle, arc, polygon_key


def replay(ears, rings, work, a, b, c, board, expected, saved_ears=None, shards=4):
    N=(a+2*b)*(2*a+b)
    @cache
    def unit(h,j):
        u,v = (F(a,c),F(b,c)) if h>=0 else (F(a+b,c),F(-b,c))
        x,y=1,0
        for _ in range(abs(h)): x,y=x*u-y*v,x*v+y*(u+v)
        for _ in range(j%6): x,y=-y,x+y
        return x,y
    @cache
    def area(s):
        x=y=ar=0
        for l,h,j in s:
            u,v=unit(h,j)
            dx,dy=l*u,l*v
            ar+=x*dy-y*dx
            x+=dx
            y+=dy
        assert (x,y)==(0,0)
        val=F(ar,a*b)
        assert val>0 and val.denominator==1
        return int(val)
    budget=area(board)
    spec=f'{a} {b} {c} {len(board)} 4\n'+''.join(f'{l} {h} {j}\n' for l,h,j in board)
    if saved_ears:
        raw=saved_ears
    else:
        raw=work/'outer.txt'
        with raw.open('w') as out:
            for i in range(shards):
                subprocess.run([ears,str(shards),str(i)],input=spec,text=True,stdout=out,check=True)
    results=subprocess.run([rings,str(a),str(b),str(c),str(budget),str(raw)],capture_output=True,text=True,check=True)
    print(results.stderr.strip(),flush=True)
    rows=[list(map(int,line.split())) for line in results.stdout.splitlines()]
    indexed={t for r in rows for t in r[1:1+r[0]]}
    outer={}
    with raw.open() as src:
        i=0
        for l in src:
            if not l.strip() or l.startswith('C'):continue
            if i in indexed:
                _,_,_,k,t,L,h,j,k2,t2,L2,h2,j2=map(int,l.split())
                start=(k,t,h,j)
                end=(k2,t2,h2,j2)
                sides=arc(board,start[:2],end[:2])+[(L2,h2,j2),(L,h,(j+3)%6)]
                if all(angle(sides[i-1],s) is not None for i,s in enumerate(sides)):
                    outer[i]=(end,polygon_key(sides))
            i+=1
    layouts=set()
    for row in rows:
        k=row[0]
        assert len(row)==2*k+2
        ids=row[1:1+k]
        if any(i not in outer for i in ids):continue
        verts=[outer[i][0] for i in ids]
        core=tuple((abs(l),v[2],(v[3]+3*(l<0))%6) for l,v in zip(row[1+k:-1],verts))
        assert area(core)==row[-1] and all(angle(core[i-1],s) is not None for i,s in enumerate(core))
        cells=tuple(sorted([outer[i][1] for i in ids]+[polygon_key(core)],key=lambda s:(area(s),s)))
        assert sum(map(area,cells))==budget
        layouts.add(cells)
    hist=dict(sorted(Counter(len(f)-1 for f in layouts).items()))
    assert hist==expected,(hist,expected)
    print('Cap or board area',budget,'distinct shape multisets by central side count',hist,flush=True)
    if len(board)==3 and all(l==2*a*b for l,_,_ in board):
        cases=json.loads((BASE/'local'/f'cases_{N}.json').read_text())
        exclusions={polygon_key(list(map(tuple,s))) for (_,s),_ in cases}
        if N==5063:
            exclusions.add(polygon_key(((455,0,0),(43,-1,2),(420,0,2),(468,0,4))))
        assert all(exclusions.intersection(S) for S in layouts)
        print('All',len(layouts),'layouts contain a locally excluded cell.',flush=True)


if __name__=='__main__':
    if not __debug__:raise SystemExit('Run with assertions enabled.')
    with tempfile.TemporaryDirectory() as temp:
        work=Path(temp)
        ears,rings=work/'ears',work/'rings'
        for exe,src in ((ears,BASE/'ears.cpp'),(rings,ROOT/'rings.cpp')):
            subprocess.run(['c++','-std=c++20','-O3',str(src),'-o',str(exe)],check=True)
        for a,b,c,expect in [(33,7,37,{3:35,4:40}),(35,13,43,{3:137,4:440})]:
            side=2*a*b
            replay(ears,rings,work,a,b,c,((side,0,0),(side,0,2),(side,0,4)),expect)

        if '--boards' in sys.argv:
            for a,b,c,counts in [
                (33,7,37,{3:111,4:950,5:642,6:232,7:3}),
                (35,13,43,{3:200,4:1603,5:962,6:509,7:77}),
            ]:
                board=((b*(2*a+b),0,0),(c*c,2,1),(a*(a+2*b),0,4))
                replay(ears,rings,work,a,b,c,board,counts,shards=16)
