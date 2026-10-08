#!/usr/bin/env python3
"""Independent integer metric, containment and positioned-boundary certificate.

Imports no constructor or search code. Positive polygon multiplicities and
equal compactly supported boundary currents imply multiplicity exactly one.
"""
from collections import defaultdict
from hashlib import sha256
from math import gcd
from pathlib import Path
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    here = Path(__file__).resolve().parent
    source = here / 'W5022.json'
    data = json.loads(source.read_text())
    den = data['denominator']
    D = data['metric_y_coefficient']
    require(type(den) is int and den > 0 and D == 160, 'Coordinate metric')
    require(data['tile'] == [42, 13, 49], 'Tile')
    require(len(data['triangles']) == 5022, 'Count')
    require((data['u'], data['v'], data['scale']) == (6, 7, 9), 'Parameters')
    events = defaultdict(lambda: defaultdict(int))

    def polygon(poly, sign, sides):
        require(len(poly) == 3, 'Triangle vertex count')
        require(all(len(p) == 2 and all(type(x) is int for x in p) for p in poly), 'Coordinates')
        area = 0
        lengths = []
        for a, b in zip(poly, poly[1:] + poly[:1]):
            dx, dy = b[0] - a[0], b[1] - a[1]
            area += a[0]*b[1] - a[1]*b[0]
            lengths.append(dx*dx + D*dy*dy)
            g = gcd(dx, dy)
            require(g > 0, 'Degenerate edge')
            ux, uy = dx//g, dy//g
            if (ux, uy) < (0, 0):
                ux, uy = -ux, -uy
            line = (ux, uy, ux*a[1] - uy*a[0])
            ta, tb = ux*a[0] + uy*a[1], ux*b[0] + uy*b[1]
            direction = sign if ta < tb else -sign
            events[line][min(ta, tb)] += direction
            events[line][max(ta, tb)] -= direction
        require(area > 0, 'Nonpositive orientation')
        require(sorted(lengths) == sorted(den*den*s*s for s in sides), 'Side lengths')
        return area

    target = data['target']
    area_target = polygon(target, -1, [3087, 3348, 819])
    total = 0
    for triangle in data['triangles']:
        total += polygon(triangle, 1, [42, 13, 49])
        for a, b in zip(target, target[1:] + target[:1]):
            for p in triangle:
                require((b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0]) >= 0, 'Containment')
    require(total == area_target, 'Area equality')
    require(all(x == 0 for line in events.values() for x in line.values()), 'Boundary cancellation')
    report = dict(status='PASS', count=5022, tile=[42,13,49],
                  target_sides=[3087,3348,819], metric_y_coefficient=D,
                  denominator=den, all_metrics_exact=True,
                  all_tiles_contained=True, all_orientations_positive=True,
                  exact_area_equality=True, positioned_boundary_identity=True,
                  lines=len(events), certificate_sha256=sha256(source.read_bytes()).hexdigest())
    (here/'W5022_checked.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
