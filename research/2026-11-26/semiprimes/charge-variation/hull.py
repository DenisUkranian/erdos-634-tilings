"""Bound odd charge variation using distinct physical owners and the charge tree."""
from functools import lru_cache


def ceil_div(n, d):
    return -(-n // d)


def degree_profiles(c, d, num, den, maximum_charge, budget):
    """(charge, half-excess cost, 2 - degree) with dominated options removed."""
    profiles = []
    for k in range(1, maximum_charge + 1):
        best_previous = budget + 1
        min_minority = int(k == 1 or (c == 43 and k == 2))
        for degree in range(1, 2*c + 1):
            best = budget + 1
            for x in range(min_minority, budget//c + 1):
                cap = num*c*k//den + c*x
                outside = ceil_div(c*k - degree*cap, d)
                best = min(best, c*x + max(0, c*outside - d*k))
            if best < best_previous:
                profiles.append((k, best, 2-degree))
                best_previous = best
            if best == 0:
                break
    return profiles


def maximum_degree_surplus(c, d, num, den, N, variation):
    budget = (N - (c+d)*variation)//2
    plus, minus = (variation+1)//2, (variation-1)//2
    profiles = degree_profiles(c, d, num, den, plus, budget)
    impossible = -10**6
    rows = [[impossible]*(budget+1) for _ in range(plus+1)]
    rows[0] = [0]*(budget+1)
    for total in range(1, plus+1):
        for k, cost, surplus in profiles:
            if k > total:
                break
            for available in range(cost, budget+1):
                prev = rows[total-k][available-cost]
                if prev != impossible:
                    rows[total][available] = max(rows[total][available], prev+surplus)
    return max(rows[plus][i]+rows[minus][budget-i] for i in range(budget+1))


def independent_test(c, d, num, den, N, variation):
    """Separate exact-cost recursion returning minimum total degree minus twice order.

    Enumerate minority populations and scan the possible gate total dj directly.
    For a given allocation we take the least possible degree, calculated by
    dividing the required current by one gate capacity.
    """
    plus, minus = (variation+1)//2, (variation-1)//2
    budget = (N-(c+d)*variation)//2
    choices = {}
    for k in range(1, plus+1):
        for m in range(0, budget+1, c):
            if m == 0 and k in ((1, 2) if c == 43 else (1,)):
                continue
            cap = (num*(c*k+m)+(den-num)*m)//den
            # j<0 cannot improve the budget or reduce the necessary degree.
            for j in range((budget-m+d*k)//c + 1):
                degree = max(1, ceil_div(c*k-d*j, cap))
                if degree > 2*c:
                    continue
                cost = m + max(0, c*j-d*k)
                key = k, cost
                choices[key] = min(choices.get(key, 2*c), degree-2)

    @lru_cache(None)
    def best(total, available):
        if total == 0:
            return 0
        return min((penalty + best(total-k, available-cost)
                    for (k, cost), penalty in choices.items()
                    if k <= total and cost <= available), default=10**6)

    return -min(best(plus,i)+best(minus,budget-i) for i in range(budget+1))


def check():
    report = {}
    for c,d,num,den,N,expected in [
        (37,26,43,222,3431,{53:-1,51:0}),
        (43,22,8,43,5063,{77:-4,75:-2,73:-1,71:1}),
    ]:
        assert N//(c+d) in (max(expected),max(expected)+1)
        for variation, score in expected.items():
            assert maximum_degree_surplus(c,d,num,den,N,variation) == score
            assert independent_test(c,d,num,den,N,variation) == score
        report[str(N)] = {str(k):v for k,v in expected.items()}
    return report
