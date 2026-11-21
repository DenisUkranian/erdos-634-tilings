#!/usr/bin/env python3
"""Contained height-one columns, preserving every real supporting line.

The path frame is divided by z=(a+b*rho)/c.  Height-one anchors are
integer axial coordinates.  Endpoints are periodic by c only along their
own axis: (axis 0, y, x mod c), (axis 1, x, y mod c), and
(axis 2, x+y, y mod c).  These are necessary cylinder equations, not
the full physical endpoint current and not nonoverlap constraints.
"""
from dataclasses import dataclass
import numpy as np

U = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))


def ceildiv(p, q):
    return -((-p) // q)


@dataclass
class Catalogue:
    a: int
    b: int
    c: int
    board: tuple
    bounds: tuple
    offsets: tuple
    endpoint_rows: int
    x: np.ndarray
    y: np.ndarray
    j: np.ndarray
    s: np.ndarray
    eps: np.ndarray
    gate: np.ndarray
    rows: np.ndarray

    @property
    def count(self):
        return len(self.x)

    @property
    def row_count(self):
        return self.endpoint_rows + 2*self.c

    def rhs(self, f=2):
        rhs = np.zeros(self.row_count)
        rhs[self.endpoint_rows] = 2*self.c-(self.a-self.b)*f
        rhs[self.endpoint_rows+self.c] = -self.c+(self.a-self.b)*f
        return rhs

    def score(self, dual):
        """All columns, using exactly four endpoint terms and one gate."""
        return (self.s*(dual[self.rows[0]]-dual[self.rows[1]]
                       +dual[self.rows[2]]-dual[self.rows[3]])
                +self.eps*dual[self.endpoint_rows+self.gate.astype(np.int32)])

    def sparse_columns(self, ids):
        ids = np.asarray(ids, dtype=np.int32)
        n = len(ids)
        indices = np.empty((n, 5), dtype=np.int32)
        indices[:, :4] = self.rows[:, ids].T
        indices[:, 4] = self.endpoint_rows+self.gate[ids].astype(np.int32)
        values = np.empty((n, 5), dtype=np.float64)
        values[:, 0] = self.s[ids]
        values[:, 1] = -self.s[ids]
        values[:, 2] = self.s[ids]
        values[:, 3] = -self.s[ids]
        values[:, 4] = self.eps[ids]
        return (np.arange(0, 5*n+1, 5, dtype=np.int32),
                indices.ravel(), values.ravel())

    def labels(self, ids):
        return np.column_stack((self.x[ids], self.y[ids],
                                self.j[ids], self.s[ids])).tolist()


def build(a=33, b=7, c=37):
    if a*a+a*b+b*b != c*c:
        raise ValueError('Tile must have a^2+ab+b^2=c^2')
    B = a*(a+2*b)
    # Board vertices in coordinates c*z^(-1) times the path frame.
    board = ((0, 0), (c*c*(a+b), -c*c*b), (B*a, B*b))
    inequalities = []
    for p, q in zip(board, board[1:]+board[:1]):
        dx, dy = q[0]-p[0], q[1]-p[1]
        inequalities.append((dy*c, -dx*c, dy*p[0]-dx*p[1]))
    xmin = ceildiv(min(p[0] for p in board), c)
    xmax = max(p[0] for p in board)//c
    ymin = ceildiv(min(p[1] for p in board), c)
    ymax = max(p[1] for p in board)//c
    tmin = ceildiv(min(p[0]+p[1] for p in board), c)
    tmax = max(p[0]+p[1] for p in board)//c
    offsets = (0, (ymax-ymin+1)*c,
               (ymax-ymin+xmax-xmin+2)*c)
    nr = offsets[2]+(tmax-tmin+1)*c

    xx, yy, jj, ss = [], [], [], []
    for j in range(6):
        for s in (-1, 1):
            off = ((0, 0), (-a*U[j][0], -a*U[j][1]),
                   (b*U[(j+s)%6][0], b*U[(j+s)%6][1]))
            ineq = [(p, q, r-max(p*x+q*y for x, y in off))
                    for p, q, r in inequalities]
            for y in range(ymin, ymax+1):
                lo, hi = xmin, xmax
                for p, q, r in ineq:
                    v = r-q*y
                    if p > 0:
                        hi = min(hi, v//p)
                    elif p < 0:
                        lo = max(lo, ceildiv(v, p))
                    elif v < 0:
                        hi = lo-1
                        break
                if lo <= hi:
                    n = hi-lo+1
                    xx.append(np.arange(lo, hi+1, dtype=np.int16))
                    yy.append(np.full(n, y, dtype=np.int16))
                    jj.append(np.full(n, j, dtype=np.int8))
                    ss.append(np.full(n, s, dtype=np.int8))
    x, y, j, s = map(np.concatenate, (xx, yy, jj, ss))
    eps = s*np.where(j%2, -1, 1).astype(np.int8)
    ux = x-a*np.asarray([p[0] for p in U], dtype=np.int16)[j]
    uy = y-a*np.asarray([p[1] for p in U], dtype=np.int16)[j]
    wx = x+b*np.asarray([p[0] for p in U], dtype=np.int16)[(j+s)%6]
    wy = y+b*np.asarray([p[1] for p in U], dtype=np.int16)[(j+s)%6]
    # Multiplication must not overflow the compact coordinate storage.
    gate = np.where(s > 0,
                    (a*uy.astype(np.int32)-b*ux.astype(np.int32)) % c,
                    c+(a*ux.astype(np.int32)-b*uy.astype(np.int32)) % c)
    gate = gate.astype(np.int16)

    def row(axis, px, py):
        axis = axis % 3
        px, py = px.astype(np.int32), py.astype(np.int32)
        return np.where(axis == 0, (py-ymin)*c+px % c,
               np.where(axis == 1, offsets[1]+(px-xmin)*c+py % c,
                        offsets[2]+(px+py-tmin)*c+py % c)).astype(np.int32)

    rows = np.stack((row(j, x, y), row(j, ux, uy),
                     row(j+s, wx, wy), row(j+s, x, y)))
    if rows.min() < 0 or rows.max() >= nr:
        raise ArithmeticError('Endpoint row escaped the board bounds')
    expected = {(33, 7, 37): 4207420, (35, 13, 43): 12830527}
    if (a, b, c) in expected and len(x) != expected[a, b, c]:
        raise ArithmeticError(f'Catalogue count {len(x)} != expected count')
    return Catalogue(a, b, c, board,
                     (xmin, xmax, ymin, ymax, tmin, tmax), offsets,
                     nr, x, y, j, s, eps, gate, rows)
