#!/usr/bin/env python3
"""Independent exact audit of profile duals and finite charge enumeration.

Only the standard library is used. No optimization model or cut generator
is imported. Polygon columns and optional small Cartesian profile controls
are reconstructed independently. A passed dual/filter is not a tiling.
"""
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
import subprocess

U = ((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))


def rotate(p):
    x,y=p
    return -y,x+y


def flip(p):
    x,y=p
    return -x-y,y


def gate(a,b,c,p,s):
    x,y=p
    return ((a*y-b*x) if s==1 else (a*x-b*y))%c


def load(path):
    raw=json.loads(path.read_text())
    data=raw.get('certificate',raw)
    a,b,c=data['tile']
    assert a*a+a*b+b*b==c*c and math.gcd(a*b,c)==1
    D=data['D']; tables=data['endpoint_tables']
    assert isinstance(D,int) and D>0
    assert len(tables)==3
    assert all(len(t)==c and all(len(row)==c for row in t) for t in tables)
    assert all(isinstance(x,int) for t in tables for row in t for x in row)
    if 'up_remote_weights' in data:
        t=data['charge_multiplier_t']
        up=[t+x for x in data['up_remote_weights']]
        down=[t+x for x in data['down_remote_weights']]
    else:
        up=data['up_weights'];down=data['down_weights']
    assert len(up)==len(down)==c
    assert all(isinstance(x,int) for x in up+down)
    return data,(a,b,c),D,tables,up,down


def column(a,b,c,tables,up,down,x,y,j,s):
    q=(x,y)
    beta=(x-a*U[j][0],y-a*U[j][1])
    alpha=(x+b*U[(j+s)%6][0],y+b*U[(j+s)%6][1])
    vertices=[beta,q,alpha] if s==1 else [alpha,q,beta]
    area=sum(p[0]*r[1]-p[1]*r[0] for p,r in zip(vertices,vertices[1:]+vertices[:1]))
    assert area==a*b
    weight=0;lengths=[]
    for p,r in zip(vertices,vertices[1:]+vertices[:1]):
        v=(r[0]-p[0],r[1]-p[1]);norm=v[0]*v[0]+v[0]*v[1]+v[1]*v[1]
        lengths.append(norm)
        if norm==c*c:continue
        length=a if norm==a*a else b
        assert norm==length*length
        axis=next(k for k in range(3) if v in ((length*U[k][0],length*U[k][1]),(-length*U[k][0],-length*U[k][1])))
        weight+=tables[axis][r[0]%c][r[1]%c]-tables[axis][p[0]%c][p[1]%c]
    assert sorted(lengths)==sorted((a*a,b*b,c*c))
    eps=s*(-1 if j%2 else 1)
    return weight+eps*(up if s==1 else down)[gate(a,b,c,beta,s)]


def variants(a,b,c,D,up,down):
    """Derive all transformed gate weights from images of actual residues."""
    representative={s:{} for s in (-1,1)}
    for x in range(c):
        for y in range(c):
            for s in (-1,1):
                representative[s].setdefault(gate(a,b,c,(x,y),s),(x,y))
    out=[]
    for k in range(6):
        for reflected in (False,True):
            pair={}
            for s in (1,-1):
                values=[]
                for r in range(c):
                    p=representative[s][r]
                    if reflected:p=flip(p)
                    for _ in range(k):p=rotate(p)
                    hand=-s if reflected else s
                    target=gate(a,b,c,p,hand)
                    values.append((-1)**k*(up if hand==1 else down)[target])
                pair[s]=values
            out.append((D,pair[1],pair[-1]))
    return out


def verify_geometry_symmetries(a,b,c):
    shifts={(gate(a,b,c,(x,y),1),gate(a,b,c,(x,y),-1)) for x in range(c) for y in range(c)}
    assert len(shifts)==c*c
    checks=0
    for x in range(c):
        for y in range(c):
            p=(x,y)
            for s in (-1,1):
                r=gate(a,b,c,p,s)
                factor=(-a*pow(b,-1,c) if s==1 else -b*pow(a,-1,c))%c
                assert gate(a,b,c,rotate(p),s)==factor*r%c
                factor=(a*pow(b,-1,c) if s==1 else b*pow(a,-1,c))%c
                assert gate(a,b,c,flip(p),-s)==factor*r%c
                checks+=2
    for j in range(6):
        for s in (-1,1):
            eps=s*(-1 if j%2 else 1)
            assert s*(-1 if (j+1)%2 else 1)==-eps
            assert (-s)*(-1 if (3-j)%2 else 1)==eps
    return {'independent_translation_pairs':len(shifts),'rotation_reflection_residue_checks':checks,'status':'PASS'}


