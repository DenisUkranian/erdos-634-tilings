"""Locate the unchanged, unrestricted geometry and corner implementations."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[5]
CONTINUATION = ROOT / 'research/2026-11-20/semiprimes/continuation'
BASE_DIR = CONTINUATION / 'global-endpoints/integer'
CORNER_DIR = CONTINUATION / 'vertex-phase'
for directory in (BASE_DIR, CORNER_DIR):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

import global_core_sat as core
from corner_oracle import CornerOracle, and_, or_, angular_groups
from corner_search import make_search_class, GracefulResourceStop

