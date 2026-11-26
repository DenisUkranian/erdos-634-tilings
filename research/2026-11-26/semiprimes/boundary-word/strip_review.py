"""Independent relaxed lower bound by sweeping residual integer rows."""
from itertools import product


def minimum(a,b,c):
    bound = c,b,c-a
    allowed = {a*i+b*j for i in range(c*b//a+1) for j in range(c+1)}
    best = None
    for residue in range(b):
        # Keep the minimum accumulated rectangle area per state. Subsequent
        # admissibility in this independent relaxation depends only on counts.
        distance = {(0,0,0):0}
        for state in product(*(range(n+1) for n in bound)):
            if state not in distance:
                continue
            i,j,k = state
            width = b*i-c*j
            depth = a*i+c*k
            choices = [(i<c and width in allowed,a*width),
                       (j<b and (-depth)%b==residue,0),
                       (k<c-a and width in allowed and width%a==0,c*width)]
            for axis,(ok,area) in enumerate(choices):
                if ok:
                    to = list(state)
                    to[axis] += 1
                    to = tuple(to)
                    new = distance[state]+area
                    distance[to] = min(new,distance.get(to,new))
        if bound in distance:
            value = distance[bound]
            best = value if best is None else min(best,value)
    assert best is not None
    count,rem = divmod(2*best,a*b)
    assert rem==0
    return c+count


if __name__=="__main__":
    assert minimum(33,7,37)==925
    assert minimum(35,13,43)==1247
    print("Minimum cell populations independently verified from slices alone.")
