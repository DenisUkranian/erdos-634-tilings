"""Exhaust the signed cut relaxation below a fixed unmatched-tile ceiling."""
from itertools import product


def cut_rows(c, d, k, limit):
    bound = limit // c
    rows = []
    for even, odd in product(range(-bound, bound + 1), repeat=2):
        if c*(abs(even)+abs(odd)) > limit:
            continue
        diff = (c-d)*(even+odd)-c
        summ = (-1)**k * ((c+d)*(even-odd)+c)
        if (diff+summ)%2:
            continue
        p, q = (summ+diff)//2, (summ-diff)//2
        lower = max(c, abs(p)+abs(q))
        lower += (lower-p-q)%2
        if lower <= limit-c:
            rows.append((p, q, c*even, c*odd, lower))
    return rows


def candidates(a, b, c):
    d = a-b
    limit = 3*c+d
    result = []
    for first, second in product(cut_rows(c,d,1,limit), cut_rows(c,d,2,limit)):
        p,q,e,o,m = first
        t,v,f,j,k = second
        charges = (-d-e-q, -c-o, e-f, o-j-p-v, f-t, j)
        lower = m+k+sum(map(abs,charges))
        if lower <= limit:
            result.append((lower, (p,q,t,v), (m,k), charges))
    return sorted(result)


if __name__ == "__main__":
    for a,b,c,minimum in [(5,3,7,23),(33,7,37,107),(35,13,43,149)]:
        rows = candidates(a,b,c)
        assert rows[0][0] == minimum
        if c in (37,43):
            assert [(r[1],r[3]) for r in rows if r[0]==minimum] == [
                ((-2*c+a-b, c-a+b, -c, c-a+b), (0,)*6)]
        print((a+2*b)*(2*a+b), rows)
