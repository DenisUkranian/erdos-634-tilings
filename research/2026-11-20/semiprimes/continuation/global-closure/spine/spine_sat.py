#!/usr/bin/env python3
"""Complete-row endpoint SAT restricted to the entire two-tree spine class.

This changes the incident oracle's admissibility predicate, not just its
initial catalogue. A certified UNSAT result closes this class only.
"""
from functools import lru_cache
from math import ceil,floor
from pathlib import Path
import argparse
import hashlib
import json
import pickle
import sys


SCOPE=('All contained placements with h=0,q in R; h=1,q in A+zR; '
       'or h=2,q in A+z^2R. This is the complete no-occupied-exterior-free-'
       'node class in both phase trees, not all unrestricted tilings.')


def locate_continuation():
    for ancestor in Path(__file__).resolve().parents:
        for candidate in (ancestor,ancestor/'repo/research/2026-11-20/semiprimes/continuation'):
            if (candidate/'global-endpoints/integer/global_core_sat.py').exists():
                return candidate
    raise FileNotFoundError('Pass --continuation pointing to the existing continuation package.')


def install_restriction(core,closed_gates=False):
    original_geometry=core.Geometry

    class SpineGeometry(original_geometry):
        @lru_cache(50000)
        def on_spine(self,tile):
            q,h,j,s=tile
            if h not in (0,1,2):
                return False
            shift=(self.A if h else 0,0,0)
            m=self.mult(self.sub(q,shift),self.unit(-h,0))
            denominator=self.power(m[2])
            return m[0]%denominator==0 and m[1]%denominator==0

        @lru_cache(50000)
        def admissible(self,tile):
            return self.on_spine(tile) and super().admissible(tile)

        def long_gate_open(self,tile):
            q,h,j,s=tile
            endpoint=self.add(q,self.scale(-self.a,self.unit(h,j)))
            return self.on_spine((endpoint,h+s,0,1))

        def mate(self,tile):
            q,h,j,s=tile
            offset=self.add(self.scale(-self.a,self.unit(h,j)),
                            self.scale(self.b,self.unit(h,j+s)))
            return self.add(q,offset),h,(j+3)%6,s

        def seed(self,path=None):
            if path:
                data=json.loads(Path(path).read_text())
                if isinstance(data,dict) and data.get('format')=='positive-endpoint-tiling-v1':
                    assert tuple(data['sides'])==(self.a,self.b,self.c)
                    for q,h,j,s in data['tiles']:
                        yield tuple(q),h,j,s
                    return
            yield from super().seed(path)

    core.Geometry=SpineGeometry

    class SpineSearch(core.Search):
        def __init__(self,args):
            super().__init__(args)
            self.journal.write('; RESTRICTED COMPLETE SPINE CLASS: '+SCOPE+'\n')

        def insert(self,tile):
            if tile in self.index:
                return self.index[tile]
            i=super().insert(tile)
            if closed_gates and not self.g.long_gate_open(tile):
                mate=self.g.mate(tile)
                if not self.g.admissible(mate):
                    self.assert_(f'(not x{i})')
                else:
                    k=self.insert(mate)
                    self.assert_(f'(= x{i} x{k})')
            return i

        def checkpoint(self,iteration,status):
            if status in ('global-unsat-needs-proof-audit','global-probe-unsat-needs-proof-audit'):
                status='spine-class-unsat-needs-proof-audit'
            super().checkpoint(iteration,status)
            status_path=self.out/'status.json'
            report=json.loads(status_path.read_text())
            report['format']='spine-integer-endpoint-v1'
            report['scope']=SCOPE
            report['oracle_predicate']='Exact native-coset test in Geometry.admissible, applied to every incident placement.'
            report['closed_long_gates_force_actual_mates']=closed_gates
            report['source_sha256']=hashlib.sha256(Path(core.__file__).read_bytes()).hexdigest()
            status_path.write_text(json.dumps(report,indent=2)+'\n')
            checkpoint=self.out/'checkpoint.pickle'
            with checkpoint.open('rb') as f:
                data=pickle.load(f)
            data['format']=report['format']
            data['scope']=SCOPE
            with checkpoint.open('wb') as f:
                pickle.dump(data,f)

        def run(self):
            print('RESTRICTED SPINE CLASS:',SCOPE,flush=True)
            super().run()
            old=self.out/'global_unsat.smt2'
            if old.exists():
                old.replace(self.out/'spine_unsat.smt2')
            print('SCOPE REMINDER: inherited necessary-model UNSAT messages refer only to the complete spine class.',flush=True)

    core.Search=SpineSearch
    return SpineGeometry


def main():
    parser=argparse.ArgumentParser(add_help=False)
    parser.add_argument('--continuation',type=Path)
    parser.add_argument('--corners',action='store_true')
    parser.add_argument('--closed-gates',action='store_true')
    args,rest=parser.parse_known_args()
    continuation=args.continuation or locate_continuation()
    sys.path.insert(0,str(continuation/'global-endpoints/integer'))
    import global_core_sat as core
    install_restriction(core,args.closed_gates)
    if args.corners:
        sys.path.insert(0,str(continuation/'vertex-phase'))
        import corner_search

        class SpineCornerOracle(corner_search.CornerOracle):
            @lru_cache(100000)
            def through_possible(self,p,ray):
                # A genuine half-fan endpoint and both endpoints of its
                # through-side belong to the same maximal supporting run.
                # The integral-offset theorem makes the displacement integral.
                unit=self.g.unit(*ray)
                for tile,low,high,length in self.through_intervals(p,ray):
                    q,h,j,s=tile
                    if h not in (0,1,2):
                        continue
                    for t in range(max(1,ceil(low)),min(length-1,floor(high))+1):
                        shifted=self.g.add(q,self.g.scale(-t,unit)),h,j,s
                        if self.g.admissible(shifted):
                            return True
                return False

        corner_search.CornerOracle=SpineCornerOracle
        sys.argv=[sys.argv[0],'--base-dir',str(continuation/'global-endpoints/integer'),*rest]
        corner_search.main()
    else:
        sys.argv=[sys.argv[0],*rest]
        core.main()


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Run without -O.')
    main()
