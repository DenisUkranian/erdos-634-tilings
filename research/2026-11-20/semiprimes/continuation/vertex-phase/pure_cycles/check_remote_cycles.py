"""Check the direction-width and thickness bounds for the two F2 controls."""
from fractions import Fraction
from itertools import combinations
from math import gcd


def norm(point):
    x, y = point
    return x*x + x*y + y*y


def check_board(a, b, c, expected_radius_squared):
    assert gcd(a*b, c) == 1 and c*c == a*a + a*b + b*b
    p, q = a + 2*b, 2*a + b
    assert p < 2*c and q < 2*c
    A, B = Fraction(a*p, c), Fraction(b*q, c)
    assert B <= A and c <= A and A*A < 3*a*a
    # Each row encodes |u*x+v*y| <= t. The first three describe
    # T-T. The next three substitute rho*(x+y*rho)= -y+(x+y)*rho.
    forms = [(1, 0, A), (0, 1, B), (B, A, A*B),
             (0, 1, A), (1, 1, B), (A, A-B, A*B)]
    lines = [(sgn*u, sgn*v, t) for u,v,t in forms for sgn in (-1,1)]
    vertices = set()
    for (u,v,t),(r,s,z) in combinations(lines, 2):
        d = u*s-v*r
        if not d:
            continue
        x, y = (t*s-v*z)/d, (u*z-t*r)/d
        if all(i*x+j*y <= k for i,j,k in lines):
            vertices.add((x, y))
    radius_squared = max(map(norm, vertices))
    assert radius_squared == expected_radius_squared < a*a
    thickness = B*(1 - Fraction(a, 1)/A)
    assert thickness < b
    print(f'{p*q}: max common squared chord {radius_squared} < {a*a}; '
          f'thickness <= {thickness} < {b}')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O.')
    check_board(33, 7, 37, Fraction(1331780030161, 3293267769))
    check_board(35, 13, 43, Fraction(9230010672961, 8428158025))
