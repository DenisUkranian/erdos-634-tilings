#!/usr/bin/env python3
"""Independent supported-polygon audit controls from saved exact placements."""
from copy import deepcopy
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

from through_geometry import ExactGeometry,det,sub,scale
from verify_snapshot import SnapshotAudit,freeze


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
RULE = 'integral-tile-area-and-two-signed-characters-v1'


def model_for(sides,tiles,witness):
    g = ExactGeometry(*sides)
    return dict(sides=list(sides),N=g.N,unrestricted_heights=True,
                fixed_odd_population=None,temporary_row_equations=False,
                tiles=tiles,fan_paths=[],general_area_cycle_cuts=[witness],general_area_cycle_rule=RULE)


def area_audit(model):
    audit = SnapshotAudit(model)
    audit.general_area_cycles()
    return audit


def forbidden_mixed_witness(data):
    """Construct the historical cycle directly, without importing a detector."""
    g = ExactGeometry(*data['tile'])
    tiles = [(tuple(t['q']),t['h'],t['j'],t['s']) for t in data['placements']]
    edges = [(edge['start'],edge['end'],edge['tile']) for edge in data['cycle']]
    assert all(g.point(edges[k][1]) == g.point(edges[(k+1)%len(edges)][0]) for k in range(len(edges)))
    area2 = sum(det(g.point(p),g.point(q)) for p,q,_ in edges)
    if area2<0:
        edges = [(q,p,i) for p,q,i in reversed(edges)]
        area2 = -area2
    records = []
    W0 = W1 = F(0)
    for encoded_p,encoded_q,i in edges:
        p,q = g.point(encoded_p),g.point(encoded_q)
        polygon = g.polygon(tiles[i])
        found = []
        for k,(a,b) in enumerate(zip(polygon,polygon[1:]+polygon[:1])):
            if det(sub(b,a),sub(p,a)) or det(sub(b,a),sub(q,a)):
                continue
            axis = 0 if a[0]!=b[0] else 1
            if not (min(a[axis],b[axis])<=p[axis]<=max(a[axis],b[axis])
                    and min(a[axis],b[axis])<=q[axis]<=max(a[axis],b[axis])):
                continue
            possibilities = [(H,j,L) for H in range(tiles[i][1]-1,tiles[i][1]+2)
                             for j in range(6) for L in (g.a,g.b,g.c)
                             if sub(b,a) == scale(L,g.unit(H,j))]
            assert len(possibilities)==1
            H,j,L = possibilities[0]
            signed = L*(q[axis]-p[axis])/(b[axis]-a[axis])
            found.append((k,H,j,signed))
        assert len(found)==1
        k,H,j,signed = found[0]
        W0 += signed*(-1 if j%2 else 1)
        W1 += signed*(-1 if (H+j)%2 else 1)
        records.append(dict(start=encoded_p,end=encoded_q,representative=i,side=k,
                            selected_owners=[i],length=str(abs(signed)),
                            direction=[H,j if signed>0 else (j+3)%6]))
    E0,E1 = W0/(g.a-g.b-g.c),W1/(g.a-g.b+g.c)
    even,odd = (E0+E1)/2,(E0-E1)/2
    area = area2/(g.a*g.b)
    assert area.denominator == even.denominator == odd.denominator == 1
    assert area>=abs(even)+abs(odd) and (area-even-odd)%2 == 0
    witness = dict(indices=sorted({i for _,_,i in edges}),
                   vertices=[p for p,_,_ in edges]+[edges[0][0]],edges=records,
                   twice_axial_area=str(area2),tile_area_ratio=str(area),
                   budget=dict(W0=str(W0),W1=str(W1),even_charge=str(even),odd_charge=str(odd),violations=[]))
    return tiles,witness


def main():
    source = HERE.parent/'corner-tests/AREA_CYCLE_REPLAY.json'
    raw = source.read_bytes()
    controls = json.loads(raw)['fractional_hole_controls']
    sides = {3431:(33,7,37),5063:(35,13,43)}
    accepted,corrupt = [],[]
    for k,control in enumerate(controls):
        model = model_for(sides[control['N']],control['tiles'],control['witness'])
        audit = area_audit(model)
        assert len(audit.expected)==1
        accepted.append(dict(N=control['N'],height=control['height'],area=control['witness']['tile_area_ratio']))
        for kind in ('wrong_character','wrong_area','missing_support'):
            bad = deepcopy(model)
            witness = bad['general_area_cycle_cuts'][0]
            if kind == 'wrong_character': witness['budget']['W0'] = str(F(witness['budget']['W0'])+1)
            elif kind == 'wrong_area': witness['tile_area_ratio'] = '1'
            else: witness['indices'] = witness['indices'][:-1]
            try:
                area_audit(bad)
            except (AssertionError,ValueError,KeyError):
                corrupt.append(f'{k}:{kind}')
            else:
                raise AssertionError('Accepted corrupt area witness')
    legal = []
    directory = ROOT/'research/2026-11-20/semiprimes/continuation/common-obstruction/boundary'
    for N in (143,3431,5063):
        data = json.loads((directory/f'mixed_cycle_{N}.json').read_bytes())
        tiles,witness = forbidden_mixed_witness(data)
        try:
            area_audit(model_for(data['tile'],tiles,witness))
        except AssertionError as error:
            assert 'no demonstrated obstruction' in str(error), str(error)
            legal.append(dict(N=N,area=witness['tile_area_ratio'],charges=[witness['budget']['even_charge'],witness['budget']['odd_charge']],not_forbidden=True))
        else:
            raise AssertionError('A compatible mixed-height cycle was incorrectly forbidden')
    result = dict(status='PASS',source_sha256=hashlib.sha256(raw).hexdigest(),
                  independently_checked_forbidden_supports=accepted,rejected_corrupt_witnesses=len(corrupt),
                  compatible_mixed_height_cycles=legal,
                  scope='Only local supported-polygon cuts and corrupt-witness controls; no target or corner root exclusion.')
    (HERE/'AREA_AUDIT_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
