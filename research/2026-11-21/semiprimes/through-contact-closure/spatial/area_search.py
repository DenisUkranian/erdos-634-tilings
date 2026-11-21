#!/usr/bin/env python3
"""Whole-contact search with exact area and charge cuts on supported polygons."""
import argparse
from copy import deepcopy
import gzip
import json
from pathlib import Path
import sys

PACKAGE=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(PACKAGE/'population'),str(PACKAGE/'whole-edges'),str(PACKAGE/'corner-tests')]
import whole_edge_search as driver
from area_cycles import selected_area_cycles
from verify_area_cycles import check_witness
from pattern_isometries import pattern_isometries,pattern_key,transform_area_witness


def area_extension(base,quota=4,corner_bank_file=None,isometry_seed_file=None,propagate=False):
    class AreaSearch(base):
        def __init__(self,args):
            self.area_records={}
            self.pattern_seeds={}
            self.pattern_history=[]
            self.use_patterns=bool(propagate or isometry_seed_file)
            super().__init__(args)

        def install_area_witness(self,witness,seed=True):
            key=tuple(sorted(witness['indices']))
            if seed and self.use_patterns:
                support=pattern_key(self.g,self.tiles,witness['indices'])
                self.pattern_seeds.setdefault(support,witness)
            if key in self.area_records:
                return 0
            self.area_records[key]=witness
            self.assert_('(not (and '+' '.join(f'x{i}' for i in key)+'))')
            return 1

        def propagate_area_patterns(self):
            if not self.use_patterns:
                return 0
            added=0
            for witness in self.pattern_seeds.values():
                for occurrence in pattern_isometries(self.g,self.tiles,self.index,witness['indices']):
                    key=tuple(occurrence['indices'])
                    if key in self.area_records:
                        continue
                    mapped=transform_area_witness(self.g,witness,occurrence)
                    added+=self.install_area_witness(mapped,seed=False)
            self.pattern_history.append(dict(columns=len(self.tiles),
                seed_patterns=len(self.pattern_seeds),new_isometric_cuts=added,
                total_area_cuts=len(self.area_records)))
            print('ISOMETRIC_AREA_CUTS',json.dumps(self.pattern_history[-1],sort_keys=True),flush=True)
            return added

        def refine_fans(self,chosen,residual):
            added=0
            for witness in selected_area_cycles(self.g,self.tiles,chosen,max_cycles=quota):
                added+=self.install_area_witness(witness)
            if self.history:
                self.history[-1]['new_area_charge_cycle_cuts']=added
            if added:
                print('AREA_CHARGE_CUTS',added,flush=True)
            refined=super().refine_fans(chosen,residual)
            self.propagate_area_patterns()
            return refined

        def boundary(self):
            super().boundary()
            if corner_bank_file:
                catalogue=json.loads(Path(corner_bank_file).read_text())
                assert tuple(catalogue['sides'])==tuple(self.args.sides)
                placements={self.canonical_tile(t) for root in catalogue['surviving_roots']
                            for t in root['tiles']}
                for tile in sorted(placements):
                    self.install_tile_edges(tile)
                print('ALL_CORNER_BANKS',len(placements),flush=True)
            path=getattr(self.args,'model_checkpoint',None)
            if path:
                self.restore_area_source(path)
            if isometry_seed_file:
                self.restore_area_source(isometry_seed_file)
            self.propagate_area_patterns()

        def restore_area_source(self,path):
            raw=Path(path).read_bytes()
            if str(path).endswith('.gz'):
                raw=gzip.decompress(raw)
            source=json.loads(raw)
            assert tuple(source['sides'])==tuple(self.args.sides)
            old_tiles=[self.canonical_tile(t) for t in source['tiles']]
            for original in source.get('general_area_cycle_cuts',[]):
                all_owners={i for edge in original['edges'] for i in edge['selected_owners']}
                check_witness(self.g,old_tiles,all_owners,original)
                assert original['budget']['violations']
                mapping={i:self.insert(old_tiles[i]) for i in original['indices']}
                witness=deepcopy(original)
                witness['indices']=sorted(mapping.values())
                for edge in witness['edges']:
                    edge['representative']=mapping[edge['representative']]
                    edge['selected_owners']=[edge['representative']]
                check_witness(self.g,self.tiles,witness['indices'],witness)
                self.install_area_witness(witness)

        def necessary_snapshot(self):
            snapshot=super().necessary_snapshot()
            snapshot['general_area_cycle_cuts']=[v for _,v in sorted(self.area_records.items())]
            snapshot['general_area_cycle_rule']='integral-tile-area-and-two-signed-characters-v1'
            return snapshot

        def checkpoint(self,iteration,status):
            super().checkpoint(iteration,status)
            path=self.out/'status.json'
            report=json.loads(path.read_text())
            report.update(general_area_cycle_cuts=len(self.area_records),
                          isometry_seed_patterns=len(self.pattern_seeds),
                          isometry_propagation=self.pattern_history)
            path.write_text(json.dumps(report,indent=2)+'\n')

    return AreaSearch


def main():
    options=argparse.ArgumentParser(add_help=False)
    options.add_argument('--allocation',choices=('unsigned','joint'),default='unsigned')
    options.add_argument('--area-cuts-per-round',type=int,default=4)
    options.add_argument('--corner-bank-file',help='Query every side of every listed corner placement; no corner root is forced.')
    options.add_argument('--isometry-seeds',help='Verified supported-polygon seeds to propagate among existing whole candidates.')
    options.add_argument('--propagate-isometries',action='store_true')
    args,rest=options.parse_known_args()
    assert args.area_cuts_per_round>=0
    if args.allocation=='unsigned':
        from population_whole_edge_search import PopulationWholeEdgeSearch as base
    else:
        from joint_whole_edge_search import JointWholeEdgeSearch as base
    sys.argv=[sys.argv[0],*rest]
    driver.WholeEdgeSearch=area_extension(base,args.area_cuts_per_round,args.corner_bank_file,
                                        args.isometry_seeds,args.propagate_isometries)
    driver.main()


if __name__=='__main__':main()
