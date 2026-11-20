"""Produce candidate witnesses; exact verification uses only verify_phase.py."""
import json
from pathlib import Path
import numpy as np
from lp_torus import solve
from verify_phase import read_bound

out=[]
for a,b,c in [(33,7,37),(35,13,43),(85,11,91),(143,25,157),(161,15,169),(323,37,343)]:
    res, matrix, _, costs=solve(a,b,c)
    assert res.success
    den=100000
    weights=np.rint(den*res.eqlin.marginals).astype("int64")
    assert max(map(abs,weights))<2**50
    bounds=matrix.T.dot(weights)
    den=max([den]+[-(-int(x)//y) for x,y in zip(bounds,costs)])
    case={"tile":[a,b,c],"denominator":den,"weights":weights.tolist()}
    print(read_bound(case),flush=True)
    out.append(case)
    Path(__file__).with_name("phase_duals.json").write_text(json.dumps(out,separators=(",",":"))+"\n")
