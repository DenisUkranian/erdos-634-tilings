"""Run the exact boundary-word checkpoint with standard Python."""
from pathlib import Path
import subprocess
import sys

if not __debug__:
    raise RuntimeError("Enable Python assertions for the replay.")
here = Path(__file__).resolve().parent
for args in (["nested.py"], ["remote.py"], ["control.py"], ["spectrum.py","--check"],
             ["inventory.py","--check"], ["audit.py"], ["strip_review.py"], ["rectangle.py"]):
    subprocess.run([sys.executable,*args],cwd=here,check=True)
print("PASS. Both original tiling counts remain OPEN.")
