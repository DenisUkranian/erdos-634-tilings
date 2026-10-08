#!/usr/bin/env python3
"""Check the positive certificate directly, without any search or solver."""
from fractions import Fraction as F
import json
from pathlib import Path
from decode_q480 import boundary, cross, determinant, edge_pairs, norm, overlap, sub

here=Path(__file__).resolve().parent
data=json.loads((here/'q480_tiling.json').read_text())
q=[tuple(map(F,p)) for p in data['target']]
triangles=[tuple(tuple(map(F,p)) for p in t) for t in data['triangles']]
assert q==[(22,0),(528,0),(-242,242),(-48,48)]
assert len(triangles)==480
for t in triangles:
    assert determinant(t)==264
    assert sorted(norm(sub(b,a)) for a,b in edge_pairs(t))==[121,576,961]
    assert all(cross(sub(b,a),sub(v,a))>=0 for v in t for a,b in edge_pairs(q))
assert boundary(triangles)==boundary([q])
pairs=0
for i,t in enumerate(triangles):
    for u in triangles[:i]:
        assert not overlap(t,u)
        pairs+=1
assert sum(determinant(t) for t in triangles)==sum(cross(a,b) for a,b in edge_pairs(q))
print(json.dumps({'status':'PASS','count':480,'exact_pairwise_nonoverlap_checks':pairs,
                  'lengths_containment_area_and_oriented_boundary':'PASS'}))
