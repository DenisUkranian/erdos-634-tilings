#!/usr/bin/env python3
"""Independent integer verification of native3431 gate-excess certificates.
Uses only the standard library and reconstructs every tile column directly.
"""
from collections import Counter
from pathlib import Path
import gzip,json

HERE=Path(__file__).resolve().parent
U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))


def columns(a,b,c):
    base=3*c*c
    for x in range(c):
      for y in range(c):
       for j in range(6):
        for s in (-1,1):
            eps=s*(-1)**j
            ux,uy=x-a*U[j][0],y-a*U[j][1]
            wx,wy=x+b*U[(j+s)%6][0],y+b*U[(j+s)%6][1]
            terms=Counter()
            for ax,xx,yy,v in ((j,x,y,s),(j,ux,uy,-s),(j+s,wx,wy,s),(j+s,x,y,-s)):
                terms[(ax%3)*c*c+(xx%c)*c+yy%c]+=v
            part=int(s<0)
            gate=(a*uy-b*ux)%c if s>0 else (a*ux-b*uy)%c
            terms[base+part*c+gate]+=eps
            yield (x,y,j,s,part,gate,eps),{i:v for i,v in terms.items() if v}



def positive_control():
    """Check the shared column/sign/gate convention on a complete 143 tiling.

    The 3431-specific inequalities are not asserted for this different shape.
    """
    from fractions import Fraction as Q
    import importlib.util
    root=next(p for p in HERE.parents if (p/'research').is_dir() and (p/'scripts').is_dir())
    old=root/'research/2026-11-20/semiprimes/continuation/global-endpoints'
    raw=json.loads((old/'tiling_143.json').read_text())
    spec=importlib.util.spec_from_file_location('gate_excess_positive_control',old/'verify_endpoint_tiling.py')
    checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)
    checked=checker.check(raw);assert checked['verified_positive_tiling']
    a,b,c=raw['sides'];z=(Q(a,c),Q(b,c));B=a*(a+2*b)
    def mul(p,q):return p[0]*q[0]-p[1]*q[1],p[0]*q[1]+p[1]*q[0]+p[1]*q[1]
    cmap={lab[:4]:(lab,col) for lab,col in columns(a,b,c)}
    residual=Counter();gminus=Counter();signs=Counter()
    for (x,y,e),h,j,s in raw['tiles']:
        if h!=1:continue
        q=(Q(x,c**e),Q(y,c**e));conj=(q[0]+q[1],-q[1]);term=mul(mul((0,1),z),conj)
        anchor=(B*z[0]-term[0],B*z[1]-term[1]);assert all(v.denominator==1 for v in anchor)
        lab,col=cmap[int(anchor[0])%c,int(anchor[1])%c,(4-j)%6,-s]
        part,gate,eps=lab[-3:]
        for row,v in col.items():residual[row]+=v
        signs[eps]+=1
        if eps<0:gminus[part,gate]+=1
    assert all(not val for row,val in residual.items() if row<3*c*c)
    assert signs==Counter({1:56,-1:49})
    native=sum(v for (part,gate),v in gminus.items() if gate==0)
    excess=native+sum(max(v-1,0) for (part,gate),v in gminus.items() if gate)
    K=sum(v>0 for (part,gate),v in gminus.items() if gate)
    assert excess==49-K
    return {'full_143_tiling_verified':True,'odd_tiles':105,'signs':[56,49],'all_periodic_endpoint_rows_zero':True,'integer_gate_identity_checked':True,'target_specific_bound_applied':False}


def run():
    data=json.loads(gzip.decompress((HERE/'GATE_EXCESS_CERTIFICATE.json.gz').read_bytes()))
    a,b,c=data['tile'];assert (a,b,c)==(33,7,37)
    base=3*c*c
    ex=data['profile_exclusion'];D=ex['D'];w=ex['weights'];assert len(w)==base+2*c and all(isinstance(v,int) for v in w)
    greatest=-10**30;count=0
    for lab,col in columns(a,b,c):
        score=sum(w[i]*v for i,v in col.items());assert score<=D;greatest=max(greatest,score);count+=1
    numerator=ex['profile'][0]*w[base]+ex['profile'][1]*w[base+c]
    assert numerator==ex['numerator'] and numerator>111*D
    eb=data['excess_bound'];E=eb['D'];u=eb['eq_weights'];v=eb['cap_weights']
    assert len(u)==base+2*c+2 and len(v)==2*(c-1)
    assert all(isinstance(k,int) for k in u+v) and all(k<=0 for k in v)
    minimum_slack=10**30;costed_native=0;tile_count=0
    for lab,col in columns(a,b,c):
        x,y,j,s,part,gate,eps=lab
        score=sum(u[i]*k for i,k in col.items())+u[base+2*c+int(eps<0)]
        if eps<0 and gate:
            score+=v[part*(c-1)+gate-1]
        objective=int(eps<0 and gate==0)
        slack=E*objective-score;assert slack>=0;minimum_slack=min(minimum_slack,slack);tile_count+=1;costed_native+=objective
    for vv in v:assert -vv<=E
    numerator2=eb['profile'][0]*u[base]+eb['profile'][1]*u[base+c]+74*u[-2]+37*u[-1]+sum(v)
    assert numerator2==eb['numerator'] and numerator2>2*E
    assert 2*E<numerator2<3*E
    # Independent exact checks of E=m_native+sum(max(m_g-1,0))=m_total-K
    # for all small integral gate populations, including occupied/empty bins.
    identities=0
    from itertools import product
    for native in range(4):
      for masses in product(range(4),repeat=5):
        total=native+sum(masses);K=sum(x>0 for x in masses)
        excess=native+sum(max(x-1,0) for x in masses)
        assert excess==total-K;identities+=1
    report={'status':'PASS','tile':[a,b,c],'profile_minus4_41':{'all_tile_columns_checked':count,'maximum_score':greatest,'D':D,'lower_numerator':numerator,'lower_denominator':D,'excludes_population_111':True},'profile22_15':{'all_tile_columns_checked':tile_count,'slack_columns_checked':len(v),'native_negative_columns_costed':costed_native,'minimum_column_slack':minimum_slack,'excess_lower_numerator':numerator2,'excess_lower_denominator':E,'integer_excess_minimum':3,'nonempty_remote_parent_gates_maximum':34},'small_gate_identity_checks':identities,'positive_143_control':positive_control(),'scope':'This finite checker counts nonempty odd-parent long-edge gates. The occupied remote-cell upper bound additionally uses the written visibility theorem in INVISIBLE_EVEN_NODES.md. Both original targets remain open.'}
    (HERE/'GATE_EXCESS_REPLAY.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

if __name__=='__main__':
    if not __debug__:raise SystemExit('Run with assertions enabled.')
    print(json.dumps(run(),indent=2))
