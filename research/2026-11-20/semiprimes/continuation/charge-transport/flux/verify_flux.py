#!/usr/bin/env python3
"""Exact signed transport on a verified full tiling and saved local controls.

This checks transport identities, not completion of any partial packing.
"""
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
import argparse
import json
import sys


def find_continuation():
    for ancestor in Path(__file__).resolve().parents:
        for candidate in (ancestor, ancestor/'repo/research/2026-11-20/semiprimes/continuation'):
            if (candidate/'global-endpoints/integer/global_core_sat.py').exists():
                return candidate
    raise FileNotFoundError('Pass --continuation pointing at the project continuation folder.')


def epsilon(tile):
    return tile[3]*(1 if tile[2]%2==0 else -1)


def parity(h):
    return 1 if h%2==0 else -1


def mate(g,tile):
    q,h,j,s=tile
    offset=g.add(g.scale(-g.a,g.unit(h,j)),g.scale(g.b,g.unit(h,j+s)))
    return g.add(q,offset),h,(j+3)%6,s


def chain_values(g,p,q):
    x,y,e=p;u,v,f=q
    x,y=Fraction(x,g.c**e),Fraction(y,g.c**e)
    u,v=Fraction(u,g.c**f),Fraction(v,g.c**f)
    return (u-x,v-y),x*v-y*u


def json_exact(value):
    if isinstance(value,Fraction):
        return value.numerator if value.denominator==1 else str(value)
    if isinstance(value,(list,tuple)):
        return [json_exact(x) for x in value]
    if isinstance(value,dict):
        return {k:json_exact(v) for k,v in value.items()}
    return value


def cut_data(g,budget,tiles):
    edges=defaultdict(lambda:{'P':0,'Q':0,'uP':0,'uQ':0,'tilesP':0,'tilesQ':0,
                             'vectorP':[Fraction(0),Fraction(0)],
                             'vectorQ':[Fraction(0),Fraction(0)],
                             'detP':Fraction(0),'detQ':Fraction(0)})
    selected=set(tiles)
    matched={t for t in tiles if mate(g,t) in selected}
    assert len(matched)%2==0
    node_G=Counter();node_H=Counter()
    for tile in tiles:
        q,h,j,s=tile;eps=epsilon(tile)
        endpoint=g.add(q,g.scale(-g.a,g.unit(h,j)))
        short=budget.node(q,budget.sign*h)
        long=budget.node(endpoint,budget.sign*(h+s))
        node_G[short]+=eps;node_H[long]+=eps
        if short[0]>long[0]:
            child=short;direction='P'
            assert long[0]==short[0]-1
        else:
            child=long;direction='Q'
            assert short[0]==long[0]-1
        row=edges[child]
        row[direction]+=eps
        row['tiles'+direction]+=1
        vertices=g.vertices(tile)
        vector,det=chain_values(g,vertices[-1],vertices[0])
        for axis in range(2):
            row['vector'+direction][axis]+=vector[axis]
        row['det'+direction]+=det
        if tile not in matched:
            row['u'+direction]+=1
    return edges,node_G,node_H,matched


