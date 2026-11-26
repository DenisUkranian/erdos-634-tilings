"""Recompute the signed charge census and enumerate all equality paths."""
import json
from pathlib import Path
import subprocess
import tempfile
from charged_cut import census, odd_source
from strip_starts import control,passes,path_jumps
from remote import inventories

HERE=Path(__file__).resolve().parent


def check():
    result={}
    with tempfile.TemporaryDirectory() as tmp:
        binary=Path(tmp)/"seam"
        subprocess.run(["c++","-O3","-std=c++17",str(HERE/"seam.cpp"),"-o",str(binary)],check=True)
        lines=subprocess.check_output([str(binary)],text=True).splitlines()
    for a,b,c,l,expected,minimum in [
        (33,7,37,3,[171,159,203,149,181,181],149),
        (35,13,43,5,[213,193,263,171,235,221],171)
    ]:
        d=a-b
        floor=census(a,b,c)
        assert [floor[key] for key in sorted(floor)]==expected
        local,attain=odd_source(a,b,c)
        assert local['axial']+c+d==minimum
        assert all(row[1]==(-c,0,0,c) and row[2][2]==0 for row in attain)
        assert list(inventories(a,b,c,1,-c,0,local['axial']-c))==[
            (a+b+3*l,(b,-l,a),(0,-l,l))]
        assert list(inventories(a,b,c,2,0,c,c))==[(c,(0,0,0),(0,0,c))]
        axis_one={(i,j) for i in range(l+1) for j in range(l+1) if (b*i+c*j)%a==0}
        assert axis_one=={(0,0),(l,l)}
        axis_two=[(i,j) for i in range(b+1) for j in range(l+1) if (i or j) and (b*i+c*j)%a==0]
        assert min(j for _,j in axis_two)*2>l
        words=[w for w in lines if len(w)==a+b+3*l and w.isdigit()]
        counts=next(list(map(int,row.split()))[1:] for row in lines if row.startswith(str(c)+" "))
        assert counts[-1]==len(set(words))==len(words)
        survivors={}
        for w in words:
            jumps=path_jumps(a,b,c,w)
            if passes(jumps,a,b):
                area=-sum(t*v for J in jumps for t,v in J.items())
                assert area%(a*b)==0
                population=area//(a*b)+a+b+l+c
                assert population%(2*c)==0
                survivors[w]=population
        assert set(survivors)=={'2'*a+'3'*l+'1'*l+'4'*l+'0'*b,
                                  '4'*l+'2'*a+'1'*l+'0'*b+'3'*l}
        result[str((a+2*b)*(2*a+b))]={"charged_leaf_by_parity_and_region":expected,
            "single_odd_source_middle_vertex_cost":local,
            "filter_counts":counts,"first_paths_and_middle_populations":survivors,
            "original_status":"OPEN"}
    assert odd_source(5,3,7)[0]['native']==23
    result["complete_143_controls"]={name:control(name) for name in ("known","macro")}
    return result


if __name__=="__main__":
    if not __debug__:
        raise SystemExit("Enable assertions.")
    print(json.dumps(check(),indent=2))
