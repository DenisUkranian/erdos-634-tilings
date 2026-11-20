"""Independent finite audit using line inventories and exact convex hulls."""
from math import gcd, isqrt
from verify_full_board import shape


def turn(p, q, r):
    return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])


def half(points):
    chain = []
    for point in points:
        while len(chain) >= 2 and turn(chain[-2], chain[-1], point) <= 0:
            chain.pop()
        chain.append(point)
    return chain


def mean_possible(types, r, c):
    if not types:
        return False
    points = sorted((r*m, r*l) for m, l in types)
    hull = half(points)[:-1] + half(reversed(points))[:-1] if len(points)>1 else points
    target = (c, c)
    if len(hull) == 1:
        return target == hull[0]
    if len(hull) == 2:
        a, b = hull
        return (turn(a, b, target) == 0 and all(min(x, y) <= c <= max(x, y) for x, y in zip(a,b)))
    return all(turn(hull[i-1], hull[i], target) >= 0 for i in range(len(hull)))


def audit(u, v):
    a, b, c = shape(u, v)
    g = gcd(3, u-v)
    # The scalar sum of the positive line loads bounds the number of lines.
    max_lines = 3*(u+v)//g
    inverse = pow(b, -1, c)
    inventories = []
    for m in range(max_lines):
        first = a*m*inverse % c
        for l in range(first, max_lines, c):
            if m or l:
                inventories.append((m, l))
    checked = 0
    for r in range(isqrt(c), max_lines+1):
        if r*(r-1) < c:
            continue
        types = [(m,l) for m,l in inventories if max(m,l)<r]
        assert not mean_possible(types,r,c), (u,v,r,types)
        checked += 1
    return checked


def main():
    cases = lines = 0
    for u in range(2, 101, 2):
        for v in range(1, u, 2):
            if gcd(u,v) != 1 or shape(u,v)[0] <= shape(u,v)[1]:
                continue
            lines += audit(u,v)
            cases += 1
    print(f'Line-inventory convex hulls exclude the single block in {cases} shapes ({lines} line counts).')
    for u,v in [(10,1),(6,1),(44,3),(122,5)]:
        a,b,c = shape(u,v)
        print(f'{(a+2*b)*(2*a+b)}: v={v}, g={gcd(3,u-v)}, c={c}, {audit(u,v)} line counts excluded')


if __name__ == '__main__':
    main()
