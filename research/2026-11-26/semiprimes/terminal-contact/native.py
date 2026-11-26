"""Signed physical-bank profiles below the new nonnative thresholds."""
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"boundary-word"))
from remote import inventories


def profiles(a, b, c, first_free):
    limit = first_free - 1
    d = a-b
    rows = []
    for k in range(-(limit//c), limit//c+1):
        p, q, t, v = -2*c-d*k, -d-c*k, c*k, c+d*k
        bank_floor = sum(map(abs, (p,q,t,v)))
        if bank_floor > limit:
            continue
        first = min((m for m, _, _ in inventories(a,b,c,1,p,q,limit-c)), default=limit+1)
        second = min((m for m, _, _ in inventories(a,b,c,2,t,v,limit-c)), default=limit+1)
        if first + second <= limit:
            rows.append((k, (p,q,t,v), first+second, (limit-bank_floor)//2))
    return rows


if __name__ == "__main__":
    for a,b,c,threshold,expected in [
        (33,7,37,123,[(-1,(-48,11,-37,11),107,7)]),
        (35,13,43,165,[(-1,(-64,21,-43,21),149,7),(0,(-86,-22,0,43),151,6)]),
    ]:
        assert profiles(a,b,c,threshold)==expected
        print("Small-M native bank profiles", c, expected)
