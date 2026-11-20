"""Construct the two-grid notch theorem in exact Eisenstein coordinates."""
from itertools import combinations

from verify_control import det, edges, length2, separates


def grid_tiles(a, b, c, t, k):
    """Return all CCW tiles, in the Eisenstein frame scaled by c."""
    assert a > b > 0 and a*a + a*b + b*b == c*c
    assert k > 0 and t >= a + c*((k+a-1)//a)
    # Coordinates in this construction begin in the radial (1,z) frame.
    def physical(p):
        x, y = p
        return (c*x+a*y, b*y)

    def cell(i, j, dx, dy):
        x, y = i*dx, j*dy
        p, q, r, s = map(physical, [(x,y), (x+dx,y), (x,y+dy), (x+dx,y+dy)])
        return [(p,q,r), (s,r,q)]

    coarse_size = a*c
    coarse = {(i,j) for i in range((k+a-1)//a) for j in range((k+c-1)//c)
              if i*a+j*c < k}
    tiling = []
    for i in range(t):
        for j in range(t-i):
            if (i*a//coarse_size, j*c//coarse_size) in coarse:
                continue
            pair = cell(i,j,a,c)
            tiling.append(pair[0])
            if i+j+2 <= t:
                tiling.append(pair[1])

    for coarse_i,coarse_j in sorted(coarse):
        for i in range(coarse_i*a,(coarse_i+1)*a):
            for j in range(coarse_j*c,(coarse_j+1)*c):
                pair = cell(i,j,c,a)
                if i+j >= k:
                    tiling.append(pair[0])
                if i+j+1 >= k:
                    tiling.append(pair[1])
    return tiling


def check(a,b,c,t,k):
    tiling=grid_tiles(a,b,c,t,k)
    board=[(t*a*c,0),(t*a*c,t*b*c),(k*a*a,k*a*b),(k*c*c,0)]
    assert len(tiling)==t*t-k*k
    expected=sorted((u*c)**2 for u in (a,b,c))
    for tri in tiling:
        assert det(*tri)==a*b*c*c
        assert sorted(length2(p,q) for p,q in edges(tri))==expected
        assert all(det(p,q,r)>=0 for p,q in edges(board) for r in tri)
    assert all(separates(x,y) or separates(y,x) for x,y in combinations(tiling,2))
    assert sum(p[0]*q[1]-p[1]*q[0] for p,q in edges(board))==sum(map(lambda r:det(*r),tiling))
    print((a,b,c,t,k),len(tiling),"tiles checked")


if __name__=="__main__":
    for pars in [(5,3,7,12,5),(5,3,7,14,5),(5,3,7,19,9),(8,7,13,21,4)]:
        check(*pars)
