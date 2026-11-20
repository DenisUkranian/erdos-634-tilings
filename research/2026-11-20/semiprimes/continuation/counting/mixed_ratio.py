"""List every prime pair outside the unit F2 staircase in a fixed ratio interval."""
from fractions import Fraction
from math import gcd, isqrt
from pathlib import Path
import csv


def ratio(x):
    return Fraction(2*x*x + 2*x - 1, x*x + 4*x + 1)


def primes_through(n):
    sieve = bytearray([1]) * (n+1)
    sieve[:2] = bytes(2)
    for k in range(2,isqrt(n)+1):
        if sieve[k]:
            sieve[k*k::k] = bytes((n-k*k)//k+1)
    return [k for k, yes in enumerate(sieve) if yes]


def residuals(bound):
    if not 1 < bound < 2:
        raise ValueError("Choose a rational bound strictly between one and two.")
    upper = 3
    while ratio(upper) <= bound:
        upper += 1
    # Every missed board has x=u/v > 4(v-1) and x < upper.
    vmax = (upper+3)//4
    umax = upper*vmax
    primes = primes_through(3*umax)
    def prime(n):
        for ell in primes:
            if ell*ell > n:
                return True
            if n % ell == 0:
                return False
        return True  # Both factors below are less than 9*umax**2.
    records = []
    for v in range(1,vmax+1,2):
        for u in range(2,upper*v,2):
            if gcd(u,v) != 1:
                continue
            g = gcd(3,u-v)
            threshold = 4*v*(v-1 if g == 3 and v%3 == 2 else v)
            if u <= threshold:
                continue
            a,b = (u*u-v*v)//g, v*(2*u+v)//g
            if a <= b:
                continue
            p,q = a+2*b, 2*a+b
            if q*bound.denominator > p*bound.numerator or not (prime(p) and prime(q)):
                continue
            c = (u*u+u*v+v*v)//g
            assert p>3 and p<q<2*p and p*q%24==23
            assert (p*p-p*q+q*q)==3*c*c and Fraction(a+c,b)==Fraction(u,v)
            records.append((p*q,p,q,u,v))
    return sorted(records)


if __name__ == '__main__':
    import argparse
    import hashlib
    parser=argparse.ArgumentParser()
    parser.add_argument('--wide', action='store_true',
                        help='also verify the 199/100 table fingerprint')
    parser.add_argument('--write-wide',type=Path,
                        help='write the 199/100 exception rows to this CSV file')
    args=parser.parse_args()
    rows = residuals(Fraction(19,10))
    with (Path(__file__).parent/'mixed_ratio_19_10.csv').open(encoding='ascii') as f:
        stored = [tuple(map(int,r)) for r in list(csv.reader(f))[1:]]
    assert rows == stored
    for cutoff in (Fraction(7,4), Fraction(9,5), Fraction(19,10)):
        selected = residuals(cutoff)
        assert selected == [r for r in rows if Fraction(r[2],r[1]) <= cutoff]
        print(f"q/p <= {cutoff}: {len(selected)} exceptions, largest product {selected[-1][0]:,}, largest smaller prime {max(r[1] for r in selected):,}")
        if cutoff == Fraction(7,4):
            print("Products:", ", ".join(str(r[0]) for r in selected))

    if args.wide or args.write_wide:
        wide = residuals(Fraction(199,100))
        data = ''.join(','.join(map(str,r))+'\n' for r in wide).encode('ascii')
        digest = hashlib.sha256(data).hexdigest()
        assert digest=='c54e2541756eb1506861973d6720bef120b68c27d3a0c139bc2af14487c81b50'
        assert len(wide)==18789 and wide[-1]==(125845513570493443703,7952292373,15825061211,88878,149)
        print(f'q/p <= 199/100: {len(wide)} exceptions, last {wide[-1]}, SHA-256 {digest}')
        if args.write_wide:
            args.write_wide.write_bytes(b'N,p,q,u,v\n'+data)
