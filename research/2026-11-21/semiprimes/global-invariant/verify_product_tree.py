#!/usr/bin/env python3
"""Exact replay of an auxiliary invariant and its calibration obstruction.

No solver is imported. Fractions reconstruct every projected certificate.
Nothing in this script asserts the existence or nonexistence of a target
physical tiling.
"""
from collections import Counter,defaultdict
from fractions import Fraction as F
from pathlib import Path
import json
from product_tree_probe import develop,fill,square_boundary,stats,mul
HERE=Path(__file__).resolve().parent

def gm(g,h,m):
    for i,e in h:g=mul(g,i,e,m)
    return g

def freeze(x):
    return tuple(freeze(y) for y in x) if isinstance(x,list) else x

def translated_edge(edge,g,m):
    (prefix,i),leaf=edge
    base=gm(g,prefix,m)
    star=(base[:-1] if base and base[-1][0]==i else base,i)
    return star,gm(g,leaf,m)

def tile_segments(a,b,c,h,j,s):
    if s==1:return [(a,h,j),(b,h,j+1),(c,h+1,j+3)]
    assert s==-1
    return [(b,h,j+2),(a,h,j+3),(c,h-1,j)]

def tile_fill(a,b,c,h,j,s):
    chain,boundary=develop(tile_segments(a,b,c,h,j,s),a,b,c)
    assert square_boundary(chain)==boundary
    return chain

def projection_certificate(cert):
    a,b,c=cert['tile'];A=b*(2*a+b);B=a*(a+2*b)
    board,boundary=develop([(A,0,0),(c*c,2,1),(B,0,4)],a,b,c)
    assert square_boundary(board)==boundary
    total=defaultdict(F);cost=F(0)
    for term in cert['terms']:
        h,j,s,gA,gB=freeze(term['placement'])
        weight=F(*term['weight'])
        assert weight>0
        chain=tile_fill(a,b,c,h,j,s)
        cost+=weight
        for (ea,eb),value in chain.items():
            key=(translated_edge(ea,gA,a),translated_edge(eb,gB,b))
            total[key]+=weight*value
    for key,value in board.items():assert total[key]==value,(a,b,c,key,total[key],value)
    outside={key:value for key,value in total.items() if key not in board and value}
    assert cost==F(*cert['total_cost'])
    assert outside # The certificate is deliberately only a finite projection.
    return {'tile':[a,b,c],'target_N':(a+2*b)*(2*a+b),'terms':len(cert['terms']),
            'exact_projected_cost':str(cost),'board_square_support':len(board),
            'uncontrolled_nonzero_square_count':len(outside),
            'all_weights_positive':True,'projected_equality_exact':True,
            'scope':'Upper bound on any universally valid linear tile-count calibration supported only on these board-filling squares. Not a full-chain filling or a physical tiling.'}

def controls(a,b,c):
    norm_hist=Counter();tile_checks=0
    for h in range(6):
        for j in range(6):
            for s in [-1,1]:
                chain=tile_fill(a,b,c,h,j,s)
                norm_hist[stats(chain)['norm']]+=1;tile_checks+=1
            chain,boundary=develop([(a*b,h,j)],a,b,c)
            assert chain==boundary=={}
    first=fill([(a,0,0),(b,0,1),(c,1,3)],a,b,c)
    second=fill([(c,1,0),(a,0,3),(b,0,4)],a,b,c)
    pair,boundary=develop([(a,0,0),(b,0,1),(a,0,3),(b,0,4)],a,b,c)
    assert square_boundary(pair)==boundary
    joined={k:first.get(k,0)+second.get(k,0) for k in first.keys()|second.keys()}
    assert {k:v for k,v in joined.items() if v}==pair
    opposite=sorted(k for k in first.keys()&second.keys() if first[k]*second[k]<0)
    assert opposite
    A=b*(2*a+b);B=a*(a+2*b)
    board,boundary=develop([(A,0,0),(c*c,2,1),(B,0,4)],a,b,c)
    assert square_boundary(board)==boundary
    shortened=fill([(A%(a*b),0,0),(c*c%(a*b),2,1),(B%(a*b),0,4)],a,b,c)
    assert shortened==board
    # The positive physical half-turn pair has vertices 0, a, a+b*rho,
    # b*rho. The two CCW triangle determinants are both ab.
    det=lambda p,q:p[0]*q[1]-p[1]*q[0]
    t1=((0,0),(a,0),(a,b));t2=((0,0),(a,b),(0,b))
    for tri in [t1,t2]:assert sum(det(tri[i],tri[(i+1)%3]) for i in range(3))==a*b
    assert B*a+A*b<=A*B # The entire parallelogram lies inside the target.
    return {'tile':[a,b,c],'tile_chain_boundary_checks':tile_checks,
            'zero_period_chain_checks':36,'tile_l1_norm_histogram':dict(norm_hist),
            'board_l1_norm':stats(board)['norm'],
            'positive_half_turn_pair':{
                'first_tile_l1':stats(first)['norm'],'second_tile_l1':stats(second)['norm'],
                'union_l1':stats(pair)['norm'],'opposite_square_count':len(opposite),
                'first_opposite_square':opposite[0],
                'coefficients':[first[opposite[0]],second[opposite[0]]],
                'exact_chain_addition':True,'physical_positive_area_checks':True,
                'contained_in_target':True},
            'boundary_lengths':[A,c*c,B],
            'boundary_lengths_mod_ab':[A%(a*b),c*c%(a*b),B%(a*b)],
            'period_reduced_boundary_same_filling':True}

def main():
    certs=json.loads((HERE/'projected_calibration_certificates.json').read_text())
    result={'status':'PASSED','physical_target_decisions':{'3431':'OPEN','5063':'OPEN'},
            'controls':[controls(*t) for t in [(5,3,7),(33,7,37),(35,13,43)]],
            'projected_certificates':[projection_certificate(x) for x in certs['cases']]}
    (HERE/'PRODUCT_TREE_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'projected_costs':[(x['target_N'],x['exact_projected_cost']) for x in result['projected_certificates']]},indent=2))

if __name__=='__main__':main()
