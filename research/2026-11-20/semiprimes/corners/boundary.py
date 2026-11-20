"""Two-candidate Apéry normal form and exact boundary length checks."""
from heapq import heappop, heappush
from math import gcd


def shape(u, v):
    g = gcd(3, u-v)
    a, b, c = (u*u-v*v)//g, v*(2*u+v)//g, (u*u+u*v+v*v)//g
    assert gcd(u, v) == 1 and a > b > 0 and c*c == a*a + a*b + b*b
    A = (u+2*v)//g
    return a, b, c, A, (u if g == 1 else A), (2*u+v)//g


def least(length, u, v):
    a, b, c, A, C, D = shape(u, v)
    residue = (length * pow(a, -1, D)) % D
    first = 1-C + (residue+C-1) % D
    for difference in range(first, A, D):
        low = max(0, -difference)
        z = low if v == 1 else low + (((length-a*difference)//D)*pow(u, -1, v)-low) % v
        x = z+difference
        if x < A and z < C:
            value = x*a+z*c
            assert min(x, z) < v and (length-value) % b == 0
            return value, (x, (length-value)//b, z)
    raise AssertionError('missing residue')


def shortest_paths(a, b, c):
    dist = [None]*b
    dist[0] = 0
    queue = [(0, 0)]
    while queue:
        value, at = heappop(queue)
        if dist[at] != value:
            continue
        for weight in (a, c):
            new, dest = value+weight, (at+weight) % b
            if dist[dest] is None or new < dist[dest]:
                dist[dest] = new
                heappush(queue, (new, dest))
    return dist


def verify():
    boards = residues = witness_tests = 0
    for u in range(3, 76):
        for v in range(1, u):
            if gcd(u, v) != 1 or u*u-v*v <= v*(2*u+v):
                continue
            a, b, c, A, C, D = shape(u, v)
            dist = shortest_paths(a, b, c)
            for r, m in enumerate(dist):
                assert least(r, u, v)[0] == m
            assert max(dist) == max((A-1)*a+(v-1)*c, (v-1)*a+(C-1)*c)
            boards += 1
            residues += b
            g = gcd(3, u-v)
            missed = u > 4*v*v - (4*v if g == 3 and v % 3 == 2 else 0)
            R = a*(a+2*b)-c*(a+b)
            if v == 1:
                assert R < least(R, u, v)[0]
            if missed and v >= 3 and v % 2:
                w, delta, F = b-c+a, c-a, (u-v)//g
                witness = (w-A-v*v, F-delta+v*u, F-v*v)
                assert min(witness) >= 0 and sum(x*y for x,y in zip(witness,(a,b,c))) == R
                witness_tests += 1
    print(f'Apéry checks: {boards} primitive triples, {residues} residue minima, {witness_tests} positive cap-length tests.')
    for u in (10, 6):
        print(f'u={u}, v=1, minimum for residue of 71 = {least(71,u,1)[0]}')


if __name__ == '__main__':
    verify()
