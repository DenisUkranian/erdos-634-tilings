"""Check the corner-seam calculations with exact axial vectors."""
from fractions import Fraction
from math import gcd, isqrt

def plus(x, y):
    return tuple(a+b for a, b in zip(x, y))

def minus(x, y):
    return tuple(a-b for a, b in zip(x, y))

def times(t, x):
    return tuple(t*a for a in x)

def det(x, y):
    return x[0]*y[1] - x[1]*y[0]

def norm2(x):
    a, b = x
    return a*a+a*b+b*b

def length(x):
    n = Fraction(norm2(x))
    r, s = isqrt(n.numerator), isqrt(n.denominator)
    if r*r != n.numerator or s*s != n.denominator:
        raise ValueError("expected rational length")
    return Fraction(r, s)

def unit(x):
    return times(1/length(x), x)

def intersection(x, dx, y, dy):
    k = det(dx, dy)
    l = det(minus(y, x), dy) / k
    m = det(minus(y, x), dx) / k
    if l <= 0 or m <= 0 or plus(x, times(l, dx)) != plus(y, times(m, dy)):
        raise ValueError("intersection outside the two positive rays")
    return l, m

def check(a, b, c):
    if gcd(a, b) != 1 or c*c != a*a+a*b+b*b or not a > b > 0:
        raise ValueError("invalid input")
    p, q = a+2*b, 2*a+b
    zero, B, C = (0, 0), (b*q, 0), (0, a*p)
    # Derive both bisectors from the board's actual side vectors.
    dB = unit(plus(unit(minus(zero, B)), unit(minus(C, B))))
    dC = unit(plus(unit(minus(zero, C)), unit(minus(B, C))))
    if intersection(B, dB, C, dC) != (b*c, a*c):
        raise ValueError("incenter lengths")
    if plus(B, times(b*c, dB)) != (a*b, a*b):
        raise ValueError("incenter coordinates")
    # Rotating opposite a 120-degree corner gives the two unit rays at zero.
    zb, za = unit((a, b)), unit((b, a))
    rows = [
        (zb, B, dB, a*b*q, b*b*q, c),
        (zb, C, dC, a*b*p, a*a*p, c),
        (za, B, dB, b*c*q, b*c*q, p),
        (za, C, dC, a*c*p, a*c*p, q),
    ]
    for d, v, e, m, n, den in rows:
        s, t = intersection(zero, d, v, e)
        if (s, t) != (Fraction(m, den), Fraction(n, den)):
            raise ValueError("incorrect intersection distances")
        if (s.denominator, t.denominator) != (den, den):
            raise ValueError("denominator did not survive reduction")
        x = times(s, d)
        if not all(det(minus(w, v), minus(x, v)) > 0 for v,w in
                   [(zero,B),(B,C),(C,zero)]):
            raise ValueError("crossing outside board")
    root = (-a * pow(b, -1, c)) % c
    conjugate = ((a+b) * pow(b, -1, c)) % c
    for x in (root, conjugate):
        if (x*x-x+1) % c:
            raise ValueError("failed specialization")
    if (a+b-b*root-q) % c or (a+b*conjugate-q) % c:
        raise ValueError("failed localization denominator")
    if (a*p*root-b*q) % c or (a*p*conjugate-b*q-3*a*a) % c:
        raise ValueError("incorrect corner residues")
    if any(gcd(x, c) != 1 for x in (b*q, a*p*conjugate, 3*a*a)):
        raise ValueError("nonunit corner difference")
    return (p*q, c, p, q)

def main():
    tested = 0
    for a in range(2, 601):
        for b in range(1, a):
            c = isqrt(a*a+a*b+b*b)
            if c*c == a*a+a*b+b*b and gcd(a,b) == 1:
                check(a, b, c)
                tested += 1
    for tile in [(33,7,37),(35,13,43)]:
        n,c,p,q = check(*tile)
        print(f"{n}: beta denominators {c},{c}; alpha denominators {p},{q}")
    print(f"PASS: all {tested} primitive triples with 1 <= b < a <= 600.")

if __name__ == "__main__":
    main()
