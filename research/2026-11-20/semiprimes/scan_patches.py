"""Find every uncut F2 triangle of a specified scale inside an exact grid certificate."""
from collections import defaultdict
from math import gcd, isqrt
from pathlib import Path
import json
import sys

from controls.verify_grids import check as verify_grid

ROOT = Path(__file__).resolve().parent


def sub(p, q):
    return p[0]-q[0], p[1]-q[1]


def cross(p, q):
    return p[0]*q[1]-p[1]*q[0]


def norm(p):
    return p[0]*p[0]+p[0]*p[1]+p[1]*p[1]


def direction(p):
    factor = gcd(*p)
    if p[0] < 0 or (p[0] == 0 and p[1] < 0):
        factor = -factor
    return p[0]//factor, p[1]//factor


def merged(intervals):
    result = []
    for lo, hi in sorted(intervals):
        if result and lo <= result[-1][1]:
            result[-1] = (result[-1][0], max(hi, result[-1][1]))
        else:
            result.append((lo, hi))
    return result


def unit_steps(block):
    corners = block['points']
    tri = len(corners) == 3
    n = block['scale'] if tri else block['rows']
    m = n if tri else block['cols']
    u, v = sub(corners[1], corners[0]), sub(corners[-1], corners[0])
    assert all(value % n == 0 for value in u) and all(value % m == 0 for value in v)
    return corners[0], (u[0]//n, u[1]//n), (v[0]//m, v[1]//m), n, m, tri


def seams(block, elementary=False):
    origin, u, v, n, m, tri = unit_steps(block)
    def point(i, j):
        return (origin[0]+i*u[0]+j*v[0], origin[1]+i*u[1]+j*v[1])
    if elementary:
        for i in range(n):
            for j in range(n-i if tri else m):
                corner = point(i, j)
                right, up = point(i+1, j), point(i, j+1)
                yield corner, right
                yield corner, up
                if tri or block['diagonal'] == 'difference':
                    yield right, up
                else:
                    yield corner, point(i+1, j+1)
                if not tri or i+j+1 < n:
                    yield right, point(i+1, j+1)
                    yield up, point(i+1, j+1)
        return
    for i in range(n+1):
        yield point(i, 0), point(i, n-i if tri else m)
    for j in range(m+1):
        yield point(0, j), point(n-j if tri else n, j)
    if tri or block['diagonal'] == 'difference':
        for t in range(1, (n if tri else n+m)+1):
            lo, hi = max(0, t-m), min(n, t)
            yield point(lo, t-lo), point(hi, t-hi)
    else:
        for t in range(1-m, n):
            lo, hi = max(0, -t), min(m, n-t)
            yield point(lo+t, lo), point(hi+t, hi)


def seam_index(data, elementary=False):
    index = defaultdict(lambda: defaultdict(list))
    for block in data['blocks']:
        for p, q in seams(block, elementary):
            if p == q:
                continue
            axis = direction(sub(p, q))
            coord = 0 if axis[0] else 1
            index[axis][cross(axis, p)].append(tuple(sorted((p[coord], q[coord]))))
    return {axis: {key: merged(intervals) for key, intervals in lines.items()}
            for axis, lines in index.items()}


def long_lines(index, axis, physical_length):
    n = isqrt(norm(axis))
    assert n*n == norm(axis)
    coord = 0 if axis[0] else 1
    return {key: runs for key, runs in index.get(axis, {}).items()
            if any(n*(hi-lo) >= abs(axis[coord])*physical_length for lo, hi in runs)}


def supported(runs, start, end):
    lo, hi = sorted((start, end))
    return any(left <= lo and hi <= right for left, right in runs)


def patches(data, scale, check_elementary=False):
    index = seam_index(data)
    if check_elementary:
        assert index == seam_index(data, elementary=True)
    a, b, c = data['tile']
    den = scale*data['coordinate_denominator']
    short, long, base = den*b*(2*a+b), den*a*(a+2*b), den*c*c
    if scale <= 0:
        raise ValueError('positive integer patch scale required')
    candidates = set()
    for axis in index:
        n = isqrt(norm(axis))
        assert n*n == norm(axis)
        starts = long_lines(index, axis, short)
        for orientation in (1, -1):
            dx, dy = orientation*axis[0], orientation*axis[1]
            for rx, ry in ((-dy, dx+dy), (dx+dy, -dx)):
                # Every corner is a genuine mesh vertex and the certificate grid is integral.
                if any(value % n for value in (short*dx, short*dy, long*rx, long*ry)):
                    continue
                e = (short*dx//n, short*dy//n)
                f = (long*rx//n, long*ry//n)
                second = direction(f)
                third = direction(sub(f, e))
                end_lines = long_lines(index, second, long)
                base_lines = long_lines(index, third, base)
                if not end_lines or not base_lines:
                    continue
                determinant = cross(axis, second)
                i, j, k = (0 if v[0] else 1 for v in (axis, second, third))
                for key1, intervals1 in starts.items():
                    for key2, intervals2 in end_lines.items():
                        xnum = key1*second[0]-key2*axis[0]
                        ynum = key1*second[1]-key2*axis[1]
                        if xnum % determinant or ynum % determinant:
                            continue
                        origin = (xnum//determinant, ynum//determinant)
                        a_end = (origin[0]+e[0], origin[1]+e[1])
                        b_end = (origin[0]+f[0], origin[1]+f[1])
                        if (supported(intervals1, origin[i], a_end[i]) and
                            supported(intervals2, origin[j], b_end[j]) and
                            supported(base_lines.get(cross(third, a_end), []), a_end[k], b_end[k])):
                            candidates.add((origin, a_end, b_end))
    return sorted(candidates)


def controlled_subdivision(unit):
    """Four disjoint copies of a known certificate, with a half turn in the center."""
    o, h, v = map(tuple, unit['target'])
    assert o == (0, 0)
    offsets = [(o, 1), (h, 1), (v, 1), ((h[0]+v[0], h[1]+v[1]), -1)]
    blocks = []
    known = set()
    for (x, y), sign in offsets:
        def transform(point):
            return (x+sign*point[0], y+sign*point[1])
        known.add(tuple(transform(point) for point in unit['target']))
        for block in unit['blocks']:
            blocks.append(dict(block, points=[transform(point) for point in block['points']]))
    large = dict(unit, blocks=blocks, target=[(2*x,2*y) for x,y in unit['target']],
                 dilation=2, count=4*unit['count'])
    verify_grid(large)
    hits = set(patches(large, 1))
    assert known <= hits
    # Conjugation and a 60 degree rotation, followed by a translation.
    def transform(point):
        x, y = point
        return (y+19, x-11)
    reflected = dict(large, target=list(map(transform,large['target'])),
                     blocks=[dict(b, points=list(map(transform,b['points']))) for b in blocks])
    verify_grid(reflected)
    assert set(patches(reflected,1)) == {tuple(map(transform,triplet)) for triplet in hits}
    return len(hits)


def main():
    if len(sys.argv) > 1:
        if len(sys.argv) != 3:
            raise SystemExit('Usage: python scan_patches.py CERTIFICATE.json PATCH_SCALE')
        data = json.loads(Path(sys.argv[1]).read_text())
        verify_grid(data)
        print(json.dumps(patches(data, int(sys.argv[2]))))
        return
    files = [ROOT/'staircase'/'certificate_143.json', ROOT/'controls'/'double_3431.json',
             ROOT/'controls'/'double_5063.json']
    print(f'Four-copy positive control: {controlled_subdivision(json.loads(files[0].read_text()))} unit patches, also after reflection.')
    for path in files:
        data = json.loads(path.read_text())
        verify_grid(data)
        own_scale = data.get('dilation', 1)
        targets = patches(data, 1, check_elementary=True)
        full = patches(data, own_scale)
        assert len(full) == 1 and set(full[0]) == set(map(tuple, data['target']))
        print(f"{path.name}: unit patches {len(targets)}, whole-source patches {len(full)}")


if __name__ == '__main__':
    main()
