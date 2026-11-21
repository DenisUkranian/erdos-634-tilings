#!/usr/bin/env python3
"""Exact minimal-mode 3431 gate, core, and endpoint budget checks."""
from pathlib import Path
from collections import Counter
import gzip,hashlib,importlib.util,json

HERE=Path(__file__).resolve().parent
U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))


def mate_and_gate(a,b,c):
    checked=0
    for x in range(c):
        for y in range(c):
            for j in range(6):
                for s in (-1,1):
                    def mate(t):
                        x,y,j,s=t
                        return ((x-a*U[j][0]+b*U[(j+s)%6][0])%c,
                                (y-a*U[j][1]+b*U[(j+s)%6][1])%c,(j+3)%6,s)
                    def gate(t):
                        x,y,j,s=t;ux=x-a*U[j][0];uy=y-a*U[j][1]
                        return s,(a*uy-b*ux)%c if s==1 else (a*ux-b*uy)%c
                    t=(x,y,j,s);other=mate(t)
                    assert other!=t and mate(other)==t
                    assert gate(t)==gate(other)
                    assert s*(-1)**j == -other[3]*(-1)**other[2]
                    checked+=1
    return dict(tile=[a,b,c],labels_checked=checked,mate_orbits=checked//2)


def weak_profiles():
    rows=[]
    for gu in range(-4,-1):
        for gd in range(4):
            up=74+26*gu;down=-37+26*gd
            assert -37<=up<=44 and -37<=down<=44
            for sp in range(3):
                for sn in range(2):
                    if gu+gd+sp-sn:continue
                    demanded_plus=max(up,0)+max(down,0)+26*sp
                    demanded_minus=max(-up,0)+max(-down,0)+26*sn
                    if demanded_plus>74 or demanded_minus>37:continue
                    S=sp+sn;leftover=111-abs(up)-abs(down)-26*S
                    assert leftover>=0 and leftover%2==0
                    Kmax=leftover//2
                    native_up=(8+37*max(gu+1,0),19+37*max(-gu-1,0))
                    native_blocks=(2,5,10,13)[gd]
                    assert native_blocks>=2 and (native_blocks-gd)%2==0
                    if gd:assert 22*native_blocks>=91*gd
                    native_down=(37*(native_blocks+gd)//2,37*(native_blocks-gd)//2)
                    assert native_up[0]-native_up[1]==26+37*gu
                    assert native_down[0]-native_down[1]==37*gd
                    assert native_up[0]%37==8 and native_up[1]%37==19
                    allocations=[]
                    for K in range(Kmax+1):
                        plus=native_up[0]+native_down[0]+111*sp+74*sn+37*K
                        minus=native_up[1]+native_down[1]+74*sp+111*sn+37*K
                        assert plus-minus==26
                        total=111+plus+minus
                        assert total<=3431 and (3431-total)%74==0
                        padding=(3431-total)//74
                        assert plus+37*padding==1673 and minus+37*padding==1647
                        assert S+K<=37
                        allocations.append(dict(zero_defective_gates=K,total_before_padding=total,balanced_blocks_added=padding))
                    rows.append(dict(gu=gu,gd=gd,positive_charged_remote=sp,negative_charged_remote=sn,
                                     up_current=up,down_current=down,maximum_zero_defective_gates=Kmax,
                                     native_population=sum(native_up)+sum(native_down),
                                     maximum_pre_padding_population=allocations[-1]['total_before_padding'],
                                     checked_allocations=allocations))
    assert len(rows)==13
    assert max(r['maximum_pre_padding_population'] for r in rows)==3283
    return rows


def dependency_checks():
    path=HERE.parent/'core-budget/verify_core_budget.py'
    spec=importlib.util.spec_from_file_location('gate_budget_core_dependency',path)
    core=importlib.util.module_from_spec(spec);spec.loader.exec_module(core)
    checked=[core.check_certificate(HERE.parent/f'core-budget/CORE_3431_G_MINUS{-g}.json') for g in (-4,-3,-2)]
    assert {r['native_charge_units']:r['rounded_population'] for r in checked}=={-4:582,-3:397,-2:212}
    source=HERE.parent/'target3431/GATE_EXCESS_CERTIFICATE.json.gz'
    data=json.loads(gzip.decompress(source.read_bytes()));assert data['tile']==[33,7,37]
    ex=data['profile_exclusion'];eb=data['excess_bound'];a,b,c=33,7,37;base=3*c*c
    D=ex['D'];E=eb['D'];w=ex['weights'];u=eb['eq_weights'];v=eb['cap_weights']
    assert all(isinstance(k,int) for k in w+u+v) and all(-E<=k<=0 for k in v)
    columns=0
    for x in range(c):
        for y in range(c):
            for j in range(6):
                for s in (-1,1):
                    ux,uy=x-a*U[j][0],y-a*U[j][1]
                    wx,wy=x+b*U[(j+s)%6][0],y+b*U[(j+s)%6][1]
                    row=Counter()
                    for axis,xx,yy,value in ((j,x,y,s),(j,ux,uy,-s),(j+s,wx,wy,s),(j+s,x,y,-s)):
                        row[(axis%3)*c*c+(xx%c)*c+yy%c]+=value
                    sign=s*(-1)**j;part=int(s<0)
                    gate=(a*uy-b*ux)%c if s>0 else (a*ux-b*uy)%c
                    row[base+part*c+gate]+=sign
                    assert sum(w[k]*z for k,z in row.items())<=D
                    score=sum(u[k]*z for k,z in row.items())+u[base+2*c+int(sign<0)]
                    if sign<0 and gate:score+=v[part*(c-1)+gate-1]
                    assert score<=E*int(sign<0 and gate==0)
                    columns+=1
    ex_num=-4*w[base]+41*w[base+c]
    excess_num=22*u[base]+15*u[base+c]+74*u[-2]+37*u[-1]+sum(v)
    assert ex_num==ex['numerator']>111*D
    assert excess_num==eb['numerator'] and 2*E<excess_num<3*E
    return dict(core_certificates=checked,endpoint_gate_certificate_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                endpoint_columns_checked=columns,excluded_profile=[-4,41],native22_15_parent_used_zero_gates_maximum=34)


def strengthened_profiles(weak):
    rows=[]
    for old in weak:
        gu,gd=old['gu'],old['gd'];sp=old['positive_charged_remote'];sn=old['negative_charged_remote'];S=sp+sn
        core={-4:582,-3:397,-2:212}[gu];native_zero=(0,5,10,13)[gd]*37
        Kold=old['maximum_zero_defective_gates']
        base=111+core+native_zero+185*S
        budget_cap=(3431-base)//74
        excluded=(gu,gd,sp,sn)==(-3,3,0,0)
        parent_used_cap=34 if (gu,gd,sp,sn)==(-2,2,0,0) else None
        K=min(Kold,budget_cap,parent_used_cap if parent_used_cap is not None else 72)
        assert K>=0
        row=dict(gu=gu,gd=gd,positive_charged_remote=sp,negative_charged_remote=sn,
                 up_current=old['up_current'],down_current=old['down_current'],
                 core_population_floor=core,native_height0_population_floor=native_zero,
                 orbit_count_cap=Kold,population_budget_cap=budget_cap,
                 parent_used_zero_gate_cap=parent_used_cap,
                 profile_excluded_by_endpoint_certificate=excluded,
                 remaining_occupied_balanced_remote_node_cap=None if excluded else K,
                 remaining_mate_defective_zero_gate_cap=None if excluded else K,
                 population_at_old_orbit_cap=base+74*Kold,
                 population_at_remaining_cap=None if excluded else base+74*K)
        rows.append(row)
    assert len(rows)==13
    cut=next(r for r in rows if (r['gu'],r['gd'],r['positive_charged_remote'],r['negative_charged_remote'])==(-3,2,1,0))
    assert cut['orbit_count_cap']==33 and cut['population_budget_cap']==32 and cut['population_at_old_orbit_cap']==3505
    assert sum(r['profile_excluded_by_endpoint_certificate'] for r in rows)==1
    return rows


def main():
    if not __debug__:raise RuntimeError('Assertions must be enabled.')
    weak=weak_profiles();dependencies=dependency_checks();strong= strengthened_profiles(weak)
    result=dict(status='PASS',scope='Exact minimal-mode 3431 charge and occupied-even-node budgets with verified inhomogeneous core and endpoint certificates, using the separately written visibility theorem; no full target exclusion.',
                mate_checks=[mate_and_gate(*shape) for shape in ((5,3,7),(33,7,37),(35,13,43))],
                dependencies=dependencies,strengthened_profiles=strong,
                geometric_visibility_dependency=dict(
                    statement='In a complete target tiling with short heights 0,1,2 and all odd tiles in native zR, every occupied remote even cell has a nonempty odd-parent long-edge gate.',
                    main_proof='../target3431/INVISIBLE_EVEN_NODES.md',
                    independent_audit='INVISIBLE_EVEN_NODES_AUDIT.md',
                    audit_sha256=hashlib.sha256((HERE/'INVISIBLE_EVEN_NODES_AUDIT.md').read_bytes()).hexdigest(),
                    status='Written geometric proof; not inferred from this finite arithmetic replay.'),
                weaker_projection_profiles=weak,full_3431_excluded=False,full_5063_excluded=False,
                native_gd_zero_floor='Zero: the native height0 node may be empty; the weaker arithmetic construction optionally allocated74.',
                conclusion='The core budget reduces the occupied balanced remote node cap from33 to32 in one profile. The endpoint certificate excludes native(-4,41) with zero remote charges and bounds parent-used gates by34 for native(22,15) with zero remote charges; visibility also bounds occupied remote even nodes by34 there. Neither target is closed.')
    (HERE/'EMPTY_GATE_BUDGET_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],charge_profiles=len(strong),
                         weaker_arithmetic_allocations=sum(len(r['checked_allocations']) for r in weak),
                         strengthened_profiles=strong,mate_checks=result['mate_checks']),indent=2))


if __name__=='__main__':main()
