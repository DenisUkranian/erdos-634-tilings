"""Integrate the hash-checked uniform-reduction snapshot; preserve Actions permissions."""
from pathlib import Path
import hashlib, json, lzma, subprocess, sys
HERE = Path(__file__).resolve().parent
root = Path(sys.argv[1]).resolve()
raw = b''.join((HERE / f'uniform{i:02}').read_bytes() for i in range(3))
if hashlib.sha256(raw).hexdigest() != 'd41f31225536792fcf4a0d9c068c270085d8894200bbe8287c4ddce54e66636f':
    raise ValueError('Uniform transport digest mismatch')
entries = json.loads(lzma.decompress(raw))
if len(entries) != 19:
    raise ValueError('Unexpected uniform source count')
def put(name, text):
    p = (root / name).resolve()
    if root not in p.parents or '.git' in p.relative_to(root).parts:
        raise ValueError('Unsafe path')
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')
for e in entries:
    if Path(e['path']).name != e['path']:
        raise ValueError('Unexpected source filename')
    data = e['content'].encode('utf-8')
    if len(data) != e['bytes'] or hashlib.sha256(data).hexdigest() != e['sha256']:
        raise ValueError('Uniform source mismatch: ' + e['path'])
    put('research/uniform-reduction/' + e['path'], e['content'])
put('verification/uniform-source-provenance.json', json.dumps({
    'source_date': '2026-09-30', 'verified_source_files': 19,
    'transport_sha256': hashlib.sha256(raw).hexdigest(),
    'entries': [{k:e[k] for k in ('path','bytes','sha256')} for e in entries],
    'pdf': 'Rebuilt from the included original paper.tex; not byte-identical to the earlier PDF.',
    'frozen_reports': 'Historical preparation reports remain unchanged; fresh replay occurs in a temporary copy.',
    'full_problem_solved': False
}, indent=2) + '\n')
p = root / 'scripts/build_publication_outputs.py'
t = p.read_text()
needle = '    if not args.pdfs_only:\n'
if t.count(needle) != 1:
    raise ValueError('Unexpected document builder layout')
t = t.replace(needle, '''        u=ROOT/'research/uniform-reduction';(u/'build').mkdir(exist_ok=True)
        for _ in range(2):run(['xelatex','-interaction=nonstopmode','-halt-on-error','-no-shell-escape','-output-directory=build','paper.tex'],u)
        (u/'paper.pdf').write_bytes((u/'build/paper.pdf').read_bytes())
        lines=[hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.name for f in sorted(u.iterdir()) if f.is_file() and f.name not in {'MANIFEST.sha256','SHA256SUMS.txt'}]
        (u/'MANIFEST.sha256').write_text('\\n'.join(lines)+'\\n')
''' + needle)
p.write_text(t)
p = root / 'scripts/verify_all.py'
t = p.read_text()
needle = "        reports['c_relations']=run("
if t.count(needle) != 1:
    raise ValueError('Unexpected verification coordinator layout')