def verify(path):
    data,tile,D,tables,up,down=load(path);a,b,c=tile
    smallest=None;largest=None
    for x in range(c):
        for y in range(c):
            for j in range(6):
                for s in (-1,1):
                    score=column(a,b,c,tables,up,down,x,y,j,s)
                    assert score<=D,(str(path),x,y,j,s,score,D)
                    smallest=score if smallest is None else min(smallest,score)
                    largest=score if largest is None else max(largest,score)
    report={'source':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'tile':tile,'columns':12*c*c,'minimum_score':smallest,'maximum_score':largest,'D':D,'status':'PASS'}
    gup=gdown=None
    if 'up_gate_charges' in data:
        gup=data['up_gate_charges'];gdown=data['down_gate_charges']
    elif 'native_up_charge_units' in data:
        gup=[0]*c;gdown=[0]*c
        gup[0]=data['native_up_charge_units'];gdown[0]=data['native_down_charge_units']
        (gup if data['hand']=='up' else gdown)[data['remote_residue']]=data['remote_charge_units']
    if gup is not None:
        assert len(gup)==len(gdown)==c and sum(gup)+sum(gdown)==0
        assert all(isinstance(x,int) for x in gup+gdown)
        qup=[(a-b)*x for x in gup];qdown=[(a-b)*x for x in gdown]
        qup[0]+=2*c;qdown[0]-=c
        lower=sum(x*y for x,y in zip(up,qup))+sum(x*y for x,y in zip(down,qdown))
        assert lower==data['lower_numerator'] and data['lower_denominator']==D
        report.update(profile_lower_numerator=lower,excludes_3c_for_recorded_profile=lower>3*c*D)
    return report,variants(a,b,c,D,up,down)


