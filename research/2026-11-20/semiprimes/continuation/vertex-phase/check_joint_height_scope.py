#!/usr/bin/env python3
"""Independent shared-height capacity controls, without geometric claims."""
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_signed_scope as signed_controls
from joint_height_search import make_joint_height_search_class

SignedSearch = signed_controls.SignedSearch
JointSearch = make_joint_height_search_class(SignedSearch)
options, fix, query, close = (signed_controls.options, signed_controls.fix,
                              signed_controls.query, signed_controls.close)


def physical_records(search, tree, height, count):
    budget = search.phase_budgets[tree]
    level = budget.sign * height
    denominator = max(1, 1 - level)
    nodes = [budget.node((i, 0, denominator), level) for i in range(1, count + 1)]
    assert len(set(nodes)) == count and (0, 0, 0) not in nodes
    return [search.signed_node(tree, node) for node in nodes]


def fix_records(records, plus, minus):
    return [clause for record in records for clause in fix(record, plus, minus)]


def core_zero(search):
    return [clause for nodes in search.signed_nodes for clause in fix(nodes[(0, 0, 0)], 0, 0)]


def fix_height(search, height, plus, minus):
    return fix({'bits': search.joint_heights[height]}, plus, minus)


def check_joint():
    for sides in ((33, 7, 37), (35, 13, 43)):
        with tempfile.TemporaryDirectory(prefix='joint-height-') as tmp:
            search = JointSearch(options(tmp, sides))
            count = search.signed_caps[0] // 2
            demand = 2 * count
            left = physical_records(search, 0, 2, count)
            right = physical_records(search, 1, 2, count)
            assert set(search.joint_heights) == {0, 2}
            # Both trees describe the same population at physical h=2.
            # The common capacity pays once, not once for each tree.
            same = core_zero(search) + fix_records(left + right, 2, 0)
            query(search, same + fix_height(search, 0, 0, 0)
                  + fix_height(search, 2, demand, 0), 'sat')
            query(search, same + fix_height(search, 2, demand - 1, 0), 'unsat')

            mixed = core_zero(search) + fix_records(left + right, 1, 1)
            query(search, mixed + fix_height(search, 2, count, count), 'sat')
            query(search, mixed + fix_height(search, 2, count, count - 1), 'unsat')

            # Add a new physical height after a queued pop. Declarations and
            # coupling sums must be reconstructed from the expanded catalogue.
            remote = physical_records(search, 1, 4, count)
            assert set(search.joint_heights) == {0, 2, 4}
            same += fix_records(remote, 0, 0)
            query(search, same + fix_height(search, 4, 0, 0), 'sat')
            split = core_zero(search) + fix_records(left + remote, 2, 0)
            split += fix_records(right, 0, 0)
            assert demand <= search.signed_caps[0] < 2 * demand
            query(search, split, 'unsat')
            search.rebuild(1)
            query(search, same, 'sat')
            query(search, split, 'unsat')
            close(search)

        # This verifies that the split-height contradiction specifically uses
        # shared H. Each independent tree budget admits the same fixed counts.
        with tempfile.TemporaryDirectory(prefix='uncoupled-height-') as tmp:
            search = SignedSearch(options(tmp, sides))
            count = search.signed_caps[0] // 2
            left = physical_records(search, 0, 2, count)
            remote = physical_records(search, 1, 4, count)
            split = core_zero(search) + fix_records(left + remote, 2, 0)
            query(search, split, 'sat')
            close(search)


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O.')
    # Reuse the independent signed scope controls through the new subclass.
    signed_controls.SignedSearch = JointSearch
    signed_controls.check_scope()
    signed_controls.check_partial_parity()
    check_joint()
    print('PASS: shared physical heights, one payment for both trees, both signs;')
    print('strictly stronger split-height contradiction, new-height query scope, rebuild;')
    print('and all prior signed scope controls through the shared-height subclass.')
