#!/usr/bin/env python3
"""Permanent whole-edge contact constraints with unrestricted actual tiles."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import sys

PACKAGE=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(PACKAGE/'owned'),str(PACKAGE/'spatial'),str(PACKAGE/'corner-tests')]
from spatial_search import SpatialSearch
from owned_search import OwnedSearch,defaults,GracefulResourceStop
from legacy import core,or_
from exact_geometry import polygon_record,records_overlap
from long_cycles import selected_long_cycles
from whole_edge_oracle import WholeEdgeOracle


class WholeEdgeSearch(SpatialSearch):
    def __init__(self,args):
        self.edge_catalogues={}
        self.edge_obligations={}
        self.edge_bank_cliques=set()
        self.edge_neighbor_ids=set()
        self.edge_complete_tiles=set()
        self.edge_refinement_log=[]
        self.long_cycle_records={}
        self.restart_metadata=None
        self.use_grid=not getattr(args,'no_grid',False)
        self.vertex_fan_quota=getattr(args,'vertex_fans_per_round',0)
        self.edge_tile_quota=getattr(args,'edge_tiles_per_round',8)
        # The inherited driver calls the refinement hook only when this is
        # positive. Actual vertex-fan quota is kept separately and can be 0.
        args.owner_fans_per_round=1 if self.edge_tile_quota or self.vertex_fan_quota else 0
        if not hasattr(args,'grid_step'):
            args.grid_step=0
        super().__init__(args)
        self.whole=WholeEdgeOracle(self.g)

    def insert(self,tile):
        if self.use_grid:
            return super().insert(tile)
        return OwnedSearch.insert(self,tile)

    def install_edge(self,tile,edge_index):
        tile=self.canonical_tile(tile)
        index=self.insert(tile)
        key=index,edge_index
        if key in self.edge_obligations:
            return
        edge=self.whole.edge(tile,edge_index)
        record=dict(tile=index,edge_index=edge_index,start=edge.start,end=edge.end,
                    ray=edge.ray,length=edge.length,boundary=edge.boundary)
        if edge.boundary:
            record.update(neighbors=(),intervals=(),clauses=())
            self.edge_obligations[key]=record
            return
        bank_key=edge.start,edge.ray,edge.length
        if bank_key not in self.edge_catalogues:
            catalogue=self.whole.catalogue(*bank_key)
            ids=tuple(self.insert(q) for q in catalogue.tiles)
            groups=tuple(tuple(ids[i] for i in group) for group in catalogue.intervals)
            self.edge_catalogues[bank_key]=dict(indices=ids,spans=catalogue.spans,intervals=groups)
            self.edge_neighbor_ids.update(ids)
            for k,group in enumerate(groups):
                if len(group)>1:
                    self.edge_bank_cliques.add((edge.start,edge.ray,edge.length,k,group))
                    # All these tiles contain the open unit interval on
                    # its right bank and therefore pairwise overlap there.
                    self.assert_(core.atmost(1,[f'x{i}' for i in group]))
        bank=self.edge_catalogues[bank_key]
        clauses=tuple(f'(=> x{index} {or_(f"x{i}" for i in group)})'
                      for group in bank['intervals'])
        for clause in clauses:
            self.assert_(clause)
        record.update(neighbors=bank['indices'],intervals=bank['intervals'],clauses=clauses)
        self.edge_obligations[key]=record

    def install_tile_edges(self,tile):
        tile=self.canonical_tile(tile)
        index=self.insert(tile)
        if index in self.edge_complete_tiles:
            return
        for k in range(3):
            self.install_edge(tile,k)
        self.edge_complete_tiles.add(index)

    def load_root(self):
        super().load_root()
        for i in self.root_indices:
            self.install_tile_edges(self.tiles[i])

    def boundary(self):
        super().boundary()
        path=getattr(self.args,'model_checkpoint',None)
        if not path:
            return
        raw=Path(path).read_bytes()
        if str(path).endswith('.gz'):
            raw=gzip.decompress(raw)
        data=json.loads(raw)
        assert tuple(data['sides'])==tuple(self.args.sides)
        old_tiles=data['tiles']
        def placement(index):
            return self.canonical_tile(old_tiles[index])
        for p,h,j in data.get('complete_rows',[]):
            self.install((self.g.point(*p),h,j))
        for record in data.get('corner_roots',[]):
            self.install_corner_tile(placement(record['tile']),tuple(record['point']))
        for record in data.get('whole_edge_obligations',[]):
            self.install_edge(placement(record['tile']),record['edge_index'])
        for index in data.get('whole_edge_complete_tiles',[]):
            self.install_tile_edges(placement(index))
        for old_i,old_j in data.get('overlap_pairs',[]):
            first,second=placement(old_i),placement(old_j)
            assert records_overlap(polygon_record(self.g,first),polygon_record(self.g,second))
            i,j=sorted((self.insert(first),self.insert(second)))
            self.overlap_records.add((i,j))
            self.assert_(f'(not (and x{i} x{j}))')
        for record in data.get('supported_long_cycle_cuts',[]):
            indices=[self.insert(placement(i)) for i in record['indices']]
            self.install_long_cycle_cuts(indices)
        self.restart_metadata=dict(source=str(path),sha256=hashlib.sha256(raw).hexdigest(),
                                   prior_root=data.get('root'),prior_root_assumptions_imported=False,
                                   arbitrary_assertions_imported=False)

    def install_long_cycle_cuts(self,chosen):
        if getattr(self.args,'no_cycle_cuts',False):
            return 0
        added=0
        for witness in selected_long_cycles(self.g,self.tiles,chosen):
            key=tuple(sorted(witness['indices']))
            if key in self.long_cycle_records:
                continue
            self.long_cycle_records[key]=witness
            self.assert_('(not (and '+' '.join(f'x{i}' for i in key)+'))')
            added+=1
        return added

    def selected_owner_rows(self,chosen):
        requested=self.owner_ids|self.edge_neighbor_ids
        return sorted({row for i in chosen if i in requested
                       for row,_ in self.g.rows(self.tiles[i]) if row not in self.exact})

    def refine_fans(self,chosen,residual):
        cycle_cuts=self.install_long_cycle_cuts(chosen)
        points={row[0] for row in residual}
        pending=[i for i in chosen if i not in self.edge_complete_tiles]
        pending.sort(key=lambda i:(i not in self.root_indices,
                                   i not in self.edge_neighbor_ids and i not in self.owner_ids,
                                   not any(p in points for p in self.g.vertices(self.tiles[i])),
                                   self.tiles[i]))
        installed=pending[:self.edge_tile_quota]
        for i in installed:
            self.install_tile_edges(self.tiles[i])
        vertex_fans=0
        if self.vertex_fan_quota:
            trigger=self.args.owner_fans_per_round
            self.args.owner_fans_per_round=self.vertex_fan_quota
            try:
                vertex_fans=super().refine_fans(chosen,residual)
            finally:
                self.args.owner_fans_per_round=trigger
        record=dict(iteration=self.iteration,new_edge_tiles=len(installed),
                    selected_edge_neighbors=len(set(chosen)&self.edge_neighbor_ids),
                    completed_edge_tiles=len(self.edge_complete_tiles),
                    edge_obligations=len(self.edge_obligations),vertex_fans=vertex_fans,
                    new_supported_cycle_cuts=cycle_cuts)
        self.edge_refinement_log.append(record)
        if self.history:
            self.history[-1]['whole_edges']=record
        print('WHOLE_EDGES',json.dumps(record,sort_keys=True),flush=True)
        return len(installed)+vertex_fans

    def necessary_snapshot(self):
        snapshot=super().necessary_snapshot()
        snapshot['whole_edge_extension']='complete-opposite-bank-v1'
        snapshot['geometric_restart']=self.restart_metadata
        snapshot['spatial_grid_enabled']=self.use_grid
        snapshot['whole_edge_obligations']=[v for _,v in sorted(self.edge_obligations.items())]
        snapshot['whole_edge_catalogues']=[dict(start=p,ray=ray,length=length,**record)
            for (p,ray,length),record in sorted(self.edge_catalogues.items())]
        snapshot['whole_edge_bank_cliques']=[dict(start=p,ray=ray,length=length,unit=k,indices=group)
            for p,ray,length,k,group in sorted(self.edge_bank_cliques)]
        snapshot['whole_edge_complete_tiles']=sorted(self.edge_complete_tiles)
        snapshot['supported_long_cycle_cuts']=[v for _,v in sorted(self.long_cycle_records.items())]
        return snapshot

    def checkpoint(self,iteration,status):
        super().checkpoint(iteration,status)
        path=self.out/'status.json'
        report=json.loads(path.read_text())
        report.update(whole_edge_obligations=len(self.edge_obligations),
                      whole_edge_complete_tiles=len(self.edge_complete_tiles),
                      whole_edge_neighbor_candidates=len(self.edge_neighbor_ids),
                      supported_long_cycle_cuts=len(self.long_cycle_records),
                      geometric_restart=self.restart_metadata,
                      whole_edge_refinement=self.edge_refinement_log,
                      vertex_fans_per_round=self.vertex_fan_quota,
                      edge_tiles_per_round=self.edge_tile_quota)
        path.write_text(json.dumps(report,indent=2)+'\n')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('sides',type=int,nargs=3)
    parser.add_argument('--out',required=True)
    parser.add_argument('--root-file')
    parser.add_argument('--root-id')
    parser.add_argument('--rows')
    parser.add_argument('--model-checkpoint',help='Regenerate complete rows, owned fans, whole banks and audited conflicts; prior root literals are not imported.')
    parser.add_argument('--corner-checkpoint')
    parser.add_argument('--seed-json')
    parser.add_argument('--grid-step',type=int,default=0)
    parser.add_argument('--no-grid',action='store_true',help='Disable optional interior-point sampling cliques.')
    parser.add_argument('--no-cycle-cuts',action='store_true',help='Disable the optional target-specific supported-cycle theorem cuts.')
    parser.add_argument('--prefer-tiles',action='store_true')
    parser.add_argument('--edge-tiles-per-round',type=int,default=8)
    parser.add_argument('--vertex-fans-per-round',type=int,default=0)
    parser.add_argument('--timeout-ms',type=int,default=45000)
    parser.add_argument('--time-limit',type=float,default=600)
    parser.add_argument('--rounds',type=int,default=100)
    parser.add_argument('--expand',type=int,default=100)
    parser.add_argument('--owner-rows-per-round',type=int,default=300)
    parser.add_argument('--max-columns',type=int,default=180000)
    parser.add_argument('--max-rss-mb',type=float,default=2200)
    parser.add_argument('--stop-file')
    parser.add_argument('--rebuild-every',type=int,default=10)
    parser.add_argument('--proof',action='store_true')
    args=defaults(**vars(parser.parse_args()))
    assert bool(args.root_file)==bool(args.root_id)
    assert args.grid_step>=0 and args.edge_tiles_per_round>=0 and args.vertex_fans_per_round>=0
    search=WholeEdgeSearch(args)
    try:
        search.run()
    except GracefulResourceStop as exc:
        print('INCONCLUSIVE:',exc,flush=True)
    finally:
        search.close()


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Run without -O: exact geometry assertions are required.')
    main()
