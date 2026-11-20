"""Replay the five signed inventories for the 250-tile pentagon."""
from itertools import product


def distributions():
    a, b, c, t, k, j = 35, 13, 43, 22, 17, 1
    total = 250
    heights = list(range(-1,3))
    short_residue = {0:t*t, 1:-k*k + j*(2*((t*c-k*a)//b)+j)}
    sign_residue = {0:t,1:k+j}
    choices = []
    for h in heights:
        choices.append([n for n in range(total+1)
                        if (n - short_residue.get(h,0))%c == 0
                        and (h in (0,1) or n != c)])
    for populations in product(*choices):
        if sum(populations) != total or populations[2] < 29:
            continue
        ranges = []
        for h,n in zip(heights,populations):
            ranges.append([s for s in range(-n,n+1,2)
                           if (s-sign_residue.get(h,0))%c==0])
        for signature in product(*ranges):
            G = dict(zip(heights,signature))
            if G[0]+G[2] != t or G[-1]+G[1] != k+j:
                continue
            n = dict(zip(heights,populations)); up={}
            for h in range(-2,4):
                d = a-b
                exterior = {0:d*t-c*(k+j),1:d*(k+j)-c*t}.get(h,0)
                numerator = d*G.get(h,0)-exterior
                assert numerator % c==0
                down = numerator//c - up.get(h-1,0)
                up[h+1] = G.get(h+1,0)-down
                if abs(up[h+1])+abs(down)>n.get(h+1,0):
                    break
            else:
                yield populations,signature


if __name__=="__main__":
    result=list(distributions())
    assert [p for p,g in result]==[(0,54,110,86),(0,54,196,0),(0,140,110,0),
                                  (86,54,110,0),(129,54,67,0)]
    for p,g in result:
        print(p,g)
