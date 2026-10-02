"""Check the fixed package manifest without regenerating it."""
from hashlib import sha256
from pathlib import Path
import json


def main():
    root=Path(__file__).resolve().parent
    entries=json.loads((root/'manifest.json').read_text())['sha256']
    for name,expected in entries.items():
        path=(root/name).resolve()
        if root not in path.parents or not path.is_file():
            raise ValueError(f'Invalid or missing manifest path: {name}')
        actual=sha256(path.read_bytes()).hexdigest()
        if actual!=expected:
            raise ValueError(f'Hash mismatch: {name}')
    print(json.dumps({'status':'PASS','files_checked':len(entries)}))

if __name__=='__main__':main()