def brute_profiles(c,d,cap,cuts):
    """Cartesian remote-charge enumeration, not positive-multiset recursion."""
    accepted=set();visited=0;reserved=0
    for remote in itertools.product(range(-1,cap//d+1),repeat=2*(c-1)):
        P=sum(max(g,0) for g in remote);M=sum(max(-g,0) for g in remote)
        if P>2*c//d or M>c//d:continue
        lo=-((3*c)//d)  # ceil(-3c/d)
        hi=(cap-2*c)//d
        for gu in range(lo,hi+1):
            gd=-gu-sum(remote)
            qu=2*c+d*gu;qd=-c+d*gd
            if not -c<=qu<=cap or not -c<=qd<=cap:continue
            visited+=1
            if max(qu,0)+max(qd,0)+d*P>2*c:continue
            if max(-qu,0)+max(-qd,0)+d*M>c:continue
            reserved+=1
            up=[qu]+[d*g for g in remote[:c-1]]
            down=[qd]+[d*g for g in remote[c-1:]]
            valid=True
            for D,wu,wd in cuts:
                # Enumerate each pair of shifts directly, rather than relying
                # on the C++ sum-of-separate-maxima optimization.
                for su in range(c):
                    for sd in range(c):
                        score=sum(up[r]*wu[(r+su)%c]+down[r]*wd[(r+sd)%c] for r in range(c))
                        if score>3*c*D:valid=False;break
                    if not valid:break
                if not valid:break
            if valid:accepted.add((gu,gd,remote))
    return accepted,visited,reserved


def compare_enumerator(binary):
    reports=[]
    cases=[(3,2,4,[]),(5,3,6,[]),(5,3,6,[(2,[3,-2,1,0,-3],[-1,3,-2,2,0]),(1,[-2,0,3,1,-1],[2,-3,0,1,2])])]
    for c,d,cap,cuts in cases:
        expected,visited,reserved=brute_profiles(c,d,cap,cuts)
        lines=[f'{c} {d} {cap} {2*c//d} {c//d} {len(cuts)} 100000000']
        for D,up,down in cuts:lines.extend([str(D),' '.join(map(str,up)),' '.join(map(str,down))])
        result=subprocess.run([str(binary)],input='\n'.join(lines)+'\n',capture_output=True,text=True,check=True)
        records=[json.loads(s) for s in result.stdout.splitlines()]
        summary=records.pop();actual=set()
        for record in records:
            remote=[0]*(2*(c-1))
            for i in record['remote_positive_indices']:remote[i]+=1
            if record['remote_negative_index']>=0:remote[record['remote_negative_index']]-=1
            entry=(record['native_up'],record['native_down'],tuple(remote))
            assert entry not in actual
            actual.add(entry)
        assert summary['exhaustive'] and actual==expected
        assert summary['visited']==visited and summary['reserve_passed']==reserved
        assert summary['cut_passed']==len(expected)
        reports.append({'c':c,'d':d,'capacity':cap,'cuts':len(cuts),'visited':visited,'reserve_passed':reserved,'survivors':len(expected),'status':'PASS'})
    return reports


def check_cut_file(path,cuts,tile):
    data=list(map(int,path.read_text().split()));c,d,cap,P,M,n,limit=data[:7]
    a,b,expected_c=tile
    assert c==expected_c and d==a-b and cap==(51 if c==43 else 44)
    assert P==2*c//d and M==c//d==1 and d>=2 and limit>=0
    assert n==len(cuts) and len(data)==7+n*(1+2*c)
    actual=[];offset=7
    for _ in range(n):
        D=data[offset];up=data[offset+1:offset+1+c];down=data[offset+1+c:offset+1+2*c]
        actual.append((D,up,down));offset+=1+2*c
        assert 6*c*max([abs(x) for x in up+down]+[D])<2**63
    assert actual==cuts
    return {'file':path.name,'cuts':n,'exact_transformed_arrays_match':True,'int64_arithmetic_bound':'PASS','status':'PASS'}


def universe_counts(tile):
    """Closed-form counts independent of C++ recursion and endpoint cuts."""
    a,b,c=tile;d=a-b;cap=51 if c==43 else 44
    assert (a,b,c) in ((35,13,43),(33,7,37))
    n=2*(c-1);max_entry=cap//d
    visited=reserved=0;rows=[]
    for positive in range(2*c//d+1):
        for negative in range(c//d+1):
            patterns=0
            for occupied in range(positive+1):
                doubled=positive-occupied
                if not 0<=doubled<=occupied:continue
                if max_entry==1 and doubled:continue
                patterns+=math.comb(n,occupied)*math.comb(occupied,doubled)*(n-occupied if negative else 1)
            eligible=retained=0
            for gu in range(-(3*c//d),(cap-2*c)//d+1):
                gd=-gu-positive+negative
                qu=2*c+d*gu;qd=-c+d*gd
                if not -c<=qu<=cap or not -c<=qd<=cap:continue
                eligible+=1
                if max(qu,0)+max(qd,0)+d*positive>2*c:continue
                if max(-qu,0)+max(-qd,0)+d*negative>c:continue
                retained+=1
            visited+=patterns*eligible;reserved+=patterns*retained
            rows.append({'positive_units':positive,'negative_units':negative,'remote_patterns':patterns,'native_before_reserves':eligible,'native_after_reserves':retained})
    return {'visited':visited,'reserve_passed':reserved,'derivation_by_block_counts':rows}


if __name__=='__main__':
    if not __debug__:raise SystemExit('Run without -O.')
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('certificates',type=Path,nargs='+')
    p.add_argument('--cut-file',type=Path)
    p.add_argument('--enumerator',type=Path)
    p.add_argument('--filter-output',type=Path)
    p.add_argument('--out',type=Path,required=True)
    ar=p.parse_args();reports=[];cuts=[];tile=None
    for path in ar.certificates:
        report,more=verify(path);reports.append(report);cuts.extend(more)
        if tile is None:tile=tuple(report['tile'])
        assert tile==tuple(report['tile'])
    output={'certificates':reports,'geometric_symmetries':verify_geometry_symmetries(*tile),'profile_universe':universe_counts(tile),'scope':'Exact necessary residue-dual inequalities and finite enumeration controls only; not a geometric tiling certificate.'}
    if ar.cut_file:output['serialized_cuts']=check_cut_file(ar.cut_file,cuts,tile)
    if ar.enumerator:output['independent_small_enumerations']=compare_enumerator(ar.enumerator)
    if ar.filter_output:
        summary=json.loads(ar.filter_output.read_text().splitlines()[-1])
        assert summary['summary'] and summary['exhaustive']
        assert summary['visited']==output['profile_universe']['visited']
        assert summary['reserve_passed']==output['profile_universe']['reserve_passed']
        assert sum(summary['rejected'])+summary['cut_passed']==summary['reserve_passed']
        output['complete_filter_accounting']={'summary':summary,'status':'PASS'}
    ar.out.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'certificates':len(reports),'columns':sum(r['columns'] for r in reports),'geometric_symmetries':output['geometric_symmetries'],'serialized_cuts':output.get('serialized_cuts'),'small_enumerations':output.get('independent_small_enumerations'),'status':'PASS'},indent=2))
