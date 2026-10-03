#!/usr/bin/env python3
"""Replay all published finite suites in disposable copies; preserve frozen research files."""
from __future__ import annotations
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile,time
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if not __debug__ or os.environ.get('PYTHONOPTIMIZE'):
    raise SystemExit('Use ordinary Python: -O/-OO/PYTHONOPTIMIZE would disable legacy assertions.')

def run(cmd,cwd,timeout=1800):
    start=time.monotonic();p=subprocess.run([sys.executable,*cmd],cwd=cwd,text=True,capture_output=True,timeout=timeout)
    if p.returncode:
        sys.stderr.write(p.stdout+p.stderr);raise RuntimeError(f'Failed: {cmd} (code {p.returncode})')
    return {'command':cmd,'seconds':round(time.monotonic()-start,3),'stdout':p.stdout,'stderr':p.stderr}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--jobs',type=int,default=2);ap.add_argument('--output',type=Path,default=ROOT/'audit-output/full-replay.json');args=ap.parse_args()
    if args.jobs<1:ap.error('--jobs must be positive')
    started=time.monotonic();reports={}
    reports['repository']=run(['scripts/check_repository.py'],ROOT)
    print('REPOSITORY_INTEGRITY_AND_LINKS=PASS',flush=True)
    with tempfile.TemporaryDirectory(prefix='erdos634-full-replay-') as td:
        work=Path(td)/'repo'
        shutil.copytree(ROOT,work,ignore=shutil.ignore_patterns('.git','__pycache__','audit-output','.publication','*.pyc'))
        reports['legacy']=run(['scripts/reproduce.py'],work)
        print('LEGACY_SUITE=PASS',flush=True)
        nw=work/'research/n105'
        reports['n105']=run(['verify_all.py','--jobs',str(args.jobs)],nw)
        nr=json.loads((nw/'VERIFIED_RESULTS.json').read_text())
        if nr.get('result')!='ALL_PACKAGED_CHECKS_PASSED' or nr.get('global_N105_exclusion') is not True or nr.get('full_Erdos634_solved') is not False:raise ValueError('Unexpected N105 scope/report')
        reports['n105']['report']=nr
        print('GLOBAL_N105_FINITE_COMPONENTS=PASS',flush=True)
        sw=work/'research/general-spectra'
        reports['spectra_construction']=run(['verify_certificate.py','construction_116640.json','--expand','--report','fresh-expanded.json'],sw)
        sr=json.loads((sw/'fresh-expanded.json').read_text())
        if sr.get('expanded_tiles_checked')!=116640 or sr.get('expanded_coordinate_sha256')!='86710b7ea51c174e070bf1cc4cda6860815f9e9c790529008caca53d49bf0f23':raise ValueError('Expanded construction mismatch')
        reports['spectra_construction']['report']=sr
        reports['spectra_formula_tests']=run(['check_general_formulas.py'],sw)
        print('GENERAL_SPECTRA_AND_EXPANDED_CONSTRUCTION=PASS',flush=True)
        uw=work/'research/uniform-reduction'
        reports['uniform_reduction']=run(['verify_all.py'],uw)
        ur=json.loads((uw/'VERIFIED_RESULTS.json').read_text())
        if ur.get('result')!='ALL_SUPPLEMENTARY_CHECKS_PASSED' or ur.get('full_problem_solved') is not False:
            raise ValueError('Unexpected uniform-reduction scope/report')
        reports['uniform_reduction']['report']=ur
        print('UNIFORM_REDUCTION_SUPPLEMENTARY_CHECKS=PASS',flush=True)
        reports['c_relations']=run(['check_relations.py','--max-v','40'],work/'research/c-relations')
        if json.loads(reports['c_relations']['stdout']).get('status')!='PASS':raise ValueError('c-relations did not pass')
        print('SHARP_C_RELATIONS_ARITHMETIC=PASS',flush=True)
        for key,package in [('uniform_sectors','uniform-sectors'),('square_class_saturation','square-class-saturation'),('group2_f4','group2-f4')]:
            pw=work/'research'/package
            reports[key]=run(['run_checks.py','--output','fresh-replay.json'],pw)
            pr=json.loads((pw/'fresh-replay.json').read_text())
            if pr.get('status')!='PASS':
                raise ValueError(f'Unexpected {package} verification report')
            reports[key]['report']=pr
            print(f'{key.upper()}_FINITE_CHECKS=PASS',flush=True)
    result={'status':'ALL_FINITE_SUITES_PASS','date':datetime.now(timezone.utc).date().isoformat(),'python':sys.version,'seconds':round(time.monotonic()-started,3),'suites':reports,'full_Erdos634_solved':False,'prime_case_formally_verified':False,'human_and_published_theorems_formally_verified':False,'external_peer_review':False,'verification_boundary':'All packaged finite checks, syntax, integrity and local-link targets. Not a proof-assistant verification or independent human referee report.'}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('ALL_PUBLISHED_FINITE_SUITES=PASS',flush=True)
if __name__=='__main__':main()
