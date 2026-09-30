#!/usr/bin/env python3
"""Fail-closed tests and the supported-angle regression for the new checker."""
from pathlib import Path
import copy,json,sys,time,contextlib,io
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
from replay_16 import Checker

def run():
    d=json.loads((HERE/'data/f1_5_16_19.json').read_text())
    out=[]
    def reject(name,z):
        try:
            with contextlib.redirect_stdout(io.StringIO()):Checker(z).verify()
        except (ValueError,KeyError,IndexError) as e:out.append({'test':name,'result':'REJECTED','reason':str(e)})
        else:raise AssertionError('invalid certificate accepted: '+name)
    z=copy.deepcopy(d);z['tile']=[5,16,20];reject('wrong tile',z)
    z=copy.deepcopy(d);z['points'][z['outer'][1]][0]='81';reject('wrong target',z)
    root=next(iter(d['root_results']))
    z=copy.deepcopy(d);z['root_results']={root:'REFUTED'};z['root_definitions'][root]['tiles']=z['root_definitions'][root]['tiles'][:-1];reject('incorrect root identity',z)
    state=tuple(sorted(d['root_definitions'][root]['tiles']));where={tuple(sorted(n['tiles'])):i for i,n in enumerate(d['nodes'])};i=where[state]
    z=copy.deepcopy(d);z['root_results']={root:'REFUTED'};z['nodes'][i]={'tiles':list(state),'rule':'REJECT','reason':['FAKE_REJECTION']};reject('unreproduced terminal assertion',z)
    c=Checker(d)
    C=c.pt(-25,105);P=c.pt(-20,84);R=c.pt(-20,100);W=c.pt(-15,79)
    T=c.tri((C,P,R));U=c.tri((P,R,W));c.valid_state((T,U))
    if P in c.marks(U)[0] or c.elementary((T,U)):raise AssertionError('interior vertex incorrectly marked')
    if c.overlap(T,U) or not c.overlap(T,T):raise AssertionError('contact/overlap predicate error')
    return {'result':'PASS','malformed_certificates':out,'boundary_supported_angle_regression':'PASS',
            'exact_patch':{'C':[-25,105],'P':[-20,84],'R':[-20,100],'W':[-15,79]},
            'scope':'Regression only; complete certificate replay is separate.'}

if __name__=='__main__':
    result=run();(HERE/'verification/new_checker_tests.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
