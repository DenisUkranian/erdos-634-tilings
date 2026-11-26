"""Run the new geometry and the two inherited profile exclusions."""
from argparse import ArgumentParser
import json
from pathlib import Path
import subprocess
import sys

from controls import HERE

SOURCE = HERE.parents[2] / "2026-11-21/semiprimes"


def run(script,*args):
    subprocess.run([sys.executable, "-u", str(script), *map(str,args)], check=True)


def arithmetic():
    for a,b,c,R in [(33,7,37,45),(35,13,43,58)]:
        assert a*a+a*b+b*b==c*c
        N=(2*a+b)*(a+2*b)
        assert (N-N%c-c)//(2*c)==R
        for sigma in (-1,1):
            if c!=43:
                continue
            for o in (0,c*(1-2*sigma)):
                assert all((sigma*t+o)%(a-b) for t in range(1,17))
        assert (2*c)%(a-b) and c%(a-b)
        num,den=(43,222) if c==37 else (8,43)
        for blocks in ((2,3) if c==37 else (2,)):
            cap=num*(blocks*c)//den
            assert cap<a-b and (blocks*c+cap-1)//cap==6
        assert (N-N%c)//(14*c)==(6 if c==37 else 8)
    assert all((2*x)%43!=0 for x in range(1,43))
    assert 4*42**2*31==218736 and 2*2*42==168
    assert 218736+168+1==218905
    print("Ordinary occupied lift budgets: 45 and 58. Prior 5063 population schemes: 218905 -> 1.")


if __name__=="__main__":
    if not __debug__:
        raise SystemExit("Enable Python assertions for this replay.")
    parser=ArgumentParser()
    parser.add_argument("--full",action="store_true")
    args=parser.parse_args()
    arithmetic()
    for local in ("controls.py","moments.py","sections.py"):
        run(HERE/local)
    charged=SOURCE/"charged-branches"
    terminal=subprocess.run([sys.executable,str(charged/"verify_terminal_gate.py"),
                            *map(str,[charged/"terminal_3431_exact.json",charged/"terminal_5063_exact.json"])],
                            check=True,capture_output=True,text=True)
    results=json.loads(terminal.stdout)
    assert [r["rounded_bounds"]["1"]["minimum_tiles"] for r in results]==[185,301]
    assert results[1]["rounded_bounds"]["2"]["minimum_tiles"]==602
    print("Isolated-gate columns and charged polygon controls verified for both shapes.")
    if args.full:
        run(SOURCE/"replay.py")
        run(SOURCE/"global-closure-next/five-block-two-heights/replay_single_offset.py")
