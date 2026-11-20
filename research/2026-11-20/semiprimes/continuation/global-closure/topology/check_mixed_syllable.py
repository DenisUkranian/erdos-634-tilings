#!/usr/bin/env python3
"""Exact local bank controls for a mixed torsion syllable; not full tilings."""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json
import sys


def cross(a, b):
    return a[0]*b[1]-a[1]*b[0]


def sub(a, b):
    return a[0]-b[0], a[1]-b[1]


def dot(a, b):
    return a[0]*b[0]+(a[0]*b[1]+a[1]*b[0])/2+a[1]*b[1]


def overlap(a, b):
    for p, q in ((a,b),(b,a)):
        for u,v in zip(p,p[1:]+p[:1]):
            if all(cross(sub(v,u),sub(w,u)) <= 0 for w in q):
                return False
    return True


def reduce_word(word, modulus):
    stack=[]
    for axis,n in word:
        n %= modulus
        if not n:
            continue
        if stack and stack[-1][0] == axis:
            n=(stack.pop()[1]+n)%modulus
        if n:
            stack.append((axis,n))
    return stack


def group_word(a,b,c,steps):
    s=b*pow(c,-1,a)%a
    assert s*s%a == 1
    word=[]
    for h,j in steps:
        k=(h+j)%6
        word.append((k%3,(-1 if k>=3 else 1)*c*pow(s,h,a)))
    return reduce_word(word,a)


def record(Geometry,a,b,c,m):
    g=Geometry(a,b,c)
    def pt(p):
        return F(p[0],c**p[2]),F(p[1],c**p[2])
    def linear_iso(p):
        conjugate=(p[0]+p[1],-p[1],p[2])
        return g.scale(-1,g.mult(g.unit(2,1),conjugate))
    out=[]
    for name,steps in (
        ('one_switch',[(1,5)]*m+[(2,4)]*m),
        ('alternating',[(1,5),(2,4)]*m),
    ):
        u=(0,0,0)
        tiles=[]
        vertices=[u]
        for h,j in steps:
            short,s=(2,-1) if h==1 else (1,1)
            q=g.add(u,g.scale(a,g.unit(short,j)))
            tile=(q,short,j,s)
            v=g.add(u,g.scale(c,g.unit(h,j)))
            assert set(g.vertices(tile)) == {
                q,u,v
            }
            tiles.append(tile)
            vertices.append(v)
            u=v
        polygons=[[pt(v) for v in g.vertices(t)] for t in tiles]
        assert all(sum(cross(u,v) for u,v in zip(p,p[1:]+p[:1]))==a*b
                   for p in polygons)
        conflicts=[(i,j) for i in range(len(polygons)) for j in range(i)
                   if overlap(polygons[i],polygons[j])]
        increments=[sub(pt(v),pt(u)) for u,v in zip(vertices,vertices[1:])]
        direction=tuple(increments[0][i]+increments[-1][i] for i in (0,1))
        assert all(dot(v,direction)>0 for v in increments)
        # Map the path frame isometrically to the canonical board frame,
        # then translate the complete bank patch into the board if possible.
        transformed=[[pt(linear_iso(v)) for v in g.vertices(t)] for t in tiles]
        minx=min(v[0] for p in transformed for v in p)
        miny=min(v[1] for p in transformed for v in p)
        shifted=[[(v[0]-minx,v[1]-miny) for v in p] for p in transformed]
        cap=max(g.B*v[0]+g.A*v[1] for p in shifted for v in p)
        fits=cap <= g.A*g.B
        word=group_word(a,b,c,steps)
        assert word == []
        out.append({
            'order':name,'steps':steps,'tiles':len(tiles),
            'positive_area_per_bank_tile':a*b,'overlap_pairs':conflicts,
            'simple_path_by_strict_projection':True,
            'fits_after_translation':fits,
            'board_capacity_used':str(cap),'board_capacity':g.A*g.B,
            'free_product_reduction':word,
            'whole_syllable_exponent':m*(b+c),
            'torsion_order':a,
            'translated_bank_triangles':[[[str(x),str(y)] for x,y in p] for p in shifted],
        })
    return {'N':g.N,'tile':[a,b,c],
            'scope':'Local simple upper-path segments and their actual bank triangles only. No tiled median region or full tiling is asserted.',
            'controls':out}


def main():
    if not __debug__:
        raise SystemExit('Run without -O.')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--continuation',type=Path,required=True)
    parser.add_argument('--known-replay',type=Path,required=True)
    parser.add_argument('--out',type=Path)
    args=parser.parse_args()
    sys.path.insert(0,str(args.continuation/'global-endpoints/integer'))
    from global_core_sat import Geometry
    actual=json.loads(args.known_replay.read_text())
    for label in ('known','macro'):
        for path in actual[label]['paths']:
            assert group_word(5,3,7,path['steps']) == [(0,49%5)]
    result={
        'known_143_ordered_words':'PASS for both actual complete controls',
        'targets':[record(Geometry,33,7,37,3),record(Geometry,35,13,43,5)],
    }
    if args.out:
        args.out.write_text(json.dumps(result,indent=2)+'\n')
    for row in result['targets']:
        for c in row['controls']:
            print(row['N'],c['order'],'overlaps',c['overlap_pairs'],
                  'fits',c['fits_after_translation'],
                  'torsion',c['whole_syllable_exponent']//c['torsion_order'])
    print(result['known_143_ordered_words'])


if __name__=='__main__':
    main()
