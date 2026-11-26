"""A bounded-inventory free-product grammar for positioned directed walks."""
from functools import lru_cache
from itertools import product

from geometry import HEADINGS, add, det


def back(mask, shift):
    return mask >> shift if shift >= 0 else mask << (-shift)


@lru_cache(maxsize=64)
def program(profile, a, c, s, directions):
    """Each entry lists pairs of previous entries whose paths may be concatenated."""
    axes = [(j if i < 3 else j+s) % 3 for i,j in enumerate(HEADINGS)]
    factors = [[i for i in range(6) if axes[i]==k] for k in range(3)]
    coefficient = [(p[0] if k==0 else p[1]) % a for p,k in zip(directions,axes)]
    neutral, unrestricted = [], []
    for i,j in factors:
        options = list(product(range(profile[i]+1),range(profile[j]+1)))
        unrestricted.append(options)
        neutral.append([(x,y) for x,y in options if (coefficient[i]*x+coefficient[j]*y)%a==0])
    # A value in factor k has zero abelian residue in the two other factors.
    states = {}
    for k in range(3):
        choices = neutral.copy()
        choices[k] = unrestricted[k]
        for pairs in product(*choices):
            v = [0]*6
            for (i,j),(x,y) in zip(factors,pairs):
                v[i],v[j] = x,y
            states.setdefault(tuple(v),[]).append(k)

    zero = (0,)*6
    lookup = {(zero,k):6 for k in range(3)}
    neutral_ids = []
    displacements = list(directions)+[(0,0)]
    rules = []
    def emit(terms, target):
        terms = list(dict.fromkeys(terms))
        for left,right in terms:
            assert add(displacements[left],displacements[right]) == target
            assert det(displacements[left],displacements[right]) % (a*c) == 0
        rules.append(terms)
        displacements.append(target)
        return len(displacements)-1

    for v, possible in sorted(states.items(),key=lambda item:sum(item[0])):
        if v == zero:
            continue
        target = tuple(sum(n*d[i] for n,d in zip(v,directions)) for i in (0,1))
        if target == (0,0) and v != profile:
            continue
        remainders = [(i,tuple(x-y for x,y in zip(v,q))) for q,i in neutral_ids
                      if all(x>=y for x,y in zip(v,q))]
        all_terms = []
        for k in possible:
            terms = []
            for i in factors[k]:
                if v[i]:
                    tail = list(v)
                    tail[i] -= 1
                    node = lookup.get((tuple(tail),k))
                    if node is not None:
                        terms.append((i,node))
            for i,tail in remainders:
                node = lookup.get((tail,k))
                if node is not None:
                    terms.append((i,node))
            if len(possible)==3:
                all_terms.extend(terms)
            elif terms:
                lookup[v,k] = emit(terms,target)
        if all_terms:
            node = emit(all_terms,target)
            neutral_ids.append((v,node))
            for k in range(3):
                lookup[v,k] = node
    assert lookup[profile,0] == len(displacements)-1
    return rules, displacements


def shifted_program(rules, shifts):
    offsets = list(shifts)+[0]
    for terms in rules:
        left,right = terms[0]
        offsets.append(offsets[left]+offsets[right])
    return offsets


def boolean(rules, offsets, edges, vertices):
    starts = [*edges, vertices]
    for terms in rules:
        mask = 0
        for left,right in terms:
            if starts[left] and starts[right]:
                mask |= starts[left] & back(starts[right],offsets[left])
        starts.append(mask)
    return starts[-1]


def restrict_edges(edges, shifts, vertices):
    return [edge & vertices & back(vertices,shift) for edge,shift in zip(edges,shifts)]
