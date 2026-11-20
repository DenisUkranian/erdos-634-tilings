#!/usr/bin/env python3
"""Adaptive exact-dual cuts and exploratory fixed-profile LPs.

No generated floating feasible point is called a tiling or a certificate.
An exhausted integer filter still requires independent proof checking.
"""
import argparse,json,subprocess,time
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from strengthened_gate_model import old
from build_profile_cuts import load_cut,transforms


def build_data(paths,solutions):
    cuts=[];tile=None
    for path in paths:
        t,D,u,v=load_cut(path)
        if tile is None:tile=t
        assert tile==t
        cuts.extend(transforms(*t,D,u,v))
    a,b,c=tile;d=a-b;cap=51 if c==43 else 44
    lines=[f'{c} {d} {cap} {2*c//d} {c//d} {len(cuts)} {solutions}']
    for D,u,v in cuts:lines.extend([str(D),' '.join(map(str,u)),' '.join(map(str,v))])
    return '\n'.join(lines)+'\n'


def solve_profile(a,b,c,equations,labels,profile,seconds):
    nc=len(labels);base=3*c*c;d=a-b
    g=np.zeros(2*c,dtype=int);g[0]=profile['native_up'];g[c]=profile['native_down']
    for r in profile['remote_positive_indices']:
        g[(0 if r<c-1 else c)+r%(c-1)+1]+=1
    neg=profile['remote_negative_index']
    if neg>=0:g[(0 if neg<c-1 else c)+neg%(c-1)+1]-=1
    target=np.zeros(base+2*c);target[base:]=d*g
    target[base]+=2*c;target[base+c]-=c
    assert sum(target[base:])==c
    start=time.monotonic()
    result=linprog(np.ones(nc),A_eq=equations,b_eq=target,bounds=(0,None),
                   method='highs-ipm',options={'time_limit':seconds})
    out={'tile':[a,b,c],'profile':profile,'up_gate_charges':g[:c].tolist(),
         'down_gate_charges':g[c:].tolist(),'status':int(result.status),
         'message':result.message,'seconds':time.monotonic()-start,
         'scope':'Necessary all-residue projection. Floating feasibility is not a tiling or an exact certificate.'}
    if result.x is not None:
        out['floating_population']=float(result.fun)
        out['maximum_equality_residual']=float(np.max(abs(equations@result.x-target)))
        if result.fun<=3*c+1e-7:
            out['support']=[list(labels[i])+[float(v)] for i,v in enumerate(result.x) if v>1e-8]
    if result.status==0:
        dual=np.rint(np.asarray(result.eqlin.marginals)*1000000).astype(np.int64)
        scores=np.asarray(equations.T@dual,dtype=np.int64)
        D=max(1,int(max(scores)))
        bound=int(np.asarray(target,dtype=np.int64)@dual)
        out.update(endpoint_tables=dual[:base].reshape(3,c,c).tolist(),
                   up_weights=dual[base:base+c].tolist(),down_weights=dual[base+c:].tolist(),
                   D=D,lower_numerator=bound,lower_denominator=D,
                   exact_column_inequalities=bool(np.all(scores<=D)))
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--cuts',nargs='+',type=Path,required=True)
    p.add_argument('--out-dir',type=Path,required=True)
    p.add_argument('--enumerator',type=Path,required=True)
    p.add_argument('--iterations',type=int,default=30)
    p.add_argument('--seconds',type=float,default=45)
    ar=p.parse_args();ar.out_dir.mkdir(parents=True,exist_ok=True)
    a,b,c=load_cut(ar.cuts[0])[0]
    A,_,_,_,_,labels=old.make_model(a,b,c)
    equations=A[:3*c*c+2*c,:len(labels)]
    paths=list(ar.cuts);history=[]
    for it in range(ar.iterations):
        data=build_data(paths,1)
        (ar.out_dir/'latest_cuts.dat').write_text(data)
        result=subprocess.run([str(ar.enumerator)],input=data,text=True,capture_output=True,check=True)
        lines=[json.loads(line)for line in result.stdout.splitlines()]
        report=lines[-1];history.append({'iteration':it,'filter':report})
        if len(lines)==1:
            print(json.dumps({'event':'FILTER_EXHAUSTED','iteration':it,'filter':report}),flush=True)
            break
        profile=lines[0]
        print(json.dumps({'event':'CANDIDATE','iteration':it,'profile':profile,'filter':report}),flush=True)
        probe=solve_profile(a,b,c,equations,labels,profile,ar.seconds)
        path=ar.out_dir/f'profile_{it:03d}.json';path.write_text(json.dumps(probe,indent=2)+'\n')
        small={k:v for k,v in probe.items() if k not in ('support','endpoint_tables','up_weights','down_weights','up_gate_charges','down_gate_charges')}
        history[-1]['lp']=small
        (ar.out_dir/'history.json').write_text(json.dumps(history,indent=2)+'\n')
        print(json.dumps({'event':'LP','iteration':it,**small}),flush=True)
        if probe['status']!=0 or probe.get('floating_population',1e9)<=3*c+1e-7:break
        paths.append(path)
    (ar.out_dir/'history.json').write_text(json.dumps(history,indent=2)+'\n')
