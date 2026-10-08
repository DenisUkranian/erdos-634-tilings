#!/usr/bin/env python3
"""Compare continued DFS against one uninterrupted deterministic DFS prefix."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess


def run(command,log):
    with log.open('w') as output:
        subprocess.run(command,stdout=output,stderr=output,check=True)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('search',type=Path)
    ap.add_argument('resume',type=Path)
    ap.add_argument('workdir',type=Path)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    args.workdir.mkdir(parents=True,exist_ok=True)
    full,first,continued=[args.workdir/name for name in ('full','first','continued')]
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures=[pool.submit(run,[str(args.search),'300',str(cap),str(prefix)],prefix.with_suffix('.log'))
                 for prefix,cap in ((full,4000),(first,1000))]
        for future in futures:future.result()
    run([str(args.resume),str(first),'300',str(continued),'4000'],continued.with_suffix('.log'))
    read_report=lambda prefix:json.loads(Path(str(prefix)+'-report.json').read_text())
    reports=[read_report(prefix) for prefix in (full,first,continued)]
    assert all(r['status']=='INCOMPLETE' for r in reports)
    assert reports[0]['nodes']==4000 and reports[1]['nodes']==1000
    assert reports[2]['nodes_this_run']==4000
    traces=[Path(str(prefix)+'-trace.txt').read_text().splitlines() for prefix in (full,first,continued)]
    assert traces[0][:len(traces[1])]==traces[1]
    assert traces[2][:len(traces[0])]==traces[0]
    assert reports[2]['prior_dead_states']==reports[1]['dead_states']
    report={'status':'PASS','uninterrupted_nodes':4000,'initial_checkpoint_nodes':1000,
            'continuation_nodes':4000,'matching_closed_state_prefix_records':len(traces[0]),
            'partially_explored_ancestors_revisited':True,
            'scope':'Exact trace-prefix match; checkpoint is trusted operational state, not an independently replayed negative certificate',
            'N154_decided':False,'full_Erdos634_solved':False}
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
