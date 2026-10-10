#!/usr/bin/env python3
"""Run exactly this phase's two audit suites. No network or search solver."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parent
for script in ('check_universal_geometry.py','check_boundary_foundations.py'):
 subprocess.run([sys.executable,str(root/'code'/script)],cwd=root,check=True)
print('Phase 2 audit suites completed. Read scope limits in REPORT.md.')
