"""Verify two independent three-placement obstructions in the 3431 packing."""
import json

from check_boards import HERE, exchange, final_exchange, tile_key
from check_inventory import replay
from packing_replay import add, det, edges, norm, pos, sub

A = [(14208,6105), (12987,6105), (12987,5846)]
B = [(12876,6105), (14245,6105), (13965,6336)]
C = [(14014,7425), (14245,6105), (14525,5874)]


def run():
    assert A[0][1] == A[1][1] == B[0][1] == B[1][1] == 6105
    assert B[0][0] < A[1][0] < A[0][0] < B[1][0]
    assert A[2][1] < 6105 < B[2][1]
    u, v = A[0], B[1]
    assert norm(sub(v,u)) == 37**2 and v == C[1]
    # Strict interior at v+(1,0) implies the entire open segment from v
    # to that point is interior by convexity.
    right = add(v,(1,0))
    assert all(det(sub(q,p),sub(right,p))>0 for p,q in edges(pos(C)))
    sides = (33,7,37)
    certificate = json.loads((HERE/'inventory_certificate.json').read_text())
    board, placements, ids = replay(*sides, certificate['3431'])
    baseline = [placements[i] for i in sorted(ids)]
    proof = json.loads((HERE/'exchange_3431_final.json').read_text())
    intermediate = exchange(board,baseline,proof,sides)
    assert len(intermediate)==3423
    result = final_exchange(board,intermediate,sides)
    assert len(result)==3425
    known = {tile_key(t) for t in result}
    keys = set()
    for offset in [(0,0),(-4662,6105)]:
        for endpoint in (u,v):
            point = add(endpoint,offset)
            assert all(det(sub(q,p),sub(point,p))>0 for p,q in edges(board))
        for triangle in (A,B,C):
            scaled = [tuple(i*37**4 for i in add(p,offset)) for p in triangle]
            key = tile_key(scaled)
            assert key in known and key not in keys
            keys.add(key)
    print("Two disjoint forbidden triples verified in the 3425 packing.")


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O.')
    run()
