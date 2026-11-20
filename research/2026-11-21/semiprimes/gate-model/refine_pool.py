#!/usr/bin/env python3
"""Refine a completely enumerated charge pool with checked-candidate duals.

An exhausted pool proves exclusion only after the source enumeration,
all certificate inequalities, and the filter have been independently
replayed. A floating feasible projection is never called a tiling.
"""
import argparse,hashlib,importlib.util,json,subprocess,time
from pathlib import Path
from refine_profiles import build_data,solve_profile,old

SOURCE=Path(__file__).resolve().parents[1]/'global-invariant/additive_gate_model.py'
spec=importlib.util.spec_from_file_location('additive_gate_model',SOURCE)
additive=importlib.util.module_from_spec(spec);spec.loader.exec_module(additive)


def charges(c,profile):
    up=[0]*c;down=[0]*c
    up[0]=profile['native_up'];down[0]=profile['native_down']
    for r in profile['remote_positive_indices']:
        (up if r<c-1 else down)[r%(c-1)+1]+=1
    r=profile['remote_negative_index']
    if r>=0:(up if r<c-1 else down)[r%(c-1)+1]-=1
    return up,down


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--pool',type=Path,required=True)
    p.add_argument('--cuts',nargs='+',type=Path,required=True)
    p.add_argument('--filter',type=Path,required=True)
    p.add_argument('--out-dir',type=Path,required=True)
    p.add_argument('--iterations',type=int,default=300)
    ar=p.parse_args();ar.out_dir.mkdir(parents=True,exist_ok=True)
    tile=json.loads(ar.cuts[0].read_text())['tile'];a,b,c=tile
    pool=ar.pool;paths=list(ar.cuts);new_cuts=paths[:];history=[];full=None
    metadata={'tile':tile,'initial_pool':str(pool),'initial_pool_sha256':hashlib.sha256(pool.read_bytes()).hexdigest(),
              'initial_certificates':[str(path)for path in paths],
              'scope':'Necessary finite charge model. Completeness is inherited from the separately recorded exhaustive initial pool; all cuts require independent integer replay.'}
    (ar.out_dir/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    for it in range(ar.iterations):
        next_pool=ar.out_dir/f'pool_{it:03d}.txt'
        start=time.monotonic()
        run=subprocess.run([str(ar.filter),str(pool),str(next_pool)],input=build_data(new_cuts,0),text=True,capture_output=True,check=True)
        lines=[json.loads(s)for s in run.stdout.splitlines()]
        summary=lines[-1]
        record={'iteration':it,'filter':summary,'filter_seconds':time.monotonic()-start,
                'pool_input_sha256':hashlib.sha256(pool.read_bytes()).hexdigest(),
                'pool_output_sha256':hashlib.sha256(next_pool.read_bytes()).hexdigest(),
                'new_certificates':[str(path)for path in new_cuts]}
        history.append(record)
        print(json.dumps({'event':'POOL','iteration':it,**{k:v for k,v in summary.items()if k!='rejected'},'seconds':record['filter_seconds']}),flush=True)
        if len(lines)==1:
            record['outcome']='EXHAUSTED';break
        profile=lines[0];record['profile']=profile
        up,down=charges(c,profile)
        result=additive.solve(a,b,c,up,down);result['profile']=profile
        if result['status']==0 and result['floating_population']<=3*c+1e-7:
            record['additive_population']=result['floating_population']
            if full is None:
                A,_,_,_,_,labels=old.make_model(a,b,c)
                full=(A[:3*c*c+2*c,:len(labels)],labels)
            result=solve_profile(a,b,c,*full,profile,45)
            record['used_full_projection']=True
        path=ar.out_dir/f'certificate_{it:03d}.json'
        path.write_text(json.dumps(result,indent=2)+'\n')
        record['lp']={k:v for k,v in result.items()if k in ('status','message','seconds','floating_population','maximum_equality_residual','D','lower_numerator','lower_denominator')}
        print(json.dumps({'event':'LP','iteration':it,'profile':profile,**record['lp']}),flush=True)
        (ar.out_dir/'history.json').write_text(json.dumps(history,indent=2)+'\n')
        if result['status']!=0 or result.get('floating_population',1e9)<=3*c+1e-7:
            record['outcome']='NO_EXCLUSION_FROM_CURRENT_PROJECTION';break
        if result['lower_numerator']<=3*c*result['D']:
            record['outcome']='ROUNDED_CERTIFICATE_NOT_STRICT';break
        paths.append(path);new_cuts=[path];pool=next_pool
    (ar.out_dir/'history.json').write_text(json.dumps(history,indent=2)+'\n')
    (ar.out_dir/'certificate_paths.json').write_text(json.dumps([str(path)for path in paths],indent=2)+'\n')
