"""Replay valuation and budget calculations on the 3431 F2 board."""
import json
from pathlib import Path
import sys


def run(path):
    a, b, c = 33, 7, 37
    n = (a+2*b)*(2*a+b)
    root = (-a*pow(b, -1, c)) % c
    assert root == 27 and (root*root-root+1) % c == 0
    assert (a+b*(1-root)) % c != 0
    cert = json.loads(path.read_text())
    assert cert['denominator'] == c**5
    rows = cert['placements']
    lows = []
    for h, _, _, x, y in rows:
        residue = (x+root*y) % c
        assert residue
        if h < 41:
            lows.append((h,residue))
    assert sorted(lows) == [(0,16),(0,32),(0,34),(1,18)]
    assert len(rows) == 14 and 2*(len(rows)-len(lows)) == 20
    length = a*(a+2*b)+b*(2*a+b)
    outside = n-(41-(-4))*2*c
    assert outside == 101
    candidates = [(a*i+b*j,i,j) for i in range(28) for j in range(28-i)
                  if ((a-b)*(i-j)-length) % c == 0]
    assert max(candidates) == (683,19,8)
    assert length-c*c == 693 > 683
    assert 4*2*c-2-4 == 290
    assert ((5*3+6)-1)*2*c-8-4 == 1468
    print('20 individually forbidden high placements; four remote low branches,', sorted(lows))
    print('Outside budget 101; short-edge capacity 683 < 693.')
    print('Keeping any low replacement forces at least 290 omissions; keeping all eight forces 1468.')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    path = Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent/'packing'/'pentagon14.json'
    run(path)
