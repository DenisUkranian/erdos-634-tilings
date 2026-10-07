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
        for key,package in [('uniform_sectors','uniform-sectors'),('square_class_saturation','square-class-saturation'),('group2_f4','group2-f4'),('w_beta_caps','w-beta-caps')]:
            pw=work/'research'/package
            reports[key]=run(['run_checks.py','--output','fresh-replay.json'],pw)
            pr=json.loads((pw/'fresh-replay.json').read_text())
            if pr.get('status')!='PASS':
                raise ValueError(f'Unexpected {package} verification report')
            reports[key]['report']=pr
            print(f'{key.upper()}_FINITE_CHECKS=PASS',flush=True)
        tw=work/'research/group2-trapezoids'
        for key,command,report_name,expected in [
                ('group2_trapezoids','check_family.py','VERIFIED_RESULTS.json','verified'),
                ('balanced_f4','check_balanced_f4.py','balanced_f4_verification.json','PASS'),
                ('free_k','check_free_k.py','free_k_verification.json','PASS'),
                ('target_bridges','check_target_bridges.py','target_bridges_verification.json','PASS')]:
            reports[key]=run([command],tw)
            pr=json.loads((tw/report_name).read_text())
            if pr.get('status')!=expected or pr.get('full_Erdos634_solved') is not False:
                raise ValueError(f'Unexpected {key} verification report')
            reports[key]['report']=pr
            print(f'{key.upper()}_FINITE_CHECKS=PASS',flush=True)
        reports['f2_unit']=run(['verify_f2.py','certificates/f2_balanced_8_7_13_m2.json'],tw)
        f2=json.loads(reports['f2_unit']['stdout'])
        if f2.get('status')!='PASS' or f2.get('unit_triangles')!=2024:
            raise ValueError('Unexpected F2 unit verification report')
        print('F2_FULL_UNIT_CHECKS=PASS',flush=True)
        reports['chord_bound_counterexample']=run(['check_corner_chord.py'],work/'research/attempt-obstructions')
        print('PARTIAL_CORNER_CHORD_COUNTEREXAMPLE=PASS',flush=True)
        pw=work/'research/pure-convex-islands'
        for key,command in [('pure_laurent_jets','verify_laurent_jets.py'),
                            ('pure_hex_jets','verify_hex_jets.py'),
                            ('pure_stepped_seed','verify_stepped_seed.py')]:
            reports[key]=run([command],pw)
        print('CONVEX_PURE_ISLAND_EXACT_CHECKS=PASS',flush=True)
        nw=work/'research/nonconvex-chirality'
        reports['nonconvex_chirality_witness']=run(['verify_witness.py'],nw)
        reports['nonconvex_chirality_boundary']=run(['check_boundary.py'],nw)
        print('NONCONVEX_CHIRALITY_COUNTEREXAMPLE=PASS',flush=True)
        ew=work/'research/extreme-pure-embedding'
        reports['extreme_pure_collar']=run(['verify_collar.py'],ew)
        reports['extreme_pure_corner']=run(['research/general-spectra/verify_certificate.py','research/extreme-pure-embedding/corner_base.json'],work)
        reports['extreme_pure_embedding']=run(['verify_embedding.py'],ew)
        er=json.loads(reports['extreme_pure_embedding']['stdout'])
        if er.get('result')!='PASS' or er.get('all_tiles')!=4822335:
            raise ValueError('Unexpected extreme-pure embedding report')
        print('TRIANGULAR_EXTREME_PURE_EMBEDDING=PASS',flush=True)
        reports['square_class_tails']=run(['run_checks.py'],work/'research/square-class-tails')
        tr=json.loads(reports['square_class_tails']['stdout'])
        if tr.get('status')!='PASS' or tr.get('full_Erdos634_solved') is not False:
            raise ValueError('Unexpected square-class tail/ray report')
        reports['square_class_tails']['report']=tr
        print('SQUARE_CLASS_TAIL_AND_RAY_CHECKS=PASS',flush=True)
        reports['composite_support']=run(['run_checks.py'],work/'research/composite-support')
        cr=json.loads(reports['composite_support']['stdout'])
        if cr.get('status')!='PASS' or cr.get('full_Erdos634_solved') is not False:
            raise ValueError('Unexpected composite-support/class-22 report')
        reports['composite_support']['report']=cr
        print('COMPOSITE_SUPPORT_AND_COMPLETE_CLASS22_CHECKS=PASS',flush=True)
        pw=work/'research/elliptic-sectors'
        reports['elliptic_sectors']=run(['run_checks.py'],pw)
        es=json.loads(reports['elliptic_sectors']['stdout'])
        if es.get('status')!='PASS' or es.get('full_Erdos634_solved') is not False:
            raise ValueError('Unexpected elliptic-sector scope/report')
        reports['elliptic_sectors']['report']=es
        reports['alpha_elliptic_maps']=run(['check_alpha_maps.py'],pw)
        if json.loads(reports['alpha_elliptic_maps']['stdout']).get('result')!='PASS':
            raise ValueError('Alpha rational identities did not pass')
        print('ELLIPTIC_SECTORS_AND_ALPHA_MAPS=PASS',flush=True)
        reports['local_descent']=run(['run_checks.py'],work/'research/local-descent')
        ld=json.loads(reports['local_descent']['stdout'])
        if ld.get('status')!='PASS' or ld.get('full_Erdos634_solved') is not False:
            raise ValueError('Unexpected local-descent scope/report')
        reports['local_descent']['report']=ld
        print('LOCAL_DESCENT_ODD_MULTIPLIER_CHECKS=PASS',flush=True)
        for key,package,command in [
                ('infinite_minimal_orbit','infinite-minimal','verify_orbit.py'),
                ('seam_certificates','seam-certificates','verify_seams.py'),
                ('abstract_disk_certificates','disk-certificates','test_disk.py'),
                ('f3_vertex_defects','f3-vertex-defects','check_inventory.py'),
                ('norm_geometric_remainder','arithmetic-continuation','check_norm_remainder.py'),
                ('f3_split_part','arithmetic-continuation','check_split_part.py'),
                ('four_norm_split_parts','arithmetic-continuation','check_other_split_branches.py'),
                ('global_fixed_split_part','arithmetic-continuation','check_global_split_part.py'),
                ('global_sector_cli','arithmetic-continuation','check_global_sector_cli.py'),
                ('nested_corner_certificates','group2-nested-corners','run_checks.py'),
                ('balanced_ratio_finite_completion','group2-nested-corners','check_balanced_7_5_small.py'),
                ('ternary_semigroup_conductor','f3-descent-attempt','semigroup_tail.py'),
                ('squarefree_f3_front','arithmetic-continuation','check_squarefree_f3_front.py'),
                ('gamma_corner_certificates','group2-gamma-corners','run_checks.py'),
                ('gamma_single_height_obstruction','group2-gamma-corners','check_two_axis_obstruction.py'),
                ('f3_full_signature','f3-descent-attempt','check_full_signature.py'),
                ('gamma_staircase_arithmetic','global-classification-continuation','check_gamma_staircase.py'),
                ('gamma_staircase_certificate','group2-mixed-gamma','run_checks.py'),
                ('gamma_arbitrary_direction_boundary','f3-position-invariants','check_infinite_boundary_examples.py'),
                ('gamma_4830_boundary_collar','f3-position-invariants','check_boundary.py'),
                ('norm_exchange_diameter_barrier','global-normal-forms','check_diameter_exchange_barrier.py'),
                ('i120_full_signature','i120-continuation','check_i120.py'),
                ('sharp_nested_ratio_cone','global-criterion-oct7','check_sharp_cone.py'),
                ('norm_orientation_level_divisibility','i120-global-oct7','check_height_levels.py'),
                ('theta_exact_base_count_threshold','w-global-oct7','check_theta_base.py'),
                ('f3_contained_position_moment_barrier','f3-moments-oct7','independent_check.py'),
                ('w_scale_two_universal_local_collar','w-scale-two-oct7','check_symbolic_collar.py'),
                ('same_count_parameter_descent_audit','strategy-oct7','check_plan_b.py'),
                ('fixed_degree_moment_barrier','strategy-oct7','check-plan-c.py'),
                ('f3_positive_fan_hexagon','final-push-oct7/f3','check_fan_hexagon.py'),
                ('f3_fan_short_height_obstruction','final-push-oct7/pentagon','check_currents.py'),
                ('local_multiple_cover_and_prime_exponent_barriers','final-push-oct7/duality','check_duality.py'),
                ('w56_local_escape_patch','group1-global-scales','verify_local_patch.py')]:
            reports[key]=run([command],work/'research'/package)
            pr=json.loads(reports[key]['stdout'])
            if pr.get('status')!='PASS' or pr.get('full_Erdos634_solved') is not False:
                raise ValueError(f'Unexpected {package} scope/report')
            reports[key]['report']=pr
            print(f'{key.upper()}_FINITE_CHECKS=PASS',flush=True)
    result={'status':'ALL_FINITE_SUITES_PASS','date':datetime.now(timezone.utc).date().isoformat(),'python':sys.version,'seconds':round(time.monotonic()-started,3),'suites':reports,'full_Erdos634_solved':False,'prime_case_formally_verified':False,'human_and_published_theorems_formally_verified':False,'external_peer_review':False,'verification_boundary':'All packaged finite checks, syntax, integrity and local-link targets. Not a proof-assistant verification or independent human referee report.'}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('ALL_PUBLISHED_FINITE_SUITES=PASS',flush=True)
if __name__=='__main__':main()
