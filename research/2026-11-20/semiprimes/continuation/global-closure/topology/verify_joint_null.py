#!/usr/bin/env python3
"""Exact simultaneous-quotient periods and complete-143 path controls.

No tiling search is performed. A path control is read from the previously
verified complete-tiling median replay.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json


def add(u,v): return u[0]+v[0],u[1]+v[1]
def sub(u,v): return u[0]-v[0],u[1]-v[1]
def mul(u,v):
    return u[0]*v[0]-u[1]*v[1],u[0]*v[1]+u[1]*v[0]+u[1]*v[1]
def scale(t,u): return t*u[0],t*u[1]
def norm(u): return u[0]*u[0]+u[0]*u[1]+u[1]*u[1]
def div(u,v): return scale(1/norm(v),mul(u,(v[0]+v[1],-v[1])))
def power(u,n):
    r=(F(1),F(0))
    for _ in range(n): r=mul(r,u)
    return r


UNITS=[power((F(0),F(1)),j) for j in range(6)]


def append_letter(stack,axis,n,modulus):
    n %= modulus
    if n and stack and stack[-1][0]==axis:
        n=(stack.pop()[1]+n)%modulus
    if n: stack.append((axis,n))


def prefixes(a,b,c,steps):
    z=(F(a,c),F(b,c))
    sa=b*pow(c,-1,a)%a
    sb=a*pow(c,-1,b)%b
    assert sa*sa%a==sb*sb%b==1
    wa=[];wb=[];u=(F(0),F(0))
    states=[((),())];positions=[u]
    for h,j in steps:
        ja=(j+h)%6
        append_letter(wa,ja%3,(-1 if ja>=3 else 1)*c*pow(sa,h,a),a)
        jb=j%6
        append_letter(wb,jb%3,(-1 if jb>=3 else 1)*c*pow(sb,h,b),b)
        u=add(u,scale(c,mul(power(z,h),UNITS[j])))
        states.append((tuple(wa),tuple(wb)));positions.append(u)
    assert states[-1]==(((0,c*c%a),),((0,c*c%b),))
    assert positions[-1]==(c*c,0)
    return states,positions


def in_difference_body(v,c,C):
    # T=conv(0,(c^2,0),C). In this basis T-T has inequalities
    # |r|<=1, |s|<=1, |r+s|<=1.
    s=v[1]/C[1]
    r=(v[0]-s*C[0])/(c*c)
    return max(abs(r),abs(s),abs(r+s))<=1


def plain(u): return [str(u[0]),str(u[1])]


def geometry_record(a,b,c,pi):
    z=(F(a,c),F(b,c))
    pi=tuple(map(F,pi))
    assert norm(pi)==c
    assert all(x.denominator==1 for x in div((F(a),F(b)),pi))
    A=b*(2*a+b);B=a*(a+2*b)
    C=scale(B,power(z,2))
    generator=scale(a*b,mul(z,pi))
    first=norm(generator);diameter=max(A,B,c*c)
    periods=[mul(generator,u) for u in UNITS]
    fits=[in_difference_body(v,c,C) for v in periods]
    exhaustive=3*first>diameter*diameter
    injective=first>diameter*diameter or (exhaustive and not any(fits))
    if c in (37,43): assert injective
    if c==7: assert not injective and any(fits)
    return {
        'N':(a+2*b)*(2*a+b),'tile':[a,b,c],
        'pi':plain(pi),'path_board_C':plain(C),
        'joint_period_generator':plain(generator),
        'minimum_nonzero_period_norm_squared':int(first),
        'next_shell_norm_squared_at_least':int(3*first),
        'board_diameter_squared':diameter*diameter,
        'six_shortest_periods':[{'vector':plain(v),'is_board_chord':f} for v,f in zip(periods,fits)],
        'first_shell_exhausts_possible_nonzero_chords':exhaustive,
        'no_nonzero_joint_period_is_board_chord':injective,
    },generator


def main():
    if not __debug__: raise SystemExit('Run without -O.')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--known-replay',type=Path,required=True)
    parser.add_argument('--out',type=Path)
    args=parser.parse_args()
    cases=[(5,3,7,(1,2)),(33,7,37,(3,4)),(35,13,43,(6,1))]
    result={'scope':'Necessary simultaneous-quotient path condition only; neither target is decided.',
            'geometric_periods':[],'canonical_word_controls':[]}
    for a,b,c,pi in cases:
        row,generator=geometry_record(a,b,c,pi)
        result['geometric_periods'].append(row)
        states,positions=prefixes(a,b,c,[(1,0)]*a+[(1,5)]*b)
        assert len(set(states))==len(states)
        result['canonical_word_controls'].append({
            'tile':[a,b,c],'steps':a+b,
            'both_boundary_words':'PASS',
            'joint_prefix_states_distinct':True,
            'scope':'The canonical word passes this necessary condition; no completion above it is asserted.'})
    raw=args.known_replay.read_bytes()
    source=json.loads(raw)
    result['actual_143_replay_sha256']=hashlib.sha256(raw).hexdigest()
    result['actual_143_paths']=[]
    _,generator=geometry_record(5,3,7,(1,2))
    for label in ('known','macro'):
        for path in source[label]['paths']:
            states,positions=prefixes(5,3,7,path['steps'])
            repeats=[]
            for j in range(len(states)):
                for i in range(j):
                    if states[i]==states[j]:
                        delta=sub(positions[j],positions[i])
                        coeff=div(delta,generator)
                        assert all(x.denominator==1 for x in coeff)
                        repeats.append({'prefix_indices':[i,j],
                                        'displacement':plain(delta),
                                        'joint_period_coefficients':plain(coeff)})
            result['actual_143_paths'].append({
                'control':label,'steps':len(path['steps']),
                'both_boundary_words':'PASS','simultaneous_null_subpaths':repeats,
                'complete_certificate_sha256':source[label]['source_sha256']})
    if args.out: args.out.write_text(json.dumps(result,indent=2)+'\n')
    for row in result['geometric_periods']:
        print(row['N'],'joint-period chord excluded:',row['no_nonzero_joint_period_is_board_chord'],
              'minimum norm squared:',row['minimum_nonzero_period_norm_squared'])
    for row in result['actual_143_paths']:
        print('actual143',row['control'],'common-null subpaths:',len(row['simultaneous_null_subpaths']))
    print('All exact identities and path controls PASS.')


if __name__=='__main__': main()
