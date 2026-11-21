#!/usr/bin/env python3
"""Exact consequence of the separately proved cell minority/kernel exclusions.

This checker verifies their recorded interfaces and the complete finite
population arithmetic. Replay the referenced verifiers for the geometric
and kernel-search premises themselves.
"""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent


def main():
    dependencies=[HERE.parent/'global/CELL_MINORITY_REPLAY.json',
                  HERE.parent/'integer3431/SMALL_BALANCED_CELLS_REPLAY.json']
    minority,kernels=[json.loads(p.read_text()) for p in dependencies]
    assert minority['proved_minority_lower_bound']==5
    assert all(r['surviving_patterns']==0 for r in minority['results'] if r['minority']<5)
    assert kernels['status']=='PASS'
    absent=set(kernels['excluded_balanced_populations'])
    assert absent=={2,4,8,10,14}
    target=next(r for r in kernels['targets'] if r['tile']==[35,13,43])
    assert {r['population'] for r in target['small_exclusions'] if r['all_absent']}==absent
    kept=[];rejected=[]
    for x in range(1,43):
        reasons=[]
        if x<5:reasons.append('charged_cell_minority_below_5')
        if 2*x in absent:reasons.append('first_balanced_cell_population_excluded')
        if 2*(43-x) in absent:reasons.append('offdiagonal_balanced_cell_population_excluded')
        matrix=[[(x,x),(43-x,43-x)],[(43-x,43-x),(43+x,x)]]
        assert all(sum(matrix[i][j][0] for j in range(2))==[43,86][i] for i in range(2))
        assert all(sum(matrix[i][j][1] for j in range(2))==43 for i in range(2))
        assert all(sum(matrix[i][j][0] for i in range(2))==[43,86][j] for j in range(2))
        assert all(sum(matrix[i][j][1] for i in range(2))==43 for j in range(2))
        assert sum(sum(cell) for row in matrix for cell in row)==215
        if reasons:rejected.append({'x':x,'reasons':reasons})
        else:kept.append(x)
    assert kept==[6]+list(range(8,36))+[37,40]
    counts={'one_cell':1,'two_cells':2*2*42,'four_cells':4*42**2*len(kept)}
    counts['total']=sum(counts.values())
    assert len(kept)==31 and counts['total']==218905
    out={'status':'PASS','remaining_four_cell_parameters':kept,
         'parameter_count':len(kept),'rejected_parameters':rejected,
         'charged_cell_population_range':[43+2*min(kept),43+2*max(kept)],
         'containing_skeleton_counts':counts,'previous_total':296521,
         'removed_skeletons':296521-counts['total'],
         'premise_replays':[{'path':str(p.relative_to(HERE.parent)),
                            'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in dependencies],
         'scope':'Necessary containing-list reduction for the 215 odd-tile mode only. No retained skeleton is claimed realizable; neither215 nor5063 is excluded.'}
    (HERE/'REDUCED_SKELETONS_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
