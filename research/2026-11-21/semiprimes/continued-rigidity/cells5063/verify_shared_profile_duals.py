#!/usr/bin/env python3
"""Replay every new cell dual with independent integer polygon geometry.

No discovery code, floating linear program, or integer optimizer is used.
Each recorded gate vector is checked explicitly against the dual weights.
"""
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'research').is_dir() and (p/'scripts').is_dir())
spec=importlib.util.spec_from_file_location('independent_cell_polygon_audit',
    ROOT/'research/2026-11-21/semiprimes/audit/verify_profile_duals.py')
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)


def main():
    reports=[]
    for path in sorted(HERE.glob('shared_profile_cut_*.json')):
        report,_=audit.verify(path)
        data=json.loads(path.read_text())
        currents=data['cell_gate_currents']
        assert len(currents)==86 and all(isinstance(q,int) for q in currents)
        value=sum(q*w for q,w in zip(currents,data['up_weights']+data['down_weights']))
        assert value==data['lower_numerator']
        assert data['lower_denominator']==data['D']
        minimum=(value+data['D']-1)//data['D']
        minimum+=(minimum-sum(currents))%2
        report.update(recorded_cell_charge=sum(currents),
                      recorded_profile_lower_numerator=value,
                      recorded_profile_lower_denominator=data['D'],
                      greatest_population_excluded_for_recorded_profile=(value-1)//data['D'],
                      least_population_with_recorded_charge_parity=minimum)
        reports.append(report)
    assert reports
    out={'status':'PASS','certificates':len(reports),'polygon_columns_per_certificate':22188,
         'records':reports,
         'scope':'Exact universal endpoint inequalities and their individual recorded-profile bounds. No exhaustion of the shared-node current universe and no whole-target exclusion are asserted.'}
    (HERE/'SHARED_PROFILE_DUALS_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