def full_control(Geometry,PhaseBudget,continuation):
    data=json.loads((continuation/'global-endpoints/tiling_143.json').read_text())
    tiles=[(tuple(t[0]),*t[1:]) for t in data['tiles']]
    assert len(set(tiles))==len(tiles)==143
    g=Geometry(5,3,7);d=g.a-g.b
    assert sum(epsilon(t) for t in tiles)==-(g.c+d)
    assert sum(parity(t[1])*epsilon(t) for t in tiles)==g.c-d
    assert sum(epsilon(t) for t in tiles if t[1]%2)==-g.c
    output=[]
    for tree in (1,-1):
        budget=PhaseBudget(g,tree)
        edges,G,H,matched=cut_data(g,budget,tiles)
        node_b=Counter()
        outer=[]
        for wall,current in zip(g.walls(),(g.A,-g.c*g.c,g.B)):
            p,q,height,_=wall
            node=budget.node(p,tree*height)
            node_b[node]+=current
            vector,det=chain_values(g,p,q)
            outer.append((p,tree*height,current,vector,det))
        for node in G.keys()|H.keys()|node_b.keys():
            assert d*G[node]-g.c*H[node]==node_b[node]
        energy=unmatched=0;records=[]
        for child,row in edges.items():
            level=child[0];k=tree*level
            inside=[t for t in tiles if tree*t[1]>=level and budget.node(t[0],level)==child]
            gs=sum(epsilon(t) for t in inside)
            gst=sum(parity(t[1])*epsilon(t) for t in inside)
            selected_outer=[entry for entry in outer
                            if entry[1]>=level and budget.node(entry[0],level)==child]
            bsum=sum(entry[2] for entry in selected_outer)
            outer_vector=[sum(entry[3][axis] for entry in selected_outer) for axis in range(2)]
            outer_det=sum(entry[4] for entry in selected_outer)
            P,Q=row['P'],row['Q']
            assert g.c*(P-Q)==(g.c-d)*gs+bsum
            assert g.c*parity(k)*(P+Q)==(g.c+d)*gst-bsum
            for axis in range(2):
                assert row['vectorP'][axis]-row['vectorQ'][axis]==-outer_vector[axis]
            assert g.a*g.b*len(inside)==outer_det+row['detP']-row['detQ']
            e=abs(P)+abs(Q)
            assert e==max(abs(P-Q),abs(P+Q))
            assert row['uP']>=abs(P) and row['uQ']>=abs(Q)
            assert (row['uP']-P)%2==0 and (row['uQ']-Q)%2==0
            strict=e
            active=bool(inside) and budget.exterior_free(child)
            if active:
                assert row['uP']>0 and row['uQ']>0
                strict+=2*(P==0)+2*(Q==0)
            assert row['uP']+row['uQ']>=strict
            energy+=e;unmatched+=row['uP']+row['uQ']
            if P or Q:
                records.append({'child':list(child),'physical_root_height':k,
                                'subtree_tiles':len(inside),'G':gs,'G_star':gst,
                                'exterior_current':bsum,'exterior_vector':outer_vector,
                                'exterior_determinant':outer_det,**row})
        assert unmatched==143-len(matched)==23
        assert energy==3*g.c+d==23
        output.append({'tree':tree,'edge_count':len(edges),'ordinary_energy':energy,
                       'actual_unmatched':unmatched,'nonzero_cuts':records})
    return {'scope':'Signed transport, physical displacement, and area on the previously verified complete 143 tiling.',
            'long_edge_pairs':60,'unmatched':23,'trees':output}


def strip_controls(Geometry,PhaseBudget,folder):
    output=[]
    for N in (143,3431,5063):
        data=json.loads((folder/f'mixed_cycle_{N}.json').read_text())
        a,b,c=data['tile'];g=Geometry(a,b,c);budget=PhaseBudget(g,1)
        placements=data['placements']
        tiles=[(tuple(t['q']),t['h'],t['j'],t['s']) for t in placements]
        root=budget.node(tuple(data['shift']),0)
        assert budget.exterior_free(root)
        inside=[tile for tile,p in zip(tiles,placements) if p['role']=='interior']
        assert len(inside)==2*c
        assert all(budget.node(t[0],t[1])==root for t in inside)
        assert sum(epsilon(t) for t in inside)==0
        edges,G,H,matched=cut_data(g,budget,tiles)
        row=edges[root]
        assert row['P']==row['Q']==0
        assert row['uP']==2 and row['uQ']==2*a
        output.append({'N':N,'root':list(root),'P':0,'Q':0,
                       'unmatched_inside_crossing':2,'unmatched_outside_crossing':2*a,
                       'bidirectional_target_lower_bound':4 if N in (3431,5063) else None,
                       'scope':'Exact local strip cut only; no F2 completion or continued terminality asserted.'})
    return output


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--continuation',type=Path)
    p.add_argument('--patch-dir',type=Path)
    p.add_argument('--out',type=Path)
    args=p.parse_args()
    continuation=args.continuation or find_continuation()
    sys.path[:0]=[str(continuation/'global-endpoints/integer'),str(continuation/'vertex-phase')]
    from global_core_sat import Geometry
    from phase_budget import PhaseBudget
    if args.patch_dir:
        patch_dir=args.patch_dir
    else:
        candidates=[continuation/'common-obstruction/boundary',
                    Path(__file__).resolve().parents[2]/'impossibility/boundary']
        patch_dir=next(p for p in candidates if (p/'mixed_cycle_3431.json').exists())
    report={'full_143':full_control(Geometry,PhaseBudget,continuation),
            'local_balanced_strips':strip_controls(Geometry,PhaseBudget,patch_dir),
            'scope':'Necessary transport identities and geometric matching counts; neither target is decided.'}
    report=json_exact(report)
    if args.out:
        args.out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Run without -O.')
    main()
