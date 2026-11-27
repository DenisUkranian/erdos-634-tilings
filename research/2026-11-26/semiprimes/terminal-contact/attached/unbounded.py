"""Two sheet paths via binary endpoint currents, with no cutoff on path length."""
from collections import defaultdict
from itertools import combinations, product
from native_owners import UNITS, add, board, compatible, inside, offsets, scale, shape
from terminal import det
from middle_pairs import valid


def xor_basis(edges, column):
    basis = {}
    kernel = []
    for i, edge in enumerate(edges):
        value, support = column(*edge), 1<<i
        while value:
            p = value.bit_length()-1
            if p not in basis:
                basis[p] = value,support
                break
            v,u = basis[p]
            value ^= v
            support ^= u
        else:
            kernel.append(support)
    return basis,kernel


def normal(value, basis):
    support = remainder = 0
    while value:
        k = value.bit_length()-1
        if k in basis:
            z,m = basis[k]
            value ^= z
            support ^= m
        else:
            value ^= 1<<k
            remainder ^= 1<<k
    return remainder,support


def system(a,b,c,s,j):
    V = board(a,b,c)
    v = offsets(a,b,c,s,j)[0][6]
    sheets = []
    for shift in ((0,0),v):
        # Rational bounding box with a one-step coset shift on either side.
        bounds = [(min(t[i] for t in V)//(c*c)-3, max(t[i] for t in V)//(c*c)+4) for i in (0,1)]
        sheets.append({p for x,y in product(*(range(l,r) for l,r in bounds))
                       if inside(scale(c,p:=add(shift,(c*x,c*y))),V)})
    A,B = sheets
    edges = [(p,q,k) for sheet in sheets for p in sorted(sheet) for k in range(3)
             if (q:=add(p,scale(c,UNITS[k]))) in sheet]
    rows = {}
    def bit(key):
        return 1 << rows.setdefault(key,len(rows))
    def column(p,q,k,exception=False):
        result = bit(p)^bit(q)
        for m in (a,b):
            axis = (k+(s if exception and m==a else 0))%3
            for x,y in (p,q):
                result ^= bit((m,axis,x%m,y%m))
        return result
    basis,kernel = xor_basis(edges,column)
    groups = defaultdict(list)
    for p in sorted(A):
        q = add(p,v)
        if q in B:
            remainder,support = normal(column(p,q,j,True),basis)
            groups[remainder].append((p,support))
    return edges,kernel,groups


def words(a,b,c,s,j):
    edges,kernel,groups = system(a,b,c,s,j)
    v = offsets(a,b,c,s,j)[0][6]
    dest = scale(c,(a+b,-b))
    index = {tuple(sorted((p,q))):i for i,(p,q,k) in enumerate(edges)}
    canonical = 0
    p = (0,0)
    for k in [0]*a+[5]*b:
        q = add(p,scale(c,UNITS[k]))
        canonical |= 1<<index[tuple(sorted((p,q)))]
        p = q
    masks = [0]
    for vector in kernel:
        masks += [m^vector for m in masks]
    incidence = defaultdict(list)
    for i,(p,q,k) in enumerate(edges):
        incidence[p].append((1<<i,q,k))
        incidence[q].append((1<<i,p,(k+3)%6))
    degrees = {p:sum(bit for bit,q,k in ls) for p,ls in incidence.items()}

    def walk(mask,p,q):
        bridges = {}
        for u in (p,q):
            z = add(u,v)
            bridges[u],bridges[z] = (z,6),(u,7)
        for u in bridges:
            if (mask & degrees.get(u,0)).bit_count() != int(u not in ((0,0),dest)):
                return
        cur = (0,0)
        seen = set()
        path = []
        area = 0
        while cur != dest:
            if cur in seen:
                return
            seen.add(cur)
            ls = [t for t in incidence[cur] if t[0]&mask]
            if cur in bridges:
                ls.append((0,*bridges[cur]))
            if len(ls)!=1:
                return
            bit,u,k = ls[0]
            if bit:
                mask ^= bit
            else:
                del bridges[u],bridges[cur]
            area += det(cur,u)
            cur = u
            path.append(k)
        if mask or bridges or area>=0 or -area%(a*b*c) or (-area//(a*b*c))%2==0:
            return
        for m in (a,b):
            stack = []
            def push(k,power):
                if stack and stack[-1][0]==k:
                    power += stack.pop()[1]
                if power%m:
                    stack.append((k,power%m))
            for t in path:
                k = t if t<6 else (j+(s if m==a else 0)+(3 if t==7 else 0))%6
                e = 1 if t<6 else (b if m==a else a)*pow(c,-1,m)
                push(k%3,e if k<3 else -e)
            push(2,b)
            push(0,-a)
            if stack:
                return
        return ''.join(map(str,path)),-area//(a*b)

    passing = []
    for g in groups.values():
        for (p,x),(q,y) in combinations(g,2):
            for correction in masks:
                w = walk(canonical^x^y^correction,p,q)
                if w is not None and shape(a,b,c,s,j,w[0]):
                    passing.append(w)
    return len(kernel), sorted(passing)


def check():
    singles = {}
    rows = {}
    for s in (1,-1):
        rows[s] = []
        for j in range(6):
            if (j+s)%3==0:
                continue
            dim,passing = words(33,7,37,s,j)
            singles[f'{s},{j}'] = dict(nullity=dim,paths=len(passing),
                                       cap_counts=sorted({n for w,n in passing}))
            rows[s].extend((j,w,n,shape(33,7,37,s,j,w)) for w,n in passing)
    pairs = [[j,k,n,m,w,u] for (j,w,n,C),(k,u,m,T) in product(rows[1],rows[-1])
             if n-m>=74 and compatible(C,T)]
    assert len(pairs)==4 and sorted(n-m for j,k,n,m,w,u in pairs)==[74,74,148,148]
    assert all(valid(33,7,37,(n,j,w),(m,k,u)) < 3 for j,k,n,m,w,u in pairs)
    return dict(single_paths=singles, geometric_pairs=pairs,
                forced_two_lift_cases=[r for r in pairs if r[2]-r[3]==148])


if __name__=='__main__':
    import json
    if not __debug__:
        raise SystemExit('Assertions must be enabled.')
    print(json.dumps(check(),indent=2))
