"""Lower bounds on exchanging fixed placements to obtain an exact F2 tiling."""
from collections import Counter
from fractions import Fraction as F
import json

from check_boards import HERE, exchange, tile_key
from check_inventory import replay
from check_saturation import read_region, product
from packing_replay import add, edges, norm, sub


def low_headings():
    lookup = {}
    for h in range(-8,9):
        direction = (F(1), F(0))
        step = (F(33,37), F(7,37)) if h >= 0 else (F(40,37), F(-7,37))
        for _ in range(abs(h)):
            direction = product(direction, step)
        for _ in range(6):
            lookup[direction] = h
            direction = (-direction[1], direction[0]+direction[1])
    return lookup


def baseline_bridges():
    cert = json.loads((HERE/'inventory_certificate.json').read_text())
    board, tiles, ids = replay(33,7,37,cert['3431'])
    proof = json.loads((HERE/'exchange_3431_final.json').read_text())
    full = exchange(board,[tiles[i] for i in sorted(ids)],proof,(33,7,37))
    _, originals = read_region()
    inside = {tile_key([add((int(37*x),int(37*y)),shift) for x,y in tri])
              for shift in ((0,0),(-4662,6105)) for tri in originals}
    lookup = low_headings()
    result = Counter()
    for triangle in full:
        if tile_key(triangle) in inside:
            continue
        indices = set()
        for x,y in edges(triangle):
            dx,dy = sub(x,y)
            length = next(side for side in (7,33,37) if (37*side)**2==norm((dx,dy)))
            indices.add(lookup[F(dx,37*length),F(dy,37*length)])
        lo, hi = sorted(indices)
        assert lo+1 == hi
        result[lo] += 1
    assert sum(result.values()) == 3399
    return result


def best_bound(count, budget):
    # An actual tiling has every integer level between its extrema. If we
    # shrink those extrema to bound retained tiles and board headings 0,2,
    # no further tile from the given packing is lost.
    lows = sorted({0} | {h for h in count if h<0})
    highs = sorted({2} | {h+1 for h in count if h+1>2})
    values = []
    for lo in lows:
        for hi in highs:
            present = {h for h in count if lo<=h<hi}
            outside = sum(v for h,v in count.items() if h not in present)
            missing = hi-lo-len(present)
            values.append((max(outside,missing-budget), lo,hi,outside,missing))
    return min(values)


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O.')
    rows=json.loads((HERE/'pentagon14.json').read_text())['placements']
    counts=baseline_bridges()
    print('Prior bridge distribution:',sorted(counts.items()))
    for h,_,reflected,_,_ in rows:
        counts[h if reflected else h-1] += 2
    print('All bridge counts:',sorted(counts.items()))
    assert sum(counts.values()) == 3427
    assert sum(n for h,n in counts.items() if h >= 40) == 20
    assert all(h not in counts for h in range(2,40))
    result = best_bound(counts,4)
    assert result[0] == 20
    print('At least 20 retained positions must change; retaining a high tile requires at least 38 new placements.')
