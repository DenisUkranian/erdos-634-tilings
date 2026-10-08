#!/usr/bin/env python3
"""Reproduce arithmetic gates and the source-to-project transfer arithmetic."""
from dataclasses import asdict
import importlib.util
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('literature_gate',ROOT/'research/uniform-reduction/candidates.py')
module=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=module
spec.loader.exec_module(module)


def main():
    gates=[]
    for n in [14,23,33,56,92,132,143,297,14430]:
        gates.append(dict(count=n,classical=module.classical(n),
                          arithmetic_candidates=[asdict(x) for x in module.enumerate_candidates(n)]))
    last=gates[-1]['arithmetic_candidates']
    if len(last)!=1 or last[0]['tile']!=(56,9,61) or last[0]['multiplier']!=1:
        raise RuntimeError('14430 candidate gate changed')
    a,b,c=56,9,61
    U,V=a+2*b,2*a+b
    eq=4*a*b
    f2=U*V
    f3=3*(a+b)*U
    if eq+c*c+a*a+b*b!=f2 or f2+U*U!=f3 or f3!=14430:
        raise RuntimeError('Incorrect transfer identity')
    rows=[]
    for a,b in [(3,5),(5,3)]:
        rows.append(dict(tile=[a,b,7],equilateral=a*b,
                         isosceles=b*(a+2*b),F1=b*(a+b),
                         F4=(2*a+b)*(a+b),F2=(a+2*b)*(2*a+b),
                         F3=3*(a+2*b)*(a+b)))
    report=dict(status='PASS',gates=gates,small_tile_transfer_coefficients=rows,
                high_ratio_transfer=dict(tile=[56,9,61],equilateral_side=2*56*9,
                    equilateral_count=eq,F2_count=f2,F3_count=f3,
                    F2_target=[a for a in [56*74,9*121,61**2]],
                    geometric_existence_not_established=True),
                new_complete_square_class_claimed=False,
                gate_is_not_geometric_sufficiency=True)
    (HERE/'candidate_checks.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',complete_gates=len(gates),transfer_identity=f3)))


if __name__=='__main__':main()
