#!/usr/bin/env python3
"""Regenerate and independently verify all complete five-height exclusions.

Large temporary bitmap traces are deleted after each replay. C++17 compiler
required. This program proves the positioned exclusions; GLOBAL_154_PROOF.md
identifies the separate exhaustive arithmetic and height-bound inputs.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

HERE=Path(__file__).resolve().parent
PRODUCERS=HERE.parent/'154-cpsat'
CASES=[('center',-2,2,0,4773371018,'bitmap_zero.cpp'),
       ('offset',-1,3,1,4770414013,'bitmap_zero_rotated.cpp'),
       ('extreme',0,4,1,4759540301,'bitmap_zero_rotated.cpp')]

def run(args):
    subprocess.run([str(x) for x in args],check=True)

def sha(path):
    digest=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):
            digest.update(block)
    return digest.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--seconds',type=int,default=600)
    ap.add_argument('--case',choices=['center','offset','extreme'])
    ap.add_argument('--existing-trace-dir',type=Path,
                    help='Directory containing 634-bitmap-five-CASE.json and .bitmap_trace.bin')
    args=ap.parse_args();results=[]
    with tempfile.TemporaryDirectory(prefix='erdos634-five-heights-') as temporary:
        temp=Path(temporary);verifier=temp/'verify';executables={}
        run(['g++','-std=c++17','-O2',HERE/'replay_bitmap.cpp','-o',verifier])
        for name,L,U,rotation,count,source in CASES:
            if args.case and name!=args.case:continue
            if args.existing_trace_dir:
                prefix=args.existing_trace_dir/f'634-bitmap-five-{name}'
            else:
                if source not in executables:
                    executable=temp/source.removesuffix('.cpp')
                    run(['g++','-std=c++17','-O2',PRODUCERS/source,'-o',executable])
                    executables[source]=executable
                prefix=temp/f'634-bitmap-five-{name}'
                run([executables[source],L,U,prefix,args.seconds,1,0])
            producer=json.loads(prefix.with_suffix('.json').read_text())
            if not producer['conflict'] or producer['incomplete']:
                raise RuntimeError(f'{name}: no completed producer refutation; a timeout proves nothing')
            if (producer['L'],producer['U'],producer.get('basis_rotation',0),producer['candidate_placements'])!=(L,U,rotation,count):
                raise RuntimeError(f'{name}: unexpected geometric scope')
            trace=Path(str(prefix)+'.bitmap_trace.bin');output=temp/f'{name}-independent.json'
            run([verifier,L,U,rotation,trace,output,count,producer['bad_direction'],
                 producer['bad_y'],producer['bad_word'],producer['bad_mask'],source])
            result=json.loads(output.read_text())
            if result['status']!='PASS' or not result['required_sign_support_empty']:
                raise RuntimeError(f'{name}: independent verification failed')
            result['trace_sha256']=sha(trace);result['case']=name;results.append(result)
            if not args.existing_trace_dir:
                trace.unlink()
    print(json.dumps({'status':'PASS','all_three_five_height_representatives_checked':len(results)==3,
                      'results':results},indent=2))

if __name__=='__main__':
    main()
