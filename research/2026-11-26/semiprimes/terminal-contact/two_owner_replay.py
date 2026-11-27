"""Replay the two-owner group and position tests."""
from collections import Counter
from pathlib import Path
import json
import sys

from middle_pairs import valid
from native_positions import main as paired_cuts
from two_bank_words import census, evaluate



def control(which):
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'charge-variation'))
    from verify import cell,geom,reconstruct,step
    g=geom.Geometry(5,3,7)
    tiles,_=geom.read_tiles(g,which)
    polys,centres,centre,*_=geom.check_full_tiling(g,tiles)
    paired,_=geom.long_pairs(g,tiles,polys,centres,centre)
    lifts,T=reconstruct(g,tiles,polys)
    B,C=T[:-1],T[:1]
    origin=g.scale(g.B,g.unit(2,0))
    def chart(p):
        reflected=g.sub(origin,g.mult(g.unit(2,1),(p[0]+p[1],-p[1],p[2])))
        return g.mult(reflected,g.unit(-1,0))
    counts=Counter()
    for i,tile in enumerate(tiles):
        v=lifts[i]
        w=step(v,cell(g,tile[1]+tile[3],g.vertices(tile)[-1]))
        for gate,s in ((C,1),(T,-1)):
            if {v,w}!={B,gate} or i in paired:
                continue
            p,apex,q=map(chart,g.vertices(tile))
            # Chart reflection reverses CCW. Travel on the O-to-D path
            # reverses the reflected CCW long edge on the selected side.
            if (v==B)==(s==1):
                p,q=q,p
            intrinsic=s if v==B else -s
            delta=g.mult(g.unit(-intrinsic,0),g.sub(q,p))
            assert g.scale(g.c,g.sub(apex,p))==g.scale(g.a,delta)
            counts['axial' if s==1 else 'slant']+=1
    return dict(counts)


def two_gate_offsets():
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'axial-reserve'))
    from reserve import gate
    records=json.loads(Path(__file__).with_name('two_gate_potentials.json').read_text())
    remaining=set(range(1,38))
    for rec in records:
        first,_,den=gate(33,7,37,rec)
        remaining={k for k in remaining if 26*(first-rec['table'][111+k])<=74*den}
    assert remaining=={3,4,30}
    return sorted(remaining)


def replay(a,b,c):
    good=paired_cuts(a,b,c)
    before=Counter()
    surviving=Counter()
    for C,T in good:
        delta,rem=divmod(C[0]-T[0],c)
        assert not rem
        before[delta]+=1
        if delta==2 and valid(a,b,c,C,T)<3:
            continue
        surviving[delta]+=1
    assert 2 in before and 2 not in surviving
    return dict(remote_positive_area_words=census(a,b,c),native_pairs_by_middle_blocks=dict(sorted(before.items())),
                after_single_lift_test_at_two_blocks=dict(sorted(surviving.items())))


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Enable assertions.')
    out={str(c):replay(a,b,c) for a,b,c in ((33,7,37),(35,13,43))}
    assert evaluate(35,13,43,[0]+[1]*6,[1]*6+[0])==(86,16)
    out['central_two_gate_labels_3431']=two_gate_offsets()
    out['controls_143']={s:control(s) for s in ('known','macro')}
    print(json.dumps(out,indent=2))
