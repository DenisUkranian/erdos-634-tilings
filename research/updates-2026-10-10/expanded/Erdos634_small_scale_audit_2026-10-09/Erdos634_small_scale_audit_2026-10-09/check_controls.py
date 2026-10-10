#!/usr/bin/env python3
"""Positive and deliberately invalid controls for the independent verifier."""
from copy import deepcopy
from pathlib import Path
import json
import verify_certificate as v
here=Path(__file__).parent
p=json.loads((here/'W28_positive_control.json').read_text())
D,N=p['D'],p['N']; T=v.canonical(tuple(map(v.point,p['target'])))
tiles=[v.canonical(tuple(map(v.point,t))) for t in p['triangles']]
v.need(len(tiles)==N==28,'positive control count')
for t in tiles:
    v.need(sorted(v.norm(v.minus(a,b),D) for a,b in v.ee(t))==[4,9,16],'positive tile metric')
    v.need(all(v.within(T,a) for a in t),'positive containment')
for i,t in enumerate(tiles):
    v.need(all(v.separate(t,s) for s in tiles[:i]),'positive overlap')
v.need(not v.residual(T,tiles),'positive coverage')
base=json.loads((here/'beta_2_3_1_refutation.json').read_text())
tests=[]
x=deepcopy(base);x['nodes'][0]['children'].pop();tests.append(('deleted_branch',x))
x=deepcopy(base);x['nodes'][0]['children'][0]['triangle'][0][0]='999';tests.append(('moved_tile',x))
x=deepcopy(base);x['nodes'][0]['children'][0]['node']=0;tests.append(('cycle',x))
for name,x in tests:
    try:v.verify(x)
    except (v.Invalid,KeyError,IndexError):pass
    else:raise AssertionError('accepted invalid '+name)
r={'positive_control':'PASS','positive_tiles':28,'positive_pairs':378,'corrupted_certificates_rejected':[x[0] for x in tests]}
(here/'controls_report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
