"""Exact residual projections for terminal cuts, with a finite word replay."""
from collections import Counter
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
UNITS = ((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))


def add(p,q):
    return p[0]+q[0], p[1]+q[1]


def scale(k,p):
    return k*p[0], k*p[1]


def det(p,q):
    return p[0]*q[1]-p[1]*q[0]


def decode(code,r):
    digits = []
    for _ in range(r):
        code,t = divmod(code,12)
        digits.append(t)
    assert code==0
    return digits[::-1]


def word_from_codes(left,right,r):
    return decode(left,r)+[6*(t//6)+(t+3)%6 for t in reversed(decode(right,r))]


def projected_events(a,b,c,word):
    p = (0,0)
    events = [Counter() for _ in range(3)]
    for token in word:
        j = token%6
        segments = [(j,a),((j-1)%6,b)] if token<6 else [(j,c)]
        for k,length in segments:
            u = UNITS[k%3]
            events[k%3][det(u,p)] += length if k<3 else -length
            p = add(p,scale(length,UNITS[k]))
    return p,events


def width_obstruction(a,b,c,word):
    p,events = projected_events(a,b,c,word)
    if p!=(0,0):
        return True
    for support in events:
        active = 0
        for offset in sorted(support):
            active += support[offset]
            if active < 0 or not any((active-i*a)%b==0 for i in range(active//a+1)):
                return True
        assert active==0
    return False


def verify():
    cases = [(33,7,37,[5,6,7]), (35,13,43,[6,7])]
    counts = {}
    with tempfile.TemporaryDirectory() as tmp:
        binary = Path(tmp)/"word_join"
        subprocess.run(["c++","-O3","-std=c++17",str(HERE/"word_join.cpp"),"-o",str(binary)],check=True)
        for a,b,c,depths in cases:
            for r in depths:
                # 4*pi*area <= perimeter squared. pi>3.1, sqrt(3)>1.73.
                assert 1000*(2*r*c)**2 < 31*173*6*c*a*b
                run = subprocess.run([str(binary),*map(str,(a,b,c,r))],
                                     check=True,text=True,capture_output=True)
                count = 0
                for line in run.stdout.splitlines():
                    multiple,left,right = map(int,line.split())
                    assert multiple in (1,2)
                    assert width_obstruction(a,b,c,word_from_codes(left,right,r))
                    count += 1
                counts[c,2*r] = count
    assert counts=={(37,10):0,(37,12):0,(37,14):44,(43,12):0,(43,14):0}
    print("Terminal words surviving the additive test before projected widths:",counts)


if __name__ == "__main__":
    verify()
