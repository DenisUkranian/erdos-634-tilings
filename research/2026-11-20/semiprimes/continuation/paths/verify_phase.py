"""Exact dual certificates for the short-height-one population invariant."""
import json
from fractions import Fraction
from pathlib import Path

UNITS = ((1,0), (0,1), (-1,1), (-1,0), (0,-1), (1,-1))

def read_bound(case):
    a, b, c = case["tile"]
    d = case["denominator"]
    weights = case["weights"]
    assert type(d) is int and d > 0
    assert len(weights) == 3*c and all(type(w) is int for w in weights)
    assert a*a+a*b+b*b == c*c
    def phi(j, length):
        x, y = UNITS[j % 6]
        return length * (b*x+(a+b)*y)
    def val(j, phase):
        return weights[(j % 3)*c+phase % c]
    def effect(j, sign, apex):
        first = val(j,apex)-val(j,apex-phi(j,a))
        second = val(j+sign,apex+phi(j+sign,b))-val(j+sign,apex)
        return sign*(first+second)
    for j in range(6):
        for apex in range(c):
            assert effect(j,1,apex) <= d
            opposite = apex-phi(j,a)+phi(j-1,b)
            assert effect(j,-1,apex)+effect(j+3,-1,opposite) <= 2*d
    base = -c*effect(0,-1,a*b)
    lower = c+Fraction(base,d)
    blocks = -(-lower//c)
    return lower, blocks, blocks if blocks % 2 else blocks+1

if __name__ == "__main__":
    cases = json.loads(Path(__file__).with_name("phase_duals.json").read_text())
    for case in cases:
        lower, blocks, odd = read_bound(case)
        a, b, c = case["tile"]
        print(f"{(a,b,c)}  N={(a+2*b)*(2*a+b)}  n1 >= {lower},  blocks >= {blocks},  two heights >= {odd}c")
