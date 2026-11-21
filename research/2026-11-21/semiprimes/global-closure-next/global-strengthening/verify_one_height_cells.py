#!/usr/bin/env python3
"""Finite arithmetic of the one-height 215 cell classification, not tilings."""
import json
from pathlib import Path


def main():
    if not __debug__:
        raise RuntimeError('Run without -O.')
    c,d=43,22
    assert (2*c)%d and (-c)%d
    flags=[(u,v) for u in (0,1) for v in (0,1)
           if (c-2*c*u+c*v)%d == 0]
    assert flags==[(1,1)]
    retained=[]
    for x in range(c+1):
        matrix=[[(x,x),(c-x,c-x)],[(c-x,c-x),(c+x,x)]]
        rows=[tuple(sum(cell[s] for cell in row) for s in (0,1))
              for row in matrix]
        cols=[tuple(sum(matrix[i][j][s] for i in (0,1)) for s in (0,1))
              for j in (0,1)]
        assert rows==cols==[(c,c),(2*c,c)]
        assert [[p-m for p,m in row] for row in matrix]==[[0,0],[0,c]]
        if x in (0,c):
            continue  # Prior geometric theorem / exact certificate transfer.
        assert all(p+m>0 for row in matrix for p,m in row)
        assert c+2 <= sum(matrix[1][1]) <= 3*c-2
        retained.append(x)
    assert len(retained)==42
    gate_positive_cap=(8*(2*c)+35*c)//43
    assert gate_positive_cap==51
    assert [e for e in range(-10,10) if -43<=22*e<=51]==[-1,0,1,2]
    assert [e for e in range(-10,10) if -43<=86+22*e<=51]==[-5,-4,-3,-2]
    skeleton_counts={'single_single':1,'one_split':2*2*(c-1),
                     'both_split':4*(c-1)**2*len(retained)}
    assert skeleton_counts=={'single_single':1,'one_split':168,'both_split':296352}
    assert sum(skeleton_counts.values())==296521
    report={
        'scope':'One-height 215 necessary cell matrices for 5063; no tiling feasibility decision.',
        'native_exact_nodes_forced_occupied':True,
        'native_flag_pairs_for_isolated_charged129_cell':flags,
        'candidate_matrix_parameters_checked':44,
        'retained_four_cell_parameters':retained,
        'excluded_endpoint_parameters':{
            '0':'An existing geometric theorem excludes the monochromatic 43-cell.',
            '43':'The isolated native 129-class satisfies every hypothesis of the 65-certificate profile proof.'},
        'possible_numbers_of_occupied_joint_cells':[1,2,4],
        'native_joint_cell_occupied':True,
        'ambient_height_one_phase_class_count':c*c,
        'containing_phase_sign_skeleton_counts':skeleton_counts,
        'total_containing_phase_sign_skeletons':sum(skeleton_counts.values()),
        'finite_arithmetic':'PASS',
        'full_215_exclusion':False,
    }
    encoded=json.dumps(report,indent=2)+'\n'
    Path(__file__).with_name('ONE_HEIGHT_CELL_CLASSIFICATION_REPLAY.json').write_text(encoded)
    print(encoded,end='')


if __name__=='__main__':
    main()
