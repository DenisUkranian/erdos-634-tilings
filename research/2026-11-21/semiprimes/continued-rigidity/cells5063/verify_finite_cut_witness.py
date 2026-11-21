#!/usr/bin/env python3
"""Exact independent replay of the two-cell finite-cut-pool current witness."""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'research').is_dir() and (p/'scripts').is_dir())
INDEX=ROOT/'research/2026-11-21/semiprimes/gate-model/CERTIFICATES_5063.json'


def main():
    a,b,c=35,13,43
    data=json.loads((HERE/'TWO_CELL_FINITE_CUT_WITNESS.json').read_text())
    assert data['tile']==[a,b,c]
    assert data['cells']==[[0,0,43,43],[0,1,86,43]]
    currents=data['cell_currents']
    assert len(currents)==2 and all(len(q)==2*c for q in currents)
    for cell,q in zip(data['cells'],currents):
        assert all(type(v) is int for v in q)
        pos,neg=cell[2:]
        assert sum(q)==pos-neg
        assert sum(max(v,0) for v in q)<=pos
        assert sum(max(-v,0) for v in q)<=neg
        cap_pos=min(pos,(8*pos+35*neg)//c)
        cap_neg=min(neg,(8*neg+35*pos)//c)
        assert all(-cap_neg<=v<=cap_pos for v in q)
    e=data['node_charge_units']
    assert len(e)==3*c and all(type(v) is int for v in e)
    for g in range(c):
        assert currents[0][g]+currents[1][g]==86*(g==0)+22*e[g]
        assert currents[0][c+g]==-43*(g==0)+22*e[c+g]
        assert currents[1][c+g]==22*e[2*c+g]
    assert e[0]==-2 and e[c]==2 and sum(e)==0
    assert all(v==0 for i,v in enumerate(e) if i not in (0,c))
    index=json.loads(INDEX.read_text())
    assert len(index['certificates'])==65
    checked=0
    minimum_slack=None
    for item in index['certificates']:
        raw=(ROOT/item['path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest()==item['sha256']
        cert=json.loads(raw)
        if 'certificate' in cert:cert=cert['certificate']
        assert cert['tile']==[a,b,c]
        D=cert['D']
        if 'up_remote_weights' in cert:
            t=cert['charge_multiplier_t']
            original_up=[t+v for v in cert['up_remote_weights']]
            original_down=[t+v for v in cert['down_remote_weights']]
        else:
            original_up=cert['up_weights']
            original_down=cert['down_weights']
        for k in range(6):
            sign=(-1)**k
            lu=pow((-a*pow(b,-1,c))%c,k,c)
            ld=pow((-b*pow(a,-1,c))%c,k,c)
            up=[sign*original_up[lu*r%c] for r in range(c)]
            down=[sign*original_down[ld*r%c] for r in range(c)]
            transformed=[(up,down),
                ([down[(a*pow(b,-1,c)*r)%c] for r in range(c)],
                 [up[(b*pow(a,-1,c)*r)%c] for r in range(c)])]
            for u,v in transformed:
                for cell,q in zip(data['cells'],currents):
                    lhs=max(sum(q[r]*u[(r+s)%c] for r in range(c)) for s in range(c))
                    lhs+=max(sum(q[c+r]*v[(r+s)%c] for r in range(c)) for s in range(c))
                    slack=D*(cell[2]+cell[3])-lhs
                    assert slack>=0
                    minimum_slack=slack if minimum_slack is None else min(minimum_slack,slack)
                    checked+=1
    result={'status':'PASS','base_certificates':65,'symmetry_transforms':780,
            'cell_and_transform_inequalities':checked,'independent_shifts_per_hand':43,
            'minimum_integer_slack':minimum_slack,
            'cell_charges':[sum(q) for q in currents],
            'native_whole_node_currents':[42,1],
            'scope':'Exact integer-current witness for this finite dual-cut pool and shared-node constraints only. No full endpoint-column realization or tiling.',
            'full_5063_excluded':False}
    (HERE/'FINITE_CUT_POOL_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    if not __debug__:raise SystemExit('Run with assertions enabled.')
    main()
