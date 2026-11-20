"""Check the 3431 exchanges and locate the holes of the reference 5063 packing."""
import json
from pathlib import Path

from check_inventory import contained, overlap_pairs, replay
from packing_replay import add, area, edges, norm, pos, sub, verify_boundary

HERE = Path(__file__).resolve().parent


def tile_key(points):
    return tuple(sorted(map(tuple, points)))


def exchange(board, tiles, proof, sides):
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
    lengths = sorted((c*s)**2 for s in sides)
    for tri in result:
        assert area(tri) == a*b*c*c
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
                tiles = exchange(board, tiles, json.loads(path.read_text()), sides)
            print(f'3431: verified {len(tiles)} complete tiles after the coordinate exchanges.')
        else:
            check_holes(board, tiles)
            print('5063: the complement consists of two translates of the two-unit hexagon.')
