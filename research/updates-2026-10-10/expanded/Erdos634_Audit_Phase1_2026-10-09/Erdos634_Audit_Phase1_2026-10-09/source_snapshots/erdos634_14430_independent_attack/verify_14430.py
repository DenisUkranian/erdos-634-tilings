#!/usr/bin/env python3
"""Exact arithmetic audit for F3, N=14430; NOT a tiling certificate.

Standard library only. Checks the canonical geometry, boundary semigroups,
directional-current witness, population congruences, two character charges,
and the finite arithmetic consequences of the gap lemmas proved in the note.
It does not certify geometric realizability or an impossibility proof.
"""
from fractions import Fraction as Q
from pathlib import Path
import json

A, B, C, N = 56, 9, 61, 14430

def mul(v, w):
    x, y = v
    u, t = w
    return (x*u-y*t, x*t+y*u+y*t)

def scale(s, v):
    return (s*v[0], s*v[1])

def sub(v,w):
    return (v[0]-w[0],v[1]-w[1])

def power(v, n):
    result = (Q(1),Q(0))
    for _ in range(n):
        result = mul(result,v)
    return result

def rotate_counts(j):
    result = [0,0,0]
    result[j%3] = 1 if j%6 < 3 else -1
    return result

def chi(v):
    return v[0]-v[1]+v[2]

