#!/usr/bin/env python3
"""Exact rational full-endpoint witnesses for two cells sharing a215-node.

Standard library only. Reuses the independently audited exact Fourier
inverse bound. Endpoint columns are rebuilt from counterclockwise polygons.
The approximate rational points are corrected by the rational Moore-Penrose
inverse; integer norm bounds prove positivity and both sign-specific caps.
"""
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'research').is_dir() and (p/'scripts').is_dir())
FOURIER=ROOT/'research/2026-11-21/semiprimes/global-invariant/verify_3431_rational_projection.py'
U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))


def check_cell(data,K):
    a,b,c=35,13,43
    D=data['point_denominator'];base=data['uniform_point_numerator']
    assert isinstance(D,int) and D>0 and isinstance(base,int)
    values=[base]*(12*c*c)
    def column(x,y,j,s):return ((x*c+y)*6+j)*2+(s==1)
    seen=set()
    for x,y,j,s,increment in data['point_increments']:
        assert all(isinstance(v,int) for v in (x,y,j,s,increment))
        assert 0<=x<c and 0<=y<c and 0<=j<6 and s in (-1,1)
        index=column(x,y,j,s)
        assert index not in seen;seen.add(index)
        values[index]+=increment
    minimum=min(values);assert minimum>0
    gatebase=3*c*c;populationrow=gatebase+2*c
    rows=[0]*(populationrow+1)
    bins={1:[0]*(2*c),-1:[0]*(2*c)}
    def endpoint(axis,p):return axis*c*c+(p[0]%c)*c+p[1]%c
    for x in range(c):
        for y in range(c):
            for j in range(6):
                for s in (-1,1):
                    v=values[column(x,y,j,s)]
                    q=(x,y)
                    beta=(x-a*U[j][0],y-a*U[j][1])
                    alpha=(x+b*U[(j+s)%6][0],y+b*U[(j+s)%6][1])
                    vertices=[beta,q,alpha] if s==1 else [alpha,q,beta]
                    area=sum(p[0]*r[1]-p[1]*r[0] for p,r in zip(vertices,vertices[1:]+vertices[:1]))
                    assert area==a*b
                    lengths=[]
                    for p,r in zip(vertices,vertices[1:]+vertices[:1]):
                        dx,dy=r[0]-p[0],r[1]-p[1]
                        squared=dx*dx+dx*dy+dy*dy
                        lengths.append(squared)
                        if squared==c*c:continue
                        length=a if squared==a*a else b
                        assert squared==length*length
                        axis=next(k for k in range(3) if (dx,dy) in (
                            (length*U[k][0],length*U[k][1]),(-length*U[k][0],-length*U[k][1])))
                        rows[endpoint(axis,r)]+=v
                        rows[endpoint(axis,p)]-=v
                    assert sorted(lengths)==[b*b,a*a,c*c]
                    sign=s*(-1 if j%2 else 1)
                    gate=((a*beta[1]-b*beta[0])%c if s==1 else
                          c+(a*beta[0]-b*beta[1])%c)
                    rows[gatebase+gate]+=sign*v
                    rows[populationrow]+=v
                    bins[sign][gate]+=v
    pos,neg=data['positive_population'],data['negative_population']
    q=data['gate_currents']
    assert len(q)==2*c and all(isinstance(v,int) for v in q)
    assert sum(q)==pos-neg
    target=[0]*len(rows)
    target[gatebase:populationrow]=[v*D for v in q]
    target[populationrow]=(pos+neg)*D
    residual=[t-r for t,r in zip(target,rows)]
    squared=sum(v*v for v in residual)
    assert K*squared<minimum*minimum
    capacities={1:min(pos,(8*pos+35*neg)//c),-1:min(neg,(8*neg+35*pos)//c)}
    slacks={s:min(capacities[s]*D-v for v in bins[s]) for s in (1,-1)}
    assert all(slacks[s]>0 and (3*c)**2*K*squared<slacks[s]**2 for s in (1,-1))
    assert sum(max(v,0) for v in q)<=pos
    assert sum(max(-v,0) for v in q)<=neg
    assert all(-capacities[-1]<=v<=capacities[1] for v in q)
    return {'status':'PASS','variables':len(values),'equations':len(rows),
            'point_denominator':D,'minimum_approximate_numerator':minimum,
            'residual_squared_numerator':squared,'norm_bound_K':K,
            'strict_positivity_inequality':[K*squared,minimum**2],
            'sign_gate_capacities':{str(s):capacities[s] for s in (1,-1)},
            'minimum_sign_gate_slacks':{str(s):slacks[s] for s in (1,-1)},
            'gate_capacity_error_bound_squared':(3*c)**2*K*squared,
            'exact_population':pos+neg,'exact_positive_population':pos,
            'exact_negative_population':neg,'exact_gate_currents':q}


def main():
    path=HERE/'TWO_CELL_RATIONAL_CERTIFICATE.json.gz'
    compressed=path.read_bytes();assert compressed[4:8]==b'\0\0\0\0'
    cert=json.loads(gzip.decompress(compressed));assert cert['tile']==[35,13,43]
    source=ROOT/cert['fourier_bound_source']
    assert hashlib.sha256(source.read_bytes()).hexdigest()==cert['fourier_bound_source_sha256']
    fourier_data=json.loads(gzip.decompress(source.read_bytes()))
    assert fourier_data['tile']==[35,13,43]
    spec=importlib.util.spec_from_file_location('audited_exact_fourier_bound',FOURIER)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    K,histogram=module.inverse_bound(fourier_data)
    reports=[]
    assert [case['native_column'] for case in cert['cases']]==[0,1]
    for case in cert['cases']:
        assert [(cell['node_row'],cell['node_column'],cell['positive_population'],cell['negative_population'])
                for cell in case['cells']]==[(0,0,43,43),(0,1,86,43)]
        assert case['native_row']==0
        cells=[check_cell(cell,K) for cell in case['cells']]
        q0,q1=[cell['gate_currents'] for cell in case['cells']]
        node_currents=[[q0[i]+q1[i] for i in range(43)],q0[43:],q1[43:]]
        charge_units=[]
        for node,current in enumerate(node_currents):
            offset=86 if node==0 else (-43 if node==1+case['native_column'] else 0)
            residues=[v-(offset if gate==0 else 0) for gate,v in enumerate(current)]
            assert all(v%22==0 for v in residues)
            charge_units.append([v//22 for v in residues])
        assert sum(sum(e) for e in charge_units)==0
        reports.append({'name':case['name'],'native_column':case['native_column'],
                        'cells':cells,'complete_node_currents':node_currents,
                        'complete_node_charge_units':charge_units})
    out={'status':'PASS','tile':[35,13,43],
         'certificate_sha256':hashlib.sha256(compressed).hexdigest(),
         'fourier_bound_certificate_sha256':cert['fourier_bound_source_sha256'],
         'fourier_verifier_sha256':hashlib.sha256(FOURIER.read_bytes()).hexdigest(),
         'fourier_blocks_checked':43**2,'block_row_counts':histogram,
         'cases':reports,
         'integer_cell_gate_currents':True,'integer_complete_node_charge_units':True,
         'integer_individual_tile_multiplicities':False,'physical_tiling_constructed':False,
         'scope':'Strictly positive rational full-endpoint witnesses with the prescribed two-cell sign populations and exact shared-node currents, for both possible native roles in the split tree. This is an exact limitation of the continuous periodic cell relaxation, not a full 215 or 5063 construction.'}
    (HERE/'TWO_CELL_RATIONAL_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({key:value for key,value in out.items() if key!='cases'},indent=2))
    for case in reports:
        for index,record in enumerate(case['cells']):
            print(json.dumps({'case':case['name'],'cell':index,
                **{key:value for key,value in record.items() if key!='exact_gate_currents'}},indent=2))


if __name__=='__main__':
    if not __debug__:raise SystemExit('Run with assertions enabled.')
    main()
