"""Certified outer contours and their residuals after removing the known far owners."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[2] / "2026-11-26/semiprimes/terminal-contact"
sys.path.insert(0, str(SOURCE))
from native_positions import overlap
from remote_boundary import accepted_words, signature
from terminal import UNITS, add, det, scale
from two_bank_words import census
from two_native import turn


def two_owner_words(a, b, c):
    words = set()

    def collect(result, outgoing, returning):
        if result[0] != 4*c:
            return
        raw = [6, *outgoing, 9, *((j+3)%6 for j in reversed(returning))]
        # Pure far bank: rotate the exceptional vector z to 1.
        words.add(signature(raw))
        # Pure near bank: conjugate and reverse to retain positive orientation.
        word = [6+(3-j)%6 if j<6 else (3-(j-6))%6 for j in reversed(raw)]
        words.add(signature(word))

    census(a, b, c, collect)
    return words


def repair(word, a, b, c):
    point = (0, 0)
    chain = Counter()
    owners = []
    area = 0
    for letter in word:
        j = letter % 6
        far = letter < 6
        start = point
        apex_offset = turn((a*c, 0) if far else (a*(a+b), -a*b), j)
        for heading, length in ([(j, a), ((j-1)%6, b)] if far else [(j, c)]):
            for _ in range(length):
                end = add(point, UNITS[heading])
                edge = tuple(sorted((point, end)))
                chain[edge] += 1 if edge[0] == point else -1
                point = end
        area += det(start, point)
        u, v = scale(c, start), scale(c, point)
        tri = (u, v, add(u, apex_offset))
        if det((v[0]-u[0], v[1]-u[1]), apex_offset) < 0:
            tri = (tri[1], tri[0], tri[2])
        owners.append(tri)
    assert point == (0, 0) and area == 4*c*a*b
    if any(overlap(left, right) for left, right in combinations(owners, 2)):
        return None

    successor = {}
    for (p, q), count in chain.items():
        if not count:
            continue
        assert abs(count) == 1
        if count < 0:
            p, q = q, p
        assert p not in successor
        successor[p] = q
    assert set(successor) == set(successor.values())
    point = start = min(successor)
    vertices = []
    while point in successor:
        vertices.append(point)
        point = successor.pop(point)
    assert point == start and not successor
    # Unit triangular-lattice edges can only meet at integer endpoints.
    corners = []
    for i, p in enumerate(vertices):
        q, r = vertices[i-1], vertices[(i+1)%len(vertices)]
        if det((p[0]-q[0], p[1]-q[1]), (r[0]-p[0], r[1]-p[1])):
            corners.append(p)
    remaining = 4*c-sum(letter<6 for letter in word)
    assert sum(det(p,q) for p,q in zip(corners, corners[1:]+corners[:1])) == remaining*a*b
    return corners


def cases(join, sides):
    a, b, c = sides
    short = ({w for k,w in accepted_words(join,a,b,c,8) if k==2}
             if c==37 else set())
    two = two_owner_words(a,b,c)
    assert (len(short), len(two)) == ((24,6) if c==37 else (0,2))
    return [(kind, word, repair(word,*sides))
            for kind, words in [('sixteen',short), ('two_owner',two)]
            for word in sorted(words)]
