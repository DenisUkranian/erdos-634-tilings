"""Compute exact exposed lengths of the two fixed packings, including T-junctions."""
from collections import defaultdict
from fractions import Fraction as F
from math import gcd, isqrt
import json

from check_boards import HERE, exchange, final_exchange, tile_key
from check_inventory import replay
from check_triples import A, B, C
from packing_replay import add, edges


def exposed_lengths(board, tiles, denominator):
    # Each input side contributes its owner's ID to its open projected intervals.
    lines = defaultdict(lambda: defaultdict(list))
    for owner, poly in enumerate([board] + tiles):
        for p, q in edges(poly):
            dx, dy = q[0]-p[0], q[1]-p[1]
            g = gcd(dx, dy)
            ux, uy = dx//g, dy//g
            if (ux, uy) < (0, 0):
                ux, uy = -ux, -uy
            key = (ux, uy, ux*p[1]-uy*p[0])
            left, right = sorted((p, q))
            lines[key][left].append((owner, 1))
            lines[key][right].append((owner, -1))

    exposed = [F(0)]*(len(tiles)+1)
    for (ux, uy, _), events in lines.items():
        length = isqrt(ux*ux+ux*uy+uy*uy)
        assert length**2 == ux*ux+ux*uy+uy*uy
        active = set()
        previous = None
        for point, changes in sorted(events.items()):
            if len(active) == 1:
                d = gcd(point[0]-previous[0], point[1]-previous[1])
                exposed[next(iter(active))] += F(d*length, denominator)
            for owner, sign in changes:
                if sign == 1:
                    active.add(owner)
                else:
                    active.remove(owner)
            assert len(active) <= 2
            previous = point
        assert not active
    return exposed


def measure():
    a, b, c, n = 33, 7, 37, 3431
    cert = json.loads((HERE/'inventory_certificate.json').read_text())
    board, inv, ids = replay(a,b,c,cert[str(n)])
    baseline = [inv[i] for i in sorted(ids)]
    stage = exchange(board, baseline, json.loads((HERE/'exchange_3431_final.json').read_text()), (a,b,c))
    tiles = final_exchange(board, stage, (a,b,c))
    board = [tuple(x*37**4 for x in p) for p in board]
    exposed = exposed_lengths(board, tiles, 37**5)
    assert sum(exposed)==1618 and exposed[0]==0
    by_coordinate = {tile_key(t): i+1 for i,t in enumerate(tiles)}
    for offset in ((0,0),(-4662,6105)):
        group = [by_coordinate[tile_key([tuple(v*37**4 for v in add(p,offset))
                                          for p in tri])] for tri in (A,B,C)]
        assert [exposed[i] for i in group] == [0,1,7]
    assert 1618-2*7-6*77 == 1142 > 14*77
    print('3425 packing: exposed perimeter 1618, exposed triple lengths 0,1,7 twice.')
    print('Removing at most eight leaves at least 1142 to cover with perimeter at most 1078.')


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Run without -O.')
    measure()
