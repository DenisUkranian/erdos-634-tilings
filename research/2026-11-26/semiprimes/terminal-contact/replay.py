"""Run exact geometric controls and the terminal and nested-cut exclusions."""
from argparse import ArgumentParser
from pathlib import Path
import subprocess
import sys

from terminal import verify
from junction import verify as verify_junction
from remote import exclusions

HERE = Path(__file__).resolve().parent


def run(name):
    subprocess.run([sys.executable, "-u", str(HERE / name)], check=True)


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("The replay requires Python assertions.")
    parser = ArgumentParser()
    parser.add_argument("--independent", action="store_true",
                        help="also run the slower integer-tuple terminal-word enumeration")
    args = parser.parse_args()
    run("control143.py")
    run("native.py")
    run("patch5063.py")
    verify()
    for a, b, c, floor, expected in [(33, 7, 37, 123, [7, 7]), (35, 13, 43, 165, [14, 14])]:
        assert exclusions(a, b, c, 16, floor) == expected
        print("Nonnative unmatched floor", floor, "profiles tested per cut", expected, flush=True)
        verify_junction(a, b, c)
    run("review_junction.py")
    run("rare_core.py")
    if args.independent:
        run("review_terminal.py")
