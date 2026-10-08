#!/usr/bin/env python3
"""Regenerate and independently replay the five complete E135 direction bands."""
import argparse,json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
CASES=[('center',-4,4,420445247592,246600,49479639),
       ('offset1',-3,5,420583549524,246600,50644031),
       ('offset2',-2,6,420309426351,246558,50429425),
       ('offset3',-1,7,420224867466,186798,49218545),
       ('edge',0,8,420441801582,83163,50973015)]
def run(args):subprocess.run(list(map(str,args)),check=True)
def main():
 p=argparse.ArgumentParser();p.add_argument('directory',type=Path);p.add_argument('--seconds',type=int,default=600);p.add_argument('--existing',action='store_true');p.add_argument('--keep-traces',action='store_true');p.add_argument('--case',choices=[r[0]for r in CASES]);a=p.parse_args();a.directory.mkdir(parents=True,exist_ok=True)
 producer=a.directory/'produce-rle';verifier=a.directory/'verify-rle'
 run(['g++','-std=c++17','-O2',HERE/'replay_e135_rle.cpp','-o',verifier])
 if not a.existing:run(['g++','-std=c++17','-O2',HERE.parent/'e135/rle_equilateral135.cpp','-o',producer])
 records=[]
 for name,L,U,count,remaining,steps in CASES:
  if a.case and a.case!=name:continue
  prefix=a.directory/f'e135-rle-k9-{name}'
  if not a.existing:run([producer,L,U,prefix,a.seconds,1,0])
  report=json.loads(Path(str(prefix)+'.json').read_text())
  if report['incomplete']or report['conflict']:raise RuntimeError('No completed reduction; a timeout does not prove this result')
  if (report['L'],report['U'],report['candidate_placements'],report['remaining'],report['trace_records'])!=(L,U,count,remaining,steps):raise RuntimeError('Recorded reduction differs; investigate before accepting')
  trace=Path(str(prefix)+'.rle_trace.bin');output=a.directory/f'{name}-independent.json'
  run([verifier,L,U,report['basis_rotation'],trace,Path(str(prefix)+'.remaining.txt'),output,count,remaining,steps,name])
  checked=json.loads(output.read_text())
  if checked['status']!='PASS':raise RuntimeError('Independent replay failed')
  records.append(checked)
  if not a.keep_traces and not a.existing:trace.unlink()
 print(json.dumps(dict(status='PASS',all_five_bands_checked=len(records)==5,records=records),indent=2))
if __name__=='__main__':main()
