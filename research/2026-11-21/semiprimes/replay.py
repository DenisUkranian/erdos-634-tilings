#!/usr/bin/env python3
"""Replay the exact 5063 minimal-odd exclusion without an optimizer."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]


def main():
    if not __debug__:
        raise SystemExit('Run with assertions enabled; do not use -O.')
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--saved-enumeration',action='store_true')
    p.add_argument('--out',type=Path)
    args=p.parse_args()
    index=json.loads((HERE/'gate-model/CERTIFICATES_5063.json').read_text())
    assert index['full_5063_excluded'] is False and index['full_3431_excluded'] is False
    source=ROOT/index['enumerator_source']
    cut_file=ROOT/index['cut_file']
    for file,digest in [(source,index['enumerator_source_sha256']),(cut_file,index['cut_file_sha256'])]:
        assert hashlib.sha256(file.read_bytes()).hexdigest()==digest,str(file)
    spec=importlib.util.spec_from_file_location('independent_profile_audit',HERE/'audit/verify_profile_duals.py')
    audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
    reports=[];cuts=[];start=time.monotonic()
    for entry in index['certificates']:
        file=ROOT/entry['path']
        assert hashlib.sha256(file.read_bytes()).hexdigest()==entry['sha256'],str(file)
        report,variants=audit.verify(file)
        assert tuple(report['tile'])==tuple(index['tile']),str(file)
        reports.append(report);cuts.extend(variants)
    assert len(reports)==65 and sum(r['columns']for r in reports)==1442220
    tile=tuple(index['tile'])
    serialized=audit.check_cut_file(cut_file,cuts,tile)
    symmetries=audit.verify_geometry_symmetries(*tile)
    universe=audit.universe_counts(tile)
    print('EXACT_COLUMN_INEQUALITIES_AND_TRANSFORMS=PASS',flush=True)
    with tempfile.TemporaryDirectory(prefix='erdos634-minimal-odd-') as td:
        binary=Path(td)/'enumerate_profiles'
        subprocess.run(['g++','-O3','-std=c++17',str(source),'-o',str(binary)],check=True,capture_output=True,text=True)
        controls=audit.compare_enumerator(binary)
        if args.saved_enumeration:
            output=(HERE/'gate-model/FINAL_PROFILE_ENUMERATION_5063.jsonl').read_text()
        else:
            output=subprocess.run([str(binary)],input=cut_file.read_text(),text=True,capture_output=True,check=True,timeout=900).stdout
    records=[json.loads(line)for line in output.splitlines()]
    assert len(records)==1,'A surviving profile was emitted.'
    result=records[0]
    assert result['summary'] and result['exhaustive']
    assert result['visited']==universe['visited']==34672599
    assert result['reserve_passed']==universe['reserve_passed']==17800359
    assert result['cut_passed']==0
    assert sum(result['rejected'])==17800359
    report={'status':'PASS','tile':tile,'excluded_odd_population':129,
            'necessary_odd_population_lower_bound':215,
            'full_5063_excluded':False,'full_3431_excluded':False,
            'fresh_exhaustive_enumeration':not args.saved_enumeration,
            'base_certificates':len(reports),'column_inequalities':sum(r['columns']for r in reports),
            'serialized_cuts':serialized,'symmetries':symmetries,
            'small_independent_controls':controls,'complete_enumeration':result,
            'seconds':time.monotonic()-start,
            'scope':'Exact finite exclusion of n_odd=129 using the cited complete-tiling geometric reduction; neither original count is decided.'}
    if args.out:args.out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in ('complete_enumeration','small_independent_controls','symmetries','serialized_cuts')},indent=2))


if __name__=='__main__':main()
