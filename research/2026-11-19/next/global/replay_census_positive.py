"""Independent exact geometry checks for the two incoming census certificates."""

from fractions import Fraction
from hashlib import sha1, sha256
from itertools import combinations
import json
from math import lcm
from pathlib import Path

HERE = Path(__file__).resolve().parent


def edges(tri):
    return zip(tri, tri[1:] + tri[:1])


def side(a, b, p):
    return (b[0]-a[0])*(p[1]-a[1]) - (b[1]-a[1])*(p[0]-a[0])


def squared_length(a, b):
    x, y = a[0]-b[0], a[1]-b[1]
    return x*x+x*y+y*y


def separated(left, right):
    return any(all(side(a,b,p) <= 0 for p in right) for a,b in edges(left))


def check(n, expected_git_blob):
    raw = (HERE / f"certificate{n}.json").read_bytes()
    blob = sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    assert blob == expected_git_blob
    obj = json.loads(raw)
    base = int(obj.get("denominator", 1))
    polygons = [[(Fraction(x)/base, Fraction(y)/base) for x,y in tri]
                for tri in [obj["target"], *obj["triangles"]]]
    den = lcm(*(w.denominator for tri in polygons for v in tri for w in v))
    def integer_ccw(tri):
        out = tuple((int(x*den), int(y*den)) for x,y in tri)
        return out if side(*out) > 0 else tuple(reversed(out))
    target, *tiles = map(integer_ccw, polygons)
    assert len(tiles) == n
    expected_lengths = sorted((den*z)**2 for z in obj["tile"])
    for tri in tiles:
        assert side(*tri)>0 and sorted(squared_length(a,b) for a,b in edges(tri)) == expected_lengths
        assert all(side(a,b,p)>=0 for a,b in edges(target) for p in tri)
    pair_count = 0
    for left,right in combinations(tiles,2):
        assert separated(left,right) or separated(right,left)
        pair_count += 1
    assert sum(side(*tri) for tri in tiles) == side(*target)
    return dict(n=n, git_blob=blob, sha256=sha256(raw).hexdigest(),
                pairs=pair_count, rational_denominator=den)


if __name__ == "__main__":
    print(json.dumps([check(240,"5fcd3c252d82748c7582dbbc0ed25f73aa14cf65"),
                      check(264,"04a2c82ce3129d911dd063a3ad17514aa9d40672")], indent=2))
