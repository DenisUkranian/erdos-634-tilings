"""Exact physical area bounds from the six unsigned axis counts of a neutral cut."""
from itertools import combinations
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "2026-11-26/semiprimes/terminal-contact"))
from remote_boundary import identity

def det(p, q):
    return p[0]*q[1] - p[1]*q[0]

def axes(v):
    x, y = v
    return [v, (-y,x+y), (-x-y,x)]

def zeros(a,b,c,m):
    """Enumerate all two-bank signed axis vectors with zero character and closed sum."""
    solution = {}
    for bank in (axes((a+b,-b)), axes((c,0))):
        by_point = {}
        for x in range(-m,m+1):
            for z in range(-m,m+1):
                s = (x,x+z,z)
                if sum(map(abs,s)) > m:
                    continue
                p = tuple(sum(t*v[i] for t,v in zip(s,bank)) for i in range(2))
                by_point[p] = s
        if not solution:
            solution = by_point
        else:
            for p,s in by_point.items():
                other = solution.get((-p[0],-p[1]))
                if other is not None and sum(map(abs,other+s)) <= m:
                    yield other+s

def splits(total, size):
    if size == 1:
        yield (total,)
        return
    for v in range(total+1):
        for tail in splits(total-v, size-1):
            yield (v,)+tail

def table(a,b,c,limit):
    directions = axes((a+b,-b)) + axes((c,0))
    terms = [(i,j,abs(det(directions[i],directions[j]))) for i,j in combinations(range(6),2)]
    minima = {tuple(map(abs,s)) for s in zeros(a,b,c,limit)}
    rows = {}
    for m in range(16,limit+1,2):
        best = 0
        maximizers = set()
        for base in minima:
            rem = m-sum(base)
            if rem < 0 or rem%2:
                continue
            for pairs in splits(rem//2,6):
                v = [n+2*k for n,k in zip(base,pairs)]
                if not sum(v[:3]) or not sum(v[3:]):
                    continue
                score = sum(k*v[i]*v[j] for i,j,k in terms)
                if score > best:
                    best = score
                    maximizers.clear()
                if score == best:
                    maximizers.add(tuple(v))
        cap = best//(4*a*b*c)*(2*c)
        equal_word = False
        if cap and best == 2*a*b*cap:
            # At equality the boundary is half the zonotope. Each side is whole.
            def allowed(v):
                if any(k%2 for k in v):
                    return False
                word = [token for j in range(6)
                        for token,count in [(j,v[j%3]),(6+j,v[3+j%3])]
                        for _ in range(count//2)]
                return all(identity(word,a,b,c,order) for order in (a,b))
            equal_word = not any(allowed(v) for v in maximizers)
            if equal_word:
                cap -= 2*c
        rows[m] = dict(determinant_sum=best, equality_word_rejected=equal_word,
                       maximizing_inventories=len(maximizers),
                       population_cap=min(cap,2*c) if m==16 else cap)
    return rows

if __name__ == '__main__':
    import json
    out = {}
    for a,b,c,m in [(33,7,37,42),(35,13,43,22)]:
        rows = table(a,b,c,m)
        disjoint = max((row['population_cap']+rows[j]['population_cap']
                        for i,row in rows.items() for j in rows if i+j<=m),default=None)
        out[c] = dict(cuts=rows, one=max(v['population_cap'] for v in rows.values()),
                      two_disjoint=disjoint)
    print(json.dumps(out,indent=2))
