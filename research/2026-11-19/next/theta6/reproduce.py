"""Verify the integer obstruction; --rebuild also regenerates the exhaustive pool."""
import argparse
from hashlib import sha256
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

here = Path(__file__).resolve().parent
source = here.parent/"alpha280mesh"
weights = here.parent/"theta6lp"
digest = "7e26641ac3db164d9cba1c1a38e7c7d075713d18132852e06e842e2dff0800a1"


def check_weights(pool):
    subprocess.run([sys.executable,str(weights/"verify.py"),str(pool),str(weights/"d729-weights.tsv.gz")],check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rebuild",action="store_true")
    args = parser.parse_args()
    check_weights(weights/"candidates.dat.gz")
    if not args.rebuild:
        return
    with TemporaryDirectory() as tmp:
        work=Path(tmp)
        env=os.environ.copy()
        for flag in ("EXACT_LATTICE","DUMP_CELLS"):
            env.pop(flag,None)
        solver=work/"mesh"
        subprocess.run(["g++","-std=c++20","-O3","-DWIDE_INIT","-DHALF_EDGES","-DMIRROR_CELLS","-I"+str(here.parent/"cubes/beta_shapes"),
                        str(source/"mesh.cpp"),"-lgmpxx","-lgmp","-o",str(solver)],check=True)
        for h,q in [(80,3),(30,18),(15,36),(7,54),(6,81)]:
            print(f"Checking angular window {h}, mesh {q}.",flush=True)
            if q==81:
                env["DUMP_CELLS"]=str(work/"cells")
            out=subprocess.check_output([str(solver),str(h),str(q),"125","3","500","0"],env=env,stderr=subprocess.STDOUT)
            assert out.splitlines()==(here/f"h{h}-q{q}.log").read_bytes().splitlines()
        lift=work/"lift"
        subprocess.run(["g++","-std=c++20","-O3",str(here/"lift_cells.cpp"),"-lgmpxx","-lgmp","-o",str(lift)],check=True)
        pool=work/"pool.dat"
        out=subprocess.check_output([str(lift),"729","180",str(pool),str(work/"cells")])
        assert out.splitlines()==(here/"lift.log").read_bytes().splitlines()
        assert sha256(pool.read_bytes()).hexdigest()==digest
        assert (work/"pool.dat.shapes").read_bytes()==(weights/"candidates.dat.shapes").read_bytes()
        print("Rebuilt all 146,434 candidates and the exact reference digest.",flush=True)
        check_weights(pool)


if __name__=="__main__":
    main()
