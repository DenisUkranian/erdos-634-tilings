"""Exact square-class tests and conservative constructive bounds.
No geometric existence is inferred from the local test at a small scale.
Standard library only. Trial division is intentionally simple, not a claim of
fast factorization for unrestricted large input.
"""
from __future__ import annotations
from math import gcd, isqrt


def positive_int(n: int) -> None:
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError('Expected a positive integer')


def factor(n: int) -> dict[int, int]:
    positive_int(n)
    out: dict[int, int] = {}
    p = 2
    while p*p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0)+1
            n //= p
        p = 3 if p == 2 else p+2
    if n > 1:
        out[n] = out.get(n, 0)+1
    return out


def squarefree_decomposition(n: int) -> tuple[int, int]:
    d = m = 1
    for p,e in factor(n).items():
        d *= p**(e % 2)
        m *= p**(e // 2)
    return d,m


def is_squarefree(d: int) -> bool:
    return all(e == 1 for e in factor(d).values())


def norm2_test(d: int) -> bool:
    """Negative norm -d in Z[sqrt(2)], for squarefree positive d."""
    if not is_squarefree(d):
        raise ValueError('The kernel d must be squarefree')
    return all(p == 2 or p % 8 in (1,7) for p in factor(d))


def norm3_test(d: int) -> bool:
    """Negative norm -d in Z[sqrt(3)], for squarefree positive d."""
    fs = factor(d)
    if any(e != 1 for e in fs.values()):
        raise ValueError('The kernel d must be squarefree')
    if any(p > 3 and p % 12 not in (1,11) for p in fs):
        return False
    return d % 3 == 2 if 3 not in fs else (d//3) % 3 == 1


def parameters(d: int, family: str = 'W') -> list[tuple[int,int]]:
    """All reduced primitive solutions d=k*v^2-u^2, 0<u<v.
    The finite bound is proved in PROOF.md, not guessed from a search limit.
    Degenerate norm cases d=1,2 (W) or d=2,3 (beta) need classical tilings.
    """
    positive_int(d)
    if not is_squarefree(d):
        raise ValueError('Expected a squarefree kernel')
    if family not in ('W','beta'):
        raise ValueError('Family must be W or beta')
    k = 2 if family == 'W' else 3
    result = []
    for v in range(2, isqrt((d-1)//(k-1))+1):
        r = k*v*v-d
        if r <= 0:
            continue
        u = isqrt(r)
        if u*u == r and u < v and gcd(u,v) == 1:
            result.append((u,v))
    return result


def bounds(u: int, v: int) -> dict[str,int]:
    if not (isinstance(u,int) and isinstance(v,int) and not isinstance(u,bool)
            and not isinstance(v,bool) and 0 < u < v and gcd(u,v) == 1):
        raise ValueError('Require primitive integers 0<u<v')
    a,b,c = u*v,v*v-u*u,v*v
    R = (c+b-1)//b
    H = (b+c*(R-1)+u-1)//u
    S = v*((H+v-1)//v)
    C = S+(u-1)*(v-1)
    return dict(a=a,b=b,c=c,Q=b+c,P=b+2*c,R=R,H=H,S=S,C=C)


def plan(u: int, v: int, m: int) -> dict[str,int]:
    """A multiples-of-v seed followed by fewer than v additions of u.
    Can accept some small scales, but never declares failure nonexistence.
    """
    positive_int(m)
    k = bounds(u,v)
    if m % v == 0:
        return dict(u=u,v=v,m=m,seed_scale=m,seed_factor=m//v,steps=0,
                    H=k['H'],C=k['C'])
    steps = (m*pow(u,-1,v)) % v
    seed = m-steps*u
    if seed < max(v,k['H']) or seed % v:
        raise ValueError('No certificate from this construction; this is not a NO result')
    return dict(u=u,v=v,m=m,seed_scale=seed,seed_factor=seed//v,
                steps=steps,H=k['H'],C=k['C'])


def classify(n: int) -> dict:
    d,m = squarefree_decomposition(n)
    answer = dict(N=n,squarefree_kernel=d,multiplier=m)
    if d in (1,2,3,6):
        return answer | dict(status='YES',reason='classical_square_multiple',coefficient=d)
    # This is the only global negative branch in this module.
    isolated = d % 16 == 14 and gcd(d*m,3) == 1 and m % 2 == 1
    if isolated and not norm2_test(d):
        return answer | dict(status='NO',reason='W_only_sector_inert_prime',
            obstructing_primes=[p for p in factor(d) if p>2 and p%8 not in (1,7)])
    candidates=[]
    for family,test in [('W',norm2_test),('beta',norm3_test)]:
        if not test(d):
            continue
        for u,v in parameters(d,family):
            bnd=bounds(u,v)
            try:
                p=plan(u,v,m)
            except ValueError:
                continue
            candidates.append((p['steps'],p['C'],family,u,v,p))
    if candidates:
        _,_,family,u,v,p=min(candidates)
        return answer | dict(status='YES',reason='explicit_construction_scheme',
                              family=family,parameters=[u,v],plan=p)
    return answer | dict(status='UNKNOWN',reason='outside_constructed_scales',
                          in_W_only_sector=isolated)
