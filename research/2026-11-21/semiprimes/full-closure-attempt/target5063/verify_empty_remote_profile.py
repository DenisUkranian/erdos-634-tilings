#!/usr/bin/env python3
"""Exact native single/pair inequality and rational 215-row witness.

Independent of SciPy and of the LP column-merging implementation. This
checks a necessary periodic projection and does not construct a tiling.
"""
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'research').is_dir() and (p/'scripts').is_dir())
U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))

def column(x,y,j,s,a,b,c):
    u=x-a*U[j][0],y-a*U[j][1]
    w=x+b*U[(j+s)%6][0],y+b*U[(j+s)%6][1]
    eps=s*(-1)**j
    gate=((a*u[1]-b*u[0]) if s>0 else (a*u[0]-b*u[1]))%c
    row=Counter()
    for axis,p,value in ((j,(x,y),s),(j,u,-s),(j+s,w,s),(j+s,(x,y),-s)):
        row[(axis%3)*c*c+(p[0]%c)*c+p[1]%c]+=value
    row[3*c*c+(0 if s>0 else c)+gate]+=eps
    mate=((u[0]+w[0]-x)%c,(u[1]+w[1]-y)%c,(j+3)%6,s)
    return row,gate,eps,mate

def positive_control():
    source=ROOT/'research/2026-11-21/semiprimes/continued-rigidity/physical/CONTROL_143.json'
    data=json.loads(source.read_text());a,b,c=data['sides'];z=(F(a,c),F(b,c));rho=(0,1)
    def mul(p,q):return(p[0]*q[0]-p[1]*q[1],p[0]*q[1]+p[1]*q[0]+p[1]*q[1])
    def sub(p,q):return(p[0]-q[0],p[1]-q[1])
    shift=(a*(a+2*b)*z[0],a*(a+2*b)*z[1]);rz=mul(rho,z)
    tiles=set()
    for (x,y,e),h,j,s in data['tiles']:
        if h!=1:continue
        q=(F(x,c**e),F(y,c**e));conj=(q[0]+q[1],-q[1]);p=sub(shift,mul(rz,conj))
        assert all(v.denominator==1 for v in p)
        tiles.add((int(p[0]),int(p[1]),(4-j)%6,-s))
    assert len(tiles)==105
    residual=Counter();gates=Counter();paired=set()
    for x,y,j,s in tiles:
        row,g,eps,_=column(x,y,j,s,a,b,c)
        residual.update(row);gates[(s,g)]+=eps
        if g:
            mate=(x-a*U[j][0]+b*U[(j+s)%6][0],y-a*U[j][1]+b*U[(j+s)%6][1],(j+3)%6,s)
            assert mate in tiles
            paired.add(tuple(sorted(((x,y,j,s),mate))))
    assert all(value==0 for r,value in residual.items() if r<3*c*c)
    assert gates[(1,0)]==14 and gates[(-1,0)]==-7
    assert all(value==0 for (s,g),value in gates.items()if g)
    return {'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'N':143,'odd_population':105,'native_gate_profile':[14,-7],'remote_actual_whole_pairs':len(paired),'all_remote_tiles_have_actual_mates':True}

def main():
    dual=json.loads((HERE/'EMPTY_REMOTE_EXACT_DUAL_5063.json').read_text());a,b,c=dual['tile'];D=dual['D'];assert (a,b,c,D)==(35,13,43,13)
    potential=sum(dual['endpoint_tables'],[])+dual['gate_weights'];assert len(potential)==3*c*c+2*c
    labels=[];columns=[];gates=[];signs=[];mate_keys=[]
    for x in range(c):
        for y in range(c):
            for j in range(6):
                for s in (-1,1):
                    row,gate,eps,mate=column(x,y,j,s,a,b,c)
                    labels.append((x,y,j,s));columns.append(row);gates.append(gate);signs.append(eps);mate_keys.append(mate)
    index={lab:i for i,lab in enumerate(labels)};mates=[index[t]for t in mate_keys]
    assert all(mates[k]==i and k!=i and signs[k]==-signs[i] and gates[k]==gates[i]for i,k in enumerate(mates))
    score=[sum(value*potential[r]for r,value in row.items())for row in columns]
    groups=[];singles=pairs=0;max_single=max_pair=-10**9
    for i,g in enumerate(gates):
        if g==0:
            assert score[i]<=D;max_single=max(max_single,score[i]);groups.append([i]);singles+=1
        elif i<mates[i]:
            assert score[i]+score[mates[i]]<=2*D;max_pair=max(max_pair,score[i]+score[mates[i]]);groups.append([i,mates[i]]);pairs+=1
    assert (singles,pairs,max_single,max_pair)==(516,10836,13,26)
    assert (potential[3*c*c],potential[3*c*c+c])==(83,-3)
    # The half-turn/reflection column bijection exchanges the two native gates
    # and preserves epsilon, so the transposed bound is equally necessary.
    for i,(x,y,j,s) in enumerate(labels):
        reflected=((-x-y)%c,y%c,(3-j)%6,-s)
        k=index[reflected]
        factor=(a*pow(b,-1,c) if s>0 else b*pow(a,-1,c))%c
        assert signs[k]==signs[i] and gates[k]==factor*gates[i]%c
        assert index[((-mate_keys[i][0]-mate_keys[i][1])%c,mate_keys[i][1]%c,(3-mate_keys[i][2])%6,-mate_keys[i][3])]==mates[k]
    survivors=[]
    for e in range(-100,101):
        up=2*c+(a-b)*e;down=-c-(a-b)*e
        if 83*up-3*down<=D*215 and 83*down-3*up<=D*215:survivors.append([e,up,down])
    assert survivors==[[-3,20,23]]
    # The inequalities directly imply 9<=Q_up<=34; no finite e cutoff is used.
    assert (D*215+3*c)//86==34
    witness=json.loads((HERE/'EMPTY_REMOTE_RATIONAL_215_5063.json').read_text());assert witness['tile']==[a,b,c]
    kappa=F(witness['uniform_column_kernel_coefficient']);assert kappa>0
    x=[kappa]*len(labels);seen=set()
    for k,value in witness['sparse_minimum_point']:
        assert k not in seen;seen.add(k);value=F(value);assert value>0
        for i in groups[k]:x[i]+=value
    residual=[F(0)]*len(potential);positive=negative=F(0)
    for i,value in enumerate(x):
        assert value>0
        for r,coef in columns[i].items():residual[r]+=coef*value
        if signs[i]>0:positive+=value
        else:negative+=value
        if gates[i]:assert value==x[mates[i]]
    expected=[F(0)]*len(potential);expected[3*c*c]=20;expected[3*c*c+c]=23
    assert residual==expected and (positive,negative)==(129,86)
    formal=json.loads((HERE/'EMPTY_REMOTE_SIGNED_INTEGER_215_5063.json').read_text())
    formal_columns=[0]*len(labels);seen=set()
    for group,amount in formal['signed_group_multiplicities']:
        assert group not in seen and isinstance(amount,int);seen.add(group)
        for i in groups[group]:formal_columns[i]+=amount
    formal_residual=[0]*len(potential);formal_plus=formal_minus=0
    for i,amount in enumerate(formal_columns):
        for r,coef in columns[i].items():formal_residual[r]+=coef*amount
        if signs[i]>0:formal_plus+=amount
        else:formal_minus+=amount
        if gates[i]:assert amount==formal_columns[mates[i]]
    assert formal_residual==expected and (formal_plus,formal_minus)==(129,86)
    negative=sum(v<0 for _,v in formal['signed_group_multiplicities'])
    assert negative==formal['negative_group_coefficients']==949
    replay={'status':'PASS','scope':'Exact necessary native periodic single/pair model; not integer placements or a full tiling.','dual':{'D':D,'native_weights':[83,-3],'single_columns_checked':singles,'remote_pairs_checked':pairs,'maximum_single_score':max_single,'maximum_pair_score':max_pair,'all_integer_empty_remote_profiles_at_215':survivors},'rational_witness':{'population':215,'positive':129,'negative':86,'native_currents':[20,23],'all_5547_endpoint_rows_zero':True,'all_84_remote_gate_currents_zero':True,'all_10836_remote_mate_equalities':True,'strictly_positive_rational_columns':len(labels),'integer_tile_multiplicities':False,'physical_tiling':False},'signed_integer_witness':{'all_rows_checked':True,'formal_population':215,'formal_sign_totals':[129,86],'negative_group_coefficients':negative,'nonnegative_integer_solution':False},'positive_control_143':positive_control()}
    (HERE/'EMPTY_REMOTE_PROFILE_REPLAY.json').write_text(json.dumps(replay,indent=2)+'\n');print(json.dumps(replay,indent=2))
if __name__=='__main__':main()
