#!/usr/bin/env python3
"""Budgeted constructive CP-SAT attempt; nonpositive outcomes are scoped."""
import argparse
import json
from pathlib import Path
import struct
import sys
import time
import os

if os.environ.get('ERDOS_ORTOOLS_PATH'):
    sys.path.insert(0,os.environ['ERDOS_ORTOOLS_PATH'])
elif Path('/tmp/erdos634-ortools').is_dir():
    sys.path.insert(0,'/tmp/erdos634-ortools')
from ortools.sat.python import cp_model,cp_model_helper

ap=argparse.ArgumentParser()
ap.add_argument('prefix',type=Path)
ap.add_argument('--seconds',type=float,default=45)
ar=ap.parse_args();start=time.monotonic();prefix=str(ar.prefix)
p=cp_model_helper.CpModelProto()
p.parse_text_format(Path(prefix+'.pbtxt').read_text())
m=cp_model.CpModel(p)
s=cp_model.CpSolver()
s.parameters.max_time_in_seconds=ar.seconds
s.parameters.num_search_workers=1
s.parameters.linearization_level=0
s.parameters.symmetry_level=0
s.parameters.random_seed=634
s.parameters.log_search_progress=True
status=s.solve(m)
report={'status':s.status_name(status),'seconds':time.monotonic()-start,
        'scope':'Only this finite constructive placement model; no unrestricted nonexistence claim.'}
if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
    solution=s.response_proto.solution
    chosen=[]
    for group,o,x,y in struct.iter_unpack('iiii',Path(prefix+'.mapping.bin').read_bytes()):
        if group<0 or solution[group]:chosen.append([o,x,y])
    Path(prefix+'.chosen.json').write_text(json.dumps(chosen)+'\n')
    report['selected_count']=len(chosen)
    report['geometric_certificate_status']='PENDING_INDEPENDENT_CHECK'
Path(prefix+'.solver.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
