"""Local necessary tile costs for the two F2 boards, in reflected path signs."""
from functools import lru_cache

from hull import ceil_div


class Layers:
    def __init__(self, c, d, A, D, W, V, core_allowance):
        self.c, self.d, self.A, self.D = c, d, A, D
        self.W, self.V, self.core_allowance = W, V, core_allowance
        self.ranges = (range(-(W//2), W//2+1), range(-((V-1)//2), (V+1)//2+1))

    @lru_cache(None)
    def cost(self, signed, inward, outward, core=False):
        """One distinguished gate, all other gates combined, one short lift."""
        assert inward + outward == signed
        c, A, D = self.c, self.A, self.D
        floor = (64 if c == 37 else 75) if core else 0
        offset = self.core_allowance if core else 0
        aligned = signed if inward >= 0 else -signed
        capacity = ceil_div(2*D*abs(inward) + (D-2*A)*aligned - 2*offset, D)
        lower = max(floor, abs(inward)+abs(outward), capacity)
        residue = (19 if c == 37 else 5) if core else 0
        initial = signed + 2*residue
        n = initial + 2*c*max(0, ceil_div(lower-initial, 2*c))
        if not core and (n == c or (c == 43 and n == abs(signed) == 2*c)):
            n += 2*c
        return n

    def step_cost(self, x, y, z):
        c, d = self.c, self.d
        return self.cost(c*(x-z), c*x-d*y, d*y-c*z)

    def side(self, even, odd, axial, forest):
        c, d = self.c, self.d
        source = d if axial else 0
        inward = c*even - d*odd + source
        return min(self.cost(c*(even-z)+source, inward, d*odd-c*z, core=axial)
                   + forest[1, odd, z] for z in self.ranges[0])