t = t.replace(needle, '''        uw=work/'research/uniform-reduction'
        reports['uniform_reduction']=run(['verify_all.py'],uw)
        ur=json.loads((uw/'VERIFIED_RESULTS.json').read_text())
        if ur.get('result')!='ALL_SUPPLEMENTARY_CHECKS_PASSED' or ur.get('full_problem_solved') is not False:
            raise ValueError('Unexpected uniform-reduction scope/report')
        reports['uniform_reduction']['report']=ur
        print('UNIFORM_REDUCTION_SUPPLEMENTARY_CHECKS=PASS',flush=True)
''' + needle)
p.write_text(t)
put('README.md', '''# Erdős Problem 634 — congruent triangle tilings

**Denis Paliy** · Research with ChatGPT assistance · 30 September 2026

[Status](STATUS.md) · [Reproduce](REPRODUCIBILITY.md) · [Full-problem roadmap](docs/full-solution-roadmap.md) · [Citation](CITATION.cff)

Which positive integers N allow a triangle to be dissected into N congruent triangles? Reflections and arbitrary T-junctions are allowed.

**This repository contains partial research results, not a complete solution of Erdős problem 634.** The N=105 argument combines written geometric lemmas, published classification inputs, and separately replayed exact certificates. Universal arguments are not formally certified by running the code; the all-primes manuscript remains a candidate.

## Results and complete materials

| Result | Read and reproduce |
|---|---|
| Global exclusion of N=105 | [Written proof](research/n105/PROOF_N105.md), [PDF](research/n105/PROOF_N105.pdf), [four certificates and checking programs](research/n105/), [report](research/n105/VERIFIED_RESULTS.json). Covers both equilateral and both scalene candidates. |
| General scale restrictions and constructive bounds | [Proof](research/general-spectra/PROOF.md), [PDF](research/general-spectra/paper.pdf), [code and data](research/general-spectra/). Small multipliers remain unclassified in general. |
| Exact construction with 116,640 tiles | Tile (45,32,67), equilateral side 12,960: [macrocertificate](research/general-spectra/construction_116640.json), [all coordinates](research/general-spectra/tiles_116640.jsonl.gz), [checker](research/general-spectra/verify_certificate.py). |
| Squarefree obstructions and finite candidate reduction | [Proof](research/uniform-reduction/PROOF.md), [PDF](research/uniform-reduction/paper.pdf), [full supplementary package](research/uniform-reduction/). Includes the double-angle scale restriction and limits of linear boundary signatures. N=154 remains incomplete. |
| All-prime classification candidate | [Manuscript](paper/prime-case-candidate.pdf), [dependencies](docs/prime-case-dependencies.md), [c-relation audit](research/c-relations/audit.md). Universal geometric forcing still requires scrutiny. |
| Construction with 322 tiles and an infinite family | [Two-piece construction](docs/two-piece-construction.md), [PDF](paper/two-piece-construction.pdf), [certificate](data/tiling-322.json). |
| All five rational shapes at sufficiently large scales | [Two-annulus theorem](docs/universal-rational-scales.md) and [explicit seeds](docs/explicit-theta-seeds.md). Bounds depend on the fixed tile. |
| Complete fixed-tile analysis for (2,3,4) | [Classification](docs/first-tile-classification.md), including the [75-tile construction](docs/theta-75-construction.md). Prior results are credited. |
| Global exclusion of 21 | [Reduction](docs/n21-global-reduction.md) and [391-state certificate argument](docs/alpha-21-obstruction.md). Independently reproduces previously reported work. |

The N=105 root coverage is 120/120 for each scalene target, 15/15 for tile (5,19,21), and 1,788/1,788 for tile (7,13,15). Historical partial collars remain as regression fixtures, not as substitutes for these complete finite proofs.

## Verification

Python 3.11 or newer; the finite tests use the standard library:

```bash
python scripts/verify_all.py --jobs 2
```

Use ordinary Python, without `-O`, `-OO`, or `PYTHONOPTIMIZE`. The coordinator checks integrity and local links, replays the legacy suite and all four N=105 certificates, expands the 116,640-tile construction, and runs the uniform-reduction and c-relation tests in temporary copies. Reports record the scope of each check. See [REPRODUCIBILITY.md](REPRODUCIBILITY.md).

## Remaining question and attribution

A finite exception interval for each fixed tile is not a finite exception list over infinitely many tiles. Neither the necessary arithmetic spectra nor the existing finite membership search supplies the requested structural classification of all N. See the [roadmap](docs/full-solution-roadmap.md).

Denis Paliy directed the investigation; ChatGPT assisted with derivations, drafting and code. [Assistance disclosure](AI_USAGE_DISCLOSURE.md). No external referee acceptance, proof-assistant verification of the whole project, or priority is claimed. [Corrections](CONTRIBUTING.md) are welcome.

Software: [MIT](LICENSE). Original documentation and figures: [CC BY 4.0](LICENSE-DOCUMENTATION.md). Cited third-party work retains its own rights.
''')
put('docs/uniform-reduction.md', '''# Square-class obstructions and uniform finite reduction

The complete [source note](../research/uniform-reduction/PROOF.md), [PDF](../research/uniform-reduction/paper.pdf), and [supplementary code and records](../research/uniform-reduction/) are included.

The written argument excludes squarefree counts congruent to 19 modulo 24 or 35 modulo 120, subject to its explicit published classification and rationality inputs. It proves the necessary double-angle form N=(v²−u²)t² with t>=2, gives an explicit finite arithmetic overlist, and constructs formal direction-signature witnesses for scale-one W/beta candidates. These witnesses are not geometric tilings.

The stored N=154 investigation, tile (8,7,13) and target (91,91,154), is **INCOMPLETE**. No impossibility result follows from that stopped search. The new module does not validate the separate all-primes candidate and does not claim an all-N classification.

Run `python verify_all.py` from `research/uniform-reduction`, or the repository-wide coordinator. Frozen preparation reports describe their historical run; fresh integrated results are written under `audit-output/`.
''')
for name in ['STATUS.md','CHANGELOG.md','REPRODUCIBILITY.md','docs/open-frontier.md','docs/full-solution-roadmap.md']:
    p=root/name
    addition='''\n## Integrated continuation: uniform reduction (30 September 2026)

The [uniform-reduction note](LINK) and its complete source, test data, and separately checked positive witnesses are included in this publication. Its results are necessary spectra, two squarefree congruence obstructions, a finite candidate overlist, and formal boundary-signature witnesses. They are not a complete all-integer classification. The N=154 search is recorded as INCOMPLETE. The root verification coordinator now also replays all supplementary tests of this module in a disposable copy. Historical reports are retained with their original preparation scope.
'''.replace('LINK','uniform-reduction.md' if name.startswith('docs/') else 'docs/uniform-reduction.md')
    p.write_text(p.read_text()+addition)
workflow_dir=root/'.github/workflows'
if workflow_dir.exists():
    import shutil
    shutil.rmtree(workflow_dir)
subprocess.run(['git','restore','--source=47331354525e35515858ef96740866e1d4b3c300','--staged','--worktree','--','.github/workflows'],cwd=root,check=True)
print('UNIFORM_SOURCE_HASHES=PASS',len(entries),flush=True)
print('WORKFLOW_TREE_PRESERVED_FROM_BASE',flush=True)
