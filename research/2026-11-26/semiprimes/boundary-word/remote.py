"""Exact nonnative unmatched floors using two distinguished physical cuts."""
from itertools import product
from nested import cut_rows


def norm_hex(x, y):
    return max(abs(x), abs(y), abs(x+y))


def signed_axes(x, y, char):
    middle, remainder = divmod(char-x+y, 3)
    if remainder:
        return None
    return middle+x, middle, middle-y


def inventories(a,b,c,k,p,q,cap):
    A, B = b*(2*a+b), a*(a+2*b)
    X, Y = A, -B
    if k == 2:
        X, rx = divmod((a+b)*A-b*B, c)
        Y, ry = divmod(-b*A-a*B, c)
        assert not rx and not ry
    for x in range(-cap, cap+1):
        for y in range(max(-cap, -cap-x), min(cap, cap-x)+1):
            u, rx = divmod(X-a*x+b*y, c)
            v, ry = divmod(Y-b*x-(a+b)*y, c)
            if rx or ry or norm_hex(u,v)+norm_hex(x,y)>cap:
                continue
            left = signed_axes(u,v,-p)
            right = signed_axes(x,y,q)
            if left is None or right is None:
                continue
            length = sum(map(abs,left+right))
            if length <= cap:
                yield length, left, right


def exclusions(a,b,c,free_cost,threshold):
    # Search strictly below the proposed threshold. The cap is valid because
    # each distinguished edge needs at least c crossings in physical length.
    cap = threshold-1
    options = []
    for k in (1,2):
        current = []
        for p,q,e,o,_ in cut_rows(c,a-b,k,cap):
            row = min(inventories(a,b,c,k,p,q,cap-c), default=None)
            if row:
                current.append((p,q,e,o,row[0]))
        options.append(current)
    for first, second in product(*options):
        p,q,e,o,m = first
        t,v,f,j,k = second
        residual = (b-a-e-q,-c-o,e-f,o-j-p-v,f-t,j)
        assert m+k+max(free_cost,sum(map(abs,residual))) >= threshold
    return [len(rows) for rows in options]


if __name__ == "__main__":
    for a,b,c,cost,threshold in [(33,7,37,10,117),(35,13,43,12,161)]:
        assert 7*(cost-2)**2*c*c < 36*2*c*a*b
        assert cost <= min(c-(a-b),c+(a-b))
        print(c, "directional profiles", exclusions(a,b,c,cost,threshold),
              "nonnative floor", threshold)
