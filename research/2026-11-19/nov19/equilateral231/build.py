"""Retarget the positioned-current checker to the equilateral triangle of side 231."""
from pathlib import Path
import subprocess
import sys

source=Path(__file__).resolve().parent.parent/"iso329"
outdir=Path(sys.argv[1]).resolve()
outdir.mkdir(parents=True,exist_ok=True)
for name, old, new in [
    ("strip_replay","V{0,0},scale(329,transform),V{49,231}*transform","V{0,0},scale(231,transform),V{0,231}*transform"),
    ("segments","P{0,0},times(329,inv),mul({49,231},inv)},count,{329,259,259}","P{0,0},times(231,inv),mul({0,231},inv)},count,{231,231,231}")]:
    src=(source/(name+".cpp")).read_text()
    assert src.count(old)==1
    target=outdir/(name+".cpp")
    target.write_text(src.replace(old,new))
    subprocess.run(["c++","-std=c++17","-O3",str(target),"-o",str(outdir/name)],check=True)
