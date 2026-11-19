"""Check Paliy's original two coordinate lists with integer geometry. No packages."""
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json


def cycle(polygon):
    return zip(polygon, polygon[1:] + polygon[:1])


def left(a, b, p):
    return (b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0])


def area2(triangle):
    return left(*triangle)


def side_squares(triangle, metric):
    return sorted((p[0]-q[0])**2 + metric*(p[1]-q[1])**2 for p,q in cycle(triangle))


def disjoint_interiors(first, second):
    # Separating axis of two convex polygons may be chosen normal to an edge of either.
    return any(all(left(a, b, p) <= 0 for p in other)
               for poly,other in ((first, second),(second, first)) for a,b in cycle(poly))


def verify(n, expected_tile, expected_outer, metric, denom):
    file = Path(__file__).resolve().parents[2] / "data" / f"tiling-{n}.json"
    data = json.loads(file.read_bytes())
    triangles, outer = data["tiles"], data["target"]
    assert data["N"] == n == len(triangles)
    assert data["denominator"] == denom and data["D"] == metric
    for tri in [outer]+triangles:
        assert len(tri)==3 and all(len(p)==2 and all(type(c) is int for c in p) for p in tri)
        assert area2(tri)>0
    assert side_squares(outer,metric)==sorted((s*denom)**2 for s in expected_outer)
    for tri in triangles:
        assert side_squares(tri,metric)==sorted((s*denom)**2 for s in expected_tile)
        assert all(left(a,b,p)>=0 for a,b in cycle(outer) for p in tri)
    assert sum(map(area2,triangles)) == area2(outer)
    for first,second in combinations(triangles,2):
        assert disjoint_interiors(first,second)
    # Mutations: duplicate a triangle; apply an inexact perturbation to a vertex.
    assert not disjoint_interiors(triangles[0],triangles[0])
    changed=[p[:] for p in triangles[0]]
    changed[0][0]+=1
    assert side_squares(changed,metric)!=side_squares(triangles[0],metric)
    return dict(N=n,tile_sides=expected_tile,target_sides=expected_outer,
                pair_tests=n*(n-1)//2,sha256=sha256(file.read_bytes()).hexdigest(),result="PASS")


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O.")
    print(json.dumps([verify(322,(6,5,9),(81,115,126),32,18),
                      verify(897,(12,7,16),(256,273,368),55,32)], indent=2))
