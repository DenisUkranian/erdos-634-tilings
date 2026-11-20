#!/usr/bin/env python3
"""Two exact even-height corner tiles and primitive base-gap arithmetic.

The corner objects are partial packings, not completed F2 tilings.
"""
from pathlib import Path
from fractions import Fraction
import argparse,json,sys
from verify_actual_median import find_continuation,point,cross,sub

HERE=Path(__file__).resolve().parent
CONT=find_continuation()
sys.path.insert(0,str(CONT/'global-endpoints/integer'))
from global_core_sat import Geometry

def record(a,b,c):
    g=Geometry(a,b,c)
    # Path-frame board: O=0, B=c^2, C=a(a+2b)z^2.
    path_tiles=[((a,0,0),0,0,1),(g.scale(a,g.unit(2,0)),2,0,-1)]
    O=(0,0,0);P=g.scale(c,g.unit(1,0))
    for q,h,j,s in path_tiles:
        u=g.sub(q,g.scale(a,g.unit(h,j)))
        w=g.add(q,g.scale(b,g.unit(h,j+s)))
        assert u==O and w==P
    q0,q2=path_tiles[0][0],path_tiles[1][0]
    vec=point(g,P)
    assert cross(vec,point(g,q0))*cross(vec,point(g,q2))<0
    # The two triangles share their entire long edge and have disjoint interiors.
    standard=[]
    for q,h,j,s in path_tiles:
        qc=(q[0]+q[1],-q[1],q[2])
        qstd=g.sub((0,g.B,0),g.mult(g.unit(2,1),qc))
        tile=qstd,2-h,(4-j)%6,-s
        assert g.admissible(tile)
        vs=[point(g,v) for v in g.vertices(tile)]
        assert sum(cross(u,v) for u,v in zip(vs,vs[1:]+vs[:1]))==a*b
        standard.append([list(qstd),tile[1],tile[2],tile[3]])
    gaps=[]
    for k in range(1,c+1):
        solutions=[[m,(c*k-a*m)//b] for m in range(c*k//a+1) if (c*k-a*m)%b==0]
        if solutions:gaps.append({'k':k,'short_edge_counts':solutions})
    assert gaps
    return {'N':g.N,'tile':[a,b,c],
            'corner_scope':'Two even-height tiles strictly form a local partial packing at the path-frame O corner; no completion claimed.',
            'path_frame_short_heights':[0,2],
            'shared_long_edge':[list(O),list(P)],
            'standard_frame_placements':standard,
            'exact_containment_and_disjointness':'PASS',
            'minimum_nonzero_base_gap_multiple':gaps[0],
            'gap_scope':'Arithmetic for a gap of length kc covered only by a,b edges; geometric realizability is not asserted.'}

def main():
    if not __debug__:
        raise SystemExit('Run without -O.')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path)
    args=parser.parse_args()
    out=[record(*t) for t in ((5,3,7),(33,7,37),(35,13,43))]
    for row in out:print(json.dumps(row,sort_keys=True))
    if args.out:
        args.out.write_text(json.dumps(out,indent=2)+'\n')

if __name__=='__main__':
    main()
