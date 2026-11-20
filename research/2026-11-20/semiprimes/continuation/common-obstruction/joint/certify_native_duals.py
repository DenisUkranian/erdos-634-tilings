#!/usr/bin/env python3
"""Round numerical search output, then check every inequality with integers."""
from pathlib import Path
import json
from verify_native_torus import events,pair_events,gate,check_dual
HERE=Path(__file__).resolve().parent
for tag,abc in [('3431',(33,7,37)),('5063',(35,13,43))]:
    p=HERE/('torus'+tag);a,b,c=abc;scale=1000000
    f=[round(scale*x)for x in json.loads((p/'dual.json').read_text())]
    def value(es):return sum(v*f[j*c*c+q[0]*c+q[1]]for(j,q),v in es)
    D=scale
    for j in range(6):
     for x in range(c):
      for y in range(c):
       q=x,y
       if gate(a,b,c,j,q):D=max(D,value(events(a,b,c,j,1,q))+(-1)**j*f[-1])
    for s in(-1,1):
     for j in range(3):
      for x in range(c):
       for y in range(c):D=max(D,-(-value(pair_events(a,b,c,j,s,(x,y)))//2))
    case={'format':'native-two-height-torus-dual-v1','tile':list(abc),'denominator':D,'weights':f,'scope':'Assume all short heights are 1,2 and vertices at height h lie in z^h Z[rho]. This does not establish unrestricted nonexistence.'}
    report=check_dual(case);case['verified_bound']=report
    (p/'exact_dual.json').write_text(json.dumps(case,separators=(',',':'))+'\n')
    print(json.dumps(report),flush=True)
