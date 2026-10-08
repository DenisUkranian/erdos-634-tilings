#!/usr/bin/env python3
"""Exact exploratory 4830 search: ordinary grids and the known good F4.

Only a completed positive placement would establish a tiling. Timeouts and
recipe exhaustion are not unrestricted obstructions.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from math import isqrt
import argparse, json, sys, time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'f3-primitive-oct7'))
from macro_search import Search, E

class Mixed(Search):
    def __init__(self, max_macros, seconds, require_f4=True):
        super().__init__(24, 11, 31, max_macros=max_macros, seconds=seconds)
        conv = lambda p: (F(p[0]) + F(p[1], 2), F(p[1], 2))
        # F4(11,24,31): count 1610, already constructed in group2-f4.
        self.good = E.triangle(tuple(map(conv, [(0, 0), (1085, 0),
                        (F(1104*24, 31), F(1104*11, 31))])))
        self.require_f4 = require_f4
        self.sg = {24*a + 11*b + 31*c for a in range(61)
                   for b in range(132) for c in range(47)
                   if 24*a+11*b+31*c <= 1426}

    @lru_cache(None)
    def possible(self, n, slots, needed):
        if n == 0:
            return not needed
        if slots <= 0:
            return False
        # Keep the special-piece count explicit; the ordinary-grid sums
        # routine is a complete numerical pruning condition.
        return any(self.sums(n-1610*j, slots-j, isqrt(n-1610*j))
                   for j in range(int(needed), min(slots, n//1610)+1))

    def dfs_mixed(self, placed=(), kinds=()):
        self.check(); self.nodes += 1
        self.deepest = max(self.deepest, len(placed))
        n = self.n - sum(1610 if k == 'F4' else k*k for k in kinds)
        needed = self.require_f4 and 'F4' not in kinds
        slots = self.max_macros - len(placed)
        if n == 0:
            if needed: return False
            self.found = placed, kinds
            return True
        if not self.possible(n, slots, needed): return False
        key = tuple(sorted(placed))
        if key in self.dead: return False
        B = E.atomic_boundary(self.target, placed, self.check)
        for u, v in B:
            if any(E.on_segment(a,b,u) and E.on_segment(a,b,v)
                   for a,b in E.edges(self.target)):
                length=E.rational_sqrt(E.dot(E.sub(v,u),E.sub(v,u),3))
                if length.denominator != 1 or int(length) not in self.sg:
                    self.dead.add(key); return False
        templates = []
        if n >= 1610 and self.possible(n-1610, slots-1, False):
            templates.append(('F4', self.good))
        for k in range(isqrt(n), 0, -1):
            if self.possible(n-k*k, slots-1, needed):
                templates.append((k,self.templates[k]))
        best = None
        for sector in E.convex_sectors(B,3)[:4]:
            ps = [(k,t) for k,tmp in templates
                  for t in E.placements(tmp,sector,self.target,placed,3,self.check)]
            if best is None or len(ps)<len(best):best=ps
            if not best:break
        for k,t in best:
            if self.dfs_mixed(placed+(t,),kinds+(k,)):return True
        self.dead.add(key); return False

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--max-macros',type=int,default=5)
    p.add_argument('--seconds',type=float,default=120)
    p.add_argument('--output',type=Path)
    a=p.parse_args();s=Mixed(a.max_macros,a.seconds)
    s.start=time.monotonic()
    try:r=s.dfs_mixed()
    except (E.BudgetExceeded,RecursionError):r=None
    out={'status':'FOUND' if r else 'RESTRICTED_EXHAUSTED' if r is False else 'INCOMPLETE',
         'nodes':s.nodes,'deepest':s.deepest,'seconds':time.monotonic()-s.start,
         'tile':[24,11,31],'count':4830,'max_macros':a.max_macros,
         'required_macro':'At least one known F4(11,24,31), tile count 1610',
         'other_macros':'Integer-scaled copies of the original tile',
         'scope':'Exploratory construction search, not a nonexistence certificate',
         'full_Erdos634_solved':False,
         'macros':None if s.found is None else [
             {'kind':k,'vertices':E.encode_tri(t)} for t,k in zip(*s.found)]}
    if a.output:a.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
