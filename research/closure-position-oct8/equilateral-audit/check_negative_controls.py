#!/usr/bin/env python3
"""Meaningful rejection checks for the independent geometry verifier."""
import copy,json,tempfile
from pathlib import Path
from independent_geometry import audit

def main():
    root=Path(__file__).resolve().parents[1]
    original=json.loads((root/'equilateral-position/cpsat/T30_30_0-1_certificate.json').read_text())
    cases=[]
    changed=copy.deepcopy(original);changed['triangles'][0][0][0]+=1
    cases.append(('changed_side',changed,'not congruent'))
    duplicate=copy.deepcopy(original);duplicate['triangles'][1]=copy.deepcopy(duplicate['triangles'][0])
    cases.append(('overlap_without_area_change',duplicate,'Positive-area overlap'))
    shifted=copy.deepcopy(original)
    for t in shifted['triangles']:
        for p in t:p[0]+=10000
    cases.append(('rigid_displacement',shifted,'not contained'))
    report=[]
    with tempfile.TemporaryDirectory() as directory:
        for name,certificate,expected in cases:
            path=Path(directory)/(name+'.json');path.write_text(json.dumps(certificate))
            try:audit(path)
            except ValueError as error:
                if expected not in str(error):raise
                report.append({'case':name,'rejected':True,'reason':str(error)})
            else:raise RuntimeError('Invalid certificate was accepted: '+name)
    return {'status':'PASS','controls':report}

if __name__=='__main__':print(json.dumps(main(),indent=2))
