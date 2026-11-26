"""Transverse component test on the previously proved staircase word list."""
from itertools import groupby
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "terminal-contact"))
from junction import Model


def check(a,b,c):
    rejected=[]
    total=0
    for word,population in Model(a,b,c).upper():
        width=0
        rows=[]
        for letter in word:
            if letter=="0":
                rows.extend([width]*a)
                width+=b
            elif letter=="1":
                width-=c
            else:
                rows.extend([width]*c)
        assert width==0 and len(rows)==c*c
        for column in sorted({0,*rows}):
            sections=groupby(rows,key=lambda w:w>column)
            lengths=[sum(1 for _ in block) for inside,block in sections if inside]
            bad=[n for n in lengths if all((n-i*a)%b for i in range(n//a+1))]
            if bad:
                rejected.append((population,column,bad[0]))
                break
        total+=1
    return total,sorted(rejected)


if __name__=="__main__":
    assert check(33,7,37)==(42,[])
    result=check(35,13,43)
    assert result==(109,[(1849,477,121),(1935,477,121),(2021,477,121)])
    print("5063 transverse section at depth 477+1/2: 3 of 109 words have a component of length 121.")