def rows(length):
    result=[]
    for a in range(length//A+1):
        for b in range((length-A*a)//B+1):
            remainder=length-A*a-B*b
            if remainder % C == 0:
                result.append((a,b,remainder//C))
    return result

def main():
    assert C*C == A*A+A*B+B*B
    assert N == 3*(A+B)*(A+2*B)
    rho = (Q(0),Q(1))
    z = (Q(A,C),Q(B,C))
    O = (Q(0),Q(0))
    P = (Q(C*C),Q(0))
    T = scale(C*(A+2*B), power(z,3))
    side2 = scale(3*B*(A+B),mul(rho,power(z,2)))
    assert sub(T,P) == side2
    # Normalized area: 4*area/sqrt(3).
    area_normalized = P[0]*T[1]
    assert area_normalized == N*A*B
    lengths = [C*C,3*B*(A+B),C*(A+2*B)]
    word_tables = [rows(length) for length in lengths]
    short_min = min(x+y for x,y,z0 in word_tables[1])
    minimizers = [r for r in word_tables[1] if r[0]+r[1] == short_min]
    assert list(map(len, word_tables)) == [233,55,341]
    assert short_min == 12 and minimizers == [(0,12,27)]

    # Actual nonnegative orientation COUNTS, not positioned triangles.
    # Tuple: short height, chirality, rotation mod 6, population.
    # Convention of DIRECTIONAL_SUPPORT.md.
    witness = [
        (1,"A",3,61),
        (1,"B",3,122),
        (2,"A",0,6916),
        (2,"A",3,6990),
        (2,"A",2,121),
        (2,"B",1,147),
        (2,"B",4,73),
    ]
    currents = {}
    population = {}
    signed = {}
    def edge(h,j,length,multiplicity):
        vec = currents.setdefault(h,[0,0,0])
        sign = 1 if j%6 < 3 else -1
        vec[j%3] += sign*length*multiplicity

    for h,typ,j,count in witness:
        assert count >= 0
        population[h] = population.get(h,0)+count
        sv = signed.setdefault((h,typ),[0,0,0])
        rv = rotate_counts(j)
        for k in range(3):
            sv[k] += count*rv[k]
        if typ=="A":
            edge(h,j,A,count)
            edge(h-1,j+3,C,count)
            edge(h,j+5,B,count)
        else:
            edge(h,j,B,count)
            edge(h+1,j+2,C,count)
            edge(h,j+5,A,count)

    currents={h:v for h,v in currents.items() if any(v)}
    expected={0:[3721,0,0],2:[0,1755,0],3:[-4514,0,0]}
    assert currents == expected
    assert sum(population.values()) == N
    assert population == {1:183,2:14247}
    assert all(n%C == (N%C if h==2 else 0) for h,n in population.items())

    D = sum(chi(signed.get((h,"B"),[0,0,0])) -
            chi(signed.get((h,"A"),[0,0,0])) for h in population)
    Ds = sum((-1)**h * (chi(signed.get((h,"B"),[0,0,0])) -
                        chi(signed.get((h,"A"),[0,0,0]))) for h in population)
    assert (D,Ds) == (-182,-60)
    assert ((D+Ds)//2,(D-Ds)//2) == (-121,-61)
    assert sum(n for h,n in population.items() if h%2==0)%2 == 1
    assert sum(n for h,n in population.items() if h%2==1)%2 == 1

    # Consequences of the proved signed-current gap lemmas.
    # This finite calculation does not replace the proofs of those lemmas.
    external_tails=[n for n in range(1,N) if n%(2*C*C)==0]
    internal_lower=[n for n in range(1,N) if n%(C*C)==0 and n%2==1]
    assert external_tails == [7442]
    assert internal_lower == [3721,11163]
    assert [N-n for n in internal_lower] == [10709,3267]
    assert N-7442 == 6988
    max_occupied=1+(N-(N%C))//C
    assert max_occupied==237

    # Two gaps + 237 occupied levels would force these two supports.
    # Every height except 2 would then have 61 tiles, and height 2 has 34.
    # Both supports violate the independently derived parity charge.
    bands=[
        (list(range(-60,1))+list(range(2,56))+list(range(57,179))),
        (list(range(-183,-61))+list(range(-60,1))+list(range(2,56))),
    ]
    extreme_reports=[]
    for heights in bands:
        assert len(heights)==237 and 2 in heights
        pops={h:(34 if h==2 else 61) for h in heights}
        assert sum(pops.values())==N
        evens=sum(n for h,n in pops.items() if h%2==0)
        odds=sum(n for h,n in pops.items() if h%2==1)
        assert evens%2==odds%2==0  # Must both be odd in an actual tiling.
        extreme_reports.append({
            "minimum_height":min(heights),"maximum_height":max(heights),
            "even_height_population":evens,"odd_height_population":odds,
            "failure":"Both populations even; character requires both odd."
        })
    # <=1 gap: span <=236+1. Two gaps: <=236 occupied => span <=235+2.
    max_span=237

    # Consistency control from the repo's saved 4830 height audit.
    # Not a recheck of its full positioned geometry.
    control_pop={1:2883,2:1823,3:124}
    assert sum(control_pop.values())==4830
    assert all(n%31 == (4830%31 if h==2 else 0)
               for h,n in control_pop.items())
    assert control_pop[2]%2==1
    assert (control_pop[1]+control_pop[3])%2==1

    report={
        "status":"PASS",
        "scope":"Necessary-condition and formal-current audit; N=14430 remains undecided.",
        "tile":[A,B,C],"N":N,
        "canonical_top_eisenstein":[str(q) for q in T],
        "boundary_lengths_in_height_order_0_2_3":lengths,
        "normalized_area":str(area_normalized),
        "number_of_boundary_count_rows":list(map(len,word_tables)),
        "height_2_boundary_rows":word_tables[1],
        "minimum_short_edges_on_height_2_side":short_min,
        "minimum_rows":minimizers,
        "formal_orientation_witness":witness,
        "formal_populations":population,
        "directional_currents":currents,
        "characters":{"D":D,"D_star":Ds,"even":-121,"odd":-61},
        "external_gap_tail_counts":external_tails,
        "missing_height_1_lower_counts":internal_lower,
        "maximum_occupied_heights":max_occupied,
        "maximum_height_span_from_gap_and_parity_lemmas":max_span,
        "excluded_extreme_two_gap_supports":extreme_reports,
        "not_proved":[
            "Existence of a positioned tiling",
            "Nonexistence of a tiling",
            "A single-class exterior boundary",
            "Geometric realizability of the formal orientation witness"
        ],
    }
    path=Path(__file__).with_name("verification_14430.json")
    path.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({k:report[k] for k in (
        "status","scope","boundary_lengths_in_height_order_0_2_3",
        "minimum_short_edges_on_height_2_side","formal_populations",
        "external_gap_tail_counts","missing_height_1_lower_counts",
        "maximum_occupied_heights","maximum_height_span_from_gap_and_parity_lemmas"
    )},indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
