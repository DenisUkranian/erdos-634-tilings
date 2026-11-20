"""Check the 3431 exchanges and locate the holes of the reference 5063 packing."""
import json
from fractions import Fraction
from math import lcm
from pathlib import Path

from check_inventory import contained, overlap_pairs, replay
from packing_replay import add, area, edges, norm, pos, sub, verify_boundary

HERE = Path(__file__).resolve().parent


def tile_key(points):
    return tuple(sorted(map(tuple, points)))


def exchange(board, tiles, proof, sides, denominator=None):
    """Apply a coordinate exchange and verify the resulting packing from scratch."""
    tiles = {tile_key(t): t for t in tiles}
    assert len(tiles) == proof['base_count']
    for points in proof['remove']:
        del tiles[tile_key(points)]
    for points in proof['add']:
        k = tile_key(points)
        assert k not in tiles
        tiles[k] = pos(list(map(tuple, points)))
    result = list(tiles.values())
    assert len(result) == proof['new_count']
    a, b, c = sides
    denominator = denominator or c
    lengths = sorted((denominator*s)**2 for s in sides)
    for tri in result:
        assert area(tri) == a*b*denominator**2
        assert sorted(norm(sub(q, p)) for p, q in edges(tri)) == lengths
        assert contained(tri, board)
    assert next(overlap_pairs(result, range(len(result))), None) is None
    return result


def check_holes(board, tiles):
    # Relative vertices of the hexagon in SATURATED_HEXAGON.md, multiplied by 43.
    relative = [(0,0),(-817,0),(-817,-559),(688,-559),(688,-1118),(1248,-910)]
    centers = [(35217,13545), (24037,27090)]
    holes = [[add(p, origin) for p in relative] for origin in centers]
    for hole in holes:
        assert contained(hole, board)
        assert area(hole) == 2*35*13*43**2
    assert max(p[0] for p in holes[1]) < min(p[0] for p in holes[0])
    verify_boundary([(1, tri) for tri in tiles] + [(1, h) for h in holes] + [(-1, board)])


def check_pentagons(board, tiles):
    rows = (HERE / 'remaining_region.txt').read_text().splitlines()
    assert tuple(map(int, rows[0].split())) == (33, 7, 37, 12)
    shapes = []
    for row in rows[1:]:
        size, *entries = map(int, row.split())
        shape = list(zip(entries[::2], entries[1::2], strict=True))
        assert len(shape) == size
        shapes.append(shape)
    hull, *obstacles = shapes
    assert len(obstacles) == 12
    assert area(hull) == 16*33*7*37**2
    assert min(norm(sub(v, u)) for u, v in edges(hull)) == 37**2
    known = {tile_key(t) for t in tiles}
    traced = [(1, t) for t in tiles] + [(-1, board)]
    hulls = []
    for offset in ((0, 0), (-4662, 6105)):
        polygon = [add(p, offset) for p in hull]
        assert contained(polygon, board)
        hulls.append(polygon)
        traced.append((1, polygon))
        for obstacle in obstacles:
            tri = [add(p, offset) for p in obstacle]
            assert tile_key(tri) in known
            assert contained(tri, polygon)
            traced.append((-1, tri))
    assert max(x for x,y in hulls[1]) < min(x for x,y in hulls[0])
    verify_boundary(traced)


def final_exchange(board, tiles, sides):
    proof = json.loads((HERE / 'round_3425.json').read_text())
    fractions = [Fraction(x) for kind in ('add', 'remove')
                 for triangle in proof[kind] for point in triangle for x in point]
    denominator = lcm(sides[2], *(x.denominator for x in fractions))
    assert denominator == 37**5
    for kind in ('add', 'remove'):
        proof[kind] = [[[int(Fraction(x)*denominator) for x in p]
                         for p in triangle] for triangle in proof[kind]]
    def rescale(polygon):
        return [tuple(x*(denominator//sides[2]) for x in point) for point in polygon]
    return exchange(rescale(board), [rescale(t) for t in tiles], proof, sides, denominator)


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    certificate = json.loads((HERE/'inventory_certificate.json').read_text())
    for sides in ((33, 7, 37), (35, 13, 43)):
        a, b, c = sides
        number = (a+2*b)*(2*a+b)
        board, placements, ids = replay(a,b,c,certificate[str(number)])
        tiles = [placements[i] for i in sorted(ids)]
        if number == 3431:
            files = sorted(HERE.glob('exchange_3431*.json'))
            assert files
            for path in files:
                candidate = exchange(board, tiles, json.loads(path.read_text()), sides)
                print(f'3431: verified {len(candidate)} complete tiles using {path.name}.')
                if len(candidate) == 3423:
                    check_pentagons(board, candidate)
                    latest = final_exchange(board, candidate, sides)
                    print(f'3431: verified {len(latest)} tiles, all coordinates in units of 1/37^5.')
        else:
            check_holes(board, tiles)
            print('5063: the complement consists of two translates of the two-unit hexagon.')
