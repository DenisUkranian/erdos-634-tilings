"""The equality core in standard axial coordinates, and its six terminal edge types."""
from itertools import product

import numpy as np

UNITS = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))
HEADINGS = (0, 2, 4, 1, 3, 5)
GENERATORS = {(37, 1): (3, 4), (37, -1): (4, 3),
              (43, 1): (6, 1), (43, -1): (1, 6)}


def add(p, q):
    return p[0] + q[0], p[1] + q[1]


def subtract(p, q):
    return p[0] - q[0], p[1] - q[1]


def scale(n, p):
    return n * p[0], n * p[1]


def multiply(p, q):
    x, y = p
    u, v = q
    return x*u - y*v, x*v + y*u + y*v


def det(p, q):
    return p[0]*q[1] - p[1]*q[0]


def conjugate(p):
    return p[0] + p[1], -p[1]


def exact_divide(p, n):
    assert all(v % n == 0 for v in p)
    return p[0] // n, p[1] // n


def repaired_boundary(a, b, c, l, word_id):
    words = ['2'*a+'3'*l+'1'*l+'4'*l+'0'*b, '4'*l+'2'*a+'1'*l+'0'*b+'3'*l]
    steps = [[(0,c)], [(5,c)], [(4,c)], [(5,a),(0,b)], [(4,a),(5,b)]]
    start = (0, a*(a+2*b))
    end = (b*(2*a+b), 0)
    path = [start]
    for symbol in words[word_id]:
        for j, length in steps[int(symbol)]:
            path.append(add(path[-1], scale(length, UNITS[j])))
    assert path[-1] == end
    polygon = list(reversed(path)) + [(0,0), end]
    segments = []
    for p, q in zip(polygon, polygon[1:]):
        if segments and segments[-1][1] == p and det(subtract(p,segments[-1][0]),subtract(q,p)) == 0:
            p = segments.pop()[0]
        if p != q:
            segments.append((p, q))
    return segments


def inside(segments, c, x, y):
    """Exact even-odd test, including the boundary, in coordinates scaled by c."""
    parity = np.zeros(x.shape, dtype=bool)
    boundary = parity.copy()
    for (px,py),(qx,qy) in segments:
        u, v = qx-px, qy-py
        cross = u*(y-c*py) - v*(x-c*px)
        if v > 0:
            parity ^= (c*py <= y) & (y < c*qy) & (cross > 0)
        if v < 0:
            parity ^= (c*qy <= y) & (y < c*py) & (cross < 0)
        boundary |= ((cross == 0) & (c*min(px,qx) <= x) & (x <= c*max(px,qx))
                     & (c*min(py,qy) <= y) & (y <= c*max(py,qy)))
    return parity | boundary


def shapes(a, b, c, s):
    """Each triple starts at the directed contour tail. All points scaled by c."""
    znum = (a,b) if s == 1 else (a+b,-b)
    result = []
    for i, heading in enumerate(HEADINGS):
        terminal_owner = i < 3
        hand = -s if terminal_owner else s
        j = (heading + (3 if s == -1 else 0)) % 6
        assert hand * (-1)**j == -1
        frame = znum if terminal_owner else (c,0)
        q = multiply(frame, scale(a, UNITS[j]))
        w = add(q, multiply(frame, scale(b, UNITS[(j+hand)%6])))
        if s == -1:
            q, w = subtract(q,w), scale(-1,w)
        expected = scale(c, UNITS[heading]) if terminal_owner else multiply(znum,UNITS[heading])
        assert w == scale(c, expected)
        result.append(((0,0), q, w))
    return result


def exact_profiles(a, b, c, directions):
    def totals(n):
        return ((i,j,n-i-j) for i in range(n+1) for j in range(n-i+1))
    def displacement(ns, ds):
        return tuple(sum(n*d[k] for n,d in zip(ns,ds)) for k in (0,1))
    lows = {displacement(ns,directions[:3]):ns for ns in totals(c)}
    result = []
    for high in totals(a-b):
        target = scale(-1, displacement(high,directions[3:]))
        if target in lows:
            result.append(lows[target] + high)
    return result


def chart(a, b, c, l, word_id, s, t):
    """Supergraph of all possible positioned owners. A bit index encodes one lattice point."""
    segments, pi, xmin, ymin, stride, ymax = layout(a,b,c,l,word_id,s,t)
    # For an allowed segment both coordinates lie in this rectangular index range.
    dy, dx = np.indices((ymax-ymin+1,stride),dtype=np.int64)
    x,y = multiply(pi,(dx+xmin,dy+ymin))
    x = x+t
    domain = inside(segments,c,c*x,c*y)
    def pack(array):
        return int.from_bytes(np.packbits(array.ravel(),bitorder='little').tobytes(),'little')
    directions, shifts, edges = [], [], []
    for _,q,w in shapes(a,b,c,s):
        direction = exact_divide(w,c)
        u,v = exact_divide(multiply(conjugate(pi),direction),c)
        allowed = domain & inside(segments,c,c*x+q[0],c*y+q[1])
        allowed &= inside(segments,c,c*x+w[0],c*y+w[1])
        directions.append(direction)
        shifts.append(u+stride*v)
        edges.append(pack(allowed))
    area2 = sum(det(p,q) for p,q in segments)
    assert area2 == a*b*({(37,0):471,(37,1):693,(43,0):935,(43,1):1365}[c,word_id] - 2*l)
    return tuple(directions), tuple(shifts), edges, pack(domain)

def layout(a,b,c,l,word_id,s,t):
    pi = GENERATORS[c,s]
    znum = (a,b) if s == 1 else (a+b,-b)
    assert multiply(pi,conjugate(pi)) == (c,0)
    exact_divide(multiply(conjugate(znum),pi), c)
    segments = repaired_boundary(a,b,c,l,word_id)
    corners = [p for edge in segments for p in edge]
    # Bound coordinates of every point in the residual after division by pi.
    rect = product((min(x for x,y in corners),max(x for x,y in corners)),
                   (min(y for x,y in corners),max(y for x,y in corners)))
    box = [multiply(conjugate(pi),subtract(p,(t,0))) for p in rect]
    xmin = min(x for x,y in box)//c
    xmax = max(x for x,y in box)//c
    ymin = min(y for x,y in box)//c
    ymax = max(y for x,y in box)//c
    stride = xmax-xmin+1
    return segments, pi, xmin, ymin, stride, ymax
