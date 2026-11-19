"""Replay the signed endpoint inequality entirely in integer arithmetic.

First compile pool136.cpp and run pool136 D 136 output.dat. Run this script
on output.dat. The weights use the basis 1,w=(1+i sqrt(35))/2 and denominator 81.
"""
import gzip
from math import gcd, lcm
from pathlib import Path
import sys

def canonical(x, y):
    g = gcd(x, y)
    if x < 0 or (x == 0 and y < 0):
        g = -g
    return x // g, y // g

def directions():
    result = {}
    for sign, generator in [(1, (-1, 1)), (-1, (0, -1))]:
        x, y = 1, 0
        u, v = generator
        for n in range(101):
            direction = canonical(x, y)
            assert direction not in result or result[direction] == sign * n
            result[direction] = sign * n
            x, y = x*u - 9*y*v, x*v + y*u + y*v
    return result

HEIGHT = directions()
def events(triangle):
    for (x, y), (u, v) in zip(triangle, triangle[1:] + triangle[:1]):
        h = HEIGHT[canonical(u-x, v-y)]
        yield (x, y, h), 1
        yield (u, v, h), -1

def norm(x, y):
    return x*x + x*y + 9*y*y

def verify(pool_file):
    with pool_file.open() as stream:
        D, N, count = map(int, stream.readline().split())
        assert N == 136 and D > 0
        common = lcm(D, 81)
        positions = [tuple(map(int, line.split())) for line in stream]
    assert len(positions) == count and len(set(positions)) == count
    with Path(str(pool_file) + '.shapes').open() as stream:
        d, n, ns = map(int, stream.readline().split())
        assert (d, n) == (D, N)
        shapes = [tuple(map(int, line.split())) for line in stream]
    assert len(shapes) == ns
    weights = {}
    with gzip.open(Path(__file__).with_name('weights136.tsv.gz'), 'rt') as stream:
        for line in stream:
            x, y, h, val = map(int, line.split())
            row = x*(common//81), y*(common//81), h
            assert row not in weights
            weights[row] = val
    for x, y, u, v in shapes:
        assert x*v-y*u == 8*D*D
        assert sorted([norm(x,y),norm(u,v),norm(u-x,v-y)]) == [9*D*D,64*D*D,81*D*D]
    target = [(0,0),(136*D,0),(64*D,8*D)]
    def value(t):
        return sum(sign*weights.get((x*(common//D),y*(common//D),h),0)
                   for (x,y,h),sign in events(t))
    demand = value(target)
    cap = 0
    for j, x, y in positions:
        u, v, w, z = shapes[j]
        t = [(x,y),(x+u,y+v),(x+w,y+z)]
        cap += max(0,value(t))
    assert demand > cap
    print(f'D={D} candidates={count} target={demand} capacity={cap} gap={demand-cap}')

if __name__ == '__main__':
    for filename in sys.argv[1:]:
        verify(Path(filename))
