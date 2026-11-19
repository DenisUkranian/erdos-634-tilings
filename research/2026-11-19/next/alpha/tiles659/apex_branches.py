"""Rebuild and check every D=9 joint corner configuration of the 280 target."""
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from itertools import product
from math import gcd
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
BOARD = ((0, 0), (1260, 0), (630, 360))
POOL_HASH = '199af3d2a7743b00bb913a1c17179651242d4b275b385bd01d1f9ab24925a043'
SHAPES_HASH = '77e5eb408dcd482bbd8967c2e45e0a3003dd918afdc3616747197140c6855492'


def shape_path(path):
    return Path(str(path) + '.shapes')


def vertices(pose, shapes):
    k, x, y = pose
    u, v, a, b = shapes[k]
    return ((x, y), (x + u, y + v), (x + a, y + b))


def ray(p, q):
    x, y = q[0] - p[0], q[1] - p[1]
    g = gcd(x, y)
    return x // g, y // g


def corner_fans(poses, shapes):
    # A counterclockwise tile occupies the sector from its outgoing edge to
    # the reversed incoming edge. Only tiles at the board corner are eligible.
    outgoing = [{} for _ in BOARD]
    for i, pose in enumerate(poses):
        t = vertices(pose, shapes)
        for j, p in enumerate(t):
            if p in BOARD:
                start, end = ray(p, t[(j + 1) % 3]), ray(p, t[(j - 1) % 3])
                outgoing[BOARD.index(p)].setdefault(start, []).append((i, end))
    fans = []
    for k, p in enumerate(BOARD):
        start, finish = ray(p, BOARD[(k + 1) % 3]), ray(p, BOARD[(k - 1) % 3])
        result = []
        def visit(r, row):
            if r == finish:
                result.append(tuple(row))
                return
            for i, s in outgoing[k].get(r, ()):
                assert i not in row
                visit(s, row + [i])
        visit(start, [])
        assert all(len(row) == (3 if k == 2 else 1) for row in result)
        fans.append(result)
    return fans


def interior_disjoint(t, s):
    for a, b in ((t, s), (s, t)):
        for p, q in zip(a, a[1:] + a[:1]):
            dx, dy = q[0] - p[0], q[1] - p[1]
            if all(dx * (v - p[1]) - dy * (u - p[0]) <= 0 for u, v in b):
                return True
    return False


def bounds(t):
    x, y = zip(*t)
    return min(x), max(x), min(y), max(y)


def joint_cases(poses, shapes):
    fans = corner_fans(poses, shapes)
    assert tuple(map(len, fans)) == (2, 2, 12)
    ids = sorted({i for options in fans for row in options for i in row})
    pins = {i: vertices(poses[i], shapes) for i in ids}
    bit = {i: 1 << j for j, i in enumerate(ids)}
    def signature(row, mirror):
        return tuple(sorted(tuple(sorted((1260-x if mirror else x, y) for x, y in pins[i])) for i in row))
    cases = []
    for left, right, apex in product(*fans):
        row = left + right + apex
        direct, reflected = signature(row, False), signature(row, True)
        assert direct != reflected
        if direct < reflected:
            cases.append(row)
    assert len(cases) == 24
    # Store which of the 14 potential corner tiles has positive-area overlap
    # with each position. A selected corner tile itself is always retained.
    pin_boxes = {i: bounds(t) for i, t in pins.items()}
    forbidden = []
    for j, pose in enumerate(poses):
        t = vertices(pose, shapes)
        a, b, c, d = bounds(t)
        mask = 0
        for i, (u, v, w, z) in pin_boxes.items():
            if j != i and a < v and u < b and c < z and w < d and not interior_disjoint(t, pins[i]):
                mask |= bit[i]
        forbidden.append(mask)
    return [(row, sum(bit[i] for i in row)) for row in cases], forbidden


def run_filter(exe, inp, output):
    reply = subprocess.run([str(exe), str(inp), str(output)], check=True, capture_output=True, text=True)
    last = reply.stdout.rstrip().splitlines()[-1].split()
    if last[:3] == ['missing', 'target', 'corner']:
        return int(last[-1]), 0
    assert len(last) == 6 and last[0] == 'pass' and last[2] == 'incoming'
    assert last[4] == 'surviving' and last[3] == last[5]
    return int(last[1]), int(last[5])


def make_pool(folder, filter_exe):
    pool_exe = folder / 'makepool'
    subprocess.run(['c++', '-O3', '-std=c++17', str(HERE.parents[2] / 'nov19/alpha280/pool.cpp'), '-o', str(pool_exe)], check=True)
    raw, pruned = folder / 'initial', folder / 'all-corners'
    subprocess.run([str(pool_exe), '9', '280', str(raw)], check=True, capture_output=True)
    assert run_filter(filter_exe, raw, pruned)[1] == 196212
    shutil.copyfile(shape_path(raw), shape_path(pruned))
    return pruned


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--pool', type=Path, help='use the precomputed 196212-position global pool')
    parser.add_argument('--jobs', type=int, default=4)
    args = parser.parse_args()
    records = json.loads((HERE / 'apex_branch_results.json').read_text())
    expected = {tuple(tuple(p) for p in row['pins']): row for row in records}
    with TemporaryDirectory() as temp:
        folder = Path(temp)
        filter_exe = folder / 'fan_filter'
        subprocess.run(['c++', '-O3', '-std=c++20', str(HERE.parents[1] / 'alpha280mesh/sparse_fans.cpp'), '-o', str(filter_exe)], check=True)
        pool = args.pool or make_pool(folder, filter_exe)
        assert sha256(pool.read_bytes()).hexdigest() == POOL_HASH
        assert sha256(shape_path(pool).read_bytes()).hexdigest() == SHAPES_HASH
        with pool.open() as f:
            assert f.readline().split() == ['9', '280', '196212']
            poses = [tuple(map(int, l.split())) for l in f]
        with shape_path(pool).open() as f:
            assert f.readline().split() == ['9', '280', '20']
            shapes = [tuple(map(int, l.split())) for l in f]
        cases, forbidden = joint_cases(poses, shapes)
        assert {tuple(poses[i] for i in row) for row, _ in cases} == set(expected)
        lines = [f'{k} {x} {y}\n' for k, x, y in poses]
        def check_branch(item):
            index, (row, mask) = item
            pins = tuple(poses[i] for i in row)
            rec = expected[pins]
            inp, out = folder / f'input-{index}', folder / f'output-{index}'
            count = sum(not (word & mask) for word in forbidden)
            assert count == rec['initial']
            with inp.open('w') as f:
                f.write(f'9 280 {count}\n')
                f.writelines(line for word, line in zip(forbidden, lines) if not word & mask)
            shutil.copyfile(shape_path(pool), shape_path(inp))
            passes, count = run_filter(filter_exe, inp, out)
            assert (passes, count) == (rec['passes'], rec['survivors'])
            with out.open() as f:
                assert f.readline().split() == ['9', '280', str(count)]
                found = {l for l in f if l in {lines[i] for i in row}}
            assert len(found) == 5
            inp.unlink()
            out.unlink()
            return count
        with ThreadPoolExecutor(max_workers=args.jobs) as workers:
            counts = list(workers.map(check_branch, enumerate(cases)))
        print(f'Raw corner combinations 48. Reflection classes {len(cases)}. All five pins survive in {len(counts)} classes.')
        print(f'Stable pool sizes {min(counts)} through {max(counts)}.')

if __name__ == '__main__':
    main()
