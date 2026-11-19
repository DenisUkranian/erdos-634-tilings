"""Check an arbitrary positive count against certified reductions; preserve unresolved cases."""
import argparse
import json
import sys
from math import gcd, isqrt
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / "tripleproducts"))
sys.path.insert(0, str(BASE / "powers"))
sys.path.insert(0, str(BASE / "squareclasses"))
from check_rows import recover_product_rows, square
from check_powers import notch
from classify import classify as classify_square_class


def factors(n):
    result = {}
    p = 2
    while p*p <= n:
        if n % p == 0:
            count = 0
            while n % p == 0:
                n //= p
                count += 1
            result[p] = count
        p = 3 if p == 2 else p + 2
    if n > 1:
        result[n] = 1
    return result


def divisors(powers):
    values = [1]
    for p, exponent in powers.items():
        values = [k * p**j for k in values for j in range(exponent + 1)]
    return sorted(values)


def residual_shapes(n, powers):
    square_part = {p:e//2 for p,e in powers.items() if e >= 2}
    found = []
    for t in divisors(square_part):
        d = n//(t*t)
        found.extend((family, u, v, c, t) for family,u,v,c in recover_product_rows(d))
        if t == 1:
            continue
        for v in range(2, isqrt(d) + 1):
            for family, form in (("W",2), ("beta",3)):
                u2 = form*v*v-d
                if 0 < u2 < v*v and square(u2) and gcd(isqrt(u2),v) == 1:
                    found.append((family,isqrt(u2),v,0,t))
        for low in divisors(factors(d)):
            high = d//low
            if low >= high or (high-low) % 2:
                continue
            u,v = (high-low)//2,(high+low)//2
            if gcd(u,v) == 1:
                found.append(("theta",u,v,0,t))
                if v < 2*u:
                    found.append(("double",u,v,0,t))
    return sorted(found)


def realizes(shape):
    name, a, b, c, t = shape
    if name == "Paliy":
        return True
    if name in ("W","beta"):
        return t >= b
    if name == "theta":
        return t >= notch(a,b)[-1]
    if name == "alpha":
        return t*b >= notch(a,b)[-1]
    if name == "double":
        return False
    if name == "F4" and a < b:
        return True
    return t >= 3*(max(a,b)//min(a,b)+2)


def classify(n, use_reference=True):
    if n < 1:
        raise ValueError("A positive integer is required.")
    def result(verdict, reason, **metadata):
        return dict(N=n, verdict=verdict, reason=reason, **metadata)
    ps = factors(n)
    if all(e % 2 == 0 or p % 4 != 3 for p,e in ps.items()):
        return result("YES", "sum of two squares (including squares)")
    if any(n % k == 0 and square(n//k) for k in (3,6)):
        return result("YES", "classical 3 or 6 times a square")
    if all(e % 2 == 0 or e >= 5 for e in ps.values()):
        return result("YES", "fifth power times a square")
    if n in (231,329):
        return result("NO","archived arithmetic reduction and exact geometric exclusion")
    if len(ps) == 1 and next(iter(ps.values())) == 1:
        return result("NO","prime classification")
    for r, additional in ((7,{7,11}),(19,{19})):
        if n % r == 0:
            q = n//r
            if q > 1 and factors(q) == {q:1}:
                return result("YES" if q in additional else "NO",f"complete {r}q prime row")
    candidates = residual_shapes(n, ps)
    if n % 4 == 0 and n//4 > 3 and factors(n//4) == {n//4:1}:
        # Proposition 6.4(ii) and Theorem F in the hypotheses of the 4p reduction.
        candidates = [s for s in candidates if s[0] not in ("theta","double")]
    if n==280:
        candidates = [s for s in candidates if s[0] not in ("F1","equilateral60")]
    for shape in candidates:
        if realizes(shape):
            return result("YES","fixed-shape construction",shape=shape)
    if candidates and n <= 200 and use_reference:
        known = json.loads(Path(__file__).with_name("spectrum200.json").read_text())["positive"]
        return result("YES" if n in known else "NO", "Bonfioli's complete classification through 200 (Theorem 1.3)")
    if candidates:
        arithmetic_result = classify_square_class(n)
        if arithmetic_result["status"] != "UNRESOLVED":
            return result(arithmetic_result["status"], arithmetic_result["reason"], square_class=arithmetic_result)
        return result("UNRESOLVED","surviving necessary shapes below applied construction thresholds",shapes=candidates)
    return result("NO","all necessary count forms excluded")


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("N",type=int,nargs="+")
    args=parser.parse_args()
    print(json.dumps([classify(n) for n in args.N],indent=2))
